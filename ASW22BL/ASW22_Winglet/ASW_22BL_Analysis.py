# ASW 22BL With Winglets, Empennage and Control Surfaces
# ANALYSIS Script
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
from SUAVE.Core import (Data, Container)

def vehicle_setup():

    vehicle = SUAVE.vehicle()

    vehicle.name = "ASW_22BL"

    