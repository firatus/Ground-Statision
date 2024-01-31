import io
import folium
from PyQt5.QtWidgets import*
from PyQt5.QtWebEngineWidgets import QWebEngineView
from ground import gl
from ground import son_telemetri
class Wmap(QWidget):

    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        coordinate = (41.0475108, 28.94125)
        self.m = folium.Map(
            width=480, height=350,
        	zoom_start=15,
        	location=coordinate
        )
        folium.Marker([41.0475108, 28.94125]).add_to(self.m)
        # save map data to data object
        data = io.BytesIO()
        self.m.save(data, close_file=False)

        self.webView = QWebEngineView()
        self.webView.setHtml(data.getvalue().decode())
        self.layout.addWidget(self.webView)


