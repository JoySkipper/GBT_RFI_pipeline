# GBT_RFI_pipeline. 
Pipeline for reducing and extracting useful information from the Green Bank Telescope RFI scans 

## Installations required

### 1.

Currently, before running this script, you will need to download the "gifclip" bash command (http://giflib.sourceforge.net/gifclip.html) before being able to run it and have the .gif files produced to not be empty. Otherwise, if you are solely interested in the .txt files produced, installing gifclip is not necessary. 

#### Note: The need for the gifclip installation is in the works to be phased out in version 1.0 of GBT_RFI_Pipeline. 

### 2. 

You will also need to clone/download the GBT_RFI_Analysis_Tool (https://github.com/JoySkipper/GBT_RFI_Analysis_Tool) in order to import the functionality of rfitrends/GBT_receiver_specs.py. 

#### Note: GBT_RFI_Analysis_Tool will be merged as a new module into GBT_RFI_Pipeline in version 1.0. 

## How the Code Works

The crux of this package is that it relies on a GBTIDL processing script called rfiscans_mod, written by a different author. In the future, it's hoped in version 1.0 of this package that rfiscans_mod will be truncated in place of code that is more robust. However, for now, this package primarily gleans the data necessary for calling rfiscans_mod and then calls it for each file. 

### First script: Process_new_RFI_files.py

The first thing that's called is process_new_RFI_files.py using path_to_current_RFI_files and path_to_processed_RFI_files as the two in-line arguments. 

Process_new_RFI_files.py starts with using the determine_new_RFI_files function. This function looks at the path_to_processed_RFI_files, which is assumed to have all RFI files that have been processed so far, and compares it to the path_to_current_RFI_files to determine which of those current RFI files in that directory still need to be processed. Determine_new_RFI_files then returns a list containing those RFI files that need to be processed. 

Next, process_new_RFI_files.py calls find_parameters_to_process_file. This looks into each of these files that needs to be processed, opens up the .index file, and gleans information that's necessary to run the rfiscans_mod function that processes GBT RFI files. It then returns a list of lists with that data. 

After this, process_new_RFI_files.py writes the data that was output by find_parameters_to_process_file and writes it to a csv called RFI_file_parameters.csv. 

Finally, process_new_RFI_files calls automation_of_processing.pro, which is an IDL script that then handles the parameters necessary to run rfiscans_mod and runs it. 

### Second script: automation_of_processing.pro

Automation_of_processing.pro first reads in the data output by process_new_RFI_files.py, "RFI_file_parameters.csv." 

Next, the script deals with the ymax value. The ymax value is input needed for the rfiscans_mod script. It is determined by the receiver. Some receivers have a ymax of 10, and some have a ymax of 100. This value is simply the maximum y value shown in the .gif images. The script then makes a list of the receivers that need ymax of 100 and those that need a ymax of 10. 

Next, the script goes to read, line by line, the RFI_file_parameters.csv that has the necessary information to run rfiscans_mod for each file. It first pulls that information and gives them more reasonable name. 

It then takes the number of scans, given by the .csv file, and creates a list of those scans in ascending order so that it can be the proper input for the rfiscans_mod. For example, if there are 3 scans, it makes a list such as [1,2,3]. 

### Note: We are able to use all scans because rfiscans_mod cannot handle bad scans or skip over them. In version 1.0 of this package, the script will not automatically use all scans but instead skip over those bad scans as well. Currently, it throws out any files that contain any bad scans. 

After this, the script calculates the ymax value for the given file, by comparing the receiver name and seeing if it is in the ymax100 list or the ymax10 list that was created earlier. 

Finally, the script starts using GBTIDL proper. It loads in the current file into GBTIDL, then calls rfiscans_mod at 4 different zoom levels. It also checks if the receiver is the Ka receiver, and adds the appropriate /ka flag necessary in rfiscans_mod for files that use the Ka receiver. 