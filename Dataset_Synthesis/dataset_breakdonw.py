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
input_d = input("Enter the input directory: ")

# Set the output directory
output_d = input("Enter the output directory: ")

while not os.path.exists(os.path.join(input_d, d_name)):
    print('The dataset was not found, should be in the same directory as the .py script')
    d_name = input("Enter the name of the dataset(Include file extention): ")
    input_d = input("Enter the input directory: ")

data = pd.read_csv(os.path.join(input_d, d_name))
col = data.columns
home = input_d
for c in col:
    f_data = data[['PageName', c]]
    f_data.columns = ['PageName', 'MEAN']
    if '' in c:
        f_data.to_csv(os.path.join(home, c.replace('MEAN_', '') + '.csv'))
    print(f_data)