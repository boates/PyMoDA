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
    def __init__(self):
        """
        """
        self._configurations = []

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

    def get_configurations():
        """
        return: list[Configuration]
        """
        return self._configurations

    def insert_configuration(configuration):
        self._configurations.append(configuration)

    def num_configurations():
        """
        return: int
        """
        return len(self.get_configurations())

