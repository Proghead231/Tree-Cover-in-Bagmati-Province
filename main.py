import streamlit as st
import pandas as pd
import geopandas as gpd
import os
from pyproj import CRS
from streamlit_folium import st_folium
import folium
import pathlib


path = pathlib.Path().absolute()

#Data with all info 
data = pd.read_csv(os.path.join(path, "merged_csv.csv"))

#Creating GPD and reprojecting
data['geometry'] = gpd.GeoSeries.from_wkt(data['geometry'])
data_gdf = gpd.GeoDataFrame(data, geometry='geometry')
data_gdf = data_gdf.set_crs('epsg:32645', allow_override = True)
data_gdf.crs = CRS.from_epsg(32645)
data_gdf = data_gdf.to_crs(epsg = 4326)
data_gdf['geoid'] = data_gdf.index.astype(str)
data_gdf = data_gdf.dropna()
data = data_gdf[["geoid","municipality", "district","tof_area_ha", "forest_area_ha", "total_tree_cover_ha", "tof_percent","forest_percent", "geometry"]]


st.title("Tree Cover Bagmati Province")

#Selectbox for changing type of the maps
add_select = st.selectbox("Select Basemap",("OpenStreetMap", "Stamen Terrain","Stamen Toner"))

# Create a Map instance
m = folium.Map(location=[27.5, 85.5], tiles = add_select, zoom_start=8, control_scale=True)


# Plot a choropleth map
# Notice: 'geoid' column that we created earlier needs to be assigned always as the first column
custom_scale1 = (data['tof_percent'].quantile((0,0.2,0.4,0.6,0.8,1))).tolist()
custom_scale2 = (data['forest_percent'].quantile((0,0.2,0.4,0.6,0.8,1))).tolist()
tof_col = 'tof_percent'
forest_col = 'forest_percent'

def maps(column, scale):
    folium.Choropleth(
    geo_data=data,
    name='TOF',
    data=data,
    columns=['geoid', column],
    key_on='feature.id',
    fill_color='YlOrRd',
    fill_opacity=0.7,
    line_opacity=0.2,
    line_color='white', 
    line_weight=0,
    highlight=False, 
    smooth_factor=1.0,
    threshold_scale=scale,
    legend_name= column).add_to(m)
    return st_folium(m, width = 725)

select_map_data = st.selectbox("Select Tree Cover Data to Display", ("TOF", "Forest"))
if select_map_data == "TOF":
    maps(tof_col, custom_scale1)
else:
    maps(forest_col, custom_scale2)

#Displaying Raw data
raw_data = data_gdf[["municipality", "district","tof_area_ha", "forest_area_ha", "total_tree_cover_ha", "tof_percent","forest_percent"]].drop_duplicates(subset = ['municipality', 'district'], keep = 'first')
if st.checkbox("Show All Data", False):
    st.write(raw_data)

#Calculating total areas by district
groups = raw_data[["district", "tof_area_ha","forest_area_ha", "total_tree_cover_ha"]]
grouped = groups.groupby(by = "district").sum()
st.write(grouped)


