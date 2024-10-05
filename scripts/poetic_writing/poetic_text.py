import base64
import requests
import json

class ImageInterpreter:
    def __init__(self, api_key, image_path):
        self.api_key = api_key
        self.image_path = image_path
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }

    def encode_image(self):
        """Converts an image file to a base64 string."""
        with open(self.api_keyimage_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')

    def interpret_single_image(self):
        """Sends a single image to the OpenAI API for interpretation."""
        base64_image = self.encode_image(self.image_path)
        payload = {
            "model": "gpt-4o-mini",
            "messages": [
                {
                    "role": "user",
                    "content": "text", "text": "RolePlay as a bot phylosopher. Generate a phylosophical text about the given image and reflect about the feelings that it evoke on the viewer."

                },
                {
                    "role": "user",
                    "content":
                        
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}"
                            }
                        }
                },
                {
                    "role": "user",
                    "content": "verify if the produced text makes sense gramatically. If not, correct it."
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
        #return response.json()

        return response['choices'][0]['message']['content']

    def interpret_multiple_images(self, image_path):
        """Sends multiple images to the OpenAI API and generates a combined response."""

        # Add each image in base64 to the payload
        for image in self.image_path:
            base64_image = self.encode_image(image)
            messages_content.append({
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/jpeg;base64,{base64_image}"
                }
            })

        payload = {
            "model": "gpt-4o-mini",
            "messages": [
                {
                    "role": "user",
                    "content": "text", "text": "RolePlay as a bot phylosopher. Generate a phylosophical text about the given image and reflect about the feelings that it evoke on the viewer."
                },
                {
                    "role": "user",
                    "content":
                        
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}"
                            }
                        }
                },
                {
                    "role": "user",
                    "content": "Verify if the produced text makes sense gramatically. If not, correct it."
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
        #return response.json()

        return response['choices'][0]['message']['content']
