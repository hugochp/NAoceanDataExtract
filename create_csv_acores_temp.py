import xarray as xr
import pandas as pd
import cftime

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

# Filtrer les données pour la région des Açores
azores_region = depth_range.sel(lat=slice(30, 50), lon=slice(320, 340))

# Calculer la moyenne des températures sur les profondeurs filtrées
mean_temp_azores = azores_region['thetao'].mean(dim='lev')

# Calculer la moyenne spatiale (latitude et longitude) pour chaque point dans le temps
mean_temp_time = mean_temp_azores.mean(dim=['lat', 'lon'])

# Convertir les temps en datetime
times = mean_temp_time.indexes['time'].to_datetimeindex()

# Convertir en DataFrame
temp_df = pd.DataFrame({'Date': times, 'Temperature': mean_temp_time.values}, columns=['Date', 'Temperature'])

# Formater les dates
temp_df['Date'] = temp_df['Date'].dt.strftime('%d/%m/%Y')

# Sauvegarder en fichier CSV
temp_df.to_csv('azores_temperature.csv', index=False)

print("Le fichier CSV des températures moyennes dans les Açores a été créé avec succès.")
