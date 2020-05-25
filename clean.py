#!/home/krupickm/sw/bin/python3

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("inputfile")
parser.add_argument("--maxoff", type=float, help="maximum off-distance", default=1.4)
parser.add_argument("--interpcutoff", type=float, help="interpolation distance", default=0.10)
parser.add_argument("--zmax", type=float, help="zmax", default=50)
args=parser.parse_args()

a=np.loadtxt(args.inputfile)

dcl=np.round(a[:,1],2)
dim1=len(np.unique(dcl))
dbr=np.round(a[:,2],2)
dclbr=abs(a[:,1]+a[:,2]-a[:,3])
dim2=len(np.unique(dbr))
e=a[:,0]
#print(dclbr)
#plt.plot(dclbr,"ro")
#plt.hist(dclbr,20)
#plt.show()
maxoff=args.maxoff
interpcutoff=args.interpcutoff

wrongvaules=[]
for i in range(0,len(e)):
    # Test for distance diagnostics
    if(dclbr[i]>maxoff):
        print("%.2f %.2f %.2f %.4f -> NaN"%(dcl[i],dbr[i],dclbr[i],e[i]))
        e[i]=np.nan
        wrongvaules.append(i)
        print("diagout:",i)

        continue

    # test as statistical outlier
    surroundings = []
    # ignore edges
    if(dcl[i] in (min(dcl),max(dcl)) or dbr[i] in (min(dbr),max(dbr))):
        continue
    for j in range(0,len(e)):
        if(abs(dcl[j]-dcl[i])<=interpcutoff and
                abs(dbr[j]-dbr[i])<=interpcutoff and
                not np.isnan(e[j])
                and i!=j):
            surroundings.append(e[j])

    avg=np.average(surroundings)
    std=np.std(surroundings)
    if(not (avg-std<e[i]<avg+std)):
        wrongvaules.append(i)
        print("avgout ",i)



for i in wrongvaules:
    newsum=0
    newcount=0
    for j in range(0,len(e)):
        if(abs(dcl[j]-dcl[i])<=interpcutoff and abs(dbr[j]-dbr[i])<=interpcutoff and not np.isnan(e[j])):
            newsum+=e[j]
            newcount+=1
    if(newcount>0):
        e[i]=newsum/newcount
    else:
        print(dcl[i],dbr[i])

# Normalize E, make it from zero (lowest value) to zmax
emin=min(e)
e=e-emin
for i in range(0,len(e)):
    e[i]=e[i]*627.5
    if(e[i]>args.zmax):
        e[i]=args.zmax


# write result
with open(args.inputfile+".clean","w") as f:
    for i in range(0,len(e)):
        print("%10.5f %10.5f %10.5f"%(dcl[i],dbr[i],e[i]),file=f)


fig = plt.figure()
ax = fig.add_subplot(111,projection='3d')
ax.scatter(dcl,dbr,e,marker=".")

ax.scatter(dcl[wrongvaules],dbr[wrongvaules],e[wrongvaules],color="r",marker="o")
plt.show()