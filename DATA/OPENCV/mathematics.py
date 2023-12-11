import math
from KERNEL.PYTHON.classes.basic import PYBASE

class Mathematics(PYBASE):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.__start()

    def __start(self):
        pass

    def angles_of_triangle(self, A, B, C):
        """
            A, B, C are nodes in triangle
            look at this: @OPENCV/import/triangleangle.jpg
        """
        lengthSquare = lambda X, Y: (((X[0] - Y[0]) ** 2) + ((X[1] - Y[1]) ** 2))
        a2, b2, c2 = lengthSquare(A, C), lengthSquare(B, C), lengthSquare(A, B)
        a, b, c = math.sqrt(a2), math.sqrt(b2), math.sqrt(c2)
        alpha = math.acos((a2 + c2 - b2) / (2 * a * c)) * 180 / math.pi
        beta  = math.acos((a2 + b2 - c2) / (2 * a * b)) * 180 / math.pi
        gamma = math.acos((b2 + c2 - a2) / (2 * b * c)) * 180 / math.pi
        return alpha, beta, gamma