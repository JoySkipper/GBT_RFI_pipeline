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
The GBT RFI Pipeline requires one argument: The location of the raw GBT RFI data you are in possession of

However, there are several optional arguments controlled by several flags:

1.) -output_directory : Specifies the output directory to which you'd like to put the .txt files. Defaults to the current directory if output directory is not specified. 

2.) --skipalreadyprocessed : Decides if you'd like to specify a directory of files that you would like to be ignored, or that have already been processed. If you provide this flag, you will need to give the processed_path argument, which is the path containing those files you'd like to be ignored, just after this flag. 

Optionally, you can simply put 'output_directory' as the processed_path argument, and it will choose the same directory given by the output_directory flag. 

If you place any of the text files into the path of this argument, the pipeline will automatically detect already processed data and skip them upon the next reduction.

3.) --upload_to_database decides if you'd like to upload the produced data to an SQL database. If this is selected, you will need to provide 4 arguments:
    
    a.) host_name: the host name of the machine that the SQL database that you would like to upload your data to lives on
    
    b.) database_name: the name of that SQL database that you would like to upload your data to
    
    c.) main_table: the table to which you would like all clean, unflagged data to be uploaded
    
    d.) dirty_table: the table to which you'd like all flagged data to be uploaded


## Simplest working example:

```console
python process_new_RFI_files.py </path/to/raw/RFI/data/to/process>
```

Output results will be dumped into your current directory for this setup. Ensure you have write permissions to your current working directory

This pipeline generates four (4) .gif images of varying zoom levels and an ASCII text file containing reduced RFI intensity values vs. frequency values and corresponding header information.

## Recommended method example: 

```console
python process_new_RFI_files.py '</path/to/raw/RFI/data/to/process>' -output_directory '</path/to/output/directory>' -skipalreadyprocessed 'output_directory' --upload_to_database -host_name <my_host_name> -database_name <my_database_name> -main_table <my_main_table> -bad_table <my_bad_data_table>
```

Output results will be dumped to the specified directory for this setup. Ensure you have write permissions to your current working directory. 

This example generates a .txt file containing the reduced data, dumps it to the output directory, as well as loads that same data into the specified SQL database. 

## Citations: 

This repository includes rfiDisplay_wilsonedit.pro and scalUtils_wilsonedit.pro, which are modified forms of scripts rfiDisplay.pro and scalUtils.pro. These original scripts were written by Ron Maddalena at Green Bank Observatory (rmaddale@nrao.edu). He is now an emeritus senior scientist at the observatory, and no longer maintains these scripts. Due to this, any questions regarding these scripts should be directed towards Joy Skipper (jskipper@nrao.edu).