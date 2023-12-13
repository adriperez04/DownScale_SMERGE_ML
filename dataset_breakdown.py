import os
#os.environ["MODIN_ENGINE"] = "dask"
import datetime
import pandas as pd
#import modin.pandas as pd
import numpy as np
import re
import string
import warnings
import sys

def breakdown(output_d,input_d, d_name):
    data = pd.read_csv(os.path.join(input_d, d_name))
    col = data.columns
    home = output_d
    for c in col:
        f_data = data[['PageName', c]]
        f_data.columns = ['PageName', 'MEAN']
        if 'MEAN' in c:
            f_data.to_csv(os.path.join(home, c.replace('MEAN_', '') + '.csv'))
            #print(c)

auto = input("Do you wish to breakdown all CSVs in a directory(type Y) or individually(type N): ")

while auto != 'Y' and auto != 'N':
    auto = input("Input invalid")

# Set the input directory
input_d = input("Enter the input directory: ")

# Set the output directory
output_d = input("Enter the output directory: ")

if auto == 'N':
    # Set data product name
    d_name = input("Enter the name of the dataset(Include file extention): ")

    while not os.path.exists(os.path.join(input_d, d_name)):
        print('The dataset was not found, should be in the same directory as the .py script')
        d_name = input("Enter the name of the dataset(Include file extention): ")
        input_d = input("Enter the input directory: ")
    breakdown(output_d, input_d, d_name)

if auto == 'Y':
    reso = input('What is the resolution ID, if non leave blank and press enter: ')
    for f in os.listdir(input_d):
        if f.endswith('.csv') and reso in f:
            print(f)
            breakdown(output_d, input_d, f)



