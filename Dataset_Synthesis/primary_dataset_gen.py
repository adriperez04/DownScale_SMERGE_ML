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

#Thsi can be automatied with a simple for loop and a lists of nessary inputs, column names and data product names may need to be
#cahnge depending on structure, this script relies on all the data tables to be in the same directory and for the data sets to be
#broken up by day


# Read list of dates
text_file = open("dates.txt", "r")

while not os.path.exists(text_file):
    print('The date list txt was not found, should be in the same directory as the .py script')
    text_file = input("Press enter to try again")
date = text_file.read().split(',')
num_dates = len(date)

def main_data_synth(name, input_dir, output_dir):
    static_home = input_dir
    file_list = []
    # This loop screens out all none .csv files
    for f in os.listdir(input_dir):
        if f.endswith(".csv"):
            file_list.append(f)
    file_list = natsorted(file_list)
    alb_file_list = []
    lai_file_list = []
    lst_file_list = []
    ndvi_file_list = []
    smerge_file_list = []
    ver_file_list = []
    # This loop sorts all file names into different categories based on the first few characters
    for w in file_list:
        if w.startswith("ALB"):
            alb_file_list.append(os.path.join(input_dir, w))
        if w.startswith("LAI"):
            lai_file_list.append(os.path.join(input_dir, w))
        if w.startswith("Prism"):
            lst_file_list.append(os.path.join(input_dir, w))
        if w.startswith("CON"):
            ndvi_file_list.append(os.path.join(input_dir, w))
        if w.startswith("Sme"):
            smerge_file_list.append(os.path.join(input_dir, w))
        if w.startswith("Ver"):
            ver_file_list.append(os.path.join(input_dir, w))

    f_data = pd.DataFrame(
        columns=['SMERGE', 'Date', 'Temp', 'LAI', 'Albedo', 'NDVI', 'Clay', 'Sand', 'Silt', 'Slope', 'Elevation',
                 'Aspect'])
    static = pd.read_csv(os.path.join(static_home, name + '_static.csv'))
    # This loop collects all the data columns associated with a date and then combines them vertically
    for k in range(1, num_dates):
        current = pd.DataFrame(index=static["PageName"],
                               columns=['SMERGE', 'Date', 'Temp', 'LAI', 'Albedo', 'NDVI', 'Clay', 'Sand', 'Silt',
                                        'Slope', 'Elevation', 'Aspect'])
        index = static["PageName"]
        current['SMERGE'] = pd.read_csv(smerge_file_list[k - 1], usecols=["MEAN", "PageName"]).set_index("PageName")
        print(lst_file_list[k - 1])
        current['Temp'] = pd.read_csv(lst_file_list[k - 1], usecols=["MEAN", "PageName"]).set_index("PageName")
        current["LAI"] = pd.read_csv(lai_file_list[k - 1], usecols=["MEAN", "PageName"]).set_index("PageName")
        current['Temp'] = pd.read_csv(lst_file_list[k - 1], usecols=["MEAN", "PageName"]).set_index("PageName")
        current["Albedo"] = pd.read_csv(alb_file_list[k - 1], usecols=["MEAN", "PageName"]).set_index("PageName")
        current["NDVI"] = pd.read_csv(ndvi_file_list[k - 1], usecols=["MEAN", "PageName"]).set_index("PageName")
        current[['Clay', 'Sand', 'Silt', 'Slope', 'Elevation', 'Aspect']] = static[
            ['Clay', 'Sand', 'Silt', 'Slope', 'Elevation', 'Aspect', 'PageName']].set_index("PageName")
        if verify == 'Y':
            current["Verifier"] = pd.read_csv(ver_file_list[k - 1], usecols=["MEAN", "PageName"]).set_index("PageName")
        current['PageName'] = current.index
        current.index = range(current.shape[0])
        current["Date"] = pd.DataFrame(date[k - 1], columns=['Date'], index=range(current.shape[0]))
        f_data = pd.concat([f_data, current])
        if k == (num_dates - 1):
            f_data.to_csv(os.path.join(output_dir, name+'_untrimmed.csv'))
            data = pd.read_csv(os.path.join(output_dir, name+'_untrimmed.csv'))
            #Dat Cleaning
            data1 = data[(data['LAI'] <= 249) & (data['Albedo'] != 32767) & (data['Aspect'] > 0)]
            data1 = data1[
                ~(data1[["LAI", "Albedo", "NDVI", "Clay", "Sand", "Silt", "Slope", "Elevation", "Aspect"]] < 0).any(axis=1)].dropna()
            data1.to_csv(os.path.join(output_dir, name+'_processed.csv'), index=False)
            train_test(data1, output_dir, name)

# Creates the training and testing dataset, depending on whether there is verification data or not.
def train_test(data, out, n):
    df_train, df_test = train_test_split(data, test_size=0.30, random_state=42)
    if verify == 'Y' and verify2 == 'N':
        v = data[data['Verifier'] != pd.NA]
        ver = v['PageName'].tolist()
        inst = df_train.loc[df_train['PageName'].isin(ver)]
        df_train = df_train.loc[~df_train['PageName'].isin(ver)]
        df_test = pd.concat([df_test, inst])
        df_train.to_csv(out, n+'_train.csv', index=False)
        df_test.to_csv(out, n+'_test.csv', index=False)



#Set data product name
d_name = input("Enter the name of the dataset: ")

# Set the input directory
input_d = input("Enter the input directory: ")

# Set the output directory
output_d = input("Enter the output directory: ")

verify = input('Do you have verification data? Y/N')
verify2 = input('Is the verification complete? Y/N')

main_data_synth(d_name, input_d, output_d)
