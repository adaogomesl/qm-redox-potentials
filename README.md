# qm-redox-potentials
Python code to automate quantum mechanical (QM) calculations, extract results, and analyze data for excited-state redox potentials. This includes input generation, job submission, parsing output files, and performing statistical and graphical analysis of computed redox properties.

## **Prerequisites**  
- Access to a **high-performance computing (HPC) cluster**  
- **Gaussian 16** ([Gaussian 16 Website](https://gaussian.com/gaussian16/)) and/or **GAMESS** ([GAMESS Website](https://www.msg.chem.iastate.edu/GAMESS/)) (version 2018-R1 or later)  
- **Anaconda** with **Python 3.8+** ([Anaconda Website](https://www.anaconda.com/))  
- Required software dependencies:  
  - **PyFlow** ([GitHub](https://github.com/adaogomesl/PyFlow))  
  - **workflowV2** ([GitHub](https://github.com/neal-p/workflowV2))  
  - **Open Babel**  
  - **Python libraries**:  
    - `numpy`  
    - `pandas`  
    - `matplotlib`  
    - `scipy`  
    - `networkx`  
    - `rdkit` (for molecular processing)  

## Workflow
<img width="761" alt="Screenshot 2024-04-01 at 5 05 06 PM" src="https://github.com/adaogomesl/Leticia-LopezLab/assets/100699955/d9bf93f6-7c90-488f-b049-3841c3d38f48">

--- 

## Generating Molecules

#### Draw molecule on Chemdraw and select substituent location by using U for spacers
<img width="149" alt="Example Core" src="https://github.com/Kimpton22/Tutorials-And-Guides/assets/100699955/c88389c5-64fc-41dc-9a27-c6f020c07565">

#### Changing spacers and terminals
Below are the spacers and terminal on the shared pymolgen script, if you need to change them, please edit the script

<img width="387" alt="terminal and spacers" src="https://github.com/Kimpton22/Tutorials-And-Guides/assets/100699955/c6599344-0b81-451d-9aa9-5a2715cfcc70">

### Generate pdb from SMILES using RDKit from pyflow
1. Remember to source your pyflow environment and request resources
2. To generate pdb files, use the following command, replacing "name-molecule" with the actual molecule name and "SMILES" with the actual SMILES string.
   ```
   python pymolgen.py name-molecule 'SMILES'
   ```
### Generate pdb from SMILES using CREST
1. Remember to have workflow-CREST.py on the folder you will generate the molecule
2. 2. To generate CREST workflow, use the following command, replacing "name-molecule" with the actual molecule name and "SMILES" with the actual SMILES string.
   ```
   python pymolgen-CREST.py name-molecule 'SMILES'
   ```
3. Submit the sbatch file generated and a CREST workflow will run to search for conformers
4. When the CREST search ends, xyz files will be generated and need to be converted to pbd. Change InchKey to the specific Inchkey of the molecule, generated by pymolgen-CREST.py
   ```
   obabel InchKey.xyz -O InchKey.pdb
   ```
--- 

## Creating and submitting workflows

#### 1. Set up workflow: change XXX for the workflow name
   ```
pyflow setup XXX --config_file config.json
   ```

#### 2. Copy molecules generated to unopt_pdbs directory inside the workflow folder 
_Limit of 1000 pdbs per workflow, conformers must be on the same workflow_

#### 3. Go inside workflow directory and submit the following command
   ```
pyflow begin
   ```
_If workflow with same name was submitted before, add --do_not_track flag_
 ```
pyflow begin --do_not_track flag
   ```

#### 4. Check progress
   ```
pyflow progress
   ``` 
---

## Check Normal termination calculations
Check if calculations have Normal terminal and no negative frequencies.
```
sbatch check_log.sh NAME-WORKFLOW
```
---

## Clean up workflow
Remove temporary files for failed jobs, for completed jobs them are automatically deleted
```
rm -r workflow*/*/*/failed/*.chk
```
```
rm -r workflow*/*/*/failed/*.rwf
```
---

## Check failed calculations
Check error message failed jobs on workflow and generate a csv with the information
```
python3 check-error-message.py NAME-WORKFLOW
```
---
## Resubmit failed calculations
The script will automatically configure resubmission files
```
python3 failed-organize-resub.py NAME-WORKFLOW
```
---

## Extract Potentials
1. Copy extraction script to the same directory of the workflow directory - gather-results.py

2. Extract the results - Replace workflow_name by the workflow directory name
_Reminders: Request resources and have PyFlow environment sourced_
```
python gather-results.py workflow_name
```

A CSV file will be generated with computed properties. Example of CSV is below:
<img width="644" alt="Screenshot 2025-03-28 at 9 18 16 PM" src="https://github.com/user-attachments/assets/8fff81bc-0f96-439a-8b5a-f40ebe994849" />


---
## Generate plots
### Compare predicted with experimental results
#### MAE Scatter plot and extract MAE, Error and MSE
```
python3 prepare_results.py STATE+redox
```
<img width="461" alt="Screenshot 2025-03-28 at 9 24 38 PM" src="https://github.com/user-attachments/assets/34f1a00c-20ad-4010-ad4b-e170ec838ca4" />


#### Plot Computation time and MAE
```
python3 plot_bar.py Title-freqtime.csv
```
<img width="556" alt="Screenshot 2025-03-28 at 9 30 45 PM" src="https://github.com/user-attachments/assets/c258572f-911c-4742-8af9-dc812475e486" />

#### Compare Correlation between predicted values and experimental value 
```
python3 plot_bar.py Title-freqtime.csv
```
<img width="502" alt="Screenshot 2025-03-28 at 9 31 09 PM" src="https://github.com/user-attachments/assets/7c07e967-17b4-4ac0-81af-a246ba1bcc79" />

### S0 Potentials + ColorMap showing wavelength
CSV details
  1. Need to be named S0.csv
  2. Collumn must have specific names: Oxi_S0,Red_S0,Wavelength

Usage
```
python3 pred-exp-plot_T1Red.py
```

Resulted plot
<img width="467" alt="Screenshot 2025-03-28 at 9 32 50 PM" src="https://github.com/user-attachments/assets/f90dcf45-b93e-4bb5-8259-1e80b81636ca" />


### Excited State Potentials + ColorMap showing wavelength
CSV details
  1. Need to be named S1.csv or T1.csv
  2. Collumn must have specific names: Oxi_S1,Red_S1
     
_in case of T1, replace S1 for T1_

Usage
```
python3 plot-scatter.py S1
```
Resulted plot
<img width="469" alt="Screenshot 2025-03-28 at 9 25 33 PM" src="https://github.com/user-attachments/assets/7f01c8d7-a19d-42e8-8e45-b0802c855d53" />

