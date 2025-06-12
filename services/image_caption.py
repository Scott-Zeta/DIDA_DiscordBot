import aiohttp
import asyncio
from google import genai
from google.genai import types
from config import GEMINI_API_KEY
from utils.logger import Logger

log = Logger("services.image_caption")

async def generate_caption(image_url, image_type):
    """
    Generate a caption for the given image using Gemini API.
    
    Args:
        image_url (str): The URL of the image to be captioned.
        image_type (str): The type of the image (e.g., "image/jpeg").
    
    Returns:
        str: The generated caption for the image.
    """
    log.info(f"Generating caption for image type: {image_type}")
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(image_url, timeout=30) as response:
                if response.status != 200:
                    log.error(f"Failed to download image: HTTP {response.status}")
                    return "Error: Failed to download image"
                    
                image_bytes = await response.read()
                
        log.debug(f"Image downloaded successfully ({len(image_bytes)} bytes)")
        image = types.Part.from_bytes(data=image_bytes, mime_type=image_type)
        
        client = genai.Client(api_key=GEMINI_API_KEY)
        response = client.models.generate_content(
            model="gemini-2.0-flash-exp",
            contents=["Generate the image description for accessibility, no more than 150 tokens", image],
        )

        log.info("Caption generated successfully")
        return response.text
        
    except aiohttp.ClientError as e:
        log.error(f"Network error during image download: {e}")
        return "Error: Could not download the image"
    except asyncio.TimeoutError:
        log.error("Timeout while downloading image")
        return "Error: Image download timed out"
    except Exception as e:
        log.error(f"Error generating caption: {e}")
        return "There was an error when generating the caption"