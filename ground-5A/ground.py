import io
import sys
import urllib
from PyQt5.uic import loadUi
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtLocation import *
import folium
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import (NavigationToolbar2QT as NavigationToolbar)
import cv2
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import math

import socket
import numpy as np
import random
from PyQt5.QtWebEngineWidgets import QWebEngineView

from PyQt5 import QtOpenGL  # provides QGLWidget, a special OpenGL QWidget
from OpenGL import GLU
from OpenGL.arrays import vbo
import OpenGL.GL as gl  # python wrapping of OpenGL
from OpenGL import GLU  # OpenGL Utility Library, extends OpenGL functionality
from PyQt5 import QtGui  # extends QtCore with GUI functionality
from PyQt5.QtWidgets import *
from PyQt5 import QtCore
import csv
import requests
import pandas as pd



hata_kod = "11111"
paket_sirasi = 0
dene = 0
takim_no = ""
paket_no = ""
saat = ""
basinc1 = ""
basinc2 = ""
yukseklik1 = ""
yukseklik2 = ""
irtifa = ""
inis = ""
sicaklik = ""
pil_gerilim = ""

gps1_lat = ""
gps1_alt = ""
gps1_long = ""

gps2_lat = ""
gps2_alt = ""
gps2_long = ""
uydu_status = ""
pitch = "0"
roll = "0"
yaw= "0"


donus_sayisi = ""
video_info = ""

file_name = ""

map_locations = []

telemetri = []
son_telemetri = []

# Gsicaklik
xs = []
ys = []

# Gbasinc
xs2 = []
ys2 = []

# GTbasinc
xs3 = []
ys3 = []

# Gyukseklik
xs4 = []
ys4 = []

# Tyukseklik
xs5 = []
ys5 = []

# Gbatarya
xs6 = []
ys6 = []

# Gbinis
xs7 = []
ys7 = []

xs8 = []
ys8 = []

class Model3d(QtOpenGL.QGLWidget):



    def __init__(self, parent=None):
        self.parent = parent
        QtOpenGL.QGLWidget.__init__(self, parent)

    def initializeGL(self):
        self.qglClearColor(QtGui.QColor(0, 0, 0))  # initialize the screen to blue
        gl.glEnable(gl.GL_DEPTH_TEST)  # enable depth testing

        self.initGeometry()
        self.rotX = 0.0
        self.rotY = 0.0
        self.rotZ = 0.0


    def resizeGL(self, width, height):
        gl.glViewport(0, 0, width, height)
        gl.glMatrixMode(gl.GL_PROJECTION)
        gl.glLoadIdentity()
        aspect = width / float(height)

        GLU.gluPerspective(45.0, aspect, 1.0, 100.0)
        gl.glMatrixMode(gl.GL_MODELVIEW)

    def paintGL(self):
        gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)

        gl.glPushMatrix()  # push the current matrix to the current stack

        gl.glTranslate(0.0, 0.0, -50.0)  # third, translate cube to specified depth
        gl.glScale(20.0, 20.0, 20.0)  # second, scale cube
        gl.glRotate(self.rotX, 1.0, 0.0, 0.0)
        gl.glRotate(self.rotY, 0.0, 1.0, 0.0)
        gl.glRotate(self.rotZ, 0.0, 0.0, 1.0)
        gl.glTranslate(-0.5, -0.5, -0.5)  # first, translate cube center to origin

        gl.glEnableClientState(gl.GL_VERTEX_ARRAY)
        gl.glEnableClientState(gl.GL_COLOR_ARRAY)

        gl.glVertexPointer(3, gl.GL_FLOAT, 0, self.vertVBO)
        gl.glColorPointer(3, gl.GL_FLOAT, 0, self.colorVBO)

        gl.glDrawElements(gl.GL_QUADS, len(self.cubeIdxArray), gl.GL_UNSIGNED_INT, self.cubeIdxArray)

        gl.glDisableClientState(gl.GL_VERTEX_ARRAY)
        gl.glDisableClientState(gl.GL_COLOR_ARRAY)

        gl.glPopMatrix()  # restore the previous modelview matrix

    def initGeometry(self):
        self.cubeVtxArray = np.array(
            [[0.0, 0.0, 0.0],
             [1.0, 0.0, 0.0],
             [1.0, 1.0, 0.0],
             [0.0, 1.0, 0.0],
             [0.0, 0.0, 1.0],
             [1.0, 0.0, 1.0],
             [1.0, 1.0, 1.0],
             [0.0, 1.0, 1.0]])
        self.vertVBO = vbo.VBO(np.reshape(self.cubeVtxArray,
                                          (1, -1)).astype(np.float32))
        self.vertVBO.bind()

        self.cubeClrArray = np.array(
            [[0.0, 0.0, 0.0],
             [1.0, 0.0, 0.0],
             [1.0, 1.0, 0.0],
             [0.0, 1.0, 0.0],
             [0.0, 0.0, 1.0],
             [1.0, 0.0, 1.0],
             [1.0, 1.0, 1.0],
             [0.0, 1.0, 1.0]])
        self.colorVBO = vbo.VBO(np.reshape(self.cubeClrArray,
                                           (1, -1)).astype(np.float32))
        self.colorVBO.bind()

        self.cubeIdxArray = np.array(
            [0, 1, 2, 3,
             3, 2, 6, 7,
             1, 0, 4, 5,
             2, 1, 5, 6,
             0, 3, 7, 4,
             7, 6, 5, 4])

    def setRotX(self, val):
        self.rotX = np.pi * val

    def setRotY(self, val):
        self.rotY = np.pi * val

    def setRotZ(self, val):
        self.rotZ = np.pi * val


class MatplotlibWidget(QMainWindow):

    def __init__(self):
        QMainWindow.__init__(self)

        loadUi("kopya.ui", self)


        self.setWindowTitle("TALIA 5A")

        self.camera = realTimeVideo(self.camera)
        self.camera.start()
        self.map()

        self.gl = Model3d(self)
        self.gl.setGeometry(1680,500,450,400)


        self.create_csv()
        self.change_color()


        self.video_sec_bt.clicked.connect(self.video_sec)

        # self.show_3d()
        self.start_bt.clicked.connect(self.timer)
        self.video_bt.clicked.connect(self.video_gonder)

        self.system_start_bt.clicked.connect(self.system_start)
        self.system_stop_bt.clicked.connect(self.system_stop)
        self.ayrilmabt.clicked.connect(self.command_ayrilma)
        self.showMaximized()


    # Update Graphs
    def graphGsicaklik(self):
        global xs, paket_sirasi
        global ys, sicaklik, dene

        xs.append(paket_sirasi)
        ys.append(sicaklik)

        paket_sirasi += 1

        xs = xs[-5:]
        ys = ys[-5:]

        self.Wsicaklik.canvas.axes.clear()

        self.Wsicaklik.canvas.axes.plot(xs, ys, linewidth=4, color="orange")
        self.Wsicaklik.canvas.axes.set_title('Görev Yükü Sıcaklık(°C)')
        self.Wsicaklik.canvas.axes.set_xlabel("Zaman")
        self.Wsicaklik.canvas.draw()

    def graphGbasinc(self):
        global xs2, paket_sirasi
        global ys2, basinc1

        xs2.append(paket_sirasi)
        ys2.append(basinc1)

        xs2 = xs2[-5:]
        ys2 = ys2[-5:]
        paket_sirasi += 1

        self.Wbasinc.canvas.axes.clear()

        self.Wbasinc.canvas.axes.plot(xs2, ys2, linewidth=4, color="orange")
        # labellines.labelLines(self.MplWidget.canvas.axes.get_lines())
        self.Wbasinc.canvas.axes.set_title('Görev Yükü Basınç(p)')
        self.Wbasinc.canvas.axes.set_xlabel("Zaman")
        self.Wbasinc.canvas.draw()

    def graphTbasinc(self):
        global xs3, paket_sirasi
        global ys3, basinc2
        xs3.append(paket_sirasi)
        ys3.append(basinc2)

        xs3 = xs3[-5:]
        ys3 = ys3[-5:]
        paket_sirasi += 1

        self.Wtbasinc.canvas.axes.clear()
        self.Wtbasinc.canvas.axes.plot(xs3, ys3, linewidth=4, color="orange")
        # labellines.labelLines(self.MplWidget.canvas.axes.get_lines())
        self.Wtbasinc.canvas.axes.set_title('Taşıyıcı Basınç(p)')
        self.Wtbasinc.canvas.axes.set_xlabel("Zaman")
        self.Wtbasinc.canvas.draw()

    '''def graphyukseklikG(self):
        global xs4, paket_sirasi
        global ys4, yukseklik1, yukseklik2

        global xs5
        global ys5

        xs4.append(paket_sirasi)
        ys4.append(yukseklik1)

        xs4 = xs4[-5:]
        ys4 = ys4[-5:]

        xs5.append(paket_sirasi)
        ys5.append(yukseklik2)

        xs5 = xs5[-5:]
        ys5 = ys5[-5:]

        paket_sirasi += 1



        #self.Wyukseklik.canvas.axes.clear()


        self.Wyukseklik.canvas.axes.plot(xs4, ys4, linewidth=4, label="Görev Yükü", color="blue")

        self.Wyukseklik.canvas.axes.plot(xs5, ys5, linewidth=4, label="Taşıyıcı", color="red")

        self.Wyukseklik.canvas.axes.set_title('Görev Yükü Yükseklik(m)')
        self.Wyukseklik.canvas.axes.set_xlabel("Zaman")
        #self.Wyukseklik.canvas.axes.legend(('Taşıyıcı', 'Görev Yükü'), loc='lower left')

        self.Wyukseklik.canvas.draw()'''

    def graphYukseklikG(self):
        global xs4, paket_sirasi
        global ys4, yukseklik1

        xs4.append(paket_sirasi)
        ys4.append(yukseklik1)


        paket_sirasi += 1

        xs4 = xs4[-5:]
        ys4 = ys4[-5:]

        self.WyukseklikG.canvas.axes.clear()

        self.WyukseklikG.canvas.axes.plot(xs4, ys4, linewidth=4, color="blue")
        # labellines.labelLines(self.MplWidget.canvas.axes.get_lines())
        self.WyukseklikG.canvas.axes.set_title('Görev Yükü Yükseklik(m)')
        self.WyukseklikG.canvas.axes.set_xlabel("Zaman")
        self.WyukseklikG.canvas.draw()


    def graphYukseklikT(self):
        global xs5, paket_sirasi
        global ys5, yukseklik1

        xs5.append(paket_sirasi)
        ys5.append(yukseklik1)

        paket_sirasi += 1

        xs5 = xs5[-5:]
        ys5 = ys5[-5:]

        self.WyukseklikT.canvas.axes.clear()

        self.WyukseklikT.canvas.axes.plot(xs5, ys5, linewidth=4, color="red")
        # labellines.labelLines(self.MplWidget.canvas.axes.get_lines())
        self.WyukseklikT.canvas.axes.set_title('Taşıyıcı Yükü Yükseklik(m)')
        self.WyukseklikT.canvas.axes.set_xlabel("Zaman")
        self.WyukseklikT.canvas.draw()


    def graphGbatarya(self):
        global xs6, paket_sirasi
        global ys6, pil_gerilim

        xs6.append(paket_sirasi)
        ys6.append(pil_gerilim)

        xs6 = xs6[-5:]
        ys6 = ys6[-5:]
        self.Wbatarya.canvas.axes.clear()

        self.Wbatarya.canvas.axes.plot(xs6, ys6, linewidth=4, color="orange")
        # labellines.labelLines(self.MplWidget.canvas.axes.get_lines())
        self.Wbatarya.canvas.axes.set_title('Görev Yükü Batarya Seviyesi(V)')
        self.Wbatarya.canvas.axes.set_xlabel("Zaman")

        self.Wbatarya.canvas.draw()

    def graphGinis(self):
        global xs7
        global paket_sirasi
        global ys7, inis

        xs7.append(paket_sirasi)
        ys7.append(inis)

        xs7 = xs7[-5:]
        ys7 = ys7[-5:]

        paket_sirasi += 1

        self.Winis.canvas.axes.clear()

        self.Winis.canvas.axes.plot(xs7, ys7, linewidth=4, color="orange")
        # labellines.labelLines(self.MplWidget.canvas.axes.get_lines())
        self.Winis.canvas.axes.set_title('Görev Yükü Düşey Hız(m/s)')
        self.Winis.canvas.axes.set_xlabel("Zaman")
        self.Winis.canvas.draw()




    def video_sec(self):
        global file_name
        filename = QFileDialog.getOpenFileName(
            caption='Select a video',
            filter='Video File(*.mp4 *.avi *.mkv)'

        )
        file_name = (filename[0])

    def video_gonder(self):
        global file_name
        try:
            url = "http://192.168.4.1/file"
            data = {'title': 'metadata', 'timeDuration': 120}
            mp4_f = open(str(file_name), 'rb')
            files = {'messageFile': mp4_f}

            req = requests.post(url, files=files, json=data)
            print(req.status_code)

        except:
            print("Bağlantı yok")



    def command_ayrilma(self):
        try:
            r = requests.post('http://192.168.4.1/command', data="9")
        except:
            print("Ayrılma Gerçekleşmedi!!")


    def system_start(self):
        try:
            requests.post('http://192.168.4.1/start')

            requests.post('http://192.168.4.1/command', data="p")

            self.timer()
        except:
            print("Bağlantı koptu")
    def system_stop(self):
        try:
            requests.post('http://192.168.4.1/stop')
        except:
            print("Bağlantı koptu")

    def map(self):
        global gps1_lat, gps1_long, map_locations

        self.wmap = QWebEngineView(self.wmap)
        gps1_lat = 41.0475108
        gps1_long = 28.94125
        coordinate = (gps1_lat, gps1_long)
        locations = []

        self.base_map = folium.Map(

            zoom_start=15,
            location=coordinate
        )

        text_old = "Last Satellite Location"
        text_live = "Live Satellite Location"
        old_locations = folium.FeatureGroup(name="old_location").add_to(self.base_map)
        old_locations.add_child(folium.Marker([gps1_lat, gps1_long], tooltip=text_old))

        live_locations = folium.FeatureGroup(name="live_location").add_to(self.base_map)
        live_locations.add_child(folium.Marker([41.038284, 28.970329], tooltip=text_live))

        folium.LayerControl().add_to(self.base_map)

        data = io.BytesIO()
        self.base_map.save(data, close_file=False)
        self.wmap.resize(480, 349)
        self.wmap.setHtml(data.getvalue().decode())

    # 6graph 1map 1data
    def timer(self):

        self.timer1 = QTimer()
        self.timer1.setInterval(1000)
        self.timer1.timeout.connect(self.getdata)
        self.timer1.start()


        self.timer3 = QTimer()
        self.timer3.setInterval(1000)
        self.timer3.timeout.connect(self.graphGbasinc)
        self.timer3.start()

        self.timer4 = QTimer()
        self.timer4.setInterval(1000)
        self.timer4.timeout.connect(self.graphTbasinc)
        self.timer4.start()

        self.timer5 = QTimer()
        self.timer5.setInterval(1000)
        self.timer5.timeout.connect(self.graphGbatarya)
        self.timer5.start()

        self.timer6 = QTimer()
        self.timer6.setInterval(1000)
        self.timer6.timeout.connect(self.graphGinis)
        self.timer6.start()

        self.timer7 = QTimer()
        self.timer7.setInterval(1000)
        self.timer7.timeout.connect(self.graphGsicaklik)
        self.timer7.start()
        '''
        self.timer10 = QTimer()
        self.timer10.setInterval(1000)
        self.timer10.timeout.connect(self.graphGTyukseklik)
        self.timer10.start()'''


        '''
        self.timer8 = QTimer()
        self.timer8.setInterval(1000)
        self.timer8.timeout.connect(self.map)
        self.timer8.start()
        '''


        self.timer2 = QTimer()
        self.timer2.setInterval(1000)
        self.timer2.timeout.connect(self.gl.updateGL)
        self.timer2.start()

        self.timer20 = QTimer()
        self.timer20.setInterval(1000)
        self.timer20.timeout.connect(self.graphYukseklikG)
        self.timer20.start()

        self.timer30 = QTimer()
        self.timer30.setInterval(1000)
        self.timer30.timeout.connect(self.graphYukseklikT)
        self.timer30.start()

        self.timer40 = QTimer()
        self.timer40.setInterval(1000)
        self.timer40.timeout.connect(self.change_color)
        self.timer40.start()



        self.timer7 = QTimer()
        self.timer7.setInterval(1000)
        self.timer7.timeout.connect(self.graphGsicaklik)
        self.timer7.start()


    def getdata(self):
        global takim_no, paket_no, saat, basinc1, basinc2, yukseklik1, yukseklik2, irtifa, inis, sicaklik, pil_gerilim, xy, ys
        global pitch,roll,yawgps1_alt, gps1_lat, gps1_long, gps2_alt, gps2_lat, gps2_long, uydu_status, donus_sayisi, video_info, telemetri, son_telemetri, hata_kod

        try:

            resp = requests.get("http://192.168.4.1/data")
            telemetri = resp.text

            son_telemetri = resp.text.split(";")

            for i in range(len(son_telemetri)):

                if son_telemetri[i] == "-":
                    son_telemetri[i] = "0"

            self.write_csv(son_telemetri)
            print(son_telemetri)
            paket_no = int(son_telemetri[0])
            uydu_status = (son_telemetri[1])

            hata_kod = son_telemetri[2]

            saat = son_telemetri[3]

            basinc1 = float(son_telemetri[4])
            basinc2 = float(son_telemetri[5])
            yukseklik1 = float(son_telemetri[6])
            yukseklik2 = float(son_telemetri[7])
            irtifa = float(son_telemetri[8])

            inis = float(son_telemetri[9])
            sicaklik = float(son_telemetri[10])

            pil_gerilim = float(son_telemetri[11])
            gps1_lat = float(son_telemetri[12])
            gps1_long = float(son_telemetri[13])
            gps1_alt = float(son_telemetri[14])

            pitch = float(son_telemetri[15])
            yaw = float(son_telemetri[16])
            rol = float(son_telemetri[17])
            takim_no = son_telemetri[18]



            self.hata_kodu.setText(str(hata_kod))
            self.takim_no_label.setText(str(takim_no))
            self.paket_no_label.setText(str(paket_no))
            self.saat_label.setText(str(saat))
            self.basinc1_label.setText(str(basinc1))
            self.basinc2_label.setText(str(basinc2))
            self.yukseklik_label.setText(str(yukseklik1))
            self.yukseklik2_label.setText(str(yukseklik2))

            self.irtifa_label.setText(str(irtifa))
            self.inis_hiz_label.setText(str(inis))
            self.sicaklik_label.setText(str(sicaklik))
            self.pil_gerilim_label.setText(str(pil_gerilim))

            self.gps1_lat_label.setText(str(gps1_lat))
            self.gps1_long_label.setText(str(gps1_long))
            self.gps1_alt_label.setText(str(gps1_alt))

            self.uydu_status_label.setText(str(uydu_status))
            self.pitch_label.setText(str(pitch))
            self.roll_label.setText(str(roll))
            self.yaw_label.setText(str(yaw))

            self.gl.setRotX(pitch)
            self.gl.setRotY(yaw)
            self.gl.setRotZ(roll)

        except:
            print("Bağlantı Koptu")

    def write_csv(self, son_telemetri):
        with open('deneme.csv', 'a') as f:
            writer = csv.writer(f)

            writer.writerow(son_telemetri)

    def create_csv(self):
        with open('deneme.csv', 'w') as f:
            writer = csv.writer(f)
            writer.writerow(
                ['PAKET NUMARASI', 'UYDU STATUSU', 'HATA KODU', 'GONDERME SAATI', 'BASINC1', 'BASINC2', 'YUKSEKLIK1',
                 'YUKSEKLIK2',
                 'IRTIFA FARKI', 'INIS HIZI', 'SICAKLIK', 'PIL GERILIMI', 'GPS1 LATITUDE', 'GPS1 LONGTITUDE',
                 'GPS1 ALTITUDE', 'PITCH', 'ROLL',
                 'YAW', 'TAKIM NO']
            )

    def change_color(self):

        global hata_kod
        sayi = str(hata_kod)
        print(sayi)

        adim = 0

        for i in sayi:

            if (int(i) == 1):
                self.alarm_table.item(0, adim).setBackground(QtGui.QColor('red'))
                adim += 1

            else:

                self.alarm_table.item(0, adim).setBackground(QtGui.QColor('green'))
                adim += 1






class realTimeVideo(QThread):
    def __init__(self, label):
        super(realTimeVideo, self).__init__()
        self.label = label

    '''
    def run(self):

        self.cap = cv2.VideoCapture(0)

        fourcc = cv2.VideoWriter_fourcc(*'DIVX')
        self.out = cv2.VideoWriter('kayit.avi', fourcc, 25.0, (462, 331))

        while (self.cap.isOpened()):
            ret, frame = self.cap.read()
            if ret == True:
                frame = cv2.flip(frame, 180)
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

                frame = cv2.resize(frame, (462, 331))
                self.out.write(frame)

                image = QImage(frame, frame.shape[1], frame.shape[0], frame.strides[0], QImage.Format_RGB888)
                self.label.setPixmap(QPixmap.fromImage(image))
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            else:
                break
            cv2.destroyAllWindows()'''

    def run(self):

        fourcc = cv2.VideoWriter_fourcc(*'DIVX')
        self.out = cv2.VideoWriter('kayit.avi', fourcc, 25.0, (462, 331))

        try:
            while True:

                imgResponse = urllib.request.urlopen('http://192.168.4.1/picture')  # http response al

                imgNp = np.array(bytearray(imgResponse.read()),
                                 dtype=np.uint8)  # isteği byte formata çeviriyoruz kolayca aktarılması için

                frame = cv2.imdecode(imgNp, cv2.IMREAD_COLOR)  # bytearrayi image formata dönüştürüyoruz
                frame = cv2.resize(frame, (462, 331))

                self.out.write(frame)
                image = QImage(frame, frame.shape[1], frame.shape[0], frame.strides[0],
                               QImage.Format_RGB888)  # yükseklik,genişlik,strides
                self.label.setPixmap(QPixmap.fromImage(
                    image))  # Görüntüyü gösterbilir hale getirmek için Qpickmax sınıfı kullanıyoruz ve label üzerinden gösteriyoruz.
                key = cv2.waitKey(25)
                if key == ord(('q')):
                    break
            cv2.destroyAllWindows()

            self.out.release()
        except:
            print("Kamera Bağlantısı Koptu")



if __name__ == "__main__":
    app = QApplication([])
    window = MatplotlibWidget()
    window.show()
    sys.exit(app.exec_())
