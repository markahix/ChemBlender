import bpy
import os
import sys
import numpy as np
import math
sys.path.append("/home/mark/Scripts/Blender")
from MoldenUtilities.Molden_FileParser import *
from BlenderUtilities.Blender_Utilities import *
from ChemistryUtilities.Blender_Chemistry import *

for i in range(1,10):
    moldenfile = "/home/mark/Projects/OrbitalMovies/TEST_Moldens/GFP.molden." + str(i)
    MoldenLicorice(moldenfile)
