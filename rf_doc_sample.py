# Importing necessary libraries
import os
import subprocess
import pandas as pd
import numpy as np
import xarray as xr
import tensorflow as tf
from contextlib import redirect_stdout
import datetime
import matplotlib.pyplot as plt
import seaborn as sns
import tensorflow_decision_forests as forest
from tensorflow.python.client import device_lib

# Setting environment variables for TensorFlow configuration
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
os.environ['CUDA_VISIBLE_DEVICES'] = '0'

# Setting display options for pandas
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

# Checking available devices (useful for confirming GPU usage)
print(device_lib.list_local_devices())

# Defining a function to plot variable importances for TensorFlow Decision Forests
def plot_tfdf_importances(inspector: forest.inspector.AbstractInspector, importance_type: str, name: str):
    scoredate = pd.DataFrame(columns=['name', 'scores'])
    try:
        importances = inspector.variable_importances()[importance_type]
    except KeyError:
        raise ValueError(f"Unknown importance type: {importance_type}")

    # Setting the labels for the variable importance plot
    plt.xlabel(importance_type)
    plt.title("Variable Importance")
    scoredate['name'] = names
    scoredate['scores'] = scores

    # Saving the variable importance data and plot
    scoredate.to_csv(name.replace('.png', '.csv'), index=False)
    plt.savefig(name)
    plt.show()

# Configuring the task type for the decision forest
task = forest.keras.Task.REGRESSION


# Asking the user for the resolution of the dataset
resolution = [input("Enter the resolution of the dataset: ")]

# Constructing paths based on zone and resolution
home_directory = input("Enter the home directory where the datasets are located: ")

# Asking for the name of the training dataset and constructing the full path
train_dataset_name = input("Enter the name of the training dataset (including file extension): ")
train_file = os.path.join(home_directory, train_dataset_name)

# Checking if the training file exists and prompting the user until a valid file is provided
while not os.path.exists(train_file):
    print("The specified training file does not exist. Please enter the correct dataset name.")
    train_dataset_name = input("Enter the name of the training dataset (including file extension): ")
    train_file = os.path.join(home_directory, train_dataset_name)

# Asking for the name of the testing dataset and constructing the full path
test_dataset_name = input("Enter the name of the testing dataset (including file extension): ")
test_file = os.path.join(home_directory, test_dataset_name)

# Checking if the testing file exists and prompting the user until a valid file is provided
while not os.path.exists(test_file):
    print("The specified testing file does not exist. Please enter the correct dataset name.")
    test_dataset_name = input("Enter the name of the testing dataset (including file extension): ")
    test_file = os.path.join(home_directory, test_dataset_name)
# Defining columns for training, testing, and exporting data
var1 = ['Clay', 'Sand', 'Silt', 'Elevation', 'Aspect', 'Slope', 'Lai', 'SMERGE', 'NDVI', 'Albedo', 'Temp',"Date"]  # training vars
var2 = ['Clay', 'Sand', 'Silt', 'Elevation', 'Aspect', 'Slope', 'Lai', 'NDVI', 'Albedo', 'Temp',"Date"]  # testing vars
var3 = ['Clay', 'Sand', 'Silt', 'Elevation', 'Aspect', 'Slope', 'Lai', 'SMERGE', 'NDVI', 'Albedo', 'Temp',"Date"]  # vars for export csv

# Reading training data
train_data = pd.read_csv(train_file,
                         usecols=['SMERGE', 'Date', 'Temp', 'PageName', 'LAI', 'Albedo', 'NDVI', 'Clay', 'Sand', 'Silt',
                                  'Slope', 'Elevation', 'Ascept'])
train_data = train_data[
    ['Clay', 'Sand', 'Silt', 'Elevation', 'Ascept', 'Slope', 'NDVI', 'SMERGE', 'Date', 'LAI', 'Albedo', 'Temp']]
print(train_data)

# Reading test data
test_data = pd.read_csv(test_file,
                        usecols=['SMERGE', 'Date', 'Temp', 'PageName', 'LAI', 'Albedo', 'NDVI', 'Clay', 'Sand', 'Silt',
                                 'Slope', 'Elevation', 'Ascept'])
test_page = test_data[['PageName']]
ndvi = test_data['NDVI']
dates = test_data['Date']
test_data.drop(['PageName'], axis=1)
test_data = test_data[
    ['Clay', 'Sand', 'Silt', 'Elevation', 'Ascept', 'Slope', 'NDVI', 'SMERGE', 'Date', 'LAI', 'Albedo', 'Temp']]
print(test_data)
# Defining columns for scaling
scale_columns = ['Clay', 'Sand', 'Silt', 'Elevation', 'Ascept', 'Slope', 'NDVI', 'SMERGE']

# Configuration for the model training
t = 1100
k = 15
tuner = forest.tuner.RandomSearch(num_trials=9 * k, use_predefined_hps=True)
model_img_file = resolution + "model.png"
n = test_data.shape[0]

# Initializing output array
out = np.empty(shape=(0, 1))

# Creating an empty DataFrame with specific columns
x = pd.DataFrame(columns=var3)

# Configuring the random forest model
model = forest.keras.RandomForestModel(
        verbose=1, tuner=tuner, num_trees=t, allow_na_conditions=True, task=task, winner_take_all=True,
        categorical_algorithm='CART', honest=True, honest_fixed_separation=True,
        honest_ratio_leaf_examples=0.75, bootstrap_size_ratio=1.05,
        adapt_bootstrap_size_ratio_for_maximum_training_duration=True,
        keep_non_leaf_label_distribution=False, num_threads=12, max_depth=9)

# Processing 'Date' column for training
train_data['Date'] = pd.to_datetime(train_data['Date'], format="%m/%d/%Y").astype(int)

# Creating a TensorFlow dataset for training
train_ds = forest.keras.pd_dataframe_to_tf_dataset(train_data[var1], label='SMERGE', task=task)

# Compiling and training the model
model.compile(metrics=["mae"])
model.fit(train_ds)
# Creating a TensorFlow dataset for testing
test_data['Date'] = pd.to_datetime(test_data['Date'], format="%m/%d/%Y").astype(int)
test_data1 = test_data
test_ds = forest.keras.pd_dataframe_to_tf_dataset(test_data1[var2], task=task)

# Extracting relevant data for output processing
out_data = test_data1[var3]

# Predicting with the trained model
hope = model.predict(test_ds, verbose=1)
h = hope
out = np.vstack([out, h])
x = pd.concat([x, out_data])

# Writing the model summary to a text file
with open(resolution + "sum_model.txt", "w") as txt_file:
    with redirect_stdout(txt_file):
        model.summary()

# Saving the model plot to an HTML file
with open(resolution + "model.html", "w") as html_file:
    html_file.write(forest.model_plotter.plot_model(model, tree_idx=0, max_depth=10))

# Resetting the model states (if any)
model.reset_states()

# Preparing the output dataframe
x['ML_'] = out
df_out = pd.DataFrame(h, columns=['ML_'])
x['NDVI'] = ndvi
x['Date'] = dates
x['PageName'] = test_page

# Saving the output dataframe to a CSV file
x.to_csv(resolution + ".csv", index=False)

# Generating variable importance plots
inspector = model.make_inspector()
plot_tfdf_importances(inspector=inspector, importance_type='INV_MEAN_MIN_DEPTH', name=resolution + "_IMMD.png")
plot_tfdf_importances(inspector=inspector, importance_type='NUM_NODES', name=resolution + "_NumNodes.png")



# Running another script at the end of the current script
subprocess.run(["python", "Era3_1400.py"])

