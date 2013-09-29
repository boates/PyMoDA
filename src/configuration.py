#!/usr/bin/env python
"""
configuration.py
Author: Brian Boates

Implementes Configuration()
"""
import numpy as np

class Configuration(object):
    """
    """
    def __init__(self):
        self._atoms = []
        self._lattice = None

    def __str__(self):
        """
        return: string
        """
        s = ''
        return s

    def __repr__(self):
        """
        return: string
        """
        return self.__str__()

    def get_lattice(self):
        """
        return: Lattice
        """
        return self._lattice

    def set_lattice(self, lattice):
        self._lattice = lattice

    def get_atoms(self):
        """
        return: list[Atom]
        """
        return self._atoms

    def get_natom(self):
        """
        return: int | number of atoms currently in configuration
        """
        return len(self.get_atoms())

    def insert_atom(self, atom):
        self._atom.append(atom)

    def insert_atoms(self, atom_list):
        """
        parameters:
            atom_list: list[Atom]
        """
        for atom in atom_list:
            self.insert_atom(atom)

    def foo(self):
        """
        """
        pass


