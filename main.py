import sys
import serial
import serial.tools.list_ports

from PyQt5.QtWidgets import (
    QApplication, QDialog, QMainWindow, QMessageBox
)
from PyQt5.QtCore import QTimer
from PyQt5.uic import loadUi

from gui import Ui_MainWindow

import minimalmodbus

BAUDRATE = 57600
ADDRESS = 1
TABLE_HEIGHT_ADDRESS = 2000
BUTTON_PRESS_ADDRESS = 2002
USER_POS_1_ADDRESS = 26004
USER_POS_2_ADDRESS = 26006
USER_POS_3_ADDRESS = 26008
USER_POS_4_ADDRESS = 26010


class Window(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.timer = QTimer(self)
        self.connectSignalsSlots()
        

    def connectSignalsSlots(self):
        self.refreshButton.clicked.connect(self.refreshComboBox)
        #self.action_Exit.triggered.connect(self.close)
        #self.action_About.triggered.connect(self.about)
        self.connectButton.clicked.connect(self.connect)
        self.timer.timeout.connect(self.getHeight)
        self.button1.clicked.connect(self.setPosition1)
        self.button2.clicked.connect(self.setPosition2)
        self.button3.clicked.connect(self.setPosition3)
        self.button4.clicked.connect(self.setPosition4)
        self.upButton.pressed.connect(self.moveUp)
        self.upButton.released.connect(self.stopMove)
        self.downButton.pressed.connect(self.moveDown)
        self.downButton.released.connect(self.stopMove)

        self.actionSet_Position_1.triggered.connect(self.storePosition1)



    def refreshComboBox(self):
        ports = serial.tools.list_ports.comports()
        self.portlist = [port.name for port in ports]

        self.COMList.clear()
        for port in ports:
            self.COMList.addItem(port.name)

    def connect(self):
        print(self.COMList.currentText())
        self.table = minimalmodbus.Instrument(self.COMList.currentText(), 1)
        self.table.serial.baudrate = BAUDRATE 
        self.table.serial.stopbits = 2
        self.timer.start(500)

    def getHeight(self):
        self.height = self.readRegister(TABLE_HEIGHT_ADDRESS, 0)
        self.heightLCD.display(self.height)

    def setPosition1(self):
        self.writeRegister(BUTTON_PRESS_ADDRESS, 1, 0)
        height = self.readRegister(USER_POS_1_ADDRESS,0)
        self.heightLCD.display(height)
        print("go to preset 1:"+str(height)+" cm")
        
    def setPosition2(self):
        self.writeRegister(BUTTON_PRESS_ADDRESS, 2, 0)
        height = self.readRegister(USER_POS_2_ADDRESS,0)
        self.heightLCD.display(height)
        print("go to preset 2:"+str(height)+" cm")
    
    def setPosition3(self):
        self.writeRegister(BUTTON_PRESS_ADDRESS, 3, 0)
        height = self.readRegister(USER_POS_3_ADDRESS,0)
        self.heightLCD.display(height)
        print("go to preset 3:"+str(height)+" cm")

    def setPosition4(self):
        self.writeRegister(BUTTON_PRESS_ADDRESS, 4, 0)
        height = self.readRegister(USER_POS_4_ADDRESS,0)
        self.heightLCD.display(height)
        print("go to preset 4:"+str(height)+" cm")


    def moveUp(self):
        self.writeRegister(BUTTON_PRESS_ADDRESS, 5, 0)
        #self.writeRegister(BUTTON_PRESS_ADDRESS, 5, 0)

    def moveDown(self):
        self.writeRegister(BUTTON_PRESS_ADDRESS, 6, 0)
    
    def stopMove(self):
        self.writeRegister(BUTTON_PRESS_ADDRESS, 0, 0)
    
    def storePosition1(self):
        self.writeRegister(USER_POS_1_ADDRESS, self.height, 0)
    def storePosition2(self):
        self.writeRegister(USER_POS_2_ADDRESS, self.height, 0)
    def storePosition3(self):
        self.writeRegister(USER_POS_3_ADDRESS, self.height, 0)
    def storePosition4(self):
        self.writeRegister(USER_POS_4_ADDRESS, self.height, 0)

    def readRegister(self,*args):
        try:
            answer = self.table.read_register(*args)
        except Exception as error:
            answer = None
            # handle the exception
            print("An exception occurred:", type(error).__name__)
        return answer
    
    def writeRegister(self, *args):
        print("Writeregister"+str(args))
        try:
            self.table.write_register(*args)
        except Exception as error:
            # handle the exception
            print("An exception occurred:", type(error).__name__)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = Window()
    win.show()
    sys.exit(app.exec())
