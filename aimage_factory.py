import falai
from falai import FalAI

class ServiceFactory:
    def __init__(self):
        self._services = {}

    def register_service(self, name, service):
        self._services[name] = service

    def get_service(self, name):
        service = self._services.get(name)
        if not service:
            raise ValueError(name)
        return service() # instantiate the class

factory = ServiceFactory()
factory.register_service('FALAI', FalAI)
# factory.register_service('HUGGINGFACE', HuggingFace)
# factory.register_service('REPLICATE', Replicate)