'''Compute the shape features on each nodule'''
from collections import OrderedDict
import pandas as pd

import nibabel as nib
import numpy as np
import pylidc as pl
from pylidc.utils import consensus

from radiomics_pg.utilities.misc import Roi

from functions.utilities import features_lut, get_config

config = get_config()

#Read the nodules metadata
df_nodules = pd.read_csv(filepath_or_buffer = '../data/attributes.csv')

df_features = pd.DataFrame()

#Get the unique patient ids
patient_ids = df_nodules['patient_id'].unique()
patient_ids.sort()

for patient_id in patient_ids:
    
    #Get the dicom folder
    scan = pl.query(pl.Scan).filter(pl.Scan.patient_id == patient_id).first()
    dicom_folder = scan.get_path_to_dicom_files()   
    nodules = scan.cluster_annotations() 
    
    #Create an empty mask array the same size as the input scan
    voxel_model = scan.to_volume()
    mask = np.zeros(voxel_model.shape).astype(np.int8)    
    
    nodule_ids = df_nodules[df_nodules['patient_id'] == patient_id]['nodule_id'].unique()
    
    for nodule_id in nodule_ids:
    
        nodule = nodules[nodule_id]     
    
        #***************************************************************************
        #*************************** ROI definition ********************************
        #***************************************************************************
        
        #Reset the mask
        mask[:] = 0
        
        #Get the consensus ROI
        cmask, cbbox, masks = consensus(nodule, clevel=0.5)    
        mask[cbbox][cmask] = True
    
        #Cache the ROI in nii format
        nii_roi = nib.Nifti1Image(dataobj = mask, affine = np.eye(4))
        nii_roi.to_filename(filename = config['roi_cache'])
    
        #***************************************************************************
        #***************************************************************************
        #***************************************************************************
    
        #Generate the ROI in radiomics_pg format
        roi = Roi.from_dcm_and_nii(mask_file = config['roi_cache'], scan_folder = dicom_folder)
        
        #debug_fig = plt.figure()
        #roi.draw_mesh(fig = debug_fig, other_elems=['aabb'])
        #debug_fig.show()
    
        #Compute and store the features
        record = OrderedDict({'patient_id' : patient_id, 'nodule_id' : nodule_id})
        for feature_to_compute in config['features_to_compute']:
                    
            if config['verbose']:
                print(f'Computing: patient_id = {patient_id}, nodule_id = {nodule_id}, feature = {feature_to_compute}')
        
            feature_value = features_lut[feature_to_compute](roi)
            record.update({feature_to_compute : feature_value})
    
        df_features = df_features.append(record, ignore_index = True)
df_features.to_csv(path_or_buf = config['features_file'], index = False)
    