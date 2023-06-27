from flask import Flask, request, render_template_string, send_file, render_template
import json
import pinecone as pc
from pywebio import start_server
from pywebio.input import input, TEXT, NUMBER
from pywebio.output import put_text
from pywebio.platform.flask import webio_view
from pywebio import STATIC_PATH

import openai
import speech_recognition as sr
from werkzeug.utils import secure_filename
from gradio_client import Client
from gtts import gTTS

# Initialize Flask app
app = Flask(__name__)

# Set OpenAI API Key

# Set Pinecone API key and environment
pc.init(api_key="", environment='')

# Initialize global variables
role = ''
experience = ''
question = ''
json_dict = ''
csv_data = [[]]

# Define the route to generate an embedding for the input text using OpenAI
def gen_embed(text):
    response = openai.Embedding.create(
        input=text,
        engine="text-embedding-ada-002"
    )
    return response['data'][0]['embedding']

# Query Pinecone index to retrieve all question-answer pairs and store them in a CSV file
def finalizePC():
    index = pc.Index('ques-ans')
    res = index.query(
        vector=[0] * 1536,
        top_k=index.describe_index_stats()['total_vector_count'],
        include_metadata=True,
    )
    csv_file = []
    print(res['matches'])
    for i in res['matches']:
        a = (str(i).split(","))[1]
        csv_file.append([i['id'], a])
    global csv_data
    csv_data = csv_file

# Index a question-answer pair in Pinecone and start the web server for the Vinay route if the question contains '10'
def index(ques, ansemb, meta):
    # Upsert vector to Pinecone
    pc.Index('ques-ans').upsert([(str(ques), list(ansemb), meta)])

    if '10' in ques:
        finalizePC()
        vinay(role, experience)
        start_server(webio_view(vinay), port=8000)

    return True

# Extract details from a resume PDF file using the Resume Details Extractor model
def extract_resume_details(pdf_file):
    client = Client("https://sujanmidatani-resume-details-extractor.hf.space/")
    result = client.predict(pdf_file, api_name="/predict")
    with open(result, "r", encoding='utf-8') as f:
        return f.read()

# Convert a question to an audio file using the gTTS library
def question_to_audio(question):
    tts = gTTS(text=question, lang='en')
    audio_file = question + '.mp3'
    tts.save(audio_file)
    return audio_file

# Evaluate a question and answer pair using the Question Evaluation model
def question_eval(questi, answer):
    global question
    question = questi
    client = Client("https://sujanmidatani-questioneval.hf.space/")
    result = client.predict(
        question,  # str in 'question' Textbox component
        answer,  # str in 'answer' Textbox component
        role,  # str in 'role' Textbox component
        experience,  # str in 'exp' Textbox component
        api_name="/predict"
    )
    grading_measures = result[1]  # Extract the grading measures from the tuple
    evaluation_result = result[0]  # Extract the evaluation result from the tuple
    return grading_measures, evaluation_result

# Route for the Vinay endpoint
@app.route('/vinay', methods=['POST'])
def vinay(role, experience):
    csv_file = csv_data

    # Get the JSON dictionary, role, and experience from the form
    role = role
    experience = experience

    client = Client("https://sujanmidatani-finalgrading.hf.space/")
    result = client.predict(
        csv_file,  # str in 'csv_file' FileUpload component
        json_dict,  # str in 'resume' Textbox component
        role,  # str in 'role' Textbox component
        experience,  # str in 'experience' Textbox component
        api_name="/predict"
    )

    print(result)

    index = pc.Index('ques-ans')
    index.delete(delete_all=True)

    return render_template('result1.html', result=result)

# Generate questions from resume details using the Resume Details to Questions model
def questions_generator(resume_details, rol, experienc):
    global json_dict
    json_dict = resume_details
    global role
    role = rol
    global experience
    experience = experienc

    client = Client("https://sujanmidatani-resume-details-to-questions.hf.space/")
    result = client.predict(
        resume_details,  # str in 'resume' Textbox component
        role,  # str in 'role' Textbox component
        experience,  # str in 'experience' Textbox component
        api_name="/predict"
    )
    questions = result.strip('][').split("', '")[1:]
    audio_files = []
    for question in questions:
        audio_file = question_to_audio(question)
        audio_files.append(audio_file)
    return zip(questions, audio_files)

# Home route
@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        pdf_file = request.files['pdf_file']
        role = request.form.get('role')
        experience = request.form.get('experience')
        pdf_file.save(secure_filename(pdf_file.filename))
        resume_details = extract_resume_details(pdf_file.filename)
        result = questions_generator(resume_details, role, experience)
        return render_template_string('''
    <h1>Generated Questions</h1>
    {% for question, audio_file in result %}
    <div class="question-block">
        <p>{{ question }}</p>
        <audio controls>
            <source src="{{ url_for('serve_audio', filename=audio_file) }}" type="audio/mp3">
            Your browser does not support the audio element.
        </audio>
        <form action="/record" method="post">
            <input type="hidden" name="question" value="{{ question }}">
            <input type="submit" value="Record Answer">
        </form>
    </div>
    {% endfor %}
    <a href="/">Back</a>
''', result=result)

    return '''
        <html>
        <head>
            <title>Resume Questions Generator</title>
            <style>
                .question-block {
                    margin-bottom: 20px;
                    border: 1px solid #ddd;
                    padding: 10px;
                    border-radius: 5px;
                    background-color: #fff;
                    box-shadow: 0px 0px 10px rgba(0,0,0,0.1);
                }
                audio {
                    margin-top: 10px;
                    width: 100%;
                }
                body {
                    font-family: Arial, sans-serif;
                    margin: 0;
                    padding: 0;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    height: 100vh;
                    background-color: #f0f0f0;
                }
                form {
                    text-align: center;
                    padding: 20px;
                    border: 1px solid #ddd;
                    border-radius: 10px;
                    background-color: #fff;
                    width: 50%;
                    box-shadow: 0px 0px 10px rgba(0,0,0,0.1);
                }
                input[type="file"],
                input[type="text"] {
                    width: 100%;
                    padding: 10px;
                    margin-bottom: 20px;
                    border-radius: 5px;
                    border: 1px solid #ddd;
                }
                input[type="submit"] {
                    padding: 10px 20px;
                    border: none;
                    border-radius: 5px;
                    background-color: #007BFF;
                    color: #fff;
                    cursor: pointer;
                    transition: background-color 0.5s ease;
                }
                input[type="submit"]:hover {
                    background-color: #0056b3;
                }
                h1 {
                    text-align: center;
                    color: #333;
                }
                p {
                    text-align: center;
                    color: #666;
                }
                a {
                    display: block;
                    text-align: center;
                    margin-top: 20px;
                    color: #007BFF;
                    text-decoration: none;
                }
            </style>
        </head>
        <body>
            <form method="POST" enctype="multipart/form-data">
                <input type="file" name="pdf_file" required>
                <input type="text" name="role" placeholder="Role" required>
                <input type="text" name="experience" placeholder="Experience" required>
                <input type="submit" value="Generate Questions">
            </form>
        </body>
        </html>
    '''

# Serve audio files
@app.route('/audio/<path:filename>')
def serve_audio(filename):
    return send_file(filename, mimetype='audio/mp3')

# Record route
@app.route('/record', methods=['POST'])
def record():
    global question
    question = request.form['question']
    return render_template('record.html', question=question)

# Upload route
@app.route('/upload', methods=['POST'])
def upload():
    print("question from record", question)
    print(role)
    file = request.files['audio']
    request.files['audio'].save(file.filename)
    client = Client("https://sujanmidatani-speechtotext.hf.space/")
    result = client.predict(
        file.filename,  # str (filepath or URL to file) in 'audio' Audio component
        api_name="/predict"
    )

    # Retrieve the text output from the response
    answer = result

    # print(answer)
    grading_measures, evaluation_result = question_eval(question, answer)
    with open(evaluation_result, 'r') as file:
        json_data = json.load(file)

    # Save JSON contents in a variable
    print(json_data[list(json_data.keys())[-1]]["score"])
    print("-------", grading_measures)
    print("=========", evaluation_result)
    # print(grading_measures)
    ques_id = question
    ansemb = gen_embed(answer)
    meta = {"grade": json_data[list(json_data.keys())[-1]]["score"]}
    index(ques_id, ansemb, meta)
    return render_template('result.html', grading_measures=grading_measures, evaluation_result=evaluation_result)

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
