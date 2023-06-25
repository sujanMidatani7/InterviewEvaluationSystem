# Interview Question Generator

This project aims to generate interview questions based on a user's resume, desired role, and experience. It utilizes a language model to generate relevant interview questions.

## Requirements

- Python 3.7 or above
- Install the required libraries by running the following command:

pip install -r requirements.txt

## Usage

1. Prepare the user's resume details, desired role, and relevant experience.

2. Update the `.env` file with your desired configuration.

3. In the `main.py` file, call the `generate_questions` function with the appropriate inputs:

  - `Resume_deatails` extracted from `Resume Deatails Extractor` mention before.
  - `role` role of the job user applied for
  - `experience` how much experience did user have in the mentioned field

The generated interview questions will be displayed on the console.

## Code Documentation

For detailed documentation of the code and its functions, please refer to the source code comments.

- `generate_questions(resume_details, role='', experience='')`: Generates interview questions based on the given resume, desired role, and experience.

## Libraries Used

- `langchain`: A library that provides tools for working with language models and prompt generation.
- `dotenv`: A library for loading environment variables from a `.env` file.



