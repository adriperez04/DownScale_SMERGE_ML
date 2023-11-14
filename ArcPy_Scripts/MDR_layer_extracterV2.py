import arcpy
import os
import pandas as pd
import re

arcpy.env.overwriteOutput = True

#Set data product name
product = input("Enter the name of the data product: ")

# Set the input directory
input_dir = input("Enter the input directory: ")

# Set the output directory
output_dir = input("Enter the output directory: ")

# Set the layer name
layer_name = input("Enter the layer name to be extracted: ")

# Read list of dates
text_file = open("dates.txt", "r")

while not os.path.exists(text_file):
    print('The date list txt was not found, should be in the same directory as the .py script')
    co = input("Press enter to try again")
date = text_file.read().split(',')

offset = input('Enter the date offset, if there is none enter 0: ')
try:
    offset = int(offset)
except:
    while offset.isnumeric():
        offset = input('Offset given was not a integer value, please trt again')
# Create a list of .hdf  files in the input directory
hdf_files = []
for d in date:
    g = 0
    date_n = pd.to_datetime(d, format="%m/%d/%Y")
    date_n = date_n + pd.DateOffset(months=1)
    year = date_n.year
    month = date_n.month
    day = date_n.day
    doy = date_n.timetuple().tm_yday
    #print(str(year) + str(doy))
    date_c = str(year) + str(doy)
    #date_c = str(year) + str(doy).zfill(2)
    print(date_c)
    for file in os.listdir(input_dir):
        if file.endswith(".hdf"):
            file_p = file.split('.')
            #print(file_p[1])
            file_p = re.sub("\D", "", file_p[1])
            date_p = pd.to_datetime(file_p, format="%Y%j")
            if date_p.year == year and (int(date_c)-offset <= int(file_p) and int(file_p) <= int(date_c)+offset):
                #print(file)
                hdf_files.append(os.path.join(input_dir, file))
                g = 1
                break;
        if g == 1:
            g = 0
            break;
i = 0
# Iterate through the list of .hdf files and perform the subset
for hdf_file in hdf_files:
    #converts the date format in to YYYYmmdd
    date_in = pd.to_datetime(date[i], format="%m/%d/%Y")
    doy_in = date_in.timetuple().tm_yday
    #joins the locat and file name
    output_file = os.path.join(output_dir, product + '_'+str(date_in.year)+str(doy_in)+'.tif')
    print(hdf_file)
    # Perform the subset
    arcpy.SubsetMultidimensionalRaster_md(hdf_file,output_file, layer_name)
    i = i + 1

print("Process complete")
