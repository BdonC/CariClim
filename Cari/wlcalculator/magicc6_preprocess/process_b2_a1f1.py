# Copyright (C) 2014 Matthias Mengel
#
# This file is part of wacalc.
#
# wacalc is free software; you can redistribute it and/or modify it under the
# terms of the GNU General Public License as published by the Free Software
# Foundation; either version 3 of the License, or (at your option) any later
# version.
#
# wacalc is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License
# along with wacalc; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA


"""
preprocess magicc6 output to have wacalc conform netcdf4 file
"""

import os, glob
import csv
import numpy as np
import netCDF4 as nc
import matplotlib.pylab as plt

magicc6_source = "/mnt/mengel/Archiv/20140506_Magicc6_A1F1_B2_data/"
runids_b2      = "./b2_ids.csv"
runids_a1f1    = "./a1f1_ids.csv"


### read in id file to have id -> scenario mapping
scenmap = {}
for idfile in [runids_b2,runids_a1f1]:

  with open(idfile , 'rb') as csvfile:
    spamreader = csv.reader(csvfile, delimiter='\t')
    for i, row in enumerate(spamreader):
      # extract id
      runid_short = row[0][0:8]
      scenmap[runid_short] = row[1].lower()


### get magicc6 data
runs = glob.glob(magicc6_source + "*")
magicc6_data = {}

for run in runs:

  runid = run.split("/")[-1][2:]
  magicc6_data[runid] = {}

  with open (run + '/MAGCFG_USER.CFG', 'rb') as myfile:
    model_line = myfile.readlines()[8]
    model      = model_line.split("FULLTUNE_")[-1].split('\",')[0]
    magicc6_data[runid]["model"]    = model.lower()
    magicc6_data[runid]["scenario"] = scenmap[runid[0:8]]
    #print magicc6_data[runid]["model"]

  with open(run + '/OUT/DAT_SURFACE_TEMP.OUT', 'rb') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=' ')
    tm  = []
    tas = []

    for i, row in enumerate(spamreader):
      #print row
      if i<20: continue

      row = [x for x in row if x != '']
      tm.append(int(row[0]))
      tas.append(float(row[1]))


    magicc6_data[runid]["time"] = np.array(tm)
    magicc6_data[runid]["tas_global"] = np.array(tas)

  if i != 355:
    raise Exception("time series deviates from standard length of 101 years.")


# write to wacalc conform netcdf.

for runid in magicc6_data:

  m = magicc6_data[runid]

  fname = m["model"]+"."+m["scenario"]+".magicc6.merged.nc"
  ncf = nc.Dataset("./temp/"+fname, 'w', format='NETCDF3_CLASSIC')
  ncf.createDimension('time',size=None)

  nct = ncf.createVariable( 'time','float32',('time',) )
  nct.standard_name = "time"
  # this is not netcdf conform as years should be > 0, but we wanna stay consistent with
  # the other data
  nct.units         = "months since 0000-01-01 00:00:00"
  nct.calendar      = "standard"

  nctas       = ncf.createVariable( 'tas_global','float32',('time',) )
  nctas.units = "K"

  nct[:]   = m["time"]*12
  nctas[:] = m["tas_global"]
  ncf.close()

# plot for testing.

#plt.clf()
#for runid in magicc6_data:
  #if magicc6_data[runid]["scenario"] == "sresb2":
    #plt.plot(magicc6_data[runid]["time"],magicc6_data[runid]["tas_global"])
  ##print runid
#plt.show()
#plt.savefig("b2.png")


