import chromadb
from ..interface import BaseVectorDB
from ....core import ManyCars, Car


class ChromaDB(BaseVectorDB):
    def __init__(self, settings):
        self.settings = settings
        self.client = None

    def connect(self):
        self.client = chromadb.PersistentClient(path=self.settings.CHROMADB_PATH)

    def create_collection(self, name):
        self.client.create_collection(
            name=name,
            configuration={"hnsw": {"space": "cosine", "ef_construction": 200}},
        )

    def add_points(self, collection_name, ids, embeddings, metadata):
        collection = self.client.get_collection(name=collection_name)
        collection.add(ids=ids, embeddings=embeddings, metadatas=metadata)

    def semantic_search(self, collection_name, vector, top_k):
        collection = self.client.get_collection(name=collection_name)
        results = collection.query(query_embeddings=vector, n_results=top_k)
        metadata_list = results["metadatas"][0]
        obj = ManyCars(cars=[Car(**res) for res in metadata_list])
        return obj

    def metadata_filter(self, collection_name, key, value):
        collection = self.client.get_collection(name=collection_name)
        results = collection.get(where={key: value})
        return results["metadatas"][0]

    def disconnect(self): ...
