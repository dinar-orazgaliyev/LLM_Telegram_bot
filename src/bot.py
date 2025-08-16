from dotenv import load_dotenv
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes,
    CallbackContext,
    Updater,
)
from typing import Final
import os, re
from dateutil.parser import parse

import pytz

load_dotenv()
TOKEN: Final = os.getenv("api_key")
BOT_USERNAME: Final = "@Jarvis4Homa"


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Hallo! 👋 I am your German learning bot. "
        "You can chat with me in German, and I will correct your sentences. "
        "Use /exercise to practice German exercises."
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Commands:\n"
        "/start - Welcome message\n"
        "/help - Show this message\n"
        "/exercise - Get a short German exercise\n\n"
        "Or just type in German and I will reply and correct your mistakes."
    )


async def exercise_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Example simple exercise
    exercise_text = (
        "Translate the following sentence into German:\n"
        "'I am learning German at the moment.'"
    )
    context.user_data["current_exercise"] = "translate_1"
    await update.message.reply_text(exercise_text)


# === Main Chat Handler ===


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text

    # Check if user is answering an exercise
    if "current_exercise" in context.user_data:
        exercise_id = context.user_data.pop("current_exercise")
        # Here you would send user_text + exercise_id to LLaMA for evaluation
        response = (
            f"✅ Got your answer for {exercise_id}. Here’s feedback: (dummy feedback)"
        )
        await update.message.reply_text(response)
        return

    # Otherwise, normal chat (correction / conversation)
    # Send user_text to LLaMA and get a response
    response = f"🤖 LLaMA Response: (dummy reply to '{user_text}')"
    await update.message.reply_text(response)


# === Error Handler ===


async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f"Update {update} caused error {context.error}")


# === Bot Startup ===

if __name__ == "__main__":
    print("Starting German learning bot...")
    app = Application.builder().token(TOKEN).build()

    # Command handlers
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("exercise", exercise_command))

    # Message handler
    app.add_handler(MessageHandler(filters.TEXT, handle_message))

    # Error handler
    app.add_error_handler(error)

    print("Polling...")
    app.run_polling(poll_interval=3)
