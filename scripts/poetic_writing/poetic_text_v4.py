import base64
import requests
import json
import os

class ImageInterpreter:
    def __init__(self, api_key, image_dir):
        self.api_key = api_key
        self.image_dir = image_dir
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }

    def encode_images(self):
        encoded_images = []
        image_names = []
        for image_name in os.listdir(self.image_dir):
            image_path = os.path.join(self.image_dir, image_name)
            if os.path.isfile(image_path):
                with open(image_path, "rb") as image_file:
                    encoded_image = base64.b64encode(image_file.read()).decode('utf-8')
                    encoded_images.append(encoded_image)
                    image_names.append(image_name)
        return encoded_images, image_names

    def interpret_single_image(self, encoded_image):
        payload = {
            "model": "gpt-4o",
            "messages": [
                {
                    "role": "user",
                    "content": "RolePlay as a musical and artistic bot. Generate a text translating the emotion that the image evokes considering its characteristics."
                },
                {
                    "role": "user",
                    "content": "The text must be short, maximum of eight lines."
                },
                {
                    "role": "user",
                    "content": f"data:image/jpeg;base64,{encoded_image}"
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

    def interpret_single_image_for_all(self, encoded_images, image_names):
        descriptions = []
        for encoded_image, image_name in zip(encoded_images, image_names):
            result = self.interpret_single_image(encoded_image)
            descriptions.append({
                "image_name": image_name,
                "description": result
            })
        return descriptions

    def interpret_combined_images(self, encoded_images):
        messages_content = [
            {
                "role": "user",
                "content": "RolePlay as a musical and artistic bot. Generate a text translating the emotion that all the images evokes together, considering characteristics of all of them."
            },
            {
                    "role": "user",
                    "content": "The text must be short, maximum of eight lines."
            },
        ]

        for encoded_image in encoded_images:
            messages_content.append({
                "role": "user",
                "content": f"data:image/jpeg;base64,{encoded_image}"
            })

        payload = {
            "model": "gpt-4o",
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

# Main execution logic
if __name__ == "__main__":
    API_KEY = 'API_KEY'
    IMAGE_DIR = '/home/gbeneti/Documentos/JupyterLab/github_repos/StarMonics/test_images'

    if not API_KEY:
        print("Error: API key is missing.")
    elif not os.path.isdir(IMAGE_DIR):
        print("Error: Image directory is invalid or does not exist.")
    else:
        interpreter = ImageInterpreter(API_KEY, IMAGE_DIR)

        encoded_images, image_names = interpreter.encode_images()

        if not encoded_images:
            print("No images found in the directory.")
        else:
            print("Individual Image Interpretations:")
            individual_descriptions = interpreter.interpret_single_image_for_all(encoded_images, image_names)
            for description in individual_descriptions:
                print(f"Image: {description['image_name']}")
                print(f"Description: {description['description']}\n")

            print("Combined Image Interpretation:")
            combined_result = interpreter.interpret_combined_images(encoded_images)
            print(json.dumps(combined_result, indent=4))