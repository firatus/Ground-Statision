import sys
from PyQt5.uic import loadUi
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtWebEngineWidgets import QWebEngineView
import folium
from PyQt5.QtLocation import *
import io
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QOpenGLWidget
from PyQt5.QtGui import *
from PyQt5.QtOpenGL import QGL
import OpenGL.GL as gl
import OpenGL.GLU as glu
from PyQt5 import QtOpenGL  # provides QGLWidget, a special OpenGL QWidget
from OpenGL import GLU
from OpenGL.arrays import vbo
import OpenGL.GL as gl  # python wrapping of OpenGL
from OpenGL import GLU  # OpenGL Utility Library, extends OpenGL functionality
from PyQt5 import QtGui  # extends QtCore with GUI functionality
from PyQt5 import QtCore
import numpy as np
from vedo import *
import cv2
import urllib
import math
from PIL import  Image
class MatplotlibWidget(QMainWindow):

    def __init__(self):
        super().__init__()

        loadUi("ground_2.ui",self)


        self.timer()




    def model_2d(self,x,y):

        iki = False
        uc = False
        dort = False

        if (x < 0 and y < 0):
            uc = True

        elif (x > 0 and y < 0):
            dort = True

        elif (x < 0 and y > 0):
            iki = True

        angle = math.degrees(math.atan(y / x))

        if (iki):
            angle += 180

        elif (uc):
            angle += 180

        elif (dort):
            angle += 360

        return (round(angle))

    def rotate(self):
        picture = self.alma.pixmap()
        angle = self.model_2d(40,140)
        transform = QTransform().rotate(90)
        picture = picture.transformed(transform)
        self.alma.setPixmap(picture)

    def timer(self):

        self.timer1 = QTimer()
        self.timer1.setInterval(1000)
        self.timer1.timeout.connect(self.rotate)
        self.timer1.start()

class MyLabel(QLabel):
    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.setPen(QtCore.Qt.black)
        painter.translate(20, 100)
        painter.rotate(-90)
        painter.drawText(0, 0, "hellos")
        painter.end()

if __name__ == "__main__":

    app = QApplication([])
    window = MatplotlibWidget()
    window.show()
    sys.exit(app.exec_())
