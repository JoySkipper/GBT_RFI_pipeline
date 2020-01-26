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
The GBT RFI Pipeline requires two arguments: (1) Location of the raw GBT RFI data you are in possession of, and (2) Directory of previous pipeline outputs to ignore.

```console
python process_new_RFI_files.py </path/to/raw/RFI/data/to/process> </path/of/raw/RFI/data/to/ignore> 
```

Output results will be dumped into your current directory. Ensure you have write permissions to your current working directory

This pipeline generates four (4) .gif images of varying zoom levels and an ASCII text file containing reduced RFI intensity values (?) and corresponding header information.

If you place any of the text files into the path of the second argument, the pipeline will automatically detect already processed data and skip them upon the next reduction.