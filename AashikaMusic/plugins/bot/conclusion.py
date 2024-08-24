import os
import requests
import json
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

async def get_gpt_answer(question):
    # Fetch the API key from environment variables
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        LOGS.error("OpenAI API key not found!")
        return "OpenAI API key not found!"

    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "gpt-3.5-turbo",
        "messages": [
            {"role": "system", "content": "You specialize in drawing conclusions in detail. Please respond to the query in a friendly tone in Hindi (Hinglish) language. Explain the conversation, and explain what each person talked about and the overall conclusion. If someone was wrong, point out whose argument was less effective and whose was more insightful. Also, rate their conversation style out of 10 using ⭐️ emoji at the end. Format will be (user): 5/10 ⭐️. 2nd user: 8/10 ⭐️."},
            {"role": "user", "content": question}
        ],
        "max_tokens": 1000,
        "temperature": 0.7
    }

    response = requests.post(url, headers=headers, data=json.dumps(data))
    content_json = response.json()
    return content_json["choices"][0]["message"]["content"]
