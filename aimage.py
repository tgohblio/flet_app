from aimage_factory import ServiceFactory
from falai import FalAIServiceBuilder
from huggingface import HFServiceBuilder

factory = ServiceFactory()
factory.register_builder('FalAI', FalAIServiceBuilder())
factory.register_builder('Huggingface', HFServiceBuilder())


class AImage:
    ai_services = ("FalAI", "Huggingface", "Replicate")
    model = ("FLUX_DEV", "FLUX_SCHNELL", "FLUX_REALISM", "AURA_FLOW")

    def __init__(self, service_name, model, **kwargs):
        """initialize image generation parameters stored in a dict, vendor-specific
        """
        self._parameters = {}
        self._instance = factory.create(service_name, model)
        if self._instance == None:
            raise Exception("Error! Object not created")

    def __call__(self, service_name, model):
        self._instance = factory.create(service_name, model)
        if self._instance == None:
            raise Exception("Error! Object not created")

    def gen_image(self, prompt, **ignored) -> tuple:
        output, format = self._instance.gen_image(prompt)
        return (output, format)
