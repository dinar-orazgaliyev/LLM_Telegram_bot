from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_community.vectorstores import Chroma
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory

from src.llm.utils import init_vector_db
from pathlib import Path
import os
import re
import random

# llm = ChatOllama(model="phi3")


class LLMManager:
    def __init__(self, model_name: str = "phi3", temperature: float = 0.2):
        root = Path(os.getcwd())
        rag_dir = root / "data_rag"
        self.model = ChatOllama(model=model_name, temperature=temperature)
        self.db = init_vector_db(rag_dir)  # from your previous code

    def init_qa_chain(self,level='A1',exercise_text=None):
        retriever = self.db.as_retriever(search_kwargs={"filter": {"level": level}})
        memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True,output_key="answer")
        if exercise_text:
            memory.chat_memory.add_user_message(f"Exercise:\n{exercise_text}")
        self.qa_chain = ConversationalRetrievalChain.from_llm(
            llm=self.model,
            retriever=retriever,
            memory=memory,
            return_source_documents=True
        )
    def clean_exercise_context(self, chunks):
        """
        Removes headers, version numbers, and other metadata from RAG results.
        Returns only meaningful exercise content.
        """
        cleaned = []
        for chunk in chunks:
            lines = chunk.page_content.split("\n")
            filtered_lines = []
            for line in lines:
                line = line.strip()
                # Skip lines that look like version numbers, PTN codes, empty, or very short
                if (
                    not line
                    or re.match(r"Version\s+\w+", line)
                    or re.match(r"PTN-Nr\.:", line)
                    or re.match(r"^\d{1,3}/\d{4}$", line)
                    or len(line) < 5
                ):
                    continue
                filtered_lines.append(line)
            if filtered_lines:
                cleaned.append("\n".join(filtered_lines))
        return "\n\n".join(cleaned)

    def get_context(self, k=3, level="A1"):
        all_docs = self.db.similarity_search(
            query="", k=100, filter={"level": level}
        )  # get enough
        # Randomly sample k exercises
        sampled_docs = random.sample(all_docs, min(k, len(all_docs)))
        context = self.clean_exercise_context(sampled_docs)
        return context

    def get_response(self, user_text: str, system_prompt: str = None) -> str:
        """
        Send text to the LLM and return the response
        Optionally pass a system prompt for role behavior.

        """
        messages = []
        if system_prompt:
            messages.append(SystemMessage(content=system_prompt))

        messages.append(HumanMessage(content=user_text))

        response = self.model.invoke(messages)

        return response.content
