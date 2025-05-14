#!/usr/bin/env python
import argparse
import warnings
from resume_crew.crew import ResumeCrew


warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

def run(job_url=None, company_name=None, resume_file=None, llm_model=None):
    parser = argparse.ArgumentParser(description="Run the resume optimization crew.")
    parser.add_argument("-j", "--job_url", type=str, help="Job URL", default="https://example.com/vacature/data-engineer-llm/JR12345/")
    parser.add_argument("-c", "--company_name", type=str, help="Company Name", default="ExampleCorp")
    parser.add_argument("-f", "--resume_file", type=str, help="Resume File Path", default="/path/to/default/resume.pdf")
    parser.add_argument("-m", "--llm_model", type=str, help="LLM Model", default="gpt-3.5-turbo")
    args = parser.parse_args()
    inputs = {
        'job_url':  job_url or args.job_url,
        'company_name': company_name or args.company_name
    }
    resume_file = resume_file or args.resume_file
    llm_model = llm_model or args.llm_model
    ResumeCrew(resume_file, llm_model).crew().kickoff(inputs=inputs)
if __name__ == "__main__":
    run()
