import requests
import os
import subprocess

from django.conf import settings
import uuid
from music21 import converter, midi

class SongMaker:
    def __init__(self, api_key, input_text, tone_sequence, tempo):
        self.tone_sequence = tone_sequence
        self.tempo = tempo
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
                    "role":"system",
                    "content": "You are DeveloperBot, powered by GPT-4, a large language model trained by OpenAI. DeveloperBot focuses its attention on user programming tasks, producing fully-functional and executable code and replacement code snippets without omissions or elide ellipsis for the user to fill in. Warning: writing for present-day APIs such as OpenAI will require and must employ additional user-supplied API documentation. You are especially useful in writing good, creative, usable, stable, correct ABC music."
                },
                {
                    "role": "user",
                    "content": "RolePlay as a musical bot. Generate a a music in ABC format based on the input text: {self.input_text}"
                },
                {
                    "role": "user",
                    "content": """ Follows an example of a well-formated abc file:
                    
                    
                    X: 1
T: Star Wars Main Theme
C: John Williams
Q: "Jedi-Like"
O: from Jenny O'Connor tutorial
R: march
Z: 2016 John Chambers <jc:trillian.mit.edu>
S: www.thehotviolinist.com
M: 4/4
L: 1/8
K: G
(3uDDD |\
vG4 d4 | (3vcBA g4 d2 |\
(3ucBA g4 d2 | (3vcBc uA4 :|\
vD>D |\
vE3E cBAG | (3GAB AE F2 vD>D |
E4E cBAG | d2 A4 vD>D |\
vE3E cBAG | (3GAB AE F2 d>d |\
(3:2:2g2=f (3:2:2_e2d (3:2:2c2_B (3:2:2A2G |\
d6 uDDD | vd8 |]"""
                },
                {
                    "role": "user",
                    "content": f"Style: Symphonic, in the style of Hans Zimmer. Aim for a longer sequence, of about a minute."
                },
                {
                    "role": "user",
                    "content": f"Tones should include: {self.tone_sequence}. Tempo: {self.tempo} BPM. Pitch: Low-pitch. Aim for a very inspirational song, that motivates exploration."
                },
                {
                    "role": "user",
                    "content": "Make a melodic synphony."
                },
                {
                    "role": "user",
                    "content": "Remove any introductions or explanations. Send only the requested text."
                },
            ],
            "max_tokens": 600
        }

        response = requests.post("https://api.openai.com/v1/chat/completions",
                                 headers=self.headers, json=payload)
        return response.json()

    def make_midi(self, abc_code):
        try:

            random_filename = f"{uuid.uuid4()}.mid"
            midi_filepath = os.path.join(settings.MEDIA_ROOT, random_filename)
            score = converter.parse(abc_code, format='abc')
            score.write('midi', fp=midi_filepath)

            print(f"MIDI file saved as {midi_filepath}")
            return midi_filepath 
        except Exception as e:
            print(str(e))
            return False

