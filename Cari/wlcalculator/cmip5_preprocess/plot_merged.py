import os, glob, re
import netCDF4 as nc
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.pyplot as plt
plt.rcParams['font.size']=10

# find all available merged files
allmerged = sorted(glob.glob("./temp/*r1i1p1.merged.nc"))


with PdfPages('./plots/testmerged.pdf') as pdf:

  for fle in allmerged:
    print fle
    ncr = nc.Dataset(fle, 'r')

    #tas_global = ncr.variables["tas_global"][:]
    tme        = ncr.variables["time"][:]

    fig = plt.figure(figsize=(9, 9))
    plt.plot(tme/12.,ncr.variables["tas_global"][:])
    plt.plot(tme/12.,ncr.variables["tas_ctrl_global_lin"][:])
    plt.title(fle,fontsize=10)
    pdf.savefig(fig)  # saves the current figure into a pdf page
    plt.close()
    ncr.close()
