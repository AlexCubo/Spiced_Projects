## Gapminder
 The project analyzes one of the [Gapminder](https://www.gapminder.org/) projects by [Hans Rosling](https://en.wikipedia.org/wiki/Hans_Rosling).

I selected few countries (Argentina, canada, Italy and Vietnam) and plotted the life expectation vs fertility rate in 50 years. The dimension of scattered point is proportional to the population.
The population legend must be multiplied by 10 millions.

* Life Expectancy vs. Fertility:
  <p align="center">
  <img src="./Life_expectancy_Fertility/p_movies/lifeFert_movie.gif" width="50%" height="50%">
  </p>

The Jupyter notebook about this project can be found [here](./Life_expectancy_Fertility/animated_scatteredplot.ipynb)

## Surviving Titanic
The project is a classification problem. The aim is to train and test different machine learning models to predict the surviving probability of passengers of the RMS Titanic, during the tragedy of 15 April 1912.

I trained the data with Logistic Regression, Decision Tree and Random Forest and made a comparison of the three models for training and test data: 

<p align="center">
  <img src="./Surviving_Titanic/images/accuracy_comparison.png" width="100%" height="100%">
  </p>

The Jupyter notebook about this project can be found [here](./Surviving_Titanic/project2_survivingTitanic.ipynb)

I took part of the Kaggle competition "Titanic - Machine Leraning from disaster" [see here](https://www.kaggle.com/c/titanic/submissions)

## Bike Rental
The project is a regression progect. The goal is to predict the number of bikes rented in at any hour using ML regeression models. The features are timestamp and wheater information. Therefore it is a timeseries problem.

I trained the data using different regressors: Linear Regression, Linear Regression with Ridge regularization, Random Forest and Gradient Boosting Regressor. For Random Forest I made a second training
called RF_plus, where I added some additional features, just to see if I could improve the score.
I compared these models with the  most popular regression scores: MSE (Mean Square Error), RMSLE (Root Mean Square Logarithmic Error) and $R^2$ score (Coefficient of Determination):


<p align="center">
  <img src="./Bike_Rental/images/models_comparison.png" width="100%" height="100%">
  </p>

The Jupyter notebook about this project can be found [here](./Bike_Rental/bike_sharing_project.ipynb)

I took part of a Kaggle competition titled "Bike Sharing Demand - Forecast of a city bikeshare system". The results can be found [here](https://www.kaggle.com/c/bike-sharing-demand/submissions)





