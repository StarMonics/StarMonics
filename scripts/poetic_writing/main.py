from poetic_text import ImageInterpreter

API_KEY = 'sk-2y_THd9qBE0arfbCMmDRJQonjqbQr2vLEUxtKrgxVeT3BlbkFJbqxa5J7JYlPgfLIncFCmCt7eX5EmV7R4Qlg6YmpxkA'
IMAGE_PATH = '/home/gbeneti/Documentos/JupyterLab/github_repos/StarMonics/test_images'

interpreter = ImageInterpreter(API_KEY, IMAGE_PATH)


encoded_images = interpreter.encode_images()

# Interpretar uma única imagem
single_image_phylosophic_text = interpreter.interpret_single_image(encoded_images[0])
print(single_image_phylosophic_text)

# Interpretar múltiplas imagens
multiple_images_philosophic_text = interpreter.interpret_multiple_images(encoded_images)
print(multiple_images_philosophic_text)
