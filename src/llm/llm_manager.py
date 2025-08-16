from langchain_ollama import ChatOllama
from langchain.schema import HumanMessage

llm = ChatOllama(model="phi3")
response = llm.invoke([HumanMessage(content="Hallo, wie geht's dir?")])
print(response.content)
