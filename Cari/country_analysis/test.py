# -*- coding: utf-8 -*-

import sys,glob,os,pickle
import numpy as np
#from netCDF4 import Dataset,netcdftime,num2date
from netCDF4 import Dataset,num2date
import pandas as pd

#Change to auto fill base path based on 'USER' name
if(os.environ['USER'] == 'alrick'):
    local2 = '/media/sf_CA_Git/repository/Cari/'

if(os.environ['USER'] == 'bdonc'):
    local2 = '/home/bdonc/CA/'


#Change username and path above to match your PC
base_path = local2+'country_analysis/'

print base_path
#testing changes
#Final test


#sys.path.append('/Users/peterpfleiderer/Documents/Projects/country_analysis/')
sys.path.append(base_path)
try:del sys.modules['country_analysis']
except:pass
import country_analysis; reload(country_analysis)
#sys.path.append('/Users/peterpfleiderer/Documents/Projects/country_analysis/')
sys.path.append(base_path)


iso='JAM'
os.chdir(base_path)
os.system('cdo -V &pause')
# data will be stored in working_directory
COU=country_analysis.country_analysis(iso,working_directory='data/'+iso+'/',additional_tag='')

COU.load_data(quiet=False,load_region_polygons=False)

# country mask
#COU.create_mask_country('/media/sf_CA_Shared/CRU/cru_ts3.24.01.1901.2015.tmp.dat.nc','tmp',overwrite=True)

# masks for administrative regions
#COU.create_mask_admin('/media/sf_CA_Shared/CRU/cru_ts3.24.01.1901.2015.tmp.dat.nc','tmp',overwrite=True)


#COU.country_zoom('/media/sf_CA_Shared/CRU/cru_ts3.24.01.1901.2015.tmp.dat.nc',var_name='tmp',given_var_name='tas',data_type='CRU',time_format='monthly',overwrite=True)
#COU.country_zoom('/media/sf_CA_Shared/CRU/cru_ts3.24.01.1901.2015.pre.dat.nc',var_name='pre',given_var_name='pr',data_type='CRU',time_format='monthly',overwrite=True)


print len(COU.selection(['pr']))

COU.hist_merge()

COU.ensemble_mean()

# show loaded data
COU.summary()

# calculates area averages
COU.area_average('lat_weighted',overwrite=True)
