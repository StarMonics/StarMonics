import base64
import requests
import json
import os
from PIL import Image
import io

class ImageInterpreter:
    def __init__(self, api_key, image_dir):
        self.api_key = api_key
        self.image_dir = image_dir
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }

    def encode_image(self):
    
        

        image_name = os.path.basename(self.image_dir)

        # Abrir a imagem usando Pillow
        with Image.open(self.image_dir) as img:
            # Redimensionar a imagem para 500x500
            img_resized = img.resize((500, 500))
            
            # Salvar a imagem redimensionada em um buffer de bytes
            buffer = io.BytesIO()
            img_resized.save(buffer, format=img.format)
            buffer.seek(0)
            
            # Ler os bytes do buffer
            image_bytes = buffer.read()
            
            # Codificar a imagem em base64
            encoded_image = base64.b64encode(image_bytes).decode('utf-8')

        return encoded_image, image_name

    def interpret_single_image(self, encoded_image):
        payload = {
            "model": "gpt-4o-mini",
            "messages": [
                {
                    "role": "system",
                    "content": "RolePlay as a musical and artistic bot. Generate a text translating the emotion that the image evokes considering its characteristics. Consider that the given images are from space."
                },
                { 
                    "role": "system",
                    "content": "Example: If there is a star on the image, it is possible to explicit: 'The image evokes a feeling of loneliness by the presence of only one star.'"
                },
                {
                    "role": "system",
                    "content": "The poem must be short, maximum of eight lines."
                },
                {
                    "role": "system",
                    "content": "Verify if the produced text makes sense grammatically. If not, correct it."
                },
                {
                    "role": "system",
                    "content": "Remove any introductions. Send only the requested text."
                },
                
                {
                    "role": "user",
                    "content": f"data:image/jpeg;base64,{encoded_image}"
                },
            ],
            "max_tokens": 300
        }

        try:
            response = requests.post("https://api.openai.com/v1/chat/completions", headers=self.headers, json=payload)
            response_data = response.json()
            # Check if 'choices' is in the response
            if 'choices' in response_data and response_data['choices']:
                return response_data['choices'][0]['message']['content']
            else:
                return f"Error: Unexpected API response format: {response_data}"
        except requests.RequestException as e:
            return f"Error: API request failed with message: {str(e)}"

    # def interpret_single_image_for_all(self, encoded_images, image_names):
    #     descriptions = []
    #     for encoded_image, image_name in zip(encoded_images, image_names):
    #         result = self.interpret_single_image(encoded_image)
    #         descriptions.append({
    #             "image_name": image_name,
    #             "description": result
    #         })
    #     return descriptions
    
    def interpret_single_image_for_all(self, encoded_image, image_name):
   
        result = self.interpret_single_image(encoded_image)
        descriptions = {
            "image_name": image_name,
             "description": result
            }
        return descriptions

    def interpret_combined_images(self, encoded_images):
        messages_content = [
            {
                "role": "user",
                "content": "RolePlay as a musical and artistic bot. Generate a text translating the emotion that all the images evokes together, considering characteristics of all of them. Consider that the given images are from space."
            },
            {
                "role": "user",
                "content": "The text must be a poem that describes the images using the emotion that all of them combined evoke on the viewer. Focus on the colors"
            },
            {
                    "role": "user",
                    "content": "Example: If there are different celestial bodies on the images, it is posstible to explicit: 'The presence of celestial bodies in the space reminds that, despite empty, the universe has diversity.'"
            },
            {
                "role": "user",
                "content": "The poem must be short, maximum of eight lines."
            },
        ]

        for encoded_image in encoded_images:
            messages_content.append({
                "role": "user",
                "content": f"data:image/jpeg;base64,{encoded_image}"
            })

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

        try:
            response = requests.post("https://api.openai.com/v1/chat/completions", headers=self.headers, json=payload)
            return response.json()
        except requests.RequestException as e:
            return f"Error: API request failed with message: {str(e)}"

