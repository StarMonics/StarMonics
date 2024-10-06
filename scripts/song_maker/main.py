from song_maker_v4 import SongMaker

API_KEY = 'API_KEY'
INPUT_TEXT = 'In the cosmic expanse, a nebula blooms, Swirls of gas and dust like a dream in hues. Golden cliffs rise, sculpted by stellar winds, Reaching into the void where eternity begins.'

generate_song = SongMaker(API_KEY, INPUT_TEXT)

# Make a song
song = generate_song.make_song()
print(song)