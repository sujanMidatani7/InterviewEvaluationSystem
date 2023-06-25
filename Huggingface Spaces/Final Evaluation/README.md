## Final Evaluation

This code provides a function finalGradingPrompt that performs final evaluation and grading of an interview based on the provided inputs. 
The function takes the following parameters:

`resume_summary`: A JSON summary of the interviewee's performance in the interview.

`role`: The role the interviewee applied for.

`exp`: The experience of the interviewee in the applied role.

`ires`: A list of evaluation records in CSV format, containing questions answered with grades, timestamps, and plagiarism scores.

The function utilizes the OpenAI GPT-3.5 Turbo language model for generating the final evaluation. 

It uses the guidance library to interact with the model and provide a guided prompt for generating the evaluation.

## Usage

The code also includes a function `get_shape` that takes a `CSV file`, `resume_summary`, `role`, and `experience` as input.

It reads the CSV file, drops any empty rows, and calls the `finalGradingPrompt` function to obtain the final evaluation. 

The evaluation is then returned as the output.

## Dependencies

Please ensure that you have the necessary dependencies installed in your environment before running this code. The required dependencies are as follows:

`guidance`: This library provides an interface to interact with the OpenAI GPT-3.5 Turbo model.

`pandas`: This library is used for reading and manipulating CSV data.

`dotenv`: This library is used for loading environment variables (not used in the provided code snippet).

To use this code, you will also need access to an OpenAI API key. Make sure to set the API key in your environment variables or in a `.env` file before running the code.

