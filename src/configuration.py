#!/usr/bin/env python
"""
configuration.py
Author: Brian Boates

Implementes Configuration()
"""
import sys
sys.dont_write_bytecode = True
import numpy as np
from collections import defaultdict
from lattice import Lattice

class Configuration(object):
    """
    """
    def __init__(self, atoms=[], lattice=None):
        """
        parameters:
            atom: list[Atom]
            lattice: Lattice
        """
        self._atoms = atoms
        self._atom_counter = defaultdict(int)
        self._lattice = lattice

    def __str__(self):
        """
        return: string
        """
        s = '<Configuration: natom=%s>' % self.get_natom()
        return s

    def __repr__(self):
        """
        return: string
        """
        return self.__str__()

    def __iter__(self):
        """
        return: iterator
        """
        return iter(self.get_atoms())

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

    def get_atom_counter(self):
        """
        return: dict[string:int]
        """
        return self._atom_counter

    def get_natom(self, name=None):
        """
        return: int | number of atoms currently in configuration
        """
        if not name:
            return len(self.get_atoms())
        else:
            return self.get_atom_counter()[name]

    def get_ntypes(self):
        """
        return: int | number of different atom types
        """
        return len(self.get_atom_counter().keys())

    def insert_atom(self, atom):
        self._atom.append(atom)
        self._atom_counter[atom.name] += 1

    def insert_atoms(self, atom_list):
        """
        parameters:
            atom_list: list[Atom]
        """
        for atom in atom_list:
            self.insert_atom(atom)

    def wrap_coordinates(self):
        """
        Destructive: atom positions will be changed
        """
        # using any() is faster than looping
        any(atom.wrap_position() for atom in self.get_atoms())

    def get_supercell(self, A, B, C):
        """
        return: Configuration
        parameters:
            A: int | number of replications along a vector
            B: int | number of replications along b vector
            C: int | number of replications along c vector
        """
        super_idx = np.array([A, B, C])
        super_ax = self.get_lattice().get_ax() * A
        super_ay = self.get_lattice().get_ay() * B
        super_az = self.get_lattice().get_az() * C
        super_bx = self.get_lattice().get_bx() * A
        super_by = self.get_lattice().get_by() * B
        super_bz = self.get_lattice().get_bz() * C
        super_cx = self.get_lattice().get_cx() * A
        super_cy = self.get_lattice().get_cy() * B
        super_cz = self.get_lattice().get_cz() * C
        super_lattice = Lattice(super_ax, super_ay, super_ax
                               ,super_bx, super_by, super_bz
                               ,super_cx, super_cy, super_cz)
        supercell = Configuration(latttice=Lattice)

        for atom in self.get_atoms():

            new_atom = Atom(atom.name, atom.get_position()/super_idx)
            supercell.insert_atom(new_atom)

            for a in range(1, A):
                position = [atom.get_a()+a, atom.get_b(), atom.get_c()]
                supercell.insert_atom(atom.name, np.array(position)/super_idx)
            for b in range(1, B):
                position = [atom.get_a(), atom.get_b()+b, atom.get_c()]
                supercell.insert_atom(atom.name, np.array(position)/super_idx)
            for c in range(1, C):
                position = [atom.get_a(), atom.get_b(), atom.get_c()+c]
                supercell.insert_atom(atom.name, np.array(position)/super_idx)

            for a in range(1, A):
                for b in range(1, B):
                    position = [atom.get_a()+a, atom.get_b()+b, atom.get_c()]
                    supercell.insert_atom(atom.name, np.array(position)/super_idx)
            for a in range(1, A):
                for c in range(1, C):
                    position = [atom.get_a()+a, atom.get_b(), atom.get_c()+c]
                    supercell.insert_atom(atom.name, np.array(position)/super_idx)
            for b in range(1, B):
                for c in range(1, C):
                    position = [atom.get_a(), atom.get_b()+b, atom.get_c()+c]
                    supercell.insert_atom(atom.name, np.array(position)/super_idx)

            for a in range(1, A):
                for b in range(1, B):
                    for c in range(1, C):
                        position = [atom.get_a()+a, atom.get_b()+b, atom.get_c()+c]
                        supercell.insert_atom(atom.name, np.array(position)/super_idx)

            return supercell


def main():

    atom = Atom('N', [0.1, 0.2, 0.3])
    print atom
    lattice = Lattice(1,0,0,0,1,0,0,0,1)
    print lattice
    configuration = Configuration()
    configuration.insert_atom(atom)
    configuration.insert_atom(atom)
    configuration.insert_atom(atom)
    print configuration
    for a in configuration:
        print a


if __name__ == '__main__':
    main()
