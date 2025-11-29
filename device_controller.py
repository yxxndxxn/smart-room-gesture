from arduino_controller import ArduinoController

class DeviceController:
    def __init__(self, arduino_port=None):
        """
        디바이스 컨트롤러 초기화
        arduino_port: 아두이노 포트 (None이면 시뮬레이션 모드)
        """
        # 아두이노 연결
        self.arduino = ArduinoController(arduino_port)
        
        # 디바이스 상태
        self.light_on = False
        self.light_brightness = 50
        
        self.music_playing = False
        self.volume = 50
        self.current_song = "Song 1"
        
        self.fan_speed = 0
    
    def toggle_light(self, turn_on):
        """조명 ON/OFF"""
        # 아두이노에 명령 전송
        command = "LIGHT_ON" if turn_on else "LIGHT_OFF"
        self.arduino.send_command(command)
        
        # 응답 확인 (실제 아두이노가 있을 때)
        response = self.arduino.read_response()
        if response and "LIGHT:" in response:
            # 아두이노 응답으로 상태 업데이트
            self.light_on = response.split(":")[1] == "1"
        else:
            # 시뮬레이션 모드에서는 바로 업데이트
            self.light_on = turn_on
        
        status = "ON" if self.light_on else "OFF"
        print(f"💡 Light: {status}")
        return status
    
    def toggle_music(self):
        """음악 재생/정지"""
        self.arduino.send_command("MUSIC_TOGGLE")
        
        response = self.arduino.read_response()
        if response and "MUSIC:" in response:
            self.music_playing = response.split(":")[1] == "1"
        else:
            # 시뮬레이션
            self.music_playing = not self.music_playing
        
        status = "PLAYING" if self.music_playing else "PAUSED"
        print(f"🎵 Music: {status}")
        return status
    
    def volume_up(self):
        """볼륨 증가"""
        new_volume = min(100, self.volume + 10)
        self.arduino.send_command(f"VOLUME:{new_volume}")
        
        response = self.arduino.read_response()
        if response and "VOLUME:" in response:
            self.volume = int(response.split(":")[1])
        else:
            self.volume = new_volume
        
        print(f"🔊 Volume UP: {self.volume}%")
        return self.volume
    
    def volume_down(self):
        """볼륨 감소"""
        new_volume = max(0, self.volume - 10)
        self.arduino.send_command(f"VOLUME:{new_volume}")
        
        response = self.arduino.read_response()
        if response and "VOLUME:" in response:
            self.volume = int(response.split(":")[1])
        else:
            self.volume = new_volume
        
        print(f"🔉 Volume DOWN: {self.volume}%")
        return self.volume
    
    def set_fan_speed(self, speed):
        """팬 속도 조절 (0-100)"""
        speed = max(0, min(100, speed))
        self.arduino.send_command(f"FAN:{speed}")
        
        response = self.arduino.read_response()
        if response and "FAN:" in response:
            self.fan_speed = int(response.split(":")[1])
        else:
            self.fan_speed = speed
        
        print(f"🌀 Fan Speed: {self.fan_speed}%")
        return self.fan_speed
    
    def get_status(self):
        """현재 모든 디바이스 상태 반환"""
        return {
            "light": {
                "on": self.light_on,
                "brightness": self.light_brightness
            },
            "music": {
                "playing": self.music_playing,
                "volume": self.volume,
                "song": self.current_song
            },
            "fan": {
                "speed": self.fan_speed
            }
        }
    
    def close(self):
        """연결 종료"""
        self.arduino.close()

# 테스트 코드
if __name__ == "__main__":
    print("=== Device Controller Test ===\n")
    
    # 시뮬레이션 모드로 테스트
    controller = DeviceController()
    
    print("\n--- Testing Light ---")
    controller.toggle_light(True)
    controller.toggle_light(False)
    
    print("\n--- Testing Music ---")
    controller.toggle_music()
    controller.volume_up()
    controller.volume_down()
    
    print("\n--- Testing Fan ---")
    controller.set_fan_speed(50)
    
    print("\n--- Current Status ---")
    print(controller.get_status())
    
    controller.close()