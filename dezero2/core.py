"""Fill in a module description here"""

# AUTOGENERATED! DO NOT EDIT! File to edit: ../nbs/00_core.ipynb.

# %% auto 0
__all__ = ['Variable', 'Function', 'Square', 'square', 'Exp', 'exp', 'numerical_diff']

# %% ../nbs/00_core.ipynb 3
import numpy as np

# %% ../nbs/00_core.ipynb 4
class Variable:
    def __init__(self, data):
        if data is not None: # Why allowing "None" here?
            if not isinstance(data, np.ndarray):
                raise TypeError("{} is not supported".format(type(data)))
        self.data = data
        self.grad = None
        self.creator = None

    def set_creator(self, func):
        self.creator = func

    def backward(self):
        if self.grad == None:
            self.grad = np.ones_like(self.data)
        funcs = [self.creator]
        while funcs:
            f = funcs.pop()
            x, y = f.input, f.output
            x.grad = f.backward(y.grad)
            if x.creator == None:
                continue
            funcs.append(x.creator)

# %% ../nbs/00_core.ipynb 6
class Function:
    def __call__(self, input):
        x = input.data
        y = self.forward(x)
        y = np.array(y) if np.isscalar(y) else y # for numpy spec
        output = Variable(y)
        output.set_creator(self)
        self.input = input
        self.output = output
        return output

    def forward(self, in_data):
        raise NotImplementedError()

    def backward(self, gy):
        raise NotImplementedError()

# %% ../nbs/00_core.ipynb 7
class Square(Function):
    def forward(self, x):
        y = x ** 2
        return y

    def backward(self, gy):
        x = self.input.data
        gx = 2 * x * gy
        return gx

def square(x):
    return Square()(x)

# %% ../nbs/00_core.ipynb 9
class Exp(Function):
    def forward(self, x):
        return np.exp(x)

    def backward(self, gy):
        x = self.input.data
        gx = np.exp(x) * gy
        return gx

def exp(x):
    return Exp()(x)

# %% ../nbs/00_core.ipynb 12
def numerical_diff(f, x, eps=1e-4):
    x0 = Variable(np.array(x.data - eps))
    x1 = Variable(np.array(x.data + eps))
    y0 = f(x0)
    y1 = f(x1)
    return (y1.data - y0.data) / (2 * eps)
