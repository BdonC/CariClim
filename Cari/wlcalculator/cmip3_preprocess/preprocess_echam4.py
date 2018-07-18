import os, glob, re, sys
import subprocess
import numpy as np
import netCDF4 as nc

sourcep = "/iplex/01/tumble/mengel/ipcc_ar4_pcmdi/pcmdi_data/"
outp    = "./temp/"
model   = "ingv_echam4"

alldata = glob.glob(sourcep+"/*/atm/mo/tas/ingv_echam4/run1/*nc")
scens   = ["sresa1b","sresa2"] # sresa2 still to download

for d in alldata:
  p = d.split("/")
  runid = model+"."+p[7]+"."+p[12]
  #print runid
  cmd = "cdo fldmean -yearmean "+d+" "+outp+runid+"."+p[-1]
  print cmd
  #try:
    #subprocess.check_call(cmd, shell=True)
  #except subprocess.CalledProcessError:
    #print "### error on "+ runid
    #continue

for scen in scens:
  file20c  = "./temp/ingv_echam4.20c3m.run1.tas_A1.nc"
  rid = "ingv_echam4."+scen+".run1"
  filescen = "./temp/ingv_echam4."+scen+".run1.nc"
  filemerged = "./temp/"+rid+".merged.nc"
  cmd = "cdo -O mergetime "+file20c+" ./temp/"+rid+".tas*.nc "+filemerged
  print cmd
  subprocess.check_call(cmd, shell=True)
  ncf = nc.Dataset(filemerged,"a")
  time = np.arange(1870,2101)*12
  ncf.variables["time"][:] = time
  ncf.variables["time"].units = "years since 0000-01-01"
  #ncf.variables["time_bnds"][:,0] = time
  #ncf.variables["time_bnds"][:,1] = time + 12
  #ncf.variables["time_bnds"].units = "years since 0001-01-01"
  ncf.close()
  cmd = "ncrename -v tas,tas_global "+filemerged
  subprocess.check_call(cmd, shell=True)
  #cmd = "ncks -O -x -v time_bnds "+filemerged+" "+filemerged
  #print cmd
  #subprocess.check_call(cmd, shell=True)
