import xarray as xr
import matplotlib.pyplot as plt
import numpy as np

# Ouvrir le fichier NetCDF
file_path = 'ph_Omon_MPI-ESM1-2-LR_ssp119_r2i1p1f1_gn_201501-203412.nc'
ds = xr.open_dataset(file_path)

# Sélectionner les données des Açores
ds_acores = ds.sel(j=slice(50, 100), i=slice(70, 170))

# Afficher les différentes profondeurs disponibles
if 'lev' in ds_acores.coords:
    print("Profondeurs disponibles (lev) :")
    print(ds_acores['lev'].values)
else:
    print("La coordonnée 'lev' n'est pas trouvée dans le dataset.")

# Vérifier si la variable 'ph' est présente
if 'ph' in ds_acores.variables:
    ph = ds_acores['ph']

    # Filtrer les profondeurs entre 100m et 200m incluses
    depths = ds_acores['lev'].sel(lev=slice(100, 200))

    # Limiter à quatre profondeurs pour une grille 2x2
    if len(depths) > 4:
        depths = depths[:4]

    # Définir la grille 2x2
    num_cols = 2
    num_rows = 2

    fig, axes = plt.subplots(num_rows, num_cols, figsize=(15, 10), squeeze=False)

    for idx, depth in enumerate(depths):
        row = idx // num_cols
        col = idx % num_cols

        # Sélectionner la profondeur actuelle
        ph_at_depth = ph.sel(lev=depth.item(), method='nearest')

        # Calculer la moyenne du pH sur la période 2015-2034
        ph_mean_at_depth = ph_at_depth.mean(dim='time')

        # Tracer la carte dans le subplot approprié
        ax = axes[row, col]
        ph_mean_at_depth.plot(ax=ax, add_colorbar=True)
        ax.set_title(f'Mean pH at {depth.item()}m Depth (Açores)')
        ax.invert_yaxis()  # Inverser l'axe des latitudes

    # Ajuster l'espacement entre les sous-graphiques
    plt.tight_layout()
    plt.show()
else:
    print("Variable 'ph' not found in the dataset.")
