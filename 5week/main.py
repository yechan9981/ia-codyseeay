import random
import os
import platform
import psutil
import time

# DummySensor 클래스: 화성 기지의 환경 데이터를 시뮬레이션
class DummySensor:
    def __init__(self):
        # 환경 데이터를 저장하는 딕셔너리
        self.env_values = {
            'mars_base_internal_temperature': 0,  # 내부 온도
            'mars_base_external_temperature': 0,  # 외부 온도
            'mars_base_internal_humidity': 0,     # 내부 습도
            'mars_base_external_illuminance': 0, # 외부 광량
            'mars_base_internal_co2': 0,         # 내부 CO2 농도
            'mars_base_internal_oxygen': 0       # 내부 산소 농도
        }

    # 환경 데이터를 랜덤 값으로 설정
    def set_env(self):
        self.env_values['mars_base_internal_temperature'] = random.uniform(18, 30)
        self.env_values['mars_base_external_temperature'] = random.uniform(0, 21)
        self.env_values['mars_base_internal_humidity'] = random.uniform(50, 60)
        self.env_values['mars_base_external_illuminance'] = random.uniform(500, 715)
        self.env_values['mars_base_internal_co2'] = random.uniform(0.02, 0.1)
        self.env_values['mars_base_internal_oxygen'] = random.uniform(4, 7)

    # 환경 데이터를 반환하고 로그 파일에 기록
    def get_env(self):
        log = (
            f'내부온도: {self.env_values["mars_base_internal_temperature"]:.2f}°C, '
            f'외부온도: {self.env_values["mars_base_external_temperature"]:.2f}°C, '
            f'습도: {self.env_values["mars_base_internal_humidity"]:.2f}%, '
            f'광량: {self.env_values["mars_base_external_illuminance"]:.2f} W/m2, '
            f'CO2: {self.env_values["mars_base_internal_co2"]:.2f}%, '
            f'산소농도: {self.env_values["mars_base_internal_oxygen"]:.2f}%\n'
        )
        # 로그 파일에 기록
        with open('mars_mission_log.txt', 'a') as file:
            file.write(log)
        return self.env_values


# MissionComputer 클래스: 센서 데이터를 관리하고 시스템 정보를 출력
class MissionComputer:
    def __init__(self):
        self.ds = DummySensor()  # DummySensor 객체 생성
        self.running = True      # 프로그램 실행 상태 플래그
        self.data_history = []   # 최근 5분 동안의 데이터를 저장

    # 데이터를 JSON 형식으로 출력
    def print_json(self, data):
        print('{')
        for i, (key, value) in enumerate(data.items()):
            comma = ',' if i < len(data) - 1 else ''  # 마지막 항목에는 쉼표 제거
            if isinstance(value, float):  # 실수인 경우 소수점 두 번째 자리까지 출력
                print(f'    "{key}": {value:.2f}{comma}')
            else:  # 문자열 또는 정수 그대로 출력
                print(f'    "{key}": "{value}"{comma}')
        print('}')

    # 시스템 정보를 가져와 JSON 형식으로 출력
    def get_mission_computer_info(self):
        try:
            system_info = {
                '운영체계': platform.system(),
                '운영체계 버전': platform.version(),
                'CPU 타입': platform.processor(),
                'CPU 코어 수': os.cpu_count(),
                '메모리 크기': psutil.virtual_memory().total // (1024 * 1024)  # MB 단위
            }
            print('미션 컴퓨터 시스템 정보:')
            self.print_json(system_info)
        except Exception as e:
            print(f'시스템 정보를 가져오는 중 오류 발생: {e}')

    # 실시간 부하 정보를 가져와 JSON 형식으로 출력
    def get_mission_computer_load(self):
        try:
            load_info = {
                'CPU 실시간 사용량': psutil.cpu_percent(interval=1),
                '메모리 실시간 사용량': psutil.virtual_memory().percent
            }
            print('미션 컴퓨터 부하 정보:')
            self.print_json(load_info)
        except Exception as e:
            print(f'부하 정보를 가져오는 중 오류 발생: {e}')

    # 센서 데이터를 주기적으로 가져오고 출력
    def get_sensor_data(self):
        counter = 0  # 5분 평균 계산을 위한 카운터
        while self.running:
            self.ds.set_env()  # 센서 값 업데이트
            env_values = self.ds.get_env()  # 현재 센서 데이터 가져오기
            self.data_history.append(env_values.copy())  # 데이터 기록
            if len(self.data_history) > 60:  # 최대 60개의 데이터만 유지 (5초 간격으로 5분치 데이터)
                self.data_history.pop(0)

            # 현재 센서 데이터를 JSON 형식으로 출력
            print('현재 센서 데이터:')
            self.print_json(env_values)

            # 5분 평균 계산 및 출력
            counter += 1
            if counter == 60:  # 60번 반복 후 (5초 * 60 = 5분)
                counter = 0
                averages = {key: sum(d[key] for d in self.data_history) / len(self.data_history)
                            for key in env_values}
                print('\n5분 평균:')
                self.print_json(averages)

            time.sleep(1)  # 1초 지연

    # 프로그램 실행 중지
    def stop(self):
        self.running = False
        print('System stopped.')


# 프로그램 실행
if __name__ == "__main__":
    runComputer = MissionComputer()
    try:
        print('\n--- 미션 컴퓨터 시스템 정보 ---')
        runComputer.get_mission_computer_info()
        print('\n--- 미션 컴퓨터 부하 정보 ---')
        runComputer.get_mission_computer_load()
        runComputer.get_sensor_data()
    except KeyboardInterrupt:  # Ctrl+C로 프로그램 종료
        runComputer.stop()