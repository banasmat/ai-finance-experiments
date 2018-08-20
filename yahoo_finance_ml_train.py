from app.dataset.XBRLDataSetProvider import XBRLDataSetProvider
from app.xbrl.XbrlRnn import XbrlRnn
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.svm import SVC

# https://towardsdatascience.com/solving-a-simple-classification-problem-with-python-fruits-lovers-edition-d20ab6b071d2

x, y = XBRLDataSetProvider.get_dataset_from_yahoo_fundamentals()

x = np.nan_to_num(x)

# year, cik, tag
x = x.transpose((2, 0, 1))
y = y.transpose()

# flattening all years data
x = np.reshape(x, (x.shape[0] * x.shape[1], x.shape[2]))
y = np.reshape(y, (y.shape[0] * y.shape[1]))

# using only one year data
# x = x[0]
# y = y[0]

X_train, X_test, y_train, y_test = train_test_split(x, y, random_state=0)
scaler = MinMaxScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

model = SVC()

model = model.fit(X_train, y_train)
preds = model.predict(X_test)
print(accuracy_score(y_test, preds))