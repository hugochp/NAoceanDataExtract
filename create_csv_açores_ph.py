import xarray as xr
import pandas as pd

# Ouvrir le fichier NetCDF
file_path = 'ph_Omon_MPI-ESM1-2-LR_ssp119_r2i1p1f1_gn_201501-203412.nc'
ds = xr.open_dataset(file_path)

# Sélectionner les données des Açores (coordonnées approximatives)
ds_acores = ds.sel(j=slice(50, 100), i=slice(70, 170))

# Vérifier si la variable 'ph' et les profondeurs 'lev' sont présentes
if 'ph' in ds_acores.variables and 'lev' in ds_acores.coords:
    ph = ds_acores['ph']
    depths = ds_acores['lev'].sel(lev=slice(100, 200))

    # Calculer la moyenne du pH sur les profondeurs sélectionnées
    ph_mean_depths = ph.sel(lev=depths).mean(dim='lev')

    # Calculer la moyenne spatiale pour la région des Açores
    ph_mean_spatial = ph_mean_depths.mean(dim=['i', 'j'])

    # Extraire la période 2015-2035
    ph_acores_period = ph_mean_spatial.sel(time=slice('2015-01-01', '2035-12-31'))

    # Convertir en DataFrame pour l'exportation en CSV
    ph_acores_df = ph_acores_period.to_dataframe().reset_index()
    ph_acores_df['Date'] = ph_acores_df['time'].dt.strftime('%d/%m/%Y')
    ph_acores_df = ph_acores_df[['Date', 'ph']]

    # Enregistrer dans un fichier CSV
    output_file = 'ph_acores_2015_2035.csv'
    ph_acores_df.to_csv(output_file, index=False, header=False)

    print(f"Fichier CSV créé : {output_file}")
else:
    print("Variable 'ph' or coordinate 'lev' not found in the dataset.")
