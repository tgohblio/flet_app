import fal_client
import enum, sys

from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv()) # read local .env file


class FalAI():
    """Using image generator API from FalAI"""
    # enums
    class ImageSize(enum.IntEnum):
        SQUARE_HD = 0
        SQUARE = 1
        PORTRAIT_4_3 = 2
        PORTRAIT_16_9 = 3
        LANDSCAPE_4_3 = 4
        LANDSCAPE_16_9 = 5

    # class variables
    image_size = ["square_hd", "square", "portrait_4_3", "portrait_16_9", "landscape_4_3", "landscape_16_9"]
    model_dict = { 
        "AURA_FLOW": "fal-ai/aura-flow",
        "FLUX_DEV": "fal-ai/flux/dev", 
        "FLUX_SCHNELL": "fal-ai/flux/schnell",
        "FLUX_PRO": "fal-ai/flux-pro"
    }

    def __init__(self, model="FLUX_SCHNELL") -> None:
        self.photos = []
        if model in FalAI.model_dict:
            self.model = FalAI.model_dict[model]
        else:
            print("Invalid model specified")
            sys.exit(1)


    def gen_image(self, prompt: str, size=ImageSize.LANDSCAPE_4_3, infer_steps=28, cfg_val=3.5, num_images=1, safety_on=True) -> list:
        if prompt != "":
            if self.model == "fal-ai/flux/schnell":
                # maximum number of steps is 4
                infer_steps = 4
            self.handler = fal_client.submit(
                self.model,
                arguments={
                    "prompt": prompt,
                    "image_size": FalAI.image_size[size],
                    "num_inference_steps": infer_steps,
                    "guidance_scale": cfg_val,
                    "num_images": num_images,
                    "enable_safety_checker": safety_on
                },
            )

            for event in self.handler.iter_events(with_logs=True):
                if isinstance(event, fal_client.InProgress):
                    print("Request in progress")
                    # print(event)

            result = self.handler.get() # block until returns a result

            self.photos.clear() # clears previous results
            for index in range(num_images):
                img = result["images"][index]["url"]
                self.photos.append(img)
                print(img)
        else:
            print("Error! Prompt is empty")
        return self.photos

    """
    returned output:

    {
        "seed": 1712202032,
        "images": [
            {
                "url": "https://fal.media/files/zebra/dfc2ZSOuUdsjePN4ijAVQ.png",
                "width": 1024,
                "height": 768,
                "content_type": "image/jpeg"
            },
            {
                "url": "https://fal.media/files/zebra/j6bAAn4cKCAV6euoyrHPJ.png",
                "width": 1024,
                "height": 768,
                "content_type": "image/jpeg"
            }
        ],
        "prompt": "A rebel leader rallying her forces in a dystopian future in black and red in an art piece, in the style of action painter, grunge beauty, Marvel Comics, darkly romantic illustrations, messy, realistic figures ",
        "timings": {
            "inference": 4.384439425077289
        },
        "has_nsfw_concepts": [
            false,
            false
        ]
    """
    # generate_image(
    #     prompt="selfie shot of spiderman falling on his back from the sky, waving a mini singapore flag, against a backdrop of dark green army parachuters over the singapore bay",
    #     size = ImageSize.LANDSCAPE_4_3,
    #     num_images=4,
    #     safety_on=False           
    # )
