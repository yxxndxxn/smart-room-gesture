from flask import Flask, jsonify
from flask_cors import CORS
import cv2
import threading
import time
from gesture_recognition import GestureRecognizer
from device_controller import DeviceController

app = Flask(__name__)
CORS(app)  # 워드프레스에서 접근 가능하도록

# 전역 변수
recognizer = GestureRecognizer()
controller = DeviceController()  # 시뮬레이션 모드
current_gesture = "UNKNOWN"

class GestureRecognitionThread(threading.Thread):
    """백그라운드에서 계속 제스처 인식"""
    def __init__(self):
        super().__init__()
        self.running = True
        self.cap = cv2.VideoCapture(0)
        self.daemon = True  # 메인 프로그램 종료시 같이 종료
    
    def run(self):
        global current_gesture
        
        print("🎥 Camera thread started")
        
        while self.running:
            success, frame = self.cap.read()
            if not success:
                time.sleep(0.1)
                continue
            
            frame = cv2.flip(frame, 1)
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = recognizer.hands.process(frame_rgb)
            
            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    gesture = recognizer.recognize_gesture(hand_landmarks)
                    current_gesture = gesture
                    
                    # 제스처에 따른 동작 실행
                    if gesture != "UNKNOWN" and recognizer.should_trigger_action(gesture):
                        print(f"\n[API] Gesture detected: {gesture}")
                        
                        if gesture == "FIST":
                            controller.toggle_light(False)
                        elif gesture == "PALM":
                            controller.toggle_light(True)
                        elif gesture == "ONE_FINGER":
                            if not controller.music_playing:
                                controller.toggle_music()
                        elif gesture == "PEACE":
                            if controller.music_playing:
                                controller.toggle_music()
                        elif gesture == "THUMBS_UP":
                            controller.volume_up()
                        elif gesture == "THUMBS_DOWN":
                            controller.volume_down()
            else:
                current_gesture = "UNKNOWN"
            
            time.sleep(0.05)  # CPU 사용량 조절
    
    def stop(self):
        self.running = False
        self.cap.release()
        print("🎥 Camera thread stopped")

# 백그라운드 스레드 시작
gesture_thread = None

@app.route('/')
def index():
    """API 정보"""
    return jsonify({
        "name": "Smart Room Gesture Control API",
        "version": "1.0",
        "endpoints": {
            "/api/status": "Get device status",
            "/api/gesture": "Get current gesture",
            "/api/devices/light": "Get light status",
            "/api/devices/music": "Get music status"
        }
    })

@app.route('/api/status')
def get_status():
    """전체 디바이스 상태 반환"""
    status = controller.get_status()
    status['current_gesture'] = current_gesture
    return jsonify(status)

@app.route('/api/gesture')
def get_gesture():
    """현재 제스처만 반환"""
    return jsonify({
        "gesture": current_gesture,
        "timestamp": time.time()
    })

@app.route('/api/devices/light')
def get_light_status():
    """조명 상태만 반환"""
    status = controller.get_status()
    return jsonify(status['light'])

@app.route('/api/devices/music')
def get_music_status():
    """음악 상태만 반환"""
    status = controller.get_status()
    return jsonify(status['music'])

@app.route('/api/devices/fan')
def get_fan_status():
    """팬 상태만 반환"""
    status = controller.get_status()
    return jsonify(status['fan'])

def start_gesture_recognition():
    """제스처 인식 스레드 시작"""
    global gesture_thread
    if gesture_thread is None or not gesture_thread.is_alive():
        gesture_thread = GestureRecognitionThread()
        gesture_thread.start()

if __name__ == '__main__':
    print("=" * 60)
    print("🏠 Smart Room Gesture Control API Server")
    print("=" * 60)
    print("\nStarting gesture recognition...")
    
    # 제스처 인식 시작
    start_gesture_recognition()
    
    print("\n✅ Server ready!")
    print("📡 API running on http://localhost:5000")
    print("\nAvailable endpoints:")
    print("  - http://localhost:5000/api/status")
    print("  - http://localhost:5000/api/gesture")
    print("  - http://localhost:5000/api/devices/light")
    print("  - http://localhost:5000/api/devices/music")
    print("\n Press Ctrl+C to stop\n")
    print("=" * 60)
    
    try:
        app.run(host='0.0.0.0', port=5000, debug=False, use_reloader=False)
    except KeyboardInterrupt:
        print("\n\n👋 Shutting down...")
        if gesture_thread:
            gesture_thread.stop()
        controller.close()
        print("✅ Server stopped!")