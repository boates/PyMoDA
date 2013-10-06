#!/usr/bin/env python
"""
simulation.py
Author: Brian Boates

Implements Simulation()
"""
import sys
sys.dont_write_bytecode = True
import numpy as np
import file_tools
from atom import Atom
from lattice import Lattice
from configuration import Configuration

class Simulation(object):
    """
    """
    def __init__(self, configurations=[], timestep=None):
        """
        parameters:
            configurations: list[Configuration]
            timestep: float
        """
        self._configurations = []
        self._timestep = timestep
        self.insert_configurations(configurations)

    def __str__(self):
        """
        return: string
        """
        s  = '<Simulation: timestep=%s, ' % self.get_timestep()
        s += 'num_configurations=%s>' % self.num_configurations()
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
        return iter(self.get_configurations())

    def trj_str(self):
        """
        return: string | for trj file
        """
        s = ''
        for configuration in self:
            s += configuration.trj_str()
        return s

    def get_configurations(self):
        """
        return: list[Configuration]
        """
        return self._configurations

    def get_timestep(self):
        """
        return: float | simulation timestep
        """
        return self._timestep

    def set_timestep(self, timestep):
        """
        parameters:
            timestep: float
        """
        self._timestep = timestep

    def get_time(self, timestep_idx):
        """
        return: float | time of simulation at timestep_idx
        parameters:
            timestep_idx: int | configuration index
        """
        return timestep_idx * self.get_timestep()

    def length(self):
        """
        return: float
        """
        return self.get_time(self.num_configurations()-1)

    def insert_configuration(self, configuration):
        """
        parameters:
            configuration: Configuration
        """
        self._configurations.append(configuration)

    def insert_configurations(self, configurations):
        """
        parameters:
            configurations: list[Configuration]
        """
        for configuration in configurations:
            self.insert_configuration(configuration)

    def num_configurations(self):
        """
        return: int
        """
        return len(self.get_configurations())

    def get_configuration(self, timestep_idx):
        """
        return: Configuration
        parameters:
            timestep_idx: int | configuration index
        """
        if 0 <= timestep_idx < self.num_configurations():
            return self.get_configurations()[timestep_idx]
        else:
            raise IndexError, 'timestep_idx out of simulation range'

    def unwrap_coordinates(self):
        """
        """
        pass

    def set_velocities(self):
        """
        Warning: only valid if simulation is unwrapped
        """
        pass

    def to_trj(self, file_name='simulation.trj'):
        """
        Write Simulation object to trj file
        parameters:
            file_name: string | name for output trj file
        """
        with open(file_name, 'w') as outfile:
            outfile.write(self.trj_str().strip())

    def to_pkl(self, file_name='simulation.pkl'):
        """
        Save Simulation object as pickle file
        """
        file_tools.save_pkl(self, file_name)


def main():

    atom = Atom('N', [0.1, 0.2, 0.3])
    lattice = Lattice(1, 0, 0, 0, 1, 0, 0, 0, 1)
    configuration = Configuration(atoms=[atom]*5, lattice=lattice)
    simulation = Simulation([configuration]*7, timestep=0.75)

    print simulation.trj_str()
    print simulation


if __name__ == '__main__':
    main()
