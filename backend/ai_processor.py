import google.generativeai as genai
import pypdf
import os
import json

# --- PDF TEXT EXTRACTION ---
def extract_text_from_pdf(file):
    """
    Extracts text from an uploaded PDF file object provided by Streamlit.
    """
    try:
        # pypdf requires the file pointer to be at the beginning
        file.seek(0)
        reader = pypdf.PdfReader(file)
        text = ""
        for page in reader.pages:
            # Append page text, providing an empty string fallback
            text += (page.extract_text() or "") + "\n"
        return text
    except Exception as e:
        return f"Error reading PDF: {e}"

# --- GEMINI API SUMMARIZATION ---
def summarize(text, api_key):
    """
    Uses the Gemini API to summarize text using the standard library pattern.
    Args:
        text (str): The text to be summarized.
        api_key (str): The user's Google AI Studio API key from st.secrets.
    Returns:
        A tuple: (summary_text, error_message). On success, error_message is None.
    """
    if not text.strip():
        return None, "The provided text is empty. Cannot generate a summary."

    try:
        # 1. Configure the library with your API key. This is the correct first step.
        genai.configure(api_key=api_key)

        # 2. Initialize the model using genai.GenerativeModel().
        model = genai.GenerativeModel('gemini-2.5-flash') # Using the newer, faster model

        # 3. Construct the prompt for the summarization task.
        prompt = f"""
        Please provide a concise and well-structured summary of the following text.
        Focus on the main ideas and key points.

        TEXT:
        "{text}"
        """

        # 4. Call the generate_content method directly from the model object.
        response = model.generate_content(prompt)

        # 5. Return the generated text and a None value for the error.
        return response.text, None

    except Exception as e:
        # Catch any potential errors during the API call.
        return None, f"An error occurred while contacting the AI service: {e}"
