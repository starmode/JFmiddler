import os
import re
import platform
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QTime
from static import Ui_MainWindow
from JFTools.model import defaultInput, defaultArrayx, defaultCollapx, defaultPrintlib
from JFTools.read import readj, readg, readf
from JFTools.write import writef, writej
from JFTools.call import jmct, fisp


class Dynamics(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(Dynamics, self).__init__()
        self.setupUi(self)
        # 内部变量
        self._Zoom = 0
        self._LastRoute = 'C:/'
        self._FISPWork = ''
        self._InfoText = ''
        self._SavedNeutron = None
        # False--JtoF True--FtoJ
        self._ToDoL = False
        # False--callF True--callJ
        self._ToDoR = False
        self._ProgressOne = 0
        self._ProgressAll = 0
        self._Num = 0
        self._OneStep = 0
        self._AllStep = 0
        # 动作信号
        self.JOutFilePickU.clicked.connect(self.openJFileUp)
        self.JOutFilePickD.clicked.connect(self.openJFileDown)
        self.GFilePick.clicked.connect(self.openGFile)
        self.FWorkPickU.clicked.connect(self.openFDirUp)
        self.FWorkPickD.clicked.connect(self.openFDirDown)
        self.LoadFile.clicked.connect(self.loadFiles)
        self.ResetL.clicked.connect(self.resetL)
        self.QuitL.clicked.connect(QCoreApplication.instance().quit)
        self.JtoFChose.clicked.connect(self.jtoF)
        self.FtoJChose.clicked.connect(self.ftoJ)
        self.StartL.clicked.connect(self.start)
        self.JModelPick.clicked.connect(self.openJModel)

        self.FPick.clicked.connect(self.openFInstall)
        self.EPick.clicked.connect(self.openEAFDir)
        self.FWorkPick.clicked.connect(self.openFDirRight)
        self.JInPick.clicked.connect(self.openJIn)
        self.ResetR.clicked.connect(self.resetR)
        self.QuitR.clicked.connect(QCoreApplication.instance().quit)
        self.StartR.clicked.connect(self.call)

        self.CallFISP.clicked.connect(self.callF)
        self.CallJMCT.clicked.connect(self.callJ)
        self.allEnableL(True)
        self.allEnableR(True)
        self.pickPath()

        self.fis = Fis()
        self.fis.sinOut.connect(self.info)

        self.jmct = Jm()
        self.jmct.sinOut.connect(self.info)

        self.__desktop = QApplication.desktop()
        self.reSize()

    def closeEvent(self, event):
        self.savePath()
        event.accept()

    def pickPath(self):
        if 'wiz.ini' in os.listdir('.'):
            try:
                with open('./wiz.ini') as f:
                    lines = f.readlines()
                for line in lines:
                    tmp = line.split('=')
                    if len(tmp) != 2:
                        continue
                    if tmp[0] == 'FISPACT':
                        self.FPath.setText(tmp[1])
                    elif tmp[0] == 'EAF':
                        self.EPath.setText(tmp[1])
            except:
                pass

    def savePath(self):
        if self.FPath.text() != '' or self.EPath.text() != '':
            with open('./wiz.ini', 'w') as f:
                f.write('FISPACT=%s\n' % self.FPath.text())
                f.write('EAF=%s' % self.EPath.text())

    def reSize(self):
        screenRect = self.__desktop.screenGeometry()
        height = screenRect.height() * 9 // 10
        weight = round(37 * height / 52)
        self.resize(weight, height)
        self.setFixedSize(self.width(), self.height())

    def allEnableL(self, flag):
        self.JOutFilePathU.setEnabled(flag)
        self.GFilePath.setEnabled(flag)
        self.FWorkPathU.setEnabled(flag)
        self.JOutFilePickU.setEnabled(flag)
        self.GFilePick.setEnabled(flag)
        self.FWorkPickU.setEnabled(flag)
        self.GenRate.setEnabled(flag)
        self.Collapx.setEnabled(flag)
        self.Arrayx.setEnabled(flag)
        self.Input.setEnabled(flag)
        self.Printlib.setEnabled(flag)

        self._ToDoL = flag
        self.RetractLen.setEnabled(not flag)
        self.MaxFlag.setEnabled(not flag)
        self.JOutFilePathD.setEnabled(not flag)
        self.FWorkPathD.setEnabled(not flag)
        self.JModelPath.setEnabled(not flag)
        self.JOutFilePickD.setEnabled(not flag)
        self.FWorkPickD.setEnabled(not flag)
        self.JModelPick.setEnabled(not flag)
        self.JMCT.setEnabled(not flag)
        self.RemainJOut.setEnabled(not flag)

        self.FileEdit.setCurrentIndex(0 if flag else 4)

    def allEnableR(self, flag):
        self._ToDoR = flag
        self.Group.setEnabled(flag)
        self.Weight.setEnabled(flag)
        self.Particle.setEnabled(flag)
        self.FWorkPathR.setEnabled(flag)
        self.FWorkPick.setEnabled(flag)
        self.FPath.setEnabled(flag)
        self.EPath.setEnabled(flag)
        self.FPick.setEnabled(flag)
        self.EPick.setEnabled(flag)

        self.JInPath.setEnabled(not flag)
        self.JInPick.setEnabled(not flag)

    def jtoF(self):
        self.allEnableL(True)

    def ftoJ(self):
        self.allEnableL(False)

    def callF(self):
        self.allEnableR(True)

    def callJ(self):
        self.allEnableR(False)

    def getOneProgress(self, t, n):
        if self._ToDoL == True:
            self._Zoom = 1 / 8
        else:
            self._Zoom = 1 / 7
        self._Num = n
        self._OneStep = 100 / t
        self._AllStep = 100 * self._Zoom / t

    def updateBar(self, clear):
        if clear:
            self._ProgressOne = 0
            self._ProgressOne += self._OneStep
            self._ProgressAll += self._AllStep
            self.info('1/%d' % self._Num, 1)
        else:
            self._ProgressOne += self._OneStep
            self._ProgressAll += self._AllStep
            self.info(round((self._ProgressOne * self._Num) // 100), 2)
        self.Bar.setValue(round(self._ProgressAll))
        print(self._ProgressAll, self._Zoom, self._AllStep)

    def openJFileUp(self):
        self._LastRoute, ok = QFileDialog.getOpenFileName(self, "选择文件", self._LastRoute,
                                                          "JMCT Output File (*.out);;All Files (*)")
        self.JOutFilePathU.setText(self._LastRoute)
        if self.Sync.isChecked():
            self.JOutFilePathD.setText(self._LastRoute)

    def openJFileDown(self):
        self._LastRoute, ok = QFileDialog.getOpenFileName(self, "选择文件", self._LastRoute,
                                                          "JMCT Output File (*.out);;All Files (*)")
        self.JOutFilePathD.setText(self._LastRoute)
        if self.Sync.isChecked():
            self.JOutFilePathU.setText(self._LastRoute)

    def openJModel(self):
        self._LastRoute, ok = QFileDialog.getOpenFileName(self, "选择文件", self._LastRoute,
                                                          "JMCT Input File (*.in);;All Files (*)")
        self.JModelPath.setText(self._LastRoute)

    def openGFile(self):
        self._LastRoute, ok = QFileDialog.getOpenFileName(self, "选择文件", self._LastRoute,
                                                          "GDML Structure File (*.gdml);;All Files (*)")
        self.GFilePath.setText(self._LastRoute)

    def openFDirUp(self):
        self._LastRoute = QFileDialog.getExistingDirectory(self, "选择文件夹", self._LastRoute)
        self._FISPWork = self._LastRoute
        self.FWorkPathU.setText(self._LastRoute)
        if self.Sync.isChecked():
            self.FWorkPathD.setText(self._LastRoute)
        if self.GenCall.isChecked():
            self.FWorkPathR.setText(self._LastRoute)

    def openFDirDown(self):
        self._LastRoute = QFileDialog.getExistingDirectory(self, "选择文件夹", self._LastRoute)
        self._FISPWork = self._LastRoute
        self.FWorkPathD.setText(self._LastRoute)
        if self.Sync.isChecked():
            self.FWorkPathU.setText(self._LastRoute)
        if self.GenCall.isChecked():
            self.FWorkPathR.setText(self._LastRoute)

    def openFInstall(self):
        if 'Windows' in platform.system():
            self._LastRoute, ok = QFileDialog.getOpenFileName(self, "选择文件", self._LastRoute,
                                                              "FISPACT Binary File (*.exe);;All Files (*)")
        else:
            self._LastRoute, ok = QFileDialog.getOpenFileName(self, "选择文件", self._LastRoute,
                                                              "FISPACT Binary File (*.bin);;All Files (*)")
        self.FPath.setText(self._LastRoute)

    def openEAFDir(self):
        self._LastRoute = QFileDialog.getExistingDirectory(self, "选择文件夹", self._LastRoute)
        self.EPath.setText(self._LastRoute)

    def openFDirRight(self):
        self._LastRoute = QFileDialog.getExistingDirectory(self, "选择文件夹", self._LastRoute)
        self.FWorkPathR.setText(self._LastRoute)

    def openJIn(self):
        self._LastRoute, ok = QFileDialog.getOpenFileName(self, "选择文件", self._LastRoute,
                                                          "JMCT Input File (*.in);;All Files (*)")
        self.JInPath.setText(self._LastRoute)

    def info(self, text, mode=0):
        # mode=0 -- newline
        # mode=1 -- sameline
        # mode=2 -- revise
        # mode=3 -- newline without empty line
        time = QTime.currentTime()
        if mode == 0:
            if len(self._InfoText) > 0 and self._InfoText[-1] != '\n':
                self._InfoText += '\n\n'
            self._InfoText += '[%s] %s' % (time.toString(Qt.DefaultLocaleLongDate), text)
        elif mode == 1:
            self._InfoText += '...%s' % text
        elif mode == 2:
            self._InfoText = re.sub('\d+(/\d+)$', r'%d\1' % text, self._InfoText)
        elif mode == 3:
            if len(self._InfoText) > 0 and self._InfoText[-1] != '\n':
                self._InfoText += '\n'
            self._InfoText += '[%s] %s' % (time.toString(Qt.DefaultLocaleLongDate), text)
        self.StatusL.setText(self._InfoText)
        self.StatusR.setText(self._InfoText)
        self.StatusL.moveCursor(QTextCursor.End)
        self.StatusR.moveCursor(QTextCursor.End)

    def loadFiles(self):
        if self._ToDoL == True:
            if self._FISPWork == '':
                self.info('错误：未指定FISPACT工作目录', 0)
            else:
                self.info('从 %s 读取FISPACT输入文件' % self._FISPWork, 0)
                dirs = os.listdir(self._FISPWork)
                tmp = list(filter(lambda name: name[-2:] == '.i', dirs))
                # 是否找到至少一个文件
                found = False
                if 'collapx.i' in tmp:
                    self.info('更新collapx.i', 1)
                    with open(self._FISPWork + '/collapx.i') as f:
                        text = f.read()
                    self.CFileEdit.setText(text)
                    found = True
                else:
                    self.info('未找到collapx.i', 1)
                if 'arrayx.i' in tmp:
                    self.info('更新arrayx.i', 1)
                    with open(self._FISPWork + '/arrayx.i') as f:
                        text = f.read()
                    self.AFileEdit.setText(text)
                    found = True
                else:
                    self.info('未找到arrayx.i', 1)
                if 'printlib.i' in tmp:
                    self.info('更新printlib.i', 1)
                    with open(self._FISPWork + '/arrayx.i') as f:
                        text = f.read()
                    self.PFileEdit.setText(text)
                    found = True
                else:
                    self.info('未找到printlib.i', 1)
                if 'input.i' in tmp:
                    self.info('更新input.i', 1)
                    with open(self._FISPWork + '/input.i') as f:
                        text = f.read()
                    self.IFileEdit.setText(text)
                    found = True
                else:
                    self.info('未找到input.i', 1)
                if not found:
                    self.info('错误：工作目录下没有发现任何有效文件', 0)
        elif self._ToDoL == False:
            path = self.JModelPath.text()
            if path == '':
                self.info('错误：未指定JMCT模板文件', 0)
            else:
                try:
                    self.info('从 %s 读取JMCT模板文件' % path, 0)
                    with open(path) as f:
                        text = f.read()
                    self.JFileEdit.setText(text)
                except FileNotFoundError as e:
                    self.info('错误：JMCT模板文件位置无效 -> ' + repr(e), 0)
                    return
                except Exception as e:
                    self.info(repr(e))
                    return

    def resetL(self):
        self.info('左页面重置信息', 0)
        self.CFileEdit.setText(defaultCollapx)
        self.AFileEdit.setText(defaultArrayx)
        self.PFileEdit.setText(defaultPrintlib)
        self.IFileEdit.setText(defaultInput)
        self.JOutFilePathU.setText('')
        self.JOutFilePathD.setText('')
        self.GFilePath.setText('')
        self.FWorkPathU.setText('')
        self.FWorkPathD.setText('')
        self.JtoFChose.setChecked(True)
        self.RetractLen.setCurrentIndex(0)
        self.allEnableL(True)
        self._FISPWork = ''

    def resetR(self):
        self.info('右页面重置信息', 0)
        # self.Group.setCurrentIndex(3)
        # self.Weight.setCurrentIndex(0)
        # self.Particle.setCurrentIndex(0)
        # self.FPath.setText('')
        # self.EPath.setText('')
        # self.FWorkPathR.setText('')
        # self.JPath.setText('')
        # self.JInPath.setText('')
        # self.CallFISP.setChecked(True)
        # self.allEnableR(True)
        # self.envEnable()

    def start(self):
        if self._ToDoL == True:
            self._ProgressAll = 0
            self.info('执行JMCT --> FISPACT', 0)
            JPathU = self.JOutFilePathU.text()
            GPath = self.GFilePath.text()
            FPath = self.FWorkPathU.text()
            CText = self.CFileEdit.toPlainText()
            AText = self.AFileEdit.toPlainText()
            IText = self.IFileEdit.toPlainText()
            PText = self.PFileEdit.toPlainText()
            GenRate = self.GenRate.text()
            try:
                GenRate = float(GenRate)
            except ValueError:
                self.info('错误：光子单位时间产额不是有效数据', 0)
                return
            except Exception as e:
                self.info(repr(e))
                return

            if self.SaveNeu.isChecked() and self._SavedNeutron:
                self.info('读取暂存的物质信息', 0)
                neutron = self._SavedNeutron
            elif self.SaveNeu.isChecked() and not self._SavedNeutron:
                self.info('没有暂存的物质信息', 0)
            self.info('读取JMCT输出文件 %s' % JPathU, 0)
            if not (self.SaveNeu.isChecked() and self._SavedNeutron):
                try:
                    neutron = readj(JPathU, self.updateBar, self.getOneProgress)
                except FileNotFoundError as e:
                    self.info('错误：JMCT输出文件位置无效 -> ' + repr(e), 0)
                    return
                except AttributeError as e:
                    self.info('错误：JMCT输出文件不合法 -> ' + repr(e), 0)
                    return
                except Exception as e:
                    self.info(repr(e), 0)
                    return
            if self.SaveNeu.isChecked() and not self._SavedNeutron:
                self.info('储存物质信息', 0)
                self._SavedNeutron = neutron
            self.info('读取GDML结构文件 %s' % GPath, 0)
            try:
                structure = readg(GPath, self.updateBar, self.getOneProgress)
            except FileNotFoundError:
                self.info('错误：GDML结构文件位置无效', 0)
                return
            except Exception as e:
                self.info(repr(e), 0)
                return

            self.info('将FISPACT输入文件写入 %s' % FPath, 0)
            try:
                writef(FPath, GenRate, neutron, structure, IText, CText, AText, PText, self.updateBar,
                       self.getOneProgress)
            except Exception as e:
                self.info(repr(e), 0)
                return
            self.info('文件转换完成', 0)

        elif self._ToDoL == False:
            self._ProgressAll = 0
            self.info('执行FISPACT --> JMCT', 0)
            FPath = self.FWorkPathD.text()
            JPathD = self.JOutFilePathD.text()
            JModel = self.JModelPath.text()
            JText = self.JFileEdit.toPlainText()
            tmp = [' ' * 3, ' ' * 2, ' ' * 4, '\t']
            split = tmp[self.RetractLen.currentIndex()]
            if JText == '':
                self.info('自动导入JMCT模板文件')
                self.loadFiles()
                JText = self.JFileEdit.toPlainText()
            try:
                maxFlag = float(self.MaxFlag.text())
            except Exception as e:
                self.info(repr(e), 0)
                return
            if self.SaveNeu.isChecked() and self._SavedNeutron:
                self.info('读取暂存的物质信息', 0)
                neutron = self._SavedNeutron
            elif self.SaveNeu.isChecked() and not self._SavedNeutron:
                self.info('没有暂存的物质信息', 0)
            self.info('读取JMCT输出文件 %s' % JPathD, 0)
            if not (self.SaveNeu.isChecked() and self._SavedNeutron):
                try:
                    neutron = readj(JPathD, self.updateBar, self.getOneProgress)
                except FileNotFoundError:
                    self.info('错误：JMCT输出文件位置无效', 0)
                    return
                except AttributeError as e:
                    self.info('错误：JMCT输出文件不合法 -> ' + repr(e), 0)
                    return
                except Exception as e:
                    self.info(repr(e), 0)
                    return
            if self.SaveNeu.isChecked() and not self._SavedNeutron:
                self.info('储存物质信息', 0)
                self._SavedNeutron = neutron
            self.info('读取FISPACT输出文件 %s' % FPath, 0)
            try:
                distributes = readf(FPath, maxFlag, self.updateBar, self.getOneProgress)
            except FileNotFoundError as e:
                self.info('错误：FISPACT输出文件位置无效 ->' + repr(e), 0)
                return
            except Exception as e:
                self.info(repr(e), 0)
                return
            pos = JPathD.rindex('.')
            if self.RemainJOut.isChecked():

                newPath = JPathD[:pos] + '_new' + '.in'
            else:
                newPath = JPathD[:pos] + '.in'
            self.info('将新的JMCT输入文件写入 %s' % newPath, 0)
            try:
                writej(JModel, JText, neutron, distributes, split, newPath, self.updateBar, self.getOneProgress)
            except AttributeError as e:
                self.info('错误：JMCT模板文件不含有{source}关键字 -> ' + repr(e), 0)
                return
            except Exception as e:
                self.info(repr(e), 0)
                return
            self.info('文件转换完成', 0)

    def call(self):
        if self._ToDoR == True:
            # callFISP
            FPath = self.FPath.text()
            EPath = self.EPath.text()
            Case = self.FWorkPathR.text()

            tmp = ['69', '100', '172', '175', '211', '315', '351']
            g = tmp[self.Group.currentIndex()]
            tmp = ['flt', 'fis', 'fus']
            w = tmp[self.Weight.currentIndex()]
            tmp = ['n', 'p', 'd']
            p = tmp[self.Particle.currentIndex()]

            if FPath == '':
                self.info('错误：未指定FISPACT主程序位置', 0)
                return
            if EPath == '':
                self.info('错误：未指定EAF数据库安装目录', 0)
                return
            if Case == '':
                self.info('错误：未指定FISPACT工作目录', 0)
                return
            group = [p, g, w]
            env = [FPath, EPath]
            self.fis.env = env
            self.fis.group = group
            self.fis.case = Case
            self.fis.start()
        else:
            # callJMCT
            JInPath = self.JInPath.text()
            if JInPath == '':
                self.info('错误：未指定JMCT输入文件', 0)
                return
            self.jmct.JInPath = JInPath
            self.jmct.start()


class Fis(QThread):
    sinOut = pyqtSignal(str, int)
    case = ''
    env = ['', '']
    group = ['', '', '']

    def run(self):
        self.sinOut.emit('调用Fispact中...', 0)
        try:
            fisp(self.sinOut.emit, self.env, self.group, self.case)
        except BaseException as a:
            self.sinOut.emit(a, 0)
        self.sinOut.emit('调用结束', 0)


class Jm(QThread):
    sinOut = pyqtSignal(str, int)
    JInPath = ''

    def run(self):
        self.sinOut.emit('调用Jmct中...', 0)
        try:
            jmct(self.sinOut.emit, self.JInPath)
        except Exception as a:
            self.sinOut.emit(a, 0)
        self.sinOut.emit('调用结束', 0)