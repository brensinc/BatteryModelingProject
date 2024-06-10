import math
import numpy as np
import pandas as pd

import scipy as sp
from scipy.optimize import curve_fit
from scipy.optimize import differential_evolution
from scipy.interpolate import UnivariateSpline
import os

print("Current Working Directory:", os.getcwd())

file_path = "/Users/brendansinclair/Desktop/PersonalProjects/Code/BatteryModel/preprocessed_battery_data.csv"


plot_data = pd.read_csv(file_path)
    

# Retrieve SOC and Voltage values for training
soc_values = plot_data["SOC"]
voltage_values = plot_data["Voltage(V)"]

def get_voc_from_soc(soc, smoothness_factor = 0.15, max_voc = 4.2):
    spline_model = UnivariateSpline(soc_values, voltage_values, s = smoothness_factor)
    
    # Aligns height of the graph with different max_voc 
    # ** There might be a better way to do this
    vertical_shift = max_voc / 4.2
    return vertical_shift * float(spline_model(soc))

"""
Example
print(get_voc_from_soc(0.5))
    >>3.6700010389664106
"""