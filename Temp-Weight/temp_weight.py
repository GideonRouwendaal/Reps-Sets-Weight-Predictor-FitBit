import pandas as pd
import os

from sklearn.metrics import accuracy_score
from sklearn.svm import SVR

path_parent = os.path.dirname(os.getcwd())
data_location = path_parent + './FitBit/temp_weight.xlsx'

data = pd.read_excel(data_location, engine='openpyxl')
data = pd.get_dummies(data, columns=["name_day", "Date"])

data_features = pd.DataFrame(data).drop(["weight"], axis=1)
target = pd.DataFrame(data[["weight"]])

X_train = data[:(len(data_features) - 1)]
X_test = data[(len(data_features) - 1):]
y_train = target[:(len(data_features) - 1)]
y_test = target[(len(data_features) - 1):]

X_train = X_train.to_numpy()
X_test = X_test.to_numpy()
y_train = y_train.values.ravel()
y_test = y_test.values.ravel()

svr = SVR()
svr.fit(X_train, y_train)
y_pred_svr = svr.predict(X_test)
print(y_pred_svr)

# print(accuracy_score(y_test, y_pred_svr))
