#!/usr/bin/env python
"""
utils.py
Author: Brian Boates

Utility functions for PyMoDA
"""
import numpy as np

def atomic_mass(atom_name):
    """
    return: float | atomic mass in amu
    """
    masses = {'H':1.00794, 'He':4.002602, 'Li':6.941, 'Be':9.012182
             ,'B':10.811, 'C':12.0107, 'N':14.0067, 'O':15.9994
             ,'F':18.9984032, 'Ne':20.1797, 'Na':22.98976928, 'Mg':24.3050
             ,'Al':26.9815386, 'Si':28.0855, 'P':30.973762, 'S':32.065
             ,'Cl':35.453, 'Ar':39.948, 'K':39.0983, 'Ca':40.078
             ,'Sc':44.955912, 'Ti':47.867, 'V':50.9415, 'Cr':51.9961
             ,'Mn':54.938045, 'Fe':55.845, 'Co':58.933195, 'Ni':58.6934
             ,'Cu':63.546, 'Zn':65.38, 'Ga':69.723, 'Ge':72.64
             ,'As':74.92160, 'Se':78.96, 'Br':79.904, 'Kr':83.798
             ,'Rb':85.4678, 'Sr':87.62, 'Y':88.90585, 'Zr':91.224
             ,'Nb':92.90638, 'Mo':95.96, 'Tc':98.0, 'Ru':101.07
             ,'Rh':102.90550, 'Pd':106.42, 'Ag':107.8682, 'Cd':112.411
             ,'In':114.818, 'Sn':118.710, 'Sb':121.760, 'Te':127.60
             ,'I':126.90447, 'Xe':131.293, 'Cs':132.9054519, 'Ba':137.327
             ,'La':6.145, 'Ce':6.77, 'Pr':6.773, 'Nd':7.007
             ,'Pm':7.26, 'Sm':7.52, 'Eu':5.243, 'Gd':7.895
             ,'Tb':8.229, 'Dy':8.55, 'Ho':8.795, 'Er':9.066
             ,'Tm':9.321, 'Yb':6.965, 'Lu':174.9668, 'Hf':178.49
             ,'Ta':180.94788, 'W':183.84, 'Re':186.207, 'Os':190.23
             ,'Ir':192.217, 'Pt':195.084, 'Au':196.966569, 'Hg':200.59
             ,'Tl':204.3833, 'Pb':207.2, 'Bi':208.98040, 'Po':210.0
             ,'At':210.0, 'Rn':222.0, 'Fr':223.0, 'Ra':226.0}
    return masses[atom_name]

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
    parameters:
        atom1: Atom
        atom2: Atom
        unit: string | 'reduced' (default) or 'cartesian'
        lattice: Lattice
    """
    displacement = pbc_displacement(atom1, atom2, unit, lattice)
    return np.sqrt(np.dot(displacement, displacement))

