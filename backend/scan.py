from PyPDF2 import PdfReader

def scan_pdf(file_stream):
    """
    Scan a PDF file from an in-memory file stream.
    :param file_stream: A file-like object (e.g., BytesIO) containing the PDF data.
    :return: A dictionary with scan results.
    """
    reader = PdfReader(file_stream)
    num_pages = len(reader.pages)
    first_page = reader.pages[0]
    text = first_page.extract_text()

    # Example checks
    header_red = "red" in text.lower()  # Dummy check
    result = {
        "file_name": "in_memory_file.pdf",  # Placeholder name
        "num_pages": num_pages,
        "header_red": header_red,
        "text": text[:100]  # First 100 characters
    }
    return result