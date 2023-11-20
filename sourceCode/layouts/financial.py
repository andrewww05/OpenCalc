from typing import Tuple

def FinancialLayout(self, styles: object, Qt5Dependencies: tuple, financialModeState: str, states: tuple, res) -> None:
    QWidget, QVBoxLayout, QGridLayout, QPushButton, Qt, QLineEdit, QLabel, QRegExp, QRegExpValidator, QComboBox = Qt5Dependencies

    simpleInterest, compoundInterest, discounting, currencyExchange = states
    
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

    class TextArea:
        def __init__(self, value: int or float, position: Tuple[int, int]) -> None:
            self.value = value
            self.position = position # (x, y)
        
        def draw(self):
            validator = QRegExpValidator(QRegExp(r'^\d+(\.\d+)?$'))
            self.textArea = QLineEdit(central_widget)
            self.textArea.setStyleSheet(styles.textArea_financial)
            self.textArea.setCursor(Qt.IBeamCursor)
            self.textArea.setValidator(validator)
            gridLayout.addWidget(self.textArea, self.position[1], self.position[0])

        def text(self):
            return self.textArea.text()

    class Text:
        def __init__(self, text: str, position: Tuple[int, int]) -> None:
            self.text = text
            self.position = position # (x, y)
        
        def draw(self):
            text = QLabel(self.text)
            text.setStyleSheet(styles.text_class_style)
            text.setCursor(Qt.IBeamCursor)
            gridLayout.addWidget(text, self.position[1], self.position[0])

    class VariantBox:
        def __init__(self, position: Tuple[int, int]) -> None:
            self.combo = QComboBox(central_widget)
            self.position = position # (x, y)
            self._bufferedTuple = None
            self.coeficient = 1
    
        def draw(self):
            self.combo.setCursor(Qt.IBeamCursor)
            self.combo.setStyleSheet(styles.combobox_style)
            gridLayout.addWidget(self.combo, self.position[1], self.position[0]) 

        def _setCoeficient(self, value):
            for subTuple in self._bufferedTuple:
                if value == subTuple[0]:
                    self.coeficient = subTuple[1]

        def insert(self, currencies: tuple):
            self._bufferedTuple = currencies
            self.coeficient = currencies[0][1]
            for curr in currencies: # For example: curr = ("USD", 38.15)
                self.combo.addItem(curr[0])
                self.combo.currentTextChanged.connect(self._setCoeficient)

    central_widget = QWidget(self)
    layout = QVBoxLayout()

    layout.addWidget(self.resultLineEdit)

    gridLayout = QGridLayout()

    if financialModeState == currencyExchange:
        self.changeResolution(
            width=450,#px 
            height=600#px
        )
        buttons = [
            Text("Convert:",(1,1)),
            VariantBox((1,2)),

            Text("Mode:", (1,3)),
            VariantBox((1,4)),

            Text("Count", (1,5)),
            TextArea(0, (1,6)),

            Button("Calculate", lambda: self.calculateResult(f'{buttons[5].text()}{buttons[3].coeficient}{buttons[1].coeficient}'), 1, (1, 7))
        ]
        if res != None:
            buffer = []
            for currency in res.json():
                buffer.append((f"{currency['txt']}-{currency['cc']}", currency['rate']))
            buttons[1].insert(tuple(buffer))
        else:
            buttons[1].insert((("USD", 38.15), ("EUR", 38.7), ('Шкура Лева-LSK', 0.0001)))
        buttons[3].insert((('From UAH', '/'),("To UAH", '*')))
    elif financialModeState == simpleInterest:
        self.changeResolution(
            width=450,#px 
            height=650#px
        )
        buttons = [
            Text("Initial capital", (1,1)),
            TextArea(0, (1,2)),

            Text("Annual percentage %", (1,3)),
            TextArea(0, (1,4)),
            
            Text("Years of payment", (1,5)),
            TextArea(0, (1,6)),

            Button("Calculate", lambda: self.calculateResult(f'{buttons[1].text()} * (1 + ({buttons[3].text()} * {buttons[5].text()})/100)'), 1, (1, 7))
        ]
    elif financialModeState == discounting:
        self.changeResolution(
            width=450,#px 
            height=650#px
        )
        buttons = [
            Text("Value in the future", (1,1)),
            TextArea(0, (1,2)),

            Text("Discount rate %", (1,3)),
            TextArea(0, (1,4)),

            Text('Number of reporting periods', (1,5)),
            TextArea(0, (1,6)),

            Button("Calculate", lambda: self.calculateResult(f'{buttons[1].text()}/((1 + {buttons[3].text()}/100) * {buttons[5].text()})'), 1, (1, 7))
        ]
    elif financialModeState == compoundInterest:
        self.changeResolution(
            width=450,#px 
            height=800#px
        )
        buttons = [
            Text("Type of interest calculation", (1,1)),
            VariantBox((1,2)),

            Text("Initial capital", (1,3)),
            TextArea(0, (1,4)),

            Text("Percentage %", (1,5)),
            TextArea(0, (1,6)),
            
            Text("Years of payment", (1,7)),
            TextArea(0, (1,8)),

            Button("Calculate", lambda: self.calculateResult(f'{buttons[3].text()}*(1 + {buttons[5].text()} / {buttons[1].coeficient}) ** ({buttons[7].text()} * {buttons[1].coeficient})'), 1, (1, 9))
        ]
        buttons[1].insert((('monthly', 12), ('annualy', 1)))
    for btn in buttons:
        btn.draw()

    # Add the grid layout to the central widget layout.
    layout.addLayout(gridLayout)

    # Set the central widget layout.
    central_widget.setLayout(layout)

    # Set the central widget.
    self.setCentralWidget(central_widget)