# StarMonics: Sound of Silence

![StarMonics Logo](Logo.png)

## Introduction

The "Starmonics: Sound of Silence" project is part of the NASA SpaceApps2024 initiative, focusing on the challenge titled "Symphony of the Stars: Harmonizing the James Webb Space Telescope in Music and Images." This project aims to harmonize the visual beauty captured by the James Webb Space Telescope (JWST) with the art of music. By leveraging advanced image processing and language generation techniques, we provide users with an interactive platform to explore celestial imagery and experience the emotional resonance of the cosmos through poetry and music.

The JWST, with its unprecedented capabilities, explores profound topics in astronomy—from the birth of stars and galaxies to the search for signs of life beyond our solar system. Its findings inspire curiosity and wonder, prompting us to capture the essence of this remarkable mission through our project. We create a collage that merges stunning astronomic visuals with a compelling musical backdrop, encapsulating the sense of discovery and cosmic awe that the telescope inspires in a way that appeals to people of all ages.

## Objectives

1. **User Interaction**: Allow users to upload astronomical images.
2. **Emotion Translation**: Utilize a language model API to generate poetic texts that reflect the emotions conveyed by the selected images.
3. **Musical Composition**: Generate music based on the poetic text, creating a unique auditory experience that complements the visual and textual elements.
4. **Integrated Experience**: Display the selected image, the generated poem, and the composed music within a cohesive user interface, providing an immersive experience.

## Methodology

This project utilizes image processing and music generation techniques to create a musical composition based on the visual features of an input image. Thereby, the methodology is structured into several components:

1. **Color Mapping**: A dictionary maps musical notes to specific RGB color values, allowing for the association of colors extracted from the image with corresponding musical notes.

2. **Image Processing**:
   - **Brightness Calculation**: The average brightness of the image is calculated by converting it to grayscale, with the resulting value mapped to musical pitch.
   - **Image Resizing**: To optimize performance, the image is resized to a specified maximum dimension.
   - **Saturation Calculation**: The average saturation of the image is determined in HSV color space, influencing the tempo of the generated music.
   - **Color Analysis**: The code identifies the frequency of musical note colors present in the image and determines the most prominent notes through pixel analysis.

3. **Musical Feature Assignment**: Extracted features—brightness, color frequencies, and saturation—are combined to derive key musical attributes: pitch, tone sequence, and tempo.

4. **Music Generation**: The `SongMaker` class interacts with the OpenAI API to generate music in ABC notation based on the derived musical attributes.

5. **MIDI and Audio Processing**:
   - **MIDI Creation**: ABC notation is converted to a MIDI file using the `music21` library.
   - **MIDI to WAV Conversion**: The MIDI file is transformed into a WAV format using FluidSynth, with the help of a specified soundfont.
   - **Audio Effects Application**: Reverb is applied to the WAV file using SoX, followed by normalization of audio levels using the `pydub` library.

6. **Execution Flow**: The script processes the input image, extracts musical features, generates music, and produces the final audio output in a structured manner.

This methodology effectively bridges the gap between visual stimuli and auditory expression, creating a unique and immersive musical experience inspired by the characteristics of the input image.

By integrating the findings of the JWST with our artistic approach, we aim to inspire curiosity and wonder in all who experience our work, celebrating the sense of discovery that the cosmos offers.
