from poetic_text import ImageInterpreter

API_KEY = 'API_KEY'
IMAGE_PATH = 'IMAGE_PATH'

interpreter = ImageInterpreter(API_KEY, IMAGE_PATH)

# Interpretar uma única imagem
single_image_phylosophic_text = interpreter.interpret_single_image("path_to_your_image.jpg")
print(single_image_phylosophic_text)

# Interpretar múltiplas imagens
multiple_images_philosophic_text = interpreter.interpret_multiple_images("path_to_images")
print(multiple_images_philosophic_text)

