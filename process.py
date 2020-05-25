import scipy as sp
import scipy.interpolate as intp
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import argparse


def readdata(name):
    """
    Read data from file and return simple array
    :param name: filename
    :return: (x,y,z) tuple of coordinate vectors of same length
    """
    data1 = np.loadtxt(name)
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


def int2(x, y, z, npoints):
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
    return (xx, yy, znew)


def int3(x, y, z, npoints):
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

    return (xnew, ynew, intdata)


def writecubes(x, y, z, file, xmin=0, xmax=100, ymin=0, ymax=100, zmin=3, zmax=100):
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
    incrementx = (xmax - xmin) / x.shape[0]
    incrementy = (ymax - ymin) / x.shape[1]
    # Flatten the x and y arrays and rescale them to range 0-xmax mm
    x = x.flatten()
    x = x - x.min()
    x = x * ((xmax - incrementx) / x.max())
    y = y.flatten()
    y = y - y.min()
    y = y * ((ymax - incrementx) / y.max())
    # Flatten and scale z axis
    z = z.flatten()
    z = z - z.min()
    z = z * ((zmax - zmin) / z.max())

    for (a, b, c) in list(zip(x, y, z)):
        print("translate([{x1}, {y1} , {z1} ]) \
        cube([{incrementx}, {incrementy}, {height}]);".format(
            x1=a, y1=b, z1=3,
            incrementx=incrementx, incrementy=incrementy,
            height=c), file=file)


def writepolyhedra(x, y, z, file, xmin=0, xmax=100, ymin=0, ymax=100, zmin=3, zmax=100):
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
    incrementx = (xmax - xmin) / x.shape[0]
    incrementy = (ymax - ymin) / x.shape[1]
    # rescale x, y ,z arrays to range 0-xmax mm
    x = x - x.min()
    x = x * ((xmax - xmin) / x.max())
    y = y - y.min()
    y = y * ((ymax - ymin) / y.max())
    z = z - z.min()
    z = z * ((zmax - zmin) / z.max()) + zmin
    print("""CubeFaces = [
  [0,1,2,3],  // bottom
  [4,5,1,0],  // front
  [7,6,5,4],  // top
  [5,6,2,1],  // right
  [6,7,3,2],  // back
  [7,4,0,3]]; // left""", file=file)
    print("union() {", file=file)
    for i in range(0, x.shape[0] - 1):  # over X
        for j in range(0, x.shape[1] - 1):  # over Y
            x0 = x[i, j]
            x1 = x[i, j + 1]  # - 0.001
            y0 = y[i, j]
            y1 = y[i + 1, j]  # - 0.001
            z4 = z[i, j]
            z5 = z[i, j + 1]
            z6 = z[i + 1, j + 1]
            z7 = z[i + 1, j]

            print("polyhedron( points=[ [{x0:.3f},{y0:.3f},{zfloor}], [{x1:.3f},{y0:.3f},{zfloor}],"
                  "[{x1:.3f},{y1:.3f},{zfloor}],[{x0:.3f},{y1:.3f},{zfloor}],"
                  "[{x0:.3f}, {y0:.3f}, {z4:.3f}], [{x1:.3f}, {y0:.3f}, {z5:.3f}], "
                  "[{x1:.3f},{y1:.3f},{z6:.3f}],[{x0:.3f},{y1:.3f},{z7:.3f}]],"
                  "faces=CubeFaces"
                  ");\n".format(
                x0=x0, y0=y0, x1=x1, y1=y1,
                zfloor=3,
                z4=z4, z5=z5, z6=z6, z7=z7),
                file=file
            )
    print("}\n", file=file)


def writemargins(xx, yy, zz, file):
    x_description = "Distance C-C (A)"
    y_description = "Distance C-Br (A)"
    z_description = "Energy (kcal/mol)"
    x_description = args.xname
    y_description = args.yname
    z_description = args.zname

    print("""//base extensions
    translate([-15,-15,0])
    color([0,1,1])
    cube([115,115,3]);
    //
    """, file=file)

    for i in range(0, 5):
        print("translate([{xpos}, -2, 2]) color([0, 1, 1]) cube([1, 2, 2]);\n".format(
            xpos=-0.5 + i * 20
        ),
            file=file)
        print("translate([{xpos}, -5, 3]) rotate([0, 0, 0]) linear_extrude(height=1)"
              "text(text=\"{xvalue:.3f}\", size=4, halign=\"center\", valign=\"center\", "
              "font=\"Arial:style=bold\");".format(
            xpos=i * 20,
            xvalue=i * ((x.max() - x.min()) / 5) + x.min()
        ), file=file)
    print("""translate([42, -11, 3])
        rotate([0, 0, 0])
        linear_extrude(height=1)
        text(text="{x_description}",
             size=4,
             halign="center",
             valign="center",
             font="Arial:style=bold"); """.format(x_description=x_description),
          file=file)

    for i in range(0, 4):
        ypos = 10 + i * 20
        print("translate([-2,{ypos},2]) color([0,1,1]) cube([2,1,2]);\n".format(
            ypos=ypos - 0.5
        ), file=file)
        print("translate([-5,{ypos},3]) rotate([0,0,270]) linear_extrude(height=1)"
              "text(text=\"{yvalue:.3f}\", size=4, halign=\"center\", valign=\"center\", "
              "font=\"Arial:style=bold\");".format(
            ypos=ypos,
            yvalue=i * ((y.max() - y.min()) / 4) + y.min()
        ), file=file)
    print("""translate([-11, 45, 3])
            rotate([0, 0, 270])
            linear_extrude(height=1)
            text(text="{y_description}",
                 size=4,
                 halign="center",
                 valign="center",
                 font="Arial:style=bold"); """.format(y_description=y_description),
          file=file)

    print("""difference(){

            """, file=file)
    print("""
            translate([-15,96,0])
        color([0,1,1])
        cube([15,4,100]);
        //
        """, file=file)
    for i in range(0, 4):
        zpos = 10 + i * 25
        print("translate([-2,96,{zpos}]) color([0,1,1]) cube([2,1,2]);\n".format(
            zpos=zpos - 0.5
        ), file=file)
        print("translate([-5,97,{zpos}]) rotate([0,90,270]) linear_extrude(height=1)"
              "text(text=\"{zvalue:.3f}\", size=4, halign=\"center\", valign=\"center\", "
              "font=\"Arial:style=bold\");".format(
            zpos=zpos,
            zvalue=i * ((z.max() - z.min()) / 4) + z.min()
        ), file=file)
        print("""translate([-11, 97, 50])
                    rotate([0, 90, 270])
                    linear_extrude(height=1)
                    text(text="{z_description}",
                         size=4,
                         halign="center",
                         valign="center",
                         font="Arial:style=bold"); """.format(z_description=z_description),
              file=file)

    print("""}

                    """, file=file)



parser = argparse.ArgumentParser()
parser.add_argument("inputfile")
parser.add_argument("--grid", type=int, help="grid dimension", default=20)
parser.add_argument("--xname", help="X axis description", default="X axis")
parser.add_argument("--yname", help="Y axis description", default="Y axis")
parser.add_argument("--zname", help="X axis description", default="Energy (kcal/mol)")
args = parser.parse_args()

x, y, z = readdata(args.inputfile)
# Here adjust the interpolation grid density
xx, yy, zz = int2(x, y, z, args.grid)
with open(args.inputfile + ".scad", 'w') as file:
    writemargins(xx, yy, zz, file)
    # writecubes(xx,yy,zz,file)
    writepolyhedra(xx, yy, zz, file)

# fig = plt.figure()
# ax = fig.add_subplot(121, projection='3d') #, projection='3d'

# ax.scatter(xs=x, ys=y, zs=z)
# ax.scatter(xs=xx.flatten(), ys=yy.flatten(), zs=zz.flatten(),s=1)

# ax2 = fig.add_subplot(122)
# ax2.contour(xx, yy, zz, levels=30)

# plt.show()

