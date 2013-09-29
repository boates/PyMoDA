#!/usr/bin/env python
"""
utils.py
Author: Brian Boates

Utility functions for PyMoDA
"""

def pbc_displacement(atom1, atom2, unit='reduced', lattice=None):
    """
    return: np.array | displacement vector in minimum image convention
    parameters:
        atom1: Atom
        atom2: Atom
        unit: string | 'reduced' (default) or 'cartesian'
        lattice: Lattice
    """
    # make sure coordinates are wrapped
    a1 = atom1.get_a() - np.floor(atom1.get_a())
    a2 = atom2.get_a() - np.floor(atom2.get_a())
    a_diff = a1 - a2
    if a_diff > 0.5:
        a_diff += -1
    elif a_diff < -0.5:
        a_diff += 1

    b1 = atom1.get_b() - np.floor(atom1.get_b())
    b2 = atom2.get_b() - np.floor(atom2.get_b())
    b_diff = b1 - b2
    if b_diff > 0.5:
        b_diff += -1
    elif b_diff < -0.5:
        b_diff += 1

    c1 = atom1.get_c() - np.floor(atom1.get_c())
    c2 = atom2.get_c() - np.floor(atom2.get_c())
    c_diff = c1 - c2
    if c_diff > 0.5:
        c_diff += -1
    elif c_diff < -0.5:
        c_diff += 1

    if unit == 'reduced':
        return np.array([a_diff, b_diff, c_diff])

    elif unit == 'cartesian':
        if not lattice:
            raise ValueError, 'lattice required for cartesian displacement'

        x_diff  = a_diff * lattice.get_ax()
        x_diff += b_diff * lattice.get_bx()
        x_diff += c_diff * lattice.get_cx()

        y_diff  = a_diff * lattice.get_ay()
        y_diff += b_diff * lattice.get_by()
        y_diff += c_diff * lattice.get_cy()

        z_diff  = a_diff * lattice.get_az()
        z_diff += b_diff * lattice.get_bz()
        z_diff += c_diff * lattice.get_cz()

        return np.array([x_diff, y_diff, z_diff])

    else:
        raise ValueError, 'unit must be reduced or cartesian'

def pbc_distance(atom1, atom2, unit='reduced', lattice=None):
    """
    return: float | distance in minimum image convention
    """
    displacement = pbc_displacement(atom1, atom2, unit, lattice)
    return np.sqrt(np.dot(displacement, displacement))

