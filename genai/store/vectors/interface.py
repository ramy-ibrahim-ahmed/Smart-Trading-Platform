from abc import ABC, abstractmethod


class BaseVectorDB(ABC):
    @abstractmethod
    def connect(self): ...

    @abstractmethod
    def disconnect(self): ...

    @abstractmethod
    def create_collection(self, name: str): ...

    @abstractmethod
    def add_points(
        self,
        collection_name: str,
        ids: list[str],
        embeddings: list[list[float]],
        metadata: dict,
    ): ...

    @abstractmethod
    def semantic_search(
        self, collection_name: str, vectors: list[float], top_k: int
    ) -> list[dict]: ...

    @abstractmethod
    def metadata_filter(self, collection_name, key, value): ...
