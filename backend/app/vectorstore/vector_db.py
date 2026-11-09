import os
from typing import List, Dict, Any, Optional

from dotenv import load_dotenv
from app.config.settings import settings
logger = settings.get_logger()

from langchain_chroma import Chroma

from langchain_core.documents import Document

from langchain_openai import OpenAIEmbeddings
from langchain_openai import AzureOpenAIEmbeddings

from langchain_huggingface import HuggingFaceEmbeddings

load_dotenv()


class VectorDatabase:
    """
    Enterprise ChromaDB Wrapper
    """

    _instance = None

    def __new__(cls):

        if cls._instance is None:
            cls._instance = super().__new__(cls)

        return cls._instance

    def __init__(self):

        if hasattr(self, "_initialized"):
            return

        self._initialized = True

        logger.info("Initializing Chroma Vector Database...")

        self.persist_directory = os.getenv(
            "CHROMA_DB_PATH",
            "./vectorstore/chroma_db"
        )

        self.collection_name = os.getenv(
            "CHROMA_COLLECTION",
            "enterprise_ctms"
        )

        self.embedding_provider = os.getenv(
            "EMBEDDING_PROVIDER",
            "huggingface"
        ).lower()

        self.embedding_model = self._load_embeddings()

        self.vectorstore = Chroma(
            collection_name=self.collection_name,
            persist_directory=self.persist_directory,
            embedding_function=self.embedding_model
        )

        logger.success(
            f"Connected to Chroma Collection : {self.collection_name}"
        )

    def _build_where_filter(
        self,
        filters: dict | None
    ):

        if not filters:

            return None

        if len(filters) == 1:

            key = next(iter(filters))

            return {
                key: filters[key]
            }

        return {

            "$and": [

                {
                    k: v
                }

                for k, v in filters.items()

            ]
        }


    ###################################################################
    # Embeddings
    ###################################################################

    def _load_embeddings(self):

        logger.info(f"Embedding Provider : {self.embedding_provider}")

        if self.embedding_provider == "openai":

            return OpenAIEmbeddings()

        elif self.embedding_provider == "azure":

            return AzureOpenAIEmbeddings()

        else:

            return HuggingFaceEmbeddings(
                model_name=os.getenv(
                    "HUGGINGFACE_MODEL",
                    "sentence-transformers/all-MiniLM-L6-v2"
                )
            )

    ###################################################################
    # Add Documents
    ###################################################################

    def add_documents(
        self,
        documents: List[Document]
    ):

        logger.info(f"Adding {len(documents)} documents")

        ids = self.vectorstore.add_documents(documents)

        logger.success("Documents Added Successfully")

        return ids

    ###################################################################
    # Similarity Search
    ###################################################################

    def similarity_search(
        self,
        query: str,
        k: int = 5
    ):

        logger.info(f"Similarity Search : {query}")

        return self.vectorstore.similarity_search(
            query,
            k=k
        )

    ###################################################################
    # Similarity Search with Score
    ###################################################################

    def similarity_search_with_score(
        self,
        query: str,
        k: int = 5
    ):

        logger.info("Similarity Search with Score")

        return self.vectorstore.similarity_search_with_score(
            query,
            k=k
        )

    ###################################################################
    # Metadata Search
    ###################################################################

    def search_with_filter(
        self,
        query: str,
        filters,
        k: int = 5
    ):

        where = self._build_where_filter(filters)

        logger.info(f"Where Filter : {where}")

        return self.vectorstore.similarity_search(

            query=query,

            k=k,

            filter=where

        )

    ###################################################################
    # Max Marginal Relevance Search
    ###################################################################

    def mmr_search(
        self,
        query: str,
        k: int = 5,
        fetch_k: int = 20
    ):

        logger.info("MMR Search")

        return self.vectorstore.max_marginal_relevance_search(
            query=query,
            k=k,
            fetch_k=fetch_k
        )

    ###################################################################
    # Delete
    ###################################################################

    def delete_documents(
        self,
        ids: List[str]
    ):

        logger.warning(f"Deleting {len(ids)} documents")

        self.vectorstore.delete(ids=ids)

        logger.success("Documents Deleted")

    ###################################################################
    # Delete Collection
    ###################################################################

    def delete_collection(self):

        logger.warning("Deleting Collection")

        self.vectorstore.delete_collection()

        logger.success("Collection Deleted")

    ###################################################################
    # Count Documents
    ###################################################################

    def count(self):

        collection = self.vectorstore._collection

        return collection.count()

    ###################################################################
    # Get Collection Info
    ###################################################################

    def info(self):

        collection = self.vectorstore._collection

        return {
            "collection": self.collection_name,
            "documents": collection.count(),
            "path": self.persist_directory
        }

    ###################################################################
    # Reset Database
    ###################################################################

    def reset(self):

        logger.warning("Resetting Vector Database")

        self.delete_collection()

        self.vectorstore = Chroma(
            collection_name=self.collection_name,
            persist_directory=self.persist_directory,
            embedding_function=self.embedding_model
        )

        logger.success("Vector Database Reset Completed")


##########################################################################
# Singleton Instance
##########################################################################

vector_db = VectorDatabase()