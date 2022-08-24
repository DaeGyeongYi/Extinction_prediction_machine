# Preproceed

The folder that contains the first code to run.

The data is processed. The required columns are ['Source', 'State', 'Year', 'Species', 'Latitude', 'Longitude', 'public_positional_accuracy'].

If each column is not written correctly, it will need to be modified arbitrarily.

For example, if Year is a nan or contains a strange number, you can drop it.

After preprocessing, it is recommended that you store data frames in db or csv files.

And in this process, we're going to select the species that we're going to estimate the reduction rate(Target Species), and the species that represent the region where they're not present.(Absence)



# 1~7.ipynb

#### 1_making_test.ipynb

Creates the test set required for machine learning.

From 'Year_start' to 'Year_end', examine the distribution of the surrounding species of each data point and generate a column containing this result.

For example, the column 'labiculata_2007_18 km' records how many Anatis labiculata were in 2007 within a radius of 18 km of that data point.

There may be species with the same species name and classified by genus name. In this case, you might need to specify the column name yourself.



#### 2_scaling.ipynb

After dividing the test set based on the target Speceis, proceed with minmax scaling.

A test file named by target species is created.



#### 3_making_train.ipynb

Create a train set based on the test set.

Based on the year in which the data points were recorded, only the columns of species recorded that year are left.

ex) Anatis labiculata_18: Based on the year, how many labiculata species were recorded within a radius of 18 km of the data point.



#### 4_Model_dev.ipynb

Consider the regression results and multicollinearity to select the variables the model will use and measure its performance.

Compress the variables in high order through shap_values and measure the performance again.

#### 5_make_AOOcsv.ipynb

Generate csv files to estimate AOO.



#### 6_AOO_crawling.ipynb

Estimate AOO and generate CSV files that store yearly results



#### 7_generalization.ipynb

Since there is no 'ground truth', it is a process for indirect verification of the model.

Check the performance of testing data where you have never learned by learning only a fraction of the data set.





