import serial
import time

class ArduinoController:
    def __init__(self, port=None, baudrate=9600):
        """
        아두이노 컨트롤러 초기화
        port: 시리얼 포트 (None이면 시뮬레이션 모드)
              Windows: 'COM3', 'COM4' 등
              라즈베리파이: '/dev/ttyUSB0', '/dev/ttyACM0' 등
        """
        self.connected = False
        self.serial = None
        
        if port:
            try:
                self.serial = serial.Serial(port, baudrate, timeout=1)
                time.sleep(2)  # 아두이노 리셋 대기
                print(f"✅ Arduino connected on {port}")
                self.connected = True
            except Exception as e:
                print(f"❌ Arduino connection failed: {e}")
                print("⚠️  Running in SIMULATION mode")
                self.connected = False
        else:
            print("⚠️  No port specified - Running in SIMULATION mode")
    
    def send_command(self, command):
        """아두이노에 명령 전송"""
        if self.connected:
            try:
                self.serial.write(f"{command}\n".encode())
                print(f"📤 [SENT to Arduino] {command}")
                return True
            except Exception as e:
                print(f"❌ Send error: {e}")
                return False
        else:
            # 시뮬레이션 모드
            print(f"🔷 [SIMULATION] Would send: {command}")
            return True
    
    def read_response(self):
        """아두이노로부터 응답 읽기"""
        if self.connected:
            try:
                if self.serial.in_waiting > 0:
                    response = self.serial.readline().decode().strip()
                    print(f"📥 [RECEIVED from Arduino] {response}")
                    return response
            except Exception as e:
                print(f"❌ Read error: {e}")
        else:
            # 시뮬레이션 모드 - 가짜 응답
            return None
        
        return None
    
    def close(self):
        """연결 종료"""
        if self.connected and self.serial:
            self.serial.close()
            print("🔌 Arduino disconnected")

# 테스트 코드
if __name__ == "__main__":
    print("=== Arduino Controller Test ===\n")
    
    # 시뮬레이션 모드로 테스트
    controller = ArduinoController()
    
    # 명령 테스트
    controller.send_command("LIGHT_ON")
    controller.send_command("VOLUME:50")
    controller.send_command("MUSIC_TOGGLE")
    
    print("\n✅ Test completed!")