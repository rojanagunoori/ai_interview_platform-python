import PyPDF2
import numpy as np
import pandas as pd

def extract_resume_text1(uploaded_file):
    pdf_reader = PyPDF2.PdfReader(uploaded_file)
    text = ''
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

def extract_resume_text(uploaded_file):
    # Extract text from the PDF using PyPDF2
    pdf_reader = PyPDF2.PdfReader(uploaded_file)
    text = ''
    for page in pdf_reader.pages:
        text += page.extract_text()
    
    # Split the extracted text into sentences or paragraphs using numpy for structured storage
    text_data = np.array(text.split("\n"))
    
    # Convert numpy array to a pandas DataFrame for easy manipulation
    df = pd.DataFrame(text_data, columns=['Extracted_Text'])
    
    # Optional: Perform some basic cleaning or text processing with pandas
    df['Extracted_Text'] = df['Extracted_Text'].str.strip()  # Remove any leading/trailing whitespace
    
    # Return the DataFrame for structured data representation
    return df