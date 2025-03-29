import sys,os
import pandas as pd
import matplotlib.pyplot as plt
import statistics

#usage python3 prepare_results.py STATE+redox
#example python3 prepare_results.py S1Oxi

type='%s' % sys.argv[1].split('.')[0]
path=os.getcwd()

# Read the CSV file with predicted data into a dataframe
pred = type+'_pred.csv'
pred_df = pd.read_csv(pred)

# Read the CSV file with experimental data into a dataframe
exp = type+'_exp.csv'
exp_df = pd.read_csv(exp)

# Read the CSV file with model chemistries into a dataframe
model = 'model-chemistry.csv'
model_df = pd.read_csv(model)

# Merge df
pred_exp=pd.merge(pred_df,exp_df, on= 'InchKey', how = 'inner')
final_res=pd.merge(pred_exp,model_df,on= 'workflow', how = 'inner')

#Create ID
row_pd=len(final_res.axes[0])
ID=[]
for i in range(row_pd):
    ID.append(i)

final_res['ID'] = ID

#organize df
#final_res.drop(columns=["Unnamed: 3"], inplace=True)
t1=type+'_pred'
t2=type+'_exp'
col=['ID','Molecule','workflow','InchKey','functional','basis',t1,t2]
final_res=final_res[col]

#compute abs error
error_abs=[]
error_signed=[]
error_key=[]
row_pd=len(final_res.axes[0])
for i in range(row_pd):
    error_key.append(final_res.iloc[i,0])
    pred=float(final_res.iloc[i,6])
    exp=float(final_res.iloc[i,7])
    abserror=abs(pred-exp)
    error_abs.append(abserror)
    error_signed.append(pred-exp)
error_abs_df=pd.DataFrame(list(zip(error_key,error_abs)),columns =['ID','error-abs'])
error_signed_df=pd.DataFrame(list(zip(error_key,error_signed)),columns =['ID','error-signed'])
final_res_error1=pd.merge(final_res,error_abs_df, on= 'ID')
final_res_error=pd.merge(final_res_error1,error_signed_df, on= 'ID')

os.chdir(path)
final_res_error.to_csv('Error_'+type+'.csv',index=False)

#Model Chemistries 
functional=['SVWN','SVWN-5','M11-L','BB95','TPSSH','B3LYP-D3BJ','mPW1PW91','mPW1PBE','PBE0-D3BJ','M06','MPW1B95','BMK-D3BJ','MPW1K','BHandH','M06-2X','M06-HF','N12SX','MN12-SX','CAM-B3LYP-D3BJ','ωB97X','ωB97X-D']

basis=['6-311+G(d,p)','aug-cc-pVDZ']
semiempirical=['PM3','PM7','PM6','AM1']

#Compute MAE and stdev semiempirical
method_semiempirical=[]
MAE_semiempirical=[]
st_dev_semiempirical=[]

for i in semiempirical:
    method=i
    boolean_mask = final_res_error['functional']==i
    filtered_df = final_res_error[boolean_mask]
    if (not filtered_df.empty):
       error_list=[]
       row_pd=len(filtered_df.axes[0])
       error=0
       for i in range(row_pd):
           error+=float(filtered_df.iloc[i,8])
           error_list.append((filtered_df.iloc[i,8]))
       MAE=error/row_pd
       method_semiempirical.append(method)
       MAE_semiempirical.append(MAE)
       if len(error_list)>1:
          st_dev_semiempirical.append(statistics.stdev(error_list))
 
#MAE_semi_df=pd.DataFrame(list(zip(method_semiempirical,MAE_semiempirical,st_dev_semiempirical)),columns =['Method','MAE','st_dev'])
MAE_semi_df=pd.DataFrame(list(zip(method_semiempirical,MAE_semiempirical)),columns =['Method','MAE'])
MAE_semi_df = MAE_semi_df.sort_values(by='MAE', ascending=False)
os.chdir(path)
MAE_semi_df.to_csv('MAE_semiempirical_'+type+'.csv',index=False)



#Compute MAE DFT
method_dft=[]
basis_dft=[]
MAE_DFT=[]
MSE_DFT=[]
st_dev_dft=[]

for i in functional:
    method=i
    boolean_mask = final_res_error['functional']==i
    filtered_df = final_res_error[boolean_mask]
  
    for k in basis:
        basis_check=k
        boolean_mask2 = filtered_df['basis']==k
        filtered2_df = filtered_df[boolean_mask2]
        row_pd=len(filtered2_df.axes[0]) 
        #if (not filtered2_df.empty ):
        if (not filtered2_df.empty and row_pd > 4):
           error_list_abs=[]
           error_abs=0
           error_list_signed=[]
           error_signed=0
           for i in range(row_pd):
               error_abs+=float(filtered2_df.iloc[i,8])
               error_list_abs.append(float(filtered2_df.iloc[i,8]))
               error_signed+=float(filtered2_df.iloc[i,9])
               error_list_signed.append(float(filtered2_df.iloc[i,9]))
           MAE=error_abs/row_pd
           MSE=error_signed/row_pd
           method_dft.append(method)
           basis_dft.append(basis_check)
           MAE_DFT.append(MAE)
           MSE_DFT.append(MSE)
           st_dev_dft.append(statistics.stdev(error_list_abs))
        else:
              method_dft.append(method)
              basis_dft.append(basis_check)
              MAE_DFT.append(0.000000001)
              MSE_DFT.append(0.000000001)
              st_dev_dft.append(0.000000001) 

MAE_MSE_dft_df=pd.DataFrame(list(zip(method_dft,basis_dft,MAE_DFT,st_dev_dft,MSE_DFT)),columns =['Method','Basis','MAE','st_dev','MSE'])

#MAE_dft_df = MAE_dft_df.sort_values(by='MAE', ascending=False)
os.chdir(path)
MAE_MSE_dft_df.to_csv('MAE_MSE_DFT_'+type+'.csv',index=False)


# Create the figure and axes
fig, ax = plt.subplots(figsize=(10, 6))

# First basis set
basis1 = '6-311+G(d,p)'
boolean1 = MAE_MSE_dft_df['Basis'] == basis1
filtered_MAE1 = MAE_MSE_dft_df[boolean1]
x_values = filtered_MAE1['Method']
y_values_basis1 = filtered_MAE1['MSE']
mae_values_basis1 = filtered_MAE1['MAE']

# Second basis set
basis2 = 'aug-cc-pVDZ'
boolean2 = MAE_MSE_dft_df['Basis'] == basis2
filtered_MAE2 = MAE_MSE_dft_df[boolean2]
y_values_basis2 = filtered_MAE2['MSE']
mae_values_basis2 = filtered_MAE2['MAE']

# Plotting both basis sets on the same chart
bar_width = 0.35  # Width of the bars
x_indices = range(len(x_values))  # X-axis locations for the groups


# Add gridlines and labels to improve readability
ax.grid(True, which='both', axis='y', linestyle='--', alpha=0.7,zorder=1)

# Plotting MSE for basis1
ax.bar([i - bar_width / 2 for i in x_indices], y_values_basis1, width=bar_width, color='#B7C1CD', label=basis1,zorder=2)

# Plotting MSE for basis2
ax.bar([i + bar_width / 2 for i in x_indices], y_values_basis2, width=bar_width, color='#385492', label=basis2,zorder=2)

# Filter out MAE values equal to 0.000000001 for basis1
x_indices_basis1 = [i - bar_width / 2 for i, mae in zip(x_indices, mae_values_basis1) if mae != 0.000000001]
mae_values_filtered_basis1 = [mae for mae in mae_values_basis1 if mae != 0.000000001]

# Filter out MAE values equal to 0.000000001 for basis2
x_indices_basis2 = [i + bar_width / 2 for i, mae in zip(x_indices, mae_values_basis2) if mae != 0.000000001]
mae_values_filtered_basis2 = [mae for mae in mae_values_basis2 if mae != 0.000000001]

# Plotting MAE as dots for basis1 (excluding MAE = 0.000000001)
ax.scatter(x_indices_basis1, mae_values_filtered_basis1, color='#9CA5AF', edgecolors='#9CA5AF', zorder=3, label='MAE for ' + basis1)

# Plotting MAE as dots for basis2 (excluding MAE = 0.000000001)
ax.scatter(x_indices_basis2, mae_values_filtered_basis2, color='#29395D', edgecolors='#29395D', zorder=3, label='MAE for ' + basis2)



# Set axis labels and title
ax.set_ylabel('MSE (eV)',fontweight='bold',fontsize=20)
ax.set_xlabel('Density Functional',fontweight='bold',fontsize=20)

# Set x-axis ticks and labels
ax.set_xticks(x_indices)
ax.set_xticklabels(x_values, rotation=45, ha="right",fontsize=16)



# Set y-axis limits
ax.set_ylim([-0.8, 0.9])

plt.yticks(fontsize=16)


# Add legend
ax.legend(fontsize=14,loc='upper right')

# Show plot
plt.tight_layout()
figname = 'MAE_plot_' + type + '.png'
plt.savefig(figname, dpi=300)




