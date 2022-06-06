"""Summarise te population metadata"""
import pandas as pd

from functions.utilities import get_config

config = get_config()

#Scan level
df_scans = pd.read_csv(filepath_or_buffer = config['scans_metadata_file'])
df_nodules = pd.read_csv(filepath_or_buffer = config['nodules_metadata_file'])

#Filter by number of annotations
df_nodules = df_nodules[df_nodules['num_annotations'] >= config['min_annotations_per_nodule']]

#Filter the scans by patient_id
patient_ids = df_nodules['patient_id'].unique()
df_scans = df_scans[df_scans['patient_id'].isin(patient_ids)]

print(f"Num patients = {len(df_scans['patient_id'].unique())}")
print(f"{df_scans['gender'].value_counts()}")
print(f"age = {df_scans['age'].mean():3.1f} +/- {df_scans['age'].std():3.1f} "
      f"[{df_scans['age'].min()}--{df_scans['age'].max()}]")
print(f"Tube voltage = [{df_scans['tube_voltage'].min()}--{df_scans['tube_voltage'].max()} yr]")
print(f"In-plane pixel spacing = [{df_scans['pixel_spacing'].min():4.2f}--{df_scans['pixel_spacing'].max():4.2f} mm]")
print(f"Slice thickness = [{df_scans['slice_thickness'].min()}--{df_scans['slice_thickness'].max()} mm]")
print(f"Slice spacing = [{df_scans['slice_spacing'].min()}--{df_scans['slice_spacing'].max()} mm]")
#print(df_scans['gender'].describe())