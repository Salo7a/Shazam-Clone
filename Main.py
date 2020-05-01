import sys

from PyQt5.QtCore import Qt, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QPalette, QColor, QFont, QIcon
from PyQt5.QtWidgets import QWidget, QMainWindow, QFileDialog, QApplication, QVBoxLayout, QGroupBox, QPushButton, \
    QSlider, QRadioButton, QHBoxLayout, QTableWidget, QHeaderView, QTableWidgetItem, QLabel

from AudioFunctions import *
from Similarity import FindSimilar
from Spectrogram import mix


class UI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.songData = [None, None]
        self.singleSong = None
        self.state = 0
        self.songWeights = [50, 50]
        self.songBoxes = [songUI(0), songUI(1)]
        self.singleBox = singleUI()
        self.songBoxes[0].sendData.connect(self.recieveData)
        self.songBoxes[1].sendData.connect(self.recieveData)
        self.singleBox.sendSong.connect(self.recieveSong)
        self.mainBox = QVBoxLayout()
        self.mixingBox = QHBoxLayout()

        self.radioUI()

        self.setMixingUI()
        self.mixingGroup = QGroupBox()
        self.mixingGroup.setLayout(self.mixingBox)
        self.mainBox.addWidget(self.mixingGroup)
        self.mainBox.addWidget(self.singleBox)
        self.singleBox.show()
        self.mixingGroup.hide()
        self.startButton = QPushButton("Search")
        self.startButton.clicked.connect(self.searchSimilarity)
        self.startButton.setEnabled(False)
        self.mainBox.addWidget(self.startButton)

        self.createTable()
        self.tableWidget.setColumnWidth(0, 150)
        self.tableWidget.setColumnWidth(1, 150)
        self.tableWidget.setColumnWidth(2, 200)
        # self.tableWidget.resizeColumnsToContents()
        # header = self.tableWidget.horizontalHeader()       
        # header.setSectionResizeMode(0, QHeaderView.Stretch)
        # header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        # header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        self.mainBox.addWidget(self.tableWidget)
        self.mainGroup = QGroupBox()
        self.mainGroup.setLayout(self.mainBox)
        self.setCentralWidget(self.mainGroup)
        self.width = 500
        self.height = 400
        self.setGeometry(50, 50, self.width, self.height)

    def setMixingUI(self):
        self.mixingBox.addWidget(self.songBoxes[0])
        self.slider = QSlider()
        self.slider.setOrientation(Qt.Horizontal)
        self.slider.setTickPosition(QSlider.TicksBelow)
        self.slider.setMinimum(0)
        self.slider.setMaximum(100)
        self.slider.setMinimumWidth(300)
        self.slider.setMaximumWidth(500)
        self.slider.setSingleStep(10)
        self.slider.setTickInterval(10)
        self.slider.setValue(50)
        self.slider.valueChanged.connect(self.sliderMoved)
        self.slider.setEnabled(False)
        self.mixingBox.addWidget(self.slider)
        self.mixingBox.addWidget(self.songBoxes[1])

    def sliderMoved(self):
        sliderValue = self.slider.value()
        self.songWeights = [sliderValue, (100 - sliderValue)]
        self.songBoxes[0].weightLabel.setText(str(self.songWeights[0]) + '%')
        self.songBoxes[1].weightLabel.setText(str(self.songWeights[1]) + "%")

    def radioUI(self):
        hboxLayout = QHBoxLayout()
        self.radio1 = QRadioButton("Single Song")
        self.radio1.setChecked(True)
        hboxLayout.addWidget(self.radio1)
        self.radio1.toggled.connect(self.toggleState)

        self.radio2 = QRadioButton("Mix Songs")
        self.radio2.setChecked(False)
        hboxLayout.addWidget(self.radio2)
        self.radio2.toggled.connect(self.toggleState)

        self.reset = QPushButton("Reset")
        self.reset.clicked.connect(self.resetData)
        hboxLayout.addWidget(self.reset)

        groupBox = QGroupBox()
        groupBox.setLayout(hboxLayout)
        self.mainBox.addWidget(groupBox)

    def toggleState(self):
        radioBtn = self.sender()
        if radioBtn.isChecked():
            if radioBtn.text() == "Single Song":
                self.state = 0
                self.singleBox.show()
                self.mixingGroup.hide()
            elif radioBtn.text() == "Mix Songs":
                self.state = 1
                self.singleBox.hide()
                self.mixingGroup.show()
            self.checkData()

    def resetData(self):
        self.songData = [None, None]
        self.singleSong = None
        self.slider.setValue(50)
        self.slider.setEnabled(False)
        self.startButton.setEnabled(False)
        self.songBoxes[0].nameLabel.setText("Song #1")
        self.songBoxes[1].nameLabel.setText("Song #2")
        self.singleBox.label.setText("Select Song")
        self.tableDefault()

    def searchSimilarity(self):
        if self.state == 1:
            mixture = mix(self.songData[0], self.songData[1], self.songWeights[0] / 100)
        else:
            mixture = self.singleSong
        self.similarityList = FindSimilar(mixture, SongMode="Array", SimilarityMode="Permissive")
        self.showSimilarity()

    @pyqtSlot(list)
    def recieveData(self, data):
        print("recieved here also")
        self.songData[data[0]] = data[1]
        self.checkData()

    @pyqtSlot(list)
    def recieveSong(self, data):
        print("recieved song here also")
        self.singleSong = data[0]
        self.startButton.setEnabled(True)

    def checkData(self):
        if self.state == 1:
            if self.songData[0] is not None and self.songData[1] is not None:
                self.slider.setEnabled(True)
                self.startButton.setEnabled(True)
            else:
                self.slider.setEnabled(False)
                self.startButton.setEnabled(False)
        else:
            if self.singleSong is not None:
                self.startButton.setEnabled(True)
            else:
                self.startButton.setEnabled(False)

    def createTable(self):
        # Create table
        self.tableWidget = QTableWidget()
        self.tableWidget.setRowCount(10)
        self.tableWidget.setColumnCount(3)
        self.tableWidget.setStyleSheet("font-size: 16px")
        self.tableWidget.setEditTriggers(QTableWidget.NoEditTriggers)
        self.tableWidget.setFont(QFont("Times", 20))
        # table->horizontalHeader()->setSectionResizeMode(QHeaderView::Stretch);
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableWidget.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableWidget.setHorizontalHeaderLabels("Song Name; Artist ;Simliarity Factor".split(';'))
        self.tableDefault()

    def tableDefault(self):
        for row in range(10):
            for col in range(3):
                str = ''
                if col == 0:
                    str = 'Song {}'.format(row + 1)
                elif col == 1:
                    str = 'Artist {}'.format(row + 1)
                else:
                    str = 'Similarity {}'.format(row + 1)
                self.tableWidget.setItem(row, col, QTableWidgetItem(str))

    def showSimilarity(self):
        for row in range(10):
            for col in range(3):
                self.tableWidget.setItem(row, col, QTableWidgetItem(str(self.similarityList[row][col])))


class songUI(QWidget):
    sendData = pyqtSignal(list)

    def __init__(self, index):
        super().__init__()
        self.index = index
        self.nameLabel = QLabel("Song #{}".format(index + 1))
        self.nameLabel.setStyleSheet("font-size: 20px")
        self.nameLabel.setAlignment(Qt.AlignCenter)
        self.weightLabel = QLabel("50%")
        self.weightLabel.setAlignment(Qt.AlignCenter)
        self.weightLabel.setStyleSheet("font-size: 20px")
        self.openButton = QPushButton("Select Song #{}".format(index + 1))
        self.openButton.setStyleSheet("font-size: 20px")
        self.openButton.clicked.connect(self.openMusic)
        self.songClass = None
        songBox = QVBoxLayout()
        songBox.addWidget(self.nameLabel)
        songBox.addWidget(self.weightLabel)
        songBox.addWidget(self.openButton)
        self.setMaximumWidth(500)
        self.setMaximumHeight(300)
        self.setLayout(songBox)

    def openMusic(self):
        options = QFileDialog.Options()
        path, _ = QFileDialog.getOpenFileName(self, "Open Music", "",
                                              "Music Files (*.mp3)", options=options)

        if path:
            self.songClass = song2data(path)
            self.sendSongData()
            songName = self.getFileName(path)
            self.nameLabel.setText(songName)

    @pyqtSlot()
    def sendSongData(self):
        sendList = [self.index, self.songClass]
        self.sendData.emit(sendList)
        print("Sent Here")

    def getFileName(self, path):
        """
        getFileName gets the file name out of its path
        :param path: the path of the file as it contains the file name
        :return: the name of the file
        """
        return path.split('.')[-2].split('/')[-1]


class singleUI(QWidget):
    sendSong = pyqtSignal(list)

    def __init__(self):
        super().__init__()
        self.selectButton = QPushButton("Select Song")
        self.selectButton.clicked.connect(self.openFile)
        self.selectButton.setMaximumWidth(500)
        self.selectButton.setStyleSheet("font-size: 20px")
        self.label = QLabel("Select Song")
        self.label.setStyleSheet("font-size: 20px")
        self.label.setAlignment(Qt.AlignCenter)
        layout = QHBoxLayout()
        layout.addWidget(self.selectButton)
        layout.addWidget(self.label)
        self.setLayout(layout)

    def openFile(self):
        options = QFileDialog.Options()
        path, _ = QFileDialog.getOpenFileName(self, "Open Music", "",
                                              "Music Files (*.mp3)", options=options)

        if path:
            self.songClass = song2data(path)
            self.sendSongData()
            songName = self.getFileName(path)
            self.label.setText(songName)

    @pyqtSlot()
    def sendSongData(self):
        songData = getFirstData(self.songClass.data, 60)
        data = [songData]
        self.sendSong.emit(data)
        print("Sent Song Here")

    def getFileName(self, path):
        """
        getFileName gets the file name out of its path
        :param path: the path of the file as it contains the file name
        :return: the name of the file
        """
        return path.split('.')[-2].split('/')[-1]


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setApplicationName("3S Music Identifier & Mixer")
    app.setWindowIcon(QIcon("track.png"))
    app.setStyle("Fusion")
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor(53, 53, 53))
    palette.setColor(QPalette.WindowText, Qt.white)
    palette.setColor(QPalette.Base, QColor(25, 25, 25))
    palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
    palette.setColor(QPalette.ToolTipBase, Qt.white)
    palette.setColor(QPalette.ToolTipText, Qt.white)
    palette.setColor(QPalette.Text, Qt.white)
    palette.setColor(QPalette.Button, QColor(53, 53, 53))
    palette.setColor(QPalette.ButtonText, Qt.white)
    palette.setColor(QPalette.BrightText, Qt.red)
    palette.setColor(QPalette.Link, QColor(42, 130, 218))
    palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
    palette.setColor(QPalette.HighlightedText, Qt.black)
    app.setPalette(palette)
    app.setStyleSheet("QToolTip { color: #ffffff; background-color: #2a82da; border: 1px solid white; }")
    win = UI()
    win.show()
    sys.exit(app.exec_())
