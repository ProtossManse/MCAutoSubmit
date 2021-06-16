import pyautogui as pag
import sys
import os
import keyboard
import webbrowser

import PyQt5
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5 import QtTest

f3p = 0

def resource_path(relative_path):
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)
    
form = resource_path('autosubmit.ui')
 
form_class = uic.loadUiType(form)[0]

class MainDialog(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self, None)
        PyQt5.uic.loadUi(form, self)
        self.seedbutton.clicked.connect(self.seedClicked)
        self.f3Box.clicked.connect(self.f3Clicked)
        self.resetButton.clicked.connect(self.reset)
        self.startButton.setShortcut("Alt+3")
        self.startButton.clicked.connect(self.macro1)
        self.hook = keyboard.on_press(self.keyboardEventReceived)
    def seedClicked(self):
        seed, ok1 = QInputDialog.getText(self, "Change Seed", "<font face=\"Malgun Gothic\">Seed:</font>")

        if ok1 == True:
            print(seed)
            self.sText.setText("Seed: " + str(seed))

    def f3Clicked(self):
        if self.f3Box.isChecked() == False:
            self.f3Box.toggle()
    def keyboardEventReceived(self, event):
        if event.event_type == 'down':
            if event.name == 'f3':
                if self.f3Box.isChecked() == False:
                    self.f3Box.toggle()
    def reset(self):
        if self.f3Box.isChecked() == True:
            self.f3Box.toggle()


            

    #-------------------------------------------매크로--------------------- 


    def macro1(self):
        rtMin = self.rtMin.text()
        rtSec = self.rtSec.text()
        rtPoint = self.rtPoint.text()
        igtMin = self.igtMin.text()
        igtSec = self.igtSec.text()
        igtPoint = self.igtPoint.text()
        version = self.version.currentText()
        seedType = self.seedType.currentText()
        Mods = self.Mods.currentText()
        diffi = self.diffiBox.currentText()
        ytlink = self.ytLink.text()
        desc = self.sText.text()
        webbrowser.open("https://www.speedrun.com/mc")
        QtTest.QTest.qWait(2000)
        pag.moveTo(1300, 270)
        pag.click()
        QtTest.QTest.qWait(1500)
        pag.moveTo(990, 380)
        pag.click()
        pag.typewrite(rtMin)
        pag.moveTo(1070, 380)
        pag.click()
        pag.typewrite(rtSec)
        pag.moveTo(1150, 380)
        pag.click()
        pag.typewrite(rtPoint)
        pag.moveTo(990, 440)
        pag.click()
        pag.typewrite(igtMin)
        pag.moveTo(1070, 440)
        pag.click()
        pag.typewrite(igtSec)
        pag.moveTo(1150, 440)
        pag.click()
        pag.typewrite(igtPoint)
        pag.moveTo(1000, 500)
        pag.click()
        print(Mods)

        if version == "1.16.1":
            pag.moveTo(1000,536)
            pag.click()
        elif version == "1.14.4":
            pag.moveTo(1000,550)
            pag.click()
        elif version == "1.7.2":
            pag.moveTo(1000,568)
            pag.click()
        elif version == "1.7.10":
            pag.moveTo(1000,590)
            pag.click()
        elif version == "1.8.9":
            pag.moveTo(1000,604)
            pag.click()
        elif version == "1.6.4":
            pag.moveTo(1000,625)
            pag.click()

        pag.moveTo(1000,550)
        pag.click()

        if diffi == "Easy":
            pag.moveTo(1000,590)
            pag.click()
        elif diffi == "Normal":
            pag.moveTo(1000,607)
            pag.click()
        elif diffi == "Hard":
            pag.moveTo(1000,622)
            pag.click()
        elif diffi == "Hardcore":
            pag.moveTo(1000,642)
            pag.click()

        if seedType == "SSG":
            pag.moveTo(1000,600)
            pag.click()
            pag.moveTo(1000,625)
            pag.click()

        pag.moveTo(1000,650)
        pag.click()
        if version == "1.16.1":
            pag.moveTo(1000,710)
            pag.click()
        elif version == "1.14.4":
            pag.moveTo(1000,695)
            pag.click()
        else:
            pag.moveTo(1000,680)
            pag.click()
        if self.f3Box.isChecked() == False:
            pag.moveTo(1000,700)
            pag.click()
            pag.moveTo(1000,750)
            pag.click()

        pag.moveTo(1000,750)
        pag.click()

        if Mods == "Vanilla":
            pag.click()
        elif Mods == "Optifine":
            pag.moveTo(1000,800)
            pag.click()
        elif Mods == "CaffeineMC":
            pag.moveTo(1000,820)
            pag.click()

        pag.scroll(-1000)
        pag.moveTo(1000,490)
        pag.click()
        pag.typewrite(ytlink)
        pag.moveTo(1000,600)
        pag.click()
        pag.typewrite(desc)




app = QApplication(sys.argv)
main_dialog = MainDialog()
main_dialog.show()
app.exec_()


