# Report - Assignment 1

### Team Members: Karthik Viswanathan, Abhishekh Sivakumar

## 2.1     Task 1: Linear Regression

Given a pair of training data's $x$  values and $y$ values, the linear regression model takes these pairs as arguments and fits them along a straight line/curve to minimize the residual sum of squares between the observed targets in the dataset ($y$), and the targets predicted by the linear approximation ($\hat{f}$).

Mathematically, the function fits a model with coefficients $w = (w_1, ..., w_p)$ to solve the problem of the form —

$$\min_{w} || X w - y||_2^2$$

    The `LinearRegression().fit()` function implements the Ordinary Least Squares (OLS) method to estimate the unknown parameters in the linear regression model. The least-squares solution is computed using the singular value decomposition of $\mathbf{X}$.

## 2.2.2   Task

### Bias and variance changes on varying function classes

[Bias and variance per degree of model](https://www.notion.so/5b0177dca6d84553b37c31ce4b091e3f)

![Report%20-%20Assignment%201%208540b8b568d047bfa4537304bf60616d/Untitled.png](Report%20-%20Assignment%201%208540b8b568d047bfa4537304bf60616d/Untitled.png)

![Report%20-%20Assignment%201%208540b8b568d047bfa4537304bf60616d/Untitled%201.png](Report%20-%20Assignment%201%208540b8b568d047bfa4537304bf60616d/Untitled%201.png)

The best possible fit (minimum total error) is observed for the degree of polynomial near three. While the bias for further degrees until degree 10 stays low, the variance steadily increases; hence the total error increases too.

- **Polynomials of degrees one and two**
It can be seen that models of degree one and two are oversimplified and do not generalize the data well, and hence have a high bias. These models are consistent, i.e., their predicted values are not very scattered (due to the smaller number of features) which explains the low variance.
- **Polynomial of degree three**
The lowest overall error is demonstrated by the cubic polynomial regression. Clearly, it fits the data best and generalizes well to data not yet seen by the model before.
- **Polynomials of degrees four and above**
Variance sees a gradual increase with the increase in complexity. This is to be expected as the number of features is higher, leading to models that overfit the training data. The high variance can be explained by the more complex regression models attempting to fit the noise that occurs in the training data. This flexibility provided by a greater number of features leads to capturing of noise which in turn causes incorrect predictions for unseen data.
The relatively low bias is because the more complex model is able to model the training set well.

## 2.3     Task 3: Calculating Irreducible Error

[Irreducible error per degree of model](https://www.notion.so/fbb1072ba86e49e9b25539a35a8f5a6d)

![Report%20-%20Assignment%201%208540b8b568d047bfa4537304bf60616d/Untitled%202.png](Report%20-%20Assignment%201%208540b8b568d047bfa4537304bf60616d/Untitled%202.png)

                                                                  Irreducible Error Plot

Clearly, the irreducible error tabulated and graphed show no consistent variations or patterns. Irreducible errors are errors that cannot be reduced no matter what algorithm is applied. It is a measure of noise in our data, which is inherently independent of the model or regression analysis employed to make predictions.

## 2.4     Task 4: Plotting $bias^2 - variance$ graph

[Bias^2 - Variance - Error](https://www.notion.so/7b6ab136e4b54ac692c993ef3712a669)

![Report%20-%20Assignment%201%208540b8b568d047bfa4537304bf60616d/Untitled%203.png](Report%20-%20Assignment%201%208540b8b568d047bfa4537304bf60616d/Untitled%203.png)

- Polynomials of degree one and two show underfitting as they have high bias.
- Higher degree polynomial regression models (four and above) have high variance and relatively low bias which indicates overfitting.
- As expected, the total error for the best fitting degree has to be the least; and hence the degree-3 has the best fit with the least error.
- The evolution of the fit by various degrees have been shown below:

![Report%20-%20Assignment%201%208540b8b568d047bfa4537304bf60616d/Untitled%204.png](Report%20-%20Assignment%201%208540b8b568d047bfa4537304bf60616d/Untitled%204.png)

![Report%20-%20Assignment%201%208540b8b568d047bfa4537304bf60616d/Untitled%205.png](Report%20-%20Assignment%201%208540b8b568d047bfa4537304bf60616d/Untitled%205.png)

![Report%20-%20Assignment%201%208540b8b568d047bfa4537304bf60616d/Untitled%206.png](Report%20-%20Assignment%201%208540b8b568d047bfa4537304bf60616d/Untitled%206.png)

![Report%20-%20Assignment%201%208540b8b568d047bfa4537304bf60616d/Untitled%207.png](Report%20-%20Assignment%201%208540b8b568d047bfa4537304bf60616d/Untitled%207.png)

Fitting for degree-2 (underfitting)

Fitting for degree-3 (just right)

Fitting for degree-12 (high variance and low bias ; overfitting)

As we move towards higher degrees, the bias also increases along with the variance.

Fitting for degree-20 (high variance, high bias)

## Observations

- From the above graphs, it can be observed that as the complexity of the model increases beyond a certain point, the model tends to overfit the training data. This induces a condition known as *high variance* where the test data's fit tends to be spread out. Due to overfitting, the model will not be able to generalize on data it which hasn't been fed to it yet. After one point, the bias also increases along with the variance attributing to an extreme overfit.
- For lower degree polynomials, the models experience *high bias* but *low variance.* Since the model is not able to learn from the features properly, it faces high bias. Even though they face bias and the results are not accurate, the fittings are not spread out for various realizations of the model. Furthermore, it can be observed that the *irreducible error* is close to zero; indicating that there is very minimal noise in the provided dataset.
