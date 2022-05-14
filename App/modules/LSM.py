from dataclasses import dataclass, field

import numpy as np


@dataclass
class LSM:
    Xs: field(default_factory=list)
    Ys: field(default_factory=list)
    poly_degree: int
    X_matrix = None
    Y_matrix = None
    a = None

    def create_X_matrix(self) -> np.ndarray:
        self.X_matrix = np.zeros((len(self.Xs), self.poly_degree + 1))
        for i in range(self.poly_degree + 1):
            self.X_matrix[:, -(i+1)] = np.array(self.Xs) ** i
        return self.X_matrix

    def create_Y_matrix(self):
        self.Y_matrix = np.array(self.Ys)
        return self.Y_matrix

    def check_connditions(self):
        return True

    def calculate(self):
        self.a = np.linalg.inv(self.X_matrix.T @ self.X_matrix) @ self.X_matrix.T @ self.Y_matrix
        return self.a

    def create_polynomial(self):
        self.polynomial = np.poly1d(self.a)

    def _crate_plot_data(self):
        self.create_X_matrix()
        self.create_Y_matrix()
        if self.check_connditions():
            self.calculate()
            self.create_polynomial()
            self.x_output = np.linspace(min(self.Xs)-100, max(self.Xs)+100)
            self.y_output = self.polynomial(self.x_output)


if __name__ == "__main__":

    lsm = LSM([1, 2, 3, 4, 5], [1, 2, 3, 4, 5], 3)
    print(lsm.create_X_matrix())
