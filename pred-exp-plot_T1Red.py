import sys,os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats
from matplotlib.ticker import FormatStrFormatter  # Import FormatStrFormatter

plt.figure(figsize=(5, 4))

csv_files= ['B97X-63111.csv','B97X-D-6-111.csv','M06-2X-aug-pVDZ.csv']
color_plot=['#C6C6C6','#6B8CC2','#2F5597']
label_plot=['ωB97X/6-311+G(d,p)','ωB97X-D/6-311+G(d,p)','M06-2X/aug-cc-pVDZ']

for i in range(len(csv_files)):
    title = csv_files[i]  # Use each CSV file as the title
    color_plt=color_plot[i]
    label_plt=label_plot[i]

    # Read data from the CSV file
    data = pd.read_csv(title)

    # Get the columns for x (exp) and y (pred)
    x = data['exp']
    y = data['pred']

    # Perform linear regression similar to Excel's LINEST
    X = np.vstack([x, np.ones(len(x))]).T
    slope, intercept = np.linalg.lstsq(X, y, rcond=None)[0]

    # Calculate R-squared manually
    predicted = slope * x + intercept
    residuals = y - predicted
    SS_res = np.sum(residuals**2)
    SS_tot = np.sum((y - np.mean(y))**2)
    r_squared = 1 - (SS_res / SS_tot)

    # Create a scatter plot for each CSV file with label as file name
    plt.scatter(x, y, color=color_plt, label=f'{label_plt}  $R^2 = {r_squared:.2f}$')

    # Generate x values for the trendline
    x_values = np.linspace(min(x), max(x), 100)
    # Calculate corresponding y values
    y_values = slope * x_values + intercept

    # Plot the linear regression line for each CSV file
    plt.plot(x_values, y_values, linestyle='dotted',color=color_plt)


#Set labels and title
plt.xlabel('$T_{\mathrm{1}}$ $E*_{\mathrm{red, \\mathit{exp}}}$',size=14)
plt.ylabel('$T_{\mathrm{1}}$ $E*_{\mathrm{red, \\mathit{calc}}}$',size=14)

# Set font size for tick labels
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)

# Format ticks to show two decimal places
plt.gca().xaxis.set_major_formatter(FormatStrFormatter('%.2f'))
plt.gca().yaxis.set_major_formatter(FormatStrFormatter('%.2f'))

# Show legend
plt.legend(fontsize=10,loc='upper right')

font = {'family': 'sans-serif','weight':'bold','size': 20}
plt.rc('font', **font)


# Save the plot as a PNG file
plt.savefig('T1Red-predxexp.png', bbox_inches='tight', dpi=850)
plt.show()
