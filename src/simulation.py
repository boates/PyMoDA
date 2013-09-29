#!/usr/bin/env python
"""
simulation.py
Author: Brian Boates

Implements Simulation()
"""
import numpy as np
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
        self._configurations = configurations
        self._timestep = timestep

    def __str__(self):
        """
        return: string
        """
        s = '<Simulation: >'
        return s

    def __repr__(self):
        """
        return: string
        """
        return self.__str__()

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

    def insert_configuration(self, configuration):
        """
        parameters:
            configuration: Configuration
        """
        self._configurations.append(configuration)

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
        if 0 < timestep_idx < self.num_configurations():
            return self.get_configurations()[timestep_idx]
        else:
            raise IndexError, 'timestep_idx out of simulation range'

    def get_time(self, timestep_idx):
        """
        return: float | time of simulation at timestep_idx
        parameters:
            timestep_idx: int | configuration index
        """
        return timestamp_idx * self.get_timestep()


