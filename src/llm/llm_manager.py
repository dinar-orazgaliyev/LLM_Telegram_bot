from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage, SystemMessage

llm = ChatOllama(model="phi3")


def get_llm_response(user_text:str, system_prompt:str = None) -> str:
    """
    Send text to the LLM and return the response
    Optionally pass a system prompt for role behavior.

    """
    messages = []
    if system_prompt:
        #messages.append({'role':'system', 'content':system_prompt})
        messages.append(SystemMessage(content=system_prompt))

    messages.append(HumanMessage(content=user_text))

    response = llm.invoke(messages)

    return response.content