from fpdf import FPDF
import base64

def create_summary_pdf(title, summary):
    """
    Creates a new PDF document in memory from a summary text.
    
    Args:
        title (str): The title of the summary.
        summary (str): The summary text.

    Returns:
        bytes: The raw bytes of the generated PDF.
    """
    pdf = FPDF()
    pdf.add_page()
    
    # Set font for the title (Arial, Bold, 16pt)
    pdf.set_font("Arial", 'B', 16)
    # The 'ln=True' moves the cursor to the next line
    pdf.cell(0, 10, title.encode('latin-1', 'replace').decode('latin-1'), ln=True, align='C')
    
    # Add a line break
    pdf.ln(10)
    
    # Set font for the summary text (Arial, Regular, 12pt)
    pdf.set_font("Arial", '', 12)
    # Use multi_cell to automatically handle line breaks for long text
    pdf.multi_cell(0, 5, summary.encode('latin-1', 'replace').decode('latin-1'))
    
    # Output the PDF to a byte string ('S') for storing in memory.
    return pdf.output(dest='S')


def get_pdf_display(pdf_bytes):
    """
    Encodes PDF bytes into a base64 string for embedding in HTML.
    
    Args:
        pdf_bytes (bytes): The raw bytes of the PDF.

    Returns:
        str: A base64-encoded string.
    """
    base64_pdf = base64.b64encode(pdf_bytes).decode('utf-8')
    return base64_pdf