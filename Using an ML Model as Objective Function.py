import numpy as np
from scipy.optimize import minimize
from sklearn.datasets import make_regression
from sklearn.linear_model import Ridge


#Generate data for regression problem
X, y = make_regression(n_samples=1000, n_features=2, n_informative=2, n_targets=1, bias=3,  noise=2, shuffle=True, random_state=51)

#View Data X
print("Head X", pd.DataFrame(X).head())
print("Tail X", pd.DataFrame(X).tail())

#View Data y
print("Head y", pd.DataFrame(y).head())
print("Tail y", pd.DataFrame(y).tail())

#Generate Correlation Matrix to Establish Relationships
features = pd.DataFrame(X)
target = pd.DataFrame(y, columns={'t'})

features = pd.concat([features,target], axis=1)
corr = features.corr('pearson')
corr = corr.round(2)

f, ax = plt.subplots(figsize=(8,6))
cmap = sns.diverging_palette(220, 10, as_cmap=True)
sns.heatmap(corr, cmap=cmap, vmax=1,vmin=-1, center=0, square=True, linewidths=.5)



#Separate data into train and test sets
X, X_test, y, y_test = train_test_split(X, y, test_size=0.25, random_state=12)

#Build Ridge regression model
rr = Ridge(alpha=1, fit_intercept=True, normalize=True, copy_X=True, max_iter=5000, tol=0.0001, solver='svd', random_state=50).fit(X,y)

#Check Model Accuracy
print("Model Accuracy: ", rr.score(X_test, y_test))

#Define objective function
def lr(x):
    x1 = x[0]
    x2 = x[1]
    x_test = [[x1, x2]]
    final = -(rr.predict(x_test)[0]) + x1**x2
    return final


#Initial Guesses
x0 = np.array([1, 1])

b = (0, 3)

#Bounds on variables
bnds = [(-25,25), (-1.5, 5.5)]

#Minimize function
res = minimize(lr, x0, method='SLSQP', bounds=bnds)
#print results of optimization
print(res)
#Extract final value given inputs
x_final = [[res.x[0], res.x[1]]]
#Print Final Value
print(rr.predict(x_final))
