import bpy
import sys
import os

dir = os.path.dirname("/home/mark/Scripts/Blender/")
if not dir in sys.path:
    sys.path.append(dir )

from BlenderUtilities.Blender_Utilities import *

def NewIcosphere():
    bpy.ops.mesh.primitive_ico_sphere_add(radius=1,enter_editmode=False,align='WORLD',
                                          location=(0,0,0),scale=(1,1,1))
    return bpy.context.active_object
    
def ScaleObject(obj,multiplier):
    (x,y,z) = obj.scale
    obj.scale = (x*multiplier,y*multiplier,z*multiplier)

def BackgroundContainer():
    BGIco = NewIcosphere()
    ScaleObject(BGIco,20.0)
    BGIco.name="Background_Isosphere"
    bpy.ops.object.modifier_add(type='SUBSURF')
    bpy.context.object.modifiers["Subdivision"].levels = 0
    bpy.context.object.modifiers["Subdivision"].render_levels = 3
    bgmat = CreateMaterial(MatName="BGShiny",HexColor="#FFFFFF",Roughness=0,Metallic=1.0)
    AddMaterialToObject(BGIco,bgmat)

InitialSetup()
BackgroundContainer()
