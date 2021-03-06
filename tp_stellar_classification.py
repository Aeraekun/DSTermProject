# -*- coding: utf-8 -*-
"""TP_Stellar_edited4.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1Nii7Tg1yITq1VzYhLVRWc3dDMmSge2Er

# DataScience Term Project 
> ## Team 8
> ## Stellar Classification Dataset - SDSS17

## Abstract

> - In astronomy, the classification of stars is the classification of stars according to their spectral properties.

> - The early classification and distribution of stars in the sky made it clear that they made up our galaxy. As Andromeda was a separate galaxy from our own, more powerful telescopes were created, and numerous galaxies began to be investigated.
"""

from google.colab import drive
drive.mount('/content/drive')

# import libraries
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import warnings 
from sklearn.preprocessing import LabelEncoder

warnings.filterwarnings('ignore')

# read data
df = pd.read_csv('/content/drive/Shareddrives/Data_Science_Term_Project/star_classification.csv')

# print data columns
df.columns

#print head of the data
df.head()

df.info()

df.describe()

# print data shape
df.shape

# print data index
df.index

df['class'].unique()

"""## Step 1. Data Preprocessing

- Encoding Object value into numeric value
- Feature selection
- Outliers detection 
- Null/Unusable value detection

### Encoding non-numerical value, using LabelEncoder

- Due to feature 'Class' is an object data, make ir numerical value using LabelEncoder()
"""

# Encoding categorical data
le = LabelEncoder()
df['class'] = le.fit_transform(df['class'])
df['class'] = df['class'].astype(int)

df['class'].unique()

"""### Outlier detection & processing using scipy

- Show outlier examples. 
- There are outlier which value = -9999. 
"""

plt.boxplot(df['u'])

"""- Remove an outlier by using LocalOutlierFactor function"""

# Detect outlier
from sklearn.neighbors import LocalOutlierFactor
clf = LocalOutlierFactor()
y_pred = clf.fit_predict(df) 

x_score = clf.negative_outlier_factor_
outlier_score = pd.DataFrame()
outlier_score["score"] = x_score

# threshold
threshold2 = -1.5                                            
filtre2 = outlier_score["score"] < threshold2
outlier_index = outlier_score[filtre2].index.tolist()

df.drop(outlier_index, inplace=True)

"""- Check again if outlier has successfully detected and deleted"""

plt.boxplot(df['u'])

"""### Null value detection & processing"""

# Check Nan value
df.isnull().sum()

# Print data information
df.info()

# Print data description
df.describe().T

"""### Feature selection 

- After plotting each feature, select which feature to use for data analysis.
- By checking each of correlation matrix, we can check feature that which featuer has high-correlation with 'class' feature
"""

f,ax = plt.subplots(figsize=(12,8))
sns.heatmap(df.corr(), cmap="PuBu", annot=True, linewidths=0.5, fmt= '.2f',ax=ax)
plt.show()

"""- Make it numerical value
- > we can find feature that which has high correlation with 'class'
"""

corr = df.corr()
corr['class'].sort_values()

# Define function to print plot
def plot(column):
    for i in range(3):
        sns.kdeplot(data=df[df["class"] == i][column], label = le.inverse_transform([i]))
    sns.kdeplot(data=df[column],label = ["All"])
    plt.legend()
  
# Define function to print log scale plot
def log_plot(column):
    for i in range(3):
        sns.kdeplot(data=np.log(df[df["class"] == i][column]), label = le.inverse_transform([i]))
    sns.kdeplot(data=np.log(df[column]),label = ["All"])
    plt.legend();

plot('alpha')

plot('delta')

plot('r')

plot('i')

log_plot('u')

log_plot('g')

log_plot('z')

log_plot('spec_obj_ID')

log_plot('redshift')

plot('plate')

plot('MJD')

"""- `From above graph, we can select features for training as [alpha, delta, r, i, u, g, z]`"""

# class for y
df = df.drop(['obj_ID','run_ID','rerun_ID','cam_col','field_ID','fiber_ID'], axis = 1)
df = df.reset_index().drop(['index'], axis = 1)
df

"""## Data Scaling / Normalization

## Data scaling - Standard
"""

dfClean_y = df['class']

dfClean_x = df.drop(['class'], axis = 1)

from sklearn.preprocessing import StandardScaler

# Standard Scaling the data
s = StandardScaler()
dfClean_xSScaled = s.fit_transform(dfClean_x)
dfClean_xSScaled = pd.DataFrame(dfClean_xSScaled, columns = ['alpha', 'delta', 'r', 'i', 'u', 'g', 'z','spec_obj_ID','redshift','plate','MJD'])

# Show difference between befor scaling & after standard scaling
fig,(ax1,ax2) = plt.subplots(ncols = 2, figsize = (10,5))
ax1.set_title('Before scaling')
sns.kdeplot(df['alpha'],ax = ax1)
sns.kdeplot(df['delta'],ax = ax1)
sns.kdeplot(df['r'],ax = ax1)
sns.kdeplot(df['i'],ax = ax1)
sns.kdeplot(df['u'],ax = ax1)
sns.kdeplot(df['g'],ax = ax1)
sns.kdeplot(df['z'],ax = ax1)
sns.kdeplot(df['spec_obj_ID'],ax = ax1)
sns.kdeplot(df['redshift'],ax = ax1)
sns.kdeplot(df['plate'],ax = ax1)
sns.kdeplot(df['MJD'],ax = ax1)
ax2.set_title('Standard scaling')
sns.kdeplot(dfClean_xSScaled['alpha'],ax = ax2)
sns.kdeplot(dfClean_xSScaled['delta'],ax = ax2)
sns.kdeplot(dfClean_xSScaled['r'],ax = ax2)
sns.kdeplot(dfClean_xSScaled['i'],ax = ax2)
sns.kdeplot(dfClean_xSScaled['u'],ax = ax2)
sns.kdeplot(dfClean_xSScaled['g'],ax = ax2)
sns.kdeplot(dfClean_xSScaled['z'],ax = ax2)
sns.kdeplot(dfClean_xSScaled['spec_obj_ID'],ax = ax2)
sns.kdeplot(dfClean_xSScaled['redshift'],ax = ax2)
sns.kdeplot(dfClean_xSScaled['plate'],ax = ax2)
sns.kdeplot(dfClean_xSScaled['MJD'],ax = ax2)
plt.show()

"""## Data Scaling - MinMax"""

from sklearn.preprocessing import MinMaxScaler

# MinMax Scaling the data
m = MinMaxScaler()
dfClean_xMScaled = m.fit_transform(dfClean_x)
dfClean_xMScaled = pd.DataFrame(dfClean_xMScaled, columns = ['alpha', 'delta', 'r', 'i', 'u', 'g', 'z','spec_obj_ID','redshift','plate','MJD'])

# Show difference between befor scaling & after minmax scaling
fig,(ax1,ax2) = plt.subplots(ncols = 2, figsize = (10,5))
ax1.set_title('Before scaling')
sns.kdeplot(df['alpha'],ax = ax1)
sns.kdeplot(df['delta'],ax = ax1)
sns.kdeplot(df['r'],ax = ax1)
sns.kdeplot(df['i'],ax = ax1)
sns.kdeplot(df['u'],ax = ax1)
sns.kdeplot(df['g'],ax = ax1)
sns.kdeplot(df['z'],ax = ax1)
sns.kdeplot(df['spec_obj_ID'],ax = ax1)
sns.kdeplot(df['redshift'],ax = ax1)
sns.kdeplot(df['plate'],ax = ax1)
sns.kdeplot(df['MJD'],ax = ax1)
ax2.set_title('MinMax scaling')
sns.kdeplot(dfClean_xMScaled['alpha'],ax = ax2)
sns.kdeplot(dfClean_xMScaled['delta'],ax = ax2)
sns.kdeplot(dfClean_xMScaled['r'],ax = ax2)
sns.kdeplot(dfClean_xMScaled['i'],ax = ax2)
sns.kdeplot(dfClean_xMScaled['u'],ax = ax2)
sns.kdeplot(dfClean_xMScaled['g'],ax = ax2)
sns.kdeplot(dfClean_xMScaled['z'],ax = ax2)
sns.kdeplot(dfClean_xMScaled['spec_obj_ID'],ax = ax2)
sns.kdeplot(dfClean_xMScaled['redshift'],ax = ax2)
sns.kdeplot(dfClean_xMScaled['plate'],ax = ax2)
sns.kdeplot(dfClean_xMScaled['MJD'],ax = ax2)
plt.show()

"""## Data Scaling - Robust"""

from sklearn.preprocessing import RobustScaler

#Robust Scaling the data
r = RobustScaler()
dfClean_xRScaled = r.fit_transform(dfClean_x)
dfClean_xRScaled = pd.DataFrame(dfClean_xRScaled, columns = ['alpha', 'delta', 'r', 'i', 'u', 'g', 'z','spec_obj_ID','redshift','plate','MJD'])

# Show difference between befor scaling & after robust scaling
fig,(ax1,ax2) = plt.subplots(ncols = 2, figsize = (10,5))
ax1.set_title('Before scaling')
sns.kdeplot(df['alpha'],ax = ax1)
sns.kdeplot(df['delta'],ax = ax1)
sns.kdeplot(df['r'],ax = ax1)
sns.kdeplot(df['i'],ax = ax1)
sns.kdeplot(df['u'],ax = ax1)
sns.kdeplot(df['g'],ax = ax1)
sns.kdeplot(df['z'],ax = ax1)
sns.kdeplot(df['spec_obj_ID'],ax = ax1)
sns.kdeplot(df['redshift'],ax = ax1)
sns.kdeplot(df['plate'],ax = ax1)
sns.kdeplot(df['MJD'],ax = ax1)
ax2.set_title('Robust scaling')
sns.kdeplot(dfClean_xRScaled['alpha'],ax = ax2)
sns.kdeplot(dfClean_xRScaled['delta'],ax = ax2)
sns.kdeplot(dfClean_xRScaled['r'],ax = ax2)
sns.kdeplot(dfClean_xRScaled['i'],ax = ax2)
sns.kdeplot(dfClean_xRScaled['u'],ax = ax2)
sns.kdeplot(dfClean_xRScaled['g'],ax = ax2)
sns.kdeplot(dfClean_xRScaled['z'],ax = ax2)
sns.kdeplot(dfClean_xRScaled['spec_obj_ID'],ax = ax2)
sns.kdeplot(dfClean_xRScaled['redshift'],ax = ax2)
sns.kdeplot(dfClean_xRScaled['plate'],ax = ax2)
sns.kdeplot(dfClean_xRScaled['MJD'],ax = ax2)
plt.show()

"""## Select Scaling Method - Standard Scaling"""

#Select Standard Scaling
xNorm = pd.DataFrame(dfClean_xSScaled)
xNorm.columns = dfClean_x.columns

"""## dfNorm: dataFrame with final preprocessing is completed"""

dfNorm = pd.concat([xNorm, dfClean_y], axis = 1) 

dfNorm

dfNorm.describe().T

y = dfNorm['class']
X = dfNorm.drop(['class'], axis = 1)

"""## Separate Train and Test set using"""

from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, shuffle = True, stratify = y, random_state = 34)

"""## Linear regression -  Fit"""

from sklearn.model_selection import KFold
from sklearn.model_selection import cross_val_score
from sklearn.linear_model import LinearRegression

linreg = LinearRegression()
linreg.fit(X_train, y_train)

"""## Linear regression - Evaluation"""

for n in [3, 5]:
    kfold = KFold(n_splits = n, random_state = 0, shuffle = True)
    
    # Scoring each sets
    scores = cross_val_score(linreg, X_test, y_test, cv=kfold)
    print('n_splits={}, cross validation score: {}'.format(n, scores))

"""## Decision tree classifier"""

from sklearn.model_selection import GridSearchCV
from sklearn.tree import DecisionTreeClassifier

for n in [3,5]:
  dtc = DecisionTreeClassifier()
  kfold = KFold(n_splits = n, random_state = 0, shuffle = True)
  param_grid = {
              'max_depth': [None, 2, 3, 4, 5, 6, 7, 8, 9, 10],
  }
  gdtc=GridSearchCV(dtc,param_grid=param_grid,cv=kfold,n_jobs=-1)
  gdtc.fit(X_train, y_train)
  print('n_splits: ',n)
  print('best parameter: ',gdtc.best_params_)
  print('cross validation score: ',gdtc.score(X_test, y_test))

"""## Decision tree classifier - Confusion Matrix"""

from sklearn.metrics import confusion_matrix, plot_confusion_matrix

label=['GALAXY','STAR','QSO']
plot = plot_confusion_matrix(gdtc, 
                             X_test, y_test, 
                             display_labels=label, 
                             cmap=plt.cm.Blues, 
                             normalize='true') 
plot.ax_.set_title('Decision tree classifier')

"""## K-Neighbors classifier"""

from sklearn.neighbors import KNeighborsClassifier

for n in [3,5]:
  knn = KNeighborsClassifier()
  kfold = KFold(n_splits = n, random_state = 0, shuffle = True)
  param_grid = {
              'n_neighbors': [None, 2, 3, 4, 5, 6],
  }
  gknn=GridSearchCV(knn,param_grid=param_grid,cv=kfold,n_jobs=-1)
  gknn.fit(X_train, y_train)
  print('n_splits: ',n)
  print('best parameter: ',gknn.best_params_)
  print('cross validation score: ',gknn.score(X_test, y_test))

"""## K-Neighbors classifier - Confusion Matrix"""

from sklearn.metrics import confusion_matrix, plot_confusion_matrix

label=['GALAXY','STAR','QSO']
plot = plot_confusion_matrix(gknn,
                             X_test, y_test,
                             display_labels=label,
                             cmap=plt.cm.Blues,
                             normalize='true') 
plot.ax_.set_title('K-Neighbors classifier')

"""## Random forest classifier"""

from sklearn.ensemble import RandomForestClassifier

for n in [3,5]:
  rf = RandomForestClassifier()
  kfold = KFold(n_splits = n, random_state = 0, shuffle = True)
  param_grid = {
              "n_estimators": [10,100,200],
              "criterion": ["entropy"],
              "max_depth": [None, 2, 3, 4, 5],
  }
  grf=GridSearchCV(rf,param_grid=param_grid,cv=kfold,n_jobs=-1)
  grf.fit(X_train, y_train)
  print('n_splits: ',n)
  print('best parameter: ',grf.best_params_)
  print('cross validation score: ',grf.score(X_test, y_test))

"""## Random forest classifier - Classification"""

from sklearn.metrics import confusion_matrix, plot_confusion_matrix

label=['GALAXY','STAR','QSO']
plot = plot_confusion_matrix(grf,
                             X_test, y_test,
                             display_labels=label,
                             cmap=plt.cm.Blues,
                             normalize='true') 
plot.ax_.set_title('Random forest classifier')

"""## Bagging classifier"""

from sklearn.ensemble import BaggingClassifier

for n in [3,5]:
  bg = BaggingClassifier()
  kfold = KFold(n_splits = n, random_state = 0, shuffle = True)
  param_grid = {
              'n_estimators': [10, 50, 100],
              'max_samples': [1, 5, 10],
              'max_features': [1, 5, 10]
  }
  gbg=GridSearchCV(bg,param_grid=param_grid,cv=kfold,n_jobs=-1)
  gbg.fit(X_train, y_train)
  print('n_splits: ',n)
  print('best parameter: ',gbg.best_params_)
  print('cross validation score: ',gbg.score(X_test, y_test))

"""## Bagging classifier - Confusion Matrix"""

label=['GALAXY','STAR','QSO']
plot = plot_confusion_matrix(gbg,
                             X_test, y_test,
                             display_labels=label,
                             cmap=plt.cm.Blues,
                             normalize='true') 
plot.ax_.set_title('Random forest classifier')

"""## Adaboost classifier"""

from sklearn.ensemble import AdaBoostClassifier

for n in [3,5]:
  ad = AdaBoostClassifier()
  kfold = KFold(n_splits = n, random_state = 0, shuffle = True)
  param_grid = {
              'n_estimators': [25, 50, 100, 200],
              'learning_rate': [0.01, 0.1, 1.0]
  }
  gad=GridSearchCV(ad,param_grid=param_grid,cv=kfold,n_jobs=-1)
  gad.fit(X_train, y_train)
  print('n_splits: ',n)
  print('best parameter: ',gad.best_params_)
  print('cross validation score: ',gad.score(X_test, y_test))

"""## Adaboost classifier - Confusion Matrix"""

label=['GALAXY','STAR','QSO']
plot = plot_confusion_matrix(gad,
                             X_test, y_test,
                             display_labels=label,
                             cmap=plt.cm.Blues,
                             normalize='true') 
plot.ax_.set_title('Random forest classifier')

"""## Select Scaling Method - MinMax Scaling"""

#Select MinMax Scaling
xNorm = pd.DataFrame(dfClean_xMScaled)
xNorm.columns = dfClean_x.columns

"""## dfNorm: dataFrame with final preprocessing is completed"""

dfNorm = pd.concat([xNorm, dfClean_y], axis = 1) 

dfNorm

dfNorm.describe().T

y = dfNorm['class']
X = dfNorm.drop(['class'], axis = 1)

"""## Separate Train and Test set using"""

from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, shuffle = True, stratify = y, random_state = 34)

"""## Linear regression -  Fit"""

from sklearn.model_selection import KFold
from sklearn.model_selection import cross_val_score
from sklearn.linear_model import LinearRegression

linreg = LinearRegression()
linreg.fit(X_train, y_train)

"""## Linear regression - Evaluation"""

for n in [3, 5]:
    kfold = KFold(n_splits = n, random_state = 0, shuffle = True)
    
    # Scoring each sets
    scores = cross_val_score(linreg, X_test, y_test, cv=kfold)
    print('n_splits={}, cross validation score: {}'.format(n, scores))

"""## Decision tree classifier"""

from sklearn.model_selection import GridSearchCV
from sklearn.tree import DecisionTreeClassifier

for n in [3,5]:
  dtc = DecisionTreeClassifier()
  kfold = KFold(n_splits = n, random_state = 0, shuffle = True)
  param_grid = {
              'max_depth': [None, 2, 3, 4, 5, 6, 7, 8, 9, 10],
  }
  gdtc=GridSearchCV(dtc,param_grid=param_grid,cv=kfold,n_jobs=-1)
  gdtc.fit(X_train, y_train)
  print('n_splits: ',n)
  print('best parameter: ',gdtc.best_params_)
  print('cross validation score: ',gdtc.score(X_test, y_test))

"""## Decision tree classifier - Confusion Matrix"""

from sklearn.metrics import confusion_matrix, plot_confusion_matrix

label=['GALAXY','STAR','QSO']
plot = plot_confusion_matrix(gdtc, 
                             X_test, y_test, 
                             display_labels=label, 
                             cmap=plt.cm.Blues, 
                             normalize='true') 
plot.ax_.set_title('Decision tree classifier')

"""## K-Neighbors classifier"""

from sklearn.neighbors import KNeighborsClassifier

for n in [3,5]:
  knn = KNeighborsClassifier()
  kfold = KFold(n_splits = n, random_state = 0, shuffle = True)
  param_grid = {
              'n_neighbors': [None, 2, 3, 4, 5, 6],
  }
  gknn=GridSearchCV(knn,param_grid=param_grid,cv=kfold,n_jobs=-1)
  gknn.fit(X_train, y_train)
  print('n_splits: ',n)
  print('best parameter: ',gknn.best_params_)
  print('cross validation score: ',gknn.score(X_test, y_test))

"""## K-Neighbors classifier - Confusion Matrix"""

from sklearn.metrics import confusion_matrix, plot_confusion_matrix

label=['GALAXY','STAR','QSO']
plot = plot_confusion_matrix(gknn,
                             X_test, y_test,
                             display_labels=label,
                             cmap=plt.cm.Blues,
                             normalize='true') 
plot.ax_.set_title('K-Neighbors classifier')

"""## Random forest classifier"""

from sklearn.ensemble import RandomForestClassifier

for n in [3,5]:
  rf = RandomForestClassifier()
  kfold = KFold(n_splits = n, random_state = 0, shuffle = True)
  param_grid = {
              "n_estimators": [10,100,200],
              "criterion": ["entropy"],
              "max_depth": [None, 2, 3, 4, 5],
  }
  grf=GridSearchCV(rf,param_grid=param_grid,cv=kfold,n_jobs=-1)
  grf.fit(X_train, y_train)
  print('n_splits: ',n)
  print('best parameter: ',grf.best_params_)
  print('cross validation score: ',grf.score(X_test, y_test))

"""## Random forest classifier - Classification"""

from sklearn.metrics import confusion_matrix, plot_confusion_matrix

label=['GALAXY','STAR','QSO']
plot = plot_confusion_matrix(grf,
                             X_test, y_test,
                             display_labels=label,
                             cmap=plt.cm.Blues,
                             normalize='true') 
plot.ax_.set_title('Random forest classifier')

"""## Bagging classifier"""

from sklearn.ensemble import BaggingClassifier

for n in [3,5]:
  bg = BaggingClassifier()
  kfold = KFold(n_splits = n, random_state = 0, shuffle = True)
  param_grid = {
              'n_estimators': [10, 50, 100],
              'max_samples': [1, 5, 10],
              'max_features': [1, 5, 10]
  }
  gbg=GridSearchCV(bg,param_grid=param_grid,cv=kfold,n_jobs=-1)
  gbg.fit(X_train, y_train)
  print('n_splits: ',n)
  print('best parameter: ',gbg.best_params_)
  print('cross validation score: ',gbg.score(X_test, y_test))

"""## Bagging classifier - Confusion Matrix"""

label=['GALAXY','STAR','QSO']
plot = plot_confusion_matrix(gbg,
                             X_test, y_test,
                             display_labels=label,
                             cmap=plt.cm.Blues,
                             normalize='true') 
plot.ax_.set_title('Random forest classifier')

"""## Adaboost classifier"""

from sklearn.ensemble import AdaBoostClassifier

for n in [3,5]:
  ad = AdaBoostClassifier()
  kfold = KFold(n_splits = n, random_state = 0, shuffle = True)
  param_grid = {
              'n_estimators': [25, 50, 100, 200],
              'learning_rate': [0.01, 0.1, 1.0]
  }
  gad=GridSearchCV(ad,param_grid=param_grid,cv=kfold,n_jobs=-1)
  gad.fit(X_train, y_train)
  print('n_splits: ',n)
  print('best parameter: ',gad.best_params_)
  print('cross validation score: ',gad.score(X_test, y_test))

"""## Adaboost classifier - Confusion Matrix"""

label=['GALAXY','STAR','QSO']
plot = plot_confusion_matrix(gad,
                             X_test, y_test,
                             display_labels=label,
                             cmap=plt.cm.Blues,
                             normalize='true') 
plot.ax_.set_title('Random forest classifier')

"""## Select Scaling Method - Robust Scaling"""

#Select Robust Scaling
xNorm = pd.DataFrame(dfClean_xRScaled)
xNorm.columns = dfClean_x.columns

"""## dfNorm: dataFrame with final preprocessing is completed"""

dfNorm = pd.concat([xNorm, dfClean_y], axis = 1) 

dfNorm

dfNorm.describe().T

y = dfNorm['class']
X = dfNorm.drop(['class'], axis = 1)

"""## Separate Train and Test set using"""

from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, shuffle = True, stratify = y, random_state = 34)

"""## Linear regression -  Fit"""

from sklearn.model_selection import KFold
from sklearn.model_selection import cross_val_score
from sklearn.linear_model import LinearRegression

linreg = LinearRegression()
linreg.fit(X_train, y_train)

"""## Linear regression - Evaluation"""

for n in [3, 5]:
    kfold = KFold(n_splits = n, random_state = 0, shuffle = True)
    
    # Scoring each sets
    scores = cross_val_score(linreg, X_test, y_test, cv=kfold)
    print('n_splits={}, cross validation score: {}'.format(n, scores))

"""## Decision tree classifier"""

from sklearn.model_selection import GridSearchCV
from sklearn.tree import DecisionTreeClassifier

for n in [3,5]:
  dtc = DecisionTreeClassifier()
  kfold = KFold(n_splits = n, random_state = 0, shuffle = True)
  param_grid = {
              'max_depth': [None, 2, 3, 4, 5, 6, 7, 8, 9, 10],
  }
  gdtc=GridSearchCV(dtc,param_grid=param_grid,cv=kfold,n_jobs=-1)
  gdtc.fit(X_train, y_train)
  print('n_splits: ',n)
  print('best parameter: ',gdtc.best_params_)
  print('cross validation score: ',gdtc.score(X_test, y_test))

"""## Decision tree classifier - Confusion Matrix"""

from sklearn.metrics import confusion_matrix, plot_confusion_matrix

label=['GALAXY','STAR','QSO']
plot = plot_confusion_matrix(gdtc, 
                             X_test, y_test, 
                             display_labels=label, 
                             cmap=plt.cm.Blues, 
                             normalize='true') 
plot.ax_.set_title('Decision tree classifier')

"""## K-Neighbors classifier"""

from sklearn.neighbors import KNeighborsClassifier

for n in [3,5]:
  knn = KNeighborsClassifier()
  kfold = KFold(n_splits = n, random_state = 0, shuffle = True)
  param_grid = {
              'n_neighbors': [None, 2, 3, 4, 5, 6],
  }
  gknn=GridSearchCV(knn,param_grid=param_grid,cv=kfold,n_jobs=-1)
  gknn.fit(X_train, y_train)
  print('n_splits: ',n)
  print('best parameter: ',gknn.best_params_)
  print('cross validation score: ',gknn.score(X_test, y_test))

"""## K-Neighbors classifier - Confusion Matrix"""

from sklearn.metrics import confusion_matrix, plot_confusion_matrix

label=['GALAXY','STAR','QSO']
plot = plot_confusion_matrix(gknn,
                             X_test, y_test,
                             display_labels=label,
                             cmap=plt.cm.Blues,
                             normalize='true') 
plot.ax_.set_title('K-Neighbors classifier')

"""## Random forest classifier"""

from sklearn.ensemble import RandomForestClassifier

for n in [3,5]:
  rf = RandomForestClassifier()
  kfold = KFold(n_splits = n, random_state = 0, shuffle = True)
  param_grid = {
              "n_estimators": [10,100,200],
              "criterion": ["entropy"],
              "max_depth": [None, 2, 3, 4, 5],
  }
  grf=GridSearchCV(rf,param_grid=param_grid,cv=kfold,n_jobs=-1)
  grf.fit(X_train, y_train)
  print('n_splits: ',n)
  print('best parameter: ',grf.best_params_)
  print('cross validation score: ',grf.score(X_test, y_test))

"""## Random forest classifier - Classification"""

from sklearn.metrics import confusion_matrix, plot_confusion_matrix

label=['GALAXY','STAR','QSO']
plot = plot_confusion_matrix(grf,
                             X_test, y_test,
                             display_labels=label,
                             cmap=plt.cm.Blues,
                             normalize='true') 
plot.ax_.set_title('Random forest classifier')

"""## Bagging classifier"""

from sklearn.ensemble import BaggingClassifier

for n in [3,5]:
  bg = BaggingClassifier()
  kfold = KFold(n_splits = n, random_state = 0, shuffle = True)
  param_grid = {
              'n_estimators': [10, 50, 100],
              'max_samples': [1, 5, 10],
              'max_features': [1, 5, 10]
  }
  gbg=GridSearchCV(bg,param_grid=param_grid,cv=kfold,n_jobs=-1)
  gbg.fit(X_train, y_train)
  print('n_splits: ',n)
  print('best parameter: ',gbg.best_params_)
  print('cross validation score: ',gbg.score(X_test, y_test))

"""## Bagging classifier - Confusion Matrix"""

label=['GALAXY','STAR','QSO']
plot = plot_confusion_matrix(gbg,
                             X_test, y_test,
                             display_labels=label,
                             cmap=plt.cm.Blues,
                             normalize='true') 
plot.ax_.set_title('Random forest classifier')

"""## Adaboost classifier"""

from sklearn.ensemble import AdaBoostClassifier

for n in [3,5]:
  ad = AdaBoostClassifier()
  kfold = KFold(n_splits = n, random_state = 0, shuffle = True)
  param_grid = {
              'n_estimators': [25, 50, 100, 200],
              'learning_rate': [0.01, 0.1, 1.0]
  }
  gad=GridSearchCV(ad,param_grid=param_grid,cv=kfold,n_jobs=-1)
  gad.fit(X_train, y_train)
  print('n_splits: ',n)
  print('best parameter: ',gad.best_params_)
  print('cross validation score: ',gad.score(X_test, y_test))

"""## Adaboost classifier - Confusion Matrix"""

label=['GALAXY','STAR','QSO']
plot = plot_confusion_matrix(gad,
                             X_test, y_test,
                             display_labels=label,
                             cmap=plt.cm.Blues,
                             normalize='true') 
plot.ax_.set_title('Random forest classifier')