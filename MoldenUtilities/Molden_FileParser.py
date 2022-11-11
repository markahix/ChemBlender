## This is a set of functions to process/parse Molden Files.

import numpy as np
import os
import bpy
from ..BlenderUtilities.Blender_Utilities import *
from ..ChemistryUtilities import *

print("""Functions in Molden_Utilities.py:
--------------------------------------------------------
Get_Atoms(moldenfile)
Get_Gaussian_Type_Orbitals(moldenfile)
Get_Molecular_Orbitals(moldenfile)
Get_Sign_Array(first_molden_file,second_molden_file)
Write_Phase_Swapped_Molden(moldenfile,sign_array)
MoldenPhaseChecker(molden_location)
""")


def Get_Atoms(moldenfile):
    with open(moldenfile) as f:
        lines = f.readlines()
    capture=False
    atoms = []
    for line in lines:
        if "[GTO]" in line:
            capture = False
        if capture:
            splitline = line.split()
            atoms.append([splitline[0],splitline[3],splitline[4],splitline[5]])
        if "[Atoms]" in line:
            capture = True
    return atoms
    
def Get_Gaussian_Type_Orbitals(moldenfile):
    with open(moldenfile) as f:
        lines = f.readlines()
    orbitals_information = []
    capture = False
    new_orb = []
    for line in lines:
        if "[MO]" in line:
            capture = False
            orbitals_information.append(new_orb)
        if capture:
            if line == "\n":
                pass
            elif line[4] != " ":
                pass
            elif line[1] != " ":
                splitline = line.split()
                orbital=splitline[0]
                orbitals_information.append(new_orb)
                new_orb = [orbital]
            else:
                splitline = line.split()
                exponent_primitive = splitline[0]
                contraction_coeff = splitline[1]
                new_orb.append(exponent_primitive)
                new_orb.append(contraction_coeff)
        if "[GTO]" in line:
            capture = True
    return orbitals_information    
    

def Get_Molecular_Orbitals(moldenfile):
    with open(moldenfile) as f:
        lines = f.readlines()
    ene_lines = []
    for i,line in enumerate(lines):
        if "Ene=" in line:
            ene_lines.append(i)
    mol_orbs = []
    n_orbs   = len(ene_lines)
    for i in range(n_orbs-1):
        orb = []
        for line in lines[ene_lines[i]+3:ene_lines[i+1]]:
            orb.append(float(line.split()[-1]))
        mol_orbs.append(orb)
    orb = []
    for line in lines[ene_lines[n_orbs-1]+3:]:
        orb.append(float(line.split()[-1]))
    mol_orbs.append(orb)
    return mol_orbs

def Get_Sign_Array(OLD_MOL_FILE,NEW_MOL_FILE):
    old_mol_orbs = Get_Molecular_Orbitals(OLD_MOL_FILE)
    new_mol_orbs = Get_Molecular_Orbitals(NEW_MOL_FILE)
    sign_array = []
    for i in range(len(old_mol_orbs)):
        sign_array.append(np.sign(np.dot(old_mol_orbs[i],new_mol_orbs[i])))
    return sign_array

def Write_Phase_Swapped_Molden(moldenfile,sign_array):
    with open(moldenfile) as f:
        newlines = f.readlines()
    with open(moldenfile,"w") as f:
        for i,line in enumerate(newlines):
            f.write(line)
            if "[MO]" in line:
                break
        start_mo_lines = i+1
        ene_lines_encountered = -1
        for line in newlines[start_mo_lines:]:
            if "Ene=" in line:
                ene_lines_encountered += 1
                f.write(line)
            elif "Spin=" in line:
                f.write(line)
            elif "Occup=" in line:
                f.write(line)
            else:
                templine = line.split()
                if sign_array[ene_lines_encountered] == -1:
                    if "-" in templine[1]:
                        templine[1] = templine[1].replace("-"," ")
                    else:
                        templine[1] = "-"+templine[1].strip()
                newline = f"{templine[0]:>5}{float(templine[1]):>11.05f}\n"
                f.write(newline)
    return None
                
def MoldenPhaseChecker(molden_location):
    ORDERED_MOLDEN_FILELIST=[]
    startdir = os.getcwd()
    os.chdir(molden_location)
    file_list = G("*.molden.*")
    file_list.sort(key=os.path.getmtime)
    n_moldens = len(file_list)
    os.makedirs("phased_molden_files/",exist_ok=True)
    os.system(f"cp *.molden.* phased_molden_files/")
    for i in range(n_moldens-1):
        OLD_MOL_FILE="phased_molden_files/"+file_list[i]
        NEW_MOL_FILE="phased_molden_files/"+file_list[i+1]
        sign_array = Get_Sign_Array(OLD_MOL_FILE,NEW_MOL_FILE)
        Write_Phase_Swapped_Molden(NEW_MOL_FILE,sign_array)
        ORDERED_MOLDEN_FILELIST.append(os.path.abspath(OLD_MOL_FILE))
    ORDERED_MOLDEN_FILELIST.append(os.path.abspath(NEW_MOL_FILE))
    os.chdir(startdir)
    return ORDERED_MOLDEN_FILELIST
    
