# -*- coding: utf-8 -*-
"""
Created on Fri Mar 25 14:30:00 2022

@author: etaschner
"""

##############################################################################)
# Modules
import matplotlib.pyplot as plt
import numpy as np
from airfoilLoad import computeAirfoilLoad
from glauert import glauertCorrection
from prandtl import prandtlCorrection

##############################################################################
def bemLoop(Uinf, ti, omega, Nbl, airDensity, twistDist, chordDist, alpha_data, lift_data, drag_data, rNodes, rMidNodes, R, Rst, rel_err=1e-3, max_iter=100, verbose=True):
    # Define initial conditions
    a0 = 0.3*np.ones(rMidNodes.shape)
    ap0 = 0.0*np.ones(rMidNodes.shape)

    # Start Loop
    count = 0
    while True:
        print(a0)
        a1, ap1 = calcualte_induced_velocities(Uinf, ti, Nbl, R, Rst, rMidNodes, omega, alpha_data, lift_data, drag_data, chordDist, twistDist, airDensity, a0.copy(), ap0.copy())
        
        # Calcualte errors
        a_err = np.max(np.abs(a1-a0))
        ap_err = np.max(np.abs(ap1-ap0))

        if verbose:
            print(f"Iteration: {count:d} - A.Err: {a_err:0.6f} - Ap.Err: {ap_err:0.6f}")

        # Check for convergence
        if a_err < rel_err and ap_err < rel_err:
            break

        if count > max_iter:
            plt.plot(rMidNodes, a1, label="a")
            plt.plot(rMidNodes, ap1, label="ap")
            plt.legend()
            plt.show()
            raise ValueError("Maximum iterations exceed.")
        
        # Advance new iteration
        count += 1
        a0 = 0.25*a1 + 0.75*a0
        ap0 = 0.25*ap1 + 0.75*ap0

        pos = a0 > 0.95
        a0[pos] = 0.95

    # Calculate CT and Cp
    uNorm, uTang = calculate_velocity(Uinf, rMidNodes, omega, a1, ap1)
    fN, fTan = computeAirfoilLoad(uNorm, uTang, alpha_data, lift_data, drag_data, chordDist, twistDist, airDensity)

    dr = rNodes[1:]-rNodes[:-1]
    Ct = Nbl*np.sum(fN*dr)/0.5/airDensity/Uinf**2.0/np.pi/R**2.0
    Cp = Nbl*np.sum(fTan*rMidNodes*dr)*omega/0.5/airDensity/Uinf**3.0/np.pi/R**2.0

    print("CT: ", Ct)
    print("CP: ", Cp)

    plt.plot(rMidNodes, a1, label="a")
    plt.plot(rMidNodes, ap1, label="ap")
    plt.legend()
    plt.show()

    return a1, ap1

def calculate_velocity(uInf, r, omega, a, ap):
    uNorm = uInf*(1-a)
    uTang = r*omega*(1+ap)

    return uNorm, uTang

def calcualte_induced_velocities(Uinf, ti, Nbl, R, Rst, rMidNodes, omega, alpha_data, lift_data, drag_data, chordDist, twistDist, airDensity, a0, ap0):
    # Calculate relative velocity
    uNorm, uTang = calculate_velocity(Uinf, rMidNodes, omega, a0, ap0)

    # Calculate loads
    fN, fTan = computeAirfoilLoad(uNorm, uTang, alpha_data, lift_data, drag_data, chordDist, twistDist, airDensity)

    # Calculate thrust coefficient
    ct = fN*Nbl/0.5/airDensity/Uinf**2.0/2/np.pi/rMidNodes

    # Correct with Glauert
    a0 = glauertCorrection(ct)
    ap0 = fTan*Nbl/airDensity/4/np.pi/Uinf**2.0/(1-a0)/ti/(rMidNodes**2.0/R)

    # Correct with Pradtl
    pcr = prandtlCorrection(Nbl, ti, R, rMidNodes, Rst, a0)
    a1 = a0/pcr
    ap1 = ap0/pcr

    return a1, ap1
