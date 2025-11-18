from ..store import BaseNLP, BaseVectorDB, PromptFactory
from ..core import get_settings, ManyCars, TaskModelConfig

SETTINGS = get_settings()


class BestFitAgent:
    def __init__(self, nlp: BaseNLP, vectordb: BaseVectorDB):
        self.nlp = nlp
        self.vectordb = vectordb
        self.prompt_factory = PromptFactory()

    def _enhance_query(self, user_message):
        instructions = self.prompt_factory.get_prompt("query_write")
        messages = [self.nlp.create_user_message(user_message)]
        return self.nlp.chat(
            TaskModelConfig.BESTFIT_QUERY.value, instructions, messages
        )

    def _respond(self, user_message, results: ManyCars):
        prompt = self.prompt_factory.get_prompt("recommend")
        messages = prompt.format(user_message=user_message, retrieved_cars=results)
        return self.nlp.chat(
            TaskModelConfig.BESTFIT_RESPOND.value, "Arabic AI Assistant", messages
        )

    def run(self, user_message):
        enhanced_query = self._enhance_query(user_message)
        embeddings = self.nlp.embed([enhanced_query])
        nearest = self.vectordb.semantic_search(SETTINGS.CARS_COLLECTION, embeddings, 3)
        return self._respond(user_message, nearest)
