#!/bin/bash
set -e

# Start Ollama server in the background
echo "Starting Ollama server..."
ollama serve &

# Wait a few seconds for the server to be ready
sleep 5

# Pull phi3 model if not already present
if ! ollama list | grep -q "phi3"; then
    echo "Pulling phi3 model..."
    ollama pull phi3
else
    echo "phi3 model already exists."
fi

# Start the Telegram bot
echo "Starting the German learning bot..."
python -m src.main
