import cv2
import mediapipe as mp
import time
from device_controller import DeviceController

class GestureRecognizer:
    def __init__(self):
        self.mp_hands = mp.solutions.hands
        self.mp_drawing = mp.solutions.drawing_utils
        self.hands = self.mp_hands.Hands(
            max_num_hands=1,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.7
        )
        
        self.last_gesture = None
        self.last_action_time = 0
        self.action_cooldown = 0.8
    
    def get_finger_status(self, hand_landmarks):
        finger_tips = [4, 8, 12, 16, 20]
        finger_pips = [3, 6, 10, 14, 18]
        
        fingers_up = []
        
        if hand_landmarks.landmark[finger_tips[0]].x < hand_landmarks.landmark[finger_pips[0]].x:
            fingers_up.append(1)
        else:
            fingers_up.append(0)
        
        for i in range(1, 5):
            if hand_landmarks.landmark[finger_tips[i]].y < hand_landmarks.landmark[finger_pips[i]].y:
                fingers_up.append(1)
            else:
                fingers_up.append(0)
        
        return fingers_up
    
    def recognize_gesture(self, hand_landmarks):
        fingers = self.get_finger_status(hand_landmarks)
        fingers_count = fingers.count(1)
        
        # 1. 주먹
        if fingers_count == 0:
            return "FIST"
        
        # 2. 손바닥
        if fingers_count == 5:
            return "PALM"
        
        # 3. 검지 1개만
        if fingers == [0, 1, 0, 0, 0]:
            return "ONE_FINGER"
        
        # 4. 브이
        if fingers == [0, 1, 1, 0, 0]:
            return "PEACE"
        
        # 5. 세 손가락 (검지 + 중지 + 약지) - 음악 재생 ⭐
        if fingers == [0, 1, 1, 1, 0]:
            return "THREE_FINGERS"
    
        # 6. 네 손가락 (엄지 빼고 전부) - 음악 정지 ⭐
        if fingers == [0, 1, 1, 1, 1]:
            return "FOUR_FINGERS"
        
        return "UNKNOWN"
    
    def should_trigger_action(self, current_gesture):
        current_time = time.time()
        
        if current_gesture == self.last_gesture:
            if current_time - self.last_action_time < self.action_cooldown:
                return False
        
        self.last_gesture = current_gesture
        self.last_action_time = current_time
        return True

def main():
    recognizer = GestureRecognizer()
    controller = DeviceController(arduino_port='COM3')
    cap = cv2.VideoCapture(0)
    
    print("=" * 60)
    print("🏠 Smart Room Gesture Control System")
    print("=" * 60)
    print("Gestures:")
    print("  ✊ FIST        -> LED OFF")
    print("  🖐 PALM        -> LED ON")
    print("  👆 ONE_FINGER  -> Door OPEN")
    print("  ✌️  PEACE       -> Door CLOSE")
    print("  🤟 THREE_FINGERS -> Music PLAY")
    print("  🖖 FOUR_FINGERS  -> Music STOP")
    print("=" * 60)
    print("\nPress 'q' to quit.\n")
    
    try:
        while cap.isOpened():
            success, frame = cap.read()
            if not success:
                continue
            
            frame = cv2.flip(frame, 1)
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = recognizer.hands.process(frame_rgb)
            
            current_gesture = "UNKNOWN"
            
            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    recognizer.mp_drawing.draw_landmarks(
                        frame,
                        hand_landmarks,
                        recognizer.mp_hands.HAND_CONNECTIONS
                    )
                    
                    current_gesture = recognizer.recognize_gesture(hand_landmarks)
                    
                    # 제스처 표시
                    cv2.putText(frame, f"Gesture: {current_gesture}", (10, 50),
                               cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                    
                    # 디바이스 상태 표시
                    status = controller.get_status()
                    light_status = "ON" if status['light']['on'] else "OFF"
                    door_status = "OPEN" if status['door']['open'] else "CLOSED"
                    music_status = "PLAYING" if status['music']['playing'] else "STOPPED"
                    
                    cv2.putText(frame, f"Light: {light_status}", (10, 100),
                               cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)
                    cv2.putText(frame, f"Door: {door_status}", (10, 140),
                               cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)
                    cv2.putText(frame, f"Music: {music_status}", (10, 180),
                               cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)
                    
                    # 제스처에 따른 동작 실행
                    if current_gesture != "UNKNOWN" and recognizer.should_trigger_action(current_gesture):
                        print(f"\n{'='*40}")
                        print(f"[GESTURE: {current_gesture}]")
                        print('='*40)
                        
                        if current_gesture == "FIST":
                            controller.toggle_light(False)  # LED OFF
                            
                        elif current_gesture == "PALM":
                            controller.toggle_light(True)   # LED ON
                            
                        elif current_gesture == "ONE_FINGER":
                            controller.open_door()          # 문 열기
                            
                        elif current_gesture == "PEACE":
                            controller.close_door()         # 문 닫기
                            
                        elif current_gesture == "THREE_FINGERS":
                            controller.play_music()         # 음악 재생 ⭐
                            
                        elif current_gesture == "FOUR_FINGERS":
                            controller.stop_music()         # 음악 정지 ⭐
            
            cv2.imshow('Smart Room Control', frame)
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    
    finally:
        cap.release()
        cv2.destroyAllWindows()
        controller.close()
        print("\n👋 System shutdown complete!")

if __name__ == "__main__":
    main()