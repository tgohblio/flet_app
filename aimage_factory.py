class ServiceFactory:
    def __init__(self):
        self._services = {}

    def register_service(self, name, service_builder):
        """Select the service provider and text-to-image model"""
        self._services[name] = service_builder

    def create(self, name, model):
        service = self._services.get(name)
        if not service:
            raise ValueError(name)
        return service(model)

    def select_model(self, name, model):
        service = self._services.get(name)
        service.select_model(model)