"""Export the results of the correlation analysis as LaTeX tables"""
from dataclasses import dataclass
import pandas as pd

from functions.utilities import get_config

config = get_config()

@dataclass
class CorrelationLevel:
    label: str
    bounds: tuple
    colour: tuple

#Qualitative correlation labels
correlation_levels = [CorrelationLevel(label = 'very_strong_positive', 
                                       bounds = (0.9,1.0),
                                       colour = (244,109,67)),
                      CorrelationLevel(label = 'strong_positive', 
                                       bounds = (0.7,0.9),
                                       colour = (253,176,99)),
                      CorrelationLevel(label = 'moderate_positive', 
                                       bounds = (0.4,0.7),
                                       colour = (253,188,109)),
                      CorrelationLevel(label = 'weak_positive', 
                                       bounds = (0.2,0.4),
                                       colour = (253,221,136)),
                      CorrelationLevel(label = 'negligible_positive', 
                                       bounds = (0.0,0.2),
                                       colour = (254,253,188)),
                      CorrelationLevel(label = 'negligible_negative', 
                                       bounds = (-0.2,0.0),
                                       colour = (230,245,153)),
                      CorrelationLevel(label = 'weak_negative', 
                                       bounds = (-0.4,-0.2),
                                       colour = (195,230,159)),  
                      CorrelationLevel(label = 'moderate_negative', 
                                       bounds = (-0.7,-0.4),
                                       colour = (129,204,164)),   
                      CorrelationLevel(label = 'strong_negative', 
                                       bounds = (-0.9,-0.7),
                                       colour = (95,187,167)),   
                      CorrelationLevel(label = 'very_strong_negative', 
                                       bounds = (-1.0,-0.9),
                                       colour = (72,160,178))                       
                      ]

def get_correlation_level(corr_value, correlation_levels):
    """Get the correlation level (qualitative label and colormap entry)
    for a given correlation_value
    
    Parameters
    ----------
    corr_value : float [0,1]
        The correlation value (Pearson's r or Spearman's rho)
    correlation_levels : list of CorrelationLevel
        The qualitative correlation scale.
        
    Returns
    -------
    corr_level : CorrelationLevel
        The correlation level corresponding to corr_value.
    """
    corr_level = None
    for correlation_level in correlation_levels:
        if ((correlation_level.bounds[0] < corr_value) & 
            (corr_value <= correlation_level.bounds[1])):
            corr_level = correlation_level
            break
        
    return corr_level

#Save the colourmap in LaTeX format
with open(f'{config["latex_folder"]}/cmap.tex', 'w') as fp:
    for correlation_level in correlation_levels:
        rgb_triplet = str(correlation_level.colour)
        for char in ['(',')']:
            rgb_triplet = rgb_triplet.replace(char, "")
        fp.write(f'\\definecolor{{{correlation_level.label}}}{{RGB}}{{{rgb_triplet}}}\n')
    

#Load the correlation results
df_correlation = pd.read_csv(filepath_or_buffer = config['correlation_results_file'])

modes = ['Pearson', 'Spearman']
for mode in modes:
    with open(f'{config["latex_folder"]}/{mode}.tex', 'w') as fp:
        
        #Header
        columns = 'l' + 'r' * len(config['selected_attributes'])
        fp.write(f'\\begin{{tabular}}{{{columns}}}\n')
        fp.write('\\toprule\n')
        for attribute in config['selected_attributes']:
            fp.write(f'& \\rotatebox{{90}}{{{attribute}}}')
        fp.write('\\\\\n')
        fp.write('\\midrule\n')
        
        #Body
        for feature in config['features_to_compute']:
            fp.write(f'{feature}')
            
            for attribute in config['selected_attributes']:
                slice_ = df_correlation[df_correlation['Feature'] == feature]
                slice_ = slice_[slice_['Attribute'] == attribute]
                value = slice_[mode].to_list()[0]
                
                #Get the qualitative correlation level
                corr_level = get_correlation_level(corr_value = value, 
                                                   correlation_levels = correlation_levels)
                cell_colour = corr_level.label

                
                fp.write(f'& \cellcolor{{{cell_colour}}}{value:3.2f}')
            fp.write('\\\\\n')
                
        #Footer
        fp.write('\\bottomrule\n')
        fp.write('\\end{tabular}')