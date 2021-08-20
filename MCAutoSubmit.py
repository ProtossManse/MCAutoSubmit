'''
MCAutoSubmit
Copyright © 2021 by ProtossManse (Discord: ProtossManse#3053)

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
'''

import sys
import os
import keyboard
from nbt.nbt import NBTFile
import getpass
import datetime
import requests
import json


from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5 import QtTest


APPVERSION = "v1.2.2"


username = getpass.getuser()
ghostmode = False
WOWSANS = QSettings(QSettings.NativeFormat, QSettings.UserScope, "MCAutoSubmit")

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
        self.linkButton.clicked.connect(self.test)
        self.hook = keyboard.on_press(self.keyboardEventReceived)
        self.pathLine.setText(WOWSANS.value("path", os.path.join("C:\\Users",username,"AppData\\Roaming\\.minecraft")))
        global path
        path = WOWSANS.value("path", os.path.join("C:\\Users",username,"AppData\\Roaming\\.minecraft"))
        global ghostmode
        if os.path.isdir(os.path.join(path,"ghostrunner\\ghosts")) == True:
            self.grm.setText("Ghost Runner Mode ON")
            ghostmode = True
        elif os.path.isdir(os.path.join(path,"ghostrunner\\ghosts")) == False:
            self.grm.setText("")
            ghostmode = False
        self.apiLine.setText(WOWSANS.value("api"))
        self.descriptionText.setPlainText(WOWSANS.value("desc", "Description (Manual)\nDon't enter the seed."))
        # self.descriptionText.selectAll()
        self.descriptionText.setAlignment(Qt.AlignCenter)
        self.seedType.setCurrentText(WOWSANS.value("seedType", "RSG"))
        self.auto_stop = False
        self.onlyInt = QIntValidator()
        self.igtHr.setValidator(self.onlyInt)
        self.igtMin.setValidator(self.onlyInt)
        self.igtSec.setValidator(self.onlyInt)
        self.igtPoint.setValidator(self.onlyInt)
        self.rtaHr.setValidator(self.onlyInt)
        self.rtMin.setValidator(self.onlyInt)
        self.rtSec.setValidator(self.onlyInt)
        self.rtPoint.setValidator(self.onlyInt)
        self.langBox.currentIndexChanged.connect(self.lang)
        self.creditLabel.mousePressEvent = self.credit
        self.statusBar().showMessage("MCAutoSubmit by ProtossManse")
        self.auto()

        if WOWSANS.value("lang") == "한국어":
            self.langBox.setCurrentText("한국어")
        else:
            self.langBox.setCurrentText("English")
        self.apiLabel.setOpenExternalLinks(True)

    def credit(self, event):
        QMessageBox.information(self, "Credits", f"Copyright © 2021 ProtossManse (Discord ProtossManse#3053)<br><br>MCAutoSubmit for FSG {APPVERSION} by ProtossManse.<br><br>Icon by ChobojaX.<br><br>Special Thanks to Haruww, Azura, Meera and Salix.<br><br>MCAutoSubmit is under the <a href='https://github.com/ProtossManse/Auto-Submit/blob/main/LICENSE.txt'>GNU General Public License v3.0.</a>")
        

    def seedClicked(self):
        if self.langBox.currentText() == "한국어":
            seed, ok1 = QInputDialog.getText(self, "시드 변경", "<font face=\"Malgun Gothic\">시드:</font>")
        else:
            seed, ok1 = QInputDialog.getText(self, "Change Seed", "<font face=\"Malgun Gothic\">Seed:</font>")

        if ok1 == True:
            if seed != "":
                global mc_seed
                mc_seed = str(seed)
        
    def keyboardEventReceived(self, event):
        if event.event_type == 'down':
            if event.name == 'f3':
                self.f3Box.setChecked(True)
            if event.name == 'esc':
                QtTest.QTest.qWait(350)
                self.auto()
        
    def browse(self):
        global path
        global ghostmode
        pathops = QFileDialog.Options()
        pathops |= QFileDialog.ShowDirsOnly
        if self.langBox.currentText() == "한국어":
            patht = QFileDialog.getExistingDirectory(self, '탐색...', path)
        else:
            patht = QFileDialog.getExistingDirectory(self, 'Browse...', path)
        if patht != "":
            path = patht.replace("/", "\\")
            self.pathLine.setText(str(path))
            WOWSANS.setValue("path", str(path))
        
        if os.path.isdir(os.path.join(path,"ghostrunner\\ghosts")) == True:
            self.grm.setText("Ghost Runner Mode ON")
            ghostmode = True
        elif os.path.isdir(os.path.join(path, "ghostrunner\\ghosts")) == False:
            self.grm.setText("")
            ghostmode = False


    def lang(self):
        
        if self.langBox.currentText() == "한국어":
            WOWSANS.setValue("lang", "한국어")
            self.seedButton.setText("시드 변경")
            self.label.setText("인 게임 타임:")
            self.label_2.setText("리얼 타임(수동):")
            self.label_7.setText("버전:")
            self.label_8.setText("난이도:")
            self.label_9.setText("모드:")
            self.creditLabel.setText("크레딧")
            self.label_13.setText("시드 타입:")
            self.label_10.setText("경로:")
            self.apiLabel.setText("<a href='https://www.speedrun.com/api/auth'>API 키 (URL):</a>")
            self.apiLabel.setOpenExternalLinks(True)
            self.pathButton.setText("탐색...")
            self.startButton.setText("제출")
            self.resetButton.setText("새로고침\n(Esc)")
            self.linkButton.setText("테스트...")
            if self.ytLink.text() == "Video Link(Manual)":
                self.ytLink.setText("동영상 링크 (수동)")
            if self.descriptionText.toPlainText() == "Description (Manual)\nDon't enter the seed.":
                self.descriptionText.setPlainText("설명 (수동)\n시드를 입력하지 마세요.")
                self.descriptionText.selectAll()
                self.descriptionText.setAlignment(Qt.AlignCenter)
        elif self.langBox.currentText() == "English":
            WOWSANS.setValue("lang", "english")
            self.seedButton.setText("Change Seed")
            self.label.setText("In-Game Time:")
            self.label_2.setText("Real Time(Manual):")
            self.label_7.setText("Version:")
            self.label_8.setText("Difficulty:")
            self.label_9.setText("Mods:")
            self.label_13.setText("Seed Type:")
            self.label_10.setText("Path:")
            self.apiLabel.setText("<a href='https://www.speedrun.com/api/auth'>API Key (URL):</a>")
            self.apiLabel.setOpenExternalLinks(True)
            self.creditLabel.setText("Credits")
            self.pathButton.setText("Browse...")
            self.linkButton.setText("Test...")
            self.startButton.setText("Submit")
            self.resetButton.setText("Refresh\n(Esc)")
            if self.ytLink.text() == "동영상 링크 (수동)":
                self.ytLink.setText("Video Link(Manual)")
            if self.descriptionText.toPlainText() == "설명 (수동)\n시드를 입력하지 마세요.":
                self.descriptionText.setPlainText("Description (Manual)\nDon't enter the seed.")
                self.descriptionText.selectAll()
                self.descriptionText.setAlignment(Qt.AlignCenter)
    

        



    def auto(self):

        self.resetButton.setDisabled(True)

        global ghostmode

        if os.path.isdir(os.path.join(path,"ghostrunner\\ghosts")) == True:
            self.grm.setText("Ghost Runner Mode ON")
            ghostmode = True
        elif os.path.isdir(os.path.join(path, "ghostrunner\\ghosts")) == False:
            self.grm.setText("")
            ghostmode = False

                
        mc_dir = path
        mc_world = os.path.join(mc_dir, "saves")
        try:
            wrm = sorted([os.path.join(mc_world, s) for s in os.listdir(mc_world)], key=os.path.getmtime, reverse=True)
            for w in wrm.copy()[:3]:
                try:
                    world = w
                    dat = NBTFile(os.path.join(world, "level.dat"))
                    ctime = os.path.getctime(world)
                    ctime = datetime.datetime.fromtimestamp(ctime)
                    if not int(str(dat["Data"]["Time"])):
                        continue
                    else:
                        break
                except:
                    continue

            try:            
                mc_isend = str(dat["Data"]["Player"]["seenCredits"])
                if mc_isend == "0":
                    mc_isend = False
                else:
                    mc_isend = True
            except:
                mc_isend = None
            mc_igt = str(dat["Data"]["Time"])
            mc_igt = int(mc_igt) - 1
            
                
            global mc_seed

            mc_diffi = str(dat["Data"]["Difficulty"])
            mc_hardcore = str(dat["Data"]["hardcore"])
            mc_seed = str(dat["Data"]["WorldGenSettings"]["seed"])
            mc_moded = str(dat["Data"]["WasModded"])

        
                

            global mc_sec
            if ghostmode == False:
                mc_sec = int(mc_igt) // 20
                
                
                                
                min = int(mc_sec) // 60
                hr = min // 60
                sec = int(mc_sec) % 60
                min = min % 60
                ms = mc_igt % 20 * 5
                
                if len(str(ms)) == 2:
                    ms = str(ms) + "0"
                elif len(str(ms)) == 1:
                    ms = str(ms) + "00"

                if mc_isend == False or mc_isend == None:
                    self.igtHr.setText(str(hr))
                    self.igtMin.setText(str(min))
                    self.igtSec.setText(str(sec))
                    self.igtPoint.setText(str(ms))
                    self.auto_stop = False
                elif mc_isend == True:
                    if self.auto_stop == False:
                        self.igtHr.setText(str(hr))
                        self.igtMin.setText(str(min))
                        self.igtSec.setText(str(sec))
                        self.igtPoint.setText(str(ms))
                        self.auto_stop = True
            elif ghostmode == True:
                ghostdir = os.path.join(path, "ghostrunner\\ghosts")
                grm = sorted([os.path.join(ghostdir, s) for s in os.listdir(ghostdir)], key=os.path.getmtime, reverse=True)
                for g in grm.copy()[:3]:
                    try:
                        ghost = g
                        gfile = os.path.join(ghost, "info.gri")
                        
                        if not gfile:
                            continue
                        else:
                            with open (gfile, "r") as tf:
                                lines = json.load(tf)
                                gtrta = int(lines["rta"])
                                gtigt = int(lines["igt"])

                            break
                    except:
                        continue
                gtsec = gtrta // 1000
                gtrtamin = gtsec // 60
                gtrtahur = gtrtamin // 60
                gtrtasec = gtsec % 60
                gtrtamis = gtrta % 1000
                gtrtamin = gtrtamin % 60

                gtsec = gtigt // 1000
                gtigtmin = gtsec // 60
                gtigthur = gtigtmin // 60
                gtigtsec = gtsec % 60
                gtigtmis = gtigt % 1000
                gtigtmin = gtigtmin % 60

                self.rtaHr.setText(str(gtrtahur))
                self.rtMin.setText(str(gtrtamin))
                self.rtSec.setText(str(gtrtasec))
                self.rtPoint.setText(str(gtrtamis))
                self.igtHr.setText(str(gtigthur))
                self.igtMin.setText(str(gtigtmin))
                self.igtSec.setText(str(gtigtsec))
                self.igtPoint.setText(str(gtigtmis))




            if mc_hardcore == "1":
                mc_diffi = "Hardcore"
                self.diffiBox.setCurrentText("Hardcore")
            elif mc_hardcore == "0":
                if mc_diffi == "1":
                    mc_diffi = "Easy"
                    self.diffiBox.setCurrentText("Easy")
                elif mc_diffi == "2":
                    mc_diffi = "Normal"
                    self.diffiBox.setCurrentText("Normal")
                elif mc_diffi == "3":
                    mc_diffi = "Hard"
                    self.diffiBox.setCurrentText("Hard")
            if mc_moded == "1":
                mc_moded = True
            elif mc_moded == "0":
                mc_moded = False
            
            


            if int(mc_igt) <= 10 or int(mc_igt) == None:
                self.f3Box.setChecked(False)


            if mc_moded == True:
                
                self.Mods.setCurrentText("Modded")

            elif mc_moded == False:
                self.Mods.setCurrentText("Vanilla")

        

        except:
            if self.langBox.currentText() == "한국어":
                QMessageBox.warning(self, "오류", "월드를 감지할 수 없음", QMessageBox.Ok)
            else:
                QMessageBox.warning(self, "ERROR", "No World Found", QMessageBox.Ok)
        self.resetButton.setEnabled(True)




    def test(self):
        WOWSANS.setValue("api", self.apiLine.text())
        self.linkButton.setDisabled(True)
        # QtTest.QTest.qWait(300)
        api_key = self.apiLine.text()
        res = requests.get('https://www.speedrun.com/api/v1/profile', headers={'X-API-Key': api_key})
        # QtTest.QTest.qWait(300)
        if str(res) == "<Response [403]>":
            if self.langBox.currentText() == "한국어":
                QMessageBox.warning(self, "오류", "유저를 찾을 수 없음", QMessageBox.Ok)
            else:
                QMessageBox.warning(self, "ERROR", "No User Found", QMessageBox.Ok)
        elif str(res) == "<Response [200]>":
            srcuser = res.json()["data"]["names"]["international"]
            global userid
            userid = res.json()["data"]["id"]
            if self.langBox.currentText() == "한국어":
                QMessageBox.information(self, "성공", f"유저를 확인했습니다. 반갑습니다 {srcuser}. (아이디: {userid})")
            else:
                QMessageBox.information(self, "Success", f"Found User. Hello {srcuser}. (id: {userid})")
        self.linkButton.setEnabled(True)

    def closeEvent(self, QCloseEvent):
        WOWSANS.setValue("desc", self.descriptionText.toPlainText())
        WOWSANS.setValue("seedType", self.seedType.currentText())
        WOWSANS.setValue("api", self.apiLine.text())
        
        


#-------------------------------------------Submit--------------------- 


    def macro1(self):



        if self.rtaHr.text() == "":
            self.rtaHr.setText("0")
        if self.rtMin.text() == "":
            self.rtMin.setText("0")
        if self.rtSec.text() == "":
            self.rtSec.setText("0")
        if self.rtPoint.text() == "":
            self.rtPoint.setText("0")

        

        rtHour = int(self.rtaHr.text())
        rtMin = int(self.rtMin.text())
        rtSec = int(self.rtSec.text())
        rtPoint = float(self.rtPoint.text())
        igtHr = int(self.igtHr.text())
        igtMin = int(self.igtMin.text())
        igtSec = int(self.igtSec.text())
        igtPoint = float(self.igtPoint.text())
        api_key = self.apiLine.text()
        seedType = self.seedType.currentText()
        version = self.version.currentText()

        mods = self.Mods.currentText()
        if mods == "Vanilla":
            modsapi = "klrnve21"
        elif mods == "Modded":
            modsapi = "5lmj45jl"
        diffi = self.diffiBox.currentText()
        if diffi == "Easy":
            diffiid = "21g22nnl"
        elif diffi == "Normal":
            diffiid = "jqzxxng1"
        elif diffi == "Hard":
            diffiid = "klryy3jq"
        elif diffi == "Hardcore":
            diffiid = "21d33k4q"
        
        if self.f3Box.isChecked() == True: # F3
            f3 = "81w5z0m1" 
        else: # No F3
            f3 = "zqorkv5q"
        
            versionKey = "21d7k251"
            versionRange = "81p8o6el"




        ytlink = self.ytLink.text()
        desc = self.descriptionText.toPlainText()
        WOWSANS.setValue("desc", desc)
        WOWSANS.setValue("seedType", seedType)

            

        if rtHour == 00 and rtMin == 00 and rtSec == 00 and rtPoint == 000:
            if self.langBox.currentText() == "한국어":
                QMessageBox.warning(self, "오류", "리얼타임을 입력하지 않음.")
            else:
                QMessageBox.warning(self, "ERROR", "Real Time isn't set")

        else:
            if self.descriptionText.toPlainText() == "설명 (수동)\n시드를 입력하지 마세요." or self.descriptionText.toPlainText() == "Description (Manual)\nDon't enter the seed.":
                if self.langBox.currentText() == "한국어":
                    QMessageBox.warning(self, "오류", "설명을 입력하지 않음. (공백 가능)")
                else:
                    QMessageBox.warning(self, "ERROR", "Description isn't set. (Blank Available)")
            else:
                datas = {
                    "category": "n2y9z41d",
                    "date": datetime.datetime.today().strftime("%Y-%m-%d"),
                    "platform": "8gej2n93",
                    "verified": False,
                    "times": {
                        "realtime": rtHour * 3600 + rtMin * 60 + rtSec + rtPoint / 1000,
                        "realtime_noloads": 0,
                        "ingame": igtHr * 3600 + igtMin * 60 + igtSec + igtPoint / 1000,
                    },
                    "emulated": False,
                    "video": ytlink,
                    "comment": f"Seed: {mc_seed}\r\n{desc}\r\n\r\nSubmitted using MCAutoSubmit {APPVERSION}",
                    "variables": {
                        "ylpm5erl": { # Version
                            "type": "pre-defined",
                            "value": versionRange
                        },
                        "j846z5wl": { # Sub version
                            "type": "pre-defined",
                            "value": versionKey
                        },
                        "0nwkeorn": { # Difficulty
                            "type": "pre-defined",
                            "value": diffiid
                        },
                        "ylqkjo3l": { # F3
                            "type": "pre-defined",
                            "value": f3
                        },
                        "jlzwkmql": { # Mods
                            "type": "pre-defined",
                            "value": modsapi
                        },
                        "jlzrovq8": { # Version (Filtered Seed Glitchless)
                            "type": "pre-defined",
                            "value": "mlnp8rd1"
                        },
                        "ql61eov8": { # Player Count
                            "type": "pre-defined",
                            "value": "81pvroe1"
                        }
                    }
                }





                self.startButton.setDisabled(True)
                QtTest.QTest.qWait(150)
                r = requests.post('https://www.speedrun.com/api/v1/runs', json={'run': datas}, headers={'X-API-Key': api_key})
                QtTest.QTest.qWait(150)
                if r.status_code == 201:
                    if self.langBox.currentText() == "한국어":
                        QMessageBox.information(self,"MCAutoSubmit", "등록이 완료되었습니다. ")
                    else:
                        QMessageBox.information(self,"MCAutoSubmit", "Submit Finished.")
                else:
                    try:
                        if self.langBox.currentText() == "한국어":
                            QMessageBox.warning(self,"오류", str(r.json()['errors']))
                        else:
                            QMessageBox.warning(self,"ERROR", str(r.json()['errors']))
                    except:
                        if self.langBox.currentText() == "한국어":
                            QMessageBox.warning(self, "오류", "알 수 없는 오류")
                        else:
                            QMessageBox.warning(self, "ERROR", "Unknown ERROR")

                self.startButton.setEnabled(True)


        
        

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_dialog = MainDialog()
    main_dialog.show()
    app.exec_()


# sPaGhEtTi cOdE lol