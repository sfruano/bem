# -*- coding: utf-8 -*-
"""
Created on Tue Mar 22 10:21:30 2022

@author: etaschner
"""
##############################################################################
# Modules
import numpy as np

##############################################################################
def computeAirfoilLoad(uNorm, uTang, alpha_data, lift_data, drag_data, chord_data, twist_data, airDensity):
    '''
    

    Parameters
    ----------
    uNorm : TYPE
        DESCRIPTION.
    uTang : TYPE
        DESCRIPTION.
    alpha_data : TYPE
        DESCRIPTION.
    lift_data : TYPE
        DESCRIPTION.
    drag_data : TYPE
        DESCRIPTION.
    chord_data : TYPE
        DESCRIPTION.
    twist_data : TYPE
        DESCRIPTION.

    Returns
    -------
    fN : numpy array
        rotor normal force per unit length (still misses spanwise dimension)
    fTan : numpy array
        rotor tangential force per unit length (still misses spanwise dimension)

    '''
    mag = uNorm**2 + uTang**2
    ainflow = np.arctan(uNorm/uTang) * (180/np.pi)
    aoa = ainflow - twist_data                                          # Twist already includes pitch!
    clInterp = np.interp(aoa, alpha_data, lift_data)
    cdInterp = np.interp(aoa, alpha_data, drag_data)
    lift = 0.5*airDensity*mag*clInterp*chord_data
    drag = 0.5*airDensity*mag*cdInterp*chord_data
    ainflow_rad = ainflow*np.pi/180.0
    fN = lift*np.cos(ainflow_rad)+drag*np.sin(ainflow_rad)
    fTan = lift*np.sin(ainflow_rad)-drag*np.cos(ainflow_rad)
    
    return fN, fTan







