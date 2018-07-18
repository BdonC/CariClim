# -*- coding: utf-8 -*-

import sys,glob,os,pickle
import numpy as np
from netCDF4 import Dataset,num2date
import netcdftime
import pandas as pd

sys.path.append('/media/sf_CA_Shared/country_analysis/')
try:del sys.modules['country_analysis']
except:pass
import country_analysis; reload(country_analysis)
sys.path.append('/media/sf_CA_Shared/country_analysis/')


import argparse
#parser = argparse.ArgumentParser()
#parser.add_argument("--country",'-c', help="country iso",required=True)
#parser.add_argument("--overwrite",'-o', help="overwrite output files",action="store_true")
#args = parser.parse_args()

#if args.overwrite:
overwrite=True
#else:
#    overwrite=False

iso='JAM'#args.country


print iso
os.chdir('/media/sf_CA_Shared/country_analysis/')
# data will be stored in working_directory
COU=country_analysis.country_analysis(iso,working_directory='data/'+iso+'/',additional_tag='')

# ##############
# # MASKS
# ##############

# country mask
COU.create_mask_country('/media/sf_CA_Shared/CRU/cru_ts3.24.01.1901.2015.tmp.dat.nc','tmp',overwrite=False)

# masks for administrative regions
COU.create_mask_admin('/media/sf_CA_Shared/CRU/cru_ts3.24.01.1901.2015.tmp.dat.nc','tmp',overwrite=False)

# population weighted
#COU.create_mask_country('/p/projects/elis/CRUDATA_TS3_23/cru_ts3.23.1901.2014.tmp.dat.nc','tmp',mask_style='pop1990_weighted',pop_mask_file='/home/pepflei/CA/masks/population/population_1990_incrLat.nc',overwrite=False)
#COU.create_mask_country('/p/projects/elis/CRUDATA_TS3_23/cru_ts3.23.1901.2014.tmp.dat.nc','tmp',mask_style='pop2015_weighted',pop_mask_file='/home/pepflei/CA/masks/population/population_2015_incrLat.nc',overwrite=False)

# ##############
# # Zoom - save small netcdf files covering the country
# ##############
COU.country_zoom('/media/sf_CA_Shared/CRU/cru_ts3.24.01.1901.2015.tmp.dat.nc',var_name='tmp',given_var_name='tas',data_type='CRU',time_format='monthly',overwrite=False)
COU.country_zoom('/media/sf_CA_Shared/CRU/cru_ts3.24.01.1901.2015.pre.dat.nc',var_name='pre',given_var_name='pr',data_type='CRU',time_format='monthly',overwrite=False)

COU.country_zoom('/media/sf_CA_Shared/CRU/cru_ts3.24.01.1901.2015.tmp.dat.nc',var_name='tmp',given_var_name='tas',scenario='rcp4p5',model='CORDEX',data_type='CORDEX',time_format='monthly',overwrite=False)
COU.country_zoom('/media/sf_CA_Shared/CRU/cru_ts3.24.01.1901.2015.pre.dat.nc',var_name='pre',given_var_name='pr',scenario='rcp4p5',model='CORDEX',data_type='CORDEX',time_format='monthly',overwrite=False)

COU.country_zoom('/media/sf_CA_Shared/CRU/cru_ts3.24.01.1901.2015.tmp.dat.nc',var_name='tmp',given_var_name='tas',scenario='rcp4p5',model='CORDEX',data_type='CMIP',time_format='monthly',overwrite=False)
COU.country_zoom('/media/sf_CA_Shared/CRU/cru_ts3.24.01.1901.2015.pre.dat.nc',var_name='pre',given_var_name='pr',scenario='rcp4p5',model='CORDEX',data_type='CMIP',time_format='monthly',overwrite=False)



# merges historical with rcp scenarios
COU.hist_merge()

# creates ensemble mean files
print 'Showing ensemble mean'
COU.ensemble_mean()

# show loaded data
COU.summary()

# calculates area averages
COU.area_average('lat_weighted',overwrite=True)
# COU.area_average('pop2015_weighted',overwrite=False)
# COU.area_average('pop1990_weighted',overwrite=False)

# compresses the data package into a zip file
COU.zip_it()
