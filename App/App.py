import sys
import time

import numpy as np

import pandas as pd

from matplotlib.backends.qt_compat import QtWidgets
from matplotlib.backends.backend_qtagg import (
    FigureCanvas, NavigationToolbar2QT as NavigationToolbar)
from matplotlib.figure import Figure


class ApplicationWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self._main = QtWidgets.QWidget()
        self.setCentralWidget(self._main)
        layout = QtWidgets.QVBoxLayout(self._main)

        self.xs = []
        self.ys = []

        dynamic_canvas = FigureCanvas(Figure(figsize=(5, 3)))
        layout.addWidget(dynamic_canvas)
        layout.addWidget(NavigationToolbar(dynamic_canvas, self))

        self._dynamic_ax = dynamic_canvas.figure.subplots()
        self._line, = None, 
        self._points, = self._dynamic_ax.plot(self.xs, self.ys, '.')
        self.cid = self._points.figure.canvas.mpl_connect('button_press_event', self)
        self._import_data("App/data/test.xlsx")

    def _update_canvas(self):
        # TODO How to solve differential equations???
        a = None
        b = None
        p = np.poly1d([a,b])

    def __call__(self, event):
        print('click', event)
        if event.inaxes!=self._points.axes: return
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
        

    def _import_data(self, path):
        df = pd.read_excel(path,header=0)
        print(df)
        self.xs = df.x.to_list()
        self.ys = df.y.to_list()
        self._dynamic_ax.set_xlim(min(self.xs), max(self.xs))
        self._dynamic_ax.set_ylim(min(self.ys), max(self.ys))
        self._points.set_data(self.xs, self.ys)
        self._points.figure.canvas.draw()

    def _export_data(self, path):
        df = pd.DataFrame({'x':self.xs, 'y':self.ys})
        df.to_excel(path)



if __name__ == "__main__":
    qapp = QtWidgets.QApplication.instance()
    if not qapp:
        qapp = QtWidgets.QApplication(sys.argv)

    app = ApplicationWindow()
    app.show()
    app.activateWindow()
    app.raise_()
    qapp.exec()

