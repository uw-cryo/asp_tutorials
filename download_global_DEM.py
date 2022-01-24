#! /usr/bin/env python

import os,sys,glob
import subprocess
import argparse

def get_parser():
        parser = argparse.ArgumentParser(description="utility to download global DEMs from opentopo API for a given extent")
        dem_options = ['COP30','COP90','SRTMGL1_E','SRTMGL1','SRTM_GL3','NASADEM']
        parser.add_argument('-demtype',help='Select the DEM intended to be downloaded',type=str,default='COP30')
        parser.add_argument('-extent',help="Bounding box extent in single quotes  as 'minx miny maxx maxy' in lat and lon",type=str,required=True)
        parser.add_argument('-apikey',help='Opentopgraphy api key',type=str,required=True)
        parser.add_argument('-out_fn',help='Output filename',type=str,default=None)
        parser.add_argument('-out_proj',help='Final projection of output as EPSG code',type=str,default='EPSG:4326')
        return parser

def get_dem(demtype, bounds, apikey, out_fn=None, proj='EPSG:4326'):
    """
    download a DEM of choice from OpenTopography World DEM
    ## first written by David Shean
    Parameters
    ------------
    demtype: str
        type of DEM to fetch (e.g., COP30, SRTMGL1, SRTMGL1_E, SRTMGL3 etc)
    bounds: list
        geographic aoi extent in format (minx,miny,maxx,maxy)
    apikey: str
        opentopography api key
    out_fn: str
        path to output filename
    t_srs: str
        output DEM projection
    Returns
    -----------
    out_DEM: str
        path to output DEM (useful if the downloaded DEM is reprojected to custom proj)
    """
    import requests
    from distutils.spawn import find_executable
    ### first written by David Shean
    base_url="https://portal.opentopography.org/API/globaldem?demtype={}&west={}&south={}&east={}&north={}&outputFormat=GTiff&API_Key={}"
    if out_fn is None:
        out_fn = '{}.tif'.format(demtype)
    if not os.path.exists(out_fn):
        #Prepare API request url
        #Bounds should be [minlon, minlat, maxlon, maxlat]
        url = base_url.format(demtype, *bounds, apikey)
        print(url)
        #Get
        response = requests.get(url)
        #Check for 200
        if response.ok:
            print ('OK!')
        else:
            print ('Query failed')
            sys.exit()
        #Write to disk
        open(out_fn, 'wb').write(response.content)
    if proj != 'EPSG:4326':
        #Could avoid writing to disk and direclty reproject with rasterio, using gdalwarp for simplicity
        proj_fn = os.path.splitext(out_fn)[0]+'_proj.tif'
        if not os.path.exists(proj_fn):
            output_res = 30
            gdalwarp = find_executable('gdalwarp')
            gdalwarp_call = f"{gdalwarp} -r cubic -co COMPRESS=LZW -co TILED=YES -co BIGTIFF=IF_SAFER -tr {output_res} {output_res} -t_srs '{proj}' {out_fn} {proj_fn}"
            print(gdalwarp_call)
            run_bash_command(gdalwarp_call)
        out_DEM = proj_fn
    else:
        out_DEM = out_fn
    return out_DEM

def run_bash_command(cmd):
    #written by Scott Henderson
    # move to asp_binder_utils
    """Call a system command through the subprocess python module."""
    print(cmd)
    try:
        retcode = subprocess.call(cmd, shell=True)
        if retcode < 0:
            print("Child was terminated by signal", -retcode, file=sys.stderr)
        else:
            print("Child returned", retcode, file=sys.stderr)
    except OSError as e:
        print("Execution failed:", e, file=sys.stderr)


def main():
    parser = get_parser()
    args = parser.parse_args()
    minx,miny,maxx,maxy = args.extent.split(' ')
    bounds = [float(minx),float(miny),float(maxx),float(maxy)]
    print(bounds)
    get_dem(demtype=args.demtype, bounds=bounds, apikey=args.apikey, out_fn=args.out_fn, proj=args.out_proj)
    print("Script is complete")

if __name__=="__main__":
    main()
