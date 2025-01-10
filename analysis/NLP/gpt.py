from openai import OpenAI
import os
from dotenv import load_dotenv
load_dotenv()


client=OpenAI()
client.api_key = os.getenv("OPENAI_API_KEY")


def analyze_speech(system, prompt):
    """
    Sends a prompt to OpenAI's GPT API with a custom system prompt tailored for analyzing speech quality in videos.
    
    Args:
        prompt (str): The user prompt describing the analysis requirements.
    Returns:
        str: The AI's response to the prompt.
    """
    system_prompt = (
        "You are an AI specialized in analyzing the quality of speech in video recordings. Your tasks include detecting "
        "linguistic errors, assessing fluency, analyzing emotional tone or detecting pauses and filler words. "
        "Provide clear, actionable insights tailored for public speaking improvement, "
        "media training, and educational or HR purposes. Return only parts of the transcript when the errors happens and nothing more."
        "split the parts by |, but don't start or end your answer with |."
    )
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error: {str(e)}"
