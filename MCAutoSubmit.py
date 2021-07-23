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

from PyQt5 import QtWidgets
import sys
import os
import keyboard
from nbt.nbt import NBTFile
import getpass
import datetime
import requests


from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5 import QtTest

username = getpass.getuser()
path = os.path.join("C:\\Users",username,"AppData\\Roaming\\.minecraft")
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
        self.pathLine.setText(WOWSANS.value("path", path))
        self.apiLine.setText(WOWSANS.value("api"))
        self.descriptionText.setPlainText(WOWSANS.value("desc", "Description (Manual)\nDon't enter the seed."))
        self.descriptionText.selectAll()
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
        self.statusBar().showMessage("MCAutoSubmit by ProtossManse with Haru")
        self.auto()

        if WOWSANS.value("lang") == "한국어":
            self.langBox.setCurrentText("한국어")
        else:
            self.langBox.setCurrentText("English")

        self.apiLabel.setOpenExternalLinks(True)

    def credit(self, event):
        QMessageBox.information(self, "Credits", "Copyright © 2021 ProtossManse (Discord ProtossManse#3053)<br><br>MCAutoSubmit v1.1.1 by ProtossManse with Haru.<br><br>Icon by ChobojaX.<br><br>MCAutoSubmit is under the <a href='https://github.com/ProtossManse/Auto-Submit/blob/main/LICENSE.txt'>GNU General Public License v3.0.</a>")
        

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
        pathops = QFileDialog.Options()
        pathops |= QFileDialog.ShowDirsOnly
        if self.langBox.currentText() == "한국어":
            patht = QtWidgets.QFileDialog.getExistingDirectory(self, '검색...', path)
        else:
            patht = QtWidgets.QFileDialog.getExistingDirectory(self, 'Browse...', path)
        if patht != "":
            path = patht.replace("/", "\\")
            self.pathLine.setText(str(path))
            WOWSANS.setValue("path", str(path))


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
            self.pathButton.setText("검색...")
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
            try:
                mc_version = str(dat["Data"]["Version"]["Name"])
                global minor
                if mc_version == "1.7.10":
                    minor = mc_version[:-3]
                else:
                    minor = mc_version[:-2]
                    print(minor)
                
                global mc_seed

                if minor == "1.16" or minor == "1.17":
                    self.version.setCurrentText(mc_version)
                    mc_diffi = str(dat["Data"]["Difficulty"])
                    mc_hardcore = str(dat["Data"]["hardcore"])
                    mc_seed = str(dat["Data"]["WorldGenSettings"]["seed"])
                    mc_moded = str(dat["Data"]["WasModded"])
                elif minor == "1.15":
                    self.version.setCurrentText(mc_version)
                    mc_diffi = str(dat["Data"]["Difficulty"])
                    mc_hardcore = str(dat["Data"]["hardcore"])
                    mc_seed = str(dat["Data"]["RandomSeed"])
                    mc_moded = str(dat["Data"]["WasModded"])
                elif minor == "1.14":
                    self.version.setCurrentText(mc_version)
                    mc_diffi = str(dat["Data"]["Difficulty"])
                    mc_hardcore = str(dat["Data"]["hardcore"])
                    mc_seed = str(dat["Data"]["RandomSeed"])
                    mc_moded = None                
            except: 
                try: # 1.8
                    self.version.setCurrentText("Unknown")
                    mc_diffi = str(dat["Data"]["Difficulty"])
                    mc_hardcore = str(dat["Data"]["hardcore"])
                    mc_seed = str(dat["Data"]["RandomSeed"])
                    mc_moded = None
                except: #pre 1.8
                    self.version.setCurrentText("Unknown")
                    mc_diffi = None
                    mc_hardcore = str(dat["Data"]["hardcore"])
                    mc_seed = str(dat["Data"]["RandomSeed"])
                    mc_moded = None

                

            global mc_sec
            mc_sec = int(mc_igt) / 20
            

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
                elif mc_diffi == None:
                    self.diffiBox.setCurrentText("Unknown")
            if mc_moded == "1":
                mc_moded = True
            elif mc_moded == "0":
                mc_moded = False
            
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

                


            if mc_moded == True:
                if minor == "1.16":
                    self.Mods.setCurrentText("Modded")
                else:
                    self.Mods.setCurrentText("Optifine")
            elif mc_moded == False:
                self.Mods.setCurrentText("Vanilla")
            elif mc_moded == None:
                self.Mods.setCurrentText("Unknown")
        
        except:
            if self.langBox.currentText() == "한국어":
                QMessageBox.warning(self, "오류", "월드를 감지할 수 없음", QMessageBox.Ok)
            else:
                QMessageBox.warning(self, "ERROR", "No World Found", QMessageBox.Ok)



    def test(self):
        WOWSANS.setValue("api", self.apiLine.text())
        self.linkButton.setDisabled(True)
        QtTest.QTest.qWait(300)
        api_key = self.apiLine.text()
        res = requests.get('https://www.speedrun.com/api/v1/profile', headers={'X-API-Key': api_key})
        QtTest.QTest.qWait(300)
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
        rtHour = int(self.rtaHr.text())
        rtMin = int(self.rtMin.text())
        rtSec = int(self.rtSec.text())
        rtPoint = float(self.rtPoint.text())
        api_key = self.apiLine.text()
        seedType = self.seedType.currentText()
        version = self.version.currentText()

        vdict = {
				"mln68v0q": "1.16.1",
				"gq7rrnnl": "1.14.4",
				"jq6vwj1m": "1.7.2",
				"013xkx15": "1.7.10",
				"4lx5gk41": "1.8.9",
				"9qj2o314": "1.6.4",
				"rqvx06l6": "1.0",
				"5len0klo": "1.1",
				"0q54m2lp": "1.2.1",
				"4lxgk4q2": "1.2.2",
				"81496vqd": "1.2.3",
				"z19xv814": "1.2.4",
				"p129k4lx": "1.2.5",
				"81pez8l7": "1.3.1",
				"xqko3k19": "1.3.2",
				"gq72od1p": "1.4.2",
				"21g968qz": "1.4.4",
				"jqzgw8lp": "1.4.5",
				"klrxdmlp": "1.4.6",
				"21d6n5qe": "1.4.7",
				"5q8433ld": "1.5.1",
				"4qy7m2q7": "1.5.2",
				"mlne7jlp": "1.6.1",
				"8106y21v": "1.6.2",
				"21d43441": "1.7.3",
				"5lm2emqv": "1.7.4",
				"81w72vq4": "1.7.5",
				"814o96vq": "1.7.6",
				"z192xv8q": "1.7.7",
				"p12v9k4q": "1.7.8",
				"zqojex1y": "1.7.9",
				"rqvx26l6": "1.8",
				"5lenyklo": "1.8.1",
				"21dv7g1e": "1.8.2",
				"5q8276qd": "1.8.3",
				"5le86mlo": "1.8.4",
				"01340kl5": "1.8.5",
				"rqvz7516": "1.8.6",
				"5levop1o": "1.8.7",
				"gq7zyr1p": "1.8.8",
				"81pyez81": "1.9",
				"xqkeo3kq": "1.9.1",
				"gq752od1": "1.9.2",
				"21gn968l": "1.9.3",
				"jqzngw8q": "1.9.4",
				"klr3xdml": "1.10",
				"5lmygj8l": "1.10.1",
				"jq678gv1": "1.10.2",
				"0q54o3nl": "1.11",
				"zqo0rw5q": "1.11.1",
				"4lxgvw4q": "1.11.2",
				"xqkonxn1": "1.12",
				"5q8270kq": "1.12.1",
				"p12ongvl": "1.12.2",
				"8142pg0l": "1.13",
				"z19rz201": "1.13.1",
				"z19ryv41": "1.13.2",
				"9qj49koq": "1.14",
				"01305er1": "1.14.1",
				"814vn2v1": "1.14.2",
				"jqzx69m1": "1.14.3",
				"gq7zrdd1": "1.15",
				"21dor7gq": "1.15.1",
				"21go7k8q": "1.15.2",
				"mln64j6q": "1.16",
				"21d7zo31": "1.16.2",
				"21d7evp1": "1.16.3",
				"21dgwkj1": "1.16.4",
				"21dzz0jl": "1.16.5",
				"5q8ojzr1": "1.17",
				"4qy93w3l": "1.17.1"
			}
        vdict = {v:k for k,v in vdict.items()}

        if seedType == "SSG":
            seedTypeKey = "klrzpjo1"
        elif seedType == "RSG":
            seedTypeKey = "21d4zvp1"
        mods = self.Mods.currentText()
        if mods == "Vanilla":
            modsapi = "21gyvwm1"
        elif mods == "Modded":
            modsapi = "jq6kxd3l"
        elif mods == "Optifine":
            modsapi = "jqzk8rmq"
        diffi = self.diffiBox.currentText()
        if diffi == "Easy":
            diffiid = "4lxg24q2"
        elif diffi == "Normal":
            diffiid = "8149mvqd"
        elif diffi == "Hard":
            diffiid = "z19xe814"
        elif diffi == "Hardcore":
            diffiid = "p129j4lx"
        
        if self.f3Box.isChecked() == True:
            f3 = "rqvmvz6q"
        else:
            f3 = "5lee2vkl"
        
        if minor == "1.16" or minor == "1.17":
            versionKey = vdict[version]
            versionRange = "4qye4731"
        elif minor == "1.15" or minor == "1.14" or minor == "1.13" or minor == "1.12" or minor == "1.11" or minor == "1.10" or minor == "1.9":
            versionKey = vdict[version]
            versionRange = "21go6e6q"
        else:
            versionKey = vdict[version]
            versionRange = "gq7zo9p1"




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
                if diffi == "Unknown" or mods == "Unknown" or version == "Unknown":
                    if self.langBox.currentText() == "한국어":
                        QMessageBox.warning(self, "오류", "난이도 혹은 모드 혹은 버전 정보를 입력하지 않음.")
                    else:
                        QMessageBox.warning(self, "ERROR", "Difficulty or Mods or Version isn't set.")
                else:
                    datas = {
                    "category": "mkeyl926",
                    "date": datetime.datetime.today().strftime("%Y-%m-%d"),
                    "platform": "8gej2n93",
                    "verified": False,
                    "times": {
                    "realtime": rtHour * 3600 + rtMin * 60 + rtSec + rtPoint / 1000,
                    "realtime_noloads": 0,
                    "ingame": float(mc_sec)
                    },
                    "emulated": False,
                    "video": ytlink,
                    "comment": f"{mc_seed}\r\n{desc}\r\n\r\nSubmitted using MCAutoSubmit v1.1.1",
                    "variables": {
                    "jlzkwql2": {
                        "type": "pre-defined",
                        "value": versionKey
                    },
                    "9l737pn1": {
                        "type": "pre-defined",
                        "value": diffiid
                    },
                    "r8rg67rn": {
                        "type": "pre-defined",
                        "value": seedTypeKey
                    },
                    "wl33kewl": {
                        "type": "pre-defined",
                        "value": versionRange
                    },
                    "ql6g2ow8": {
                        "type": "pre-defined",
                        "value": f3
                    },
                    "dloymqd8": {
                        "type": "pre-defined",
                        "value": modsapi
                    }
                    }
                    }





                    self.startButton.setDisabled(True)
                    QtTest.QTest.qWait(300)
                    r = requests.post('https://www.speedrun.com/api/v1/runs', json={'run': datas}, headers={'X-API-Key': api_key})
                    QtTest.QTest.qWait(300)
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