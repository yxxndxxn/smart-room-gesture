# 🏠 제스처 인식 기반 스마트 룸 제어 시스템

AI + IoT를 활용한 비접촉 홈 오토메이션 프로젝트

## 📌 프로젝트 개요

손짓만으로 실내 디바이스(조명, 문, 음악)를 제어할 수 있는 비접촉 스마트 룸 시스템

### 핵심 가치

- **편의성**: 손이 더러울 때, 멀리 있을 때도 기기 제어 가능
- **위생성**: 스위치나 리모컨 접촉 없이 제어
- **직관성**: 자연스러운 제스처로 쉽게 조작

## ✋ 제스처 매핑

| 제스처         | 기능 | 디바이스           |
| -------------- | ---- | ------------------ |
| ✊ 주먹        | 끄기 | LED 조명           |
| 🖐 손바닥 펴기 | 켜기 | LED 조명           |
| 👆 검지 1개    | 열기 | 문 (서보모터)      |
| ✌️ 브이 (2개)  | 닫기 | 문 (서보모터)      |
| 🤟 세 손가락   | 재생 | 음악 (피에조 부저) |
| 🖖 네 손가락   | 정지 | 음악 (피에조 부저) |

## 🛠️ 기술 스택

### AI/ML

- **MediaPipe Hands**: 손 랜드마크 인식 (21개 포인트)
- **제스처 분류기**: 실시간 제스처 인식
- **쿨다운 시스템**: 0.8초 간격으로 오인식 방지

### 하드웨어

- **라즈베리파이 4**: 메인 컨트롤러, AI 모델 실행, 웹서버
- **아두이노 우노**: 시리얼 통신을 통한 디바이스 제어
- **카메라 모듈**: 실시간 제스처 캡처
- **센서/액추에이터**:
  - LED (조명 시뮬레이션)
  - 서보모터 SG90 (문 제어)
  - 피에조 부저 (음악 재생 - 생일 축하 노래)

### 소프트웨어

- **백엔드**: Python 3.11, Flask API
- **프론트엔드**: HTML5, CSS3, JavaScript, Chart.js
- **통신**: 시리얼 통신 (라즈베리파이 ↔ 아두이노), HTTP (API)
- **분석**: CSV 기반 로깅, 행동 패턴 분석

## 📦 설치 방법

### 1. 저장소 클론

```bash
git clone https://github.com/your-username/smart-room-gesture.git
cd smart-room-gesture
```

### 2. 가상환경 생성

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Mac/Linux (라즈베리파이)
python3 -m venv venv
source venv/bin/activate
```

### 3. 라이브러리 설치

```bash
# 라즈베리파이
sudo apt-get update
sudo apt-get install python3-opencv
pip3 install -r requirements.txt --break-system-packages

# Windows/Mac
pip install -r requirements.txt
```

## 🚀 실행 방법

### 방법 1: 제스처 인식 (카메라 화면 포함)

```bash
python gesture_recognition.py
# 또는 라즈베리파이에서
python3 gesture_recognition.py
```

### 방법 2: Flask API 서버 (백그라운드 + 대시보드)

```bash
python app.py
# 또는 라즈베리파이에서
python3 app.py
```

그 다음 브라우저에서:

- 메인 대시보드: `dashboard.html` 열기
- 통계 대시보드: `analytics.html` 열기

### 방법 3: API 테스트

브라우저 주소창:

```
http://localhost:5000/api/status          # 전체 디바이스 상태
http://localhost:5000/api/gesture         # 현재 제스처
http://localhost:5000/api/analytics       # 사용자 행동 분석
```

## 🔌 하드웨어 연결

### 아두이노 회로도

```
LED:
- 아두이노 13번 핀 → LED (+) → 220Ω 저항 → GND

서보모터 (SG90):
- 빨강선 (VCC) → 아두이노 5V
- 갈색선 (GND) → 아두이노 GND
- 주황선 (Signal) → 아두이노 9번 핀

피에조 부저:
- 아두이노 8번 핀 → 부저 (+)
- 부저 (-) → GND

시리얼 통신:
- 아두이노 USB → 라즈베리파이 USB 포트
```

### 라즈베리파이 설정

1. 아두이노를 USB로 연결
2. 포트 확인:

```bash
ls /dev/tty* | grep -E "USB|ACM"
# 보통 /dev/ttyUSB0 또는 /dev/ttyACM0
```

3. 권한 설정:

```bash
sudo chmod 666 /dev/ttyACM0
```

4. 코드에서 포트 수정:

```python
# app.py 및 gesture_recognition.py에서
controller = DeviceController(arduino_port='/dev/ttyACM0')
```

## 📁 프로젝트 구조

```
smart-room-gesture/
├── app.py                      # Flask API 서버
├── gesture_recognition.py      # 메인 제스처 인식
├── device_controller.py        # 디바이스 제어 로직
├── arduino_controller.py       # 아두이노 시리얼 통신
├── analytics.py                # 사용자 행동 분석
├── dashboard.html              # 실시간 제어 대시보드
├── analytics.html              # 통계 분석 대시보드
├── requirements.txt            # Python 의존성
├── gesture_log.csv             # 사용 로그 (자동 생성)
├── arduino/
│   └── smart_room.ino          # 아두이노 스케치
└── README.md
```

## 📊 주요 기능

### 실시간 제어 대시보드

- 실시간 제스처 인식 표시
- 현재 디바이스 상태 (LED, 문, 음악)
- 연결 상태 표시
- 반응형 디자인

### 통계 분석 대시보드

- **제스처 사용 빈도**: 가장 많이 사용한 제스처 막대 그래프
- **디바이스 사용 통계**: 디바이스 제어 패턴 파이 차트
- **시간대별 사용 패턴**: 시간대별 활동 꺾은선 그래프
- **최근 활동 로그**: 타임스탬프 기반 행동 기록
- **요약 통계**: 총 제스처 수, 가장 많이 사용한 제스처/디바이스

### 사용자 행동 패턴 분석

- 모든 제스처 동작 자동 로깅
- CSV 기반 데이터 저장
- 실시간 통계 계산
- 개인화된 사용 인사이트

## 🎯 차별화 포인트

- **능동적 제어** (단순 센서 측정이 아님)
- **AI 기반 인터랙션** (지능형 제스처 인식)
- **통합 대시보드** (모니터링 + 제어 + 분석)
- **실제 하드웨어 연동** (시뮬레이션이 아닌 실제 구현)
- **데이터 기반 인사이트** (행동 패턴 분석)

## 🐛 문제 해결

### 카메라 문제

```bash
# 카메라 테스트
python3 -c "import cv2; cap = cv2.VideoCapture(0); print('OK' if cap.isOpened() else 'FAIL'); cap.release()"
```

### 아두이노 연결 문제

```bash
# USB 디바이스 확인
ls /dev/tty*

# 권한 수정
sudo chmod 666 /dev/ttyUSB0
sudo usermod -a -G dialout $USER
```

### MediaPipe 설치 (라즈베리파이)

```bash
# Python 3.11 사용 (MediaPipe는 3.12+ 미지원)
pip3 install mediapipe==0.10.18
```

## 👤 작성자

- **손기훈** - 숭실대학교 글로벌미디어학부 (학번: 20211591)
- **윤다인** - 숭실대학교 글로벌미디어학부 (학번: 20231635)
