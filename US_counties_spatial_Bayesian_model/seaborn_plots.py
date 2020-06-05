import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns; sns.set()

"""
This script takes the INLA summary statistics from the R codes and generates a box plot for the posterior distribution of each feature. The y axis quanitifies the magnitude of the effect on the incidence or death rate (to be specified).
"""

# Read in the data and rename attributes column.
raw_data = pd.read_csv("fixed_effects_summary.csv").rename(columns={"Unnamed: 0": "Attributes"})
	
# Drop the intercept attribute as we don't plot this.
raw_data = raw_data.set_index(raw_data['Attributes']).drop("(Intercept)").reset_index(drop=True)

# Assign colour based on positive or negative effect.
my_pal = {}
new_labels = ["Annual AQI", "2 week AQI", "Income per Capita", "Hospital expenditure", "Health expenditure", "Density"]
m = 0
while m < len(raw_data):
	raw_data = raw_data.replace({"Attributes": {raw_data["Attributes"][m]: new_labels[m]}})
	if raw_data["0.5quant"][m] > 0:
		my_pal[raw_data["Attributes"][m]] = "g"
	else:
		my_pal[raw_data["Attributes"][m]] = "r"
	m += 1

# Extract the colums for the box plots.
data = pd.DataFrame(raw_data[["0.025quant", "0.5quant", "0.975quant"]]).set_index(raw_data['Attributes']).T

# Plot.
fig = plt.figure(figsize=(14, 6))
ax = plt.subplot(111)
ax.set_xlabel("Attributes", fontsize=16, labelpad=10)
ax.set_ylabel("Effect on rate", fontsize=16)
ax.set_title("Median and 95% confidence intervals for marginal posterior of each attribute", fontsize=18)
ax.axhline(y=0, linestyle='--', color='gray')
sns.boxplot(data=data, palette=my_pal, ax=ax)
plt.show()