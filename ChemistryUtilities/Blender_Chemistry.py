import bpy
import math
from ..BlenderUtilities import *

def AddAtom(element,x,y,z,index):
    bpy.ops.mesh.primitive_uv_sphere_add(radius=1, enter_editmode=False, align='WORLD', location=(x, y, z), scale=(0.1, 0.1, 0.1))
    atom = bpy.context.active_object
    atom.name=f"{element}_{index}"
    AddMaterialToObject(atom,bpy.data.materials[element])
    return atom

def cylinder_between(start,end,r):
    x1,y1,z1 = start
    x2,y2,z2 = end
    dx = x2 - x1
    dy = y2 - y1
    dz = z2 - z1    
    dist = math.sqrt(dx**2 + dy**2 + dz**2)
    bpy.ops.mesh.primitive_cylinder_add(
      radius = r, 
      depth = dist,
      location = (dx/2 + x1, dy/2 + y1, dz/2 + z1)   
    ) 
    phi = math.atan2(dy, dx) 
    theta = math.acos(dz/dist) 
    bpy.context.object.rotation_euler[1] = theta 
    bpy.context.object.rotation_euler[2] = phi 
    cyl = bpy.context.active_object
    return cyl

def AddBond(i_atom,i,j_atom,j):
    ## create cylinder of radius 0.1 (same as scale of atoms above)
    i_element = i_atom[0]
    j_element = j_atom[0]
    i_start = [ float(i_atom[1]) , float(i_atom[2]) , float(i_atom[3])]
    j_start = [ float(j_atom[1]) , float(j_atom[2]) , float(j_atom[3])]
    midpoint = [ 0.5*j_start[0] + 0.5*i_start[0] , 0.5*j_start[1] + 0.5*i_start[1] , 0.5*j_start[2] + 0.5*i_start[2] ]
    # Make i_atom bond
    i_bond = cylinder_between(i_start, midpoint, 0.1)
    i_bond.name=f"{i_element}_{i+1}_{j_element}_{j+1}_a"
    AddMaterialToObject(i_bond,bpy.data.materials[i_element])
    # Make j_atom bond        
    j_bond = cylinder_between(j_start, midpoint, 0.1)
    j_bond.name=f"{i_element}_{i+1}_{j_element}_{j+1}_b"
    AddMaterialToObject(j_bond,bpy.data.materials[j_element])
    return [i_bond,j_bond]


elemental_colors = {"H": "#FFFFFF","He": "#D9FFFF","Li": "#CC80FF","Be": "#C2FF00",
"B": "#FFB5B5","C": "#909090","N": "#3050F8","O": "#FF0D0D",
"F": "#90E050","Ne": "#B3E3F5","Na": "#AB5CF2","Mg": "#8AFF00",
"Al": "#BFA6A6","Si": "#F0C8A0","P": "#FF8000","S": "#FFFF30",
"Cl": "#1FF01F","Ar": "#80D1E3","K": "#8F40D4","Ca": "#3DFF00",
"Sc": "#E6E6E6","Ti": "#BFC2C7","V": "#A6A6AB","Cr": "#8A99C7",
"Mn": "#9C7AC7","Fe": "#E06633","Co": "#F090A0","Ni": "#50D050",
"Cu": "#C88033","Zn": "#7D80B0","Ga": "#C28F8F","Ge": "#668F8F",
"As": "#BD80E3","Se": "#FFA100","Br": "#A62929","Kr": "#5CB8D1",
"Rb": "#702EB0","Sr": "#00FF00","Y": "#94FFFF","Zr": "#94E0E0",
"Nb": "#73C2C9","Mo": "#54B5B5","Tc": "#3B9E9E","Ru": "#248F8F",
"Rh": "#0A7D8C","Pd": "#006985","Ag": "#C0C0C0","Cd": "#FFD98F",
"In": "#A67573","Sn": "#668080","Sb": "#9E63B5","Te": "#D47A00",
"I": "#940094","Xe": "#429EB0","Cs": "#57178F","Ba": "#00C900",
"La": "#70D4FF","Ce": "#FFFFC7","Pr": "#D9FFC7","Nd": "#C7FFC7",
"Pm": "#A3FFC7","Sm": "#8FFFC7","Eu": "#61FFC7","Gd": "#45FFC7",
"Tb": "#30FFC7","Dy": "#1FFFC7","Ho": "#00FF9C","Er": "#00E675",
"Tm": "#00D452","Yb": "#00BF38","Lu": "#00AB24","Hf": "#4DC2FF",
"Ta": "#4DA6FF","W": "#2194D6","Re": "#267DAB","Os": "#266696",
"Ir": "#175487","Pt": "#D0D0E0","Au": "#FFD123","Hg": "#B8B8D0",
"Tl": "#A6544D","Pb": "#575961","Bi": "#9E4FB5","Po": "#AB5C00",
"At": "#754F45","Rn": "#428296","Fr": "#420066","Ra": "#007D00",
"Ac": "#70ABFA","Th": "#00BAFF","Pa": "#00A1FF","U": "#008FFF",
"Np": "#0080FF","Pu": "#006BFF","Am": "#545CF2","Cm": "#785CE3",
"Bk": "#8A4FE3","Cf": "#A136D4","Es": "#B31FD4","Fm": "#B31FBA",
"Md": "#B30DA6","No": "#BD0D87","Lr": "#C70066","Rf": "#CC0059",
"Db": "#D1004F","Sg": "#D90045","Bh": "#E00038","Hs": "#E6002E",
"Mt": "#EB0026"}

for element,color in elemental_colors.items():
    CreateMaterial(MatName=element,
                   HexColor=color,
                   Transmission=0.0,
                   IOR=1.45,
                   Roughness=0.0,
                   EmissionColor=color,
                   EmissionStrength=0.01,
                   Transparency=1.0,
                   Metallic=1.0)

