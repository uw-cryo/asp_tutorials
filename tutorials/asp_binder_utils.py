import numpy as np
import pandas as pd
from scipy import stats 
import os,sys,glob
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
import rasterio
from osgeo import gdal
import geopandas as gpd
import contextily as ctx
from pyproj import Proj, transform

import subprocess


def get_clim(ar):
    try:
        clim = np.percentile(ar.compressed(),(2,98))
    except:
        clim = np.percentile(ar,(2,98))
    return clim
def find_common_clim(im1,im2):
    perc1 = get_clim(im1)
    perc2 = get_clim(im2)
    perc = (np.min([perc1[0],perc2[0]]),np.max([perc1[1],perc2[1]]))
    abs_max = np.max(np.abs(perc))
    perc = (-abs_max,abs_max)
    return perc
def fn_2_ma(fn,b=1):
    ds = rasterio.open(fn)
    ar = ds.read(b)
    ndv = get_ndv(ds)
    ma_ar = np.ma.masked_equal(ar,ndv)
    return ma_ar
def get_ndv(ds):
    no_data = ds.nodatavals[0]
    if no_data == None:
        #this means no data is not set in tif tag, nead to cheat it from raster
        ndv = ds.read(1)[0,0]
    else:
        ndv = no_data
    return ndv

def plot_stereo_results(out_folder,ax):
    dem = glob.glob(out_folder+'*-DEM.tif')[0]
    l_img = glob.glob(out_folder+'*L.tif')[0]
    r_img = glob.glob(out_folder+'*R.tif')[0]
    disp = glob.glob(out_folder+'*-F.tif')[0]
    error_fn = glob.glob(out_folder+'*In*.tif')[0]
    print("Found files {}\n {}\n {}\n {}\n {}\n".format(l_img,r_img,disp,error_fn,dem))
    dem_ma = fn_2_ma(dem,1)
    l_img_ma = fn_2_ma(l_img)
    r_img_ma = fn_2_ma(r_img)
    dx_ma = fn_2_ma(disp,1)
    dy_ma = fn_2_ma(disp,2)
    error_ma = fn_2_ma(error_fn,1)
    dem_ds = gdal.Open(dem)
    producttype = 'hillshade'
    hs_ds = gdal.DEMProcessing('',dem_ds,producttype,format='MEM')
    hs = hs_ds.ReadAsArray()
    #fig,ax = plt.subplots(3,2,figsize=(6,5))
    axa = ax.ravel()
    cmap_img = 'gray'
    cmap_disp = 'RdBu'
    cmap_error = 'inferno'
    plot_ar(l_img_ma,ax=axa[0],clim=get_clim(l_img_ma),cbar=False,cmap=cmap_img)
    #print(get_clim(l_img_ma))
    plot_ar(l_img_ma,ax=axa[1],clim=get_clim(r_img_ma),cbar=False,cmap=cmap_img)
    disp_clim = find_common_clim(dx_ma,dy_ma)
    plot_ar(dx_ma,ax=axa[2],clim=disp_clim,cmap=cmap_disp,label='dx (px)')
    plot_ar(dy_ma,ax=axa[3],clim=disp_clim,cmap=cmap_disp,label='dy (px)')
    #plt.colorbar(dx_im,axa[2])
    #plt.colorbar(dy_im,axa[3])
    #error_im = axa[4].imshow(error_ma,cmap=cmap_error,clim=get_clim(error_ma),interpolation='none')
    plot_ar(error_ma,ax=axa[4],clim=get_clim(error_ma),cmap=cmap_error,label='Intersection Error(m)')
    #plt.colorbar(error_im,ax=axa[4])
    axa[5].imshow(hs,cmap=cmap_img,clim=get_clim(hs),interpolation='none')
    plot_ar(dem_ma,ax=axa[5],clim=get_clim(dem_ma),label='HAE (m WGS84)',alpha=0.6)
    #print(get_clim(dem_ma))
    #plt.colorbar(dem_im,axa[5])
    plt.tight_layout()
    #print(type(dem_ma))
    for idx,axa in enumerate(ax.ravel()):
        if idx == 4:
            axa.set_facecolor('gray')
        else:
            axa.set_facecolor('k')
    
def plot_ar(im,ax,clim,cmap=None,label=None,cbar=True,alpha=1):
    if cmap:
        img = ax.imshow(im,cmap=cmap,clim=clim,alpha=alpha,interpolation='None')
    else:
        img = ax.imshow(im,clim=clim,alpha=alpha,interpolation='None')
    if cbar:
        divider = make_axes_locatable(ax)
        #cax = divider.append_axes("right", size="5%", pad=0.05)
        #cax = divider.append_axes("right", size="5%", pad="2%")
        cax = divider.append_axes("right", size="2%", pad="1.5%")
        cb = plt.colorbar(img,cax=cax,ax=ax,extend='both')
        cax.set_ylabel(label)
    ax.set_xticks([])
    ax.set_yticks([])
    
def subsetBBox(rast,proj_out):
    #originally written by Justing Pflug 
    # rasterio open data
    rB = rasterio.open(rast)
    proj_in = rB.crs
    # rasterio get bounding box
    [L,B,R,T] = rB.bounds

    if proj_in == proj_out:
        return L, R, T, B
    else:
        incord = Proj(init=proj_in)
        outcord = Proj(init=proj_out)

        [Left,Bottom] = transform(incord,outcord,L,B)
        [Right,Top] = transform(incord,outcord,R,T)
        return Left, Bottom, Right, Top

def run_bash_command(cmd,verbose=False):
    #written by Scott Henderson
    # move to asp_binder_utils
    """Call a system command through the subprocess python module."""
    print(cmd)
    try:
        if verbose:
            retcode = subprocess.call(cmd,shell=True)
        else:
            retcode = subprocess.call(cmd, stdout=subprocess.DEVNULL,
                stderr=subprocess.STDOUT,shell=True)
        if retcode < 0:
            print("Child was terminated by signal", -retcode, file=sys.stderr)
        else:
            print("Child returned", retcode, file=sys.stderr)
    except OSError as e:
        print("Execution failed:", e, file=sys.stderr)

def plot_alignment_maps(refdem,src_dem,initial_elevation_difference_fn,aligned_elevation_difference_fn):
    f,ax = plt.subplots(2,2,figsize=(8,6))
    axa = ax.ravel()

    refdem_ma = fn_2_ma(refdem,1)
    src_dem_ma = fn_2_ma(src_dem)
    initial_diff = fn_2_ma(initial_elevation_difference_fn)
    final_diff = fn_2_ma(aligned_elevation_difference_fn)

    refdem_ds = gdal.Open(refdem)
    producttype = 'hillshade'
    ref_hs_ds = gdal.DEMProcessing('',refdem_ds,producttype,format='MEM')
    ref_hs = ref_hs_ds.ReadAsArray()

    src_dem_ds = gdal.Open(src_dem)
    producttype = 'hillshade'
    src_hs_ds = gdal.DEMProcessing('',src_dem_ds,producttype,format='MEM')
    src_hs = src_hs_ds.ReadAsArray()
    #fig,ax = plt.subplots(3,2,figsize=(6,5))
    axa = ax.ravel()
    cmap_diff = 'RdBu'
    cmap_hs = 'gray'
    axa[0].imshow(ref_hs,cmap=cmap_hs,clim=get_clim(ref_hs),interpolation='none')
    plot_ar(refdem_ma,ax=axa[0],clim=get_clim(refdem_ma),label='Elevation (m WGS84)',alpha=0.6)
    axa[0].set_title('Reference DEM')

    axa[1].imshow(src_hs,cmap=cmap_hs,clim=get_clim(src_hs),interpolation='none')
    plot_ar(src_dem_ma,ax=axa[1],clim=get_clim(src_dem_ma),label='Elevation (m WGS84)',alpha=0.6)
    axa[1].set_title('Source DEM')

    diff_clim = find_common_clim(initial_diff,final_diff)
    plot_ar(initial_diff,ax=axa[2],clim=diff_clim,cmap=cmap_diff,label=' Elevation difference (m)')
    axa[2].set_title("Before alignment")

    plot_ar(final_diff,ax=axa[3],clim=diff_clim,cmap=cmap_diff,label='Elevation difference (m)')
    axa[3].set_title("After alignment")
    plt.tight_layout()

    f2,ax2 = plt.subplots()
    bins = np.linspace(diff_clim[0],diff_clim[1], 128)
    initial_mad = stats.median_abs_deviation(initial_diff.compressed())
    initial_med = np.median(initial_diff.compressed())

    final_mad = stats.median_abs_deviation(final_diff.compressed())
    final_med = np.median(final_diff.compressed())

    title = f" Pre-alignment elev. diff. median: {initial_med: .2f} m, mad: {initial_mad: .2f} m\nPost-alignment elev. diff. median: {final_med: .2f} m, mad: {final_mad: .2f} m"
    
    ax2.hist(initial_diff.compressed(),bins=bins,color='blue',alpha=0.5,label='Initial')
    ax2.hist(final_diff.compressed(),bins=bins,color='green',alpha=0.5,label='Final')
    ax2.axvline(x=0,linestyle='--',linewidth=1,color='k')
    ax2.legend()
    ax2.set_xlabel('Elevation difference')
    ax2.set_ylabel('#pixels')
    ax2.set_title(title)

def read_geodiff(csv_fn):
    #from David Shean
    resid_cols=['lon', 'lat', 'diff']
    resid_df = pd.read_csv(csv_fn, comment='#', names=resid_cols)
    resid_gdf = gpd.GeoDataFrame(resid_df, geometry=gpd.points_from_xy(resid_df['lon'], resid_df['lat'], crs='EPSG:4326'))
    return resid_gdf

def plot_alignment_maps_altimetry(reference_altimetry,src_dem,initial_elevation_difference_fn,
                        aligned_elevation_difference_fn,plot_crs,provider=ctx.providers.Esri.WorldImagery,diff_clim=(-5,5)):
    f,ax = plt.subplots(2,2,figsize=(8,6))
    axa = ax.ravel()
    markersize = 1
    #ref_alitmetry_gdf = gpd.read_file(reference_altimetry)
    src_dem_ma = fn_2_ma(src_dem)
    initial_diff = read_geodiff(initial_elevation_difference_fn)
    final_diff = read_geodiff(aligned_elevation_difference_fn)
    
    # change point file crs
    initial_diff = initial_diff.to_crs(plot_crs)
    final_diff = final_diff.to_crs(plot_crs)
    reference_altimetry = reference_altimetry.to_crs(plot_crs)
    
    src_dem_ds = gdal.Open(src_dem)
    producttype = 'hillshade'
    src_hs_ds = gdal.DEMProcessing('',src_dem_ds,producttype,format='MEM')
    src_hs = src_hs_ds.ReadAsArray()
    #fig,ax = plt.subplots(3,2,figsize=(6,5))
    axa = ax.ravel()
    cmap_diff = 'RdBu'
    cmap_hs = 'gray'
    if len(reference_altimetry)>10000:
        reference_altimetry.sample(10000).plot('h_mean',ax=axa[0])
        ctx.add_basemap(ax=axa[0],crs="EPSG:4326",attribution=False,source=provider)
    else:
        reference_altimetry.plot(column='h_mean',ax=axa[0],markersize=markersize)
    ctx.add_basemap(ax=axa[0],crs=plot_crs,attribution=False,source=provider)
    axa[0].set_title('Reference ICESat-2 altimetry points')

    axa[1].imshow(src_hs,cmap=cmap_hs,clim=get_clim(src_hs),interpolation='none')
    plot_ar(src_dem_ma,ax=axa[1],clim=get_clim(src_dem_ma),label='Elevation (m WGS84)',alpha=0.6)
    axa[1].set_title('Source DEM')

    ## Difference maps

    initial_diff.plot(column='diff',ax=axa[2],cmap='RdBu',vmin=diff_clim[0],vmax=diff_clim[1],markersize=markersize)
    final_diff.plot(column='diff',ax=axa[3],cmap='RdBu',vmin=diff_clim[0],vmax=diff_clim[1],markersize=markersize)   
    axa[2].set_title("Before alignment")
    axa[3].set_title("After alignment")
    ctx.add_basemap(ax=axa[2],crs=plot_crs,attribution=False,
                    source = provider)
    ctx.add_basemap(ax=axa[3],crs=plot_crs,attribution=False,
                    source = provider)
    axa[0].set_xticks([])
    axa[2].set_xticks([])
    axa[3].set_xticks([])

    axa[0].set_yticks([])
    axa[2].set_yticks([])
    axa[3].set_yticks([])

    
    plt.tight_layout()

    f2,ax2 = plt.subplots()
    bins = np.linspace(diff_clim[0],diff_clim[1], 128)
    initial_mad = stats.median_abs_deviation(initial_diff['diff'].values)
    initial_med = np.median(initial_diff['diff'].values)

    final_mad = stats.median_abs_deviation(final_diff['diff'].values)
    final_med = np.median(final_diff['diff'].values)

    title = f" Pre-alignment elev. diff. median: {initial_med: .2f} m, mad: {initial_mad: .2f} m\nPost-alignment elev. diff. median: {final_med: .2f} m, mad: {final_mad: .2f} m"
    
    ax2.hist(initial_diff['diff'].values,bins=bins,color='blue',alpha=0.5,label='Initial')
    ax2.hist(final_diff['diff'].values,bins=bins,color='green',alpha=0.5,label='Final')
    ax2.axvline(x=0,linestyle='--',linewidth=1,color='k')
    ax2.legend()
    ax2.set_xlabel('Elevation difference (m)')
    ax2.set_ylabel('#pixels')
    ax2.set_title(title)