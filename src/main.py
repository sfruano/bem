# -*- coding: utf-8 -*-
"""
Created on Tue Mar 22 13:12:27 2022

@author: etaschner
"""

##############################################################################
# Modules
import numpy as np
import airfoilData as aD
import solveBEM as bem

##############################################################################
# Define Input Parameters

# Environmental Conditions
Uinf = 10                                   # axial inflow velocity

# Rotor/Blade parameters
R = 50                                      # Rotor radius [m]
Rst = 0.2                                   # radial position of blade start (in %)
Nbl = 3                                     # number of blades
airfoil = 'DU95W180.cvs'                    # airfoil data file name
NblPts = 81                                 # Number of radial discretisation points
Rloc = R * np.linspace(Rst, 1, num=NblPts)  # array of discrete radial blade locations

pitch = -2                                  # blade pitch angle [deg]
yaw = np.array([0,15,30])                   # rotor yaw angle [deg]
twist_dist = 14*(1-Rloc/R)  + pitch         # twist distribution along blade (for r/R>Rst) [deg]
chord_dist = 3*(1-Rloc/R) + 1               # chord distribution along blade (for r/R>Rst) [m]

# Turbine Operation Point
TSR = np.array([6,8,10])                    # array of studied tip speed ratios
omega = TSR*Uinf/R                          # rotor rotaional speed [rad]

# Read Airfoil Data
alpha_data, lift_data, drag_data = aD.readAirfoilData(airfoil)

# Initialise Array for results
bemResults = np.zeros((NblPts-1,1))

##############################################################################
# Blade Element Solver - Loop across the independent radial blade sections

for r in range(NblPts):
    # Interpolate to obtain the local twist angle and chord length at specific radial position
    chordR = np.interp((Rloc[r]+Rloc[r+1])/2, Rloc, chord_dist)
    twistR = np.interp((Rloc[r]+Rloc[r+1])/2, Rloc, twist_dist)
    # call the BEM solver for a certain r location
    bem.bemLoop()


