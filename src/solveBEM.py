# -*- coding: utf-8 -*-
"""
Created on Fri Mar 25 14:30:00 2022

@author: etaschner
"""

##############################################################################
# Modules
import numpy as np
import airfoilLoad as aL

##############################################################################
def bemLoop():
    fN, fTan = aL.computeAirfoilLoad(uNorm, uTang, alpha_data, lift_data, drag_data, chord_dist, twist_dist)
    return