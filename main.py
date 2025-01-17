# Import necessary libraries
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import GridSearchCV

cc_apps = pd.read_csv("cc_approvals.data", header=None)
cc_apps_nans_replaced = cc_apps.replace("?", np.nan)
cc_apps_imputed = cc_apps_nans_replaced.copy()

for col in cc_apps_imputed.columns:
    if cc_apps_imputed[col].dtypes == "object":
        cc_apps_imputed[col] = cc_apps_imputed[col].fillna(
            cc_apps_imputed[col].value_counts().index[0]
        )
    else:
        cc_apps_imputed[col] = cc_apps_imputed[col].fillna(cc_apps_imputed[col].mean())

cc_apps_encoded = pd.get_dummies(cc_apps_imputed, drop_first=True)

X = cc_apps_encoded.iloc[:, :-1].values
y = cc_apps_encoded.iloc[:, -1].values

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=42)
scaler = StandardScaler()
rescaledX_train = scaler.fit_transform(X_train)
rescaledX_test = scaler.transform(X_test)

logreg = LogisticRegression()
logreg.fit(rescaledX_train, y_train.ravel())
y_train_pred = logreg.predict(rescaledX_train)
print(confusion_matrix(y_train, y_train_pred))

tol = [0.1,0.01,0.001]
max_iter= [100,200,300]
param_grid = dict(tol=tol, max_iter=max_iter)
model_grid = GridSearchCV(logreg,param_grid=param_grid,cv=5)
grid_model_fitting = model_grid.fit(rescaledX_train,y_train)

best_train_score,best_param = grid_model_fitting.best_score_, grid_model_fitting.best_params_
print("Best: %f using %s" % (best_train_score,best_param))

best_model =grid_model_fitting.best_estimator_
print("Best model: ",best_model)
best_score =  best_model.score(rescaledX_test, y_test)
print("Accuracy of logistic regression classifier: ", best_score)
