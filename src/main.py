from dotenv import load_dotenv
from typing import Final
import os 
from bot_handlers import start_command, help_command, exercise_command,handle_message, error
from telegram.ext import Application, CommandHandler, MessageHandler, filters

load_dotenv()
TOKEN: Final = os.getenv("api_key")
BOT_USERNAME: Final = "@Jarvis4Homa"
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