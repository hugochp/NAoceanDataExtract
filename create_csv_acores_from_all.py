import xarray as xr
import pandas as pd
import cftime
import matplotlib.pyplot as plt
from tkinter import Tk
from tkinter.filedialog import askopenfilenames

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
    csv_filename = 'azores_temperature.csv'
    temp_df.to_csv(csv_filename, index=False)

    print("Le fichier CSV des températures moyennes dans les Açores a été créé avec succès.")

    # Lire et afficher le fichier CSV
    print("\nContenu du fichier CSV:")
    print(temp_df)

    # Tracer la courbe des températures moyennes
    plt.figure(figsize=(10, 5))
    plt.plot(temp_df['Temperature'], marker='o', linestyle='-')
    plt.xlabel('Index')
    plt.ylabel('Temperature (°C)')
    plt.title('Mean Temperature in the Azores (100-200m Depth)')
    plt.grid(True)
    plt.tight_layout()

    # Afficher la courbe
    plt.show()
