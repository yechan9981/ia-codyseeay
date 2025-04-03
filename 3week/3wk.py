import random

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
        # 랜덤 값으로 환경 데이터 설정
        self.env_values['mars_base_internal_temperature'] = random.uniform(18, 30)  # 18~30도
        self.env_values['mars_base_external_temperature'] = random.uniform(0, 21)   # 0~21도
        self.env_values['mars_base_internal_humidity'] = random.uniform(50, 60)     # 50~60%
        self.env_values['mars_base_external_illuminance'] = random.uniform(500, 715)  # 500~715 W/m2
        self.env_values['mars_base_internal_co2'] = random.uniform(0.02, 0.1)       # 0.02~0.1%
        self.env_values['mars_base_internal_oxygen'] = random.uniform(4, 7)         # 4~7%

    def get_env(self):
        # 로그 파일에 데이터 기록
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

if __name__ == "__main__":
    # DummySensor 객체 생성
    ds = DummySensor()

    # 환경 데이터 설정하고 가져오기
    ds.set_env()
    data = ds.get_env()

    # 결과 출력
    print('Mars Base Environmental Data:')
    for key, value in data.items():
        print(f'{key}: {value:.2f}')





        