import requests
import os
import subprocess
from midi2audio import FluidSynth
from django.conf import settings

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
        """Gera uma música em formato ABC com base no texto de entrada."""
        payload = {
            "model": "gpt-4o-mini",  # Certifique-se de usar um modelo válido
            "messages": [
                {
                    "role": "system",
                    "content": "RolePlay as a musical bot. Generate a music in ABC format based on the input text."
                },
                {
                    "role": "system",
                    "content": f"Style: Symphonic, in the style of Hans Zimmer. Aim for a longer sequence, of about a minute. Tones should include: {self.tone_sequence}. Tempo: {self.tempo} BPM. Pitch: Low-pitch. Aim for a very inspirational song, that motivates exploration. Base the music on user input."
                },
                {
                    "role": "user",
                    "content": f"Using the following poem, make a melodic symphony using the piano. It should be a calm song.\n{self.input_text}"
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

    def abc_to_midi(self, abc_file, midi_file):
        """Converte um arquivo .abc para .midi usando abc2midi."""
        abc2midi_path = settings.ABC2MIDI_PATH
        
        try:
            subprocess.run([abc2midi_path, abc_file, '-o', midi_file], check=True)
            print(f'Sucesso: {abc_file} convertido para {midi_file}')
        except subprocess.CalledProcessError as e:
            print(f'Erro durante a conversão de {abc_file} para .midi: {e}')
            raise e

    def midi_to_mp3(self, midi_file, mp3_file):
        """Converte um arquivo .midi para .mp3 usando FluidSynth."""
        try:
            fs = FluidSynth(sound_font=settings.SOUNDFONT_PATH)
            fs.midi_to_audio(midi_file, mp3_file)
            print(f'Sucesso: {midi_file} convertido para {mp3_file}')
        except Exception as e:
            print(f'Erro durante a conversão de {midi_file} para .mp3: {e}')
            raise e
