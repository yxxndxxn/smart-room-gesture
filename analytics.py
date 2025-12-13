import csv
import os
from datetime import datetime
from collections import Counter

class GestureAnalytics:
    def __init__(self, log_file='gesture_log.csv'):
        self.log_file = log_file
        
        # CSV 파일 없으면 생성
        if not os.path.exists(self.log_file):
            with open(self.log_file, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(['timestamp', 'gesture', 'device', 'action'])
    
    def log_gesture(self, gesture, device, action):
        """제스처 기록"""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        with open(self.log_file, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([timestamp, gesture, device, action])
        
        print(f"📊 [LOG] {gesture} -> {device} {action}")
    
    def get_gesture_frequency(self):
        """제스처 사용 빈도"""
        gestures = []
        
        with open(self.log_file, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                gestures.append(row['gesture'])
        
        frequency = Counter(gestures)
        return dict(frequency)
    
    def get_device_usage(self):
        """디바이스 사용 통계"""
        devices = []
        
        with open(self.log_file, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                devices.append(row['device'])
        
        usage = Counter(devices)
        return dict(usage)
    
    def get_hourly_usage(self):
        """시간대별 사용 패턴"""
        hours = []
        
        with open(self.log_file, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                timestamp = datetime.strptime(row['timestamp'], '%Y-%m-%d %H:%M:%S')
                hours.append(timestamp.hour)
        
        hourly = Counter(hours)
        return dict(hourly)
    
    def get_recent_logs(self, limit=10):
        """최근 활동 로그"""
        logs = []
        
        with open(self.log_file, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                logs.append(row)
        
        # 최근 N개만
        return logs[-limit:][::-1]  # 역순으로
    
    def get_total_gestures(self):
        """총 제스처 수"""
        with open(self.log_file, 'r') as f:
            reader = csv.DictReader(f)
            return sum(1 for row in reader)
    
    def get_statistics(self):
        """전체 통계"""
        return {
            'total_gestures': self.get_total_gestures(),
            'gesture_frequency': self.get_gesture_frequency(),
            'device_usage': self.get_device_usage(),
            'hourly_usage': self.get_hourly_usage(),
            'recent_logs': self.get_recent_logs(10)
        }