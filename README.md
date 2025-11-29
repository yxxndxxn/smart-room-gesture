# 🏠 제스처 인식 기반 스마트 룸 제어 시스템

AI + IoT를 활용한 비접촉 홈 오토메이션 프로젝트

## 📌 프로젝트 개요

손짓만으로 실내 디바이스(조명, 음악, 팬 등)를 제어할 수 있는 비접촉 스마트 룸 시스템

## ✋ 제스처 목록

| 제스처         | 기능      |
| -------------- | --------- |
| ✊ 주먹        | 조명 OFF  |
| 🖐 손바닥 펴기 | 조명 ON   |
| 👆 검지 1개    | 음악 재생 |
| ✌️ 브이 (2개)  | 음악 정지 |
| 👍 엄지 UP     | 볼륨 UP   |
| 👎 엄지 DOWN   | 볼륨 DOWN |

## 🛠️ 기술 스택

- **AI/ML**: MediaPipe Hands
- **언어**: Python 3.11
- **프레임워크**: Flask, OpenCV
- **하드웨어**: 라즈베리파이, 아두이노
- **프론트엔드**: WordPress (대시보드)

## 📦 설치 방법

### 1. 저장소 클론

```bash
git clone https://github.com/your-username/smart-room-gesture.git
cd smart-room-gesture
```

### 2. 가상환경 생성 및 활성화

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

### 3. 라이브러리 설치

```bash
pip install -r requirements.txt
```

## 🚀 실행 방법

### 1. Flask API 서버 실행

```bash
python app.py
```

### 2. 제스처 인식 테스트 (웹캠 화면 포함)

```bash
python gesture_recognition.py
```

### 3. API 테스트

브라우저에서 다음 주소 접속:

- `http://localhost:5000/api/status` - 전체 상태
- `http://localhost:5000/api/gesture` - 현재 제스처

## 📁 프로젝트 구조

```
smart-room-gesture/
├── app.py                    # Flask API 서버
├── gesture_recognition.py    # 제스처 인식 메인
├── device_controller.py      # 디바이스 제어 로직
├── arduino_controller.py     # 아두이노 통신
└── requirements.txt          # 라이브러리 목록
```

## 🔌 하드웨어 연결 (라즈베리파이)

1. 아두이노를 라즈베리파이에 USB 연결
2. `device_controller.py`에서 포트 설정:

```python
controller = DeviceController(arduino_port='/dev/ttyUSB0')
```

## 📄 라이선스

This project is open source.
