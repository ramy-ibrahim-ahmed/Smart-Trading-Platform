from typing import Literal
from .interface import BaseVectorDB
from .providers import ChromaDB, QdrantDB


class VectorDBFactory:
    def __init__(self, settings):
        self.settings = settings

    def create(self, provider: Literal["chroma", "qdrant"]) -> BaseVectorDB:
        if provider.lower() == "chroma":
            return ChromaDB(settings=self.settings)
        elif provider.lower() == "qdrant":
            return QdrantDB(settings=self.settings)
        else:
            raise ValueError(f"Unknown provider: {provider}")
