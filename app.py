from flask import Flask, jsonify
from flask_cors import CORS
import cv2
import threading
import time
from gesture_recognition import GestureRecognizer
from device_controller import DeviceController

app = Flask(__name__)
CORS(app)

# 전역 변수
recognizer = GestureRecognizer()
controller = DeviceController(arduino_port='/dev/ttyUSB0')  # 또는 /dev/ttyACM0
current_gesture = "UNKNOWN"

class GestureRecognitionThread(threading.Thread):
    """백그라운드에서 계속 제스처 인식"""
    def __init__(self):
        super().__init__()
        self.running = True
        self.cap = None
        self.daemon = True
    
    def run(self):
        global current_gesture, controller
        
        print("🎥 Camera thread starting...")
        
        # 카메라 초기화
        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            print("❌ Camera not found!")
            return
        
        print("✅ Camera thread started")
        
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
                    
                    # 제스처에 따른 동작 실행 - controller 직접 호출!
                    if gesture != "UNKNOWN" and recognizer.should_trigger_action(gesture):
                        print(f"\n[API] Gesture detected: {gesture}")
                        
                        if gesture == "FIST":
                            controller.toggle_light(False)
                        elif gesture == "PALM":
                            controller.toggle_light(True)
                        elif gesture == "ONE_FINGER":
                            controller.open_door()
                        elif gesture == "PEACE":
                            controller.close_door()
                        elif gesture == "THREE_FINGERS":
                            controller.play_music()
                        elif gesture == "FOUR_FINGERS":
                            controller.stop_music()
                        
                        # 상태 변경 후 출력
                        status = controller.get_status()
                        print(f"Current status: {status}")
            else:
                current_gesture = "UNKNOWN"
            
            time.sleep(0.05)
    
    def stop(self):
        self.running = False
        if self.cap:
            self.cap.release()
        print("🎥 Camera thread stopped")

# 백그라운드 스레드
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
            "/api/devices/door": "Get door status"
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

@app.route('/api/devices/door')
def get_door_status():
    """문 상태만 반환"""
    status = controller.get_status()
    return jsonify(status['door'])

@app.route('/api/devices/music')
def get_music_status():
    """음악 상태만 반환"""
    status = controller.get_status()
    return jsonify(status['music'])

@app.route('/api/analytics')
def get_analytics():
    """사용자 행동 패턴 분석 데이터"""
    analytics = controller.get_analytics()
    return jsonify(analytics)

@app.route('/api/analytics/gestures')
def get_gesture_analytics():
    """제스처 빈도만"""
    analytics = controller.get_analytics()
    return jsonify(analytics['gesture_frequency'])

@app.route('/api/analytics/devices')
def get_device_analytics():
    """디바이스 사용 통계만"""
    analytics = controller.get_analytics()
    return jsonify(analytics['device_usage'])

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
    
    # 카메라 스레드가 시작될 때까지 잠깐 대기
    time.sleep(2)
    
    print("\n✅ Server ready!")
    print("📡 API running on http://0.0.0.0:5000")
    print("\nAvailable endpoints:")
    print("  - http://localhost:5000/api/status")
    print("  - http://localhost:5000/api/gesture")
    print("  - http://localhost:5000/api/devices/light")
    print("  - http://localhost:5000/api/devices/door")
    print("\n Press Ctrl+C to stop\n")
    print("=" * 60)
    
    try:
        app.run(host='0.0.0.0', port=5000, debug=False, use_reloader=False, threaded=True)
    except KeyboardInterrupt:
        print("\n\n👋 Shutting down...")
        if gesture_thread:
            gesture_thread.stop()
        controller.close()
        print("✅ Server stopped!")