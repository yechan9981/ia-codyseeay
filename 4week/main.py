import random

# mars_mission_computer.py
class DummySensor:
    def __init__(self):
        # 환경 데이터를 저장할 사전 초기화
        self.env_values = {
            'mars_base_internal_temperature': 0,  # 내부 온도
            'mars_base_external_temperature': 0,  # 외부 온도
            'mars_base_internal_humidity': 0,     # 내부 습도
            'mars_base_external_illuminance': 0,  # 외부 광량
            'mars_base_internal_co2': 0,          # 내부 CO2
            'mars_base_internal_oxygen': 0        # 내부 산소
        }

    def set_env(self):
        """랜덤 값으로 환경 데이터 설정"""
        self.env_values['mars_base_internal_temperature'] = random.uniform(18, 30)  # 18~30도
        self.env_values['mars_base_external_temperature'] = random.uniform(0, 21)   # 0~21도
        self.env_values['mars_base_internal_humidity'] = random.uniform(50, 60)     # 50~60%
        self.env_values['mars_base_external_illuminance'] = random.uniform(500, 715)  # 500~715 W/m2
        self.env_values['mars_base_internal_co2'] = random.uniform(0.02, 0.1)       # 0.02~0.1%
        self.env_values['mars_base_internal_oxygen'] = random.uniform(4, 7)         # 4~7%

    def get_env(self):
        """환경 데이터를 반환하고 로그 파일에 기록"""
        log = (
            f'내부온도: {self.env_values["mars_base_internal_temperature"]:.2f}°C, \n'
            f'외부온도: {self.env_values["mars_base_external_temperature"]:.2f}°C, \n'
            f'  습도 : {self.env_values["mars_base_internal_humidity"]:.2f}%, \n'
            f'  광량 : {self.env_values["mars_base_external_illuminance"]:.2f} W/m2, \n'
            f'  CO2 : {self.env_values["mars_base_internal_co2"]:.2f}%, \n'
            f'산소농도: {self.env_values["mars_base_internal_oxygen"]:.2f}%\n\n'
        )
        
        # 파일에 로그 추가
        with open('mars_mission_log.txt', 'a') as file:
            file.write(log + '\n')
        
        return self.env_values


class MissionComputer:
    DELAY_LOOP_COUNT = 500000000  # 빈 루프 반복 횟수 (5초 지연 시뮬레이션)

    def __init__(self):
        # 환경 데이터를 저장할 사전 초기화
        self.env_values = {
            'mars_base_internal_temperature': 0,  # 내부 온도
            'mars_base_external_temperature': 0,  # 외부 온도
            'mars_base_internal_humidity': 0,     # 내부 습도
            'mars_base_external_illuminance': 0,  # 외부 광량
            'mars_base_internal_co2': 0,          # 내부 CO2 농도
            'mars_base_internal_oxygen': 0        # 내부 산소 농도
        }
        self.ds = DummySensor()  # DummySensor 객체 생성
        self.running = True  # 시스템 실행 상태 플래그
        self.data_history = []  # 5분 평균 계산을 위한 데이터 기록

    def get_sensor_data(self):
        """센서 데이터를 주기적으로 가져오고 출력"""
        counter = 0  # 5분 평균 계산을 위한 카운터
        while self.running:
            # 센서 값 업데이트
            self.ds.set_env()
            self.env_values = self.ds.get_env()

            # 5분 평균 계산을 위한 데이터 저장
            self.data_history.append(self.env_values.copy())
            if len(self.data_history) > 60:  # 최대 60개의 데이터만 유지 (5초 간격으로 5분치 데이터)
                self.data_history.pop(0)

            # 현재 센서 데이터를 JSON 형식으로 출력
            print('{')
            for i, (key, value) in enumerate(self.env_values.items()):
                comma = ',' if i < len(self.env_values) - 1 else ''  # 마지막 항목에는 쉼표 제거
                print(f'    "{key}": {value:.2f}{comma}')
            print('}')

            # 5분 평균을 5분마다 출력
            counter += 1
            if counter == 5:  # 60번 반복 후 (5초 * 60 = 5분) 임시로 5로 설정
                counter = 0
                averages = {key: sum(d[key] for d in self.data_history) / len(self.data_history)
                            for key in self.env_values}
                print('\n')
                print('5분 평균:')
                print('------------------')
                print('{')
                for i, (key, value) in enumerate(averages.items()):
                    comma = ',' if i < len(averages) - 1 else ''  # 마지막 항목에는 쉼표 제거
                    print(f'    "{key}": {value:.2f}{comma}')
                print('}')
                print('------------------')
                print('\n')

            # 5초 지연 시뮬레이션 (빈 루프 사용)
            for _ in range(self.DELAY_LOOP_COUNT):
                pass

    def stop(self):
        """시스템 중지"""
        self.running = False
        print('System stopped.')


# MissionComputer 인스턴스 생성 및 실행
RunComputer = MissionComputer()
try:
    RunComputer.get_sensor_data()
except KeyboardInterrupt:  # 키보드 인터럽트(Ctrl+C)로 중지
    RunComputer.stop()