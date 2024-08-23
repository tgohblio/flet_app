from aimage_factory import ServiceFactory
from falai import FalAI
from huggingface import HuggingFace


class AImage:
    ai_services = ("FALAI", "Huggingface", "Replicate")

    def __init__(self, name):
        """initialize image generation parameters stored in a dict, vendor-specific
        """
        self._parameters = {}
        self._instance = factory.get_service(name)

    def __call__(self, name):
        self._instance = factory.get_service(name)
        return self._instance

    def gen_image(self, prompt, **ignored):
        output_url = self._instance.gen_image(prompt)
        return output_url


factory = ServiceFactory()
factory.register_service('FALAI', FalAI)
factory.register_service('Huggingface', HuggingFace)
