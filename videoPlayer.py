import csv

from PyQt5.QtCore import QDir, Qt, QUrl
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtWidgets import (QApplication, QFileDialog, QHBoxLayout, QLabel,
        QPushButton, QSizePolicy, QSlider, QStyle, QVBoxLayout, QWidget, QComboBox, QLineEdit, QMessageBox)
import time,math

class VideoPlayer(QWidget):

    def __init__(self, parent=None):
        super(VideoPlayer, self).__init__(parent)

        self.setWindowTitle("ViSA")
        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)

        videoWidget = QVideoWidget()
        openButton = QPushButton("Load Video File")
        openButton.clicked.connect(self.openFile)

        self.startValue = 0
        self.endValue = 0

        self.forwardButton = QPushButton()
        self.forwardButton.setEnabled(False)
        self.forwardButton.setIcon(self.style().standardIcon(QStyle.SP_MediaSeekForward))
        self.forwardButton.clicked.connect(self.forward)

        self.playButton = QPushButton()
        self.playButton.setEnabled(False)
        self.playButton.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.playButton.clicked.connect(self.play)

        self.backwardButton = QPushButton()
        self.backwardButton.setEnabled(False)
        self.backwardButton.setIcon(self.style().standardIcon(QStyle.SP_MediaSeekBackward))
        self.backwardButton.clicked.connect(self.backward)

        self.playBackSpeed = QComboBox()
        self.playBackSpeed.addItem("0.25")
        self.playBackSpeed.addItem("0.5")
        self.playBackSpeed.addItem("0.75")
        self.playBackSpeed.addItem("1")
        self.playBackSpeed.addItem("1.25")
        self.playBackSpeed.addItem("1.5")
        self.playBackSpeed.addItem("1.75")
        self.playBackSpeed.addItem("2")
        self.playBackSpeed.setCurrentIndex(3)
        self.playBackSpeed.setVisible(False)

        self.start = QSlider(Qt.Horizontal)
        self.start.setRange(0, 0)
        self.start.sliderMoved.connect(self.setPosition)

        self.startLabel = QLabel()

        self.end = QSlider(Qt.Horizontal)
        self.end.setRange(0, 0)
        self.end.sliderMoved.connect(self.setPosition)

        self.endLabel = QLabel()

        controlLayout = QHBoxLayout()
        controlLayout.setContentsMargins(250, 0, 350, 0)
        controlLayout.addWidget(openButton)
        controlLayout.addWidget(self.backwardButton)
        controlLayout.addWidget(self.playButton)
        controlLayout.addWidget(self.forwardButton)
        controlLayout.addWidget(self.playBackSpeed)

        sliders = QVBoxLayout()
        sliders.setContentsMargins(0, 0, 0, 0)
        sliderLayout = QHBoxLayout()
        sliderLayout.setContentsMargins(0, 0, 0, 0)
        sliderLayout.addWidget(self.startLabel)
        sliderLayout.addWidget(self.start)
        sliders.addLayout(sliderLayout)
        sliderLayout = QHBoxLayout()
        sliderLayout.setContentsMargins(0, 0, 0, 0)
        sliderLayout.addWidget(self.endLabel)
        sliderLayout.addWidget(self.end)
        sliders.addLayout(sliderLayout)

        self.editGesture = QLineEdit()
        self.editGesture.setVisible(False)
        self.editGesture.setPlaceholderText("Add Gesture")
        self.editGesture.setFixedWidth(200)

        self.gestures = QComboBox()
        self.gestures.addItem("Walking")
        self.gestures.setVisible(False)
        self.gesture = "Walking"

        self.submit = QPushButton("Submit")
        self.submit.clicked.connect(self.addGesture)
        self.submit.setVisible(False)

        self.errorLabel = QLabel()
        self.errorLabel.setSizePolicy(QSizePolicy.Preferred,
                                      QSizePolicy.Maximum)

        footer = QHBoxLayout()
        footer.setContentsMargins(250, 0, 350, 0)
        footer.addWidget(self.editGesture)
        footer.addWidget(self.gestures)
        footer.addWidget(self.submit)

        layout = QVBoxLayout()
        layout.addWidget(videoWidget)
        layout.addLayout(controlLayout)
        layout.addLayout(sliders)
        layout.addLayout(footer)
        layout.addWidget(self.errorLabel)

        self.setLayout(layout)

        self.mediaPlayer.setVideoOutput(videoWidget)
        self.mediaPlayer.stateChanged.connect(self.mediaStateChanged)
        self.mediaPlayer.positionChanged.connect(self.positionChanged)
        self.mediaPlayer.durationChanged.connect(self.durationChanged)
        self.start.valueChanged.connect(self.valueChangedStart)
        self.end.valueChanged.connect(self.valueChangedEnd)
        self.mediaPlayer.error.connect(self.handleError)
        self.gestures.activated[str].connect(self.onGestureChanged)
        self.playBackSpeed.activated[str].connect(self.playBackSpeedChanged)

    def openFile(self):
        fileName, _ = QFileDialog.getOpenFileName(self, "Open Movie",
                ".")

        if fileName != '':
            self.mediaPlayer.setMedia(
                    QMediaContent(QUrl.fromLocalFile(fileName)))
            self.playButton.setEnabled(True)
            self.gestures.setVisible(True)
            self.submit.setVisible(True)
            self.editGesture.setVisible(True)
            self.forwardButton.setEnabled(True)
            self.backwardButton.setEnabled(True)
            self.playBackSpeed.setVisible(True)
            self.errorLabel.setText(" ")

    def play(self):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.mediaPlayer.pause()
        else:
            self.mediaPlayer.play()

    def forward(self):
        self.mediaPlayer.setPosition(self.end.value() + 2000)

    def backward(self):
        self.mediaPlayer.setPosition(self.end.value() - 2000)

    def playBackSpeedChanged(self, value):
        self.mediaPlayer.setPlaybackRate(float(value))

    def mediaStateChanged(self, state):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.playButton.setIcon(
                    self.style().standardIcon(QStyle.SP_MediaPause))
        else:
            self.playButton.setIcon(
                    self.style().standardIcon(QStyle.SP_MediaPlay))

    def positionChanged(self, position):
        self.end.setValue(position)

    def durationChanged(self, duration):
        self.start.setRange(0, duration)
        self.end.setRange(0, duration)
        self.startLabel.setText("00:00:00")
        self.endLabel.setText("00:00:00")

    def onGestureChanged(self, text):
        self.gesture = text

    def setPosition(self, position):
        self.mediaPlayer.setPosition(position)

    def valueChangedStart(self):
        position = self.start.value()
        self.mediaPlayer.setPosition(position)
        self.startLabel.setText(self.getDurationInSeconds(position))
        self.startValue = position

    def valueChangedEnd(self):
        position = self.end.value()
        self.mediaPlayer.setPosition(position)
        self.endLabel.setText(self.getDurationInSeconds(position))
        self.endValue = position

    def handleError(self):
        self.playButton.setEnabled(False)
        self.errorLabel.setText("Error: " + self.mediaPlayer.errorString())

    def getDurationInSeconds(self, value):
        return time.strftime('%H:%M:%S', time.gmtime(math.ceil(value/1000)))

    def addGesture(self):
        gesture = self.editGesture.text().strip()
        with open('manifest.csv', 'a', newline='') as writer:
            writer = csv.writer(writer)
            duration = round(self.endValue//1000, 2) - round(self.startValue//1000, 2)
            if len(gesture) == 0:
                gesture = self.gesture
            gesture = gesture.replace(" ", "_")
            writer.writerow([round(self.startValue//1000, 2), duration, gesture])
        if len(self.editGesture.text()) > 0:
            if self.editGesture.text() not in [self.gestures.itemText(i) for i in range(self.gestures.count())] :
                self.gestures.addItem(self.editGesture.text())
        QMessageBox.about(self, "Info", gesture + "Gesture Added!")

if __name__ == '__main__':

    import sys, os

    with open('manifest.csv', 'w', newline='') as writer:
        writer = csv.writer(writer)
        writer.writerow(["start_time", "length", "rename_to"])
    app = QApplication(sys.argv)

    player = VideoPlayer()
    player.resize(1024, 1024)
    player.show()

    if app.exec_() == 0:
        os.system("python main.py " + "videos/vid.mp4")
        sys.exit(0)
