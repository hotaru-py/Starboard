import os
import numpy as np
import xarray as xr
import matplotlib.pyplot as plt
from skimage.graph import route_through_array

def get_optimal_route(coords):
    dataset = xr.open_dataset('./cmems_mod_glo_wav_anfc_0.083deg_PT3H-i_multi-vars_180.00W-179.92E_80.00S-90.00N_2024-09-05.nc')
    features = {
    'VHM0': 'Spectral significant wave height',
    'VTM10': 'Spectral moments (-1,0) wave period',
    'VTM02': 'Spectral moments (0,2) wave period',
    'VTPK': 'Wave period at spectral peak',
    'VMDR': 'Mean wave direction',
    'VPED': 'Wave principal direction at spectral peak',
    'VSDX': 'Stokes drift U',
    'VSDY': 'Stokes drift V',
    'VHM0_WW': 'Spectral significant wind wave height',
    'VTM01_WW': 'Spectral moments (0,1) wind wave period',
    'VMDR_WW': 'Mean wind wave direction',
    'VHM0_SW1': 'Spectral significant primary swell wave height',
    'VTM01_SW1': 'Spectral moments (0,1) primary swell wave period',
    'VMDR_SW1': 'Mean primary swell wave direction',
    'VHM0_SW2': 'Spectral significant secondary swell wave height',
    'VTM01_SW2': 'Spectral moments (0,1) secondary swell wave period',
    'VMDR_SW2': 'Mean secondary swell wave direction'
    }
    
    def get_closest(array, value):
        return np.abs(array - value).argmin()
    start_lon = get_closest(dataset.longitude.data, coords['from']['longitude'])
    start_lat = get_closest(dataset.latitude.data, coords['from']['latitude'])
    end_lon = get_closest(dataset.longitude.data, coords['to']['longitude'])
    end_lat = get_closest(dataset.latitude.data, coords['to']['latitude'])
    start = (start_lat, start_lon)
    end = (end_lat, end_lon)
    feature_costs = {}
    feature_nans = {}

    for feature in features:
        if hasattr(dataset, feature):
            costs = dataset[feature].data[0]
            feature_costs[f"{feature}_costs"] = costs
            whereAreNans = np.isnan(costs)
            feature_nans[f"{feature}_nans"] = whereAreNans

    for feature in features:
        if hasattr(dataset, feature):
            costs = feature_costs[f"{feature}_costs"]
            whereAreNans = feature_nans[f"{feature}_nans"]
            costs[whereAreNans] = 10**9
            feature_costs[f"{feature}_costs"] = costs

    feature_weights = {
    'VHM0': 5, 'VTM10': 4, 'VTM02': 3, 'VTPK': 4, 'VMDR': 4, 'VPED': 3,
    'VSDX': 2, 'VSDY': 2, 'VHM0_WW': 5, 'VTM01_WW': 3, 'VMDR_WW': 3,
    'VHM0_SW1': 4, 'VTM01_SW1': 3, 'VMDR_SW1': 3, 'VHM0_SW2': 2,
    'VTM01_SW2': 2, 'VMDR_SW2': 2
    }

    final_cost = np.zeros_like(next(iter(feature_costs.values())))
    for feature in features:
        final_cost += feature_costs[f'{feature}_costs'] * feature_weights[feature]
    
    def pathfinding(start, end):
        return route_through_array(final_cost, start, end, fully_connected=True)
    
    indices, weight = pathfinding(start, end)
    indices = np.stack(indices, axis=-1)

    # Create the figure and axis
    fig, ax = plt.subplots(figsize=(10, 5))

    # Background colour
    ax.set_facecolor('#415A77')
    fig.patch.set_facecolor('#415A77')

    # Plot optimal route
    ax.imshow(final_cost, aspect='auto', vmin=np.min(final_cost), vmax=0.5*np.max(final_cost), cmap='winter')

    # Plot the route
    ax.plot(indices[1], indices[0], 'r')

    # Plot start/end points
    ax.plot(start_lon, start_lat, 'o', ms=5, c='k', mfc='w')
    ax.plot(end_lon, end_lat, 's', ms=5, c='w', mfc='k')
    
    # Invert Y-axis
    ax.invert_yaxis()

    # Set axis and ticks to white
    ax.spines['top'].set_color('white')
    ax.spines['bottom'].set_color('white')
    ax.spines['left'].set_color('white')
    ax.spines['right'].set_color('white')
    ax.xaxis.label.set_color('white')
    ax.yaxis.label.set_color('white')
    ax.tick_params(axis='x', colors='white')
    ax.tick_params(axis='y', colors='white')

    if os.path.exists("route.png"):
        os.remove("route.png")

    plt.savefig('route.png')
    plt.close()
