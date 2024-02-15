vmec2stl.py takes a vmec file (the standard specification file for the geometry of a stellator, as input to the vmec code) and writes the points to a .scad file which can be opened with e.g. OpenSCAD; and then can be converted to an e.g. .stl file to be 3D printed.

for vmec file examples see https://github.com/PlasmaControl/DESC/blob/master/examples/VMEC/ e.g. input.NCSX for the Princeton NCSX up-down symmetric stellarator
for vmec file explanation see https://princetonuniversity.github.io/STELLOPT/VMEC

there are also functions for making the Princeton Dee, the type of toroidal magnetic field coil used in most tokamaks to minimize the amount of stress on the coils, see http://www.jaschwartz.net/journal/princeton-dee.html