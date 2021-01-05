# ASW 22BL With Winglets, Empennage and Control Surfaces
# GEOMETRY FILE
#
#   Developed by Thomas V. Greenhill
#
#   History:
#       01.05.2020 Created and Debugged, TVG
#
#   Notes:


import numpy as np
import SUAVE
from SUAVE.Core import Units


# Vehicle Definition

def vehicle_setup():
    vehicle = SUAVE.Vehicle()
    vehicle.tag = 'ASW_22BL_Tips_Tail_Surfaces'
    
    ## Mass Properties
    vehicle.mass_properties.mass = 850 #kg
    vehicle.mass_properties.center_of_gravity = 0.3 #m (SUPER APPROXIMATE, REVISE LATER)

    ## Neglect moments of inertia

    ## Main Wing
    wing = SUAVE.Components.Wings.Main_Wing()
    wing.tag = 'wing'

    wing.aspect_ratio       = 

    print(vehicle)

vehicle_setup()