FROM python:3.10-slim

# Set working directory
WORKDIR /bot

# Install curl (needed for Ollama install)
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# Install Ollama CLI
RUN curl -fsSL https://ollama.com/install.sh | sh

# Copy dependencies
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the bot source code
COPY . .

# Prevent Python from buffering stdout/stderr
ENV PYTHONUNBUFFERED=1

# Default command
CMD ["python", "-m", "src.main"]
