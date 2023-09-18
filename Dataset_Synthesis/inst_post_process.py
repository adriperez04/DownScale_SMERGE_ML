import os
#os.environ["MODIN_ENGINE"] = "dask"
import datetime
import pandas as pd
#import modin.pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from natsort import natsorted
from sklearn.preprocessing import StandardScaler
import re
import string
import warnings
import sys

#Set data product name
d_name = input("Enter the name of the dataset(Include file extention): ")
# Set the input directory
input_dir = input("Enter the input directory: ")

# Set the output directory
output_dir = input("Enter the output directory: ")

# Read list of dates
stattion_p_file = open("station_pagenames", "r")
while not os.path.exists(stattion_p_file):
    print('The station_pagenames list txt was not found, should be in the same directory as the .py script')
    n = input("Press enter to try again")
    stattion_p_file = open("station_pagenames", "r")
stattion_p = stattion_p_file.read().split(',')

# Read list of dates
stattion_n_file = open("station_names.txt", "r")
while not os.path.exists(stattion_n_file):
    print('The station_names.txt list txt was not found, should be in the same directory as the .py script')
    n = input("Press enter to try again")
    stattion_n_file = open("station_names.txt", "r")
stattion_n = stattion_n_file.read().split(',')


try:
    data = pd.read_csv(os.path.join(input_dir, d_name)).rename({'Lai': 'LAI'}, axis='columns')
except:
    data = pd.read_csv(os.path.join(input_dir, d_name))
data['Date'] = pd.to_datetime(data['Date'], format='%m/%d/%Y')
p = len(stattion_p)
out = pd.DataFrame(
    columns=['Clay', 'Sand', 'Silt', 'Elevation', 'Ascept', 'Slope', 'LAI', 'SMERGE', 'NDVI', 'Albedo',
             'Temp', 'Date', 'ML_', 'PageName', 'Station'])
for q in range(0, p):
    inst = data[data['PageName'] == stattion_p[q]]
    inst['Station'] = stattion_n[q]
    inst.reset_index(inplace=True)

    out = pd.concat([out, inst])
out.sort_values(by=['Station', 'Date'], inplace=True)
out.drop(columns=['index'], inplace=True)
print(os.path.join(input_dir, d_name))
# os.path.join() joins directory string and name in a way that the host os can understand
# d_name.replace('.csv','inst.csv') and in the end of the filename 'inst'
out.to_csv(os.path.join(input_dir, d_name.replace('.csv','inst.csv')), index=False)

