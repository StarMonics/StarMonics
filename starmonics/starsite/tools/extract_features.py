from PIL import Image
import numpy as np
from collections import Counter
import colorsys


COLOR_TO_NOTE = {
    'C': (255, 0, 0),          # Red
    'C#': (255, 102, 102),     # Light Red
    'D': (255, 165, 0),        # Orange
    'D#': (255, 140, 0),       # Dark Orange
    'E': (255, 255, 0),        # Yellow
    'F': (0, 255, 0),          # Green
    'F#': (102, 255, 102),     # Light Green
    'G': (0, 0, 255),          # Blue
    'G#': (102, 178, 255),     # Light Blue
    'A': (75, 0, 130),         # Indigo
    'A#': (238, 130, 238),     # Violet
    'B': (186, 85, 211)        # Light Purple
}

def calculate_average_brightness(image):
    """
    Calculate the average brightness of an image.
    Converts the image to grayscale and computes the mean pixel value.
    """
    grayscale_image = image.convert('L') 
    pixels = np.array(grayscale_image)
    average_brightness = np.mean(pixels)
    return average_brightness


def resize_image(image, max_size=500):
    """Reduz o tamanho da imagem para melhorar a performance."""
    image.thumbnail((max_size, max_size), Image.BILINEAR)
    return image


def calculate_saturation(image):
    """
    Calculate the average saturation of an image.
    Converts the image to RGB, then to HSV to extract saturation values.
    """
    rgb_image = image.convert('RGB') 
    pixels = np.array(rgb_image)
    # Reshape to a list of pixels
    reshaped_pixels = pixels.reshape(-1, 3)
    # Convert RGB to HSV and extract saturation
    hsv_pixels = [colorsys.rgb_to_hsv(r/255.0, g/255.0, b/255.0) for r, g, b in reshaped_pixels]
    saturations = [s for h, s, v in hsv_pixels]
    average_saturation = np.mean(saturations)
    return average_saturation

def find_nearest_note_color(pixel, color_map):
    """
    Find the nearest note color for a given pixel based on Euclidean distance.
    """
    min_distance = float('inf')
    nearest_note = None
    for note, color in color_map.items():
        distance = np.linalg.norm(np.array(pixel) - np.array(color))  
        if distance < min_distance:
            min_distance = distance
            nearest_note = note
    return nearest_note

def find_rainbow_colors(image, color_map):
    """
    Find and count the frequency of each rainbow color (including semitones) in the image.
    """
    rgb_image = image.convert('RGB') 
    pixels = np.array(rgb_image)

    reshaped_pixels = pixels.reshape(-1, 3)
    pixel_counter = Counter(map(tuple, reshaped_pixels))


    color_frequency = {note: 0 for note in color_map.keys()}

    for pixel, count in pixel_counter.items():
        note = find_nearest_note_color(pixel, color_map)
        if note:
            color_frequency[note] += count


    ordered_colors = sorted(color_frequency.items(), key=lambda x: x[1], reverse=True)
    return ordered_colors

def assign_music_features(brightness, ordered_colors, saturation):
    """
    Assign pitch, tone sequence, and tempo based on image features.
    """

    base_pitch = 440 
    pitch = int(base_pitch * (brightness / 255)) 


    tone_sequence = [note for note, freq in ordered_colors if freq > 0]

    base_tempo = 240  
    tempo = int(base_tempo * saturation) 

    return pitch, tone_sequence, tempo

def process_image(image_path, resize = True):
    """
    Process the image to extract features and assign musical attributes.
    """
    try:
        image = Image.open(image_path)
    except IOError:
        print(f"Error: Unable to open image at path '{image_path}'. Please check the file path.")
        return
    
    if resize == True:
        image = resize_image(image)

    brightness = calculate_average_brightness(image)
    saturation = calculate_saturation(image)
    ordered_colors = find_rainbow_colors(image, COLOR_TO_NOTE)

    pitch, tone_sequence, tempo = assign_music_features(brightness, ordered_colors, saturation)

    print(f"Average Brightness: {brightness:.2f}")
    print("Color Frequencies (Ordered):")
    for color, freq in ordered_colors:
        print(f"  {color}: {freq}")
    print(f"Average Saturation: {saturation:.2f}")
    print(f"Assigned Pitch (Hz): {pitch}")
    print(f"Tone Sequence: {' - '.join(tone_sequence)}")
    print(f"Assigned Tempo (BPM): {tempo}")

    return {
        "brightness": brightness,
        "ordered_colors": ordered_colors,
        "saturation": saturation,
        "pitch": pitch,
        "tone_sequence": tone_sequence,
        "tempo": tempo
    }

