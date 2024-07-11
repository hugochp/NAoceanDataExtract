import xarray as xr
import pandas as pd
import cftime
import matplotlib.pyplot as plt
from tkinter import Tk
from tkinter.filedialog import askopenfilenames
import os

# Créer une fenêtre Tkinter
root = Tk()
root.withdraw()  # Cacher la fenêtre principale

# Ouvrir un sélecteur de fichiers pour choisir les fichiers NetCDF
file_paths = askopenfilenames(
    title="Sélectionner les fichiers NetCDF",
    filetypes=[("NetCDF files", "*.nc"), ("All files", "*.*")]
)

if not file_paths:
    print("Aucun fichier sélectionné.")
else:
    # Charger les fichiers NetCDF avec xarray
    datasets = [xr.open_dataset(fp) for fp in file_paths]

    # Extraire le nom du modèle et le scénario SSP à partir du premier fichier NetCDF
    filename_parts = os.path.basename(file_paths[0]).split('_')
    model_name = filename_parts[2]
    ssp_scenario = filename_parts[3]

    # Combiner les datasets en une seule
    combined_ds = xr.concat(datasets, dim='time')

    # Filtrer les profondeurs entre 100 et 200 mètres
    depth_range = combined_ds.sel(lev=slice(100, 200))

    # Filtrer les données pour la région des Açores
    azores_region = depth_range.sel(lat=slice(30, 50), lon=slice(320, 340))

    # Liste des variables à traiter
    variables = {
        'Temperature': 'thetao',
        'pH': 'ph',
        'Nitrate': 'no3',
        'Carbon dioxide': 'co2',
        'Oxygen': 'o2',
        'Salinity': 'so'
    }

    for var_name, var_key in variables.items():
        if var_key in azores_region:
            # Calculer la moyenne des variables sur les profondeurs filtrées
            mean_var_azores = azores_region[var_key].mean(dim='lev')

            # Calculer la moyenne spatiale (latitude et longitude) pour chaque point dans le temps
            mean_var_time = mean_var_azores.mean(dim=['lat', 'lon'])

            # Convertir les temps en datetime
            times = mean_var_time.indexes['time'].to_datetimeindex()

            # Convertir en DataFrame
            temp_df = pd.DataFrame({'Date': times, var_name: mean_var_time.values}, columns=['Date', var_name])

            # Formater les dates
            temp_df['Date'] = temp_df['Date'].dt.strftime('%d/%m/%Y')

            # Sauvegarder en fichier CSV
            csv_filename = f'{model_name}_{ssp_scenario}_{var_name.lower()}_azores.csv'
            temp_df.to_csv(csv_filename, index=False)

            print(f"Le fichier CSV des {var_name.lower()} moyennes dans les Açores a été créé avec succès.")

            # Tracer la courbe des variables moyennes
            plt.figure(figsize=(10, 5))
            plt.plot(temp_df[var_name], marker='o', linestyle='-')
            plt.xlabel('Index')
            plt.ylabel(f'{var_name} (Unit)')  # Remplacer (Unit) par l'unité appropriée pour chaque variable
            plt.title(f'Mean {var_name} in the Azores (100-200m Depth)')
            plt.grid(True)
            plt.tight_layout()

            # Afficher la courbe
            plt.show()
