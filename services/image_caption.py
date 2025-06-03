from google import genai
from google.genai import types
from config import GEMINI_API_KEY
from utils.logger import Logger

import requests

log = Logger("services.image_caption")

def generate_caption(image_url, image_type):
    """
    Generate a caption for the given image using Gemini API.
    
    Args:
        image_url (str): The URL of the image to be captioned.
        image_type (str): The type of the image (e.g., "image/jpeg").
    
    Returns:
        str: The generated caption for the image.
    """
    image_bytes = requests.get(image_url).content
    image = types.Part.from_bytes(data=image_bytes, mime_type=image_type)
    
    client = genai.Client(api_key=GEMINI_API_KEY)
    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash-exp",
            contents=["Generate the image description for accessibility, no more than 150 tokens", image],
            )

        return response.text
    except Exception as e:
        print(f"Error generating caption: {e}")
        return "There is an Error when generating caption"