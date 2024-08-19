import falai
import aimage_factory

factory = aimage_factory.ServiceFactory()

factory.register_service('FALAI', FalAISvc)
factory.register_service('HUGGINGFACE', HuggingFaceSvc)
factory.register_service('REPLICATE', ReplicateSvc)

class AImage:
    def __init__(self):
        """initialize image generation parameters stored in a dict, vendor-specific
        """
        self._parameters = {}

    def __callable__(self, prompt, name):
        service_provider = factory.get_service(name)
        service_provider.send_request(prompt)
        return service_provider.output_url()

