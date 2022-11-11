import bpy
from glob import glob as G
import os


### USER_PROVIDED_VALUES ###
STL_Folder = "/home/mark/Projects/OrbitalMovies/Test_GFP_System_100steps/scr.GFP/"


LIC_FILES   = G(STL_Folder + "*Licorice.stl")
LIC_FILES.sort(key=os.path.getmtime)
UP_FILES    = G(STL_Folder + "*Phase_Up.stl")
UP_FILES.sort(key=os.path.getmtime)
DOWN_FILES  = G(STL_Folder + "*Phase_Down.stl")
DOWN_FILES.sort(key=os.path.getmtime)
NEWC_FILES  = G(STL_Folder + "*NewCartoon.stl")
n_files = min(len(LIC_FILES),len(UP_FILES),len(DOWN_FILES),len(NEWC_FILES))

### Define necessary materials
# NewCartoon Material
NewC_Mat  = bpy.data.materials.new(name="NewCartoon Material")
NewC_Mat.use_nodes=True
# Base Color = White
NewC_Mat.node_tree.nodes["Principled BSDF"].inputs[0].default_value = (0, 1, 0, 1)
# Roughness = 0.00
NewC_Mat.node_tree.nodes["Principled BSDF"].inputs[9].default_value = 0
# Metallic = 0.6
NewC_Mat.node_tree.nodes["Principled BSDF"].inputs[6].default_value = 0.6
# Change transparency of object
NewC_Mat.node_tree.nodes["Principled BSDF"].inputs[21].default_value = 0.3
# Transmission = 100%
NewC_Mat.node_tree.nodes["Principled BSDF"].inputs[17].default_value = 1.0


# Licorice Material
Lic_Mat  = bpy.data.materials.new(name="Licorice_Material")
Lic_Mat.use_nodes=True
# Base Color = White
Lic_Mat.node_tree.nodes["Principled BSDF"].inputs[0].default_value = (0.1, 0.1, 0.1, 1)
# Roughness = 0.00
Lic_Mat.node_tree.nodes["Principled BSDF"].inputs[9].default_value = 0
# Metallic = 0.6
Lic_Mat.node_tree.nodes["Principled BSDF"].inputs[6].default_value = 0.6


# Phase Up Material
Up_Mat   = bpy.data.materials.new(name="Phase_Up_Material")
Up_Mat.use_nodes=True
# Base Color = Red
Up_Mat.node_tree.nodes["Principled BSDF"].inputs[0].default_value = (1, 0, 0, 1)
# Transmission = 85%
Up_Mat.node_tree.nodes["Principled BSDF"].inputs[17].default_value = 1.0
# Index of Refraction = 1.05
Up_Mat.node_tree.nodes["Principled BSDF"].inputs[16].default_value = 1.05
# Roughness = 0.00
Up_Mat.node_tree.nodes["Principled BSDF"].inputs[9].default_value = 0
# Emission Color = Red
Up_Mat.node_tree.nodes["Principled BSDF"].inputs[19].default_value = (.1, 0, 0, 1)
# Emission Strength = 0.1
Up_Mat.node_tree.nodes["Principled BSDF"].inputs[20].default_value = 0.2
# Change transparency of object
Up_Mat.node_tree.nodes["Principled BSDF"].inputs[21].default_value = 0.5


# Phase Down Material
Down_Mat = bpy.data.materials.new(name="Phase_Down_Material")
Down_Mat.use_nodes=True
# Base Color = Blue
Down_Mat.node_tree.nodes["Principled BSDF"].inputs[0].default_value = (0, 0, 1, 1)
# Transmission = 85%
Down_Mat.node_tree.nodes["Principled BSDF"].inputs[17].default_value = 1.0
# Index of Refraction = 1.05
Down_Mat.node_tree.nodes["Principled BSDF"].inputs[16].default_value = 1.05
# Roughness = 0.00
Down_Mat.node_tree.nodes["Principled BSDF"].inputs[9].default_value = 0
# Emission Color = Blue
Down_Mat.node_tree.nodes["Principled BSDF"].inputs[19].default_value = (0, 0, .1, 1)
# Emission Strength = 0.1
Down_Mat.node_tree.nodes["Principled BSDF"].inputs[20].default_value = 0.2
# Change transparency of object
Down_Mat.node_tree.nodes["Principled BSDF"].inputs[21].default_value = 0.5



### Make Background transparent (good for overlays)
#bpy.context.scene.render.film_transparent = True

### Output Format and Filepath
bpy.context.scene.render.image_settings.file_format = 'FFMPEG'
bpy.context.scene.render.filepath = "/home/mark/Documents/"


### Set Animation end frame to n_frames
bpy.context.scene.frame_end = n_files

### Set Renderer to Cycles with GPU support
bpy.context.scene.render.engine = 'CYCLES'
bpy.context.scene.cycles.device = 'GPU'




### Add Material to Object, with quick check.
def AddMaterialToObject(obj,mat):
    if obj.data.materials:
        # assign to 1st material slot
        obj.data.materials[0] = mat
    else:
        # no slots
        obj.data.materials.append(mat)

### Show the object for exactly one frame
def HideObjectKeyframe(obj,frame_number):
    # Hide the object from the start of the scene until the desired frame number
    # Keyframes from 0 to T-1 to ensure it remains hidden the entire time.
    obj.hide_render = True
    obj.keyframe_insert(data_path="hide_render",frame=0)
    obj.keyframe_insert(data_path="hide_render",frame=frame_number-1)
    # Display the object for frame T and save keyframe.
    obj.hide_render = False
    obj.keyframe_insert(data_path="hide_render",frame=frame_number)
    # Hide object again at frame T+1 and save keyframe.
    obj.hide_render = True
    obj.keyframe_insert(data_path="hide_render",frame=frame_number+1)
    
### Run through all STL files from the VMD STL Generator Script
for i in range(n_files):
    ### Assign filenames for current iteration
    file_curr_lic  = LIC_FILES[i]
    file_curr_up   = UP_FILES[i]
    file_curr_down = DOWN_FILES[i]
    file_curr_newc = NEWC_FILES[i]
    
    ### Generate Unique Object Names
    name_curr_lic  = file_curr_lic.split("/")[-1].replace(".stl","")
    name_curr_up   = file_curr_up.split("/")[-1].replace(".stl","")
    name_curr_down = file_curr_down.split("/")[-1].replace(".stl","")
    name_curr_newc = file_curr_newc.split("/")[-1].replace(".stl","")
    
    ### Import STL files
    bpy.ops.import_mesh.stl(filepath=file_curr_lic)
    bpy.ops.import_mesh.stl(filepath=file_curr_up)
    bpy.ops.import_mesh.stl(filepath=file_curr_down)
    bpy.ops.import_mesh.stl(filepath=file_curr_newc)
    
    ### Define objects for next steps.
    curr_scene = bpy.context.scene
    curr_lic = curr_scene.objects[name_curr_lic]
    curr_up = curr_scene.objects[name_curr_up]
    curr_down = curr_scene.objects[name_curr_down]
    curr_newc = curr_scene.objects[name_curr_newc]
    
    ### Add Materials to new objects
    AddMaterialToObject(curr_lic,Lic_Mat)
    AddMaterialToObject(curr_up,Up_Mat)
    AddMaterialToObject(curr_down,Down_Mat)    
    AddMaterialToObject(curr_newc,NewC_Mat)    
    
    ### Show object only on relevant frame number.
    HideObjectKeyframe(curr_lic,i+1)    
    HideObjectKeyframe(curr_up,i+1)
    HideObjectKeyframe(curr_down,i+1)
    HideObjectKeyframe(curr_newc,i+1)

