import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QGridLayout, QPushButton, QLineEdit
from PyQt5.QtCore import Qt


class Calculator(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()  # UI 초기화 메서드 호출

    def init_ui(self):
        # 창 제목 설정
        self.setWindowTitle('아이폰 계산기')

        # 전체 배경색 설정 (검은색)
        self.setStyleSheet('background-color: #000;')  # 전체 창 배경을 검은색으로 설정

        # 전체 레이아웃
        main_layout = QVBoxLayout()

        # 출력창 설정
        self.display = QLineEdit()  # 계산 결과와 입력 값을 표시하는 출력창
        self.display.setReadOnly(True)  # 출력창은 읽기 전용으로 설정
        self.display.setStyleSheet('font-size: 36px; height: 60px; background-color: #000; color: #fff; border: none;')  # 스타일 설정
        self.display.setAlignment(Qt.AlignRight)  # 텍스트를 오른쪽 정렬
        main_layout.addWidget(self.display)  # 출력창을 메인 레이아웃에 추가

        # 버튼 레이아웃
        button_layout = QGridLayout()

        # 버튼 정의 (텍스트, 행, 열, [행 병합, 열 병합])
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
            button.clicked.connect(self.on_button_click)  # 버튼 클릭 이벤트 연결
            if span:  # 버튼이 여러 칸을 차지하는 경우
                button_layout.addWidget(button, row, col, *span)
            else:  # 기본적으로 한 칸만 차지하는 경우
                button_layout.addWidget(button, row, col)

        # 버튼 레이아웃을 메인 레이아웃에 추가
        main_layout.addLayout(button_layout)
        self.setLayout(main_layout)  # 메인 레이아웃 설정

    def get_button_style(self, text):
        """버튼 스타일 설정"""
        if text in {'C', '±', '%'}:  # 기능 버튼 스타일
            return 'font-size: 24px; background-color: #a5a5a5; color: #000; border-radius: 25px; height: 50px;'
        elif text in {'÷', '×', '-', '+', '='}:  # 연산 버튼 스타일
            return 'font-size: 24px; background-color: #f09a36; color: #fff; border-radius: 25px; height: 50px;'
        else:  # 숫자 버튼 스타일
            return 'font-size: 24px; background-color: #333; color: #fff; border-radius: 25px; height: 50px;'

    def on_button_click(self):
        """버튼 클릭 이벤트 처리"""
        sender = self.sender()  # 클릭된 버튼 객체 가져오기
        text = sender.text()  # 버튼의 텍스트 가져오기

        if text == 'C':  # 'C' 버튼: 출력창 초기화
            self.display.clear()
        elif text == '=':  # '=' 버튼: 계산 수행
            try:
                # 입력된 수식을 계산 (×와 ÷를 *, /로 변환)
                result = eval(self.display.text().replace('×', '*').replace('÷', '/'))
                self.display.setText(str(result))  # 결과를 출력창에 표시
            except Exception:  # 계산 중 오류 발생 시
                self.display.setText('오류임')  # 'Error' 메시지 표시
        else:  # 나머지 버튼: 출력창에 텍스트 추가
            self.display.setText(self.display.text() + text)


if __name__ == '__main__':
    app = QApplication(sys.argv)  # PyQt5 애플리케이션 생성
    calculator = Calculator()  # Calculator 클래스 인스턴스 생성
    calculator.resize(350, 500)  # 창 크기 설정
    calculator.show()  # 창 표시
    sys.exit(app.exec_())  # 애플리케이션 실행