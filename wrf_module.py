'''
wrf_dir="/home/ukhova/Downloads/"
wrf_met_files="met_em.d01.2010*"
wrf_input_file="wrfinput_d01"
wrf_bdy_file="wrfbdy_d01"

mera_dir="/home/ukhova/Downloads/Merra2ForVISUVI/"
mera_files="svc_MERRA2_300.inst3_3d_aer_Nv.20100*"
'''

import pathes
import re
import os
from netCDF4 import Dataset
import numpy as np

met_files=[]
met_times_files={}
wrf_times={}

start_time=""
nx=ny=nz=nw=0
wrf_p_top=0
znu=[]
xlon=[[]]
xlat=[[]]


def get_pressure_from_metfile(metfile):
    PSFC=metfile.variables['PSFC'][:]
    WRF_Pres = np.zeros([nz,ny,nx])
    for z_level in reversed(range(nz)):
        WRF_Pres[nz-1-z_level,:]=PSFC*znu[0,z_level]+ (1.0 - znu[0,z_level])*wrf_p_top
    return WRF_Pres

def get_sfcp_from_met_file(filename):
    metfile= Dataset(pathes.wrf_met_dir+"/"+filename,'r')
    PSFC=metfile.variables['PSFC'][:]
    metfile.close()
    return PSFC

def get_met_file_by_time(time):
    return met_times_files.get(time)

def get_index_in_file_by_time(time):
    return wrf_times.get(time)


numbers = re.compile(r'(\d+)')
def numericalSort1(value):
    parts = numbers.split(value)
    return int(float(parts[3])*1e6+float(parts[5])*1e4+float(parts[7])*1e2+float(parts[9]))


def get_ordered_met_files():
    return met_files


def initialise():
    global met_files,wrf_times,wrf_p_top,znu,xlon,xlat,nx,ny,nz,nw,start_time

    met_files=sorted([f for f in os.listdir(pathes.wrf_dir) if re.match(pathes.wrf_met_files, f)], key=numericalSort1)
    wrfbddy = Dataset(pathes.wrf_dir+"/"+pathes.wrf_bdy_file,'r')
    for i in range(0,len(wrfbddy.variables['Times'][:]),1):
        #wrf_times.append(''.join(wrfbddy.variables['Times'][i]))
        wrf_times.update({''.join(wrfbddy.variables['Times'][i]):i})
        met_times_files.update({''.join(wrfbddy.variables['Times'][i]):met_files[i]})

    nx=wrfbddy.dimensions['west_east'].size
    ny=wrfbddy.dimensions['south_north'].size
    nz=wrfbddy.dimensions['bottom_top'].size
    nw=wrfbddy.dimensions['bdy_width'].size

    wrfbddy.close()

    #Reading "PRESSURE TOP OF THE MODEL, PA" and "eta values on half (mass) levels"
    wrfinput=Dataset(pathes.wrf_dir+"/"+pathes.wrf_input_file,'r')
    wrf_p_top=wrfinput.variables['P_TOP'][:]
    znu=wrfinput.variables['ZNU'][:]
    xlon=wrfinput.variables['XLONG'][:]
    xlat=wrfinput.variables['XLAT'][:]
    start_time=''.join(wrfinput.variables['Times'][0])
    wrfinput.close()


#initialise()
#metfile= Dataset(pathes.wrf_met_dir+"/met_em.d01.2010-07-14_00:00:00.nc",'r')
#get_pressure_from_metfile(metfile)
