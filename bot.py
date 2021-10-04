#!/usr/bin/env python3
# Copyright (C) @PredatorHackerzZ
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
import os
from pyrogram import Client, filters
from pyrogram.types import *


Bot = Client(
    "Calculator Bot",
    bot_token = os.environ["BOT_TOKEN"],
    api_id = int(os.environ["API_ID"]),
    api_hash = os.environ["API_HASH"]
)


START_TEXT = """
𝐇𝐞𝐥𝐥𝐨 🥳 {}, 𝐓𝐡𝐢𝐬 𝐢𝐬 𝐚 𝐓𝐞𝐥𝐞𝐠𝐫𝐚𝐦 [𝐂𝐚𝐥𝐜𝐮𝐥𝐚𝐭𝐨𝐫-𝐁𝐨𝐭](https://Github.com/PredatorHackerzZ/Calculator-Bot).

▷ 𝐒𝐞𝐧𝐝 𝐦𝐞 /calculator 𝐜𝐨𝐦𝐦𝐚𝐧𝐝 𝐚𝐧𝐝 𝐒𝐞𝐞 𝐌𝐚𝐠𝐢𝐜. 

𝐌𝐚𝐝𝐞 𝐰𝐢𝐭𝐡 𝐛𝐲 ❤️ [@𝐓𝐡𝐞𝐓𝐞𝐥𝐞𝐑𝐨𝐢𝐝](https://t.me/TheTeleRoid)
"""
START_BUTTONS = InlineKeyboardMarkup(
        [[
        InlineKeyboardButton('📕 𝐒𝐨𝐮𝐫𝐜𝐞 𝐂𝐨𝐝𝐞', url='https://github.com/PredatorHackerzZ/Calculator-Bot'),
        InlineKeyboardButton('👥 𝐂𝐡𝐚𝐧𝐧𝐞𝐥 ', url='https://t.me/TeleRoidGroup')
        ]]
    )
CALCULATE_TEXT = "▷ 𝐌𝐚𝐝𝐞 𝐰𝐢𝐭𝐡 𝐛𝐲 @TheTeleRoid"
CALCULATE_BUTTONS = InlineKeyboardMarkup(
        [[
        InlineKeyboardButton("DEL", callback_data="DEL"),
        InlineKeyboardButton("AC", callback_data="AC"),
        InlineKeyboardButton("(", callback_data="("),
        InlineKeyboardButton(")", callback_data=")")
        ],[
        InlineKeyboardButton("7", callback_data="7"),
        InlineKeyboardButton("8", callback_data="8"),
        InlineKeyboardButton("9", callback_data="9"),
        InlineKeyboardButton("÷", callback_data="/")
        ],[
        InlineKeyboardButton("4", callback_data="4"),
        InlineKeyboardButton("5", callback_data="5"),
        InlineKeyboardButton("6", callback_data="6"),
        InlineKeyboardButton("×", callback_data="*")
        ],[
        InlineKeyboardButton("1", callback_data="1"),
        InlineKeyboardButton("2", callback_data="2"),
        InlineKeyboardButton("3", callback_data="3"),
        InlineKeyboardButton("-", callback_data="-"),
        ],[
        InlineKeyboardButton(".", callback_data="."),
        InlineKeyboardButton("0", callback_data="0"),
        InlineKeyboardButton("=", callback_data="="),
        InlineKeyboardButton("+", callback_data="+"),
        ]]
    )


@Bot.on_message(filters.command(["start"]))
async def start(bot, update):
    text = START_TEXT.format(update.from_user.mention)
    reply_markup = START_BUTTONS
    await update.reply_text(
        text=text,
        disable_web_page_preview=True,
        reply_markup=reply_markup,
        quote=True
    )


@Bot.on_message(filters.private & filters.command(["calc", "calculate", "calculator"]))
async def calculate(bot, update):
    await update.reply_text(
        text=CALCULATE_TEXT,
        reply_markup=CALCULATE_BUTTONS,
        disable_web_page_preview=True,
        quote=True
    )


@Bot.on_callback_query()
async def cb_data(bot, update):
        data = update.data
        try:
            message_text = update.message.text.split("\n")[0].strip().split("=")[0].strip()
            message_text = '' if CALCULATE_TEXT in message_text else message_text
            if data == "=":
                text = float(eval(message_text))
            elif data == "DEL":
                text = message_text[:-1]
            elif data == "AC":
                text = ""
            else:
                text = message_text + data
            await update.message.edit_text(
                text=f"{text}\n\n{CALCULATE_TEXT}",
                disable_web_page_preview=True,
                reply_markup=CALCULATE_BUTTONS
            )
        except Exception as error:
            print(error)


@Bot.on_inline_query()
async def inline(bot, update):
    if len(update.data) == 0:
        try:
            answers = [
                InlineQueryResultArticle(
                    title="Calculator",
                    description=f"New calculator",
                    input_message_content=InputTextMessageContent(
                        text=CALCULATE_TEXT,
                        disable_web_page_preview=True
                    ),
                    reply_markup=CALCULATE_BUTTONS
                )
            ]
        except Exception as error:
            print(error)
    else:
        try:
            message_text = update.message.text.split("\n")[0].strip().split("=")[0].strip()
            data = message_text.replace("×", "*").replace("÷", "/")
            text = float(eval(data))
            answers = [
                InlineQueryResultArticle(
                    title="Answer",
                    description=f"Results of your input",
                    input_message_content=InputTextMessageContent(
                        text=f"{data} = {text}",
                        disable_web_page_preview=True
                    )
                )
            ]
        except:
            pass
    await update.answer(answers)


Bot.run()
