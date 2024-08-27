import enum
import sys

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
        self._client = Client(self.model_url)

    def gen_image(self, prompt: str, size="", infer_steps=28, cfg_val=3.5, num_images=1, safety_on=True) -> list:
        if not prompt:
            return []
        
        match self.model:
            case "FLUX_SCHNELL":
                # maximum number of steps is 4
                result = self._client.predict(
                        prompt=prompt,
                        seed=0,
                        randomize_seed=True,
                        width=1024,
                        height=1024,
                        num_inference_steps=4,
                        api_name="/infer"
                )
            case "FLUX_REALISM":
                result = self._client.predict(
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
                result = self._client.predict(
                        prompt=prompt,
                        seed=0,
                        randomize_seed=True,
                        width=1024,
                        height=1024,
                        guidance_scale=cfg_val,
                        num_inference_steps=infer_steps,
                        api_name="/infer"
                )

        # result returns a tuple of (filepath, seed)
        self._photos.append(result[0])
        return self._photos


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
            self._client = Client(self._instance.model_url)
        return self._instance
