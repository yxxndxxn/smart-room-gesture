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
        
        # 3. 검지 1개만 (노래 재생)
        if fingers == [0, 1, 0, 0, 0]:
            return "ONE_FINGER"
        
        # 4. 브이 (노래 정지)
        if fingers == [0, 1, 1, 0, 0]:
            return "PEACE"
        
        # 5. 엄지 올리기
        if fingers == [1, 0, 0, 0, 0]:
            thumb_tip = hand_landmarks.landmark[4]
            thumb_base = hand_landmarks.landmark[2]
            if thumb_tip.y < thumb_base.y:
                return "THUMBS_UP"
        
        # 6. 엄지 내리기
        if fingers == [1, 0, 0, 0, 0]:
            thumb_tip = hand_landmarks.landmark[4]
            thumb_base = hand_landmarks.landmark[2]
            if thumb_tip.y > thumb_base.y:
                return "THUMBS_DOWN"
        
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
    controller = DeviceController()
    cap = cv2.VideoCapture(0)
    
    print("=" * 60)
    print("🏠 Smart Room Gesture Control System")
    print("=" * 60)
    print("Gestures:")
    print("  ✊ FIST        -> Light OFF")
    print("  🖐 PALM        -> Light ON")
    print("  👆 ONE_FINGER  -> Play Music")
    print("  ✌️  PEACE       -> Pause Music")
    print("  👍 THUMBS_UP   -> Volume UP")
    print("  👎 THUMBS_DOWN -> Volume DOWN")
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
                    music_status = "PLAYING" if status['music']['playing'] else "PAUSED"
                    
                    cv2.putText(frame, f"Light: {light_status}", (10, 100),
                               cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)
                    cv2.putText(frame, f"Music: {music_status} Vol: {status['music']['volume']}%", (10, 140),
                               cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)
                    
                    # 제스처에 따른 동작 실행
                    if current_gesture != "UNKNOWN" and recognizer.should_trigger_action(current_gesture):
                        print(f"\n{'='*40}")
                        print(f"[GESTURE: {current_gesture}]")
                        print('='*40)
                        
                        if current_gesture == "FIST":
                            controller.toggle_light(False)
                        elif current_gesture == "PALM":
                            controller.toggle_light(True)
                        elif current_gesture == "ONE_FINGER":
                            # 음악이 꺼져있으면 켜기
                            if not controller.music_playing:
                                controller.toggle_music()
                            else:
                                print("Music already playing!")
                        elif current_gesture == "PEACE":
                            # 음악이 켜져있으면 끄기
                            if controller.music_playing:
                                controller.toggle_music()
                            else:
                                print("Music already paused!")
                        elif current_gesture == "THUMBS_UP":
                            controller.volume_up()
                        elif current_gesture == "THUMBS_DOWN":
                            controller.volume_down()
            
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