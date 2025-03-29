import sys,os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

title='%s' % sys.argv[1].split('.')[0]

#Read time data from the CSV file
csv_name1=title+'-freqtime.csv'
time_df = pd.read_csv(csv_name1)

#Read MAE data from the CSV file
csv_name=title+'-mae.csv'
mae_df = pd.read_csv(csv_name)

# Extract data from the DataFrame
functional = time_df['Functional']
basis1='6-311+G(d,p)'
basis2='aug-cc-pVDZ'
scatter_values1=mae_df[basis1]
scatter_values2=mae_df[basis2]
values1 = time_df[basis1]
values2 = time_df[basis2]


# Set the width of the bars
bar_width = 0.20

# Create an array of indices for x-axis ticks (for positioning the bars)
x = np.arange(len(functional))

color1='#B7C1CD'
color2='#385492'

# Create the bar plot
plt.figure(figsize=(8, 6))
plt.bar(x - bar_width, values1, bar_width,color=color1, label=basis1)
plt.bar(x, values2, bar_width,color=color2, label=basis2)


# Customize the chart
plt.ylabel('Job CPU Time (hours)',weight='bold',size=20)
plt.ylim(0, 30)
plt.xlim(left=min(x - bar_width) - 4*bar_width / 2, right=5.5)
plt.xticks(x,functional,rotation=45, ha='right',size=16)
plt.yticks(fontsize=16)
plt.legend(fontsize=14,loc='upper right')

plt.tick_params(axis='both', which='both', pad=5)
plt.tight_layout()


# Create scatter plot with a secondary y-axis
ax2 = plt.twinx()
ax2.scatter(x - bar_width, scatter_values1, color='#9CA5AF', edgecolors='#9CA5AF', marker='o', label='MAE')
ax2.scatter(x, scatter_values2, color='#29395D',edgecolors='#29395D', marker='o', label='MAE')
ax2.set_ylabel('MAE (eV)', weight='bold',size=20)
ax2.set_ylim(0,0.25)
ax2.tick_params(labelsize=16)






# Step 3: Change the font settings
font = {'family': 'sans-serif', 'weight': 'bold', 'size': 14}
plt.rc('font', **font)

# Step 6: Save the plot as a PNG image
plt.savefig('plot_'+title+'.png', bbox_inches='tight',dpi=850)

