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

## Installation
1. Clone this GitHub repository into your home directory on the cluster.
	```console
	git clone https://github.com/adaogomesl/qm-redox-potentials
	```
2. Go into the newly created `qm-redox-potentials` directory and set up an Anaconda environment using the provided environment.yml file.
	```console
    conda env create --file environment.yml
	```
3. Activate the newly created environment.
	```console
    conda activate qm-redox-potentials
	```
4.  Run the following setup command within the PyFlow directory.
    ```console
    pip install -r requirements.txt
    
5. If you intend to use GAMESS, create a directory called `scr` within your scratch directory.
