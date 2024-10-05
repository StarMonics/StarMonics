import base64
import requests
import json
import os

class ImageInterpreter:
    def __init__(self, api_key, image_dir):
        self.api_key = api_key
        self.image_dir = image_dir  # Diretório das imagens
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }

    def encode_images(self):
        """Converts all image files in a directory to a list of base64 strings."""
        encoded_images = []
        # Listar todas as imagens no diretório e codificar para base64
        for image_name in os.listdir(self.image_dir):
            image_path = os.path.join(self.image_dir, image_name)
            if os.path.isfile(image_path):  # Verifica se é um arquivo
                with open(image_path, "rb") as image_file:
                    encoded_image = base64.b64encode(image_file.read()).decode('utf-8')
                    encoded_images.append(encoded_image)
        return encoded_images

    def interpret_single_image(self, encoded_image):
        """Sends a single image (already encoded) to the OpenAI API for interpretation."""
        payload = {
            "model": "gpt-4o-mini",
            "messages": [
                {
                    "role": "user",
                    "content": "text", "text": "RolePlay as a bot philosopher. Generate a philosophical text about the given image and reflect about the feelings that it evokes on the viewer."
                },
                {
                    "role": "user",
                    "content": {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{encoded_image}"
                        }
                    }
                },
                {
                    "role": "user",
                    "content": "Verify if the produced text makes sense grammatically. If not, correct it."
                },
                {
                    "role": "user",
                    "content": "Remove any introductions. Send only the requested text."
                },
            ],
            "max_tokens": 300
        }

        response = requests.post("https://api.openai.com/v1/chat/completions",
                                 headers=self.headers, json=payload)
        return response.json()

    def interpret_multiple_images(self, encoded_images):
        """Sends multiple images (already encoded) to the OpenAI API and generates a combined response."""
        messages_content = [
            {
                "role": "user",
                "content": "text", "text": "RolePlay as a bot philosopher. Generate a philosophical text about the given image and reflect about the feelings that it evokes on the viewer."
            }
        ]

        # Adiciona cada imagem codificada ao payload
        for encoded_image in encoded_images:
            messages_content.append({
                "role": "user",
                "content": {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{encoded_image}"
                    }
                }
            })

        # Montar o payload para múltiplas imagens
        payload = {
            "model": "gpt-4o-mini",
            "messages": messages_content + [
                {
                    "role": "user",
                    "content": "Verify if the produced text makes sense grammatically. If not, correct it."
                },
                {
                    "role": "user",
                    "content": "Remove any introductions. Send only the requested text."
                },
            ],
            "max_tokens": 300
        }

        response = requests.post("https://api.openai.com/v1/chat/completions",
                                 headers=self.headers, json=payload)
        return response.json()