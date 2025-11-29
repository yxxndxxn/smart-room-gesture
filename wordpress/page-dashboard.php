<?php
/*
Template Name: Smart Room Dashboard
Description: Real-time gesture control dashboard
*/
get_header();
?>

<style>
    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }
    
    body {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        min-height: 100vh;
    }
    
    .dashboard-container {
        max-width: 1400px;
        margin: 0 auto;
        padding: 40px 20px;
    }
    
    .dashboard-header {
        text-align: center;
        color: white;
        margin-bottom: 40px;
    }
    
    .dashboard-header h1 {
        font-size: 3em;
        margin-bottom: 10px;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    .dashboard-header p {
        font-size: 1.2em;
        opacity: 0.9;
    }
    
    /* 제스처 디스플레이 */
    .gesture-display {
        background: white;
        border-radius: 20px;
        padding: 40px;
        margin-bottom: 30px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.3);
        text-align: center;
    }
    
    .gesture-display h2 {
        color: #333;
        margin-bottom: 20px;
        font-size: 1.5em;
    }
    
    .gesture-text {
        font-size: 4em;
        font-weight: bold;
        color: #667eea;
        min-height: 100px;
        display: flex;
        align-items: center;
        justify-content: center;
        animation: pulse 2s infinite;
    }
    
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.7; }
    }
    
    .gesture-emoji {
        font-size: 5em;
        margin-right: 20px;
    }
    
    /* 상태 그리드 */
    .status-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
        gap: 30px;
        margin-top: 30px;
    }
    
    .status-card {
        background: white;
        border-radius: 20px;
        padding: 30px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        transition: transform 0.3s, box-shadow 0.3s;
    }
    
    .status-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 40px rgba(0,0,0,0.3);
    }
    
    .status-card h2 {
        color: #333;
        margin-bottom: 20px;
        font-size: 1.8em;
        display: flex;
        align-items: center;
        gap: 10px;
    }
    
    .card-icon {
        font-size: 1.5em;
    }
    
    .status-value {
        font-size: 2.5em;
        font-weight: bold;
        margin: 20px 0;
        transition: color 0.3s;
    }
    
    .status-details {
        color: #666;
        font-size: 1.1em;
        line-height: 1.8;
    }
    
    .status-details div {
        display: flex;
        justify-content: space-between;
        padding: 8px 0;
        border-bottom: 1px solid #eee;
    }
    
    .status-details div:last-child {
        border-bottom: none;
    }
    
    /* 조명 색상 */
    .light-on { color: #ffd700; }
    .light-off { color: #999; }
    
    /* 음악 색상 */
    .music-playing { color: #1db954; }
    .music-paused { color: #999; }
    
    /* 팬 색상 */
    .fan-active { color: #00bfff; }
    .fan-inactive { color: #999; }
    
    /* 프로그레스 바 */
    .progress-bar {
        width: 100%;
        height: 20px;
        background: #eee;
        border-radius: 10px;
        overflow: hidden;
        margin-top: 10px;
    }
    
    .progress-fill {
        height: 100%;
        background: linear-gradient(90deg, #667eea, #764ba2);
        transition: width 0.3s;
        border-radius: 10px;
    }
    
    /* 연결 상태 */
    .connection-status {
        position: fixed;
        top: 20px;
        right: 20px;
        background: white;
        padding: 15px 25px;
        border-radius: 30px;
        box-shadow: 0 5px 15px rgba(0,0,0,0.2);
        display: flex;
        align-items: center;
        gap: 10px;
        z-index: 1000;
    }
    
    .status-dot {
        width: 12px;
        height: 12px;
        border-radius: 50%;
        background: #1db954;
        animation: blink 2s infinite;
    }
    
    .status-dot.disconnected {
        background: #ff4444;
    }
    
    @keyframes blink {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.3; }
    }
    
    /* 반응형 */
    @media (max-width: 768px) {
        .dashboard-header h1 {
            font-size: 2em;
        }
        
        .gesture-text {
            font-size: 2.5em;
        }
        
        .status-grid {
            grid-template-columns: 1fr;
        }
    }
</style>

<div class="connection-status">
    <div class="status-dot" id="connection-dot"></div>
    <span id="connection-text">Connected</span>
</div>

<div class="dashboard-container">
    <div class="dashboard-header">
        <h1>🏠 Smart Room Control Dashboard</h1>
        <p>Gesture-based Home Automation System</p>
    </div>
    
    <!-- 현재 제스처 -->
    <div class="gesture-display">
        <h2>Current Gesture</h2>
        <div class="gesture-text" id="gesture">
            <span class="gesture-emoji" id="gesture-emoji">👋</span>
            <span id="gesture-name">Waiting...</span>
        </div>
    </div>
    
    <!-- 디바이스 상태 -->
    <div class="status-grid">
        <!-- 조명 카드 -->
        <div class="status-card">
            <h2>
                <span class="card-icon">💡</span>
                Light Control
            </h2>
            <div class="status-value light-off" id="light-status">OFF</div>
            <div class="status-details">
                <div>
                    <span>Status:</span>
                    <strong id="light-status-text">Off</strong>
                </div>
                <div>
                    <span>Brightness:</span>
                    <strong id="light-brightness">50%</strong>
                </div>
            </div>
            <div class="progress-bar">
                <div class="progress-fill" id="light-progress" style="width: 50%"></div>
            </div>
        </div>
        
        <!-- 음악 카드 -->
        <div class="status-card">
            <h2>
                <span class="card-icon">🎵</span>
                Music Player
            </h2>
            <div class="status-value music-paused" id="music-status">PAUSED</div>
            <div class="status-details">
                <div>
                    <span>Status:</span>
                    <strong id="music-status-text">Paused</strong>
                </div>
                <div>
                    <span>Volume:</span>
                    <strong id="music-volume">50%</strong>
                </div>
                <div>
                    <span>Song:</span>
                    <strong id="music-song">Song 1</strong>
                </div>
            </div>
            <div class="progress-bar">
                <div class="progress-fill" id="volume-progress" style="width: 50%"></div>
            </div>
        </div>
        
        <!-- 팬 카드 -->
        <div class="status-card">
            <h2>
                <span class="card-icon">🌀</span>
                Fan Control
            </h2>
            <div class="status-value fan-inactive" id="fan-status">OFF</div>
            <div class="status-details">
                <div>
                    <span>Speed:</span>
                    <strong id="fan-speed">0%</strong>
                </div>
                <div>
                    <span>Status:</span>
                    <strong id="fan-status-text">Inactive</strong>
                </div>
            </div>
            <div class="progress-bar">
                <div class="progress-fill" id="fan-progress" style="width: 0%"></div>
            </div>
        </div>
    </div>
</div>

<script>
// Flask API URL (라즈베리파이 IP로 변경 필요)
const API_URL = 'http://localhost:5000';

// 제스처 이모지 매핑
const GESTURE_EMOJIS = {
    'FIST': '✊',
    'PALM': '🖐',
    'ONE_FINGER': '👆',
    'PEACE': '✌️',
    'THUMBS_UP': '👍',
    'THUMBS_DOWN': '👎',
    'UNKNOWN': '🤷'
};

// 제스처 이름 매핑
const GESTURE_NAMES = {
    'FIST': 'Fist',
    'PALM': 'Palm Open',
    'ONE_FINGER': 'One Finger',
    'PEACE': 'Peace Sign',
    'THUMBS_UP': 'Thumbs Up',
    'THUMBS_DOWN': 'Thumbs Down',
    'UNKNOWN': 'Waiting...'
};

// 상태 업데이트 함수
async function updateStatus() {
    try {
        // API 호출
        const response = await fetch(`${API_URL}/api/status`);
        
        if (!response.ok) {
            throw new Error('API connection failed');
        }
        
        const data = await response.json();
        
        // 연결 상태 업데이트
        document.getElementById('connection-dot').classList.remove('disconnected');
        document.getElementById('connection-text').textContent = 'Connected';
        
        // 제스처 업데이트
        const gesture = data.current_gesture || 'UNKNOWN';
        document.getElementById('gesture-emoji').textContent = GESTURE_EMOJIS[gesture];
        document.getElementById('gesture-name').textContent = GESTURE_NAMES[gesture];
        
        // 조명 상태 업데이트
        const lightStatus = document.getElementById('light-status');
        lightStatus.textContent = data.light.on ? 'ON' : 'OFF';
        lightStatus.className = 'status-value ' + (data.light.on ? 'light-on' : 'light-off');
        document.getElementById('light-status-text').textContent = data.light.on ? 'On' : 'Off';
        document.getElementById('light-brightness').textContent = data.light.brightness + '%';
        document.getElementById('light-progress').style.width = data.light.brightness + '%';
        
        // 음악 상태 업데이트
        const musicStatus = document.getElementById('music-status');
        musicStatus.textContent = data.music.playing ? 'PLAYING' : 'PAUSED';
        musicStatus.className = 'status-value ' + (data.music.playing ? 'music-playing' : 'music-paused');
        document.getElementById('music-status-text').textContent = data.music.playing ? 'Playing' : 'Paused';
        document.getElementById('music-volume').textContent = data.music.volume + '%';
        document.getElementById('music-song').textContent = data.music.song;
        document.getElementById('volume-progress').style.width = data.music.volume + '%';
        
        // 팬 상태 업데이트
        const fanSpeed = data.fan.speed;
        const fanStatus = document.getElementById('fan-status');
        fanStatus.textContent = fanSpeed > 0 ? 'ON' : 'OFF';
        fanStatus.className = 'status-value ' + (fanSpeed > 0 ? 'fan-active' : 'fan-inactive');
        document.getElementById('fan-speed').textContent = fanSpeed + '%';
        document.getElementById('fan-status-text').textContent = fanSpeed > 0 ? 'Active' : 'Inactive';
        document.getElementById('fan-progress').style.width = fanSpeed + '%';
        
    } catch (error) {
        console.error('Error fetching status:', error);
        
        // 연결 실패 표시
        document.getElementById('connection-dot').classList.add('disconnected');
        document.getElementById('connection-text').textContent = 'Disconnected';
        document.getElementById('gesture-name').textContent = 'Connection Error';
    }
}

// 페이지 로드 시 즉시 업데이트
updateStatus();

// 0.5초마다 상태 업데이트 (실시간처럼 보이게)
setInterval(updateStatus, 500);
</script>

<?php get_footer(); ?>