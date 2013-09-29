#!/usr/bin/env python
"""
lattice.py
Author: Brian Boates

Implements Lattice()
"""
import numpy as np

class Lattice(object):
    """
    """
    def __init__(self, ax=None, ay=None, az=None
                     , bx=None, by=None, bz=None
                     , cx=None, cy=None, cz=None):
        self._ax = ax
        self._ay = ay
        self._az = az
        self._bx = bx
        self._by = by
        self._bz = bz
        self._cx = cx
        self._cy = cy
        self._cz = cz

    def __str__(self):
        """
        return: string
        """
        s  = '<Lattice: '
        s += 'a=(%s, %s, %s), ' % (self.get_ax(), self.get_ay(), self.get_az())
        s += 'b=(%s, %s, %s), ' % (self.get_bx(), self.get_by(), self.get_bz())
        s += 'c=(%s, %s, %s)>'  % (self.get_cx(), self.get_cy(), self.get_cz())
        return s

    def __repr__(self):
        """
        return: string
        """
        return self.__str__()

    def set_ax(self, ax):
        self._ax = ax

    def set_ay(self, ay):
        self._ay = ay

    def set_az(self, az):
        self._az = az

    def set_bx(self, bx):
        self._bx = bx

    def set_by(self, by):
        self._by = by

    def set_bz(self, bz):
        self._bz = bz

    def set_cx(self, cx):
        self._cx = cx

    def set_cy(self, cy):
        self._cy = cy

    def set_cz(self, cz):
        self._cz = cz

    def get_ax(self):
        """
        return: float
        """
        return self._ax

    def get_ay(self):
        """
        return: float
        """
        return self._ay

    def get_az(self):
        """
        return: float
        """
        return self._az

    def get_bx(self):
        """
        return: float
        """
        return self._bx

    def get_by(self):
        """
        return: float
        """
        return self._by

    def get_bz(self):
        """
        return: float
        """
        return self._bz

    def get_cx(self):
        """
        return: float
        """
        return self._cx

    def get_cy(self):
        """
        return: float
        """
        return self._cy

    def get_cz(self):
        """
        return: float
        """
        return self._cz

    def set_a(self, a_vector):
        self.set_ax(a_vector[0])
        self.set_ay(a_vector[1])
        self.set_az(a_vector[2])

    def set_b(self, b_vector):
        self.set_bx(b_vector[0])
        self.set_by(b_vector[1])
        self.set_bz(b_vector[2])

    def set_c(self, c_vector):
        self.set_cx(c_vector[0])
        self.set_cy(c_vector[1])
        self.set_cz(c_vector[2])

    def get_a(self):
        """
        return: np.array | length 3
        """
        return np.array([self.get_ax(), self.get_ay(), self.get_az()])

    def get_b(self):
        """
        return: np.array | length 3
        """
        return np.array([self.get_bx(), self.get_by(), self.get_bz()])

    def get_c(self):
        """
        return: np.array | length 3
        """
        return np.array([self.get_cx(), self.get_cy(), self.get_cz()])

    def mag_a(self):
        """
        return: float | magnitude of 'a' vector
        """
        return np.sqrt(np.dot(self.get_a(), self.get_a()))

    def mag_b(self):
        """
        return: float | magnitude of 'b' vector
        """
        return np.sqrt(np.dot(self.get_b(), self.get_b()))

    def mag_c(self):
        """
        return: float | magnitude of 'c' vector
        """
        return np.sqrt(np.dot(self.get_c(), self.get_c()))

    def alpha(self, unit='degrees'):
        """
        return: float | alpha angle
        parameters:
            unit: string | 'degrees' (default) or 'radians'
        """
        numerator = np.dot(self.get_b(), self.get_c())
        denominator = self.mag_b() * self.mag_c()
        theta = np.arccos(numerator / denominator)
        if unit == 'degrees':
            pi = np.arccos(-1)
            return theta * 180./pi
        elif unit == 'radians':
            return theta
        else:
            raise ValueError, 'unit must be degrees or radians'

    def beta(self, unit='degrees'):
        """
        return: float | alpha angle
        parameters:
            unit: string | 'degrees' (default) or 'radians'
        """
        numerator = np.dot(self.get_a(), self.get_c())
        denominator = self.mag_a() * self.mag_c()
        theta = np.arccos(numerator / denominator)
        if unit == 'degrees':
            pi = np.arccos(-1)
            return theta * 180./pi
        elif unit == 'radians':
            return theta
        else:
            raise ValueError, 'unit must be degrees or radians'

    def gamma(self, unit='degrees'):
        """
        return: float | alpha angle
        parameters:
            unit: string | 'degrees' (default) or 'radians'
        """
        numerator = np.dot(self.get_a(), self.get_b())
        denominator = self.mag_a() * self.mag_b()
        theta = np.arccos(numerator / denominator)
        if unit == 'degrees':
            pi = np.arccos(-1)
            return theta * 180./pi
        elif unit == 'radians':
            return theta
        else:
            raise ValueError, 'unit must be degrees or radians'

    def volume(self):
        """
        return: float | scalar triple product
        """
        return np.abs(np.dot(self.get_a(), np.cross(self.get_b(), self.get_c())))

