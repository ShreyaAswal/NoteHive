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
         Analyze the following text and perform two tasks:
        1.  Provide a concise summary of the content (approximately 150 words).
        2.  Identify the primary academic subject of the text like physics , chemistry, mathematics,computer science etc.

        TEXT:
        "{text}"
        Please format your entire response as a single, valid JSON object with two keys: "subject" and "summary".
        Example:
        {{
            "subject": "History",
            "summary": "The document details the key events of the ancient Roman Empire..."
        }}

        """

        # 4. Call the generate_content method directly from the model object.
        response = model.generate_content(prompt)

        #    Clean up and parse the JSON response from the model.
        #    The model sometimes wraps the JSON in markdown, which we remove.
        cleaned_response = response.text.strip().lstrip("```json").rstrip("```")
        response_data = json.loads(cleaned_response)

        # 5. Return the generated text and a None value for the error.
        return response_data, None

    except json.JSONDecodeError:
        # This error occurs if the model's output isn't valid JSON.
        return None, "Failed to parse the AI model's structured response. Please try again."
    except Exception as e:
        # Catch any other potential API errors.
        return None, f"An error occurred while contacting the AI service: {e}"