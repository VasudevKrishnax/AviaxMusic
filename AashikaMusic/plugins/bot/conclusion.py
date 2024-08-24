import requests
import json
import os
from io import BytesIO
from telethon import events
from telethon.tl.functions.messages import GetHistoryRequest
from telethon.tl.types import PeerChannel
from dotenv import load_dotenv
from AashikaMusic import bot  # Adjust this import to match your actual project structure

# Load environment variables from .env file
load_dotenv()

# Fetch environment variables
API_ID = os.getenv('API_ID')
API_HASH = os.getenv('API_HASH')
BOT_TOKEN = os.getenv('BOT_TOKEN')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

# Initialize the Telethon client
client = bot.client  # Access the bot client from AashikaMusic

async def get_gpt_answer(question):
    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
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

@client.on(events.NewMessage(pattern='/conclusion'))
async def conclusion_handler(event):
    messages = await get_recent_messages(event)
    if not messages:
        return await event.reply("Not enough messages found in the group.")
    
    await event.reply("Processing...", parse_mode="html")
    try:
        response = await get_gpt_answer(messages)
        if len(response) < 4095:
            await event.reply(f"<b></b>\n <i>{response}</i>", parse_mode="html")
        else:
            with BytesIO(response.encode()) as file:
                file.name = "gpt_response.txt"
                await client.send_file(
                    event.chat_id, file, caption=f"{messages[:1020]}", reply_to=event.message.id
                )
    except Exception as exc:
        await event.reply(f"Error: \n> {exc}")

async def get_recent_messages(event, num_messages=5):
    try:
        history = await client(GetHistoryRequest(
            peer=event.chat_id,
            offset_id=0,
            offset_date=None,
            add_offset=0,
            limit=num_messages + 1,
            max_id=0,
            min_id=0,
            hash=0
        ))

        if history.messages and len(history.messages) > 1:
            messages = []
            for msg in history.messages[1:]:
                sender = await client.get_entity(msg.from_id) if msg.from_id else None
                sender_name = sender.first_name if sender else "Unknown"
                messages.append(f"{sender_name}: {msg.message}")
            return "\n".join(reversed(messages))
        else:
            return None
            
    except Exception as exc:
        return None
