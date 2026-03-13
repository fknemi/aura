import os
import requests
from urllib.parse import quote
import random

session = requests.Session()
session.headers.update({"Authorization": f"Bearer {os.getenv('POLLINATIONS_API_KEY')}"})

def gen_image(prompt, style, width=1024, height=1024, seed=-1, enhance=False, negative_prompt="", safe=False, model="flux"):
    params = {
        "model": model,
        "width": width,
        "height": height,
        "seed": seed,
        "enhance": enhance,
        "safe": safe,
    }
    if negative_prompt:
        params["negative_prompt"] = negative_prompt

    response = session.get(
        f"https://gen.pollinations.ai/image/{quote(prompt + style)}",
        params=params,
    )
    response.raise_for_status()
    return response.content
