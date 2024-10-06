from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from django.core.exceptions import ValidationError

from .tools.extract_features import process_image
from .tools.poetic_description import ImageInterpreter
from .tools.song_maker import SongMaker

from django.conf import settings
import os 
import openai


def home(request):
    mensagem = ''
    caminho_imagem = ''
    descricao_poetica = ''
    caminho_musica = ''
    
    if request.method == 'POST':
        if 'imagem' in request.FILES:
            imagem = request.FILES['imagem']
            # Validação do tipo de arquivo
            if not imagem.content_type.startswith('image/'):
                mensagem = 'Please, send a valid image file.'
            else:

                caminho_imagem, descricao_poetica, caminho_musica = generateMusic(imagem)

                    
    return render(request, 'starsite/index.html', {
        'mensagem': mensagem,
        'caminho_imagem': caminho_imagem,
        'descricao_poetica': descricao_poetica,
        'caminho_musica': caminho_musica
    })
    
    
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

        song_maker = SongMaker(API_KEY, description, tone_sequence, tempo)
        
        song_response = song_maker.make_song()
        
        if 'choices' in song_response and song_response['choices']:
            song_abc_content = song_response['choices'][0]['message']['content']
            
            # Salvar o conteúdo ABC em um arquivo
            abc_file_name = 'song.abc'
            abc_file_path = os.path.join(settings.MEDIA_ROOT, abc_file_name)
            with open(abc_file_path, 'w') as abc_file:
                abc_file.write(song_abc_content)
            
            # Converter o ABC para MIDI e depois para MP3
            midi_file_name = 'song.mid'
            midi_file_path = os.path.join(settings.MEDIA_ROOT, midi_file_name)
            # mp3_file_name = 'song.mp3'
            # mp3_file_path = os.path.join(settings.MEDIA_ROOT, mp3_file_name)
            
            # Converter ABC para MIDI
            song_maker.abc_to_midi(abc_file_path, midi_file_path)
            
            # Converter MIDI para MP3
            # song_maker.midi_to_mp3(midi_file_path, mp3_file_path)
            
            # Obter o caminho do MP3 para passar ao template
            caminho_musica = fs.url(midi_file_name)
            
            return caminho_imagem, description, caminho_musica
        else:
            mensagem = 'Não foi possível gerar a música.'
        
        
        
