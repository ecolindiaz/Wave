import xarray as xr
import numpy as np
import pandas as pd

def convert_bathymetry_nc_to_txt(nc_file, output_txt):
        ds = xr.open_dataset(nc_file)
        elev = ds['elevation']  # GEBCO's variable



        lon, lat = np.meshgrid(elev['lon'].values, elev['lat'].values)
        depth = -elev.values  # Flip sign: SWAN expects depth positive down

        df = pd.DataFrame({
            'lon': lon.flatten(),
            'lat': lat.flatten(),
            'depth': depth.flatten()
        })

        # Optional: remove land (depth < 0 becomes NaN or 0)
        df = df[df['depth'] > 0]

        df.to_csv(output_txt, sep=' ', index=False, header=False)
        print(f"[✓] Bathymetry saved to {output_txt}")

def convert_wind_nc_to_txt(nc_file, output_txt, time_index=0):
    ds = xr.open_dataset(nc_file)
    u10 = ds['u10'].isel(valid_time=time_index)
    v10 = ds['v10'].isel(valid_time=time_index)

    lon, lat = np.meshgrid(u10['longitude'].values, u10['latitude'].values)

    df = pd.DataFrame({
        'lon': lon.flatten(),
        'lat': lat.flatten(),
        'u10': u10.values.flatten(),
        'v10': v10.values.flatten()
    })

    df = df.dropna()
    df.to_csv(output_txt, sep=' ', index=False, header=False)
    print(f"[✓] Saved wind to {output_txt}")

# Example usage:
convert_bathymetry_nc_to_txt('bathymetry.nc', 'bathymetry.txt')
convert_wind_nc_to_txt('wind.nc', 'wind.txt')
