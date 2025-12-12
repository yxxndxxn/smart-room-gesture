from arduino_controller import ArduinoController

class DeviceController:
    def __init__(self, arduino_port=None):
        self.arduino = ArduinoController(arduino_port)
        
        # 디바이스 상태
        self.light_on = False
        self.door_open = False
        self.music_playing = False  # 음악 상태 추가!
    
    def toggle_light(self, turn_on):
        """조명 ON/OFF"""
        command = "LIGHT_ON" if turn_on else "LIGHT_OFF"
        self.arduino.send_command(command)
        
        response = self.arduino.read_response()
        if response and "LIGHT:" in response:
            self.light_on = response.split(":")[1] == "1"
        else:
            self.light_on = turn_on
        
        status = "ON" if self.light_on else "OFF"
        print(f"💡 Light: {status}")
        return status
    
    def open_door(self):
        """문 열기"""
        self.arduino.send_command("DOOR_OPEN")
        
        response = self.arduino.read_response()
        if response and "DOOR:" in response:
            self.door_open = response.split(":")[1] == "1"
        else:
            self.door_open = True
        
        print(f"🚪 Door: OPEN")
        return "OPEN"
    
    def close_door(self):
        """문 닫기"""
        self.arduino.send_command("DOOR_CLOSE")
        
        response = self.arduino.read_response()
        if response and "DOOR:" in response:
            self.door_open = response.split(":")[1] == "1"
        else:
            self.door_open = False
        
        print(f"🚪 Door: CLOSED")
        return "CLOSED"
    
    def play_music(self):
        """음악 재생"""
        self.arduino.send_command("MUSIC_PLAY")
        
        response = self.arduino.read_response()
        if response and "MUSIC:" in response:
            self.music_playing = response.split(":")[1] == "1"
        else:
            self.music_playing = True
        
        print(f"🎵 Music: PLAYING")
        return "PLAYING"
    
    def stop_music(self):
        """음악 정지"""
        self.arduino.send_command("MUSIC_STOP")
        
        response = self.arduino.read_response()
        if response and "MUSIC:" in response:
            self.music_playing = response.split(":")[1] == "1"
        else:
            self.music_playing = False
        
        print(f"🎵 Music: STOPPED")
        return "STOPPED"
    
    def get_status(self):
        """현재 모든 디바이스 상태 반환"""
        return {
            "light": {
                "on": self.light_on
            },
            "door": {
                "open": self.door_open
            },
            "music": {
                "playing": self.music_playing
            }
        }
    
    def close(self):
        self.arduino.close()