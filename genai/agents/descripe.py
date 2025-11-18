from ..store import BaseNLP, BaseVectorDB, PromptFactory
from ..core import get_settings, TaskModelConfig

SETTINGS = get_settings()


class DescripeAgent:
    def __init__(self, nlp: BaseNLP, vectordb: BaseVectorDB):
        self.nlp = nlp
        self.vectordb = vectordb
        self.prompt_factory = PromptFactory()

    async def descripe_cars(self, contents: list[str]):
        descriptions = list()
        for car in contents:
            prompt = self.prompt_factory.get_prompt("descripe").format(car_features=car)
            desc = self.nlp.chat(
                TaskModelConfig.BESTFIT_DESCRIPE.value,
                "Arabic description writer for descriping the real state of a car.",
                prompt,
            )
            descriptions.append(desc)
        return descriptions

    async def process_cars(self, namespace: str, contents: list[str], ids: list):
        embeddings = self.nlp.embed(contents)
        metadata = [{"id": car_id, "text": text} for text, car_id in zip(contents, ids)]
        self.vectordb.add_points(namespace, ids, embeddings, metadata)
