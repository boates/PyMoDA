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
from utils import pbc_distance
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
        self._atoms = defaultdict(list)
        self._lattice = lattice
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
        for name, atoms in self._atoms.iteritems():
            name_str += '%s ' % name
            count_str += '%s ' % len(atoms)
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

    def get_atoms(self, name=None):
        """
        return: list[Atom]
        parameters:
            name: string | type of atoms to get
        """
        if not name:
            return list(np.concatenate(self._atoms.values()))
        else:
            return self._atoms[name]

    def get_natom(self, name=None):
        """
        return: int | number of atoms currently in configuration
        """
        return len(self.get_atoms(name))

    def get_atom_types(self):
        """
        return: list[string]
        """
        return self._atoms.keys()

    def get_ntypes(self):
        """
        return: int | number of different atom types
        """
        return len(self.get_atom_types())

    def insert_atom(self, atom):
        self._atoms[atom.get_name()].append(atom)

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

    def get_distances_dict(self, unit='cartesian'):
        """
        Computes distances between all atoms and stores them
        in a dictionary where the key is a string representing
        the atom pair type (e.g. 'C-O'), and the value is a
        list of distances for that atom pair type.

        return: dict[string:list[float]]
        parameters:
            unit: string | 'reduced' or 'cartesian' (default)
        """
        distances = defaultdict(list)
        atoms = self.get_atoms()
        for i in xrange(len(atoms)):
            name_i = atoms[i].get_name()
            for j in xrange(i+1, len(atoms)):
                name_j = atoms[j].get_name()
                key = min(name_i, name_j) + '-' + max(name_i, name_j)
                distances[key].append(pbc_distance(atoms[i], atoms[j], unit=unit
                                                  ,lattice=self.get_lattice()))

        return dict(distances)

    def get_distances_list(self, name1=None, name2=None, unit='cartesian'):
        """
        If name1 or name2 are None, a list of all distances between
        all atoms types is returned, otherwise only distances between
        atoms with type name1 and name2 are returned.

        return: list[float] | distances between atoms
        parameters:
            name1: string | atom type
            name2: string | atom type
            unit: string | either 'reduced' or 'cartesian' (default)
        """
        distances = []
        if name1 == name2:
            if not name1 or not name2:
                atoms = self.get_atoms()
            else:
                atoms = self.get_atoms(name=name1)
            for i in xrange(len(atoms)):
                for j in xrange(i+1, len(atoms)):
                    distances.append(pbc_distance(atoms[i], atoms[j], unit=unit
                                                 ,lattice=self.get_lattice()))

        else:
            atoms1 = self.get_atoms(name=name1)
            atoms2 = self.get_atoms(name=name2)
            for atom1 in atoms1:
                for atom2 in atoms2:
                    distances.append(pbc_distance(atom1, atom2, unit=unit
                                                 ,lattice=self.get_lattice()))

        return distances

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

    atom1 = Atom('N', [0.10, 0.20, 0.30])
    atom2 = Atom('C', [0.50, 0.23, 0.73])
    atom3 = Atom('O', [0.70, 0.30, 0.60])
    atom4 = Atom('O', [0.10, 0.50, 0.90])
    atom5 = Atom('O', [0.10, 0.50, 0.50])
    atoms = [atom1, atom2, atom3, atom4, atom5]
    lattice = Lattice(10, 0, 0, 0, 10, 0, 0, 0, 10)
    configuration = Configuration(atoms, lattice=lattice)
    print configuration.trj_str()

    distances = configuration.get_distances_dict()
    print distances


if __name__ == '__main__':
    main()
