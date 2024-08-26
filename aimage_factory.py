class ServiceFactory:
    def __init__(self):
        self._services = {}

    def register_builder(self, name, service_builder):
        """Select the service provider and text-to-image model"""
        self._services[name] = service_builder

    def create(self, name, model):
        service = self._services.get(name)
        if not service:
            raise ValueError(name)
        return service(model)
