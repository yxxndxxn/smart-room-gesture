import cv2
import mediapipe as mp

# MediaPipe 손 인식 초기화
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)

# 웹캠 시작
cap = cv2.VideoCapture(0)

print("Webcam started! Show your hand to the camera!")
print("Press 'q' to quit.")

while cap.isOpened():
    success, frame = cap.read()
    if not success:
        print("Cannot read webcam.")
        continue
    
    # 좌우 반전 (거울처럼 보이게)
    frame = cv2.flip(frame, 1)
    
    # BGR을 RGB로 변환
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(frame_rgb)
    
    # 손이 감지되면 그리기
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(
                frame, 
                hand_landmarks, 
                mp_hands.HAND_CONNECTIONS
            )
            # 이모지 제거
            print("Hand detected!")
    
    cv2.imshow('Hand Detection Test', frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()