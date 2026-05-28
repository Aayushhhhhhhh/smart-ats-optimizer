"""
PDF Parser Utility
Upgraded from PyPDF2 → pdfplumber for better multi-column, table, and formatting support.
"""

import pdfplumber
import io


def extract_text_from_pdf(uploaded_file) -> str:
    """
    Extracts and cleans text from a PDF file.
    Handles multi-column layouts, tables, and special characters
    much better than PyPDF2.

    Args:
        uploaded_file: Streamlit UploadedFile object or file-like object

    Returns:
        Cleaned text string
    """
    try:
        # Read bytes from the uploaded file
        file_bytes = uploaded_file.read()
        text_parts = []

        with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text(
                    x_tolerance=3,
                    y_tolerance=3,
                    layout=True,           # preserves spatial layout
                    x_density=7.25,
                    y_density=13,
                )
                if page_text:
                    text_parts.append(page_text)

        raw_text = "\n".join(text_parts)
        return _clean_text(raw_text)

    except Exception as e:
        raise ValueError(f"Could not parse PDF: {str(e)}. "
                         "Try re-saving the PDF or using a different file.")


def _clean_text(text: str) -> str:
    """Cleans extracted text — removes excess whitespace and garbage characters."""
    import re

    # Remove null bytes and control characters (except newlines/tabs)
    text = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]', '', text)

    # Collapse 3+ newlines into 2
    text = re.sub(r'\n{3,}', '\n\n', text)

    # Collapse multiple spaces into one
    text = re.sub(r'[ \t]{2,}', ' ', text)

    # Strip leading/trailing whitespace per line
    lines = [line.strip() for line in text.splitlines()]
    text = '\n'.join(line for line in lines if line)

    return text.strip()
