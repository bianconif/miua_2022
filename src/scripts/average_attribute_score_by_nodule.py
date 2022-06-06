"""Compute the average score for each nodule and attribute over the available
annotations"""
import numpy as np
import pandas as pd

from functions.utilities import get_config

config = get_config()

#Read the nodules metadata
df_nodules = pd.read_csv(filepath_or_buffer = config['nodules_metadata_file'])

#Filter by number of annotations
df_nodules = df_nodules[df_nodules['num_annotations'] >= config['min_annotations_per_nodule']]

#Store the average scores
df_scores = pd.DataFrame()

attributes = df_nodules.columns.to_list()
not_attributes = ['patient_id', 'nodule_id', 'num_annotations', 'annotation_id']
for not_attribute in not_attributes:
    attributes.remove(not_attribute)
attributes.sort()
    
#Describe the data
for attribute in attributes:
    print(f'{attribute}: {np.mean(df_nodules[attribute]):3.2f} \u00B1 '
          f'{np.std(df_nodules[attribute]):3.2f} [{np.min(df_nodules[attribute])}'
          f'-{np.max(df_nodules[attribute])}]')

patient_ids = df_nodules['patient_id'].unique()

for patient_id in patient_ids:
    nodule_ids = df_nodules[df_nodules['patient_id'] == patient_id]['nodule_id'].unique()
    for nodule_id in nodule_ids:
        record = {'nodule_id' : nodule_id, 'patient_id' : patient_id}
        selection = df_nodules[(df_nodules['patient_id'] == patient_id) &
                               (df_nodules['nodule_id'] == nodule_id)]
        for attribute in attributes:
            avg_value = selection[attribute].mean()
            record.update({attribute : avg_value})
        df_scores = df_scores.append(other = record, ignore_index = True)


sorted_cols = [*not_attributes, *attributes]
sorted_cols.remove('annotation_id')
sorted_cols.remove('num_annotations')
df_scores = df_scores[sorted_cols]

#Nodule ids as int
df_scores['nodule_id'] = df_scores['nodule_id'].astype(int) 

#Store to file
df_scores.to_csv(path_or_buf = config['attributes_file'], index = False)
