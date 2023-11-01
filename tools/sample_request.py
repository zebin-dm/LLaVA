import time
import json
import requests
import base64
from typing import List
from PIL import Image
from io import BytesIO


class LlavaClient:
    def __init__(
        self,
        addr="http://localhost:40000",
    ) -> None:
        self.addr = addr
        self.headers = {"User-Agent": "LLaVA Client"}
        self.prompt = "A chat between a curious human and an artificial intelligence assistant. The assistant gives helpful, detailed, and polite answers to the human's questions. USER: <image>\n{} ASSISTANT:"

    def get_images(self, image_files: List[str]):
        images = []
        for imf in image_files:
            image = Image.open(imf).convert("RGB")
            max_hw, min_hw = max(image.size), min(image.size)
            aspect_ratio = max_hw / min_hw
            max_len, min_len = 800, 400
            shortest_edge = int(min(max_len / aspect_ratio, min_len, min_hw))
            longest_edge = int(shortest_edge * aspect_ratio)
            W, H = image.size
            if longest_edge != max(image.size):
                if H > W:
                    H, W = longest_edge, shortest_edge
                else:
                    H, W = shortest_edge, longest_edge
                image = image.resize((W, H))

            buffered = BytesIO()
            image.save(buffered, format="PNG")
            img_b64_str = base64.b64encode(buffered.getvalue()).decode()
            images.append(img_b64_str)
        return images

    def post(
        self,
        text: str,
        image_files: List[str],
        temperature: float = 0.2,
        top_p: float = 0.7,
        max_output_tokens: int = 512,
    ):
        assert 0.0 <= temperature <= 1.0
        assert 0.0 <= top_p <= 1.0
        assert 0 < max_output_tokens < 1024
        prompt = self.prompt.format(text)
        pload = {
            "model": "llava-v1.5-13b",
            "prompt": prompt,
            "temperature": float(temperature),
            "top_p": float(top_p),
            "max_new_tokens": min(int(max_output_tokens), 1536),
            "stop": "</s>",
            "images": self.get_images(image_files),
        }
        try:
            # Stream output
            response = requests.post(
                f"{self.addr}/worker_generate_stream",
                headers=self.headers,
                json=pload,
                stream=True,
                timeout=10,
            )
            output = ""
            for chunk in response.iter_lines(decode_unicode=False, delimiter=b"\0"):
                if chunk:
                    data = json.loads(chunk.decode())
                    if data["error_code"] == 0:
                        output = data["text"][len(prompt) :].strip()
                    else:
                        output = data["text"] + f" (error_code: {data['error_code']})"
                    time.sleep(0.03)
            return output

        except requests.exceptions.RequestException as e:
            server_error_msg = "**NETWORK ERROR DUE TO HIGH TRAFFIC. PLEASE REGENERATE OR REFRESH THIS PAGE.**"
            raise Exception(server_error_msg)
            return None


if __name__ == "__main__":
    text = "What are the things I should be cautious about when I visit here?"
    image_files = [
        "llava/serve/examples/waterview.jpg",
    ]
    client = LlavaClient()
    output = client.post(
        text=text,
        image_files=image_files,
    )
    print(output)
