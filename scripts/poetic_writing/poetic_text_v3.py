import base64
import requests
import json
import os

class ImageInterpreter:
    def __init__(self, api_key, image_dir):
        self.api_key = api_key
        self.image_dir = image_dir  # Directory containing images
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }

    def encode_images(self):
        """Converts all image files in a directory to a list of base64 strings."""
        encoded_images = []
        image_names = []
        for image_name in os.listdir(self.image_dir):
            image_path = os.path.join(self.image_dir, image_name)
            if os.path.isfile(image_path):  # Check if it's a file
                with open(image_path, "rb") as image_file:
                    encoded_image = base64.b64encode(image_file.read()).decode('utf-8')
                    encoded_images.append(encoded_image)
                    image_names.append(image_name)  # Keep track of image names for clarity
        return encoded_images, image_names

    def interpret_single_image(self, encoded_image):
        """Sends a single image (already encoded) to the OpenAI API for interpretation."""
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

        response = requests.post("https://api.openai.com/v1/chat/completions",
                                 headers=self.headers, json=payload)
        return response.json()

    def interpret_single_image_for_all(self, encoded_images, image_names):
        """Interprets each image individually and returns a list of descriptions."""
        descriptions = []
        for encoded_image, image_name in zip(encoded_images, image_names):
            result = self.interpret_single_image(encoded_image)
            descriptions.append({
                "image_name": image_name,
                "description": result['choices'][0]['message']['content']  # Assuming successful completion
            })
        return descriptions

    def interpret_combined_images(self, encoded_images):
        """Sends multiple images (already encoded) to the OpenAI API and generates a combined response."""
        messages_content = [
            {
                "role": "user",
                "content": "RolePlay as a musical and artistic bot. Generate a text translating the emotion that all the images evokes together, considering characteristics of all of them."
            }
        ]

        # Add each encoded image to the payload
        for encoded_image in encoded_images:
            messages_content.append({
                "role": "user",
                "content": f"data:image/jpeg;base64,{encoded_image}"
            })

        # Build the payload for multiple images
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

        response = requests.post("https://api.openai.com/v1/chat/completions",
                                 headers=self.headers, json=payload)
        return response.json()

# Main execution logic
if __name__ == "__main__":
    # Constants
    API_KEY = 'API_KEY'
    IMAGE_DIR = '/home/gbeneti/Documentos/JupyterLab/github_repos/StarMonics/test_images'

    # Check if API key and image directory are set
    if not API_KEY:
        print("Error: API key is missing.")
    elif not os.path.isdir(IMAGE_DIR):
        print("Error: Image directory is invalid or does not exist.")
    else:
        interpreter = ImageInterpreter(API_KEY, IMAGE_DIR)

        # Encode all images in the directory
        encoded_images, image_names = interpreter.encode_images()

        if not encoded_images:
            print("No images found in the directory.")
        else:
            # First, interpret each image individually
            print("Individual Image Interpretations:")
            individual_descriptions = interpreter.interpret_single_image_for_all(encoded_images, image_names)
            for description in individual_descriptions:
                print(f"Image: {description['image_name']}")
                print(f"Description: {description['description']}\n")

            # Now, generate a combined interpretation
            print("Combined Image Interpretation:")
            combined_result = interpreter.interpret_combined_images(encoded_images)
            print(json.dumps(combined_result, indent=4))
