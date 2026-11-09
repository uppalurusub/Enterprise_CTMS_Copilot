"""
===========================================================
Enterprise CTMS Copilot
RAG Implementation
===========================================================
"""

from typing import Dict, List, Optional

from app.config.settings import settings
logger = settings.get_logger()

from langchain_core.documents import Document

from app.vectorstore.vector_db import vector_db

from app.schemas.response_model import (
    RetrievalExecution,
    SourceDocument
)


class RAGImplementation:
    """
    Enterprise Retrieval Augmented Generation (RAG)

    Responsibilities

    • Retrieve Documents
    • Metadata Filtering
    • Similarity Search
    • MMR Search
    • Build RAG Context
    • Build Source Metadata
    """

    def __init__(self):

        logger.info("Initializing RAG Implementation...")

        self.vector_db = vector_db

        logger.success("RAG Implementation Initialized Successfully.")

    ####################################################################
    # Similarity Search
    ####################################################################

    def similarity_search(
        self,
        query: str,
        top_k: int = 5
    ) -> List[Document]:

        logger.info(f"Similarity Search : {query}")

        documents = self.vector_db.similarity_search(
            query=query,
            k=top_k
        )

        logger.success(
            f"Retrieved {len(documents)} documents."
        )

        return documents

    ####################################################################
    # Metadata Filter Search
    ####################################################################

    def search_with_filter(
        self,
        query: str,
        metadata: Dict,
        top_k: int = 5
    ) -> List[Document]:

        logger.info("Executing Metadata Search")

        documents = self.vector_db.search_with_filter(
            query=query,
            filters=metadata,
            k=top_k
        )

        logger.success(
            f"Retrieved {len(documents)} documents."
        )

        return documents

    ####################################################################
    # MMR Search
    ####################################################################

    def mmr_search(
        self,
        query: str,
        top_k: int = 5
    ) -> List[Document]:

        logger.info("Executing MMR Search")

        documents = self.vector_db.mmr_search(
            query=query,
            k=top_k
        )

        logger.success(
            f"Retrieved {len(documents)} documents."
        )

        return documents

    ####################################################################
    # Build Context
    ####################################################################

    def build_context(
        self,
        documents: List[Document]
    ) -> str:

        logger.info("Building RAG Context")

        context = []

        for index, doc in enumerate(documents, start=1):

            context.append(
                f"""
Document {index}

Document Name :
{doc.metadata.get("document_name", "Unknown")}

Document Type :
{doc.metadata.get("document_type", "Unknown")}

Content

{doc.page_content}
"""
            )

        logger.success("Context Created Successfully.")

        return "\n".join(context)

    ####################################################################
    # Build Sources
    ####################################################################

    def build_sources(
        self,
        documents: List[Document]
    ) -> List[SourceDocument]:

        logger.info("Building Source Metadata")

        sources = []

        for doc in documents:

            source = SourceDocument(

                document_name=doc.metadata.get(
                    "document_name",
                    "Unknown"
                ),

                document_type=doc.metadata.get(
                    "document_type",
                    "Unknown"
                ),

                page_number=doc.metadata.get(
                    "page_number"
                ),

                chunk_id=doc.metadata.get(
                    "chunk_id"
                ),

                relevance_score=doc.metadata.get(
                    "score"
                )
            )

            sources.append(source)

        logger.success(
            f"Generated {len(sources)} sources."
        )

        return sources

    ####################################################################
    # Retrieve
    ####################################################################

    def retrieve(
        self,
        question: str,
        top_k: int = 5,
        metadata: Optional[Dict] = None,
        search_type: str = "similarity"
    ):

        logger.info("=" * 80)
        logger.info("Executing Enterprise RAG")

        if metadata:

            documents = self.search_with_filter(
                query=question,
                metadata=metadata,
                top_k=top_k
            )

        elif search_type.lower() == "mmr":

            documents = self.mmr_search(
                query=question,
                top_k=top_k
            )

        else:

            documents = self.similarity_search(
                query=question,
                top_k=top_k
            )

        context = self.build_context(documents)

        sources = self.build_sources(documents)

        rag_execution = RetrievalExecution(

            executed=True,

            retrieved_chunks=len(documents),

            top_k=top_k,

            sources=sources
        )

        logger.success("Enterprise RAG Completed Successfully.")

        return {

            "documents": documents,

            "context": context,

            "sources": sources,

            "rag_execution": rag_execution
        }


##########################################################################
# Singleton Instance
##########################################################################

rag = RAGImplementation()