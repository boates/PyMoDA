#!/usr/bin/env python
"""
atom.py
Author: Brian Boates

Implements Atom()
"""
import sys
sys.dont_write_bytecode = True
import numpy as np
import file_tools
from utils import atomic_mass
from utils import pbc_displacement

class Atom(object):
    """
    """
    def __init__(self, name, position):
        """
        parameters:
            name: string | atom type (i.e. H, He, Li, ...)
            position: np.array[float] | reduced coordinates
        """
        self._name = name
        self._a = position[0]
        self._b = position[1]
        self._c = position[2]
        self._x = None
        self._y = None
        self._z = None
        self._velocity = None

    def __str__(self):
        """
        return: string
        """
        values = (self.get_name(), self.get_a(), self.get_b(), self.get_c())
        s = '<Atom: name=%s, a=%s, b=%s, c=%s>' % values
        return s

    def __repr__(self):
        """
        return: string
        """
        return self.__str__()

    def __eq__(self, atom):
        """
        return: bool
        """
        same_name = self.get_name() == atom.get_name()
        same_a = self.get_a() == atom.get_a()
        same_b = self.get_b() == atom.get_b()
        same_c = self.get_c() == atom.get_c()
        return same_name and same_a and same_b and same_c

    def __ne__(self, atom):
        """
        return: bool
        """
        return not self.__eq__(atom)

    def trj_str(self):
        """
        return: string | for trj file
        """
        values = (self.get_name(), self.get_a(), self.get_b(), self.get_c())
        return '%s %s %s %s\n' % values

    def set_name(self, name):
        self._name = name

    def set_a(self, a):
        self._a = a

    def set_b(self, b):
        self._b = b

    def set_c(self, c):
        self._c = c

    def set_position(self, position):
        """
        parameters:
            position: np.array[float] | length 3
        """
        self.set_a(position[0])
        self.set_b(position[1])
        self.set_c(position[2])

    def get_name(self):
        """
        return: string
        """
        return self._name

    def get_mass(self):
        """
        return: float | atomic mass in amu
        """
        return atomic_mass(self.get_name())

    def get_a(self):
        """
        return: float | reduced a coordinate
        """
        return self._a

    def get_b(self):
        """
        return: float | reduced b coordinate
        """
        return self._b

    def get_c(self):
        """
        return: float | reduced c coordinate
        """
        return self._c

    def _compute_x(self, lattice):
        """
        return: float | cartesian x coordinate
        parameters:
            lattice: Lattice
        """
        x  = self.get_a() * lattice.get_ax()
        x += self.get_b() * lattice.get_bx()
        x += self.get_c() * lattice.get_cx()
        return x

    def _compute_y(self, lattice):
        """
        return: float | cartesian y coordinate
        parameters:
            lattice: Lattice
        """
        y  = self.get_a() * lattice.get_ay()
        y += self.get_b() * lattice.get_by()
        y += self.get_c() * lattice.get_cy()
        return y

    def _compute_z(self, lattice):
        """
        return: float | cartesian z coordinate
        parameters:
            lattice: Lattice
        """
        z  = self.get_a() * lattice.get_az()
        z += self.get_b() * lattice.get_bz()
        z += self.get_c() * lattice.get_cz()
        return z

    def get_x(self, lattice):
        """
        return: float | cartesian x coordinate
        parameters:
            lattice: Lattice
        """
        if not self._x:
            self._x = self._compute_x(lattice)
        return self._x

    def get_y(self, lattice):
        """
        return: float | cartesian y coordinate
        parameters:
            lattice: Lattice
        """
        if not self._y:
            self._y = self._compute_y(lattice)
        return self._y

    def get_z(self, lattice):
        """
        return: float | cartesian z coordinate
        parameters:
            lattice: Lattice
        """
        if not self._z:
            self._z = self._compute_z(lattice)
        return self._z

    def get_position(self, unit='reduced', lattice=None):
        """
        return: np.array | length 3
        parameters:
            unit: string | 'reduced' (default) or 'cartesian'
            lattice: Lattice
        """
        if unit == 'reduced':
            return np.array([self.get_a(), self.get_b(), self.get_c()])
        elif unit == 'cartesian':
            if not lattice:
                raise ValueError, 'lattice required for cartesian position'
            return np.array([self.get_x(lattice), self.get_y(lattice), self.get_z(lattice)])
        else:
            raise ValueError, 'unit must be reduced or cartesian'

    def get_wrapped_position(self):
        """
        return: np.array[float] | length 3
        """
        wrapped_a = self.get_a() - np.floor(self.get_a())
        wrapped_b = self.get_b() - np.floor(self.get_b())
        wrapped_c = self.get_c() - np.floor(self.get_c())
        return np.array([wrapped_a, wrapped_b, wrapped_c])

    def wrap_position(self):
        """
        Destructive: changes positions
        """
        self.set_position(self.get_wrapped_position())

    def _compute_velocity(self, prev_atom, dt, lattice, prev_lattice=None):
        """
        Warnings:
          - assumes atom positions are unwrapped

        return: np.array[float] | x, y, z velocity components
        parameters:
            prev_position: Atom | atom when at previous position
            dt: float | time since previous position
            lattice: Lattice | lattice for atom at current position
            prev_lattice: Lattice | lattice for atom at previous position
        """
        # if not given, assume previous lattice is same as current
        if not prev_lattice:
            prev_lattice = lattice

        dx = self.get_x(cur_lattice) - prev_atom.get_x(prev_lattice)
        dy = self.get_y(cur_lattice) - prev_atom.get_y(prev_lattice)
        dz = self.get_z(cur_lattice) - prev_atom.get_z(prev_lattice)
        vx = dx / dt if dt != 0 else np.inf
        vy = dy / dt if dt != 0 else np.inf
        vz = dz / dt if dt != 0 else np.inf
        return np.array([vx, vy, vz])

    def get_velocity(self, prev_atom, dt, lattice, prev_lattice=None):
        """
        Warnings:
          - assumes atom positions are unwrapped

        return: np.array[float] | x, y, z velocity components
        parameters:
            prev_position: Atom | atom when at previous position
            dt: float | time since previous position
            lattice: Lattice | lattice for atom at current position
            prev_lattice: Lattice | lattice for atom at previous position
        """
        if not self._velocity:
            self._velocity = self._compute_velocity(prev_atom, df, lattice, prev_lattice)
        return self._velocity

    def to_pkl(self, file_name='atom.pkl'):
        """
        Save Atom object as pickle file
        """
        file_tools.save_pkl(self, file_name)
