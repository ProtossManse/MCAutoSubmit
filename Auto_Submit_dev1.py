from PyQt5 import QtWidgets
import pyautogui as pag
import sys
import os
import keyboard
import webbrowser
import srcomapi, srcomapi.datatypes as dt
from nbt.nbt import NBTFile
import getpass

import PyQt5
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5 import QtTest

username = getpass.getuser()
userpath = os.path.join("C:\\Users",username,"AppData\\Roaming")
path = userpath




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
        self.pathButton.clicked.connect(self.browse)
        self.hook = keyboard.on_press(self.keyboardEventReceived)
        self.pathLine.setText(userpath +"/.minecraft")
        dat = NBTFile(os.path.join(path, ".minecraft\\saves\\새로운 세계 (26)\\level.dat"))

        mc_version = str(dat["Data"]["Version"]["Name"])
        mc_diffi = str(dat["Data"]["Difficulty"])
        mc_hardcore = str(dat["Data"]["hardcore"])
        mc_igt = str(dat["Data"]["DayTime"])
        mc_seed = str(dat["Data"]["WorldGenSettings"]["seed"])

        if mc_hardcore == "1":
            mc_diffi = "Hardcore"
        elif mc_hardcore == "0":
            if mc_diffi == "1":
                mc_diffi = "Easy"
            elif mc_diffi == "2":
                mc_diffi = "Normal"
            elif mc_diffi == "3":
                mc_diffi = "Hard"
        

        print(f"{str(mc_version)}\n{str(mc_diffi)}\n{mc_igt} ticks\n{int(mc_igt)/20} secs\nSeed: {mc_seed}")
    def seedClicked(self):
        seed, ok1 = QInputDialog.getText(self, "Change Seed", "<font face=\"Malgun Gothic\">Seed:</font>")

        if ok1 == True:
            if seed != "":
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

    def browse(self):
        global path
        pathops = QFileDialog.Options()
        pathops |= QFileDialog.ShowDirsOnly
        path = QtWidgets.QFileDialog.getExistingDirectory(self, 'Browse...', userpath)
        if path != "":
            self.pathLine.setText(str(path))
#--------------------------

    # def get_last_played_level():
    #     mc_dir = path
    #     mc_saves = os.path.join(mc_dir, "saves")

    #     worlds_recently_modified = sorted([os.path.join(mc_saves, s) for s in os.listdir(mc_saves)], key=os.path.getmtime, reverse=True)
    #     for w in worlds_recently_modified.copy()[:3]:
    #         try:
    #             world = w
    #             level = NBTFile(os.path.join(world, "level.dat"))
    #             if not int(str(level["Data"]["Time"])):
    #                 continue
    #             else:
    #                 break
    #         except:
    #             continue
    #     except: #* If it's pre 1.7.2
    #         stats = None

    #     try:
    #         seen_credits = bool(int(str(level["Data"]["Player"]["seenCredits"])))
    #     except: #* If it's pre 1.12 OR a server
    #         seen_credits = None

    #     try:
    #         data = {
    #             "name": str(level["Data"]["LevelName"]),
    #             "version": str(level["Data"]["Version"]["Name"]),
    #             "igt": stats["stat.playOneMinute"] if int(str(level["Data"]["DataVersion"])) < 1451 else stats["stats"]["minecraft:custom"]["minecraft:play_one_minute"],
    #             "seen_credits": seen_credits,
    #             "pre17": False
    #         }
    #     except: #* If it's pre 1.9
    #         try:
    #             data = {
    #                 "name": str(level["Data"]["LevelName"]),
    #                 "version": "Pre 1.9",
    #                 "igt": stats["stat.playOneMinute"],
    #                 "seen_credits": seen_credits,
    #                 "pre17": False
    #             }
    #         except: #* If it's pre 1.7.2
    #             data = {
    #                 "name": str(level["Data"]["LevelName"]),
    #                 "version": "Pre 1.7.2",
    #                 "igt": utils.get_pre17_igt(mc_dir),
    #                 "seen_credits": seen_credits,
    #                 "pre17": True
    #             }

    #     return data

            

#-------------------------------------------macro--------------------- 


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
        elif version == "1.14.4" or "1.15.2":
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


