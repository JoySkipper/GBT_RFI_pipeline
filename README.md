# GBT_RFI_pipeline
Pipeline for reducing and extracting useful information from the Green Bank Telescope RFI scans 

## Installation Requirements
* Python 3.5+ (setup.py coming soon!)
    * NumPy
    * Pandas
* GBTIDL v2.10.1 (http://gbtidl.nrao.edu/)
* GBT_RFI_Analysis_Tool (https://github.com/JoySkipper/GBT_RFI_Analysis_Tool)
* gifclip (http://giflib.sourceforge.net/gifclip.html)
  * Users who are not interested in producing .gif images may elect not to install gifclip.

## Prerequisites
* You should be in possession of RFI data from the Green Bank Telescope in SDFITS format.

## How to run the Pipeline
The GBT RFI Pipeline requires one argument: (1) Location of the raw GBT RFI data you are in possession of

However, there are several optional arguments controlled by two flags: 
1.)  --skipalreadyprocessed decides if you'd like to specify a directory of files that you would like to be ignored, or that have already been processed. If you provide this flag, you will need to give the processed_path argument, which is the path containing those files you'd like to be ignored, just after this flag.

If you place any of the text files into the path of this argument, the pipeline will automatically detect already processed data and skip them upon the next reduction.

2.) --upload_to_database decides if you'd like to upload the produced data to an SQL database. If this is selected, you will need to provide 4 arguments:
    
    a.) IP_address: the IP address of the SQL database that you would like to upload your data to
    
    b.) database_name: the name of that SQL database that you would like to upload your data to
    
    c.) main_table: the table to which you would like all clean, unflagged data to be uploaded
    
    d.) dirty_table: the table to which you'd like all flagged data to be uploaded

```console
python process_new_RFI_files.py </path/to/raw/RFI/data/to/process>
```

Output results will be dumped into your current directory. Ensure you have write permissions to your current working directory

This pipeline generates four (4) .gif images of varying zoom levels and an ASCII text file containing reduced RFI intensity values vs. frequency values and corresponding header information.

