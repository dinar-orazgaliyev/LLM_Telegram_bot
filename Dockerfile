FROM python:3.10-slim

WORKDIR /bot

# Install apt_pkg dependency
RUN apt-get update && \
    apt-get install -y curl git python3-apt && \
    rm -rf /var/lib/apt/lists/*

# Install Ollama CLI
RUN curl -fsSL https://ollama.com/install.sh | sh

# Copy dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY . .

ENV PYTHONUNBUFFERED=1

COPY start.sh .
CMD ["./start.sh"]


