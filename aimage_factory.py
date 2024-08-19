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
