"""Service components for article explainer agent."""

import os
from typing import Any

from langchain.schema import Document
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

# Error messages
UNSUPPORTED_FILE_ERROR = "Unsupported file format: {file_path}"
NO_API_KEY_ERROR = "No API key provided. Set OPENAI_API_KEY or OPENROUTER_API_KEY environment variable."


class ContentLoader:
    """Loads and prepares text content from .pdf documents using PyPDF."""

    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 100):
        """Initialize content loader with chunk size and overlap."""
        self.splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)

    def load(self, file_path: str) -> list[Document]:
        """Load and split content from a file."""
        if file_path.endswith(".pdf"):
            loader = PyPDFLoader(file_path)
        else:
            raise ValueError(UNSUPPORTED_FILE_ERROR.format(file_path=file_path))

        docs = loader.load()
        return self.splitter.split_documents(docs)

    def get_text(self, file_path: str, max_chunks: int | None = None) -> str:
        """Load content and return concatenated plain text."""
        docs = self.load(file_path)
        if max_chunks:
            docs = docs[:max_chunks]
        return "\n\n".join([doc.page_content for doc in docs])


def get_chat_model(model_name: str = "openai:gpt-4.1-mini") -> Any:
    """Return a LangChain chat model initialized with API key from the environment."""
    from dotenv import load_dotenv

    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        # Fallback to OpenRouter if no OpenAI key
        openrouter_api_key = os.getenv("OPENROUTER_API_KEY")
        if openrouter_api_key:
            from langchain_openai import ChatOpenAI
            from pydantic import SecretStr

            return ChatOpenAI(  # type: ignore[call-arg]
                model_name="gpt-4o",
                openai_api_key=SecretStr(openrouter_api_key),
                openai_api_base="https://openrouter.ai/api/v1",
                temperature=0,
            )
        else:
            raise ValueError(NO_API_KEY_ERROR)

    from langchain.chat_models import init_chat_model

    return init_chat_model(model=model_name, api_key=api_key)
