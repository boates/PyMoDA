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
import file_tools
from atom import Atom
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
        self._atoms = []
        self._lattice = lattice
        self._atom_counter = defaultdict(int)
        self.insert_atoms(atoms)

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

    def trj_str(self):
        """
        return: string | for trj file
        """
        s = self.get_lattice().trj_str()

        name_str, count_str = '', ''
        for name, count in self.get_atom_counter().iteritems():
            name_str += '%s ' % name
            count_str += '%s ' % count
        s += name_str.strip() + '\n' + count_str.strip() + '\n'

        for atom in self:
            s += atom.trj_str()

        return s

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

    def get_atom_types(self):
        """
        return: set[string]
        """
        return set(self.get_atom_counter.keys())

    def get_ntypes(self):
        """
        return: int | number of different atom types
        """
        return len(self.get_atom_counter().keys())

    def insert_atom(self, atom):
        self._atoms.append(atom)
        self._atom_counter[atom.get_name()] += 1

    def insert_atoms(self, atoms):
        """
        parameters:
            atoms: list[Atom]
        """
        for atom in atoms:
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

    def to_trj(self, file_name='configuration.trj'):
        """
        Write Configuration object to trj file
        parameters:
            file_name: string | name for output trj file
        """
        with open(file_name, 'w') as outfile:
            outfile.write(self.trj_str().strip())

    def to_pkl(self, file_name='configuration.pkl'):
        """
        Save Configuration object as pickle file
        """
        file_tools.save_pkl(self, file_name)


def main():

    atom = Atom('N', [0.1, 0.2, 0.3])
    lattice = Lattice(1, 0, 0, 0, 1, 0, 0, 0, 1)
    configuration = Configuration([atom]*7, lattice=lattice)
    print configuration.trj_str()


if __name__ == '__main__':
    main()
