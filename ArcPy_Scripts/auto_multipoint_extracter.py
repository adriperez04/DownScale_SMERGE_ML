import arcpy
from arcpy import env
import re
import pandas  as pd
from arcpy.sa import *
import os

# Define the parent folder and the geodatabase name
parent_folder = os.path.dirname(__file__)
geodatabase_name = "example.gdb"

# Create the file geodatabase
geodatabase_path = os.path.join(parent_folder, geodatabase_name)
#arcpy.CreateFileGDB_management(parent_folder, geodatabase_name)

# Set the geodatabase as the workspace
arcpy.env.workspace = geodatabase_path
# Set up the environment
arcpy.env.parallelProcessingFactor = 0
arcpy.CheckOutExtension("Spatial")
arcpy.env.matchMultidimensionalVariable = False
arcpy.env.overwriteOutput = True


#Set data product name
product = input("Enter the name of the data product: ")

# Set the input directory
input_dir = input("Enter the input directory: ")

# Set the output directory
output_dir = input("Enter the output directory: ")

# Read list of dates
text_file = open("dates.txt", "r")

while not os.path.exists(text_file):
    print('The date list txt was not found, should be in the same directory as the .py script')
    n = input("Press enter to try again")
    text_file = open("dates.txt", "r")
date = text_file.read().split(',')

grid_shape_file = input("Enter the full file path and name of the grid shape file: ")

while not os.path.exists(grid_shape_file):
    print('The shapefile was not found, should be in the same directory as the .py script')
    co = input("Please try again: ")

point_shape_file = input("Enter the full file path and name of the point shape file, that you wish to generate: ")
point_check = input("Enter Y if you are add to an existing point shape file, if you creating/overwrite a new point file enter N")

while not point_check != 'Y' and point_check != 'N':
    point_shape_file = input("Please try again: ")


if point_check == 'Y':
    while not os.path.exists(point_shape_file):
        print('The shapefile was not found, should be in the same directory as the .py script')
        point_shape_file = input("Please try again: ")

thirty_grids = grid_shape_file
thirty_points = point_shape_file

if point_check == 'N':
    arcpy.management.FeatureToPoint(thirty_grids, thirty_points, "CENTROID")



def raster_points(input_raster, output_raster):
    # Read the input and check rasters
    in_raster = Raster(input_raster)
    ExtractMultiValuesToPoints(thirty_points, [[in_raster, output_raster]])

i = 0
for d in date:
    j = False
    date_n = pd.to_datetime(d, format="%m/%d/%Y") + pd.DateOffset(months=1)
    year = date_n.year
    month = date_n.month
    day = date_n.day
    doy = date_n.timetuple().tm_yday
    for f in os.listdir(input_dir):
        if j == True:
            break
        #try and except is ment to account for the different MDR_layer_extractors
        try:# MDR_layer_extractorV1 complient
            file_p = f.split('.')
            date_c = str(year) + str(doy).zfill(3)
            file_p = re.sub("\D", "", file_p[1])
            date_p = pd.to_datetime(file_p, format="%Y%j")
        except: # MDR_layer_extractorV2 complient
            file_p = f.split('.')
            date_c = str(year) + str(doy).zfill(3)
            file_p = re.sub("\D", "", file_p[0])
            date_p = pd.to_datetime(file_p, format="%Y%j")

        #print(date_c)
        if f.endswith(".tif") and date_p.year == year and (int(date_c)-4 <= int(file_p) and int(file_p) <= int(date_c)+4):
            input_raster = os.path.join(input_dir, f)
            #Has to by date index number, because the arcpy multiopoint function has a name lenght limit
            data_name = product+"_"+ str(i).zfill(3)
            print(data_name + " " + date_c)
            output_raster = data_name
            raster_points(input_raster, output_raster)
            j = True
    i = i + 1