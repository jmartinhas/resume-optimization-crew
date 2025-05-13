#!/usr/bin/env python
import sys
import warnings
from config import JOB_URL, COMPANY_NAME
from resume_crew.crew import ResumeCrew

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

def run():
    """
    Run the resume optimization crew.
    """
    inputs = {
        'job_url': JOB_URL,
        'company_name': COMPANY_NAME
    }
    ResumeCrew().crew().kickoff(inputs=inputs)

if __name__ == "__main__":
    run()
