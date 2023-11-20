def StandartLayout(self, styles: object, Qt5Dependencies: tuple) -> None:
    QWidget, QVBoxLayout, QGridLayout, QPushButton, Qt, QLineEdit, QLabel, QRegExp, QRegExpValidator, QComboBox = Qt5Dependencies

    self.changeResolution(
        width=450,#px 
        height=500#px
    )

    class Button:
        def __init__(self, char: str, func: callable, btnStyle: bool, position: (int, int)) -> None:
            self.char = char
            self.func = func
            self.btnStyle = btnStyle # 0 = grey, 1 = blue
            self.position = position # (x, y)
        
        def draw(self):
            button = QPushButton(self.char, central_widget)
            button.clicked.connect(self.func)
            button.setStyleSheet(styles.button_style if self.btnStyle == 0 else styles.button_style_secondary)
            button.setCursor(Qt.PointingHandCursor)
            gridLayout.addWidget(button, self.position[1], self.position[0])

    central_widget = QWidget(self)
    layout = QVBoxLayout()
    layout.addWidget(self.resultLineEdit)
    gridLayout = QGridLayout()

    buttons = [
        Button('C', self.clearResult, 1, (1, 1)),
        Button('(', self.appendToResultLineEdit, 1, (2, 1)),
        Button(')', self.appendToResultLineEdit, 1, (3, 1)),
        Button('%', self.appendToResultLineEdit, 1, (4, 1)),

        Button('7', self.appendToResultLineEdit, 0, (1, 2)),
        Button('8', self.appendToResultLineEdit, 0, (2, 2)),
        Button('9', self.appendToResultLineEdit, 0, (3, 2)),
        Button('/', self.appendToResultLineEdit, 1, (4, 2)),
        
        Button('4', self.appendToResultLineEdit, 0, (1, 3)),
        Button('5', self.appendToResultLineEdit, 0, (2, 3)),
        Button('6', self.appendToResultLineEdit, 0, (3, 3)),
        Button('*', self.appendToResultLineEdit, 1, (4, 3)),
        
        Button('1', self.appendToResultLineEdit, 0, (1, 4)),
        Button('2', self.appendToResultLineEdit, 0, (2, 4)),
        Button('3', self.appendToResultLineEdit, 0, (3, 4)),
        Button('-', self.appendToResultLineEdit, 1, (4, 4)),

        Button('0', self.appendToResultLineEdit, 0, (1, 5)),
        Button('.', self.appendToResultLineEdit, 0, (2, 5)),
        Button('=', self.calculateResult, 1, (3, 5)),
        Button('+', self.appendToResultLineEdit, 1, (4, 5)),
    ]
    
    for btn in buttons:
        btn.draw()

    # Add the grid layout to the central widget layout.
    layout.addLayout(gridLayout)

    # Set the central widget layout.
    central_widget.setLayout(layout)

    # Set the central widget.
    self.setCentralWidget(central_widget)