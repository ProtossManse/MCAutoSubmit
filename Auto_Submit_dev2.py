from PyQt5 import QtWidgets
import sys
import os
import keyboard
from nbt.nbt import NBTFile
import getpass
import datetime
import webbrowser
import requests
import json

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
        self.descriptionText.setText(WOWSANS.value("desc", "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">p, li { white-space: pre-wrap; }</style></head><body style=\" font-family:\'맑은 고딕\'; font-size:9pt; font-weight:400; font-style:normal;\"><p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Description (Manual)</p><p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Do not enter the seed.</p></body></html>"))
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
        self.apiLabel.mousePressEvent = self.link
        self.statusBar().showMessage("MCAutoSubmit by ProtossManse with Haru")
        self.auto()
        
        

        if WOWSANS.value("lang") == "한국어":
            self.langBox.setCurrentText("한국어")

        




    def credit(self, event):
        QMessageBox.information(self, "Credits", "MCAutoSubmit by ProtossManse with Haru.\n\nIcon by ChobojaX.")
        

    def seedClicked(self):
        if self.langBox.currentText() == "한국어":
            seed, ok1 = QInputDialog.getText(self, "시드 변경", "<font face=\"Malgun Gothic\">시드:</font>")
        else:
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
        patht = QtWidgets.QFileDialog.getExistingDirectory(self, 'Browse...', path)
        if patht != "":
            path = patht.replace("/", "\\")
            self.pathLine.setText(str(path))
            WOWSANS.setValue("path", str(path))


    def lang(self):
        
        if self.langBox.currentText() == "한국어":
            WOWSANS.setValue("lang", "한국어")
            self.seedButton.setText("시드 변경")
            self.label_2.setText("Real Time (수동):")
            self.label_7.setText("버전:")
            self.label_8.setText("난이도:")
            self.label_9.setText("모드:")
            self.creditLabel.setText("크레딧")
            self.label_13.setText("시드 타입:")
            self.label_10.setText("경로:")
            self.apiLabel.setText("<html><head/><body><p><span style=\" color:#0000ff;\">API 키 (URL):</span></p></body></html>")
            self.pathButton.setText("찾기...")
            self.label_14.setText("<html><head/><body><p align=\"center\"><span style=\" font-size:11pt; font-weight:600; color:#ff0000;\">1.16.1 전용</span></p></body></html>")
            self.startButton.setText("제출")
            self.resetButton.setText("새로고침\n(Esc)")
            self.linkButton.setText("테스트...")
            if self.ytLink.text() == "Video Link(Manual)":
                self.ytLink.setText("동영상 링크 (수동)")
            if self.descriptionText.toPlainText() == "Description (Manual)\nDon't enter the seed.":
                self.descriptionText.setText("<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">p, li { white-space: pre-wrap; }</style></head><body style=\" font-family:\'맑은 고딕\'; font-size:9pt; font-weight:400; font-style:normal;\"><p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">설명 (수동)</p><p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">시드를 입력하지 마세요.</p></body></html>")
        elif self.langBox.currentText() == "English":
            WOWSANS.setValue("lang", "english")
            self.seedButton.setText("Change Seed")
            self.label_2.setText("Real Time(Manual):")
            self.label_7.setText("Version:")
            self.label_8.setText("Difficulty:")
            self.label_9.setText("Mods:")
            self.label_13.setText("Seed Type:")
            self.label_10.setText("Path:")
            self.apiLabel.setText("<html><head/><body><p><span style=\" color:#0000ff;\">API Key (URL):</span></p></body></html>")
            self.creditLabel.setText("Credits")
            self.pathButton.setText("Browse...")
            self.linkButton.setText("Test...")
            self.label_14.setText("<html><head/><body><p align=\"center\"><span style=\" font-size:11pt; font-weight:600; color:#ff0000;\">Only 1.16.1</span></p></body></html>")
            self.startButton.setText("Submit")
            self.resetButton.setText("Refresh\n(Esc)")
            if self.ytLink.text() == "동영상 링크 (수동)":
                self.ytLink.setText("Video Link(Manual)")
            if self.descriptionText.toPlainText() == "설명 (수동)\n시드를 입력하지 마세요.":
                self.descriptionText.setText("<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">p, li { white-space: pre-wrap; }</style></head><body style=\" font-family:\'맑은 고딕\'; font-size:9pt; font-weight:400; font-style:normal;\"><p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Description (Manual)</p><p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Do not enter the seed.</p></body></html>")
            


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
            global mc_sec
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

                

            # print(f"\n{str(mc_version)}\n{str(mc_diffi)}\n{mc_igt} ticks\n{hr} hour {min} min {sec} secs {ms} ms\nSeed: {mc_seed}\nModded: {mc_moded}\nCtime: {str(ctime)}\n{mc_isend}\n{mc_sec}\n")
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

    def link(self, event):
        webbrowser.open('https://www.speedrun.com/api/auth')

    def test(self):
        WOWSANS.setValue("api", self.apiLine.text())
        self.linkButton.setDisabled(True)
        QtTest.QTest.qWait(300)
        api_key = self.apiLine.text()
        res = requests.get('https://www.speedrun.com/api/v1/profile', headers={'X-API-Key': api_key})
        # print(res.json)
        QtTest.QTest.qWait(300)
        if str(res) == "<Response [403]>":
            QMessageBox.warning(self, "ERROR", "No User Found", QMessageBox.Ok)
        elif str(res) == "<Response [200]>":
            srcuser = res.json()["data"]["names"]["international"]
            global userid
            userid = res.json()["data"]["id"]
            QMessageBox.information(self, "Success", f"Found User. Hello {srcuser}. (id: {userid})")
        self.linkButton.setEnabled(True)

    
        



        


#-------------------------------------------macro--------------------- 


    def macro1(self):
        rtHour = int(self.rtaHr.text())
        rtMin = int(self.rtMin.text())
        rtSec = int(self.rtSec.text())
        rtPoint = float(self.rtPoint.text())
        api_key = self.apiLine.text()
        # igtHr = self.igtHr.text()
        # igtMin = self.igtMin.text()
        # igtSec = self.igtSec.text()
        # igtPoint = self.igtPoint.text()
        seedType = self.seedType.currentText()
        if seedType == "SSG":
            seedTypeKey = "klrzpjo1"
        elif seedType == "RSG":
            seedTypeKey = "21d4zvp1"
        mods = self.Mods.currentText()
        if mods == "Vanilla":
            modsapi = "21gyvwm1"
        elif mods == "CaffeineMC":
            modsapi = "jq6kxd3l"
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


        ytlink = self.ytLink.text()
        seed = self.sText.text()
        desc = self.descriptionText.toPlainText()
        WOWSANS.setValue("desc", "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">p, li { white-space: pre-wrap; }</style></head><body style=\" font-family:\'맑은 고딕\'; font-size:9pt; font-weight:400; font-style:normal;\"><p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">"+desc+"</p></body></html>")
        WOWSANS.setValue("seedType", seedType)
        try:

            

            if rtHour == 00 and rtMin == 00 and rtSec == 00 and rtPoint == 000:
                QMessageBox.warning(self, "ERROR", "You didn't enter RT(Real Time)!")

            else:
                
                data = {
                "category": "mkeyl926",
                "date": datetime.datetime.today().strftime("%Y-%m-%d"),
                "platform": "8gej2n93",
                "verified": False,
                "times": {
                "realtime": rtHour * 3600 + rtMin * 60 + rtSec + rtPoint / 1000,
                "realtime_noloads": 0,
                "ingame": float(mc_sec)
                },
                "players": [
                {"rel": "user", "id": "8qrllpwj"}
                ],
                "emulated": False,
                "video": ytlink,
                "comment": f"{seed}\r\n{desc}\r\n",
                "variables": {
                "jlzkwql2": {
                    "type": "pre-defined",
                    "value": "mln68v0q"
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
                    "value": "4qye4731"
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

                # {
                # "run": [{
                # "game": "j1npme6p",
                # "level": None,
                # "category": "mkeyl926",
                # "verified": False,
                # "videos": {
                #     "links": [{
                #         "uri": f"{ytlink}"
                #     }]
                # },
                # "comment": f"{seed}\r\n{desc}\r\n",
                # "players": [{
                #     "rel": "user",
                #     "id": f"{userid}",
                #     "uri": f"https://www.speedrun.com/api/v1/users/{userid}"
                # }],
                # "date": datetime.datetime.today().strftime("%Y-%m-%d"),
                # "times": {
                #     "realtime_t": rtHour * 3600 + rtMin * 60 + rtSec + rtPoint / 1000,
                #     "realtime_noloads_t": 0,
                #     "ingame_t": float(mc_sec),
                # },
                # "system": {
                #     "platform": "8gej2n93",
                #     "emulated": False,
                #     "region": None,
                # },
                # "splits": None,
                # "values": {
                #     "jlzkwql2": "mln68v0q",
                #     "9l737pn1": f"{diffiid}",
                #     "r8rg67rn": f"{seedType}",
                #     "wl33kewl": "4qye4731",
                #     "ql6g2ow8": f"{f3}",
                #     "dloymqd8": f"{modsapi}"
                #         },
                #     }],
                # }



                self.startButton.setDisabled(True)
                QtTest.QTest.qWait(300)
                r = requests.post('https://www.speedrun.com/api/v1/runs',headers={'X-API-Key': api_key}, data=json.dumps({'run': data}))
                print(r.url)
                if r.status_code == 400:
                    try:
                        QMessageBox.warning(self,"ERROR", str(r.json()['errors']))
                    except:
                        QMessageBox.warning(self, "ERROR", "Unknown ERROR")
                QtTest.QTest.qWait(300)
                self.startButton.setEnabled(True)

        except NameError:
            QMessageBox.warning(self, "ERROR", "Press \'Test\' Button!")


        
        





if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_dialog = MainDialog()
    main_dialog.show()
    app.exec_()


