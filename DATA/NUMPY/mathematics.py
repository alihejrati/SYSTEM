import torch
import numpy as np
from KERNEL.SCRIPT.python.classes.basic import PYBASE

class Mathematics(PYBASE):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.__start()

    def __start(self):
        pass

    def tanh(self, x):
        x = torch.tensor(x)
        return x.tanh().numpy()

    def tanh_sx(self, x_np):
        x_np = torch.tensor(x_np)
        x_np2 = 2 * x_np.abs()
        return torch.min(torch.max((-x_np2+1), ((x_np2/5) - (1/5))), x_np**0).numpy()
    
    def tanh_gsl(self, g, x_np):
        return g * (1 + self.tanh_sx(x_np) / 2)
    
    def triangle(self, A, B, C):
        """
            A, B, C are nodes in triangle
            look at this: @OPENCV/import/triangleangle.jpg  for interpreting which angle you look for.
        """
        lengthSquare = lambda X, Y: (((X[0] - Y[0]) ** 2) + ((X[1] - Y[1]) ** 2))
        a2, b2, c2 = lengthSquare(A, C), lengthSquare(B, C), lengthSquare(A, B)
        a, b, c = np.sqrt(a2), np.sqrt(b2), np.sqrt(c2)
        
        alpha = np.arccos(np.clip(np.true_divide((a2 + c2 - b2), (2 * a * c)), -1, 1)) * 180 / np.pi
        beta  = np.arccos(np.clip(np.true_divide((a2 + b2 - c2), (2 * a * b)), -1, 1)) * 180 / np.pi
        gamma = np.arccos(np.clip(np.true_divide((b2 + c2 - a2), (2 * b * c)), -1, 1)) * 180 / np.pi
        
        node = dict(A=A, B=B, C=C)
        edge = dict(a2=a2, b2=b2, c2=c2, a=a, b=b, c=c)
        angle = dict(alpha=alpha, beta=beta, gamma=gamma)
        return dict(node=node, edge=edge, angle=angle)