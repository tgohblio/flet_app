import aimage_factory

from aimage_factory import factory

class AImage:
    def __init__(self, name):
        """initialize image generation parameters stored in a dict, vendor-specific
        """
        self._parameters = {}
        self._service_provider = factory.get_service(name)

    def gen_image(self, prompt, **ignored):
        output_url = self._service_provider.gen_image(prompt)
        return output_url


img = AImage("FALAI")
output = img.gen_image("hello")
print(output)