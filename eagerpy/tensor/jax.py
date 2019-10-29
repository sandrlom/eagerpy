import numpy as onp

from .base import AbstractTensor
from .base import unwrapin
from .base import wrapout


class JAXTensor(AbstractTensor):
    key = None

    def __init__(self, tensor):
        from jax import numpy

        super().__init__(tensor)
        self.backend = numpy

    def numpy(self):
        return onp.asarray(self.tensor)

    def item(self):
        return self.tensor.item()

    @property
    def shape(self):
        return self.tensor.shape

    @wrapout
    def reshape(self, shape):
        return self.tensor.reshape(shape)

    @property
    def ndim(self):
        return self.tensor.ndim

    @wrapout
    def astype(self, dtype):
        return self.tensor.astype(dtype)

    @wrapout
    def clip(self, min_, max_):
        return self.backend.clip(self.tensor, min_, max_)

    @wrapout
    def square(self):
        return self.backend.square(self.tensor)

    @wrapout
    def arctanh(self):
        return self.backend.arctanh(self.tensor)

    @wrapout
    def sum(self, axis=None, keepdims=False):
        return self.tensor.sum(axis=axis, keepdims=keepdims)

    @wrapout
    def mean(self, axis=None, keepdims=False):
        return self.tensor.mean(axis=axis, keepdims=keepdims)

    @wrapout
    def min(self, axis=None, keepdims=False):
        return self.tensor.min(axis=axis, keepdims=keepdims)

    @wrapout
    def max(self, axis=None, keepdims=False):
        return self.tensor.max(axis=axis, keepdims=keepdims)

    @unwrapin
    @wrapout
    def minimum(self, other):
        return self.backend.minimum(self.tensor, other)

    @unwrapin
    @wrapout
    def maximum(self, other):
        return self.backend.maximum(self.tensor, other)

    @wrapout
    def argmin(self, axis=None):
        return self.tensor.argmin(axis=axis)

    @wrapout
    def argmax(self, axis=None):
        return self.tensor.argmax(axis=axis)

    @wrapout
    def argsort(self, axis=-1):
        return self.tensor.argsort(axis=axis)

    @classmethod
    def uniform(cls, shape, low=0.0, high=1.0):
        import jax.random as random

        if cls.key is None:
            cls.key = random.PRNGKey(0)

        cls.key, subkey = random.split(cls.key)
        return cls(random.uniform(subkey, shape, minval=low, maxval=high))

    @classmethod
    def normal(cls, shape, mean=0.0, stddev=1.0):
        import jax.random as random

        if cls.key is None:
            cls.key = random.PRNGKey(0)

        cls.key, subkey = random.split(cls.key)
        return cls(random.normal(subkey, shape) * stddev + mean)