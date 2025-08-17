
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
from src.llm.llm_manager import get_llm_response





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
    exercise_prompt = "Generate a short German learning exercise. Keep it simple for B1 level."
    exercise_text = get_llm_response(exercise_prompt)

    context.user_data["current_exercise"] = "dynamic_exercise"
    await update.message.reply_text(exercise_text)


# === Main Chat Handler ===


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text

    # Check if user is answering an exercise
    if "current_exercise" in context.user_data:
        exercise_id = context.user_data.pop("current_exercise")
        feedback = get_llm_response(
            user_text,
            system_prompt="You are a German teacher. The user just answered an exercise. "
                          "Give short feedback in German, correcting mistakes if needed."
        )
        await update.message.reply_text(f"✅ Feedback: {feedback}")
        return

    # Otherwise, normal conversation
    response = get_llm_response(
        user_text,
        system_prompt="You are a helpful German language tutor. "
                      "Correct mistakes politely and explain briefly."
    )
    await update.message.reply_text(f"🤖 {response}")


# === Error Handler ===


async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f"Update {update} caused error {context.error}")




