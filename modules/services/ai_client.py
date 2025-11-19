from typing import Optional
import logging
import google.generativeai as genai

logger = logging.getLogger(__name__)

MODEL_NAME = "gemini-2.5-flash"

def get_gemini_response(input_text: str, resume_text: str, prompt: str) -> str:
    """Generate a response from Gemini model using provided texts.

    Returns the response text or raises an exception.
    """
    try:
        model = genai.GenerativeModel(MODEL_NAME)
        # compose the final input
        final_input = f"{input_text}\n\nResume:\n{resume_text}\n\nInstructions: {prompt}"
        response = model.generate_content(final_input)
        return response.text
    except Exception as e:
        logger.exception("Model error during generation")
        logger.info("Trying alternative model...")
        try:
            # fallback: try the same model again (placeholder for future alternative)
            model = genai.GenerativeModel(MODEL_NAME)
            final_input = f"{input_text}\n\nResume:\n{resume_text}\n\nInstructions: {prompt}"
            response = model.generate_content(final_input)
            return response.text
        except Exception as e2:
            logger.exception("Fallback model also failed")
            return f"Error: {e2}"
