from PyQt5.QtWidgets import*

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

from matplotlib.figure import Figure

class Split(QWidget):

    def __init__(self, parent = None):
        QWidget.__init__(self, parent)

        self.canvas = FigureCanvas(Figure(figsize=(3, 3)))

        vertical_layout = QVBoxLayout()
        vertical_layout.addWidget(self.canvas)

        self.canvas.axes = self.canvas.figure.add_subplot(2, 1, 1)
        self.setLayout(vertical_layout)