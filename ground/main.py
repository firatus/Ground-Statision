import io
import sys
import urllib
from PyQt5.uic import loadUi
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import folium
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import (NavigationToolbar2QT as NavigationToolbar)
import cv2
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
import csv
import requests
import pandas as pd
import geopandas as gpd


host = "192.168.4.1" #ESP32 IP
port = 80
istasyon_socket = socket.socket()
#istasyon_socket.connect((host,port))
paket_sirasi = 0
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

pitch = ""
roll = ""
yaw = ""
donus_sayisi = ""
video_info = ""

telemetri = []
son_telemetri = []

#Gsicaklik
xs = []
ys = []

#Gbasinc
xs2 = []
ys2 = []

#GTbasinc
xs3 = []
ys3 = []

#Gyukseklik
xs4 = []
ys4 = []

#Tyukseklik
xs5 = []
ys5 = []

#Gbatarya
xs6 = []
ys6 = []

#Gbinis
xs7 = []
ys7 = []

xs8 = []
ys8 = []




class MatplotlibWidget(QMainWindow):

    def __init__(self):

        QMainWindow.__init__(self)

        loadUi("mainwindow.ui",self)
        self.setWindowTitle("TALIA 4B")



        self.camera = realTimeVideo(self.camera)
        self.camera.start()
        self.map()
        self.gl = Glwidget(self)
        self.gl.setGeometry(1500,400,350,300)
        self.graphGsicaklik()
        self.graphGbasinc()
        self.graphTbasinc()
        self.graphGTyukseklik()
        self.graphGbatarya()
        self.graphGinis()
        self.create_csv()
        #self.timer()


        self.video_sec_bt.clicked.connect(self.video_sec)
        self.gorev2_bt.clicked.connect(self.ozgun_gorev2_yazdir)

        '''self.durdur_bt.clicked.connect(self.command_durdur())

        
        self.buzzer_bt.clicked.connect(self.command_buzzer())
      
        self.ayrilma_bt.clicked.connect(self.command_ayrılma())'''

    #Update Graphs
    def graphGsicaklik(self):
        global xs,paket_sirasi
        global ys,sicaklik

        xs.append(paket_sirasi)
        ys.append(sicaklik)

        x = xs[-5:]

        y = ys[-5:]
        paket_sirasi += 1


        self.Wsicaklik.canvas.axes.plot(x, y,linewidth=2, label="{1}")
        # labellines.labelLines(self.MplWidget.canvas.axes.get_lines())
        self.Wsicaklik.canvas.axes.set_title('Görev Yükü Sıcaklık(°C)')
        self.Wsicaklik.canvas.axes.set_xlabel("Zaman")

        self.Wsicaklik.canvas.draw()

    def graphGbasinc(self):
        global xs2,paket_sirasi
        global ys2,basinc1

        xs2.append(paket_sirasi)
        ys2.append(basinc1)

        x = xs2[-5:]
        y = ys2[-5:]

        paket_sirasi += 1


        self.Wbasinc.canvas.axes.plot(x, y,linewidth=2, label="{1}")
        # labellines.labelLines(self.MplWidget.canvas.axes.get_lines())
        self.Wbasinc.canvas.axes.set_title('Görev Yükü Basınç(p)')
        self.Wbasinc.canvas.axes.set_xlabel("Zaman")
        self.Wbasinc.canvas.draw()

    def graphTbasinc(self):
        global xs3,paket_sirasi
        global ys3,basinc2
        xs3.append(paket_sirasi)
        ys3.append(basinc2)

        x = xs3[-5:]
        y = ys3[-5:]
        paket_sirasi += 1
        self.Wtbasinc.canvas.axes.plot(x, y,linewidth=2, label="{1}")
        # labellines.labelLines(self.MplWidget.canvas.axes.get_lines())
        self.Wtbasinc.canvas.axes.set_title('Taşıyıcı Basınç(p)')
        self.Wtbasinc.canvas.axes.set_xlabel("Zaman")
        self.Wtbasinc.canvas.draw()

    def graphGTyukseklik(self):
        global xs4,paket_sirasi
        global ys4,yukseklik1,yukseklik2

        global xs5
        global ys5

        xs4.append(paket_sirasi)
        ys4.append(yukseklik1)

        xs5.append(paket_sirasi)
        ys5.append(yukseklik2)

        x = xs4[-5:]
        y = xs4[-5:]
        paket_sirasi += 1

        self.Wyukseklik.canvas.axes.plot(x, y, linewidth=2, label="Taşıyıcı")
        x2 = xs5[-5:]
        y2 = xs5[-5:]

        self.Wyukseklik.canvas.axes.plot(x2, y2, linewidth=2, label="Görev Yükü")
        # labellines.labelLines(self.MplWidget.canvas.axes.get_lines())
        self.Wyukseklik.canvas.axes.set_title('Görev Yükü ve Taşıyıcı Yükseklik(m)')
        self.Wyukseklik.canvas.axes.set_xlabel("Zaman")
        self.Wyukseklik.canvas.axes.legend(('Taşıyıcı', 'Görev Yükü'), loc='lower left')

        self.Wyukseklik.canvas.draw()

    def graphGbatarya(self):
        global xs6,paket_sirasi
        global ys6,pil_gerilim

        xs6.append(paket_sirasi)
        ys6.append(pil_gerilim)

        x = xs6[-5:]
        y = ys6[-5:]

        self.Wbatarya.canvas.axes.plot(x, y, linewidth=2, label="{1}")
        # labellines.labelLines(self.MplWidget.canvas.axes.get_lines())
        self.Wbatarya.canvas.axes.set_title('Görev Yükü Batarya Seviyesi(V)')
        self.Wbatarya.canvas.axes.set_xlabel("Zaman")

        self.Wbatarya.canvas.draw()

    def graphGinis(self):
        global xs7
        global paket_sirasi
        global ys7,inis

        xs7.append(paket_sirasi)
        ys7.append(inis)
        print(ys7)
        x = xs7[-5:]
        y = ys7[-5:]
        paket_sirasi += 1

        self.Winis.canvas.axes.plot(x, y, linewidth=2, label="{1}")
        # labellines.labelLines(self.MplWidget.canvas.axes.get_lines())
        self.Winis.canvas.axes.set_title('Görev Yükü Düşey Hız(m/s)')
        self.Winis.canvas.axes.set_xlabel("Zaman")
        self.Winis.canvas.draw()

    def video_sec(self):

        filename = QFileDialog.getOpenFileName(
            caption='Select a video',
            filter='Video File(*.mp4 *.avi *.mkv)'

        )
        print(filename[0])

    def ozgun_gorev2(self):

        global xs8,ys8
        global gps1_alt,gps1_long

        xs8.append(gps1_lat)
        ys8.append(gps1_long)

    def ozgun_gorev2_yazdir(self):
        #xs8
        #
        df = pd.DataFrame(
            {'Latitude': [41.3, 41.07, 41.05, 41.30, 41, 41.2, 41.14, 41.17, 41.185, 41.116],
             'Longitude': [28.66, 28.91, 28.66, 28.18, 29.220, 29, 29.6, 29.2, 28.46, 28.78]})
        fig, ax = plt.subplots()
        ist_map = gpd.read_file("D:\son\Last\istanbul-districts.json")
        ax = ist_map.plot(ax=ax, color='white', edgecolor='black', )
        gdf = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df.Longitude, df.Latitude))
        gdf.plot(ax=ax, color='red', markersize=8)

        plt.plot(df.Longitude, df.Latitude)
        plt.axis('off')
        plt.show()


    def command_baslat(self):
        r = requests.post('192.168.4.1/komut2', data="{'number':1}")

    def command_durdur(self):

        r = requests.post('192.168.4.1/komut2', data="{'number':1}")


    def command_video_sec(self):
        r = requests.post('192.168.4.1/komut2', data="{'number':1}")

    def command_video_goster(self):
        r = requests.post('192.168.4.1/komut2', data="{'number':1}")

    def command_buzzer(self):
        r = requests.post('192.168.4.1/komut2', data="{'number':1}")


    def command_ayrılma(self):
        r = requests.post('192.168.4.1/komut2', data="{'number':1}")


    def map(self):
        self.wmap = QWebEngineView(self.wmap)

        coordinate = (41.0475108, 28.94125)
        self.m = folium.Map(

            zoom_start=15,
            location=coordinate
        )
        folium.Marker([41.0475108, 28.94125]).add_to(self.m)

        data = io.BytesIO()
        self.m.save(data, close_file=False)
        self.wmap.resize(480, 349)
        self.wmap.setHtml(data.getvalue().decode())

    def update_map(self):
        global gps1_lat,gps1_long


        folium.Marker([gps1_lat, gps1_long]).add_to(self.m)

        data = io.BytesIO()
        self.m.save(data, close_file=False)
        self.wmapsetHtml(data.getvalue().decode())

    #6graph 1map 1data
    def timer(self):
        
        self.timer = QTimer()
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.getdata)
        self.timer.start()

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

        self.timer8 = QTimer()
        self.timer8.setInterval(1000)
        self.timer8.timeout.connect(self.graphGTyukseklik)
        self.timer8.start()

        self.timer8 = QTimer()
        self.timer8.setInterval(10000)
        self.timer8.timeout.connect(self.ozgun_gorev2)
        self.timer8.start()

        '''self.timer2 = QTimer()
        self.timer2.setInterval(1000)
        self.timer2.timeout.connect(self.updateGL)
        self.timer2.start()'''

    #Baslama butonu
    def getdata(self):

        global takim_no,paket_no,saat,basinc1,basinc2,yukseklik1,yukseklik2,irtifa,inis,sicaklik,pil_gerilim,xy,ys
        global gps1_alt,gps1_lat,gps1_long,gps2_alt,gps2_lat,gps2_long,uydu_status,pitch,roll,yaw,donus_sayisi,video_info,telemetri,son_telemetri

        key = "0"
        #istasyon_socket.send(key.encode())

        #telemetri paketinden gelen verileri değişkene ata
        # map,graph,3D verilerini değişkene ver
        #telemetri = istasyon_socket.recv(1024)
        resp = requests.get("http://192.168.4.1/data")
        print(resp.text)
        if resp.text == '['']':
            exit()
        #telemetri = resp.split(',')
        #telemetri= "1111,1,12.00,5,10,5,10,20,10,30.0,15,41.041964,28.939417,10,20,20,20,HAVADA,10,20,30,1,IYI"
        #son_telemetri = telemetri[0:22]
        text = resp.text[:22]
        telemetri = resp.text.split("!")
        print(telemetri)
        son_telemetri = telemetri
        print(son_telemetri)
        self.write_csv(son_telemetri)
        takim_no = son_telemetri[0]
        paket_no = int(son_telemetri[1])
        saat =  son_telemetri[2]
        basinc1 = float(son_telemetri[3])
        basinc2 = float(son_telemetri[4])
        yukseklik1 = float(son_telemetri[5])
        yukseklik2 = float(son_telemetri[6])
        irtifa = float(son_telemetri[7])

        inis = float(son_telemetri[8])
        sicaklik = float(son_telemetri[9])

        pil_gerilim = float(son_telemetri[10])
        gps1_alt = float(son_telemetri[11])
        gps1_long = float(son_telemetri[12])
        gps1_lat = float(son_telemetri[13])
        gps2_alt = float(son_telemetri[14])
        gps2_long = float(son_telemetri[15])
        gps2_lat = float(son_telemetri[16])
        uydu_status = (son_telemetri[17])
        pitch = float(son_telemetri[18])
        roll = float(son_telemetri[19])
        yaw = float(son_telemetri[20])
        self.gl.setRotX(pitch)
        self.gl.setRotX(roll)
        self.gl.setRotX(yaw)

        donus_sayisi = float(son_telemetri[21])
        video_info = (son_telemetri[22])


        self.takim_no_label.setText(str(son_telemetri[0]))
        self.paket_no_label.setText((son_telemetri[1]))
        self.saat_label.setText(str(son_telemetri[2]))
        self.basinc1_label.setText(str(son_telemetri[3]))
        self.basinc2_label.setText(str(son_telemetri[4]))
        self.yukseklik_label.setText(str(son_telemetri[5]))
        self.yukseklik2_label.setText(str(son_telemetri[6]))

        self.irtifa_label.setText(str(son_telemetri[7]))
        self.inis_hiz_label.setText(str(son_telemetri[8]))
        self.sicaklik_label.setText(str(son_telemetri[9]))
        self.pil_gerilim_label.setText(str(son_telemetri[10]))

        self.gps1_lat_label.setText(str(son_telemetri[11]))
        self.gps1_long_label.setText(str(son_telemetri[12]))
        self.gps1_alt_label.setText(str(son_telemetri[13]))

        self.gps2_lat_label.setText(str(son_telemetri[14]))
        self.gps2_long_label.setText(str(son_telemetri[15]))
        self.gps2_alt_label.setText(str(son_telemetri[16]))


        self.uydu_status_label.setText(str(son_telemetri[17]))
        self.pitch_label.setText(str(son_telemetri[18]))
        self.roll_label.setText(str(son_telemetri[19]))
        self.yaw_label.setText(str(son_telemetri[20]))
        self.donus_sayisi_label.setText(str(son_telemetri[21]))
        self.video_info_label.setText(str(son_telemetri[22]))


    def write_csv(self,son_telemetri):

        with open('deneme.csv', 'a') as f:
            writer = csv.writer(f)

            writer.writerow(son_telemetri)

    def create_csv(self):
        with open('deneme.csv', 'w') as f:
            writer = csv.writer(f)
            writer.writerow(
                ['TAKIM NO', 'PAKET NUMARASI', 'GONDERME SAATI', 'BASINC1', 'BASINC2', 'YUKSEKLIK1', 'YUKSEKLIK2',
                 'IRTIFA FARKI', 'INIS HIZI', 'SICAKLIK', 'PIL GERILIMI', 'GPS1 LATITUDE', 'GPS1 LONGTITUDE',
                 'GPS1 ALTITUDE', 'GPS2 LATITUDE', 'GPS2 LONGTITUDE', 'GPS2 ALTITUDE', 'UYDU STATUSU', 'PITCH', 'ROLL',
                 'YAW', 'DONUS SAYISI', 'VIDEO AKTARIM BILGISI'])



class Glwidget(QtOpenGL.QGLWidget):

    def __init__(self, parent=None):
	    self.parent = parent
	    QtOpenGL.QGLWidget.__init__(self, parent)



    def initializeGL(self):
        self.qglClearColor(QtGui.QColor(0, 0, 255))  # initialize the screen to blue
        gl.glEnable(gl.GL_DEPTH_TEST)  # enable depth testing

        self.initGeometry()
        self.rotX = 30.0
        self.rotY = 90.0
        self.rotZ = 0


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







class realTimeVideo(QThread):
    def __init__(self, label):
        super(realTimeVideo, self).__init__()
        self.label = label

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
            cv2.destroyAllWindows()

    '''def run(self):

        while True:
            imgResponse = urllib.request.urlopen('http://172.20.10.13/capture?')
            imgNp = np.array(bytearray(imgResponse.read()), dtype=np.uint8)
            frame = cv2.imdecode(imgNp, -1)
            fourcc = cv2.VideoWriter_fourcc(*'DIVX')
            self.out = cv2.VideoWriter('kayit.avi', fourcc, 25.0, (462, 331))
            self.out.write(frame)
            image = QImage(frame, frame.shape[1], frame.shape[0], frame.strides[0], QImage.Format_RGB888)
            self.label.setPixmap(QPixmap.fromImage(image))
            key = cv2.waitKey(25)
            if key == ord(('q')):
                break
        cv2.destroyAllWindows()'''





if __name__ == "__main__":
    app = QApplication([])
    window = MatplotlibWidget()
    window.show()
    sys.exit(app.exec_())
