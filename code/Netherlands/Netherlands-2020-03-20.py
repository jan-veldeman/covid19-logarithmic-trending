# Data for Netherlands
# Sources:
# https://www.rivm.nl/nieuws/actuele-informatie-over-coronavirus
# ICU
# NOS drawing

import matplotlib.pyplot as plt
from matplotlib.pyplot import figure
from math import log, exp, pow
import numpy as np
import pandas as pd

day_of_march  = [14, 15, 16, 17, 18, 19, 20]
day_of_march_ICU  = [16, 17, 18, 19, 20]
day_of_march_future = [14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24]

hosp = [136, 162, 205, 314, 408, 489, 643]
ICU = [96, 135, 178, 210, 281]
deceased = [12, 20, 24, 43, 58, 76, 106]

log2_hosp = [log(x, 2) for x in hosp if x]
log2_ICU = [log(x, 2) for x in ICU if x]
log2_deceased = [log(x, 2) for x in deceased if x]

last_log2_diff_hosp = log2_hosp[-1] - log2_hosp[-2]
last_log2_diff_ICU = log2_ICU[-1] - log2_ICU[-2]
average_last_log2_diff = (last_log2_diff_hosp+last_log2_diff_ICU)/2
print("Average doubling days = %.2f" % (1/average_last_log2_diff))

# Fitting Polynomial Regression to the dataset
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression

X = [[x] for x in day_of_march]
X_ = [[x] for x in day_of_march_future]
y = log2_hosp

poly = PolynomialFeatures(degree = 2)
X_poly = poly.fit_transform(X)

poly.fit(X_poly, y)
lin2 = LinearRegression()
lin2.fit(X_poly, y)

figure(num=1, figsize=(10, 8))
plt.yscale("log")

values = [10, 25, 50, 100, 200, 400, 600, 800, 1000, 1500, 2000, 2500, 3000]
plt.yticks(values, ['%d' % val for val in values])
plt.plot(day_of_march, hosp, 's-', label="hospitalisations")
plt.plot(day_of_march_ICU, ICU, 's-', label="ICU")
#plt.plot(day_of_march, deceased, 's-', label="deceased")

trend = [pow(2, x) for x in lin2.predict(poly.fit_transform(X_))]

plt.plot(X_, trend, color = 'blue', dashes=[2, 4], label="hospitlisations trendline")

# trendline_dates = X_ # use this to see all trendline values, also in the past
trendline_dates = [[20],[21],[22],[23],[24]]

log2_hosp_near_max = lin2.predict(poly.fit_transform(trendline_dates))
print(f"Days of March:     {trendline_dates}")
print(f"Trendline numbers:  {[int(pow(2, x)) for x in log2_hosp_near_max]}")

plt.xlabel("day of March")
plt.ylabel("Total numbers")
plt.title("NETHERLANDS hospitalisation, ICU; \n The trendline IS NOT A PREDICTION ! ")
plt.legend()
plt.grid()
plt.show()
