# GBT_RFI_pipeline
Pipeline for reducing and extracting useful information from the Green Bank Telescope RFI scans 

## Installation Requirements
* Python 3.5+
* GBTIDL v2.10.1 (http://gbtidl.nrao.edu/) - installed on all GBO machines
* MySQL (www.mysql.com) - installed on all GBO machines
* gifclip (http://giflib.sourceforge.net/gifclip.html)
  * Users who are not interested in producing .gif images may elect not to install gifclip.

## Installation Instructions

Once obtaining all the requirements, simply type this in the terminal in your desired environment:

```console
pip install git+https://github.com/JoySkipper/GBT_RFI_pipeline.git
```

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
    
    a.) host_name: the host name of the machine containing the SQL database that you would like to upload your data to
    
    b.) database_name: the name of that SQL database that you would like to upload your data to
    
    c.) main_table: the table to which you would like all clean, unflagged data to be uploaded
    
    d.) dirty_table: the table to which you'd like all flagged data to be uploaded


## Simplest working example:

```console
processgbtrfi </path/to/raw/RFI/data/to/process>
```

Output results will be dumped into your current directory for this setup. Ensure you have write permissions to your current working directory

This pipeline generates an ASCII text file containing reduced RFI intensity values vs. frequency values and corresponding header information.

## Recommended method example: 

```console
processgbtrfi '</path/to/raw/RFI/data/to/process>' -output_directory '</path/to/output/directory>' -skipalreadyprocessed 'output_directory' --upload_to_database -host_name <my_host_name> -database_name <my_database_name> -main_table <my_main_table> -bad_table <my_bad_data_table>
```

Output results will be dumped to the specified directory for this setup. Ensure you have write permissions to the specified directory. 

This example generates a .txt file containing the reduced data, dumps it to the output directory, as well as loads that same data into the specified SQL database. 

## How do I know it's working correctly? What output and feedback should I expect? 

There are several stages of this script.

If you are uploading to a database, it will first ask for the credentials to access the database. Then it will move on to the various stages of processing:

### Stage 1: 

You will see output of parameter data gleaned. It will look something like this: 

```console
TRFI_040520_C1 parameter data gleaned
TRFI_040420_C1 parameter data gleaned
TRFI_040420_S1 parameter data gleaned
TRFI_040320_K1 parameter data gleaned
TRFI_040220_C1 parameter data gleaned
TRFI_040220_81 parameter data gleaned
TRFI_040520_S2 parameter data gleaned
TRFI_040220_S2 parameter data gleaned
TRFI_040220_L1 parameter data gleaned
TRFI_040520_C2 parameter data gleaned
TRFI_040320_81 parameter data gleaned
TRFI_040520_81 parameter data gleaned
TRFI_040220_S1 parameter data gleaned
TRFI_040420_81 parameter data gleaned
```

These are all the files to be processed during stage 2. It shows that the metadata necessary to process the files was successfully gleaned from the files. 

### Stage 2:

Afterwards, IDL sessions will pop up and be exited out as the script processes each RFI file. It will print that the file has been written correctly if this is the case. Here is an example of the kind of output you will see: 

```console
processing file: TRFI_040520_C1
Running in process 24297
/home/apps/itt/idl71/bin/bin.linux.x86_64/idl: /opt/local/lib/libuuid.so.1: no version information available (required by /lib64/libSM.so.6)
IDL Version 7.1.1 (linux x86_64 m64). (c) 2009, ITT Visual Information Solutions
Installation number: 15269-3.
Licensed for use by: National Radio Astronomy Observatory

Starting GBTIDL

Display Device  : X
Visual Class    : TrueColor
Visual Depth    : 24-Bit
Color Table Size: 256
Number of Colors: 16777216
Decomposed Color: 0

--------------------------------------------------------------------
                    Welcome to GBTIDL v2.10.1

    For news, documentation, enhancement requests, bug tracking,
               discussion, and contributions, visit:

                   http://gbtidl.nrao.edu

    For help with a GBTIDL routine from the command line, use
             the procedure 'usage'.  For example:

   usage,'show'           ; gives the syntax of the procedure 'show'
   usage,'show',/verbose  ; gives more information on 'show'
--------------------------------------------------------------------

% Compiled module: GETFLUXCALIB.
% Compiled module: GETAPEFF.
% Compiled module: GETTAU.
% Compiled module: AIRMASS.
% Compiled module: ELEVFROMAIRMASS.
% Compiled module: TA2FLUX.
% Compiled module: QUICKTATM.
% Compiled module: DATETOMJD.
% Compiled module: GETFORECASTEDTAU.
% Compiled module: SAMPLERTOIDX.
% Compiled module: CVRTFLUX2TA.
% Compiled module: CVRTTA2FLUX.
% Compiled module: MAKEGIF.
% Compiled module: DISPLAYRFI.
% Compiled module: RFIFILENAME.
% Compiled module: GETRFISCAN.
% Compiled module: GETRFITP.
% Compiled module: BLANKFREQS.
% Compiled module: BLANKCHANS.
% Compiled module: FLAGFREQS.
% Compiled module: ZOOMGIFS.
% Compiled module: WRITEDC.
% Compiled module: CALSEQ.
% Compiled module: RFISCANS_MOD.
% Compiled module: PROCESS_FILE.
Connecting to file: /home/sdfits/TRFI_040520_C1/TRFI_040520_C1.raw.vegas
Scan:       3   Bandwith(MHz):       1080.0000   Channels:       16384
Processing Scan:       3 IFNum:           0
% Compiled module: DIGITAL_FILTER.
Processing Scan:       3 IFNum:           1
Processing Scan:       3 IFNum:           2
Processing Scan:       3 IFNum:           3
Processing Scan:       3 IFNum:           4
Processing Scan:       3 IFNum:           5
Scan:       4   Bandwith(MHz):       1080.0000   Channels:       16384
Processing Scan:       4 IFNum:           0
Processing Scan:       4 IFNum:           1
Processing Scan:       4 IFNum:           2
Processing Scan:       4 IFNum:           3
Processing Scan:       4 IFNum:           4
Processing Scan:       4 IFNum:           5
Scan:       5   Bandwith(MHz):       1080.0000   Channels:       16384
Processing Scan:       5 IFNum:           0
Processing Scan:       5 IFNum:           1
Processing Scan:       5 IFNum:           2
Processing Scan:       5 IFNum:           3
Processing Scan:       5 IFNum:           4
Processing Scan:       5 IFNum:           5
Scan:       6   Bandwith(MHz):       1080.0000   Channels:       16384
Processing Scan:       6 IFNum:           0
Processing Scan:       6 IFNum:           1
Processing Scan:       6 IFNum:           2
Processing Scan:       6 IFNum:           3
Processing Scan:       6 IFNum:           4
Processing Scan:       6 IFNum:           5
Scan:       7   Bandwith(MHz):       1080.0000   Channels:       16384
Processing Scan:       7 IFNum:           0
Processing Scan:       7 IFNum:           1
Processing Scan:       7 IFNum:           2
Processing Scan:       7 IFNum:           3
Processing Scan:       7 IFNum:           4
Processing Scan:       7 IFNum:           5
Minimum window frequencies:      3.86007      4.46007      5.06007      5.66007      6.26007      6.86007      3.86007      4.46007      5.06007      5.66007      6.26007
      6.86007      3.86007      4.46007      5.06007      5.66007      6.26007      6.86007      3.86007      4.46007      5.06007      5.66007      6.26007      6.86007      3.86007
      4.46007      5.06007      5.66007      6.26007      6.86007
Maximum window frequencies:      4.94000      5.54000      6.14000      6.74000      7.34000      7.94000      4.94000      5.54000      6.14000      6.74000      7.34000
      7.94000      4.94000      5.54000      6.14000      6.74000      7.34000      7.94000      4.94000      5.54000      6.14000      6.74000      7.34000      7.94000      4.94000
      5.54000      6.14000      6.74000      7.34000      7.94000
Writing ASCII data to TRFI_040520_C1_rfiscan1_s0003_f001_Linr_az357_el045.txt, using rfiscans_mod fxn
Data Successfully written.
plot closed
writing status to file /tmp/stat.txt...
printing good_data
file TRFI_040520_C1 processed.
```

This will repeat until all the RFI files are processed, which will take some time. Feel free to kill the session and start it up later. It will not affect the processing.

If you see some files that say they contained "bad data" and are skipped, this is normal. A minority of the files become corrupted and are skipped over and flagged as bad files. If you see that all of the files being processed are skipped, please contact the maintainer of this code to double-check if there are issues (jskipper@nrao.edu).

If you did not elect to upload these files to the database, the script will end here. If you did, it will move on to stage 3: 

### Stage 3:

The script then uploads all new files to the database in the directory you provided, not necessarily just the ones processed in this script run. So if you start processing the files, have to stop, then start again, and finally finish all the files, it will process all of those that you processed even though your script was interrupted. 

The output for uploading the files looks like this: 

```console
File already exists in database, moving on to next file.
Extracting file 437 of 1406, filename: /home/www.gb.nrao.edu/content/IPG/rfiarchive_files/GBTDataImages/TRFI_080113_81_rfiscan1_s0014_f001_Circ_az359_el045.txt
File already exists in database, moving on to next file.
Extracting file 438 of 1406, filename: /home/www.gb.nrao.edu/content/IPG/rfiarchive_files/GBTDataImages/TRFI_080113_81_rfiscan2_s0013_f001_Linr_az181_el045.txt
File already exists in database, moving on to next file.
Extracting file 439 of 1406, filename: /home/www.gb.nrao.edu/content/IPG/rfiarchive_files/GBTDataImages/TRFI_080210_31_rfiscan1_s0001_f001_Linr_az001_el045.txt
File already exists in database, moving on to next file.
Extracting file 440 of 1406, filename: /home/www.gb.nrao.edu/content/IPG/rfiarchive_files/GBTDataImages/TRFI_080210_31_rfiscan2_s0002_f001_Circ_az179_el045.txt
TRFI_080210_31_rfiscan2_s0002_f001_Circ_az179_el045.txt uploaded.
```

This section takes the longest. Each individual file takes several minutes (about 4 minutes) to upload to the database. If the script has to be stopped and restarted, this is fine, it will pick up where it left off. 

If you have any problems or questions, please contact jskipper@nrao.edu.


## Citations: 

This repository includes rfiDisplay_wilsonedit.pro and scalUtils_wilsonedit.pro, which are modified forms of scripts rfiDisplay.pro and scalUtils.pro. These original scripts were written by Ron Maddalena at Green Bank Observatory (rmaddale@nrao.edu). He is now an emeritus senior scientist at the observatory, and no longer maintains these scripts. Due to this, any questions regarding these scripts should be directed towards Joy Skipper (jskipper@nrao.edu).
