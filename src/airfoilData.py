# -*- coding: utf-8 -*-
"""
Created on Tue Mar 22 10:21:30 2022

@author: etaschner
"""
##############################################################################
# Modules
import pandas as pd

##############################################################################
def readAirfoilData(fname):
    '''
    Parameters
    ----------
    fname : string
        filename containing the polar airfoil data

    Returns
    -------
    alpha_data : series
        angle of attack
    lift_data : series
        nondimensional lift coefficient
    drag_data : series
        nondimensional drag coefficient
    '''
    data = pd.read_csv(fname, header=0, names = ["alfa", "cl", "cd", "cm"],  sep='\s+')
    alpha_data = data['alfa']
    lift_data = data['cl']
    drag_data = data['cd']
    
    return alpha_data, lift_data, drag_data