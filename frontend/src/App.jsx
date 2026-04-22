import React, { useState } from 'react';
// import './App.css';

const API_ENDPOINT = 'https://jj20t803kh.execute-api.ap-south-1.amazonaws.com/prod/analyze';

function App() {
  const [moodText, setMoodText] = useState('');
  const [image, setImage] = useState(null);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [currentSong, setCurrentSong] = useState(null);

  const handleUpload = (e) => {
    const file = e.target.files[0];
    if (file) {
      const reader = new FileReader();
      reader.onloadend = () => {
        setImage(reader.result.split(',')[1]); // Base64 portion
      };
      reader.readAsDataURL(file);
    }
  };

  const analyzeEmotion = async (type) => {
    setLoading(true);
    setResult(null);
    
    const payload = {
      type: type,
      data: type === 'text' ? moodText : image,
      userId: 'user123'
    };

    try {
      const response = await fetch(API_ENDPOINT, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });
      
      const data = await response.json();
      setResult(data);
    } catch (error) {
      console.error('Error:', error);
      alert('Failed to analyze emotion. Ensure API Gateway is set up.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app-container">
      <header>
        <h1>VibeCheck</h1>
        <p className="subtitle">Emotion-Based Music Recommendations</p>
      </header>

      <div className="main-grid">
        <div className="input-section">
          <div className="glass-card">
            <label>How are you feeling?</label>
            <textarea 
              rows="4" 
              placeholder="I've had a long day and just want to relax..."
              value={moodText}
              onChange={(e) => setMoodText(e.target.value)}
            />
            <button 
              className="btn" 
              disabled={loading || !moodText}
              onClick={() => analyzeEmotion('text')}
            >
              {loading ? 'Analyzing...' : 'Analyze Text Mood'}
            </button>
          </div>

          <div className="glass-card">
            <label>Or show your face</label>
            <div className="upload-box" onClick={() => document.getElementById('fileInput').click()}>
              {image ? 'Image Selected ✓' : 'Click to upload selfie'}
              <input 
                id="fileInput" 
                type="file" 
                hidden 
                accept="image/*" 
                onChange={handleUpload} 
              />
            </div>
            <button 
              className="btn" 
              disabled={loading || !image}
              onClick={() => analyzeEmotion('image')}
            >
              {loading ? 'Analyzing...' : 'Analyze Image Mood'}
            </button>
          </div>
        </div>

        <div className="results-section">
          <div className="glass-card" style={{minHeight: '400px'}}>
            <label>Recommendations</label>
            
            {result ? (
              <>
                <div style={{marginBottom: '1.5rem'}}>
                  <span className="emotion-badge">{result.emotion}</span>
                </div>
                <ul className="song-list">
                  {result.songs.map((song, index) => (
                    <li key={index} className="song-item">
                      <div className="song-info">
                        <h4>{song.songName}</h4>
                        <p>{song.genre}</p>
                      </div>
                      <button 
                        className="play-btn"
                        onClick={() => setCurrentSong(song)}
                      >
                        ▶
                      </button>
                    </li>
                  ))}
                </ul>
              </>
            ) : (
              <div style={{textAlign: 'center', color: 'var(--text-muted)', marginTop: '4rem'}}>
                Analysis results will appear here
              </div>
            )}
          </div>
        </div>
      </div>

      {currentSong && (
        <div className="player-footer">
          <div style={{display: 'flex', justifyContent: 'space-between', marginBottom: '0.5rem'}}>
            <span>Now Playing: <strong>{currentSong.songName}</strong></span>
            <span style={{color: 'var(--text-muted)'}}>{currentSong.genre}</span>
          </div>
          <audio controls autoPlay src={currentSong.streamUrl}>
            Your browser does not support the audio element.
          </audio>
        </div>
      )}
    </div>
  );
}

export default App;
