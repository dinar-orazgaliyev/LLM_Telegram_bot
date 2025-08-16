# German Learning Chatbot

This is a Telegram bot designed to help you **learn German** in an interactive way. The bot uses a local LLaMA-based model (phi3) via LangChain, allowing flexible integration with different language models in the future. It can also be extended to support **RAG (Retrieval-Augmented Generation)** for contextual responses.

## Features

- Interactive German conversation practice.
- Understands general text input (not just predefined commands).
- Modular architecture: separates Telegram bot logic, model interaction, and utilities.
- Future-ready for NLP enhancements and multi-model support.

For now local llama-phi3 model will be used, but later it can be integrated with other LLM models inside the llm_manager
in order for it to work install the model:
-curl -fsSL https://ollama.com/install.sh | sh