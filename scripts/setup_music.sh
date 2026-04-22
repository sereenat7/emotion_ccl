#!/bin/bash

# Create folders if they don't exist
mkdir -p music/happy music/sad music/angry music/calm

echo "Preparing to download large music library (40 tracks total)..."

# Use python to extract URLs and filenames and download them
python3 -c "
import json, os, subprocess

with open('data/music_metadata.json', 'r') as f:
    data = json.load(f)

for item in data:
    folder = item['emotion'].lower()
    filename = item['filename']
    url = item['downloadUrl']
    target = f'music/{folder}/{filename}'
    
    if not os.path.exists(target):
        print(f'Downloading {target}...')
        subprocess.run(['curl', '-L', '-o', target, url])
    else:
        print(f'✓ {target} already exists.')
"

echo "Done! 40 music files are organized in the music/ directory."
