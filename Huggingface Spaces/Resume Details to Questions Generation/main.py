from langchain.chains import LLMChain
from langchain.llms import OpenAI
from dotenv import load_dotenv
from langchain.prompts.prompt import PromptTemplate

load_dotenv() 

def generate_questions(resume_details, role='', experience=''):
    """
    Generates interview questions based on the given resume, desired role, and experience.

    Args:
        resume_details (str): The user's resume details.
        role (str, optional): The role the user wants to join. Defaults to ''.
        experience (str, optional): The user's relevant experience. Defaults to ''.

    Returns:
        list: A list of generated interview questions.
    """
    _PROMPT_TEMPLATE = """
    this is the resume of user:
    {resume_details}
    here is the role he wants to join in:
    {role}
    Based on the following experience:
    {experience}
    What are your interview questions for the given user resume and the role he wants to join in with that experience?
    generate number of questions = {questions}!
    """
    PROMPT = PromptTemplate(input_variables=["resume_details", "role", "experience", "questions"], template=_PROMPT_TEMPLATE)
  
    llm1 = OpenAI(model_name="text-davinci-003", temperature=0)
    chain = LLMChain(llm=llm1, prompt=PROMPT)
    prompt = chain.predict_and_parse(
        resume_details=resume_details,
        role=role,
        experience=experience,
        questions=10
    )
    return prompt.split('\n')
