from PyQt5 import QtWidgets
import pyautogui as pag
import sys
import os
import keyboard
from nbt.nbt import NBTFile
import getpass
import datetime

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
ico = resource_path("MCAutoSubmit2.png")

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
        QMessageBox.information(self, "Credits", "MCAutoSubmit by ProtossManse with Haru.\n\nIcon by ChobojaX.")
        self.statusBar().showMessage("MCAutoSubmit by ProtossManse with Haru")
        self.auto_stop = False
        self.langBox.currentIndexChanged.connect(self.lang)




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
            if self.textEdit.toPlainText() == "Description (Manual)\nDo not enter the seed.":
                self.textEdit.setText("<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">p, li { white-space: pre-wrap; }</style></head><body style=\" font-family:\'맑은 고딕\'; font-size:9pt; font-weight:400; font-style:normal;\"><p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">설명 (수동)</p><p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">시드를 입력하지 마세요.</p></body></html>")
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

            worlds_recently_modified = sorted([os.path.join(mc_saves, s) for s in os.listdir(mc_saves)], key=os.path.getmtime, reverse=True)
            for w in worlds_recently_modified.copy()[:3]:
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
        rtMin = self.rtMin.text()
        # rtSec = self.rtSec.text()
        # rtPoint = self.rtPoint.text()
        # igtHr = self.igtHr.text()
        # igtMin = self.igtMin.text()
        # igtSec = self.igtSec.text()
        # igtPoint = self.igtPoint.text()
        # version = self.version.currentText()
        # seedType = self.seedType.currentText()
        # Mods = self.Mods.currentText()
        # diffi = self.diffiBox.currentText()
        # ytlink = self.ytLink.text()
        # desc = self.sText.text()


        # webbrowser.open("https://www.speedrun.com/mc")
        # QtTest.QTest.qWait(4000)
        # pag.click(submitbtn)z
        # pag.moveTo(1300, 270)
        # pag.click()
        # QtTest.QTest.qWait(1500)
        # pag.moveTo(990, 380)
        # pag.click()
        # pag.typewrite(rtMin)
        # pag.moveTo(1070, 380)
        # pag.click()
        # pag.typewrite(rtSec)
        # pag.moveTo(1150, 380)
        # pag.click()
        # pag.typewrite(rtPoint)
        # pag.moveTo(990, 440)
        # pag.click()
        # pag.typewrite(igtMin)
        # pag.moveTo(1070, 440)
        # pag.click()
        # pag.typewrite(igtSec)
        # pag.moveTo(1150, 440)
        # pag.click()
        # pag.typewrite(igtPoint)
        # pag.moveTo(1000, 500)
        # pag.click()

        # if version == "1.16.1":
        #     pag.moveTo(1000,536)
        #     pag.click()
        # elif version == "1.14.4":
        #     pag.moveTo(1000,550)
        #     pag.click()
        # elif version == "1.7.2":
        #     pag.moveTo(1000,568)
        #     pag.click()
        # elif version == "1.7.10":
        #     pag.moveTo(1000,590)
        #     pag.click()
        # elif version == "1.8.9":
        #     pag.moveTo(1000,604)
        #     pag.click()
        # elif version == "1.6.4":
        #     pag.moveTo(1000,625)
        #     pag.click()

        # pag.moveTo(1000,550)
        # pag.click()

        # if diffi == "Easy":
        #     pag.moveTo(1000,590)
        #     pag.click()
        # elif diffi == "Normal":
        #     pag.moveTo(1000,607)
        #     pag.click()
        # elif diffi == "Hard":
        #     pag.moveTo(1000,622)
        #     pag.click()
        # elif diffi == "Hardcore":
        #     pag.moveTo(1000,642)
        #     pag.click()

        # if seedType == "SSG":
        #     pag.moveTo(1000,600)
        #     pag.click()
        #     pag.moveTo(1000,625)
        #     pag.click()

        # pag.moveTo(1000,650)
        # pag.click()
        # if version == "1.16.1":
        #     pag.moveTo(1000,710)
        #     pag.click()
        # elif version == "1.14.4" or "1.15.2":
        #     pag.moveTo(1000,695)
        #     pag.click()
        # else:
        #     pag.moveTo(1000,680)
        #     pag.click()
        # if self.f3Box.isChecked() == False:
        #     pag.moveTo(1000,700)
        #     pag.click()
        #     pag.moveTo(1000,750)
        #     pag.click()

        # pag.moveTo(1000,750)
        # pag.click()

        # if Mods == "Vanilla":
        #     pag.click()
        # elif Mods == "Optifine":
        #     pag.moveTo(1000,800)
        #     pag.click()
        # elif Mods == "CaffeineMC":
        #     pag.moveTo(1000,820)
        #     pag.click()

        # pag.scroll(-1000)
        # pag.moveTo(1000,490)
        # pag.click()
        # pag.typewrite(ytlink)
        # pag.moveTo(1000,600)
        # pag.click()
        # pag.typewrite(desc)



if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_dialog = MainDialog()
    main_dialog.show()
    app.exec_()


