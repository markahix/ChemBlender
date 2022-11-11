def VMDInitialize(inputfilename):
    with open(inputfilename,"w") as f:
        f.write("display update on\n")
        f.write("color add item Display Background white\n")
        f.write("color Display Background white\n")
        f.write("display projection perspective \n")
        f.write("display culling off\n")
        f.write("axes location off\n")
        f.write("display rendermode Normal\n")
        f.write("display depthcue off\n")
        f.write("display resize 1920 1080\n")
    return None

def VMDLoadMoldens(vmdcommandfile,ORDERED_MOLDEN_FILELIST,orbital_number):
    with open(vmdcommandfile,"a") as f:
        num_moldens_loaded = 0
        for moldenfile in ORDERED_MOLDEN_FILELIST:
            if num_moldens_loaded == 0:
                f.write(f"mol new {moldenfile} type molden first 0 last -1 step 1 filebonds 1 autobonds 1 waitfor all\n")
            else:
                f.write(f"mol addfile {moldenfile} type molden first 0 last -1 step 1 filebonds 1 autobonds 1 waitfor all\n")
            num_moldens_loaded += 1
        f.write("mol delrep 0 top\n")
        f.write("mol representation Licorice 0.100000 30.000000 30.000000\n")
        f.write("mol selection {all}\n")
        f.write("mol addrep top\n")
        f.write("mol selupdate 0 top 0\n")
        f.write("mol colupdate 0 top 0\n")
        f.write("mol scaleminmax top 0 0.000000 0.000000\n")
        f.write("mol smoothrep top 0 0\n")
        f.write("mol drawframes top 0 {now}\n")
        f.write(f"mol representation Orbital 0.050000 {orbital_number} 0 0 0.050 1 6 0 0 1\n")
        f.write("mol selection {all}\n")
        f.write(f"mol addrep top\n")
        f.write(f"mol selupdate 1 top 0\n")
        f.write(f"mol colupdate 1 top 0\n")
        f.write(f"mol scaleminmax top 1 0.000000 0.000000\n")
        f.write(f"mol smoothrep top 1 0\n")
        f.write("mol drawframes top 1 {now}\n")
        f.write(f"mol representation Orbital -0.050000 {orbital_number} 0 0 0.050 1 6 0 0 1\n")
        f.write("mol selection {all}\n")
        f.write(f"mol addrep top\n")
        f.write(f"mol selupdate 1 top 0\n")
        f.write(f"mol colupdate 1 top 0\n")
        f.write(f"mol scaleminmax top 1 0.000000 0.000000\n")
        f.write(f"mol smoothrep top 1 0\n")
        f.write("mol drawframes top 1 {now}\n")
        f.write("mol showrep top 0 0\n")
        f.write("mol showrep top 1 0\n")
        f.write("mol showrep top 2 0\n")


def VMDLoadProtein(inputfilename,prmtop,trajectory):
    with open(inputfilename,"a") as f:
        f.write(f"mol new {prmtop} type parm7 first 0 last -1 step 1 filebonds 1 autobonds 1 waitfor all\n")
        f.write(f"mol addfile {trajectory} type dcd first 0 last -1 step 1 filebonds 1 autobonds 1 waitfor all\n")
        f.write(f"mol delrep 0 top\n")
        f.write(f"mol representation NewCartoon 0.300000 20.000000 4.100000 0\n")
        f.write(f"mol addrep top\n")
        f.write(f"mol selupdate 0 top 0\n")
        f.write(f"mol colupdate 0 top 0\n")
        f.write(f"mol scaleminmax top 0 0.000000 0.000000\n")
        f.write(f"mol smoothrep top 0 0\n")
        f.write("mol drawframes top 0 {now}\n")
        f.write("mol showrep top 0 0\n")
        
def VMDOrbitalstoSTLs(inputfilename,STL_Filepath):
    with open(inputfilename,"a") as f:
        f.write("""proc make_orbital_STL_files {} {
set num [molinfo top get numframes]
for {set i 0} {$i < $num} {incr i 1} {
animate goto $i
display update
# render licorice STL
set filename """+STL_Filepath+"""Frame_[format "%05d" [expr $i/1]]_Licorice.stl
mol showrep 0 0 1
render STL $filename true
mol showrep 0 0 0

# render Phase-Up STL
set filename """+STL_Filepath+"""Frame_[format "%05d" [expr $i/1]]_Phase_Up.stl
mol showrep 0 1 1
render STL $filename true
mol showrep 0 1 0

# render Phase-Down STL
set filename """+STL_Filepath+"""Frame_[format "%05d" [expr $i/1]]_Phase_Down.stl
mol showrep 0 2 1
render STL $filename true
mol showrep 0 2 0
}
}
make_orbital_STL_files
""")
        
def VMDProteintoSTLs(inputfilename,STL_Filepath):
    with open(inputfilename,"a") as f:
        f.write("""proc make_protein_STL_files {} {
set num [molinfo top get numframes]
for {set i 0} {$i < $num} {incr i 1} {
animate goto $i
display update
# render NewCartoon Protein STL
set filename """+STL_Filepath+"""Frame_[format "%05d" [expr $i/1]]_NewCartoon.stl
mol showrep 1 0 1
render STL $filename true
mol showrep 1 0 0
}
}
make_protein_STL_files
""")

def VMD_Job_Writer(ORDERED_MOLDEN_FILELIST,orbitalnumber,prmtop=None,trajectory=None,vmdcommandfile="orbital_trajectory.vmd",STL_Filepath="STL_Files/"):
    VMDInitialize(vmdcommandfile)
    VMDLoadMoldens(vmdcommandfile,ORDERED_MOLDEN_FILELIST,orbitalnumber)
    if prmtop != None and trajectory != None:
        VMDLoadProtein(vmdcommandfile,prmtop,trajectory)
    VMDOrbitalstoSTLs(vmdcommandfile,STL_Filepath)
    if prmtop != None and trajectory != None:
        VMDProteintoSTLs(vmdcommandfile,STL_Filepath)
    with open(vmdcommandfile,"a") as f:
        f.write("quit\n")

