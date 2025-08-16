
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
from dateutil.parser import parse





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




