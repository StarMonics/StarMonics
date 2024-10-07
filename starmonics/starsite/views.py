from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from django.core.exceptions import ValidationError
from django.utils.safestring import mark_safe
from .tools.extract_features import process_image
from .tools.poetic_description import ImageInterpreter
from .tools.song_maker import SongMaker
import uuid
from django.conf import settings
import os 
# import openai


import subprocess
from pydub import AudioSegment
from pydub.effects import normalize


def home(request):
    mensagem = ''
    caminho_imagem = ''
    descricao_poetica = ''
    caminho_musica = ''
    
    if request.method == 'POST':
        if 'imagem' in request.FILES:
            imagem = request.FILES['imagem']

            if not imagem.content_type.startswith('image/'):
                mensagem = 'Please, send a valid image file.'
            else:

                caminho_imagem, descricao_poetica, caminho_musica = generateMusic(imagem)
                

                    
    return render(request, 'starsite/index.html', {
        'mensagem': mensagem,
        'caminho_imagem': caminho_imagem,
        'descricao_poetica': mark_safe(descricao_poetica.replace("\n", "<br>")),
        'caminho_musica': caminho_musica
    })
    
    
def make_midi_image(api_key, input_text, tone_sequence, tempo):
    finished = False


    while finished == False:
        song_maker = SongMaker(api_key, input_text, tone_sequence, tempo)
        song = song_maker.make_song()
        song_abc = song['choices'][0]['message']['content'][3:][:-4].replace('\n', '''
                                                                             ''')
        finished = song_maker.make_midi(song_abc)
    
    return finished
        
def generateMusic(imagem):
    
    fs = FileSystemStorage()
    nome_arquivo = fs.save(imagem.name, imagem)
    caminho_imagem = fs.url(nome_arquivo)
    mensagem = 'Image sent with success!'
    
    caminho_arquivo = fs.path(nome_arquivo)
    
    features = process_image(caminho_arquivo)
    tone_sequence = features["tone_sequence"]
    tempo = features["tempo"]

    
    API_KEY = os.getenv('OPENAI_API_KEY')
    IMAGE_DIR = caminho_arquivo

    if not API_KEY:
        print("Error: API key is missing.")
    else:
        interpreter = ImageInterpreter(API_KEY, IMAGE_DIR)

        encoded_image, image_name = interpreter.encode_image()

        if not encoded_image:
            print("No images found in the directory.")
        else:
            print("Individual Image Interpretations:")
            description = interpreter.interpret_single_image_for_all(encoded_image, image_name)

            print(f"Image: {description['image_name']}")
            print(f"Description: {description['description']}\n")


        midi_filepath = make_midi_image(API_KEY, description, tone_sequence, tempo)
        
        temp_name = str(uuid.uuid4())
        output_wav_file = os.path.join(settings.MEDIA_ROOT, temp_name+"output_song_with_effects.wav")
        path_relative = temp_name+"output_song_with_effects.wav"
        soundfont = settings.SOUNDFONT_PATH
        
        process_midi(midi_filepath, soundfont, output_wav_file, temp_name)
        
        if not os.path.exists(output_wav_file):
            print(f"Erro: Arquivo WAV {output_wav_file} não foi criado.")
            return caminho_imagem, description, ''


        caminho_musica = fs.url(path_relative)
        
        return caminho_imagem, description["description"], caminho_musica
        
        
        

def midi_to_wav(midi_file, soundfont, output_file):
    """
    Converts a MIDI file to WAV using FluidSynth.
    """

    command = [
        "fluidsynth",
        "-ni", soundfont, 
        midi_file,
        "-F", output_file, 
        "-r", "44100"  
    ]

    subprocess.run(command, check=True)


def apply_reverb(wav_file, output_file):
    """
    Applies reverb to a WAV file using the sox tool.
    """

    command = [
        "sox", wav_file, output_file, "reverb"
    ]

    subprocess.run(command, check=True)


def apply_effects(wav_file, output_file):
    """
    Normalizes the audio file after reverb.
    """

    audio = AudioSegment.from_wav(wav_file)
    normalized_audio = normalize(audio)
    normalized_audio.export(output_file, format="wav")


def process_midi(midi_input, soundfont, output_wav, temp_name):
    
    temp_wav = os.path.join(settings.MEDIA_ROOT, temp_name+"_temp_output.wav")

    temp_with_reverb =  os.path.join(settings.MEDIA_ROOT, temp_name+"_temp_with_reverb.wav") # Temporary file for reverb

    midi_to_wav(midi_input, soundfont, temp_wav)
    apply_reverb(temp_wav, temp_with_reverb)
    apply_effects(temp_with_reverb, output_wav)


    os.remove(temp_wav)
    os.remove(temp_with_reverb)


        