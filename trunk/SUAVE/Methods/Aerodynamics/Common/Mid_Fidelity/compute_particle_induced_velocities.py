## @ingroup Methods-Aerodynamics-Common-Mid_Fidelity
# compute_particle_induced_velocities.py
# 
# Created:  Dec 2020, R. Erhard
#           

# ----------------------------------------------------------------------
#  Imports
# ----------------------------------------------------------------------

# package imports 
import numpy as np 
from SUAVE.Core import Data



# This script is used for the viscous Vortex Particle Method (vVPM).
# It consists of the evaluation of the induced velocity using the Biot-Savart kernel.


def compute_particle_induced_velocities(x, particles):
    """Computes the velocities induced by the vortex particles at the control points x  

    Assumptions:
    None

    Source:
    1. Winckelmans, G. S., "Topics in vortex methods for the computation of three- and two-
    dimensional incompresible unsteady flows," PhD Thesis, California Institute of Technology,
    Febrauary 1989.
    
    2. Alvarex, E., and Ning, A., "Development of a Vortex Particle Code for the Modeling of 
    Wake Interaction in Distributed Propulsion," AIAA Applied Aerodynamics Conference, Atlanta,
    GA, June 2018. 

    Inputs:
    particles.
       positions
       strengths
       
    Outputs:                                   
    u

    Properties Used:
    N/A
    """ 
    
    x_p = particles.positions
    gamma_p = particles.strengths # at time t
    
    # Using the regularized kernel proposed by Winckelmans and Leonard:
    sigma = 0.1 # smoothing radius from core of vortex blob
    r = x-x_p
    r_sigma = r/sigma
    K = -r*(r_sigma**2+(5/2)) / (4*np.pi*sigma**3*(r_sigma**2+1)**(5/2))
    
    # Velocities induced at given locations and at time t by the vortex particles at locations xp
    u = np.sum(K*gamma_p)
    
    
    return u