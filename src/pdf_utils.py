import PyPDF2
import io

def extract_text_from_pdf(pdf_file):
    """
    Extracts text from a PDF file object.
    """
    try:
        reader = PyPDF2.PdfReader(pdf_file)
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"
        return text.strip()
    except Exception as e:
        return f"Error extracting PDF: {str(e)}"
