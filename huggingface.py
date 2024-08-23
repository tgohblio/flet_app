import enum
import sys

from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv())  # read local .env file


class HuggingFace:
    def __init__(self):
        print("HF init")

    def gen_image(self, prompt: str, size="", infer_steps=28, cfg_val=3.5, num_images=1, safety_on=True) -> list:
        print("HF photo")
        return ("HF photo")
