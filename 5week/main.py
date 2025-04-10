import random
import os
import platform
import psutil  # 시스템 정보를 가져오기 위해 사용
import time  # 지연을 위해 사용

class DummySensor:
    def __init__(self):
        self.env_values = {
            'mars_base_internal_temperature': 0,
            'mars_base_external_temperature': 0,
            'mars_base_internal_humidity': 0,
            'mars_base_external_illuminance': 0,
            'mars_base_internal_co2': 0,
            'mars_base_internal_oxygen': 0
        }

    def set_env(self):
        self.env_values['mars_base_internal_temperature'] = random.uniform(18, 30)
        self.env_values['mars_base_external_temperature'] = random.uniform(0, 21)
        self.env_values['mars_base_internal_humidity'] = random.uniform(50, 60)
        self.env_values['mars_base_external_illuminance'] = random.uniform(500, 715)
        self.env_values['mars_base_internal_co2'] = random.uniform(0.02, 0.1)
        self.env_values['mars_base_internal_oxygen'] = random.uniform(4, 7)

    def get_env(self):
        return self.env_values


class MissionComputer:
    def __init__(self):
        self.ds = DummySensor()
        self.running = True
        self.data_history = []

    def print_json(self, data):
        """데이터를 JSON 형식으로 출력"""
        print('{')
        for i, (key, value) in enumerate(data.items()):
            comma = ',' if i < len(data) - 1 else ''
            print(f'    "{key}": "{value}"{comma}')
        print('}')

    def get_mission_computer_info(self):
        """미션 컴퓨터의 시스템 정보를 가져와 JSON 형식으로 출력"""
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

    def get_mission_computer_load(self):
        """미션 컴퓨터의 실시간 부하 정보를 가져와 JSON 형식으로 출력"""
        try:
            load_info = {
                'CPU 실시간 사용량': psutil.cpu_percent(interval=1),
                '메모리 실시간 사용량': psutil.virtual_memory().percent
            }
            print('미션 컴퓨터 부하 정보:')
            self.print_json(load_info)
        except Exception as e:
            print(f'부하 정보를 가져오는 중 오류 발생: {e}')

    def get_sensor_data(self):
        counter = 0
        while self.running:
            self.ds.set_env()
            env_values = self.ds.get_env()
            self.data_history.append(env_values.copy())
            if len(self.data_history) > 60:
                self.data_history.pop(0)
            print('현재 센서 데이터:')
            self.print_json(env_values)
            counter += 1
            if counter == 60:
                counter = 0
                averages = {key: sum(d[key] for d in self.data_history) / len(self.data_history)
                            for key in env_values}
                print('\n5분 평균:')
                self.print_json(averages)
            time.sleep(1)

    def stop(self):
        self.running = False
        print('System stopped.')


if __name__ == "__main__":
    runComputer = MissionComputer()
    try:
        print('\n--- 미션 컴퓨터 시스템 정보 ---')
        runComputer.get_mission_computer_info()
        print('\n--- 미션 컴퓨터 부하 정보 ---')
        runComputer.get_mission_computer_load()
        runComputer.get_sensor_data()
    except KeyboardInterrupt:
        runComputer.stop()