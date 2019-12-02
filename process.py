import scipy as sp
import scipy.interpolate as intp
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt

def readdata(name):
    """
    Read data from file and return simple array
    :param name: filename
    :return: (x,y,z) tuple of coordinate vectors of same length
    """
    data1 = np.loadtxt("all.meps.data")
    x = data1[:, 0]
    y = data1[:, 1]
    z = data1[:, 2]
    return (x, y, z)




def int1():
    """
    Spline interpolation, fails for more hairy data
    """
    intdata = intp.interp2d(x=x, y=y, z=z, kind='linear', bounds_error=True)
    xnew = np.linspace(x.min(), x.max(), 11)
    ynew = np.linspace(y.min(), y.max(), 11)
    znew = intdata(xnew, ynew)
    print(znew.shape)
    xx, yy = np.meshgrid(xnew, ynew)
    print(xx.shape)
    ax.scatter(xs=xx.flatten(), ys=yy.flatten(), zs=znew.flatten())
    ax2.contour(xx, yy, znew, levels=20)
    plt.show()


def int2(x,y,z,npoints):
    """
    Simple linear interpolation
    :param x:
    :param y:
    :param z:
    :param npoints: number of points in both directions
    :return: tuple of interpolated x,y,z data
    """
    coord = list(zip(x, y))
    intdata = intp.LinearNDInterpolator(coord, z)
    xnew = np.linspace(x.min(), x.max(), npoints)
    ynew = np.linspace(y.min(), y.max(), npoints)
    xx, yy = np.meshgrid(xnew, ynew)
    znew = intdata(xx, yy)
    return (xx,yy,znew)

def int3(x,y,z,npoints):
    """
    Simple linear interpolation, returns x,y arrays and Z as function
    :param x:
    :param y:
    :param z:
    :param npoints: number of points in both directions
    :return: xarray, yarray, Zfunction
    """
    coord = list(zip(x, y))
    intdata = intp.LinearNDInterpolator(coord, z)
    xnew = np.linspace(x.min(), x.max(), npoints)
    ynew = np.linspace(y.min(), y.max(), npoints)

    return (xnew,ynew,intdata)

def writecubes(x,y,z,file,xmin=0,xmax=100, ymin=0,ymax=100, zmin=3, zmax=100):
    """

    :param x:
    :param y:
    :param z:
    :param xmin:
    :param xmax:
    :param ymin:
    :param ymax:
    :param zscale:
    :return:
    """
    # Calculate the x and y size of prism in mm based on number of prisms
    incrementx=(xmax-xmin)/x.shape[0]
    incrementy = (ymax - ymin) / x.shape[1]
    # Flatten the x and y arrays and rescale them to range 0-xmax mm
    x=x.flatten()
    x=x-x.min()
    x=x*((xmax-incrementx)/x.max())
    y=y.flatten()
    y=y-y.min()
    y = y * ((ymax-incrementx) / y.max())
    # Flatten and scale z axis
    z=z.flatten()
    z = z - z.min()
    z = z * ((zmax-zmin) / z.max())


    for (a,b,c) in list(zip(x,y,z)):
        print("translate([{x1}, {y1} , {z1} ]) \
        cube([{incrementx}, {incrementy}, {height}]);".format(
            x1=a, y1=b, z1=3,
            incrementx=incrementx, incrementy=incrementy,
            height=c),file=file)

def writepolyhedra(x,y,z,file,xmin=0,xmax=100, ymin=0,ymax=100, zmin=3, zmax=100):
    """

    :param x: X coordinates of 2d grid points
    :param y: Y coordinates of 2d grid points
    :param z: Z values of 2d grid points
    :param xmin:
    :param xmax:
    :param ymin:
    :param ymax:
    :param zscale:
    :return:
    """
    # Calculate the x and y size of prism in mm based on number of prisms
    incrementx=(xmax-xmin)/x.shape[0]
    incrementy = (ymax - ymin) / x.shape[1]
    # rescale x, y ,z arrays to range 0-xmax mm
    x=x-x.min()
    x=x*((xmax-incrementx)/x.max())
    y=y-y.min()
    y = y * ((ymax-incrementx) / y.max())
    z = z - z.min()
    z = z * ((zmax - zmin) / z.max())

    for i in range(0,x.shape[0]-1):  #over X
        for j in range(0, x.shape[1]-1):  #over Y
            x0 = x[i, j]
            x1 = x[i, j + 1]
            y0 = y[i, j]
            y1 = y[i +1, j]
            z4 = z[i, j]
            z5 = z[i , j +1]
            z6 = z[i + 1, j + 1]
            z7 = z[i +1, j]

            print("polyhedron( points=[ [{x0},{y0},{zfloor}], [{x1},{y0},{zfloor}],"
                  "[{x1},{y1},{zfloor}],[{x0},{y1},{zfloor}],"
                  "[{x0}, {y0}, {z4}], [{x1}, {y0}, {z5}], "
                   "[{x1},{y1},{z6}],[{x0},{y1},{z7}]],"
                  "faces=[[0,1,2,3],[0,1,5,4],[1,2,6,5],[3,2,6,7],[3,0,4,7],[4,5,6,7]]"
                  ");\n".format(
                x0=x0, y0=y0, x1=x1, y1=y1,
                zfloor = 3,
                z4=z4, z5=z5, z6=z6, z7=z7),
                file=file
            )

def writemargins(file):

    head = """
    //Adjust axis units and descriptions here:
x_description="C-H distance";
y_description="H-Br distance";
z_description="activation energy";

x_Units=[2.000,2.001,2.002,2.003,2.004];
y_Units=[0,1.004,2.008,3.012,4.016];
z_Units=[0.004,1.002,2.004,3.006,4.008];
//


//Commands for generating the object (advanced users only)
//
//base extensions
translate([-15,-15,0])
color([0,1,1])
cube([115,115,3]);

translate([-15,97,0])
color([0,1,1])
cube([15,3,100]);
//
//unit signs X
translate([-0.5,-2,2])
color([0,1,1])
cube([1,2,2]);

translate([19.5,-2,2])
color([0,1,1])
cube([1,2,2]);

translate([39.5,-2,2])
color([0,1,1])
cube([1,2,2]);

translate([59.5,-2,2])
color([0,1,1])
cube([1,2,2]);

translate([79.5,-2,2])
color([0,1,1])
cube([1,2,2]);
//
//unit signs Y
translate([-2,-0.5,2])
color([0,1,1])
cube([2,1,2]);

translate([-2,19.5,2])
color([0,1,1])
cube([2,1,2]);

translate([-2,39.5,2])
color([0,1,1])
cube([2,1,2]);

translate([-2,59.5,2])
color([0,1,1])
cube([2,1,2]);

translate([-2,79.5,2])
color([0,1,1])
cube([2,1,2]);
//
//unit signs Z
translate([-2,96,3])
color([0,1,1])
cube([2,2,1]);

translate([-2,96,23])
color([0,1,1])
cube([2,2,1]);

translate([-2,96,43])
color([0,1,1])
cube([2,2,1]);

translate([-2,96,63])
color([0,1,1])
cube([2,2,1]);

translate([-2,96,83])
color([0,1,1])
cube([2,2,1]);
//
//X axis descriptions
x_value_1=str(x_Units[0]);
translate([0,-5,3])
    rotate([0,0,0])
    linear_extrude(height=1)
        text(text=x_value_1,
        size=4,
        halign="center",
        valign="center",
        font="Arial:style=bold");

x_value_2=str(x_Units[1]);
translate([20,-5,3])
    rotate([0,0,0])
    linear_extrude(height=1)
        text(text=x_value_2,
        size=4,
        halign="center",
        valign="center",
        font="Arial:style=bold");

x_value_3=str(x_Units[2]);
translate([40,-5,3])
    rotate([0,0,0])
    linear_extrude(height=1)
        text(text=x_value_3,
        size=4,
        halign="center",
        valign="center",
        font="Arial:style=bold");

x_value_4=str(x_Units[3]);
translate([60,-5,3])
    rotate([0,0,0])
    linear_extrude(height=1)
        text(text=x_value_4,
        size=4,
        halign="center",
        valign="center",
        font="Arial:style=bold");

x_value_5=str(x_Units[4]);
translate([80,-5,3])
    rotate([0,0,0])
    linear_extrude(height=1)
        text(text=x_value_5,
        size=4,
        halign="center",
        valign="center",
        font="Arial:style=bold");
        
translate([50,-11,3])
    rotate([0,0,0])
    linear_extrude(height=1)
        text(text=x_description,
        size=4,
        halign="center",
        valign="center",
        font="Arial:style=bold");                  
//
//Y axis descriptions
y_value_1=str(y_Units[0]);
translate([-5,0,3])
    rotate([0,0,270])
    linear_extrude(height=1)
        text(text=y_value_1,
        size=4,
        halign="center",
        valign="center",
        font="Arial:style=bold");

y_value_2=str(y_Units[1]);
translate([-5,20,3])
    rotate([0,0,270])
    linear_extrude(height=1)
        text(text=y_value_2,
        size=4,
        halign="center",
        valign="center",
        font="Arial:style=bold");

y_value_3=str(y_Units[2]);
translate([-5,40,3])
    rotate([0,0,270])
    linear_extrude(height=1)
        text(text=y_value_3,
        size=4,
        halign="center",
        valign="center",
        font="Arial:style=bold");

y_value_4=str(y_Units[3]);
translate([-5,60,3])
    rotate([0,0,270])
    linear_extrude(height=1)
        text(text=y_value_4,
        size=4,
        halign="center",
        valign="center",
        font="Arial:style=bold");

y_value_5=str(y_Units[4]);
translate([-5,80,3])
    rotate([0,0,270])
    linear_extrude(height=1)
        text(text=y_value_5,
        size=4,
        halign="center",
        valign="center",
        font="Arial:style=bold");

translate([-11,50,3])
    rotate([0,0,270])
    linear_extrude(height=1)
        text(text=y_description,
        size=4,
        halign="center",
        valign="center",
        font="Arial:style=bold");  
//
//Z axis descriptions
module ZDesc() {
z_value_1=str(z_Units[0]);
translate([-5,97,4])
    rotate([90,90,0])
    linear_extrude(height=1)
        text(text=z_value_1,
        size=4,
        halign="center",
        valign="center",
        font="Arial:style=bold");
    };
//
module protector(){translate ([-20,90,0]) cube(20);};  
    intersection(){
     ZDesc();
     protector();
        };
//(difference for protection of the bottom)
z_value_2=str(z_Units[1]);
translate([-5,97,24])
    rotate([90,90,0])
    linear_extrude(height=1)
        text(text=z_value_2,
        size=4,
        halign="center",
        valign="center",
        font="Arial:style=bold");

z_value_3=str(z_Units[2]);
translate([-5,97,44])
    rotate([90,90,0])
    linear_extrude(height=1)
        text(text=z_value_3,
        size=4,
        halign="center",
        valign="center",
        font="Arial:style=bold");

z_value_4=str(z_Units[3]);
translate([-5,97,64])
    rotate([90,90,0])
    linear_extrude(height=1)
        text(text=z_value_4,
        size=4,
        halign="center",
        valign="center",
        font="Arial:style=bold");

z_value_5=str(z_Units[4]);
translate([-5,97,84])
    rotate([90,90,0])
    linear_extrude(height=1)
        text(text=z_value_5,
        size=4,
        halign="center",
        valign="center",
        font="Arial:style=bold");

translate([-11,97,53])
    rotate([90,90,0])
    linear_extrude(height=1)
        text(text=z_description,
        size=4,
        halign="center",
        valign="center",
        font="Arial:style=bold"); 

    """
    print(head,file=file)




x,y,z=readdata("all.meps.data")
# Here adjust the interpolation grid density
xx,yy,zz=int2(x,y,z,20)
with open("out.scad", 'w') as file:
    writemargins(file)
   # writecubes(xx,yy,zz,file)
    writepolyhedra(xx,yy,zz,file)

fig = plt.figure()
ax = fig.add_subplot(121, projection='3d') #, projection='3d'

ax.scatter(xs=x, ys=y, zs=z)
ax.scatter(xs=xx.flatten(), ys=yy.flatten(), zs=zz.flatten(),s=1)

ax2 = fig.add_subplot(122)
ax2.contour(xx, yy, zz, levels=30)

plt.show()

