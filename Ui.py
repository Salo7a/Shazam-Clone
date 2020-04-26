from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys
from AudioFunctions import *
import time

class UI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.songData = [None, None]
        self.songWeights = [50, 50]
        self.songBoxes = [songUI(0), songUI(1)]
        self.songBoxes[0].sendData.connect(self.recieveData)
        self.songBoxes[1].sendData.connect(self.recieveData)
        self.mainBox = QVBoxLayout() 
        self.mixingBox = QHBoxLayout()
        self.setMixingUI()
        self.mixingGroup = QGroupBox()
        self.mixingGroup.setLayout(self.mixingBox)
        self.mainBox.addWidget(self.mixingGroup)

        self.startButton = QPushButton("Start Mixing")
        self.startButton.setEnabled(False)
        self.mainBox.addWidget(self.startButton)

        self.createTable()
        self.tableWidget.setColumnWidth(0, 150)
        self.tableWidget.setColumnWidth(1, 150)
        # self.tableWidget.resizeColumnsToContents()
        # header = self.tableWidget.horizontalHeader()       
        # header.setSectionResizeMode(0, QHeaderView.Stretch)
        # header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        # header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        self.mainBox.addWidget(self.tableWidget)


        self.mainGroup = QGroupBox()
        self.mainGroup.setLayout(self.mainBox)
        self.setCentralWidget(self.mainGroup)

    def setMixingUI(self):
        self.mixingBox.addWidget(self.songBoxes[0])
        self.slider = QSlider()
        self.slider.setOrientation(Qt.Horizontal)
        self.slider.setTickPosition(QSlider.TicksBelow)
        self.slider.setMinimum(0)
        self.slider.setMaximum(100)
        self.slider.setMinimumWidth(200)
        self.slider.setMaximumWidth(400)
        self.slider.setSingleStep(10)
        self.slider.setTickInterval(10)
        self.slider.setValue(50)
        self.slider.valueChanged.connect(self.sliderMoved)
        self.mixingBox.addWidget(self.slider)
        self.mixingBox.addWidget(self.songBoxes[1])

    def sliderMoved(self):
        sliderValue = self.slider.value()
        self.songWeights = [sliderValue, (100-sliderValue)]
        self.songBoxes[0].weightLabel.setText(str(self.songWeights[0])+'%')
        self.songBoxes[1].weightLabel.setText(str(self.songWeights[1])+"%")
    
    @pyqtSlot(list)
    def recieveData(self, data):
        print("recieved here also")
        self.songData[data[0]] = data[1]
        self.checkData()


    def checkData(self):
        if self.songData[0] != None and self.songData[1] != None:
            self.startButton.setEnabled(True)

    def createTable(self):
       # Create table
        self.tableWidget = QTableWidget()
        self.tableWidget.setRowCount(10)
        self.tableWidget.setColumnCount(2)
        self.tableWidget.setStyleSheet("font-size: 16px")
        self.tableWidget.setEditTriggers(QTableWidget.NoEditTriggers)
        self.tableWidget.setFont(QFont("Times", 20))
        #table->horizontalHeader()->setSectionResizeMode(QHeaderView::Stretch);
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableWidget.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableWidget.setHorizontalHeaderLabels("Song Name; Simliarity Index".split(';'))
        self.tableWidget.setItem(0,0, QTableWidgetItem("Cell (1,1)"))
        self.tableWidget.setItem(0,1, QTableWidgetItem("Cell (1,2)"))
        self.tableWidget.setItem(1,0, QTableWidgetItem("Cell (2,1)"))
        self.tableWidget.setItem(1,1, QTableWidgetItem("Cell (2,2)"))
        self.tableWidget.setItem(2,0, QTableWidgetItem("Cell (3,1)"))
        self.tableWidget.setItem(2,1, QTableWidgetItem("Cell (3,2)"))
        self.tableWidget.setItem(3,0, QTableWidgetItem("Cell (4,1)"))
        self.tableWidget.setItem(3,1, QTableWidgetItem("Cell (4,2)"))
        self.tableWidget.setItem(4,0, QTableWidgetItem("Cell (5,1)"))
        self.tableWidget.setItem(4,1, QTableWidgetItem("Cell (5,2)"))
        self.tableWidget.setItem(5,0, QTableWidgetItem("Cell (6,1)"))
        self.tableWidget.setItem(5,1, QTableWidgetItem("Cell (6,2)"))
        self.tableWidget.setItem(6,0, QTableWidgetItem("Cell (7,1)"))
        self.tableWidget.setItem(6,1, QTableWidgetItem("Cell (7,2)"))
        self.tableWidget.setItem(7,0, QTableWidgetItem("Cell (8,1)"))
        self.tableWidget.setItem(7,1, QTableWidgetItem("Cell (8,2)"))
        self.tableWidget.setItem(8,0, QTableWidgetItem("Cell (9,1)"))
        self.tableWidget.setItem(8,1, QTableWidgetItem("Cell (9,2)"))
        self.tableWidget.setItem(9,0, QTableWidgetItem("Cell (10,1)"))
        self.tableWidget.setItem(9,1, QTableWidgetItem("Cell (10,2)"))




class songUI(QWidget):

    sendData = pyqtSignal(list)

    def __init__(self, index):
        super().__init__()
        self.index = index
        self.nameLabel = QLabel("Song #{}".format(index+1))
        self.nameLabel.setStyleSheet("font-size: 20px")
        self.nameLabel.setAlignment(Qt.AlignCenter)
        self.weightLabel = QLabel("50%")
        self.weightLabel.setAlignment(Qt.AlignCenter)
        self.weightLabel.setStyleSheet("font-size: 20px")
        self.openButton = QPushButton("Select Song #{}".format(index+1))
        self.openButton.setStyleSheet("font-size: 20px")
        self.openButton.clicked.connect(self.openMusic)
        self.songClass = None
        songBox = QVBoxLayout()
        songBox.addWidget(self.nameLabel)
        songBox.addWidget(self.weightLabel)
        songBox.addWidget(self.openButton)
        self.setMaximumWidth(200)
        self.setMaximumHeight(300)
        self.setLayout(songBox)
        

    def openMusic(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        path, _ = QFileDialog.getOpenFileName(self, "Open Music", "",
                                              "Images Files (*.mp3)", options=options)

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


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = UI()
    win.show()
    sys.exit(app.exec_())

