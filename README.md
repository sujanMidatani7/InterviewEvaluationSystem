# Interview Evaluation System
This project is a web application that allows users to upload their resume PDF, role and experience and get evaluated on their interview skills. The project uses several APIs from Hugging Face Spaces and Pinecone to perform the following steps:

- Extract details from the resume using the `Resume Details Extractor API`.

- Generate 10 questions based on the extracted details using the `Resume Details to Questions Generator API`.

- Convert each question from text to speech using the `Speech Recognition` module in Python and play it for the user.

- Record an audio file of the answer for each question and upload it to the interface.

- Convert the audio file to text using the `Speech to Text API` and use it as the answer.

- Evaluate each question and answer using the `Individual Question Evaluation API` and get two outputs: `grading and grading measures`.

- Store each `question` as an `index` and its `embedding and evaluation` as `metadata` in a `Pinecone index` using the Pinecone Python SDK.

- Retrieve all the 10 questions data from Pinecone and send it to the `Final Grading API` to get the final grading for the interviewee.
- Display the evaluation results to the user.

## Use Case Diagram
  ![image](https://github.com/sujanMidatani7/InterviewEvaluationSystem/assets/105052933/c36c8a77-75c9-4302-9193-024e06c0969e)

## Requirements

. Python 3.7 or higher

. Flask

. Speech Recognition

. Pinecone

. Requests

## Installation

To install the required packages, run:

`pip install -r requirements.txt`


## Usage
To run the web application, run:

python app.py



You will see a form where you can upload your resume PDF, role and experience. After submitting the form, you will be redirected to a page where you can listen to the questions and record your answers. After answering all the questions, you will see your evaluation results.

## Source Codes

The source codes for each API used in this project are available in the `Huggingface spaces folder` in this repository. You can also find them on Hugging Face Spaces using the links provided in the folder.

