from json import load
from turtle import width
import streamlit as st
import os
from src.utils.output_handler import capture_output
from resume_crew.main import run

def validate_non_empty(st_field):
    try:
        if len(st_field) > 0:
         return True, ""
    except ValueError:
        return False, f"Please enter a value in {st_field.label}"

def validate_url(st_field):
    try:
        if st_field.startswith("http"):
            return True, ""
    except ValueError:
        return False, f"Please enter a valid URL in {st_field.label}"


knowledge_dir = './knowledge'

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
        job_url = st.text_input("Job URL", placeholder="Enter the job posting URL")
        if job_url:
            is_valid, message = validate_url(job_url)
            if not is_valid:
                st.error(message)
        company_name = st.text_input("Company Name", placeholder="Enter the company name")
        if company_name:
            is_valid, message = validate_non_empty(company_name)
            if not is_valid:
                st.error(message)
        resume_file = st.file_uploader("Upload Resume", type=['pdf'], help="Upload your resume in PDF format")
        if resume_file:
            is_valid, message = validate_non_empty(resume_file.name)
            if not is_valid:
                st.error(message)
        submitted = st.form_submit_button("🚀 Optimize Resume")
       
        if submitted:            
            path = os.path.join(knowledge_dir, resume_file.name)
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
        
        # # Convert CrewOutput to string for display and download
        # result_text = str(result)

        # # save to pdf
        
        
        # # Display the final result
        # st.markdown(result_text)

        # st_md2pdf(result_text, "news.pdf")
        # with open("news.pdf", "rb") as pdf_file:
        #     PDFbyte = pdf_file.read()

        # st.divider()
        # download_col1, download_col2, download_col3 = st.columns([1, 2, 1])
        # with download_col2:
        #     st.markdown("### 📥 Download PDF Research Report")
            
        #     # Download as Markdown
        #     st.download_button(
        #         label="Download PDF Report",
        #         data=PDFbyte,
        #         file_name="news_report.pdf",
        #         mime="application/octet-stream",
        #         help="Download the research report in Markdown format"
        #     )
        
        # # Create download buttons
        # st.divider()
        # download_col1, download_col2, download_col3 = st.columns([1, 2, 1])
        # with download_col2:
        #     st.markdown("### 📥 Download MAKDOWN Research Report")
            
        #     # Download as Markdown
        #     st.download_button(
        #         label="Download Report",
        #         data=result_text,
        #         file_name="research_report.md",
        #         mime="text/markdown",
        #         help="Download the research report in Markdown format"
        #     )

# Add footer
st.divider()
footer_col1, footer_col2, footer_col3 = st.columns([1, 2, 1])
with footer_col2:
    st.caption("Made with ❤️ using [CrewAI](https://crewai.com), [PyFpdf](https://pyfpdf.readthedocs.io/) and [Streamlit](https://streamlit.io)")