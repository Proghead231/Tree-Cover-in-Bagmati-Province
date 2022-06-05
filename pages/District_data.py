import streamlit as st
from main import raw_data
from main import grouped
import sys
import cv2
import pathlib
import os
from PIL import Image
static_maps_path = os.path.join(pathlib.Path().absolute(), 'static_maps')

#Displaying Districtwise data
select_district = st.selectbox("Select district to see district data", (raw_data['district'].unique()))
st.write(raw_data.loc[raw_data["district"] == select_district][["municipality","tof_area_ha", "forest_area_ha", "total_tree_cover_ha", "tof_percent","forest_percent"]])

st.write(f"Total areas for {select_district}:")

st.write(grouped.loc[grouped.index == select_district][["tof_area_ha","forest_area_ha", "total_tree_cover_ha"]])
image = Image.open(os.path.join(static_maps_path, select_district+'.png'))


st.image(image, caption=None, width=800, use_column_width=None, clamp=False, channels="RGB", output_format="auto")
