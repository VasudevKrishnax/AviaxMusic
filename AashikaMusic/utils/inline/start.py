from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from pyrogram import Client, filters

import config
from AashikaMusic import app

# Define your video link
VIDEO_LINK = "https://graph.org/file/7c6730c50e7738078bbe5.mp4"  # Replace with the actual video link

def start_panel(_):
    buttons = [
        [
            InlineKeyboardButton(
                text=_["S_B_1"], url=f"https://t.me/{app.username}?startgroup=true"
            ),
            InlineKeyboardButton(text=_["S_B_2"], url=config.SUPPORT_GROUP),
        ],
    ]
    return buttons


def private_panel(_):
    buttons = [
        [
            InlineKeyboardButton(
                text=_["S_B_3"],
                url=f"https://t.me/{app.username}?startgroup=true",
            )
        ],
        [InlineKeyboardButton(text=_["S_B_4"], callback_data="settings_back_helper")],
        [
            InlineKeyboardButton(text=_["S_B_5"], user_id=config.OWNER_ID),
            InlineKeyboardButton(text=_["S_B_2"], url=config.SUPPORT_GROUP),
        ],
        [
            InlineKeyboardButton(text=_["S_B_6"], url=config.SUPPORT_CHANNEL),
            InlineKeyboardButton(text=_["S_B_7"], callback_data="REPO"),  # Use callback data instead of url
        ],
    ]
    return buttons


@app.on_callback_query(filters.regex("send_video"))
async def send_video_callback(client: Client, callback_query: CallbackQuery):
    """
    This function handles the sending of the video when the 'S_B_7' button is clicked.
    """
    # Answer the callback query to stop the loading circle
    await callback_query.answer()

    # Send the video to the user who pressed the button
    await client.send_video(
        chat_id=callback_query.message.chat.id,
        video=VIDEO_LINK,  # Replace this with the actual video link
        caption="Here is the video you requested!"  # Optional: Add a caption to the video
    )

# Example usage of start_panel and private_panel
#@app.on_message(filters.command("start"))
#async def start_command(client: Client, message):
    # Send the start panel buttons to the user
  ## await message.reply_text("Welcome! Here are some helpful buttons.", reply_markup=InlineKeyboardMarkup(buttons))
