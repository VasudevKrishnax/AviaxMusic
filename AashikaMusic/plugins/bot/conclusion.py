import requests
import json
import os
from io import BytesIO
from pyrogram import Client, filters
from pyrogram.types import Message
from dotenv import load_dotenv
from AashikaMusic.core.bot import Aashika

# Load environment variables from .env file
load_dotenv()

# Fetch environment variables
API_ID = os.getenv('API_ID')
API_HASH = os.getenv('API_HASH')
BOT_TOKEN = os.getenv('BOT_TOKEN')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

# Initialize the bot client
bot = Aashika()

async def get_gpt_answer(question: str, max_tokens: int) -> str:
    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "gpt-4o-mini",
        "messages": [
            {"role": "system", "content": "You specialize in drawing conclusions in detail. Please respond to the query in a friendly tone in Hindi (Hinglish) language. Explain the conversation, and explain what each person talked about and the overall conclusion. If someone was wrong, point out whose argument was less effective and whose was more insightful. Also, rate their conversation style out of 10 using ⭐️ emoji at the end. Format will be (user): 5/10 ⭐️. 2nd user: 8/10 ⭐️."},
            {"role": "user", "content": question}
        ],
        "max_tokens": max_tokens,
        "temperature": 0.7
    }

    try:
        response = requests.post(url, headers=headers, data=json.dumps(data))
        response.raise_for_status()  # Raises an HTTPError for bad responses
        content_json = response.json()
        return content_json["choices"][0]["message"]["content"]
    except requests.exceptions.RequestException as e:
        print(f"HTTP Request failed: {e}")
        return "Error: Unable to get a response from GPT."

@bot.on_message(filters.command('conclusion'))
async def conclusion_handler(client: Client, message: Message):
    print("Received /conclusion command.")
    command_args = message.text.split()
    if len(command_args) != 2:
        await message.reply("Usage: /conclusion <word_count>")
        return

    value = command_args[1]
    if value not in ('40', '90', '150'):
        await message.reply("Invalid value. Please provide 40, 90, or 150.")
        return

    # Send heart icon first
    heart_message = await message.reply("❤️")

    # Retrieve recent messages
    messages = await get_recent_messages(message)
    if not messages:
        await heart_message.edit("Not enough messages found in the group.")
        return

    try:
        # Determine max tokens based on value
        max_tokens = {
            '40': 150,  # Adjust according to your needs
            '90': 300,  # Adjust according to your needs
            '150': 500  # Adjust according to your needs
        }.get(value, 150)

        # Get the conclusion from GPT
        response = await get_gpt_answer(messages, max_tokens)
        if response:
            if len(response) < 4095:
                await heart_message.edit(f"<b></b>\n <i>{response}</i>", parse_mode="html")
            else:
                with BytesIO(response.encode()) as file:
                    file.name = "gpt_response.txt"
                    await message.reply_document(
                        file, caption=f"{messages[:1020]}", reply_to_message_id=message.message_id
                    )
        else:
            await heart_message.edit("Failed to get a response from GPT.")
    except Exception as exc:
        await heart_message.edit(f"Error: \n> {exc}")

async def get_recent_messages(message: Message, num_messages: int = 5) -> str:
    try:
        chat_id = message.chat.id
        history = await bot.get_chat_history(chat_id, limit=num_messages + 1)

        if len(history) > 1:
            messages = []
            for msg in reversed(history[1:]):  # Skip the most recent message
                sender_name = (await bot.get_users(msg.from_user.id)).first_name if msg.from_user else "Unknown"
                messages.append(f"{sender_name}: {msg.text}")
            return "\n".join(messages)
        else:
            return None
    except Exception as exc:
        print(f"Failed to get recent messages: {exc}")
        return None

# Ensure the bot starts correctly
async def main():
    await bot.start()
    print("Bot started.")
    await bot.idle()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
