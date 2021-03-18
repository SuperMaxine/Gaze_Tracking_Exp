import sys
import cv2
import numpy as np
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.uic import loadUi
from PyQt5.QtGui import QPixmap, QImage
import process

class Window(QMainWindow):
    def __init__(self):
        super(Window, self).__init__()
        loadUi('GUImain.ui', self)
        self.startButton.clicked.connect(self.start_webcam)
        self.stopButton.clicked.connect(self.stop_webcam)
        self.camera_is_running = False

    def start_webcam(self):
        if not self.camera_is_running:
            self.capture = cv2.VideoCapture(cv2.CAP_DSHOW)  # VideoCapture(0) sometimes drops error #-1072875772
            if self.capture is None:
                self.capture = cv2.VideoCapture(0)
            self.camera_is_running = True
            self.timer = QTimer(self)
            self.timer.timeout.connect(self.update_frame)
            self.timer.start(2)

    def stop_webcam(self):
        if self.camera_is_running:
            self.capture.release()
            self.timer.stop()
            self.camera_is_running = not self.camera_is_running

    def update_frame(self):
        _, base_image = self.capture.read()
        # self.display_image(base_image)
        processed_image = process.detect_face(base_image)
        self.display_image(processed_image)

    def display_image(self, img, window='main'):
        qformat = QImage.Format_Indexed8
        if len(img.shape) == 3:
            if img.shape[2] == 4:  # RGBA
                qformat = QImage.Format_RGBA8888
            else:  # RGB
                qformat = QImage.Format_RGB888

        out_image = QImage(img, img.shape[1], img.shape[0], img.strides[0], qformat)  # BGR to RGB
        out_image = out_image.rgbSwapped()
        if window == 'main':  # main window
            self.baseImage.setPixmap(QPixmap.fromImage(out_image))
            self.baseImage.setScaledContents(True)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    window.setWindowTitle("GUI")
    window.show()
    sys.exit(app.exec_())