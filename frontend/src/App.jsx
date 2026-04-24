import React, { useState } from 'react';
// import './App.css';

const API_ENDPOINT = 'https://jj20t803kh.execute-api.ap-south-1.amazonaws.com/prod/analyze';

// Local mock data for development/demo (uses real playable MP3 URLs)
const MOCK_SONGS = {
  HAPPY: [
    { songName: 'Happy Sunshine', genre: 'Pop', streamUrl: 'https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3' },
    { songName: 'Happy Rainbow', genre: 'Upbeat', streamUrl: 'https://www.soundhelix.com/examples/mp3/SoundHelix-Song-5.mp3' },
    { songName: 'Happy Glow', genre: 'Synthwave', streamUrl: 'https://www.soundhelix.com/examples/mp3/SoundHelix-Song-9.mp3' },
    { songName: 'Happy Spark', genre: 'Disco', streamUrl: 'https://www.soundhelix.com/examples/mp3/SoundHelix-Song-13.mp3' },
    { songName: 'Happy Joy', genre: 'Funk', streamUrl: 'https://www.soundhelix.com/examples/mp3/SoundHelix-Song-17.mp3' },
  ],
  SAD: [
    { songName: 'Sad Rain', genre: 'Piano', streamUrl: 'https://www.soundhelix.com/examples/mp3/SoundHelix-Song-2.mp3' },
    { songName: 'Sad Tears', genre: 'Classical', streamUrl: 'https://www.soundhelix.com/examples/mp3/SoundHelix-Song-6.mp3' },
    { songName: 'Sad Shadow', genre: 'Ambient', streamUrl: 'https://www.soundhelix.com/examples/mp3/SoundHelix-Song-10.mp3' },
    { songName: 'Sad Echo', genre: 'Blues', streamUrl: 'https://www.soundhelix.com/examples/mp3/SoundHelix-Song-14.mp3' },
    { songName: 'Sad Mist', genre: 'Melancholy', streamUrl: 'https://www.soundhelix.com/examples/mp3/SoundHelix-Song-18.mp3' },
  ],
  ANGRY: [
    { songName: 'Angry Thunder', genre: 'Rock', streamUrl: 'https://www.soundhelix.com/examples/mp3/SoundHelix-Song-3.mp3' },
    { songName: 'Angry Fire', genre: 'Metal', streamUrl: 'https://www.soundhelix.com/examples/mp3/SoundHelix-Song-7.mp3' },
    { songName: 'Angry Storm', genre: 'Industrial', streamUrl: 'https://www.soundhelix.com/examples/mp3/SoundHelix-Song-11.mp3' },
    { songName: 'Angry Rage', genre: 'Punk', streamUrl: 'https://www.soundhelix.com/examples/mp3/SoundHelix-Song-15.mp3' },
    { songName: 'Angry Clash', genre: 'Nu Metal', streamUrl: 'https://www.soundhelix.com/examples/mp3/SoundHelix-Song-19.mp3' },
  ],
  CALM: [
    { songName: 'Calm Ocean', genre: 'Ambient', streamUrl: 'https://www.soundhelix.com/examples/mp3/SoundHelix-Song-4.mp3' },
    { songName: 'Calm Mountain', genre: 'Nature', streamUrl: 'https://www.soundhelix.com/examples/mp3/SoundHelix-Song-8.mp3' },
    { songName: 'Calm Forest', genre: 'Zen', streamUrl: 'https://www.soundhelix.com/examples/mp3/SoundHelix-Song-12.mp3' },
    { songName: 'Calm Breeze', genre: 'Chillout', streamUrl: 'https://www.soundhelix.com/examples/mp3/SoundHelix-Song-16.mp3' },
    { songName: 'Calm Silent', genre: 'Meditation', streamUrl: 'https://www.soundhelix.com/examples/mp3/SoundHelix-Song-20.mp3' },
  ],
};

function App() {
  const [moodText, setMoodText] = useState('');
  const [image, setImage] = useState(null);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [currentSong, setCurrentSong] = useState(null);
  const [history, setHistory] = useState([]);
  const [useMock, setUseMock] = useState(false);

  // Dynamic Theme Effect
  React.useEffect(() => {
    if (result?.emotion) {
      document.body.className = `theme-${result.emotion}`;
    }
  }, [result]);


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

  const getMockEmotion = (type, data) => {
    if (type === 'image') return 'HAPPY';
    const text = (data || '').toLowerCase();
    if (text.includes('happy') || text.includes('joy') || text.includes('good') || text.includes('great') || text.includes('love')) return 'HAPPY';
    if (text.includes('sad') || text.includes('cry') || text.includes('depress') || text.includes('miss') || text.includes('lonely')) return 'SAD';
    if (text.includes('angry') || text.includes('mad') || text.includes('hate') || text.includes('furious') || text.includes('rage')) return 'ANGRY';
    if (text.includes('calm') || text.includes('relax') || text.includes('peace') || text.includes('chill') || text.includes('meditate')) return 'CALM';
    return 'HAPPY';
  };

  const analyzeEmotion = async (type) => {
    setLoading(true);
    setResult(null);

    if (useMock) {
      // Simulate network delay
      await new Promise(r => setTimeout(r, 600));
      const detected = getMockEmotion(type, type === 'text' ? moodText : '');
      const data = {
        emotion: detected,
        songs: MOCK_SONGS[detected] || []
      };
      setResult(data);
      setHistory(prev => [
        { emotion: data.emotion, time: new Date().toLocaleTimeString() },
        ...prev
      ].slice(0, 5));
      setLoading(false);
      return;
    }
    
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

      // Fallback to mock data if API returns no songs
      if (!data.songs || data.songs.length === 0) {
        const detected = data.emotion || 'HAPPY';
        data.songs = MOCK_SONGS[detected] || MOCK_SONGS['HAPPY'];
      }

      setResult(data);
      // Update history locally
      setHistory(prev => [
        { emotion: data.emotion, time: new Date().toLocaleTimeString() },
        ...prev
      ].slice(0, 5));
    } catch (error) {
      console.error('Error:', error);
      // Auto-fallback to mock data on API failure
      const detected = getMockEmotion(type, type === 'text' ? moodText : '');
      const fallback = {
        emotion: detected,
        songs: MOCK_SONGS[detected] || []
      };
      setResult(fallback);
      setHistory(prev => [
        { emotion: fallback.emotion, time: new Date().toLocaleTimeString() },
        ...prev
      ].slice(0, 5));
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app-wrapper">
      <div className="sphere sphere-1"></div>
      <div className="sphere sphere-2"></div>
      <div className="app-container">
        <header>
          <h1>VibeCheck</h1>
          <p className="subtitle">Premium Emotion-Based Music</p>
          <label style={{display: 'inline-flex', alignItems: 'center', gap: '0.5rem', marginTop: '0.75rem', cursor: 'pointer', fontSize: '0.85rem', color: 'var(--text-muted)'}}>
            <input
              type="checkbox"
              checked={useMock}
              onChange={(e) => setUseMock(e.target.checked)}
            />
            Use Demo Mode (no AWS required)
          </label>
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
              result.songs && result.songs.length > 0 ? (
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
                  <p>No songs found for <strong>{result.emotion}</strong> vibe.</p>
                  <p style={{fontSize: '0.8rem', marginTop: '1rem'}}>Try a different mood!</p>
                </div>
              )
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

      {history.length > 0 && (
        <div className="recent-vibes-section">
          <label>Recent Vibes</label>
          <div className="recent-vibes">
            {history.map((item, i) => (
              <div key={i} className="vibe-card">
                <strong>{item.emotion}</strong> <span>{item.time}</span>
              </div>
            ))}
          </div>
        </div>
      )}
      </div>
    </div>
  );
}

export default App;
