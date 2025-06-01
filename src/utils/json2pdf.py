import json
from fpdf import FPDF

def json_to_pdf(json_path, pdf_path):
    # Read JSON file
    with open(json_path, 'r') as f:
        data = json.load(f)
    
    # Convert JSON data to a pretty printed string
    json_str = json.dumps(data, indent=4)
    
    # Create a PDF instance
    pdf = FPDF()
    
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    
    # Split the string into lines
    lines = json_str.split('\n')
    
    # Add each line to the PDF
    for line in lines:
        pdf.multi_cell(100, 10, line)
    
    # Save the PDF to the specified path
    pdf.output(pdf_path)

