# This program is designed to be run from inside Blender (tested with 3.3.0),
# and with access to VMD (tested with 1.9.3).  Open from the "Scripting" tab in Blender.
# The section labeled "USER_PROVIDED_VALUES" is the only thing that will need to be
# modified by the end user, but I can't really stop you if you go beyond that.
# Give this program the location of your Molden files (generated by each step of a 
# QM or QM/MM optimization or molecular dynamics simulation), and a few other parameters
# such as the orbital number you want to visualize and the colors you want to use 
# (HEX Colors ONLY). This program will process the Molden files to ensure they're all in
# phase, then render them into STL format for use in Blender (by way of VMD).  Blender 
# will load the orbitals (both phases as independent objects) and the stick structure
# for each frame, building the animation iteratively and assigning the appropriate materials.
#
# Mark A. Hix, October 31, 2022

import bpy
from glob import glob as G
import os
import numpy as np
import subprocess
import sys

dir = os.path.dirname("/home/mark/Scripts/Blender/")
if not dir in sys.path:
    sys.path.append(dir )

from BlenderUtilities.Blender_Utilities import *
from MoldenUtilities.Molden_FileParser import *
from VMDUtilities.VMD_Utilities import *

### USER_PROVIDED_VALUES ###
# Where your collection of molden files are stored.
molden_path = "/home/mark/Projects/OrbitalMovies/Test_GFP_System_100steps/MoldenFilesForTesting/"

# Where you want the STL files stored (for good computational housekeeping)
STL_Filepath = molden_path+"STL_Files/"

# Where the movie will be rendered.
output_folder = "/home/mark/Documents/"  

# Orbital number you want visualized.
orbital_number = 82
 
# If you're also loading in a prmtop/dcd combo for full protein environment visualization.
prmtop = None     ### Must be None, "", or an actual filename.
trajectory = None ### Must be None, "", or an actual filename.

# doesn't really matter, but if you want to keep the file for some reason...
# idk just leave this alone tbh.  
vmd_command_file = "blender_orbital_STL.vmd"  

# Visualization Parameters
up_orbital_color = 745   ## MUST BE HEX COLORS OR WAVELENGTHS (380 nm through 750 nm)
down_orbital_color = 395 ## MUST BE HEX COLORS OR WAVELENGTHS (380 nm through 750 nm)
BG_TRANSPARENT = True ### Make background transparent (good for overlays)
cycles_sampling_level = 1024 ### Ultra-high would be like 4096, but 1024 or 2048 is fine usually

# Make or Remake STL files - set to False if you already have the STL files from a previous run.
Generate_STL_Files = True

### BEGIN PROCESSING
fullpath = os.path.abspath(molden_path)
STL_Folder = os.path.abspath(STL_Filepath)
Use_NewC = False
if all([prmtop != None,prmtop!="",trajectory != None,trajectory!=""]):
    Use_NewC = True
    

if Generate_STL_Files:
    VMD_Job_Writer(fullpath, int(orbital_number), prmtop=prmtop,trajectory=trajectory, vmdcommandfile=vmd_command_file,STL_Filepath = STL_Filepath)
    
    ## Run VMD Command File with VMD.
    subprocess.call(f"mkdir -p {STL_Folder}",shell=True)
    subprocess.call(f"vmd -e {vmd_command_file}",shell=True)

LIC_FILES   = G(STL_Folder + "/*Licorice.stl")
LIC_FILES.sort(key=os.path.getmtime)
UP_FILES    = G(STL_Folder + "/*Phase_Up.stl")
UP_FILES.sort(key=os.path.getmtime)
DOWN_FILES  = G(STL_Folder + "/*Phase_Down.stl")
DOWN_FILES.sort(key=os.path.getmtime)
if Use_NewC:
    NEWC_FILES  = G(STL_Folder + "/*NewCartoon.stl")
    n_files = min(len(LIC_FILES),len(UP_FILES),len(DOWN_FILES),len(NEWC_FILES))
else:
    n_files = min(len(LIC_FILES),len(UP_FILES),len(DOWN_FILES))

### Define necessary materials
# NewCartoon Material
NewC_Mat  = CreateMaterial(MatName="NewCartoon Material",HexColor="#00FF00",Metallic=0.6,Transparency=0.3,Transmission=1.0)

# Licorice Material
Lic_Mat  = CreateMaterial(MatName="Licorice_Material",Roughness=0.0,Metallic=0.6)

# Phase Up Material
Up_Mat   = CreateMaterial(MatName="Phase_Up_Material",
               HexColor=up_orbital_color,
               Transmission=1.0,
               IOR=1.05,
               Roughness=0.0,
               EmissionColor=up_orbital_color,
               EmissionStrength=0.2,
               Transparency=0.5)

# Phase Down Material
Down_Mat = CreateMaterial(MatName="Phase_Down_Material",
               HexColor=down_orbital_color,
               Transmission=1.0,
               IOR=1.05,
               Roughness=0.0,
               EmissionColor=down_orbital_color,
               EmissionStrength=0.2,
               Transparency=0.5)    

InitialSetup()

### Run through all STL files from the VMD STL Generator Script
for i in range(n_files):
    print("Loading File #",i,"in sequence...")
    # Load STL file with Material
    curr_lic = LoadSTLwithMaterial(LIC_FILES[i],Lic_Mat)
    SubdivideSurface()
    curr_up = LoadSTLwithMaterial(UP_FILES[i],Up_Mat)
    curr_down = LoadSTLwithMaterial(DOWN_FILES[i],Down_Mat)     
    
    ### Show object only on relevant frame number.
    HideObjectKeyframe(curr_lic,i+1)    
    HideObjectKeyframe(curr_up,i+1)
    HideObjectKeyframe(curr_down,i+1)
    
    # Only if using New Cartoon STL (from protein)
    if Use_NewC:
        curr_newc = LoadSTLwithMaterial(NEWC_FILES[i],Lic_Mat)
        HideObjectKeyframe(curr_newc,i+1)
