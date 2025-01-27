from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

client = None


def analyze_speech(system, prompt):
    global client

    """
    Sends a prompt to OpenAI's GPT API with a custom system prompt tailored for analyzing speech quality in videos.
    
    Args:
        prompt (str): The user prompt describing the analysis requirements.
    Returns:
        str: The AI's response to the prompt.
    """

    if client is None:
        client = OpenAI()
        client.api_key = os.getenv("OPENAI_API_KEY")

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": prompt},
            ],
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error: {str(e)}"
