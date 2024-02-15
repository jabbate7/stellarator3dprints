from scipy.integrate import odeint
from scipy.special import iv, modstruve
import numpy as np
import matplotlib.pyplot as plt
import re

#for vmec file examples see https://github.com/PlasmaControl/DESC/blob/master/examples/VMEC/
# e.g. input.NCSX for the Princeton NCSX up-down symmetric stellarator
#for vmec file explanation see https://princetonuniversity.github.io/STELLOPT/VMEC
vmec_file='input.NCSX'
output_file='ncsx.scad'
nPointsRadial=100
nPointsToroidal=120

#extract numerical parts from strings like "(11,-1)  = -1.40E+04"
base_regex=r"\((-?\d+)\s*,\s*(-?\d+)\)\s*=\s*(-?[\d.]+(?:[eE]-?\+?\d+)?)"
rbc_pattern="RBC"+base_regex
zbs_pattern="ZBS"+base_regex
nfp_pattern=r"NFP\s*=\s*(\d+)"
rbc_tuples=[]
zbs_tuples=[]
with open(vmec_file,'r') as f:
    for line in f:
        test_nfp=re.findall(nfp_pattern,line)
        if test_nfp:
            NFP=int(test_nfp[0])
        rbc_tuples.extend(re.findall(rbc_pattern,line))
        zbs_tuples.extend(re.findall(zbs_pattern,line))

def getPoints(phi, theta):
    def getPhase(n,m):
        return m*theta-n*phi*NFP
    z=0
    for zbs_tuple in zbs_tuples:
        n=int(zbs_tuple[0])
        m=int(zbs_tuple[1])
        coef=float(zbs_tuple[2])
        z+=coef*np.sin(getPhase(n,m))
    r=0
    for rbc_tuple in rbc_tuples:
        n=int(rbc_tuple[0])
        m=int(rbc_tuple[1])
        coef=float(rbc_tuple[2])
        r+=coef*np.cos(getPhase(n,m))
    x=np.cos(phi)*r
    y=np.sin(phi)*r
    return [np.round(point,4) for point in [x,y,z]]

thetas=np.linspace(0,2*np.pi,nPointsRadial,endpoint=False)
phis=np.linspace(0,2*np.pi,nPointsToroidal,endpoint=False)
points=[]
faces=[]
for j in range(nPointsToroidal):
    for i in range(nPointsRadial):
        points.append(getPoints(phis[j],thetas[i]))

        nextI=(i+1)%nPointsRadial
        nextJ=(j+1)%nPointsToroidal

        upperLeft=j*nPointsRadial+i
        upperRight=nextJ*nPointsRadial+i
        lowerLeft=j*nPointsRadial+nextI
        lowerRight=nextJ*nPointsRadial+nextI

        # right-hand-rule vector must face into object
        faces.append([upperLeft, upperRight, lowerRight])
        faces.append([upperLeft, lowerRight, lowerLeft])

##### For adding circular coils
# cylindrical_coil_string="""
# rotate([90,0,0])
# translate([1.2,0,0])
# difference(){
#     cylinder(r=0.9,h=0.4,center=true,$fn=100);
#     cylinder(r=0.7,h=0.45,center=true,$fn=100);
# }

# rotate([90,0,90])
# translate([1.2,0,0])
# difference(){
#     cylinder(r=0.9,h=0.4,center=true,$fn=100);
#     cylinder(r=0.7,h=0.45,center=true,$fn=100);
# }

# rotate([90,0,180])
# translate([1.2,0,0])
# difference(){
#     cylinder(r=0.9,h=0.4,center=true,$fn=100);
#     cylinder(r=0.7,h=0.45,center=true,$fn=100);
# }
# """


##### For adding D-shaped coils
# from helpers import getDeePoints
# deePointsInner=getDeePoints(0.24)
# deePointsOuter=getDeePoints(0.37)
# deePoints=np.concatenate([deePointsInner, deePointsOuter],axis=0)
# deePathInner=np.append(np.arange(deePointsInner.shape[0]),
#                        0)
# deePathOuter=np.append(deePointsInner.shape[0]+np.arange(deePointsOuter.shape[0]),
#                        deePointsInner.shape[0])
# deePaths=np.array([deePathInner,deePathOuter])

# with open(output_file,'w') as f:
#     # Stellarator
#     f.write("Points="+str(points)+";")
#     f.write("\n\n")
#     f.write("Faces="+str(faces)+";")
#     f.write("\n\n")
#     f.write("polyhedron( Points,Faces );")
#     f.write("\n\n")
#     # Dee
#     #f.write("translate([0,0.25,0])\n")
#     #f.write("rotate([0,-90,0])\n")
#     f.write("DeePoints="+str(deePoints.tolist())+";")
#     f.write("\n\n")
#     f.write("DeePaths="+str(deePaths.tolist())+";")
#     f.write("\n\n")
#     scale=0.22
#     f.write(f"""
# rotate([90,0,90])
# resize([{scale},{scale},0.05])
# linear_extrude(center=false)
# 	polygon(points=DeePoints, paths=DeePaths, convexity=10);
# translate([-0.06,0,0])
# rotate([90,0,90])
# resize([{scale},{scale},0.05])
# linear_extrude(center=false)
# 	polygon(points=DeePoints, paths=DeePaths, convexity=10);
# rotate([90,0,-90])
# resize([{scale},{scale},0.05])
# linear_extrude(center=false)
# 	polygon(points=DeePoints, paths=DeePaths, convexity=10);
# translate([0.06,0,0])
# rotate([90,0,-90])
# resize([{scale},{scale},0.05])
# linear_extrude(center=false)
# 	polygon(points=DeePoints, paths=DeePaths, convexity=10);
# """)
#     #f.write(coil_string)
