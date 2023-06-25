# Resume Text Extraction

This project aims to extract relevant information from a resume text using a combination of PDF parsing and language models. It utilizes the `PyPDF2` library to extract text from a PDF file and the `langchain` library for information extraction using language models.

## Requirements

- Python 3.7 or above
- Install the required libraries by running the following command:

pip install -r requirements.txt


## Usage

1. Place your resume in PDF format in the project directory.

2. Update the `.env` file with your desired configuration.

3. Run the `main.py` file to extract information from the resume:
        This will extract the text from the PDF file, process it using the language model, and generate a JSON file containing the extracted attributes.

4. The extracted information will be available in the generated JSON file, which can be further processed or used for various purposes.

## Code Documentation

For detailed documentation of the code and its functions, please refer to the source code comments.

- `gen_text(pdf_file)`: Extracts text from a PDF file and returns the extracted text.
- `context_extracter(text)`: Extracts relevant information from a given text using a language model.

## Libraries Used

- `PyPDF2`: A library for working with PDF files, used to extract text from the PDF document.
- `langchain`: A library that provides tools for working with language models and information extraction.
- `kor`: A library that provides methods for creating extraction chains for extracting structured data from text.
- `dotenv`: A library for loading environment variables from a `.env` file.

