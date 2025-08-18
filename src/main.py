from dotenv import load_dotenv
from typing import Final
import os
from .bot_handlers import (
    start_command,
    help_command,
    exercise_command,
    handle_message,
    error,
    set_level_command,
    set_type_command,
    level_callback,
    type_callback,
)
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    CallbackQueryHandler,
)
from telegram import BotCommand


load_dotenv()
TOKEN: Final = os.getenv("api_key")
BOT_USERNAME: Final = "@Jarvis4Deutsch"


async def set_commands(application):
    commands = [
        BotCommand("start", "Welcome message"),
        BotCommand("help", "Show help message"),
        BotCommand("exercise", "Get a German exercise"),
        BotCommand("setlevel", "Sets the level of German"),
        BotCommand("settype", "set type of exercise grammar/vocabulary"),
    ]
    await application.bot.set_my_commands(commands)


print("Starting German learning bot...")
app = Application.builder().token(TOKEN).post_init(set_commands).build()
# Command handlers
app.add_handler(CommandHandler("start", start_command))
app.add_handler(CommandHandler("help", help_command))
app.add_handler(CommandHandler("exercise", exercise_command))
app.add_handler(CommandHandler("setlevel", set_level_command))
app.add_handler(CallbackQueryHandler(level_callback, pattern="^level_"))
app.add_handler(CommandHandler("settype", set_type_command))
app.add_handler(CommandHandler("settype", set_type_command))
app.add_handler(CallbackQueryHandler(type_callback, pattern="^type_"))
# Message handler
app.add_handler(MessageHandler(filters.TEXT, handle_message))

# Error handler
app.add_error_handler(error)

print("Polling...")
app.run_polling(poll_interval=3)
