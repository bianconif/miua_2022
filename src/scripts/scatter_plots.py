"""Generate the scatter plots"""
import pandas as pd
from matplotlib import rc
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns

from functions.utilities import get_config

config = get_config()
selected_attributes = config['selected_attributes']
features = config['features_to_compute']
scatter_plots_folder = config['scatter_plots_folder']

#Load the features and the attributes
df_features = pd.read_csv(filepath_or_buffer = config['features_file'])
df_attributes = pd.read_csv(filepath_or_buffer = config['attributes_file'])

#Join the dataframes 
df_complete = pd.merge(df_features, df_attributes,  
                       on = ['patient_id', 'nodule_id'],
                       how = 'inner')
df_complete.dropna(inplace = True)

#**********************************************************************
#*************** Instruct matplotlib to use LaTeX fonts ***************
#**********************************************************************
matplotlib.use('pgf')
plt.rcParams['text.latex.preamble']=[r"\usepackage{lmodern}"]
params = {'text.usetex' : True,
          'font.size' : 11,
          'font.family' : 'lmodern'}
plt.rcParams.update(params)

#Font for axis labels (not clear why it doesn't inherit from above)
font_for_axis_label = {'family' : 'lmodern'}
font_for_title = {'family' : 'lmodern', 'size' : 14}
#**********************************************************************
#**********************************************************************
#**********************************************************************

sns.set(style='whitegrid')

for attribute in selected_attributes:
    for feature in features:
        
        #Draw the scatter-plot
        x = df_complete[attribute].to_numpy()
        y = df_complete[feature].to_numpy()
        sns.regplot(x, y)
        plt.xlim(left = min(x) - 0.2, right = max(x) + 0.2)
        
        #Set the axis labels
        plt.xlabel(xlabel = attribute, fontdict = font_for_axis_label)
        plt.ylabel(ylabel = feature, fontdict = font_for_axis_label)
        plt.title(label = f'{attribute} vs. {feature}', 
                  fontdict = font_for_title)
        
        #Save the plot
        plt.savefig(f'{scatter_plots_folder}/{attribute}-{feature}.pdf')
        plt.clf()

        