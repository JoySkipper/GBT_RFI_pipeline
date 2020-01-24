# GBT_RFI_pipeline
Pipeline for reducing and extracting useful information from the Green Bank Telescope RFI scans 

## Installations required

Currently, before running this script, you will need to download the "gifclip" bash command (http://giflib.sourceforge.net/gifclip.html) before being able to run it and have the .gif files produced to not be empty. Otherwise, if you are solely interested in the .txt files produced, installing gifclip is not necessary. 

You will also need to clone/download the GBT_RFI_Analysis_Tool (https://github.com/JoySkipper/GBT_RFI_Analysis_Tool) in order to import the functionality of rfitrends/GBT_receiver_specs.py. 

## How to Run the Script

To run the script, you need to run:

```console
process_new_RFI_files.py <path_to_current_RFI_files> <path_to_processed_RFI_files> 
```

Run this within the directory in which you'd like your processed RFI data to be dumped. Therefore, you need write permissions in your current directory to run this code. 

The first is the path to a directory containing, but not necessarily exclusively containing, new RFI data that you wish to be processed. Again, this directory can also contain already processed data. 

The second is the path to a directory containing all data that has already been processed, or that you wish to not be processed for any reason. This will be used to compare against the first argument to determine what needs to be processed. 

The script will then run and dump one .txt and 4 .gif files for each processed RFI file. The .txt file contains the processed RFI data and header information, while the 4 .gif files contain still images of the spectrum at 4 different zoom levels. 

