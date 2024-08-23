import enum
import sys

from gradio_client import Client
from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv())  # read local .env file


class HuggingFace:
    model_dict = { 
        "FLUX_DEV": "black-forest-labs/FLUX.1-dev", 
        "FLUX_SCHNELL": "black-forest-labs/FLUX.1-schnell"
    }

    def __init__(self, model="FLUX_SCHNELL"):
        self._photos = []
        if model in HuggingFace.model_dict:
            self._model = HuggingFace.model_dict[model]
        else:
            print("Invalid model specified")
            sys.exit(1)
        self._client = Client(self._model)

    def gen_image(self, prompt: str, size="", infer_steps=28, cfg_val=3.5, num_images=1, safety_on=True) -> list:
        if prompt != "":
            if self._model == HuggingFace.model_dict["FLUX_SCHNELL"]:
                # maximum number of steps is 4
                result = self._client.predict(
                        prompt=prompt,
                        seed=0,
                        randomize_seed=True,
                        width=1024,
                        height=1024,
                        num_inference_steps=4,
                        api_name="/infer"
                ) # returns a tuple of (filepath, seed)
            else:
                result = self._client.predict(
                        prompt=prompt,
                        seed=0,
                        randomize_seed=True,
                        width=1024,
                        height=1024,
                        guidance_scale=cfg_val,
                        num_inference_steps=infer_steps,
                        api_name="/infer"
                ) # returns a tuple of (filepath, seed)
            self._photos.append(result[0])
            return self._photos
