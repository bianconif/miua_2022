"""Assess the correlations between the imaging features and the manually-
assigned radiological scores (attributes)"""
from tabulate import tabulate
import pandas as pd
from scipy.stats import pearsonr, spearmanr

import matplotlib.pyplot as plt
import seaborn as sns

plt.rcParams.update({
    "text.usetex": True,
    "font.family": "sans-serif",
    "font.sans-serif": ["Helvetica"]})
# for Palatino and other serif fonts use:
plt.rcParams.update({
    "text.usetex": True,
    "font.family": "serif",
    "font.serif": ["Palatino"],
})
# It's also possible to use the reduced notation by directly setting font.family:
plt.rcParams.update({
  "text.usetex": True,
  "font.family": "Helvetica"
})

from functions.utilities import get_config

config = get_config()

#Load the features and the attributes
df_features = pd.read_csv(filepath_or_buffer = config['features_file'])
df_attributes = pd.read_csv(filepath_or_buffer = config['attributes_file'])

#Join the dataframes 
df_complete = pd.merge(df_features, df_attributes,  
                       on = ['patient_id', 'nodule_id'],
                       how = 'inner')
df_complete.dropna(inplace = True)

#Compute the correlations
df_correlation = pd.DataFrame()

#Put the scatter plots here
fig, axes = plt.subplots(nrows = len(config['features_to_compute']), 
                         ncols = len(config['selected_attributes']))

#for attribute_1 in config['selected_attributes']:
    #for attribute_2 in config['selected_attributes']:
        #attribute_1_values = df_complete[attribute_1].to_numpy()
        #attribute_2_values = df_complete[attribute_2].to_numpy()
        #spearman, _ = spearmanr(attribute_1_values, attribute_2_values)
        #sns.scatterplot(x = attribute_1_values, y = attribute_2_values)
        #plt.xlabel(attribute_1)
        #plt.ylabel(attribute_2)
        #plt.title(f'{spearman:3.2f}')
        #plt.show()
        #a = 0
    

for f, feature in enumerate(config['features_to_compute']):
    for a, attribute in enumerate(config['selected_attributes']):
        attribute_values = df_complete[attribute].to_numpy()
        feature_values = df_complete[feature].to_numpy()
        
        pearson, _ = pearsonr(attribute_values, feature_values)
        spearman, _ = spearmanr(attribute_values, feature_values)
        
        record = {'Feature': feature, 'Attribute': attribute,
                  'Pearson': pearson, 'Spearman': spearman}
        df_correlation = df_correlation.append(other = record, 
                                               ignore_index = True)
        
        #sns.scatterplot(ax = axes[f,a], x = attribute_values, y = feature_values)
        #axes[f,a].set_xlabel(f'Attribute: {attribute}')
        #axes[f,a].set_ylabel(f'Feature: {feature}')
#plt.show()

#Display the DataFrame
print(tabulate(df_correlation, headers = 'keys', tablefmt = 'psql',
               floatfmt="3.2f"))

#Store the results
df_correlation.to_csv(path_or_buf = config['correlation_results_file'],
                      index = False)
    
        