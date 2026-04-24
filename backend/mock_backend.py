import http.server
import json
import random
import os

# Configuration
PORT = 8000
METADATA_PATH = os.path.join(os.path.dirname(__file__), '../data/music_metadata.json')

class MockHandler(http.server.BaseHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.end_headers()

    def do_POST(self):
        if self.path == '/analyze':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            request_data = json.loads(post_data.decode('utf-8'))
            
            input_type = request_data.get('type', 'text')
            input_data = request_data.get('data', '')

            # Mock emotion detection
            # For demo: if text contains "sad", return SAD, etc.
            detected_emotion = 'CALM'
            if input_type == 'text':
                text = input_data.lower()
                if 'happy' in text or 'good' in text or 'great' in text:
                    detected_emotion = 'HAPPY'
                elif 'sad' in text or 'bad' in text or 'cry' in text:
                    detected_emotion = 'SAD'
                elif 'angry' in text or 'mad' in text or 'hate' in text:
                    detected_emotion = 'ANGRY'
            else:
                # Random for image upload
                detected_emotion = random.choice(['HAPPY', 'SAD', 'ANGRY', 'CALM'])

            # Load metadata
            try:
                with open(METADATA_PATH, 'r') as f:
                    all_songs = json.load(f)
                
                # Filter songs by emotion
                songs = [s for s in all_songs if s['emotion'] == detected_emotion]
                
                # Assign streamUrl to downloadUrl (since S3 won't work locally without credentials)
                for s in songs:
                    s['streamUrl'] = s['downloadUrl']
                
                # Limit to 5 songs
                recommended_songs = random.sample(songs, min(len(songs), 5))
                
                response = {
                    'emotion': detected_emotion,
                    'songs': recommended_songs
                }

                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps(response).encode('utf-8'))
                
            except Exception as e:
                self.send_response(500)
                self.end_headers()
                self.wfile.write(json.dumps({'error': str(e)}).encode('utf-8'))
        else:
            self.send_response(404)
            self.end_headers()

if __name__ == '__main__':
    print(f"Starting mock backend on port {PORT}...")
    print(f"Metadata path: {METADATA_PATH}")
    server = http.server.HTTPServer(('0.0.0.0', PORT), MockHandler)
    server.serve_forever()
