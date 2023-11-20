import sys
import requests
from PyQt5 import QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QGridLayout, QPushButton, QLineEdit, QMenu, QAction, QLabel, QComboBox
from PyQt5.QtCore import Qt, QRegExp
from PyQt5.QtGui import QRegExpValidator
from math import *
from view import styles

#Import layouts
from layouts.standart import StandartLayout
from layouts.engineering import EngineeringLayout
from layouts.financial import FinancialLayout

#Dependencies
Qt5Dependencies = (QWidget, QVBoxLayout, QGridLayout, QPushButton, Qt, QLineEdit, QLabel, QRegExp, QRegExpValidator, QComboBox)

#App state
##Consts
simpleInterestConst = 'simpleInterest'
compoundInterestConst = 'compoundInterest'
discountingConst = 'discounting'
currencyExchangeConst = 'currencyExchange'

##Default state
financialModeState = currencyExchangeConst

# UI CONFIG
standartColumns = 4
engineeringColumns = 8
financialColumns = 4
notice = ""
res = None

#default window params
windowWidth = 450 #px
windowHeight = 500 #px

#Misc
π = pi
e = exp(1)
τ = tau

#Currencies request
try:
    res = requests.get('https://bank.gov.ua/NBUStatService/v1/statdirectory/exchange?json')
except Exception as e:
    notice = " [OFFLINE]"
def ctg(function):  
    return cos(function)/sin(function)
def sec(function):
    return 1/cos(function)
def cot(function):
    return 1/tan(function)
def runApp():
    global app
    app = QApplication(sys.argv)
    calc = Calculator()
    calc.setMinimumSize(windowWidth, windowHeight)
    calc.setFixedSize(windowWidth, windowHeight)
    calc.show()
    sys.exit(app.exec_())

def restartApp():
    return 1

class Calculator(QMainWindow):
    isInitializing = True

    def loadModeMenuBar(self) -> None:
        menubar = self.menuBar()
        menubar.setStyleSheet(styles.submenu_style)
        menubar.setCursor(Qt.PointingHandCursor)

        modeMenu = menubar.addMenu('&Mode')
        modeMenu.setStyleSheet(styles.submenu_style)
        modeMenu.setCursor(Qt.PointingHandCursor)

        chooseModeSM = QMenu('Choose mode', self)
        chooseModeSM.setStyleSheet(styles.submenu_style)
        chooseModeSM.setCursor(Qt.PointingHandCursor)

        standartMode = QAction('Standart', self)
        standartMode.triggered.connect(self.StandartMode)
        chooseModeSM.addAction(standartMode)

        engineeringMode = QAction('Engineering', self)
        engineeringMode.triggered.connect(self.EngineeringMode)
        chooseModeSM.addAction(engineeringMode)

        financialMode = QAction('Financial', self)
        financialMode.triggered.connect(self.FinancialMode)
        chooseModeSM.addAction(financialMode)

        modeMenu.addMenu(chooseModeSM)

    def setFinancialModeState(self, state: str) -> None:
        global financialModeState
        financialModeState = state
        self.FinancialMode(isStateMethod=True) 

    def loadFinCalcBar(self) -> None:
        menubar = self.menuBar()
        financialModeMenu = menubar.addMenu('&Financial calculator mode')
        financialModeMenu.setStyleSheet(styles.submenu_style)
        financialModeMenu.setCursor(Qt.PointingHandCursor)

        financialMSM = QMenu('Mode', self)
        financialMSM.setStyleSheet(styles.submenu_style)
        financialMSM.setCursor(Qt.PointingHandCursor)

        currencyExchange = QAction('Currency exchange', self)
        currencyExchange.triggered.connect(lambda: self.setFinancialModeState(currencyExchangeConst))
        financialMSM.addAction(currencyExchange)

        simpleInterest = QAction('Simple interest [Credit]', self)
        simpleInterest.triggered.connect(lambda: self.setFinancialModeState(simpleInterestConst))
        financialMSM.addAction(simpleInterest)

        compoundInterest = QAction('Compound interest [Deposit]', self)
        compoundInterest.triggered.connect(lambda: self.setFinancialModeState(compoundInterestConst))
        financialMSM.addAction(compoundInterest)

        discounting = QAction('Discounting', self)
        discounting.triggered.connect(lambda: self.setFinancialModeState(discountingConst))
        financialMSM.addAction(discounting)

        financialModeMenu.addMenu(financialMSM)

    def __init__(self) -> None:
        super().__init__()
        self.initUI()
        self.error_state = False
        self.setWindowIcon(QtGui.QIcon('./icon.ico'))

    def changeResolution(self, width,height) -> None:
        global windowWidth, windowHeight
        windowWidth = width
        windowHeight = height
        self.setFixedSize(windowWidth, windowHeight)

    def StandartMode(self) -> None:
        self.clearResult()
        if self.isInitializing:
            self.isInitializing = False
        self.menuBar().clear()
        self.loadModeMenuBar()
        StandartLayout(self, styles, Qt5Dependencies)

    def EngineeringMode(self) -> None:
        self.clearResult()
        if self.isInitializing:
            self.isInitializing = False
        self.menuBar().clear()
        self.loadModeMenuBar()
        EngineeringLayout(self, styles, Qt5Dependencies)

    def FinancialMode(self, isStateMethod: bool=0) -> None:
        self.clearResult()
        if self.isInitializing:
            self.isInitializing = False
        self.menuBar().clear()
        self.loadModeMenuBar()
        self.loadFinCalcBar()
        FinancialLayout(self, styles, Qt5Dependencies, financialModeState, (simpleInterestConst, compoundInterestConst, discountingConst, currencyExchangeConst), res)

    def initUI(self) -> None:
        self.setWindowTitle(f'Calculator {notice}')
        self.setGeometry(100, 100, 450, 500)
        self.setStyleSheet(styles.window_style)

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        self.resultLineEdit = QLineEdit(central_widget)
        self.resultLineEdit.setPlaceholderText('0')
        self.resultLineEdit.setAlignment(Qt.AlignRight)
        self.resultLineEdit.setFocusPolicy(Qt.NoFocus)
        self.resultLineEdit.setStyleSheet(styles.result_line_style)

        if self.isInitializing: self.StandartMode()

    def appendToResultLineEdit(self) -> None:
        button = self.sender().text()
        current_text = self.resultLineEdit.text()
        new_text = current_text + button
        self.resultLineEdit.setText(new_text)

    def calculateResult(self, calcString=None) -> None:
        if calcString:
            expression = calcString
        else:
            expression = self.resultLineEdit.text()
        
        
        try:
            check = str(expression[::-1])
            for i in check:
                if i=='(':
                    expression += ')'
                    break
                if i==')':
                    break
            result = str(eval(expression.replace("^", "**")))
            self.resultLineEdit.setText(result)
        except Exception as e:
            if calcString:
                print(e)
            else:
                self.resultLineEdit.setText('Error')
                self.error_state = True
                self.disableButtons()

    def disableButtons(self) -> None:
        for button in self.centralWidget().findChildren(QPushButton):
            if button.text() != 'C':
                button.setEnabled(False)

    def clearResult(self) -> None:
        self.resultLineEdit.clear()
        self.enableButtons()

    def enableButtons(self) -> None:
        for button in self.centralWidget().findChildren(QPushButton):
            button.setEnabled(True)

if __name__ == '__main__':
    runApp()
