import bpy
from ..BlenderUtilities.Blender_Utilities import *
from ..ChemistryUtilities import *
from .Molden_FileParser import *

def MoldenLicorice(moldenfile,collection=None):
    bpy.context.scene.collection.children.link(bpy.data.collections.new(moldenfile.split("/")[-1]))
    molden_coll = bpy.context.scene.collection.children[moldenfile.split("/")[-1]]
    main_coll = bpy.data.collections["Collection"]
    atoms = Get_Atoms(moldenfile)
    for i,atom in enumerate(atoms):
        element=atom[0]
        x = float(atom[1])
        y = float(atom[2])
        z = float(atom[3])
        index=i+1
        atom = AddAtom(element,x,y,z,index)
        molden_coll.objects.link(atom)
        try:
            main_coll.objects.unlink(atom)
        except:
            pass
    for i, i_atom in enumerate(atoms):
        x_i = float(i_atom[1])
        y_i = float(i_atom[2])
        z_i = float(i_atom[3])
        for j,j_atom in enumerate(atoms):
            if j>i:
                x_j = float(j_atom[1])
                y_j = float(j_atom[2])
                z_j = float(j_atom[3])
                bondlength = np.linalg.norm([x_j-x_i,y_j-y_i,z_j-z_i])
                if bondlength < 2.0:
                    if j_atom[0] == "H" or i_atom[0] == "H":
                        if bondlength < 1.4:
                            bonds = AddBond(i_atom,i,j_atom,j)
                            molden_coll.objects.link(bonds[0])
                            molden_coll.objects.link(bonds[1])
                            try:
                                main_coll.objects.unlink(bonds[0])
                                main_coll.objects.unlink(bonds[1])
                            except:
                                pass
                    else:
                        bonds = AddBond(i_atom,i,j_atom,j)
                        molden_coll.objects.link(bonds[0])
                        molden_coll.objects.link(bonds[1])
                        try:
                            main_coll.objects.unlink(bonds[0])
                            main_coll.objects.unlink(bonds[1])
                        except:
                            pass
    main_object = JoinCollectionToOneMesh(molden_coll)
    if collection != None:
        collection.objects.link(main_object)
        molden_coll.objects.unlink(main_object)
        bpy.data.collections.remove(molden_coll)
    return main_object
