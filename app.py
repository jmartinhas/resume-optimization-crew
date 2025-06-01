from json import load
import streamlit as st
import os
from src.utils.output_handler import capture_output
from src.utils.md2pdf import st_md2pdf
from src.utils.json2pdf import json_to_pdf
from resume_crew.main import run
from resume_crew.models import CompanyResearch, JobRequirements, ResumeOptimization

def validate_non_empty(st_field, field_name):
    if not st_field:
        return False, f"{field_name} is required"
    return True, ""

def validate_url(st_field, field_name):
    if not st_field:
        return False, f"{field_name} is required"
    if st_field.startswith("http"):
        return True, ""
    return False, f"Please enter a valid URL in {field_name}"

# Initialize session state
if 'form_submitted' not in st.session_state:
    st.session_state.form_submitted = False
# Initialize validation summary
if 'validation_messages' not in st.session_state:
    st.session_state.validation_messages = []

def get_validation_status():
    """Get detailed validation status for all fields"""
    validation_messages = []
    # Check each field and collect validation messages
    if not st.session_state.get('job_url_valid', False):
        if st.session_state.get('job_url', ''):
            is_valid, message = validate_url(st.session_state.job_url, "Job Url")
            if not is_valid:
                validation_messages.append(message)
        else:
            validation_messages.append("Job Url is required")
    if not st.session_state.get('company_name_valid', False):
        if st.session_state.get('company_name', ''):
            is_valid, message = validate_non_empty(st.session_state.company_name, "Company Name")
            if not is_valid:
                validation_messages.append(message)
        else:
            validation_messages.append("Company Name is required")
    if not st.session_state.get('resume_file_valid', False):
        if st.session_state.get('resume_file', ''):
            is_valid, message = validate_non_empty(st.session_state.resume_file, "Resume File")
            if not is_valid:
                validation_messages.append(message)
        else:
            validation_messages.append("Resume File is required")
    return validation_messages

#--------------------------------#
#         Streamlit App          #
#--------------------------------#
# Configure the page
st.set_page_config(
    page_title="Resume Optimizer",
    page_icon="🕵️‍♂️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Logo
st.logo(
    "https://cdn.prod.website-files.com/66cf2bfc3ed15b02da0ca770/66d07240057721394308addd_Logo%20(1).svg",
    link="https://www.crewai.com/",
    size="large"
)

# Main layout
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.title("🔍 :red[CrewAI] Resume Analyzer", anchor=False)

with st.sidebar: 
    st.divider()
    llm_model = st.selectbox("Select Model:", ["gpt-4o-mini","o1"])

# Create two columns for the input section
input_col1, input_col2, input_col3 = st.columns([1, 3, 1])
with input_col2:
    st.divider()

col1, col2, col3 = st.columns([1, 5, 1])
with col2:
    with st.form("my_form"):
        st.markdown("### ⚙️ Input Parameters")
        st.write("")
        job_url = st.text_input("Job URL", placeholder="Enter the job posting URL", key="job_url")
        if job_url:  # Only validate if there's input
            is_valid, message = validate_url(job_url, "Job URL")
            st.session_state.job_url_valid = is_valid
            if not is_valid:
                st.error(message)
            else:
                st.success("Valid job url!")
        else:
            st.session_state.job_url_valid = False

        company_name = st.text_input("Company Name", placeholder="Enter the company name", key="company_name")
        if company_name:  # Only validate if there's input
            is_valid, message = validate_non_empty(company_name,"Company Name")
            st.session_state.company_name_valid = is_valid
            if not is_valid:
                st.error(message)
            else:
                st.success("Valid Company Name!")
        else:
            st.session_state.company_name_valid = False
        
        resume_file = st.file_uploader("Upload Resume", help="Upload your resume", key="resume_file")
        if resume_file:  # Only validate if there's input
            is_valid, message = validate_non_empty(resume_file, "Resume File")
            st.session_state.resume_file_valid = is_valid
            if not is_valid:
                st.error(message)
            else:
                st.success("Valid Resume File!")
        else:
            st.session_state.resume_file_valid = False

        if st.form_submit_button("🚀 Optimize Resume"):
        # Get validation messages
            validation_messages = get_validation_status()
            if not validation_messages:
                st.success("Form submitted successfully!")
                st.session_state.form_submitted = True
            else:
                st.error("Please fix the following validation errors:")
                for message in validation_messages:
                    st.error(f"• {message}")
        submitted = False
        if submitted:            
            path = os.path.join("input", resume_file.name)
            with open(path, "wb") as f:
                f.write(resume_file.getvalue())

            with st.status("🤖 Analyzing...", expanded=True) as status:
                try:
                    # Create persistent container for process output with fixed height.
                    process_container = st.container(height=500, border=True)
                    output_container = process_container.container()
                    
                    # Single output capture context.
                    with capture_output(output_container):
                        
                        result = run(job_url=job_url, company_name=company_name, 
                                    resume_file=resume_file.name, llm_model=llm_model)
                        status.update(label="✅ Analysis completed!", state="complete", expanded=False)
                except Exception as e:
                    status.update(label="❌ Error occurred", state="error")
                    st.error(f"An error occurred: {str(e)}")
                    st.stop()
    
    if os.path.isfile("output/company_research.md"):
        md_content = CompanyResearch.json_to_md()

        st.divider()
        download_col1, download_col2, download_col3 = st.columns([1, 2, 1])
        with download_col2:
            st.markdown("### 📥 Download MarkDown Company Research Report")
            
            # Download as Markdown
            st.download_button(
                label="Download MarkDown Company Report",
                data=md_content.encode('utf-8'),
                file_name="output/company_research.md",
                mime="application/octet-stream",
                help="Download the company research report in Markdown format"
            )
    
    if os.path.isfile("output/job_analysis.md"):
        md_content = JobRequirements.json_to_md()
        st.divider()
        download_col1, download_col2, download_col3 = st.columns([1, 2, 1])
        with download_col2:
            st.markdown("### 📥 Download MarkDown Job Analysis Report")
            
            # Download as Markdown
            st.download_button(
                label="Download Job Analysis Report",
                data=md_content.encode('utf-8'),
                file_name="output/job_analysis.md",
                mime="application/octet-stream",
                help="Download the job analyis report"
            )
    if os.path.isfile("output/resume_optimization.md"):
        md_content = ResumeOptimization.json_to_md()
        st.divider()
        download_col1, download_col2, download_col3 = st.columns([1, 2, 1])
        with download_col2:
            st.markdown("### 📥 Download MarkDown Resume Optimization Report")
            
            # Download as Markdown
            st.download_button(
                label="Download Resume Optimization Report",
                data=md_content.encode('utf-8'),
                file_name="output/resume_optimization.md",
                mime="application/octet-stream",
                help="Download the reume optimization report"
            )

    if os.path.isfile("output/resume_optimization.md"):
        st.divider()
        download_col1, download_col2, download_col3 = st.columns([1, 2, 1])
        with download_col2:
            st.markdown("### 📥 Download MarkDown Final Report")
            
            # Download as Markdown
            st.download_button(
                label="Download Final Report",
                data="output/final_report.md",
                file_name="output/final_report.md",
                mime="application/octet-stream",
                help="Download final report"
            )
    if os.path.isfile("output/optimized_resume.md"):
        st.divider()
        download_col1, download_col2, download_col3 = st.columns([1, 2, 1])
        with download_col2:
            st.markdown("### 📥 Download Optimized Resume Report")
            
            # Download as Markdown
            st.download_button(
                label="Download Final Report",
                data="output/optimized_resume.md",
                file_name="output/optimized_resume.md",
                mime="application/octet-stream",
                help="Download Optimized Resume report"
            )

# Add footer
st.divider()
footer_col1, footer_col2, footer_col3 = st.columns([1, 2, 1])
with footer_col2:
    st.caption("Made with ❤️ using [CrewAI](https://crewai.com) and [Streamlit](https://streamlit.io)")