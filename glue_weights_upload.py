"""GUI for the upload of module glue weight test in Vancouver."""

import numpy as np
import tkinter as tk
import math
from tkinter import filedialog
import itkdb
from datetime import datetime
from tkinter.constants import DISABLED, NORMAL
from tkinter import END

# VARIABLES TO EDIT - MODIFY THESE!
GW_METHOD = "Stencil"
INSTITUTE = 'SFU'

# CONSTANTS
ENTRY_X = 100
ENTRY_Y = 20
# following isn't currently used
GLUE_METHOD_V_H1 = ""
GLUE_METHOD_V_H2 = ""
GLUE_METHOD_V_PB = ""

# Define glue limit thicknesses - values are based on TB 120um target glue thicknesses
# 3R is H0 and H2
# 3L is H1 and H3

H0_glue_limit_dict = {
    'M0': [0.093, 0.127], # 110 +- 17
    'M1': [0.132, 0.178],# 155 +- 23
    'M2': [0.147, 0.201], # 174 +- 27
    '3R': [0.076, 0.104], # 90 +- 14
    '4R': [0.105, 0.143], # 124 +- 19
    '5R': [0.115, 0.155] # 135 +- 20
}

H1_glue_limit_dict = { 
    'M0': [0.102, 0.138], # 120 +- 18
    'M1': [0.133, 0.179], # 156 +- 23
    # M2 doesn't have H1
    '3L': [0.096, 0.130], # 113 +- 17
    '4L': [0.117, 0.157], # 137 +- 20
    '5L': [0.130, 0.172] # 151 +- 21
}


H2_glue_limit_dict = { 
    '3R': [0.092, 0.124] # 108 +- 16
}
H3_glue_limit_dict = { 
    '3L': [0.100, 0.136] # 118 +- 18
}

PB_glue_limit_dict = {
    'M0': [0.071, 0.097], # 84 +- 13
    'M1': [0.071, 0.097], # 84 +- 13
    'M2': [0.062, 0.086], # 74 +- 12
    '3R': [0.134, 0.180], # 157 +- 23
    '4R': [0.087, 0.119], # 103 +- 16
    '5R': [0.087, 0.119] # 103 +- 16
}


DATA_DICT = dict()
results = dict()

global data, client

def get_module_type():
    module_sn = serial_number.get()

    print(module_sn)

    if "M0" in module_sn:
        mod_type = "M0"
    elif "M1" in module_sn:
        mod_type = "M1"
    elif "M2" in module_sn:
        mod_type = "M2"        
    elif "3R" in module_sn:
        mod_type = "3R"
    elif "3L" in module_sn:
        mod_type = "3L"
    elif "4R" in module_sn:
        mod_type = "4R"
    elif "4L" in module_sn:
        mod_type = "4L"       
    elif "5R" in module_sn:
        mod_type = "5R"
    elif "5L" in module_sn:
        mod_type = "5L"     

    ## next lines can be used to auto-fill stencil versions when you press calculate
    # hyb1_stencil_box.insert(0, GLUE_METHOD_V_H1)
    # pb_stencil_box.insert(0, GLUE_METHOD_V_PB) 
    # if mod_type == ('M0' or 'M1' or '3R' or '3L'):
    #     hyb2_stencil_box.insert(0, GLUE_METHOD_V_H2)
     
    return mod_type            

def get_parameters():
    
    DATA_DICT["component"] = serial_number.get()
    DATA_DICT["testType"] = "GLUE_WEIGHT"
    DATA_DICT["institution"] = INSTITUTE
    DATA_DICT["runNumber"] = run_num.get()

    properties = dict()
    properties['GW_METHOD'] = 'Stencil'
    properties['GLUE_METHOD_V_PB'] = stencil_pb.get()
    properties['GLUE_METHOD_V_H1'] = stencil_hyb1.get()
    properties['GLUE_METHOD_V_H2'] = stencil_hyb2.get()

    DATA_DICT['properties']  = properties

    # store all the known values - measured during assembly
    results['GW_SENSOR'] = float(bare_sensor.get()) # weight of bare HV tabbed module
    results['GW_HYBRID1'] = float(hyb1.get()) # weight of hybrid 1 without tabs
    if hyb2.get() != '': 
        results['GW_HYBRID2'] = float(hyb2.get()) # weight of hybr 2 without tabs 
        results['GW_MODULE_H1H2'] = float(mod_w_hyb1_hyb2.get()) # weight of module with 2 hybrids
    if pb.get() != '': 
        results['GW_PB'] = float(pb.get()) # weight of powerboard
        results['GW_MODULE_H1PB'] = float(mod_w_hyb1_pb.get()) # weight ofmodule with one hybrid and powerboard 
    if total_mod.get() != '': results['GW_MODULE_H1H2PB'] = float(total_mod.get()) # weight of module with 2 hybrids and powerboard 
    if mod_w_hyb1.get() != '': results['GW_MODULE_H1'] = float(mod_w_hyb1.get()) # weight of module with 1 hybrid
    if mod_w_pb.get() != '': results['GW_MODULE_PB'] = float(mod_w_pb.get()) # weight of module with powerboard


def round(number, decimal=4):
    """Truncates a float to a value given by decimal. Default is 4 decimal places."""
    factor = 10.0 ** decimal
    return math.trunc(number * factor)/ factor

def calculate_glue_weights():

    # Clear everything
    # under_hyb1_box.delete(1.0, END)
    # under_hyb2_box.delete(1.0, END)
    # under_hyb1_hyb2_box.delete(1.0, END)
    # under_pb_box.delete(1.0, END)
    # under_hyb1_pb_box.delete(1.0, END)
    # under_hyb1_hyb2_pb_box.delete(1.0, END)
    under_hyb1_box.delete(0, END)
    under_hyb2_box.delete(0, END)
    under_hyb1_hyb2_box.delete(0, END)
    under_pb_box.delete(0, END)
    under_hyb1_pb_box.delete(0, END)
    under_hyb1_hyb2_pb_box.delete(0, END)

    # calculate all the glue weights 

    module_type = get_module_type()
    print("MODULE TYPE DETECTED: {0}".format(module_type))

    # fill in dictionary with all known values 
    get_parameters()

    # Now we have to go through all cases 
    # R0, R1 and 3R: 
    # case 1: glue hybrids first, then pb 
    # case 2: glue pb first, then hybrids 
    # case 3: glue hybrid, pb, then 2nd hybrid
    # case 4: glue both hybrids, then record weight
    
    # case 1
    if module_type in ['M0', 'M1', '3R']: 
        if (mod_w_hyb1.get() != '') and (mod_w_hyb1_hyb2.get() != '') and (mod_w_pb.get() == ''):
            # get weight under first hybrid 
            results['GW_GLUE_H1'] = results['GW_MODULE_H1'] - results['GW_SENSOR'] - results['GW_HYBRID1']
            # get weight under second hybrid 
            results['GW_GLUE_H2'] = results['GW_MODULE_H1H2'] - results['GW_MODULE_H1'] - results['GW_HYBRID2']
            # get weight under pb 
            results['GW_GLUE_PB'] = results['GW_MODULE_H1H2PB'] - results['GW_MODULE_H1H2'] - results['GW_PB']
        # case 2
        elif (mod_w_pb.get() != '') and (mod_w_hyb1_pb.get() != '') and (mod_w_hyb1.get() == ''):    
            # get weight under first hybrid 
            results['GW_GLUE_H1'] = results['GW_MODULE_H1PB'] - results['GW_MODULE_PB'] - results['GW_HYBRID1']
            # get weight under second hybrid 
            results['GW_GLUE_H2'] = results['GW_MODULE_H1H2PB'] - results['GW_MODULE_H1PB'] - results['GW_HYBRID2']
            # get weight under pb 
            results['GW_GLUE_PB'] = results['GW_MODULE_PB'] - results['GW_SENSOR'] - results['GW_PB']
        # case 3
        elif (mod_w_hyb1.get() != '') and (mod_w_hyb1_pb.get() != '') and (mod_w_pb.get() == ''):    
            # get weight under first hybrid 
            results['GW_GLUE_H1'] = results['GW_MODULE_H1'] - results['GW_SENSOR'] - results['GW_HYBRID1']
            # get weight under second hybrid 
            results['GW_GLUE_H2'] = results['GW_MODULE_H1H2PB'] - results['GW_MODULE_H1PB'] - results['GW_HYBRID2']
            # get weight under pb 
            results['GW_GLUE_PB'] = results['GW_MODULE_H1PB'] - results['GW_MODULE_H1'] - results['GW_PB'] 
        else: 
            print("Not enough values provided to calculate glue weight under each component.")        

        results['GW_GLUE_H1H2'] = results['GW_GLUE_H1'] + results['GW_GLUE_H2']
        results['GW_GLUE_H1H2PB'] = results['GW_GLUE_H1'] + results['GW_GLUE_H2'] + results['GW_GLUE_PB']

        print("Glue weight under hybrid 1: {0}".format(results['GW_GLUE_H1']))   
        print("Glue weight under hybrid 2: {0}".format(results['GW_GLUE_H2']))  
        print("Glue weight under powerboard: {0}".format(results['GW_GLUE_PB']))  
        under_hyb1_box.insert(0, f"{results['GW_GLUE_H1']:0.4f}")
        under_hyb2_box.insert(0, f"{results['GW_GLUE_H2']:0.4f}")
        under_hyb1_hyb2_box.insert(0, f"{results['GW_GLUE_H1H2']:0.4f}")
        under_pb_box.insert(0, f"{results['GW_GLUE_PB']:0.4f}")
        under_hyb1_pb_box.insert(0, f"{results['GW_GLUE_H1PB']:0.4f}")
        under_hyb1_hyb2_pb_box.insert(0, f"{results['GW_GLUE_H1H2PB']:0.4f}")

        results['GW_GLUE_H1'] = round(results['GW_GLUE_H1'], 4)
        results['GW_GLUE_H2'] = round(results['GW_GLUE_H2'], 4)
        results['GW_GLUE_H1H2'] = round(results['GW_GLUE_H1H2'], 4)
        results['GW_GLUE_H1PB'] = round(results['GW_GLUE_H1PB'], 4)
        results['GW_GLUE_H1H2PB'] = round(results['GW_GLUE_H1H2PB'], 4)
        results['GW_GLUE_PB'] = round(results['GW_GLUE_PB'], 4)

    # R2, 4R, 5R:
    # case 1: glue hybrid first
    # case 2: glue pb first
    if module_type in ['M2', '4R', '5R']:
        print(mod_w_hyb1.get())
        print(mod_w_pb.get())
        if (mod_w_hyb1.get() != '') and (mod_w_pb.get() == ''):
            # get module under hybrid 1
            results['GW_GLUE_H1'] = results['GW_MODULE_H1'] - results['GW_SENSOR'] - results['GW_HYBRID1']
            # get module under pb
            results['GW_GLUE_PB'] = results['GW_MODULE_H1PB'] - results['GW_MODULE_H1'] - results['GW_PB']
        if (mod_w_pb.get() != '') and (mod_w_hyb1.get() == ''):
            # get module under hybrid 1
            results['GW_GLUE_H1'] = results['GW_MODULE_H1PB'] - results['GW_MODULE_PB'] - results['GW_HYBRID1']
            # get module under pb
            results['GW_GLUE_PB'] = results['GW_MODULE_PB'] - results['GW_SENSOR'] - results['GW_PB']   

        results['GW_GLUE_H1PB'] = results['GW_GLUE_H1'] + results['GW_GLUE_PB']

        print("Glue weight under hybrid 1: {0}".format(results['GW_GLUE_H1']))   
        print("Glue weight under powerboard: {0}".format(results['GW_GLUE_PB']))  
        under_hyb1_box.insert(0, f"{results['GW_GLUE_H1']:0.4f}")
        under_pb_box.insert(0, f"{results['GW_GLUE_PB']:0.4f}")
        under_hyb1_pb_box.insert(0, f"{results['GW_GLUE_H1PB']:0.4f}")

        results['GW_GLUE_H1'] = round(results['GW_GLUE_H1'], 4)
        results['GW_GLUE_PB'] = round(results['GW_GLUE_PB'], 4)
        results['GW_GLUE_H1PB'] = round(results['GW_GLUE_H1PB'], 4)


    if module_type in ['3L']: 
    # case 1: glue 1 hybrid then other 
        results['GW_GLUE_H1'] = results['GW_MODULE_H1'] - results['GW_SENSOR'] - results['GW_HYBRID1']
        results['GW_GLUE_H2'] = results['GW_MODULE_H1H2'] - results['GW_MODULE_H1'] - results['GW_HYBRID2']

        results['GW_GLUE_H1H2'] = results['GW_GLUE_H1'] + results['GW_GLUE_H2']

        print("Glue weight under hybrid 1: {0}".format(results['GW_GLUE_H1']))   
        print("Glue weight under hybrid 2: {0}".format(results['GW_GLUE_H2']))  
        under_hyb1_box.insert(0, f"{results['GW_GLUE_H1']:0.4f}")
        under_hyb2_box.insert(0, f"{results['GW_GLUE_H2']:0.4f}")
        under_hyb1_hyb2_box.insert(0, f"{results['GW_GLUE_H1H2']:0.4f}")

        results['GW_GLUE_H1'] = round(results['GW_GLUE_H1'], 4)
        results['GW_GLUE_H2'] = round(results['GW_GLUE_H2'], 4)
        results['GW_GLUE_H1H2'] = round(results['GW_GLUE_H1H2'], 4)
    
    if module_type in ['4L', '5L']: 
    # case 1: glue 1 hybrid
        results['GW_GLUE_H1'] = results['GW_MODULE_H1'] - results['GW_SENSOR'] - results['GW_HYBRID1']

        print("Glue weight under hybrid 1: {0}".format(results['GW_GLUE_H1']))   
        under_hyb1_box.insert(0, f"{results['GW_GLUE_H1']:0.4f}")

        results['GW_GLUE_H1'] = round(results['GW_GLUE_H1'], 4)

    DATA_DICT['passed'] = assess_passed(module_type)
    DATA_DICT['results'] = results

# assess if glue weights pass
# using TrueBlue 120um thickness to evalute
def assess_passed(mod_type): 
    output = 'Glue weights calculated: '
    passed = False

    # check hybrid 1 glue weight - for modules with multiple hybrids - assuming that H0 is glued first for M0, M1 and 3R, and H1 is glued first on 3L
    if mod_type in ['M0', 'M1', 'M2', '3R', '4R', '5R']: 
        lower_lim = H0_glue_limit_dict[mod_type][0]*10000
        upper_lim = H0_glue_limit_dict[mod_type][1]*10000
        hyb1_glue_check = lower_lim <= (results['GW_GLUE_H1']*10000) <= upper_lim
        print(hyb1_glue_check)
    elif mod_type in ['3L', '4L', '5L']:
        lower_lim = H1_glue_limit_dict[mod_type][0]*10000
        print(lower_lim)
        upper_lim = H1_glue_limit_dict[mod_type][1]*10000
        print(upper_lim)
        hyb1_glue_check = lower_lim <= (results['GW_GLUE_H1']*10000) <= upper_lim 
        print(hyb1_glue_check)
    else: 
        hyb1_glue_check = False
        output += "Cannot evaluate glue under hybrid 1. Double check values entered. "

    if hyb1_glue_check:
        pass
    else: 
        output += "Glue under hybrid 1 fails. "       

    # check hybrid 2 glue weight - for modules with multiple hybrids - assuming that H0 is glued first for M0, M1 and 3R, and H1 is glued first on 3L
    # only checking half-modules with 2 hybrids - M0, M1, 3R, 3L
    if mod_type in ['M0', 'M1']: 
        lower_lim = H1_glue_limit_dict[mod_type][0]*10000
        upper_lim = H1_glue_limit_dict[mod_type][1]*10000
        hyb2_glue_check = lower_lim <= (results['GW_GLUE_H2']*10000) <= upper_lim
    elif mod_type in ['3R']: 
        lower_lim = H2_glue_limit_dict[mod_type][0]*10000
        upper_lim = H2_glue_limit_dict[mod_type][1]*10000
        hyb2_glue_check = lower_lim <= (results['GW_GLUE_H2']*10000) <= upper_lim 
    elif mod_type in ['3L']:
        lower_lim = H3_glue_limit_dict[mod_type][0]*10000
        upper_lim = H3_glue_limit_dict[mod_type][1]*10000
        hyb2_glue_check = lower_lim <= (results['GW_GLUE_H2']*10000) <= upper_lim     
    else: 
        hyb2_glue_check = True

    if hyb2_glue_check  == True:
        pass
    else: 
        output += "Glue under hybrid 2 fails. "    

        # output_text.set("Cannot evaluate glue under hybrid 2 - module type detected from SN does not have a second hybrid.")    

    # check hybrid 2 glue weight - for modules with multiple hybrids - assuming that H0 is glued first for M0, M1 and 3R, and H1 is glued first on 3L
    # only checking half-modules with 2 hybrids - M0, M1, 3R, 3L
    if mod_type in ['M0', 'M1', 'M2', '3R', '4R', '5R']: 
        lower_lim = PB_glue_limit_dict[mod_type][0]*10000
        upper_lim = PB_glue_limit_dict[mod_type][1]*10000
        pb_glue_check = lower_lim <= (results['GW_GLUE_PB']*10000) <= upper_lim
    else: 
        pb_glue_check = True   
        # output_text.set("Cannot evaluate glue under PB - module type detected from SN does not have a PB.")    

    if pb_glue_check == True:
        pass 
    else: 
        output += "Glue under PB fails. "   

    if all([hyb1_glue_check, hyb2_glue_check, pb_glue_check]):
        output += "All glue weights pass!"
    output_text.set(output)
    
    return all([hyb1_glue_check, hyb2_glue_check, pb_glue_check])
    


def save_data():
    """Saves the data to the database"""

    if serial_number.get() == "" or run_num.get() == "" or problems_box.curselection() == () or DATA_DICT == {}:
        output_text.set('Please ensure all mandatory values have been enteredn. Then try again.')
        return 
    else:
        if problems_box.get(problems_box.curselection()[0]) == "Yes":
             DATA_DICT["problems"]  = True
        else: 
            DATA_DICT["problems"] = False

    if retroactive_box.curselection() == () or DATA_DICT == {}:
        output_text.set('Please ensure all mandatory values have been entered. Then try again.')
        return 
    else:
        if retroactive_box.get(retroactive_box.curselection()[0]) == "GLUED":
            DATA_DICT["isRetroactive"] = True
            DATA_DICT["stage"] = "GLUED"
        else: 
            DATA_DICT["isRetroactive"] = False        

        
    DATA_DICT["component"] = serial_number.get()
    DATA_DICT["runNumber"] = run_num.get()

    db_passcode_1 =  db_pass_1.get()
    db_passcode_2 =  db_pass_2.get()

    try :
        user = itkdb.core.User(access_code1 = db_passcode_1, access_code2 = db_passcode_2)
        client = itkdb.Client(user=user)
    except:
        output_text.set("Set passcodes are incorrect. Try again.")
        return
    
    print("got passed client init!")

    result= client.post("uploadTestRunResults", json = DATA_DICT)

    if (('uuAppErrorMap')=={}):
        output_text.set('Upload of Test and File Succesful!')
    elif (('uuAppErrorMap'))[0]=='cern-itkpd-main/uploadTestRunResults/':
        output_text.set("Error in Test Upload.")
    elif list(('uuAppErrorMap'))[0]=='cern-itkpd-main/uploadTestRunResults/componentAtDifferentLocation':
        output_text.set('Component cannot be uploaded as is not currently at the given location')
    elif (('uuAppErrorMap'))[0]=='cern-itkpd-main/uploadTestRunResults/unassociatedStageWithTestType':
        output_text.set('Component cannot be uploaded as the current stage does not have this test type. You will need to update the stage of the component on the ITK DB. Note that due to a bug on the ITK DB, you might also get this error if the component is not at your current location.')
    elif (('uuAppErrorMap'))[0]!='cern-itkpd-main/uploadTestRunResults/':
        output_text.set("Upload of test successful!")
    else:
        output_text.set('Error!')

    DATA_DICT.clear()
    results.clear()    

# GUI Definition
root = tk.Tk()
frame = tk.Frame(root, height = 700, width = 800)
frame.pack()

#Define String Variables of GUI
serial_number = tk.StringVar()
module_type = tk.StringVar()
stencil_hyb1 = tk.StringVar()
stencil_hyb2 = tk.StringVar()
stencil_pb = tk.StringVar()
output_text = tk.StringVar()
run_num = tk.StringVar()

bare_sensor = tk.StringVar()
under_hyb2 = tk.StringVar()
hyb1 = tk.StringVar()
under_pb = tk.StringVar()
hyb2 = tk.StringVar()
under_hyb1 = tk.StringVar()
mod_w_hyb1_hyb2 = tk.StringVar()
under_hyb1_hyb2 = tk.StringVar()
mod_w_pb = tk.StringVar()
pb = tk.StringVar()
mod_w_hyb1_pb = tk.StringVar()
under_hyb1_pb = tk.StringVar()
total_mod = tk.StringVar()
under_hyb1_hyb2 = tk.StringVar()
mod_w_hyb1 = tk.StringVar()
under_hyb1_hyb2_pb = tk.StringVar()


db_pass_1 = tk.StringVar()
db_pass_2 = tk.StringVar()

#Define the boxes to contain the string variables.
title = tk.Label(frame, text = 'Module Glue Weight Upload GUI', font = ('calibri', 18))
title.place(x = 250, y = 10 )

# Authentication related
db_pass_1_label = tk.Label(frame, text="Access Code 1:")
db_pass_1_label.place(x = ENTRY_X + 400 , y = ENTRY_Y + 440)
db_pass_1_box = tk.Entry(frame, textvariable = db_pass_1, show='*', justify = 'left', width = 15, highlightthickness=2, highlightbackground="blue")
db_pass_1_box.place(x = ENTRY_X + 500, y = ENTRY_Y + 440)

db_pass_2_label = tk.Label(frame, text="Access Code 2:")
db_pass_2_label.place(x = ENTRY_X + 400, y = ENTRY_Y + 470)
db_pass_2_box = tk.Entry(frame, textvariable = db_pass_2, show='*',  justify = 'left', width = 15, highlightthickness=2, highlightbackground="blue")
db_pass_2_box.place(x = ENTRY_X + 500, y = ENTRY_Y + 470)

# Upload related
problems_label = tk.Label(frame, text='Problems?')
problems_label.place(x = ENTRY_X + 400, y = ENTRY_Y + 360)
problems_box = tk.Listbox(frame, width = 5, relief = 'groove', height = '2')
problems_box.place(x = ENTRY_X + 400, y = ENTRY_Y + 380)
problems_box.insert(0,"Yes")
problems_box.insert(1,"No")

serial_number_label = tk.Label(frame, text="Serial Number:")
serial_number_label.place(x = ENTRY_X - 50 , y = ENTRY_Y + 70)
serial_number_box = tk.Entry(frame, textvariable = serial_number,  justify = 'left', width = 20, highlightthickness=2, highlightbackground="yellow")
serial_number_box.place(x = ENTRY_X + 45, y = ENTRY_Y + 70)

run_label = tk.Label(frame, text="Run Number:")
run_label.place(x = ENTRY_X - 45 , y = ENTRY_Y + 100)
run_box = tk.Entry(frame, textvariable = run_num,  justify = 'left', width = 20, highlightthickness=2, highlightbackground="yellow")
run_box.place(x = ENTRY_X + 45, y = ENTRY_Y + 100)

retroactive_label = tk.Label(frame, text='Retroactive Upload?')
retroactive_label.place(x = ENTRY_X + 500, y = ENTRY_Y + 360)
retroactive_box = tk.Listbox(frame, width = 20, relief = 'groove', height = '2', exportselection=0)
retroactive_box.place(x = ENTRY_X + 500, y = ENTRY_Y + 380)
retroactive_box.insert(0,"No")
retroactive_box.insert(1,"GLUED")

'''
module_label = tk.Label(frame, text='Module Type:')
module_label.place(x = ENTRY_X - 75, y = ENTRY_Y + 150)
module_box = tk.Listbox(frame, width = 20, relief = 'groove', height = '6')
module_box.place(x = ENTRY_X + 45, y = ENTRY_Y + 150)
module_box.insert(1,"R1")
module_box.insert(2,"R2")
module_box.insert(5,"R4M0_HALFMODULE")
module_box.insert(6,"R4M1_HALFMODULE")
module_box.insert(7,"R5M0_HALFMODULE")
module_box.insert(8,"R5M1_HALFMODULE")
'''

hyb1_stencil_label = tk.Label(frame, text="Hybrid 1 Stencil:")
hyb1_stencil_label.place(x = ENTRY_X - 55 , y = ENTRY_Y + 130)
hyb1_stencil_box = tk.Entry(frame, textvariable = stencil_hyb1,  justify = 'left', width = 20, highlightthickness=2, highlightbackground="yellow")
hyb1_stencil_box.place(x = ENTRY_X + 45, y = ENTRY_Y + 130)

hyb2_stencil_label = tk.Label(frame, text="Hybrid 2 Stencil:")
hyb2_stencil_label.place(x = ENTRY_X - 55, y = ENTRY_Y + 160)
hyb2_stencil_box = tk.Entry(frame, textvariable = stencil_hyb2,  justify = 'left', width = 20, highlightthickness=2, highlightbackground="yellow")
hyb2_stencil_box.place(x = ENTRY_X + 45, y = ENTRY_Y + 160)



pb_stencil_label = tk.Label(frame, text="Powerboard Stencil:")
pb_stencil_label.place(x = ENTRY_X - 75, y = ENTRY_Y + 190)
pb_stencil_box = tk.Entry(frame, textvariable = stencil_pb,  justify = 'left', width = 20, highlightthickness=2, highlightbackground="yellow")
pb_stencil_box.place(x = ENTRY_X + 45, y = ENTRY_Y + 190)  

### ONES TO ENTER
bare_sensor_label = tk.Label(frame, text="Bare Sensor:")
bare_sensor_label.place(x = ENTRY_X + 200, y = ENTRY_Y + 50)
bare_sensor_box = tk.Entry(frame, textvariable = bare_sensor,  justify = 'left', width = 20, highlightthickness=2, highlightbackground="yellow")
bare_sensor_box.place(x = ENTRY_X + 200, y = ENTRY_Y + 70)

hyb1_label = tk.Label(frame, text="Weight of Hybrid 1:")
hyb1_label.place(x = ENTRY_X + 200, y = ENTRY_Y + 100)
hyb1_box = tk.Entry(frame, textvariable = hyb1,  justify = 'left', width = 20, highlightthickness=2, highlightbackground="yellow")
hyb1_box.place(x = ENTRY_X + 200, y = ENTRY_Y + 120)

hyb2_label = tk.Label(frame, text="Weight of Hybrid 2:")
hyb2_label.place(x = ENTRY_X + 200, y = ENTRY_Y + 150)
hyb2_box = tk.Entry(frame, textvariable = hyb2,  justify = 'left', width = 20, highlightthickness=2, highlightbackground="yellow")
hyb2_box.place(x = ENTRY_X + 200, y = ENTRY_Y + 170)

pb_label = tk.Label(frame, text="Weight of Powerboard:")
pb_label.place(x = ENTRY_X + 200, y = ENTRY_Y + 200)
pb_box = tk.Entry(frame, textvariable = pb,  justify = 'left', width = 20, highlightthickness=2, highlightbackground="yellow")
pb_box.place(x = ENTRY_X + 200, y = ENTRY_Y + 220)


mod_w_hyb1_label = tk.Label(frame, text="Module with 1 hybrid:")
mod_w_hyb1_label.place(x = ENTRY_X + 400, y = ENTRY_Y + 50)
mod_w_hyb1_box = tk.Entry(frame, textvariable = mod_w_hyb1,  justify = 'left', width = 20, highlightthickness=2, highlightbackground="yellow")
mod_w_hyb1_box.place(x = ENTRY_X + 400, y = ENTRY_Y + 70)

mod_w_pb_label = tk.Label(frame, text="Module with PB:")
mod_w_pb_label.place(x = ENTRY_X + 400, y = ENTRY_Y + 100)
mod_w_pb_box = tk.Entry(frame, textvariable = mod_w_pb,  justify = 'left', width = 20, highlightthickness=2, highlightbackground="yellow")
mod_w_pb_box.place(x = ENTRY_X + 400, y = ENTRY_Y + 120)

mod_w_hyb1_pb_label = tk.Label(frame, text="Module with 1 hybrid and PB:")
mod_w_hyb1_pb_label.place(x = ENTRY_X + 400, y = ENTRY_Y + 150)
mod_w_hyb1_pb_box = tk.Entry(frame, textvariable = mod_w_hyb1_pb,  justify = 'left', width = 20, highlightthickness=2, highlightbackground="yellow")
mod_w_hyb1_pb_box.place(x = ENTRY_X + 400, y = ENTRY_Y + 170)

mod_w_hyb1_hyb2_label = tk.Label(frame, text="Module with 2 hybrids:")
mod_w_hyb1_hyb2_label.place(x = ENTRY_X + 400, y = ENTRY_Y + 200)
mod_w_hyb1_hyb2r_box = tk.Entry(frame, textvariable = mod_w_hyb1_hyb2,  justify = 'left', width = 20, highlightthickness=2, highlightbackground="yellow")
mod_w_hyb1_hyb2r_box.place(x = ENTRY_X + 400, y = ENTRY_Y + 220)

total_mod_label = tk.Label(frame, text="Module with 2 hybrids and PB:")
total_mod_label.place(x = ENTRY_X + 400, y = ENTRY_Y + 250)
total_mod_box = tk.Entry(frame, textvariable = total_mod,  justify = 'left', width = 20, highlightthickness=2, highlightbackground="yellow")
total_mod_box.place(x = ENTRY_X + 400, y = ENTRY_Y + 270)

calc_button = tk.Button(frame, text = "Calculate", command = lambda: calculate_glue_weights())
calc_button.place(x = ENTRY_X + 300, y = ENTRY_Y + 310)

###


under_hyb1_label = tk.Label(frame, text="Glue Weight under Hybrid 1:")
under_hyb1_label.place(x = ENTRY_X - 75, y = ENTRY_Y + 360)
under_hyb1_box = tk.Entry(frame, textvariable = under_hyb1,  justify = 'left', width = 20)
under_hyb1_box.place(x = ENTRY_X - 75, y = ENTRY_Y + 380)
# under_hyb1.insert('1.0', DATA_DICT["GW_GLUE_H1"])

under_hyb2_label = tk.Label(frame, text="Glue Weight under Hybrid 2:")
under_hyb2_label.place(x = ENTRY_X - 75, y = ENTRY_Y + 410)
under_hyb2_box = tk.Entry(frame, textvariable = under_hyb2,  justify = 'left', width = 20)
under_hyb2_box.place(x = ENTRY_X - 75, y = ENTRY_Y + 430)
# under_hyb2.insert('1.0', DATA_DICT["GW_GLUE_H2"])

under_pb_label = tk.Label(frame, text="Glue Weight under PB:")
under_pb_label.place(x = ENTRY_X - 75, y = ENTRY_Y + 460)
under_pb_box = tk.Entry(frame, textvariable = under_pb,  justify = 'left', width = 20)
under_pb_box.place(x = ENTRY_X - 75, y = ENTRY_Y + 480)
# under_pb.insert('1.0', DATA_DICT["GW_GLUE_PB"])

under_hyb1_hyb2_label = tk.Label(frame, text="Glue weight under 2 hybrids:")
under_hyb1_hyb2_label.place(x = ENTRY_X + 150, y = ENTRY_Y + 360)
under_hyb1_hyb2_box = tk.Entry(frame, textvariable = under_hyb1_hyb2,  justify = 'left', width = 20)
under_hyb1_hyb2_box.place(x = ENTRY_X + 150, y = ENTRY_Y + 380)

under_hyb1_pb_label = tk.Label(frame, text="Glue weight under 1 hybrid and PB:")
under_hyb1_pb_label.place(x = ENTRY_X + 150, y = ENTRY_Y + 410)
under_hyb1_pb_box = tk.Entry(frame, textvariable = under_hyb1_pb,  justify = 'left', width = 20)
under_hyb1_pb_box.place(x = ENTRY_X + 150, y = ENTRY_Y + 430)

under_hyb1_hyb2_pb_label = tk.Label(frame, text="Glue weight under 2 hybrids and PB:")
under_hyb1_hyb2_pb_label.place(x = ENTRY_X + 150, y = ENTRY_Y + 460)
under_hyb1_hyb2_pb_box = tk.Entry(frame, textvariable = under_hyb1_hyb2_pb,  justify = 'left', width = 20)
under_hyb1_hyb2_pb_box.place(x = ENTRY_X + 150, y = ENTRY_Y + 480)
 

save_button = tk.Button(frame, text = "Save Data", command = lambda: save_data())
save_button.place(x = ENTRY_X + 500, y = ENTRY_Y + 520)

output_text_box = tk.Message(frame, textvariable = output_text, font = ('calibri', 10), width = 350, relief = 'sunken', justify = 'left')
output_text_box.place(x = ENTRY_X + -40, y = ENTRY_Y + 520)
output_text.set('Enter all values highlighted in yellow. Press "Calculate" button to calculate glue weights (assuming TrueBlue). To upload test to database, enter Access Codes and then press "Save Data".')

root.mainloop()

