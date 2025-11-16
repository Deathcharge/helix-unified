# psi_field.py
import numpy as np

class PsiField:
    def __init__(self, defaults):
        self.field = np.random.rand(64, 64)
        self.defaults = defaults

    def random_perturbation(self):
        x, y = np.random.randint(0, 64, 2)
        self.field[x, y] += np.random.uniform(0.1, 1.0)

    def update(self):
        self.field = np.clip(self.field + np.random.normal(0, 0.005, self.field.shape), 0, 1)

    def reset(self):
        self.field = np.zeros((64, 64))
