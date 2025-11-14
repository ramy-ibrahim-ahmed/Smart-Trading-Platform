from qdrant_client import QdrantClient, models
from ..interface import BaseVectorDB


class QdrantDB(BaseVectorDB):
    def __init__(self, settings):
        self.settings = settings
        self.client = None

    def connect(self):
        self.client = QdrantClient(host="qdrant", grpc_port=6334, prefer_grpc=True)

    def disconnect(self):
        if self.client:
            self.client.close()

    def create_collection(self, name):
        self.client.create_collection(
            collection_name=name,
            vectors_config=models.VectorParams(
                size=self.settings.EMBEDDING_SIZE, distance=models.Distance.COSINE
            ),
        )

    def add_points(self, collection_name, ids, embeddings, metadata):
        points = [
            models.PointStruct(id=id, vector=embedding, payload=payload)
            for id, embedding, payload in zip(ids, embeddings, metadata)
        ]
        self.client.upsert(collection_name=collection_name, points=points, wait=True)

    def semantic_search(self, collection_name, vectors, top_k):
        nearest = self.qdrant_client.query_batch_points(
            collection_name=collection_name,
            requests=[
                models.QueryRequest(query=e, with_payload=True, limit=top_k)
                for e in vectors
            ],
        )

        all_payloads = [point.payload for result in nearest for point in result.points]

        return [
            dict(item_tuple)
            for item_tuple in set(tuple(sorted(d.items())) for d in all_payloads)
        ]

    def metadata_filter(self, collection_name, key, value): ...
