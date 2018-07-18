import os, glob, re, sys
import subprocess


cmip5path= "/iplex/01/ipcc_ar5_pcmdi/pcmdiOutput/ReferenceData/"
out_dir  = "../data/cmip5_ver002"

exclude_rids = [

]

variables = "tas_global,tas_ctrl_global_lin"

exclude_scens = ["1pctCO2","abrupt4xCO2"]

# find all available 20c files and store names.
data_20c   = {}
all20c = sorted(glob.glob(cmip5path + "*historical*nc"))

checkruns = []

for fname in all20c:
  rid = fname.split("/")[-1].split(".refdata.nc")[0]
  model,scen,run = rid.split(".")
  #if model != lastmodel:
  data_20c[rid] = {}
  data_20c[rid]["model"] = model
  data_20c[rid]["run"]   = run
  data_20c[rid]["fname"] = fname.split("/")[-1]
  checkruns.append(run)
#sys.exit(0)

# find all scenario files
data_scen   = {}
allscens = sorted(glob.glob(cmip5path + "*nc"))
for fname in allscens:
  #print fname
  rid = fname.split("/")[-1].split(".refdata.nc")[0]
  #print fname.split("/")[-1]
  model,scen,run = rid.split(".")
  if scen == "historical": continue
  #print rid
  #if model != lastmodel:
  data_scen[rid] = {}
  data_scen[rid]["model"] = model
  data_scen[rid]["scen"]  = scen
  data_scen[rid]["run"]   = run
  checkruns.append(run)

for rid in data_20c:
  print "####" + rid

  #if "mpi_echam5" not in rid: continue
  model     = data_20c[rid]["model"]
  run       = data_20c[rid]["run"]
  fname_20c = data_20c[rid]["fname"]
  # find all scenarios that fit
  available_scen = [s for s in data_scen.keys() if re.search(model+"\..*\."+run, s)]
  print available_scen
  if available_scen == []: continue

  cmd = "ncks -O -v "+variables+" " + cmip5path + fname_20c +" ./temp/" +fname_20c
  print cmd
  subprocess.check_call(cmd, shell=True)

  #if model == "mpi_echam5":
  ## cut off commit scenario from 20c3m
    #tmp = fname_20c
    #fname_20c = tmp.split(".nc")[0]+"_cut"+".nc"
    #cmd = "cdo -O selyear,1860/2000 ./temp/" +tmp+" ./temp/"+fname_20c
    #print cmd
    #subprocess.check_call(cmd, shell=True)

  for rid in available_scen:
    print rid
    scen  = data_scen[rid]["scen"]
    model = data_scen[rid]["model"]
    run   = data_scen[rid]["run"]

    if scen in exclude_scens: continue

    # strange jump, and run2 looks better.
    #if rid == "ncar_pcm1.sresb1.run1": continue

    fname_scen = rid + ".refdata.nc"
    cmd = "ncks -O -v "+variables+" "+cmip5path+fname_scen+" ./temp/"+fname_scen
    print cmd
    subprocess.check_call(cmd, shell=True)
    cmd = "cdo -O mergetime ./temp/"+fname_20c+" ./temp/"+fname_scen+" ./temp/"+rid.lower()+".merged.nc"
    print cmd
    subprocess.check_call(cmd, shell=True)



# strip unnecessary variables

# merge

# check for time consistency
