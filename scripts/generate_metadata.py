import json
import os

emotions = {
    "HAPPY": ["Pop", "Upbeat", "Synthwave", "Disco", "Funk", "Dance", "Reggae", "Electropop", "Jazzy", "Soul"],
    "SAD": ["Piano", "Classical", "Ambient", "Blues", "Melancholy", "Acoustic", "Lofi", "Minimal", "Cinematic", "Downtempo"],
    "ANGRY": ["Rock", "Metal", "Industrial", "Punk", "Nu Metal", "Hardcore", "Grunge", "Alternative", "Thrash", "Heavy Metal"],
    "CALM": ["Ambient", "Nature", "Zen", "Chillout", "Meditation", "Space", "Ethereal", "Soft", "Dreamy", "Lounge"]
}

song_names = {
    "HAPPY": ["Sunshine", "Rainbow", "Glow", "Spark", "Joy", "Pulse", "Bliss", "Vibe", "Energy", "Radiance"],
    "SAD": ["Rain", "Tears", "Shadow", "Echo", "Mist", "Hollow", "Faded", "Solace", "Grief", "Drift"],
    "ANGRY": ["Thunder", "Fire", "Storm", "Rage", "Clash", "Strike", "Fury", "Blaze", "Voltage", "Chaos"],
    "CALM": ["Ocean", "Mountain", "Forest", "Breeze", "Silent", "Peace", "Eon", "Still", "Quiet", "Zenith"]
}

metadata = []

for i in range(1, 11):
    # Happy (1, 5, 9, ...)
    idx_h = (i-1) * 4 + 1
    metadata.append({
        "emotion": "HAPPY",
        "songName": f"Happy {song_names['HAPPY'][i-1]}",
        "genre": emotions["HAPPY"][i-1],
        "filename": f"happy_{i}.mp3",
        "s3Url": f"s3://emotion-music-storage/happy/happy_{i}.mp3",
        "downloadUrl": f"https://www.soundhelix.com/examples/mp3/SoundHelix-Song-{idx_h}.mp3"
    })
    
    # Sad (2, 6, 10, ...)
    idx_s = (i-1) * 4 + 2
    metadata.append({
        "emotion": "SAD",
        "songName": f"Sad {song_names['SAD'][i-1]}",
        "genre": emotions["SAD"][i-1],
        "filename": f"sad_{i}.mp3",
        "s3Url": f"s3://emotion-music-storage/sad/sad_{i}.mp3",
        "downloadUrl": f"https://www.soundhelix.com/examples/mp3/SoundHelix-Song-{idx_s}.mp3"
    })
    
    # Angry (3, 7, 11, ...)
    idx_a = (i-1) * 4 + 3
    metadata.append({
        "emotion": "ANGRY",
        "songName": f"Angry {song_names['ANGRY'][i-1]}",
        "genre": emotions["ANGRY"][i-1],
        "filename": f"angry_{i}.mp3",
        "s3Url": f"s3://emotion-music-storage/angry/angry_{i}.mp3",
        "downloadUrl": f"https://www.soundhelix.com/examples/mp3/SoundHelix-Song-{idx_a}.mp3"
    })
    
    # Calm (4, 8, 12, ...)
    idx_c = (i-1) * 4 + 4
    metadata.append({
        "emotion": "CALM",
        "songName": f"Calm {song_names['CALM'][i-1]}",
        "genre": emotions["CALM"][i-1],
        "filename": f"calm_{i}.mp3",
        "s3Url": f"s3://emotion-music-storage/calm/calm_{i}.mp3",
        "downloadUrl": f"https://www.soundhelix.com/examples/mp3/SoundHelix-Song-{idx_c}.mp3"
    })

# Write to file
with open('data/music_metadata.json', 'w') as f:
    json.dump(metadata, f, indent=2)

print(f"Generated metadata for {len(metadata)} songs.")
