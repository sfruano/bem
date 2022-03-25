# -*- coding: utf-8 -*-
"""
Created on Tue Mar 22 13:12:27 2022

@author: etaschner
"""

##############################################################################
# Modules
import numpy as np
import airfoilData as aD
from solveBEM import bemLoop

##############################################################################
# Define Input Parameters

# Environmental Conditions
Uinf = 1                                   # axial inflow velocity

# Rotor/Blade parameters
R = 50                                      # Rotor radius [m]
Rst = 0.2                                   # radial position of blade start (fraction of  total Radius)
Nbl = 3                                     # number of blades
airfoil = 'DU95W180.cvs'                    # airfoil data file name
NblPts = 81                                 # Number of radial discretisation point
airDensity = 1.225                         # Air Density [kg/m³]

pitch = 2                                  # blade pitch angle [deg]
yaw = np.array([0,15,30])                   # rotor yaw angle [deg]

# Turbine Operation Point
TSR = 8                   # array of studied tip speed ratios

# Read Airfoil Data
alpha_data, lift_data, drag_data = aD.readAirfoilData(airfoil)

# Initialise Array for results
bemResults = np.zeros((NblPts-1,1))

#############################################################################
# Generate Blade Mesh
rNodes = np.linspace(Rst, 1.0, NblPts)*R
rMidNodes = (rNodes[:-1]+rNodes[1:])/2.0

#############################################################################
# Generate Twist and Chord Distributions
twistDist = 14*(1-rMidNodes/R)  - pitch         # twist distribution along blade (for r/R>Rst) [deg]
chordDist = 3*(1-rMidNodes/R) + 1               # chord distribution along blade (for r/R>Rst) [m]

##############################################################################
# Blade Element Solver - Loop across the independent radial blade sections


omega = TSR*Uinf/R
bemLoop(Uinf, TSR, omega, Nbl, airDensity, twistDist, chordDist, alpha_data, lift_data, drag_data, rNodes, rMidNodes, R, Rst)


