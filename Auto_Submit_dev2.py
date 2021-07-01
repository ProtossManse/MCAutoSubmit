from PyQt5 import QtWidgets
from numpy import concatenate
import pyautogui as pag
import sys
import os
import keyboard
from nbt.nbt import NBTFile
import getpass
import datetime
import webbrowser

from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5 import QtTest

username = getpass.getuser()
path = os.path.join("C:\\Users",username,"AppData\\Roaming\\.minecraft")




def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
        print(base_path)
    except Exception:
        base_path = os.path.abspath(".")
        


    return os.path.join(base_path, relative_path)


macUI = resource_path("autosubmit.ui")
macUI = str(macUI)
ico = resource_path("MCAutoSubmit.png")

Ui_MainWindow = uic.loadUiType(macUI)[0]




    
 
class MainDialog(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowIcon(QIcon(ico))

        self.seedButton.clicked.connect(self.seedClicked)
        self.resetButton.clicked.connect(self.auto)
        self.startButton.clicked.connect(self.macro1)
        self.pathButton.clicked.connect(self.browse)
        self.hook = keyboard.on_press(self.keyboardEventReceived)
        self.pathLine.setText(path)
        self.auto_stop = False
        self.langBox.currentIndexChanged.connect(self.lang)
        self.creditLabel.mousePressEvent = self.credit
        self.statusBar().showMessage("MCAutoSubmit by ProtossManse with Haru")

    def credit(self, event):
        QMessageBox.information(self, "Credits", "MCAutoSubmit by ProtossManse with Haru.\n\nIcon by ChobojaX.")
        

    def seedClicked(self):
        seed, ok1 = QInputDialog.getText(self, "Change Seed", "<font face=\"Malgun Gothic\">Seed:</font>")

        if ok1 == True:
            if seed != "":
                self.sText.setText("Seed: " + str(seed))
        
    def keyboardEventReceived(self, event):
        if event.event_type == 'down':
            if event.name == 'f3':
                self.f3Box.setChecked(True)
            if event.name == 'esc':
                QtTest.QTest.qWait(350)
                self.auto()
        
    def browse(self):
        global path
        pathops = QFileDialog.Options()
        pathops |= QFileDialog.ShowDirsOnly
        path = QtWidgets.QFileDialog.getExistingDirectory(self, 'Browse...', path)
        if path != "":
            self.pathLine.setText(str(path))

    def lang(self):
        
        if self.langBox.currentText() == "한국어":
            self.seedButton.setText("시드 변경")
            self.label_2.setText("Real Time (수동):")
            self.label_7.setText("버전:")
            self.label_8.setText("난이도:")
            self.label_9.setText("모드:")
            self.label_13.setText("시드 타입:")
            self.label_10.setText("경로:")
            self.pathButton.setText("찾기...")
            self.label_14.setText("<html><head/><body><p align=\"center\"><span style=\" font-size:11pt; font-weight:600; color:#ff0000;\">1.16.1 전용</span></p></body></html>")
            self.startButton.setText("제출")
            self.resetButton.setText("새로고침\n(Esc)")
            if self.ytLink.text() == "Video Link(Manual)":
                self.ytLink.setText("동영상 링크 (수동)")
            if self.descriptionText.toPlainText() == "Description (Manual)\nDo not enter the seed.":
                self.descriptionText.setText("<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">p, li { white-space: pre-wrap; }</style></head><body style=\" font-family:\'맑은 고딕\'; font-size:9pt; font-weight:400; font-style:normal;\"><p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">설명 (수동)</p><p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">시드를 입력하지 마세요.</p></body></html>")
        elif self.langBox.currentText() == "English":
            self.seedButton.setText("Change Seed")
            self.label_2.setText("Real Time(Manual):")
            self.label_7.setText("Version:")
            self.label_8.setText("Difficulty:")
            self.label_9.setText("Mods:")
            self.label_13.setText("Seed Type:")
            self.label_10.setText("Path:")
            self.pathButton.setText("Browse...")
            self.label_14.setText("<html><head/><body><p align=\"center\"><span style=\" font-size:11pt; font-weight:600; color:#ff0000;\">Only 1.16.1</span></p></body></html>")
            self.startButton.setText("Submit")
            self.resetButton.setText("Refresh\n(Esc)")
            if self.ytLink.text() == "동영상 링크 (수동)":
                self.ytLink.setText("Video Link(Manual)")
            if self.textEdit.toPlainText() == "설명 (수동)\n시드를 입력하지 마세요.":
                self.textEdit.setText("<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">p, li { white-space: pre-wrap; }</style></head><body style=\" font-family:\'맑은 고딕\'; font-size:9pt; font-weight:400; font-style:normal;\"><p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Description (Manual)</p><p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Do not enter the seed.</p></body></html>")
            


    def auto(self):
        try:
            mc_dir = path
            mc_saves = os.path.join(mc_dir, "saves")

            wrm = sorted([os.path.join(mc_saves, s) for s in os.listdir(mc_saves)], key=os.path.getmtime, reverse=True)
            for w in wrm.copy()[:3]:
                world = w
                dat = NBTFile(os.path.join(world, "level.dat"))
                ctime = os.path.getctime(world)
                ctime = datetime.datetime.fromtimestamp(ctime)
                if not int(str(dat["Data"]["Time"])):
                    continue
                else:
                    break
            
            mc_version = str(dat["Data"]["Version"]["Name"])
            mc_diffi = str(dat["Data"]["Difficulty"])
            mc_hardcore = str(dat["Data"]["hardcore"])
            mc_igt = str(dat["Data"]["Time"])
            mc_igt = int(mc_igt) - 1
            mc_seed = str(dat["Data"]["WorldGenSettings"]["seed"])
            mc_moded = str(dat["Data"]["WasModded"])
            mc_sec = int(mc_igt) / 20
            mc_isend = str(dat["Data"]["Player"]["seenCredits"])
            if mc_version == "1.16.1":
                self.version.setCurrentText("1.16.1")
            else:
                self.version.setCurrentText("Other")
            

            dot = str(mc_sec)
            dot = dot.index(".")
            intsec = str(mc_sec)[:int(dot)]
            min = int(intsec) // 60
            hr = min // 60
            sec = int(intsec) % 60
            min = min % 60
            ms = str(mc_sec)[int(dot) + 1:]
            if len(ms) == 2:
                ms = ms + "0"
            elif len(ms) == 1:
                ms = ms + "00"

            self.sText.setText("Seed: " + mc_seed)
            if mc_hardcore == "1":
                mc_diffi = "Hardcore"
            elif mc_hardcore == "0":
                if mc_diffi == "1":
                    mc_diffi = "Easy"
                elif mc_diffi == "2":
                    mc_diffi = "Normal"
                elif mc_diffi == "3":
                    mc_diffi = "Hard"
            if mc_moded == "1":
                mc_moded = True
            elif mc_moded == "0":
                mc_moded = False
            
            if mc_isend == "0":
                    self.igtHr.setText(str(hr))
                    self.igtMin.setText(str(min))
                    self.igtSec.setText(str(sec))
                    self.igtPoint.setText(ms)
                    self.auto_stop = False
            elif mc_isend == "1":
                if self.auto_stop == False:
                    self.igtHr.setText(str(hr))
                    self.igtMin.setText(str(min))
                    self.igtSec.setText(str(sec))
                    self.igtPoint.setText(ms)
                    self.auto_stop = True

                

            print(f"\n{str(mc_version)}\n{str(mc_diffi)}\n{mc_igt} ticks\n{str(hr)}hour {str(min)} min {sec} secs {ms} ms\nSeed: {mc_seed}\nModded: {mc_moded}\nCtime: {str(ctime)}\n{mc_isend}")
            if mc_diffi == "Easy":
                self.diffiBox.setCurrentText("Easy")
            elif mc_diffi == "Normal":
                self.diffiBox.setCurrentText("Normal")
            elif mc_diffi == "Hard":
                self.diffiBox.setCurrentText("Hard")
            elif mc_diffi == "Hardcore":
                self.diffiBox.setCurrentText("Hardcore")

            if mc_moded == True:
                self.Mods.setCurrentText("CaffeineMC")
            elif mc_moded == False:
                self.Mods.setCurrentText("Vanilla")
        except:
            QMessageBox.warning(self, "ERROR", "No World Found", QMessageBox.Ok)

        


#-------------------------------------------macro--------------------- 


    def macro1(self):

        rtHour = self.rtaHr.text()
        rtMin = self.rtMin.text()
        rtSec = self.rtSec.text()
        rtPoint = self.rtPoint.text()
        igtHr = self.igtHr.text()
        igtMin = self.igtMin.text()
        igtSec = self.igtSec.text()
        igtPoint = self.igtPoint.text()
        seedType = self.seedType.currentText()
        mods = self.Mods.currentText()
        diffi = self.diffiBox.currentText()
        ytlink = self.ytLink.text()
        seed = self.sText.text()
        desc = self.descriptionText.toPlainText()

        webbrowser.open("https://www.speedrun.com/mc")
        QtTest.QTest.qWait(1000)
        submit = pag.locateCenterOnScreen(resource_path('submit.png'), confidence=0.7)
        while submit == None:
            QtTest.QTest.qWait(1000)
            submit = pag.locateCenterOnScreen(resource_path('submit.png'), confidence=0.7)
        pag.click(submit)
        QtTest.QTest.qWait(500)
        rtm = pag.locateCenterOnScreen(resource_path('RT.png'), confidence=0.7)
        while rtm == None:
            QtTest.QTest.qWait(1000)
            rtm = pag.locateCenterOnScreen(resource_path('RT.png'), confidence=0.7)
        if rtm != None:
            pag.moveTo(rtm)
            pag.moveRel(80, 0)
            pag.click()
            pag.typewrite(rtHour)
            pag.moveRel(80, 0)
            pag.click()
            pag.typewrite(rtMin)
            pag.moveRel(80, 0)
            pag.click()
            pag.typewrite(rtSec)
            pag.moveRel(80, 0)
            pag.click()
            pag.typewrite(rtPoint)
        igtm = pag.locateCenterOnScreen(resource_path('IGT.png'), confidence=0.7)
        if igtm != None:
            pag.moveTo(igtm)
            pag.moveRel(80, 0)
            pag.click()
            pag.typewrite(igtHr)
            pag.moveRel(80, 0)
            pag.click()
            pag.typewrite(igtMin)
            pag.moveRel(80, 0)
            pag.click()
            pag.typewrite(igtSec)
            pag.moveRel(80, 0)
            pag.click()
            pag.typewrite(igtPoint)
        macrovar = pag.locateCenterOnScreen(resource_path('version.png'), confidence=0.7)
        if macrovar != None:
            pag.moveTo(macrovar)
            pag.moveRel(300,0)
            pag.click()
        macrovar = pag.locateCenterOnScreen(resource_path('1_16_1.png'), confidence=0.7)
        if macrovar != None:
            pag.click(macrovar)
        macrovar = pag.locateCenterOnScreen(resource_path('difficulty.png'), confidence=0.7)
        if macrovar != None:
            pag.moveTo(macrovar)
            pag.moveRel(280, 0)
            pag.click()
        if diffi == "Easy":
            diffimac = pag.locateCenterOnScreen(resource_path('easy.png'),confidence=0.7)
            pag.click(diffimac)
        elif diffi == "Normal":
            diffimac = pag.locateCenterOnScreen(resource_path('normal.png'),confidence=0.7)
            pag.click(diffimac)
        elif diffi == "Hard":
            diffimac = pag.locateCenterOnScreen(resource_path('hard.png'),confidence=0.7)
            pag.click(diffimac)
        elif diffi == "Hardcore":
            diffimac = pag.locateCenterOnScreen(resource_path('normal.png'),confidence=0.7)
            pag.click(diffimac)

        if seedType == "SSG":
            macrovar = pag.locateCenterOnScreen(resource_path('seed_type.png'), confidence=0.7)
            if macrovar != None:
                pag.moveTo(macrovar)
                pag.moveRel(280,0)
                pag.click()
                macrovar = pag.locateCenterOnScreen(resource_path('ssg.png'), confidence=0.7)
                pag.click(macrovar)
        if self.f3Box.isChecked() == False:
            macrovar = pag.locateCenterOnScreen(resource_path('f3_1.png'), confidence=0.7)
            pag.click(macrovar)
            macrovar = pag.locateCenterOnScreen(resource_path('f3_2.png'), confidence=0.7)
            pag.click(macrovar)

        if mods == "CaffeineMC":
            macrovar = pag.locateCenterOnScreen(resource_path('mods.png'), confidence=0.7)
            pag.click(macrovar)
            macrovar = pag.locateCenterOnScreen(resource_path('caffeine.png'), confidence=0.7)
            pag.click(macrovar)

        pag.scroll(-300)
        QtTest.QTest.qWait(500)
        macrovar = pag.locateCenterOnScreen(resource_path('video.png'), confidence=0.7)
        pag.click(macrovar)
        pag.typewrite(ytlink)
        macrovar = pag.locateCenterOnScreen(resource_path('desc.png'), confidence=0.7)
        pag.click(macrovar)
        pag.typewrite(seed+"\n")
        pag.typewrite(desc)

        
        





if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_dialog = MainDialog()
    main_dialog.show()
    app.exec_()


