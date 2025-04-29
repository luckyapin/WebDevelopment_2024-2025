from pathlib import Path

from langchain_ollama import OllamaEmbeddings
from langchain_community.vectorstores import FAISS

from langchain_ollama import ChatOllama
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnablePassthrough, RunnableParallel
from langchain_core.messages import HumanMessage, AIMessage
from langchain.schema.output_parser import StrOutputParser
from typing import List, Dict, Union
import logging
from operator import itemgetter
from langchain_core.runnables import RunnableLambda
from langchain_community.document_loaders import TextLoader

from langchain.text_splitter import CharacterTextSplitter
import markdown

FAISS_INDEX_PATH = 'vectorstore'

# Кэшируем тяжелые объекты на уровне модуля
_vectorstore = None
_retriever = None
_chain = None


def load_vectorstore():
    global _vectorstore
    if _vectorstore is None:
        embeddings = OllamaEmbeddings(model="mxbai-embed-large")
        if not Path(FAISS_INDEX_PATH).exists():
            raise FileNotFoundError(f"Index not found at {FAISS_INDEX_PATH}")

        _vectorstore = FAISS.load_local(
            FAISS_INDEX_PATH,
            embeddings,
            allow_dangerous_deserialization=True
        )
    return _vectorstore


def get_retriever():
    global _retriever
    if _retriever is None:
        _retriever = load_vectorstore().as_retriever(search_kwargs={'k': 3})
    return _retriever


def get_chain():
    global _chain
    if _chain is None:
        prompt = ChatPromptTemplate.from_messages([
            ("system", "Помогай отвечать на вопросы. Контекст для помощи:\n{context}\nИстория диалога:\n{history}"),
            ("human", "{input}"),
        ])

        # Получаем ретривер один раз при инициализации
        retriever = get_retriever()

        _chain = (
                RunnableParallel(
                    # Извлекаем вопрос из входных данных
                    context=itemgetter("input") | retriever,
                    history=itemgetter("history"),
                    input=itemgetter("input")
                )
                | prompt
                | ChatOllama(model='gemma3:1b')
                | StrOutputParser()
        )
    return _chain


class ChatSession:
    def __init__(self, history: List[Dict] = None):
        self.history = history or []
        self.chain = get_chain()

    def _format_history(self) -> str:
        return "\n".join(
            f"{msg['type'].capitalize()}: {msg['content']}"
            for msg in self.history[-2:]
        )

    def get_response(self, question: str) -> str:
        try:
            self.history.append({'type': 'user', 'content': markdown.markdown(question)})

            response = self.chain.invoke({
                "input": question,
                "history": self._format_history()
            })

            self.history.append({'type': 'bot', 'content': markdown.markdown(response)})
            return response
        except Exception as e:
            logging.error(f"Error: {str(e)}")
            return f"Ошибка: {str(e)}"


def show_sample_documents(vectorstore, num=10):
    print("\nSample documents:")
    for i in range(min(num, vectorstore.index.ntotal)):
        doc_id = vectorstore.index_to_docstore_id[i]
        doc = vectorstore.docstore._dict[doc_id]
        print(f"\nDocument {i + 1}:")
        print(f"Content: {doc.page_content}...")
        print(f"Metadata: {doc.metadata}")


def inspect_vectorstore():
    vectorstore = load_vectorstore()

    # Основная информация
    print(f"Total documents: {vectorstore.index.ntotal}")
    print(f"Embedding dimension: {vectorstore.index.d}")

    # Пример метаданных первого документа
    if vectorstore.index.ntotal > 0:
        first_doc_metadata = vectorstore.docstore._dict[vectorstore.index_to_docstore_id[0]].metadata
        print("\nFirst document metadata:", first_doc_metadata)

    return vectorstore


# Использование


if __name__ == '__main__':
    FAISS_INDEX_PATH = r'C:\Users\abgor\OneDrive\Рабочий стол\WebDevelopment_2024-2025\works\K3322\Горлов_Андрей_Борисович\project\mnemos\vectorstore'
    print(load_vectorstore())
    vs = inspect_vectorstore()
    show_sample_documents(vs)
