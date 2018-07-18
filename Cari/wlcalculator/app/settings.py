# Copyright (C) 2014 Matthias Mengel and Carl-Friedrich Schleussner
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



""" the Warming Attribution Calculator setting file. """

baseperiod  = [1980,2000]
finalperiod = [2080,2100]
preindperiod = [1850,1900]

warminglevels = [1.5,2.0,3.0,4.0]


cmip5_models    = [
 'access1-0',
 'access1-3',
 'bcc-csm1-1',
 'bcc-csm1-1-m',
 'bnu-esm',
 'canesm2',
 'ccsm4',
 'cesm1-bgc',
 'cesm1-cam5',
 'cesm1-fastchem',
 'cesm1-waccm',
 'cnrm-cm5',
 'csiro-mk3-6-0',
 'fgoals-g2',
 'fgoals-s2',
 'fio-esm',
 'gfdl-cm3',
 'gfdl-esm2g',
 'gfdl-esm2m',
 'giss-e2-r',
 'hadgem2-cc',
 'hadgem2-es',
 'inmcm4',
 'ipsl-cm5a-lr',
 'ipsl-cm5a-mr',
 'ipsl-cm5b-lr',
 'miroc-esm',
 'miroc-esm-chem',
 'miroc4h',
 'miroc5',
 'mpi-esm-lr',
 'mpi-esm-mr',
 'mpi-esm-p',
 'mri-cgcm3',
 'noresm1-m',
 'noresm1-me'
]

cmip5_scenarios = [
"rcp26",
"rcp45",
"rcp60",
"rcp85"
]

cmip3_models =[
 'bccr_bcm2_0',
 'cccma_cgcm3_1',
 'cccma_cgcm3_1_t63',
 'cnrm_cm3',
 'csiro_mk3_0',
 'gfdl_cm2_0',
 'gfdl_cm2_1',
 'giss_aom',
 'giss_model_e_h',
 'giss_model_e_r',
 'iap_fgoals1_0_g',
 'ingv_echam4',
 'inmcm3_0',
 'ipsl_cm4',
 'miroc3_2_hires',
 'miroc3_2_medres',
 'miub_echo_g',
 'mpi_echam5',
 'mri_cgcm2_3_2a',
 'ncar_ccsm3_0',
 'ncar_pcm1',
 'ukmo_hadcm3',
 'ukmo_hadgem1']

cmip3_scenarios = [
"commit",
"sresa1b",
"sresb1",
"sresb2*",
"sresa2",
"sresa1fi*"
]

# use left sides to define intervals, see python's bisect function
warming_levels_wb3 = [0.5,0.8,1.25,1.75,2.25,3.5]

# give bisect's number output the right names
warming_level_names = {
0:"below 0.5 &deg;C",
1:"observed",
2:"1.0 &deg;C",
3:"1.5 &deg;C",
4:"2.0 &deg;C",
5:"3.0 &deg;C",
6:"4.0 &deg;C",
}
