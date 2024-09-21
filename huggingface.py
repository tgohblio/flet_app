import base64

from gradio_client import Client
from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv())  # read local .env file


class HuggingFace:
    model_dict = { 
        "FLUX_DEV": "black-forest-labs/FLUX.1-dev", 
        "FLUX_SCHNELL": "black-forest-labs/FLUX.1-schnell",
        "FLUX_REALISM": "DamarJati/FLUX.1-RealismLora"
    }

    def __init__(self, model="FLUX_SCHNELL"):
        self.model = model
        self.model_url = HuggingFace.model_dict[model]
        self._photos = []
        self.client = Client(self.model_url)

    def gen_image(self, prompt: str, size="", infer_steps=28, cfg_val=3.5, num_images=1, safety_on=True) -> tuple:
        if not prompt:
            raise Exception
        
        try:
            match self.model:
                case "FLUX_SCHNELL":
                    # maximum number of steps is 4
                    result = self.client.predict(
                            prompt=prompt,
                            seed=0,
                            randomize_seed=True,
                            width=1024,
                            height=1024,
                            num_inference_steps=4,
                            api_name="/infer"
                    )
                case "FLUX_REALISM":
                    result = self.client.predict(
                            prompt=prompt,
                            cfg_scale=3.2,
                            steps=infer_steps,
                            randomize_seed=False,
                            seed=3981632454,
                            width=1024,
                            height=1024,
                            lora_scale=0.85,
                            api_name="/run_lora"
                    )
                case _:
                    result = self.client.predict(
                            prompt=prompt,
                            seed=0,
                            randomize_seed=True,
                            width=1024,
                            height=1024,
                            guidance_scale=cfg_val,
                            num_inference_steps=infer_steps,
                            api_name="/infer"
                    )

            # result returns a tuple (file path, seed)
            file_path = result[0]
            # read the image file in binary mode and encode as base64 string
            with open(file_path, "rb") as f:
                image_bytes = f.read()
                base64_str = base64.b64encode(image_bytes).decode('utf-8')

            self._photos.clear()
            self._photos.append(base64_str)
            return (self._photos[0], "base64")

        except Exception as e:
            print(f"Exception caught from Huggingface: {e}")
            self._photos.clear()
            self._photos.append("./assets/blank-photo.jpg")
            return (self._photos[0], "url")

class HFServiceBuilder:
    def __init__(self):
        self._instance = None

    def __call__(self, model):
        if model not in HuggingFace.model_dict:
            self._instance = None
        elif not self._instance:
            self._instance = HuggingFace(model)
        elif self._instance and model != self._instance.model:
            self._instance.model = model
            self._instance.model_url = HuggingFace.model_dict[model]
            self._instance.client = Client(self._instance.model_url)
        return self._instance
