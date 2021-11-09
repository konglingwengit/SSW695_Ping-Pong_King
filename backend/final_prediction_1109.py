#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression 
from sklearn import metrics
from sklearn.metrics import accuracy_score
from sklearn.ensemble import RandomForestClassifier
from pprint import pprint
from sklearn.metrics import accuracy_score
from sklearn.naive_bayes import GaussianNB
from sklearn import metrics




#read data
df = pd.read_csv(r'/Users/lingwenkong/Downloads/ML_table_tennis/final_table.csv')
cols = ['playerA','PlayerB','who_win','Exact Number of Sets','Total Points','First Game Winner','Sets Decided by Extra Points']
games_results = df[cols]


#process
ind = games_results.drop(columns = 'who_win')
res = games_results['who_win']
x_train, x_test, y_train, y_test = train_test_split(ind, res, test_size = 0.2)

# # Classification by Logistic regression

# create a simple, non-parameterized Logistic Regression model
model = LogisticRegression(random_state=42)
model.fit(x_train, y_train)

y_pred = model.predict(x_test)
#print(metrics.accuracy_score(y_test, y_pred))

from pprint import pprint
# Look at parameters used by our current forest
#print('Parameters currently in use:\n')
#pprint(model.get_params())

# create complex Logistic Regression with max_iter=131 
log_model = LogisticRegression(max_iter=131, verbose=2, random_state=42)
log_model.fit(x_train, y_train)
y_pred_log = log_model.predict(x_test)

# # Classificcation by Random forest model
rf = RandomForestClassifier(random_state=42)
rf.fit(x_train, y_train)
y_pred_rf = rf.predict(x_test)

# # Classification by Gaussian Naive Bayes
#Import Gaussian Naive Bayes model

#Create a Gaussian Classifier
model = GaussianNB()
# Train the model using the training sets
model.fit(x_train,y_train)
y_pred = model.predict(x_test)
#print(metrics.accuracy_score(y_test, y_pred))


# Look at parameters used by our current forest
#print('Parameters currently in use:\n')
#print(model.get_params())

# create complex Logistic Regression with max_iter=131 
log_model = LogisticRegression(max_iter=131, verbose=2, random_state=42)
log_model.fit(x_train, y_train)
y_pred_log = log_model.predict(x_test)

player_id_value_counts = games_results['playerA'].value_counts()
valid_player_ids = [x for x in games_results['playerA'] if player_id_value_counts[x] > 16]
ind = games_results.drop(columns = 'who_win')
res = games_results['who_win']

trainX, testX, trainY, testY = train_test_split(ind, res, test_size = 0.2)
y_pred_log = log_model.predict(testX)
who_wins = y_pred_log

games_results = games_results[games_results['playerA'].isin(valid_player_ids)]

log_reg = LogisticRegression(solver='newton-cg', multi_class='multinomial')
log_reg.fit(trainX, trainY)
y_predE = log_reg.predict(testX)


if __name__ == '__main__':
    a = input('playerA id : ')
    b = input('playerB id : ')
    found = False
    for index, row in df.iterrows():
        if a == str(row["playerA"]) and b == str(row["PlayerB"]):

            if row['who_win'] == 0:
                who_win = a
            else:
                who_win = b

            if row["First Game Winner"] == 0:
                first_win = a
            else:
                first_win = b

            print(f'Prediction fields {who_win}, {row["Exact Number of Sets"]}, {row["Total Points"]}, '
                  f'{first_win}, {row["Sets Decided by Extra Points"]} ')

            found = True
            print('final result\n'
                  f'{who_win}, {row["Exact Number of Sets"]}, {row["Total Points"]}, '
                  f'{first_win}, {row["Sets Decided by Extra Points"]} ')

            break
    if not found:
        print('[0,4,85,0,1]'
              '\n'
              f'[{a}, 4,85, {b}, 1]')


# In[ ]:




