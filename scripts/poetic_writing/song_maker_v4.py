import requests
import json
import os

api_key = 'sk-FDti6mHcD9tIT6bNgmrHvPd9bUcUqCJRfJLhynB9OkT3BlbkFJSvdRzIA5BrDL_GKIhBkFTKl-fZKmmSYoUMizf8ZEMA'
input_text = 'In the cosmic expanse, a nebula blooms, Swirls of gas and dust like a dream in hues. Golden cliffs rise, sculpted by stellar winds, Reaching into the void where eternity begins.'

class SongMaker:
    def __init__(self, api_key, input_text):
        self.api_key = api_key
        self.input_text = input_text
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }


    def make_song(self):
        """Makes an ABC format song based on a input text."""
        payload = {
            "model": "gpt-4o-mini",
            "messages": [
                {
                    "role": "user",
                    "content": "RolePlay as a musical bot. Generate a a music in ABC format based on the input text."
                },
                {
                    "role": "user",
                    "content": f"Style: Symphonic, in the style of John Williams. Tone Sequence: A - B - C# - G#. Tempo: 91 BPM. Pitch: Low-pitch, inspirational and exploratory. {self.input_text}"
                },
                {
                    "role": "user",
                    "content": "Output the correspondent instruments."
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


generate_song = SongMaker(api_key, input_text)

# Make a song
song = generate_song.make_song()
print(song)