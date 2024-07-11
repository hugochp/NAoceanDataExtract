import xarray as xr
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np

# Ouvrir le fichier NetCDF
file_path = 'ph_Omon_MPI-ESM1-2-LR_ssp119_r2i1p1f1_gn_201501-203412.nc'
ds = xr.open_dataset(file_path)

# Vérifier si la variable 'ph' et les profondeurs 'lev' sont présentes
if 'ph' in ds.variables and 'lev' in ds.coords:
    ph = ds['ph']
    depths = ds['lev'].sel(lev=slice(100, 200))
    if len(depths) > 4:
        depths = depths[:4]
else:
    raise ValueError("Variable 'ph' or coordinate 'lev' not found in the dataset.")

# Définir la grille 2x2
num_cols = 2
num_rows = 2
fig, axes = plt.subplots(num_rows, num_cols, figsize=(15, 10), squeeze=False)

# Fonction pour mettre à jour les graphiques pour chaque frame
def update(frame):
    fig.suptitle(f'Month: {str(ph["time"].values[frame])[:7]}')
    for idx, depth in enumerate(depths):
        row = idx // num_cols
        col = idx % num_cols
        ax = axes[row, col]
        ax.clear()
        ph_at_depth = ph.sel(lev=depth.item(), method='nearest').isel(time=frame)
        ph_at_depth.plot(ax=ax, add_colorbar=False)
        ax.set_title(f'pH at {depth.item()}m Depth')
        ax.invert_yaxis()  # Inverser l'axe des latitudes

# Définir la vitesse de l'animation (en millisecondes)
animation_speed = 100  #1f per second

# Créer l'animation
ani = FuncAnimation(fig, update, frames=len(ph['time']), interval=animation_speed, repeat=False)

# Afficher l'animation
plt.tight_layout()
plt.show()

# Sauvegarder l'animation (optionnelle)
# ani.save('ph_animation.mp4', writer='ffmpeg', dpi=300)
