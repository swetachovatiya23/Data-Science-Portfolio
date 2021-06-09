# -*- coding: utf-8 -*-
"""click_on_Ad_or_not.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1_fO0yXoH5EBcEqB-sQW7LpaARUDG7xJg

# Logistic Regression 
- Predict whether or not customer will click on an ad based on the features of that user.
"""

from google.colab import drive
drive.mount('/content/drive')

"""#Import Libraries"""

# Commented out IPython magic to ensure Python compatibility.
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
# %matplotlib inline

"""## Get the Data

"""

data = pd.read_csv('/content/drive/MyDrive/Colab Notebooks/Machine learning/Classification/Logistic Regression/click_on_Ad_or_not/advertising.csv')

data.head()

data.info()

data.describe()

"""## Exploratory Data Analysis


"""

sns.set_style('whitegrid')
data['Age'].hist(bins=30)
plt.xlabel('Age')

"""** Finally, create a pairplot with the hue defined by the 'Clicked on Ad' column feature.**"""

sns.pairplot(data,hue='Clicked on Ad',palette='bwr')

"""# Logistic Regression

#Split the data into Train and Test set
"""

from sklearn.model_selection import train_test_split

X = data[['Daily Time Spent on Site', 'Age', 'Area Income','Daily Internet Usage', 'Male']]
y = data['Clicked on Ad']

print(np.array(X))

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=42)

"""#Train the model"""

from sklearn.linear_model import LogisticRegression

model = LogisticRegression()
model.fit(X_train,y_train)

"""## Prediction

"""

predictions = model.predict(X_test)

pred = model.predict(np.array([[6.895000e+01, 3.500000e+01 ,6.183390e+04 ,2.560900e+02, 0.000000e+00]]))

pred

"""#Evaluation"""

from sklearn.metrics import classification_report

print(classification_report(y_test,predictions))

#Store the model parameters using Pickle libraries

import pickle
pickle.dump(model, open('ads_model.pkl','wb'))

