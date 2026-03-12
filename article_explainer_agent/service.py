"""Service components for article explainer agent."""

import os
import tempfile
from typing import List
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.schema import Document


class ContentLoader:
    """Loads and prepares text content from .pdf documents using PyPDF."""

    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 100):
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size, chunk_overlap=chunk_overlap
        )

    def load(self, file_path: str) -> List[Document]:
        """Load and split content from a file."""
        if file_path.endswith(".pdf"):
            loader = PyPDFLoader(file_path)
        else:
            raise ValueError(f"Unsupported file format: {file_path}")

        docs = loader.load()
        return self.splitter.split_documents(docs)

    def get_text(self, file_path: str, max_chunks: int = None) -> str:
        """Load content and return concatenated plain text."""
        docs = self.load(file_path)
        if max_chunks:
            docs = docs[:max_chunks]
        return "\n\n".join([doc.page_content for doc in docs])


def get_chat_model(model_name: str = "openai:gpt-4.1-mini"):
    """Returns a LangChain chat model initialized with API key from the environment."""
    from dotenv import load_dotenv
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        # Fallback to OpenRouter if no OpenAI key
        openrouter_api_key = os.getenv("OPENROUTER_API_KEY")
        if openrouter_api_key:
            from langchain_openai import ChatOpenAI
            from pydantic import SecretStr
            return ChatOpenAI(
                model_name="gpt-4o",
                openai_api_key=SecretStr(openrouter_api_key),
                openai_api_base="https://openrouter.ai/api/v1",
                temperature=0,
            )
        else:
            raise ValueError("No API key provided. Set OPENAI_API_KEY or OPENROUTER_API_KEY environment variable.")
    
    from langchain.chat_models import init_chat_model
    return init_chat_model(model=model_name, api_key=api_key)
