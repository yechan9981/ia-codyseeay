import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QGridLayout, QPushButton, QLineEdit
from PyQt5.QtCore import Qt


class Calculator:
    def __init__(self):
        self.reset()  # 계산기 초기화

    def reset(self):
        """계산기 초기화"""
        self.current_value = '0'  # 현재 입력 값
        self.previous_value = None  # 이전 값
        self.operator = None  # 현재 연산자
        self.waiting_for_new_input = False  # 새로운 입력 대기 상태

    def negative_positive(self):
        """음수/양수 변환"""
        if self.current_value.startswith('-'):
            self.current_value = self.current_value[1:]  # 음수를 양수로 변환
        else:
            self.current_value = '-' + self.current_value  # 양수를 음수로 변환

    def percent(self):
        """퍼센트 계산"""
        try:
            self.current_value = str(float(self.current_value) / 100)  # 현재 값을 100으로 나눔
        except ValueError:
            self.current_value = '오류'  # 잘못된 값 처리

    def equal(self):
        """결과 계산"""
        self._calculate()  # 계산 수행
        self.operator = None  # 연산자 초기화
        self.previous_value = None  # 이전 값 초기화
        self.waiting_for_new_input = True  # 새로운 입력 대기 상태로 설정

    def _calculate(self):
        """현재 값과 이전 값으로 계산 수행"""
        if self.operator and self.previous_value is not None:
            try:
                a = float(self.previous_value)  # 이전 값
                b = float(self.current_value)  # 현재 값
                if self.operator == '+':
                    result = a + b
                elif self.operator == '-':
                    result = a - b
                elif self.operator == '*':
                    result = a * b
                elif self.operator == '/':
                    if b == 0:
                        self.current_value = '오류'  # 0으로 나누기 처리
                        return
                    result = a / b

                # 결과가 정수인지 확인
                if result.is_integer():
                    self.current_value = str(int(result))  # 정수로 변환
                else:
                    self.current_value = str(result)  # 실수로 유지

            except:
                self.current_value = '오류'  # 계산 중 오류 처리

        self.previous_value = self.current_value  # 현재 값을 이전 값으로 설정


class CalculatorUI(QWidget):
    def __init__(self):
        super().__init__()
        self.calculator = Calculator()  # Calculator 클래스 인스턴스 생성
        self.init_ui()  # UI 초기화

    def init_ui(self):
        """UI 초기화"""
        self.setWindowTitle('아이폰 계산기')  # 창 제목 설정
        self.setStyleSheet('background-color: #000;')  # 배경색 설정

        main_layout = QVBoxLayout()  # 메인 레이아웃 생성

        # 출력창 설정
        self.display = QLineEdit('0')  # 초기값 0으로 설정
        self.display.setReadOnly(True)  # 읽기 전용으로 설정
        self.display.setStyleSheet('font-size: 36px; height: 60px; background-color: #000; color: #fff; border: none;')  # 스타일 설정
        self.display.setAlignment(Qt.AlignRight)  # 텍스트 오른쪽 정렬
        main_layout.addWidget(self.display)  # 출력창을 메인 레이아웃에 추가

        # 버튼 레이아웃 설정
        button_layout = QGridLayout()
        buttons = [
            ('C', 0, 0), ('±', 0, 1), ('%', 0, 2), ('÷', 0, 3),
            ('7', 1, 0), ('8', 1, 1), ('9', 1, 2), ('×', 1, 3),
            ('4', 2, 0), ('5', 2, 1), ('6', 2, 2), ('-', 2, 3),
            ('1', 3, 0), ('2', 3, 1), ('3', 3, 2), ('+', 3, 3),
            ('0', 4, 0, 1, 2), ('.', 4, 2), ('=', 4, 3)
        ]

        # 버튼 생성 및 배치
        for text, row, col, *span in buttons:
            button = QPushButton(text)  # 버튼 생성
            button.setStyleSheet(self.get_button_style(text))  # 버튼 스타일 설정
            button.clicked.connect(lambda checked, t=text: self.on_button_click(t))  # 버튼 클릭 이벤트 연결
            if span:
                button_layout.addWidget(button, row, col, *span)  # 병합된 버튼 배치
            else:
                button_layout.addWidget(button, row, col)  # 일반 버튼 배치

        main_layout.addLayout(button_layout)  # 버튼 레이아웃을 메인 레이아웃에 추가
        self.setLayout(main_layout)  # 메인 레이아웃 설정

    def get_button_style(self, text):
        """버튼 스타일 설정"""
        if text in {'C', '±', '%'}:
            return 'font-size: 24px; background-color: #a5a5a5; color: #000; border-radius: 25px; height: 50px;'
        elif text in {'÷', '×', '-', '+', '='}:
            return 'font-size: 24px; background-color: #f09a36; color: #fff; border-radius: 25px; height: 50px;'
        else:
            return 'font-size: 24px; background-color: #333; color: #fff; border-radius: 25px; height: 50px;'

    def on_button_click(self, text):
        """버튼 클릭 이벤트 처리"""
        if text.isdigit() or text == '.':
            # 숫자 또는 소수점 입력 처리
            if self.calculator.waiting_for_new_input:
                self.calculator.current_value = '0' if text != '.' else '0.'
                self.calculator.waiting_for_new_input = False

            if text == '.' and '.' in self.calculator.current_value:
                return
            elif self.calculator.current_value == '0' and text != '.':
                self.calculator.current_value = text
            else:
                self.calculator.current_value += text

            # 연산자 포함된 상태에서 보여주기
            if self.calculator.operator:
                op_display = {'+': '+', '-': '-', '*': '×', '/': '÷'}
                self.display.setText(f"{self.calculator.previous_value} {op_display[self.calculator.operator]} {self.calculator.current_value}")
            else:
                self.display.setText(self.calculator.current_value)

        elif text == 'C':
            # 초기화 버튼
            self.calculator.reset()
            self.display.setText('0')

        elif text == '±':
            # 음수/양수 변환
            self.calculator.negative_positive()
            self.display.setText(self.calculator.current_value)

        elif text == '%':
            # 퍼센트 계산
            self.calculator.percent()
            self.display.setText(self.calculator.current_value)

        elif text in {'+', '-', '×', '÷'}:
            # 연산자 클릭 시
            if self.calculator.operator and not self.calculator.waiting_for_new_input:
                self.calculator._calculate()

            self.calculator.previous_value = self.calculator.current_value
            self.calculator.waiting_for_new_input = True

            if text == '×':
                self.calculator.operator = '*'
            elif text == '÷':
                self.calculator.operator = '/'
            else:
                self.calculator.operator = text

            self.display.setText(f"{self.calculator.previous_value} {text}")

        elif text == '=':
            # 결과 계산
            self.calculator.equal()
            self.display.setText(self.calculator.current_value)

        self.update_display()

    def update_display(self):
        """출력창 업데이트"""
        value = self.calculator.current_value
        if len(value) > 12:
            self.display.setStyleSheet('font-size: 24px; height: 60px; background-color: #000; color: #fff; border: none;')
        else:
            self.display.setStyleSheet('font-size: 36px; height: 60px; background-color: #000; color: #fff; border: none;')


if __name__ == '__main__':
    # 애플리케이션 실행
    app = QApplication(sys.argv)
    calculator_ui = CalculatorUI()
    calculator_ui.resize(400, 600)
    calculator_ui.show()
    sys.exit(app.exec_())
