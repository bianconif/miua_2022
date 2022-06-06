## Description
This repository contains the code to reproduce the results presented in the following paper:
- Correlation between IBSI morphological features and manually-annotated shape attributes on lung lesions at CT, accepted for Medical Image Understading and Analysis ([MIUA 2022](https://www.miua2022.com/d)), Cambridge, United Kingdom, 27-29 July 2022

## Usage
1. Select the features to compute and adjust the settings in the `config.yaml` file if required.
  - Note: the landing folders defined in `config.yaml` needs to be created beforehand (the routines do not create them automatically; and error will be returned if the folders do not exist).
2. Execute the `src/scripts/patient_population.py` script to extract the metadata at the scan and nodule level. The results will be stored in `scans_metadata@config.yaml` and `nodules_metadata@config.yaml`
3. Execute the `src/scripts/average_attribute_score_by_nodule.py` to compute the average radiological score for each nodule and attribute over the available annotations. The results will be stored in `attributes_file@config.yaml`
4. Execute the `src/scripts/compute_features.py` script to compute the shape features on each nodule. The results will be stored in `features_files@config.yaml`
5. Execute the `src/scripts/correlation_analysis.py` to assess the correlations among the imaging features and the manually-assigned radiological scores. The results will be stored in `correlation_results_files@config.yaml`

## Dependencies
- [Matplotlib 3.3.2](https://matplotlib.org/)
- [Nibabel 3.2.1](https://nipy.org/nibabel/gettingstarted.html)
- [Numpy 1.19.1](https://numpy.org/)
- [Pandas 1.0.5](https://pandas.pydata.org/)
- [Pylidc 0.2.2](https://pylidc.github.io/)
- [radiomics_pg 0.1.0-alpha](https://github.com/bianconif/radiomics_pg)
- [Seaborn 0.11.1](https://seaborn.pydata.org/)
- [scikit-image 1.17.2](https://scikit-image.org/)
- [tabulate 0.8.9](https://pypi.org/project/tabulate/)

## License
Released under [MIT License](https://opensource.org/licenses/MIT)

Copyright (c) 2022

Author: [Francesco Bianconi](www.bianconif.net), [bianco@ieee.org](mailto:bianco@ieee.org)

## Disclaimer
The information and content available on this repository are provided with no warranty whatsoever. Any use for scientific or any other purpose is conducted at your own risk and under your own responsibility. The authors are not liable for any damages - including any consequential damages - of any kind that may result from the use of the materials or information available on this repository or of any of the products or services hereon described.
