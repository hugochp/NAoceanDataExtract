import xarray as xr
import numpy as np
import matplotlib.pyplot as plt

# Chemins vers les fichiers NetCDF
file_paths = [
    "thetao_Omon_GFDL-ESM4_ssp119_r1i1p1f1_gr_201501-203412.nc",
    "thetao_Omon_GFDL-ESM4_ssp119_r1i1p1f1_gr_203501-205412.nc",
    "thetao_Omon_GFDL-ESM4_ssp119_r1i1p1f1_gr_205501-207412.nc",
    "thetao_Omon_GFDL-ESM4_ssp119_r1i1p1f1_gr_207501-209412.nc",
    "thetao_Omon_GFDL-ESM4_ssp119_r1i1p1f1_gr_209501-210012.nc"
]

# Charger les fichiers NetCDF avec xarray
datasets = [xr.open_dataset(fp) for fp in file_paths]

# Combiner les datasets en une seule
combined_ds = xr.concat(datasets, dim='time')

# Filtrer les profondeurs entre 100 et 200 mètres
depth_range = combined_ds.sel(lev=slice(100, 200))

# Calculer la moyenne des températures sur le temps et les profondeurs filtrées
mean_temp = depth_range['thetao'].mean(dim=['time', 'lev'])

# Extraire les données de latitude et longitude
lat = mean_temp['lat']
lon = mean_temp['lon']

# Afficher la moyenne des températures
plt.figure(figsize=(12, 6))
plt.contourf(lon, lat, mean_temp, cmap='coolwarm')
plt.colorbar(label='Mean Sea Water Potential Temperature (°C)')
plt.title('Mean Sea Water Potential Temperature (100-200m)')
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.show()
