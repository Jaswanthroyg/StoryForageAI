import os
import requests
from dotenv import load_dotenv


load_dotenv()


class ImageGenerator:

    def __init__(self):

        self.api_key = os.getenv("PIXAZO_API_KEY")

        if not self.api_key:
            raise ValueError(
                "PIXAZO_API_KEY not found in .env"
            )

        self.url = (
            "https://gateway.pixazo.ai/"
            "flux-1-schnell/v1/getData"
        )

    def generate_image(self, prompt, output_path):

        headers = {
            "Content-Type": "application/json",
            "Cache-Control": "no-cache",
            "Ocp-Apim-Subscription-Key": self.api_key
        }

        data = {
            "prompt": prompt,
            "num_steps": 4,
            "seed": 15,
            "height": 576,
            "width": 1024
        }

        print("Generating image...")

        response = requests.post(
            self.url,
            headers=headers,
            json=data,
            timeout=120
        )

        if response.status_code != 200:
            raise RuntimeError(
                f"Pixazo API error "
                f"{response.status_code}: "
                f"{response.text}"
            )

        result = response.json()

        print("Pixazo response:")
        print(result)

        image_url = result.get("output")

        if not image_url:
            raise RuntimeError(
                f"No image URL returned by Pixazo:\n{result}"
            )

        print("Downloading image...")

        image_response = requests.get(
            image_url,
            timeout=120
        )

        if image_response.status_code != 200:
            raise RuntimeError(
                f"Failed to download image: "
                f"{image_response.status_code}"
            )

        output_directory = os.path.dirname(output_path)

        if output_directory:
            os.makedirs(
                output_directory,
                exist_ok=True
            )

        with open(output_path, "wb") as file:
            file.write(image_response.content)

        print("Image saved successfully.")

        return output_path