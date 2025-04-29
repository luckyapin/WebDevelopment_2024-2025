import numpy as np
from langchain_community.vectorstores import FAISS
from langchain_ollama import OllamaEmbeddings
from langchain_core.documents import Document
from typing import List, Dict, Any
import json
import ollama
if __name__ == '__main__':
    import ingest, fragment_splitter, parse_fragment
else:
    from . import ingest, fragment_splitter, parse_fragment

EMBEDDING_MODEL = "mxbai-embed-large"
FAISS_INDEX_PATH = "vectorstore"

DATA_JSON_PATH = "data.json"
VECTOR_DIMENSION = 1024  # mxbai-embed-large создает векторы размерности 1024




def get_embeddings(texts: List[str]) -> np.ndarray:
    """Получает эмбеддинги через Ollama"""
    embeddings = []
    for text in texts:
        response = ollama.embeddings(model=EMBEDDING_MODEL, prompt=text)
        embeddings.append(response["embedding"])
    return np.array(embeddings).astype('float32')


def recursive_text_extractor(data: Dict[str, Any], texts: List[str]) -> None:
    """Рекурсивно извлекает все текстовые поля из фрагмента"""
    if isinstance(data, dict):
        for key, value in data.items():
            if key == 'text' and isinstance(value, str):
                texts.append(value)
            elif isinstance(value, (dict, list)):
                recursive_text_extractor(value, texts)
    elif isinstance(data, list):
        for item in data:
            recursive_text_extractor(item, texts)



class VectorStoreManager:
    def __init__(self):
        self.embeddings = OllamaEmbeddings(model=EMBEDDING_MODEL)
        self.vectorstore = None

    def create_store(self, documents: List[Document]):
        self.vectorstore = FAISS.from_documents(
            documents=documents,
            embedding=self.embeddings
        )

    def save_store(self):
        if self.vectorstore:
            self.vectorstore.save_local(FAISS_INDEX_PATH)

    def load_store(self):
        self.vectorstore = FAISS.load_local(
            FAISS_INDEX_PATH,
            self.embeddings,
            allow_dangerous_deserialization=True
        )


def fragment_to_documents(fragment: Dict) -> List[Document]:
    """Конвертирует кастомные фрагменты в Documents LangChain"""
    texts = []
    recursive_text_extractor(fragment, texts)

    return [
        Document(
            page_content=text,
            metadata={
                "fragment_type": fragment.get("type"),
                "note_date": fragment.get("note_date"),
                "source_file": fragment.get("source_file"),
                "original_title": fragment.get("original_title")
            }
        ) for text in texts
    ]


def full_pipeline(notes_dir: str):
    manager = VectorStoreManager()
    all_documents = []

    notes = ingest.load_notes_from_folder(notes_dir)

    for note in notes:
        fragments = fragment_splitter.split_text_by_headers(note)
        for frag in fragments:
            print(frag)
            parsed = parse_fragment.parse_fragment(frag)
            print(parsed)
            all_documents.extend(fragment_to_documents(
                json.loads(parsed.model_dump_json())
            ))

    # Создание и сохранение хранилища
    manager.create_store(all_documents)
    manager.save_store()
    print(f"Saved {len(all_documents)} documents")


if __name__ == "__main__":
    full_pipeline(r"C:\Users\abgor\OneDrive\Рабочий стол\WebDevelopment_2024-2025\works\K3322\Горлов_Андрей_Борисович\project\mnemos\media")
