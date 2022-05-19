import sys

import numpy as np

import pandas as pd

from modules.LSM import LSM

from matplotlib.backends.qt_compat import QtWidgets
from matplotlib.backends.backend_qtagg import (FigureCanvas, NavigationToolbar2QT as NavigationToolbar)
from matplotlib.figure import Figure
from PyQt6 import QtGui


class ApplicationWindow(QtWidgets.QMainWindow):
    """
    docstring
    """

    def __init__(self):
        super().__init__()
        self._main = QtWidgets.QWidget()
        self.setWindowTitle("Metoda Najmniejszych Kwadratów")
        self.setWindowIcon(QtGui.QIcon('App/data/images/icon.png'))
        self.setCentralWidget(self._main)
        layout = QtWidgets.QVBoxLayout(self._main)

        self.xs = []
        self.ys = []

        dynamic_canvas = FigureCanvas(Figure(figsize=(5, 3)))
        self.equation_label = QtWidgets.QLabel()
        layout.addWidget(self.equation_label)
        layout.addWidget(dynamic_canvas)
        layout.addWidget(NavigationToolbar(dynamic_canvas, self))
        self.poly_conf_lay = QtWidgets.QHBoxLayout()
        poly_deg_label = QtWidgets.QLabel()
        poly_deg_label.setText("Wybierz stopień wielomianu:")
        self.poly_conf_lay.addWidget(poly_deg_label)
        self.select_poly_deg = QtWidgets.QSpinBox()
        self.select_poly_deg.setMinimum(1)
        self.select_poly_deg.valueChanged.connect(self._update_canvas)
        self.poly_conf_lay.addWidget(self.select_poly_deg)
        layout.addLayout(self.poly_conf_lay)
        buttons_layout = QtWidgets.QHBoxLayout()
        import_button = QtWidgets.QPushButton()
        import_button.setText("Importuj dane")
        import_button.clicked.connect(self._import_data)
        export_button = QtWidgets.QPushButton()
        export_button.setText("Eksportuj dane")
        export_button.clicked.connect(self._export_data)
        buttons_layout.addWidget(import_button)
        buttons_layout.addWidget(export_button)
        layout.addLayout(buttons_layout)
        self._dynamic_ax = dynamic_canvas.figure.subplots()
        self._line, = None,
        self._points, = self._dynamic_ax.plot(self.xs, self.ys, '.')
        self.cid = self._points.figure.canvas.mpl_connect('button_press_event', self)

    def _update_canvas(self):
        self.lsm = LSM(self.xs, self.ys, self.select_poly_deg.value())
        self.lsm.create_plot_data()
        if self._line is None:
            self._line, = self._dynamic_ax.plot(self.lsm.x_output, self.lsm.y_output)
        else:
            self._line.set_data(self.lsm.x_output, self.lsm.y_output)
            self._line.figure.canvas.draw()

        self.equation_label.setText(self.lsm.__repr__())

    def __call__(self, event):
        print('click', event)
        if event.inaxes != self._points.axes:
            return
        if event.button == 1:
            self.xs.append(np.round(event.xdata, 3))
            self.ys.append(np.round(event.ydata, 3))
        elif event.button == 3:
            for i in range(len(self.xs)):
                if self.xs[i] == np.round(event.xdata, 3) and self.ys[i] == np.round(event.ydata, 3):
                    self.xs.pop(i)
                    self.ys.pop(i)
                    break
        self._points.set_data(self.xs, self.ys)
        self._points.figure.canvas.draw()
        self._update_canvas()

    def _import_data(self):
        file_name = QtWidgets.QFileDialog.getOpenFileName(self, 'Select file to import...', 'c://','*.xlsx')
        if file_name == '': 
            return

        try:
            df = pd.read_excel(file_name[0], header=0)
        except FileNotFoundError:
            return
        self.xs = df.x.to_list()
        self.ys = df.y.to_list()
        self._dynamic_ax.set_xlim(min(self.xs), max(self.xs))
        self._dynamic_ax.set_ylim(min(self.ys), max(self.ys))
        self._points.set_data(self.xs, self.ys)
        self._points.figure.canvas.draw()
        self._update_canvas()

    def _export_data(self):
        file_path = str(QtWidgets.QFileDialog.getExistingDirectory(self, "Select Directory"))+"/results.xlsx"
        if file_path == '': 
            return
        df = pd.DataFrame({'x': self.xs, 'y': self.ys})
        df["poly degree"] = [self.lsm.polynomial.c] + [None for i in range(len(self.xs)-1)] 
        print(df)
        df.to_excel(file_path)


if __name__ == "__main__":
    qapp = QtWidgets.QApplication.instance()
    if not qapp:
        qapp = QtWidgets.QApplication(sys.argv)

    app = ApplicationWindow()
    app.show()
    app.activateWindow()
    app.raise_()
    qapp.exec()
