
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ConversationHandler,
    filters,
    ContextTypes,
    CallbackContext,
    Updater,
)
from typing import Final
from dateutil.parser import parse
from src.llm.llm_manager import LLMManager
from src.prompts.prompts import exercise_prompt, feedback_prompt


llm_manager = LLMManager(model_name="phi3")

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
        "setlevel - Set your Deutsch level\n\n"
        "settype - set exercise type (Grammar or Vocabulary)\n\n"
        "Or just type in German and I will reply and correct your mistakes."
    )

async def set_level_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [
            InlineKeyboardButton("A1", callback_data="level_A1"),
            InlineKeyboardButton("A2", callback_data="level_A2"),
            InlineKeyboardButton("B1", callback_data="level_B1"),
        ],
        [
            InlineKeyboardButton("B2", callback_data="level_B2"),
            InlineKeyboardButton("C1", callback_data="level_C1"),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Select your German level:", reply_markup=reply_markup)

async def level_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()  # Acknowledge the callback
    
    # Extract the level from callback_data
    level = query.data.split("_")[1]
    context.user_data['level'] = level
    await query.edit_message_text(f"✅ Your level is set to {level}")


async def set_type_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [
            InlineKeyboardButton("Grammar", callback_data="type_grammar"),
            InlineKeyboardButton("Vocabulary", callback_data="type_vocabulary"),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Select exercise type:", reply_markup=reply_markup)


# Step 2: Callback when a button is clicked
async def type_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()  # Acknowledge the callback
    
    # Extract the type from callback_data
    exercise_type = query.data.split("_")[1]
    context.user_data["exercise_type"] = exercise_type
    await query.edit_message_text(f"✅ Exercise type set to {exercise_type}")

async def exercise_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    
    level = context.user_data.get('level','A1')
    print(level)
    exercise_type = context.user_data.get("exercise_type","grammar")
    rag_context = llm_manager.get_context(level=level)
    print(rag_context)
    prompt_text = exercise_prompt.format(exercise_type=exercise_type,context=rag_context,level=level)
    exercise_text = llm_manager.get_response(prompt_text)

    
    context.user_data["current_exercise"] = {
    "level": level,
    "type": exercise_type,
    "id": "dynamic_exercise",
    "text": exercise_text
    }
    await update.message.reply_text(exercise_text)


# === Main Chat Handler ===


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text

    # Check if user is answering an exercise
    if "current_exercise" in context.user_data:
        exercise_info  = context.user_data["current_exercise"]
        exercise_type = exercise_info["type"]
        level = exercise_info["level"]
        exercise_text = exercise_info["text"]
        print(exercise_info)
        prompt_text = feedback_prompt.format(
            user_text=user_text,
            exercise_type=exercise_type,
            level=level,
            exercise_text=exercise_text
        )
        feedback = llm_manager.get_response(
            user_text,
            system_prompt=prompt_text
        )
        await update.message.reply_text(f"✅ Feedback: {feedback}")
        return

    # Otherwise, normal conversation
    response = llm_manager.get_response(
        user_text,
        system_prompt="You are a helpful German language tutor. "
                      "Correct mistakes politely and explain briefly in both German and English."
    )
    await update.message.reply_text(f"🤖 {response}")


# === Error Handler ===


async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f"Update {update} caused error {context.error}")




