from flask import Flask, request, render_template_string, send_file, render_template, url_for
import json
import pinecone as pc
import openai
from werkzeug.utils import secure_filename
from gradio_client import Client
from gtts import gTTS
import os
from dotenv import load_dotenv

load_dotenv()
role = ''
experience = ''
question = ''
json_dict = ''

csv_data = [[]]
app = Flask(__name__, static_folder='static')


pc.init(api_key=os.getenv("API_KEY"), environment=os.getenv("ENVIRONMENT"))


def gen_embed(text):
    response = openai.Embedding.create(
        input=text,
        engine="text-embedding-ada-002")
    return response['data'][0]['embedding']


def finalizePC():
    index = pc.Index('ques-ans')
    res = index.query(
        vector=[0]*1536,
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


def index(ques, ansemb, meta):

    # Upsert vector to Pinecone
    pc.Index('ques-ans').upsert([(str(ques), list(ansemb), meta)])
    # if '10' in ques:

    # start_server(webio_view(/),port=8000)

    return True


def extract_resume_details(pdf_file):
    client = Client("https://sujanmidatani-resume-details-extractor.hf.space/")
    result = client.predict(pdf_file, api_name="/predict")
    with open(result, "r", encoding='utf-8') as f:
        return f.read()


def question_to_audio(question):
    tts = gTTS(text=question, lang='en')
    audio_file = question+'.mp3'
    tts.save(audio_file)
    return audio_file


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
    # Extract the evaluation result from the tuple
    evaluation_result = result[0]
    return grading_measures, evaluation_result
# @app.route('/vinay', methods=['POST'])


def vinay():
    finalizePC()
    csv_file = csv_data
    # Get the JSON dictionary, role, and experience from the form

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

    return result.split("\n")


def questions_generator(resume_details, rol, experienc):
    global json_dict
    json_dict = resume_details
    global role
    role = rol
    global experience
    experience = experienc

    client = Client(
        "https://sujanmidatani-resume-details-to-questions.hf.space/")
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
    return zip(questions, audio_files), len(questions)


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        pdf_file = request.files['pdf_file']
        role = request.form.get('role')
        experience = request.form.get('experience')
        pdf_file.save(secure_filename(pdf_file.filename))
        resume_details = extract_resume_details(pdf_file.filename)
        result, total_questions = questions_generator(
            resume_details, role, experience)
        return render_template_string('''
    
    <link rel="stylesheet" type="text/css" href="{{ url_for('static', filename='style.css') }}">
    <h1>Generated Questions</h1>
    <form action="/submit" method="post">
        {% for question, audio_file in result %}
        <div class="question-block">
            <p>{{ question }}</p>
            <audio controls>
                <source src="{{ url_for('serve_audio', filename=audio_file) }}" type="audio/mp3">
                Your browser does not support the audio element.
            </audio>
            <a href="/record?question={{ question }}">Record Answer</a>
        </div>
        {% endfor %}
        {% if result %}
        <input type="submit" value="Submit Answers">
        {% endif %}
    </form>
    <a href="/">Back</a>

''', result=result, total_questions=total_questions)

    return '''
        <html>
        <head>
            <title>Interview Simulation System</title>
             <style>
                .question-block {
  margin-bottom: 20px;
  border: 1px solid #ddd;
  padding: 10px;
  border-radius: 5px;
  background-color: #fff;
  box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1);
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
  box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1);
}

input[type="submit"] {
  padding: 10px 20px;
  border: none;
  background-color: #4CAF50;
  color: #fff;
  cursor: pointer;
  border-radius: 5px;
  font-size: 16px;
}

input[type="submit"]:hover {
  background-color: #45a049;
}

input[type="file"] {
  margin-bottom: 10px;
}

input[type="text"] {
  padding: 10px;
  width: 100%;
  margin-bottom: 10px;
}

h1 {
  text-align: center;
  margin-bottom: 30px;
}

a {
  display: block;
  text-align: center;
  margin-top: 20px;
}

label {
  display: block;
  text-align: left;
   
  font-weight: bold;
}

            </style>
        </head>
        <body>
        <form method="post" enctype="multipart/form-data">
            <h1>Interview Evaluation System</h1>
            <label for="pdf_file">Upload Resume</label>
            <input type="file" name="pdf_file" id="pdf_file">
            <input type="text" name="role" placeholder="Enter Role">
            <input type="text" name="experience" placeholder="Enter Experience">
            <input type="submit" value="start Interview">
        </form>
        </body>
        </html>
    '''


@app.route('/submit', methods=['POST'])
def submit_answers():

    result = vinay()
    return render_template('result1.html', final_grading=result)


@app.route('/result')
def show_result():
    result = request.args.get('result')
    return render_template('result1.html', result=result)


@app.route('/record')
def record():
    global question
    question = request.args.get('question')

    return render_template('record.html', question=question)


print(question)


@app.route('/audio/<path:filename>')
def serve_audio(filename):
    return send_file(filename, mimetype='audio/mp3')


@app.route('/upload', methods=['POST'])
def upload():
    print("question from record", question)
    print(role)
    file = request.files['audio']
    request.files['audio'].save(file.filename)
    client = Client("https://sujanmidatani-speechtotext.hf.space/")
    result = client.predict(
        # str (filepath or URL to file) in 'audio' Audio component
        file.filename,
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
    answ_embed = gen_embed(answer)
    meta_d = {"score": json_data[list(json_data.keys())[-1]]["score"]}

    index(ques_id, answ_embed, meta_d)

    return render_template('index1.html')


# if __name__ == '__main__':
#     app.run(debug=True)
