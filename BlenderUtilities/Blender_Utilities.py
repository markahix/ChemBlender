# This is my Blender Utilities, a collection of QOL functions I've made for myself.
# Mark A. Hix, October 31, 2022

import bpy
import os
from .Blender_Materials import *
import numpy as np

def InitialSetup(outputdir=os.getenv("HOME")):
    ### Make Background transparent (good for overlays)
    bpy.context.scene.render.film_transparent = True

    ### Output Format and Filepath
    bpy.context.scene.render.image_settings.file_format = 'FFMPEG'
    bpy.context.scene.render.filepath = outputdir
    print("Output File Location: ", bpy.context.scene.render.filepath)

    ### Set Animation end frame to n_frames
    frames_per_second  = 30 #framerate of animation
    animation_duration = 10 ##integer in seconds
    bpy.context.scene.frame_end = frames_per_second * animation_duration

    ### Set Renderer to Cycles with GPU support
    bpy.context.scene.render.engine = 'CYCLES'
    bpy.context.scene.cycles.samples = 4096
    bpy.context.scene.cycles.device = 'GPU'

def LoadSTLwithMaterial(STL_file,material):
    name = STL_file.split("/")[-1].replace(".stl","")
    bpy.ops.import_mesh.stl(filepath=STL_file)
    curr_scene = bpy.context.scene
    obj = curr_scene.objects[name]
    AddMaterialToObject(obj,material)
    return obj

def SubdivideSurface():
    bpy.ops.object.modifier_add(type='SUBSURF')
    bpy.context.object.modifiers["Subdivision"].levels = 0
    bpy.context.object.modifiers["Subdivision"].render_levels = 2
    
def CreateNewCollection(collection_name,owner=None):
    coll = bpy.data.collections.new(collection_name)
    if owner == None:
        bpy.context.scene.collection.children.link(coll)
    else:
        owner.children.link(coll)
    return coll
    
def Add_Center_Of_Collection(collection):
    [x,y,z] = [0,0,0]
    i=0
    for obj in collection.all_objects:
        x+=obj.location[0]
        y+=obj.location[1]
        z+=obj.location[2]
        i+=1
    bpy.ops.object.empty_add(type='PLAIN_AXES', align='WORLD', location=(x/i, y/i, z/i), scale=(1, 1, 1))
    plain_axes = bpy.context.active_object
    plain_axes.name="GeometricCenterOfCollection"
    collection.objects.link(plain_axes)
    bpy.data.collections["Collection"].objects.unlink(plain_axes)
    return plain_axes

def JoinCollectionToOneMesh(collection):
    for obj in collection.all_objects:
        obj.select_set(True)
    bpy.ops.object.join()
    curr_obj = bpy.context.active_object
    curr_obj.name = collection.name
    return curr_obj


def GeometricCenterofObject(object):
    x = np.median([x.co[0] for x in object.data.vertices])
    y = np.median([x.co[1] for x in object.data.vertices])
    z = np.median([x.co[2] for x in object.data.vertices])
    return (x,y,z)

def TrackCameraToObject(object):
    camera = bpy.context.scene.objects["Camera"]
    ttc = camera.constraints.new(type='TRACK_TO')
    ttc.target = object