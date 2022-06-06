import yaml

from radiomics_pg.features.shape.mask import area_density, asphericity,\
     compactness_1,compactness_2, ibsi_elongation, ibsi_flatness,\
     mesh_volume, sphericity, spherical_disproportion, volume_density


def get_config(config_file='../config.yaml'):
    """Read the configuration data
    
    Parameters
    ----------
    config_file : str
        Path to the YAML configuration file
        
    Returns
    -------
    config : dict
        The configuration dictionary
    """
    config = None
    with open(config_file, 'r') as stream:
        config = yaml.load(stream)
    
    return config 

features_lut = {'AreaDensity'            : area_density,
                'Asphericity'            : asphericity,
                'Compactness1'           : compactness_1,
                'Compactness2'           : compactness_2,
                'Elongation'             : ibsi_elongation,
                'Flatness'               : ibsi_flatness,
                'SphericalDisproportion' : spherical_disproportion,
                'Sphericity'             : sphericity,
                'Volume'                 : mesh_volume,
                'VolumeDensity'          : volume_density}