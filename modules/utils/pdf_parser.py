import PyPDF2
import logging

logger = logging.getLogger(__name__)


def extract_text_from_pdf(uploaded_file):
    """Extract text from a PDF uploaded file-like object.

    Returns a single string with concatenated text from all pages.
    Raises a ValueError if reading fails.
    """
    if uploaded_file is None:
        raise FileNotFoundError("No file uploaded")

    try:
        pdf_reader = PyPDF2.PdfReader(uploaded_file)
        text = ""
        for page in pdf_reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
        return text
    except Exception as e:
        logger.exception("Error reading PDF")
        raise ValueError(f"Error reading PDF: {e}") from e
