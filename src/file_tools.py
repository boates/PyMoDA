#!/usr/bin/env python
"""
file_tools.py
Author: Brian Boates

Methods to assist with input/output file handling
"""
import numpy as np
from atom import Atom
from lattice import Lattice
from configuration import Configuration
from simulation import Simulation

def read_trj(trj_file):
    """
    return: nothing
    parameters:
        trj_file: string | name of trj file
    """
    simulation = Simulation()
    with open(trj_file, 'r') as trj:

        while True:

            line = trj.readline()
            if not line:
                break
            lattice = Lattice()
            lattice.set_a(np.array(line.split(), dtype=float))
            lattice.set_b(np.array(trj.readline().split(), dtype=float))
            lattice.set_c(np.array(trj.readline().split(), dtype=float))

            configuration = Configuration(lattice=lattice)

            atom_types = trj.readline().split()
            atom_counts = np.array(trj.readline().split(), dtype=int)
            natom = np.sum(atom_counts)

            for i in xrange(natom):
                atom_record = trj.readline().split()
                atom_name = atom_record[0]
                atom_position = np.array(atom_record[1:], dtype=float)
                configuration.insert_atom(Atom(atom_name, atom_position))

            simulation.insert_configuration(configuration)

