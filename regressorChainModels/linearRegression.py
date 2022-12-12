# import libraries
import numpy as np
import pandas as pd
from collections import Counter
import glob
import statistics


# import data
# filePath = '/Users/raymond/Desktop/Capstone Project/Regression/dataset'
filePath = 'C:/flamlMultiOutput/dataset'
allFiles = glob.glob(filePath + "/*.csv")
dataFrames = []
for i in allFiles:
    df = pd.read_csv(i, index_col=None, header=0)
    dataFrames.append(df)
data = pd.concat(dataFrames)

print(data.head())

# data preprocessing
data.drop(["No"], axis = 1, inplace = True)
data.rename(columns = {'year': 'Year',
                       'month': 'Month',
                       'day': "Day",
                       'hour': 'Hour',
                       'pm2.5': 'PM2.5',
                       'DEWP': 'DewP',
                       'TEMP': 'Temp',
                       'PRES': 'Press',
                       'RAIN': 'Rain',
                       'wd': 'WinDir',
                       'WSPM': 'WinSpeed',
                       'station': 'Station'}, inplace = True)
print(data.isnull().sum())

# fill the null values with average value
unique_Month = pd.unique(data.Month)

# find PM2_5 averages in Month specific
# Equalize the average PM2.5 values to the missing values in PM2_5 specific to Month
temp_data = data.copy()  # set temp_data variable to avoid losing real data
columns = ["PM2.5", 'PM10', 'SO2', 'NO2', 'CO', 'O3', 'Temp', 'Press', 'DewP', 'Rain', 'WinSpeed'] # it can be add more column
for c in unique_Month:
    
    # create Month filter
    Month_filtre = temp_data.Month == c
    # filter data by Month
    fitered_data = temp_data[Month_filtre]
    
    # find average for values in specific to Month
    for s in columns:
        mean = np.round(np.mean(fitered_data[s]), 2)
        if ~np.isnan(mean): # if there if average specific to Month
            fitered_data[s] = fitered_data[s].fillna(mean)
            print(f"Missing Value in {s} column fill with {mean} when Month:{c}")
        else: # find average for all data if no average in specific to Month
            all_data_mean = np.round(np.mean(data[s]),2)
            fitered_data[s] = fitered_data[s].fillna(all_data_mean)
            print(f"Missing Value in {s} column fill with {all_data_mean}")
    # Synchronize data filled with missing values in PM2.5 to data temporary            
    temp_data[Month_filtre] = fitered_data

# equate the deprecated temporary data to the real data variable
data = temp_data.copy() 
print(data.isnull().sum())

unique_Station = pd.unique(data.Station)

# find columns mode value in WinDir column according to Station column specific
# Equalize the mode values of columns to the missing values
temp_data = data.copy()  # set temp_data variable to avoid losing real data
columns = ["WinDir"] # it can be add more column
for c in unique_Station:
    
    # create Station filter
    Station_filtre = temp_data.Station == c
    
    # filter data by Station
    filtered_data = temp_data[Station_filtre]
    
    # find mode for WinDir specific to Station
    for column in columns:
        mode = statistics.mode(filtered_data[column])
        filtered_data[column] = filtered_data[column].fillna(mode)
        print(f"Missing Value in {column} column fill with {mode} when Station:{c}")

    # Synchronize data filled with missing values in WinDir to data temporary            
    temp_data[Station_filtre] = filtered_data

# equate the deprecated temporary data to the real data variable
data = temp_data.copy() 
print(data.isnull().sum())

# creating date field for further analysis by extracting day of the week, month etc.
data['Date']=pd.to_datetime(data[['Year', 'Month', 'Day']])
data.tail()

# function to find day of the week based on the date field
import calendar
def findDay(date): 
    dayname = calendar.day_name[date.weekday()]
    return dayname

data['DayNames'] = data['Date'].apply(lambda x: findDay(x))
print(data.head())

# preprocessing for training the model
from sklearn.preprocessing import LabelEncoder
# define a function for label encoding
def labelEncoder(labelColumn):
    labelValues = labelColumn
    unique_labels = labelColumn.unique()
    le = LabelEncoder()
    labelColumn = le.fit_transform(labelColumn)
    print('Encoding Approach:')
    for i, j in zip(unique_labels, labelColumn[np.sort(np.unique(labelColumn, return_index=True)[1])]): 
        print(f'{i}  ==>  {j}')
    return labelColumn

categorical_variables = ["WinDir", "Station"]
for i in categorical_variables:
    print(f"For {i} column ")
    data[f"{i}"] = labelEncoder(data[f"{i}"])
    print("**********************************")


# create input and output
data.drop(["DayNames", "Date", "Year", "Month", "Day", "Hour"], axis=1, inplace=True)
y = data[['PM2.5', 'PM10', 'SO2', 'NO2']]
X = data.drop(['PM2.5', 'PM10', 'SO2', 'NO2'], axis = 1)

from sklearn.linear_model import LinearRegression
from sklearn.multioutput import RegressorChain
from sklearn import preprocessing

# y = preprocessing.normalize(y)
# X = preprocessing.normalize(X)

# split the train test data
from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state=128)

from sklearn.metrics import mean_absolute_error, r2_score, mean_squared_error

#Train the Models

# Multi-Output Models
# LinearRegression
reg = LinearRegression()
ChainRegression = RegressorChain(reg)
ChainRegression.fit(X_train, y_train)
pred = ChainRegression.predict(X_test)
mae_score = mean_absolute_error(y_test, pred)
rmse_score = np.sqrt(mean_squared_error(y_test, pred))
print(mae_score, rmse_score)



y_pred1 = pred[:,0]
y_pred2 = pred[:,1]
y_pred3 = pred[:,2]
y_pred4 = pred[:,3]

y_test1 = y_test['PM2.5']
y_test2 = y_test['PM10']
y_test3 = y_test['SO2']
y_test4 = y_test['NO2']


mae_score1 = mean_absolute_error(y_test1, y_pred1)
mae_score2 = mean_absolute_error(y_test2, y_pred2)
mae_score3 = mean_absolute_error(y_test3, y_pred3)
mae_score4 = mean_absolute_error(y_test4, y_pred4)

mse_score1 = mean_squared_error(y_test1, y_pred1)
mse_score2 = mean_squared_error(y_test2, y_pred2)
mse_score3 = mean_squared_error(y_test3, y_pred3)
mse_score4 = mean_squared_error(y_test4, y_pred4)

r2_score1 = r2_score(y_test1, y_pred1)
r2_score2 = r2_score(y_test2, y_pred2)
r2_score3 = r2_score(y_test3, y_pred3)
r2_score4 = r2_score(y_test4, y_pred4)


print(f'Evaluation on test data PM2.5: MAE: {mae_score1}, MSE: {mse_score1}, R2: {r2_score1}')
print(f'Evaluation on test data PM10: MAE: {mae_score2}, MSE: {mse_score2}, R2: {r2_score2}')
print(f'Evaluation on test data SO2: MAE: {mae_score3}, MSE: {mse_score3}, R2: {r2_score3}')
print(f'Evaluation on test data NO2: MAE: {mae_score4}, MSE: {mse_score4}, R2: {r2_score4}')