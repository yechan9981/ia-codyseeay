# mars_mission_computer.py

class DummySensor:
    def get_internal_temperature(self):
        return 20  # 예제 값 (내부 온도)

    def get_external_temperature(self):
        return -60  # 예제 값 (외부 온도)

    def get_internal_humidity(self):
        return 40  # 예제 값 (내부 습도)

    def get_external_illuminance(self):
        return 300  # 예제 값 (외부 광량)

    def get_internal_co2(self):
        return 0.04  # 예제 값 (내부 CO2 농도)

    def get_internal_oxygen(self):
        return 21  # 예제 값 (내부 산소 농도)


class MissionComputer:
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
        counter = 0  # 5분 평균 계산을 위한 카운터
        while self.running:
            # 센서 값 업데이트
            self.env_values['mars_base_internal_temperature'] = self.ds.get_internal_temperature()
            self.env_values['mars_base_external_temperature'] = self.ds.get_external_temperature()
            self.env_values['mars_base_internal_humidity'] = self.ds.get_internal_humidity()
            self.env_values['mars_base_external_illuminance'] = self.ds.get_external_illuminance()
            self.env_values['mars_base_internal_co2'] = self.ds.get_internal_co2()
            self.env_values['mars_base_internal_oxygen'] = self.ds.get_internal_oxygen()

            # 5분 평균 계산을 위한 데이터 저장
            self.data_history.append(self.env_values.copy())
            if len(self.data_history) > 60:  # 최대 60개의 데이터만 유지 (5초 간격으로 5분치 데이터)
                self.data_history.pop(0)

            # 현재 센서 데이터를 JSON 형식으로 출력
            print('{')
            for key, value in self.env_values.items():
                print(f'    "{key}": {value},')
            print('}')

            # 5분 평균을 5분마다 출력
            counter += 1
            # if counter == 60:  # 60번 반복 후 (5초 * 60 = 5분)
            if counter == 3:
                counter = 0
                averages = {key: sum(d[key] for d in self.data_history) / len(self.data_history)
                            for key in self.env_values}
                print('5분 평균:')
                print('{')
                for key, value in averages.items():
                    print(f'    "{key}": {value},')
                print('}')

            # 5초 지연 시뮬레이션
            for _ in range(50):
                if not self.running:  # 실행 상태 확인
                    break
                for _ in range(10000000):  # 지연을 위한 빈 루프
                    pass

    def stop(self):
        # 시스템 중지
        self.running = False
        print('Sytem stoped….')


# MissionComputer 인스턴스 생성 및 실행
RunComputer = MissionComputer()
try:
    RunComputer.get_sensor_data()
except KeyboardInterrupt:  # 키보드 인터럽트(Ctrl+C)로 중지
    RunComputer.stop()