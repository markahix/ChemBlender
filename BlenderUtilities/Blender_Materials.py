import bpy
from .Blender_Colors import *

def CreateMaterial(MatName="NewMaterial",HexColor="#FFFFFF",Transmission=0.0,IOR=1.45,Roughness=0.0,EmissionColor="#000000",EmissionStrength=0,Transparency=1.0,Metallic=0.0):
    # Creating Materials is such a process.  this function makes it a little easier to do.
    # I'll likely update this in the future with the full array of material options, or 
    # alternatively create a way to just import existing materials from a library or something.
    mat = bpy.data.materials.new(name=MatName)
    mat.use_nodes=True
    mat_r,mat_g,mat_b = generate_rgb(HexColor)
    em_r,em_g,em_b = generate_rgb(EmissionColor)
    mat.node_tree.nodes["Principled BSDF"].inputs[0].default_value = (mat_r,mat_g,mat_b, 1)
    mat.node_tree.nodes["Principled BSDF"].inputs[17].default_value = Transmission
    mat.node_tree.nodes["Principled BSDF"].inputs[16].default_value = IOR
    mat.node_tree.nodes["Principled BSDF"].inputs[9].default_value = Roughness
    mat.node_tree.nodes["Principled BSDF"].inputs[19].default_value = (em_r,em_g,em_b, 1)
    mat.node_tree.nodes["Principled BSDF"].inputs[20].default_value = EmissionStrength
    mat.node_tree.nodes["Principled BSDF"].inputs[21].default_value = Transparency
    mat.node_tree.nodes["Principled BSDF"].inputs[6].default_value = Metallic
    return mat

    
### Add Material to Object, with quick check.
def AddMaterialToObject(obj,mat):
    if obj.data.materials:
        # assign to 1st material slot
        obj.data.materials[0] = mat
    else:
        # no slots
        obj.data.materials.append(mat)