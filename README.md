# glue_weights_upload
Tkinter GUI to help upload EC module glue weights (configured specifically for stencils can be adapted in necessary).

# Dependencies

Depends on the GUI library tkinter, numpy and itkdb.
itkdb version must be newer than v0.4, this will affect ITkDB access. 

# Installation
Windows: 

To create a virtual environment to ensure correct package versions are installed, running the following commands: 
```
python -m venv venv 
venv\Scripts\activate
```
Then run the following command to install all requireed packages
```
pip install -r requirements.txt
```
To close virtual environment, if desired, run following command: 
```
deactivate
```

To reopen virtual environment, simply run (has be to be done before using upload script): 
```
venv\Scripts\activate
```

Linux: 
To create a virtual environment to ensure correct package versions are installed, running the following commands: 
```
python -m venv venv 
source .venv/bin/activate
```
Then run the following command to install all requireed packages
```
pip install -r requirements.txt
```
To close virtual environment, if desired, run following command: 
```
deactivate
```

To reopen virtual environment, simply run (has be to be done before using upload script): 
```
source .venv/bin/activate
```

# Edits

At the top of the script there are a few variables which may need to be edited for proper upload. These are all under the heading:

```
# VARIABLES TO EDIT
GW_METHOD = "Stencil"
INSTITUTE = 'SFU'
```

# Running

To run the file, open a terminal and navigate to the folder containing this program and enter the following command:

Metrology:
Windows:
```
python glue_weights_upload.py 
```

Linux/MAC:
```
python3 glue_weights_upload.py
```

# Instructions

The GUI will pop up and request that you enter the serial number, run number, stencil version used and the weights that were taken during module assembly. You do not have to fill in every single value.

For modules with 2 hybrids and powerboard (R0, R1 and 3R), you need to enter one of the following combinations: 

    * bare sensor weight, hybrid 1 weight, hybrid 2 weight, powerboard weight, module with 1 hybrid weight, module with 2 hybrids weight, module with 2 hybrids and powerboard
    * bare sensor weight, hybrid 1 weight, hybrid 2 weight, powerboard weight, module with powerboard weight, module with 1 hybrid and powerboard weight, module with 2 hybrids and powerboard
    * bare sensor weight, hybrid 1 weight, hybrid 2 weight, powerboard weight, module with 1 hybrid weight, module with 1 hybrid and powerboard weight, module with 2 hybrids and powerboard

For modules with 1 hybrid and 1 powerboard (R2, 4R, 5R), you need to enter one of the following combinations: 
    * bare sensor weight, hybrid 1 weight, powerboard weight, module with 1 hybrid weight, module with 1 hybrid and powerboard
    * bare sensor weight, hybrid 1 weight, powerboard weight, module with powerboard weight, module with 1 hybrid and powerboard
    
For modules with 2 hybrids and no powerboard (3L), you need to enter all of the following weights: 
    * bare sensor weight, hybrid 1 weight, module with 1 hybrid, module with 2 hybrids  

For modules with 1 hybrid and no powerboard (4L and 5L), you need to enter all of the following weights: 
    * bare sensor weight, hybrid 1 weight, module with 1 hybrid    

After the all the required values are entered, press the "Calculate" button. The calculated glue weights will appear, the pass status will appear in the textbox at the bottom of the GUI. 
Press the "Save Data" button if you wish to proceed with uploading the test. 
