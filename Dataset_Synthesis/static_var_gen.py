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

# Constructing home paths
home = input("Enter the home directory where the datasets are located: ")
# Asking for the name of the training dataset and constructing the full path
static_dataset_name = input("Enter the name of the dataset had has the static data (including file extension): ")
static_file = os.path.join(home, static_dataset_name)

# Checking if the file exists using os.path.exists and prompting the user until a valid file is provided
while not os.path.exists(static_file):
    print(static_file + " does not exist. Please enter the correct dataset name.")
    # Constructing home paths
    home = input("Enter the home directory where the datasets are located: ")
    static_dataset_name = input("Enter the name of the dataset had has the static data (including file extension): ")
    static_file = os.path.join(home, static_dataset_name)

i = ''
static_vars = ['PageName']
data = pd.read_csv(static_file)
print('These are the column names of the given table, which columsn are the statics variables, type exit when finished. The Pagename column will automaticly be add.')
print(data.columns)
while i != 'exit':
    i = input(':  ')
    if i != 'exit':
        static_vars.append(i)
# Constructing file name
name = input("Enter the name of the dataset: (NOT including file extension)")
static = data[static_vars]
static.to_csv(os.path.join(home, name + '_static.csv'), index=False)
