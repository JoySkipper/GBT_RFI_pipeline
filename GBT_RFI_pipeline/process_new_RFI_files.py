import sys
import numpy as np
import os
import csv
import pandas
from rfitrends import GBT_receiver_specs
from rfitrends import RFI_input_for_SQL
import time
import multiprocessing as mp
import subprocess

def timeout(func, args = (), kwds = {}, timeout = 1, default = None):
    pool = mp.Pool(processes = 1)
    result = pool.apply_async(func, args = args, kwds = kwds)
    try:
        val = result.get(timeout = timeout)
    except mp.TimeoutError:
        pool.terminate()
        return default
    else:
        pool.close()
        pool.join()
        return val




def determine_new_RFI_files(path_to_current_RFI_files: str,path_to_processed_RFI_files: str):
    """
    :param path_to_all_RFI_files: This is the path to all recent RFI files that have not been pushed to the archive, including those that have been processed into the database and those that haven't
    :param path_to_processed_RFI_files: This is the path to the RFI files that have been processed into the database
    :return: Returns RFI_files_to_be_processed, which is all the names of files that still need go through the processing script
    """

    processed_RFI_files = []
    RFI_files_to_be_processed = []

    # This for loop gathers a list of processed RFI files from the directory in which they're contained
    for processed_file in os.listdir(path_to_processed_RFI_files): 
        if processed_file.endswith(".txt") and processed_file != "URLS.txt": # We only care about the .txt files containing actual data of RFI
            processed_RFI_files.append(processed_file)
    # This for loop goes through all the RFI files still in sdfits and that haven't been archived, finds those that needs to be processed, and appends them to RFI_files_to_be_processed        
    for current_RFI_file in os.listdir(path_to_current_RFI_files): 
        if current_RFI_file.startswith("TRFI") and not any(current_RFI_file in s for s in processed_RFI_files):
            RFI_files_to_be_processed.append(current_RFI_file)

    #return(RFI_files_to_be_processed)
    return(['TRFI_052219_X1','TRFI_033019_C1','TRFI_041319_L1', 'TRFI_052319_X1'])
    #return(['TRFI_062119_31'])
    #return(['TRFI_052319_X1'])
    #return(['TRFI_033019_C1'])
    #return(['TRFI_041319_L1'])

def read_header(file_to_be_processed: str, path_to_current_RFI_files: str):
    """
    :param file_to_be_processed: This is the string containing the name of the file that needs to be processed by the IDL processing script
    :param path_to_current_RFI_files: This is the string containing the path to all current RFI files, in which the files to be processed are contained
    :return: header, and line_to_start_reader; the header contains all the header information, and the line_to_start reader is the line in which the header ends, needed for reading in the data later
    """
    #line_to_start reader is counting the line in which the header ends, so that we can later read in the data of the file and skip the header
    line_to_start_reader = 0

    with open(path_to_current_RFI_files+file_to_be_processed+"/"+file_to_be_processed+".raw.vegas/"+file_to_be_processed+".raw.vegas.index") as f:
        header = {}
        file_index = f.readline()
        
        # The equal sign indicates that this is header information, such as filename = myfile.fits
        while(file_index):
            if "=" in file_index: 
                header_entry = file_index.strip().split("=")
                header[header_entry[0]] = header_entry[1].strip()
            # The [] signs indicate that this is a line that can be skipped
            elif "[" in file_index: 
                pass
            # Once we've reached the end of the header, we want to break the line.
            else: 
                break
                
            file_index = f.readline()
            line_to_start_reader += 1

    return(header,line_to_start_reader)

ymax_determiner = {
    "Rcvr_342":100,
    "Rcvr_450":100,
    "Rcvr_600":100,
    "Rcvr_800":100,
    "RcvrPF_2":100,
    "RcvrPF_1":100,
    "Rcvr1_2":100,
    "Rcvr2_3":10,
    "Rcvr4_6":10,
    "Rcvr8_10":10,
    "Rcvr12_18":10,
    "RcvrArray18_26":10,
    "Rcvr26_40":10,
    "Rcvr40_52":10,
    "Rcvr68_92":10,
    "RcvrArray75_115":10
}

def find_parameters_to_process_file(RFI_files_to_be_processed: list,path_to_current_RFI_files):
    """
    param: RFI_files_to_be_processed: List of all RFI files that need to be processed by the GBTIDL processing script
    param: path_to_current_RFI_files: String containing the path to all current RFI files, in which the files to be processed are contained
    return: data_to_process; which is a list of lists containing each file with the information needed to run the GBTIDL processing script
    """
    data_to_process = []
    #data_to_process.append(["filename", "receiver", "max_scan_number", "min_scan_number", "number_of_feeds", "number_of_IFs"])
    
    for file_to_be_processed in RFI_files_to_be_processed:

        _, line_to_start_reader = read_header(file_to_be_processed, path_to_current_RFI_files)

        # Read the csv-non header portion in
        with open(path_to_current_RFI_files+file_to_be_processed+"/"+file_to_be_processed+".raw.vegas/"+file_to_be_processed+".raw.vegas.index") as f:
            data = pandas.read_csv(f,delimiter='\s+|\t+|\s+\t+|\t+\s+',skiprows=line_to_start_reader,engine='python')
        # If the source is unknown, this is a bad scan. Currently, the processing IDL code we are feeding this into cannot handle files with even one bad scan. 
        # This processing IDL code is in the works to be replaced with one that is more robust. 
        if "Unknown" in data["SOURCE"]:
            continue
        max_scan_number = max(data["SCAN"]) #Scans are 1-indexed
        min_scan_number = min(data["SCAN"]) 
        number_of_feeds = max(data["FDNUM"])+ 1 #FDNUM is zero-indexed
        number_of_IFs = max(data["IFNUM"]) + 1 #IFNUM is zero-indexed

        # Getting the first part of the filename (i.e. TRFI_122001_PF1) and taking the last component (PF1) that actually names the receiver
        receiver_name = file_to_be_processed.split("_")[-1]

        # The receiver name is not consistent in it's naming scheme. This changes the receiver name to the GBT standardized frontend naming scheme
        verified_receiver_name = GBT_receiver_specs.FrontendVerification(receiver_name)
        scanlist = list(range(min_scan_number,max_scan_number))
        
        
        ymax = ymax_determiner[verified_receiver_name]


        # Creating a list representing one line of the eventual output file with the necessary info for each file

        
        oneline_data_to_be_processed = {
            "filename": file_to_be_processed, 
            "frontend": verified_receiver_name,
            "list_of_scans": scanlist,
            "number_of_feeds":number_of_feeds,
            "number_of_IFs":number_of_IFs,
            "ymax":ymax
        }

        # Appending oneline data to be processed to create a list of lists for the file info
        data_to_process.append(oneline_data_to_be_processed)

        print(str(file_to_be_processed)+" parameter data gleaned")
        
    return(data_to_process)
    

def analyze_file(file_to_process):
    if file_to_process["frontend"] == "Rcvr26_40":
        #print(timeout(os.system, args=("gbtidl -e \"offline, \'"+str(file_to_process["filename"])+"\' & process_file,  "+str(file_to_process["list_of_scans"])+", fdnum="+str(file_to_process["number_of_feeds"])+"-1, ymax="+str(file_to_process["ymax"])+", ifmax = "+str(file_to_process["number_of_IFs"])+"-1, nzoom = 0, /blnkChans, /makefile, /ka\""),timeout=3,default="Process Timed Out.")) 
        process = subprocess.Popen(['gbtidl', '-e', 'offline, \''+str(file_to_process["filename"])+'\' & process_file, '+str(file_to_process["list_of_scans"])+', fdnum='+str(file_to_process["number_of_feeds"])+'-1, ymax='+str(file_to_process["ymax"])+', ifmax = '+str(file_to_process["number_of_IFs"])+'-1, nzoom = 0, /blnkChans, /makefile, /ka'])
        
        try:
            print('Running in process', process.pid)
            process.wait(timeout=300)
        except subprocess.TimeoutExpired:
            print('Timed out - killing', process.pid)
            process.kill()
        print("Done")
    else:
        #print('\"offline, \''+str(file_to_process["filename"])+'\' & process_file, '+str(file_to_process["list_of_scans"])+', fdnum='+str(file_to_process["number_of_feeds"])+'-1, ymax='+str(file_to_process["ymax"])+', ifmax = '+str(file_to_process["number_of_IFs"])+'-1, nzoom = 0, /blnkChans, /makefile\"')
        process = subprocess.Popen(['gbtidl', '-e', 'offline, \''+str(file_to_process['filename'])+'\' & process_file, '+str(file_to_process['list_of_scans'])+', fdnum='+str(file_to_process['number_of_feeds'])+'-1, ymax='+str(file_to_process['ymax'])+', ifmax = '+str(file_to_process['number_of_IFs'])+'-1, nzoom = 0, /blnkChans, /makefile'])
        #process = subprocess.Popen(['gbtidl', '-e', 'offline, \''+str(file_to_process['filename'])+'\''])
        try:
            print('Running in process', process.pid)
            process.wait(timeout=300)
        except subprocess.TimeoutExpired:
            print('Timed out - killing', process.pid)
            process.kill()
        print("Done")
        #print(timeout(os.system, args=("gbtidl -e \"offline, \'"+str(file_to_process["filename"])+"\' & process_file, "+str(file_to_process["list_of_scans"])+", fdnum="+str(file_to_process["number_of_feeds"])+"-1, ymax="+str(file_to_process["ymax"])+", ifmax = "+str(file_to_process["number_of_IFs"])+"-1, nzoom = 0, /blnkChans, /makefile\"",),timeout=3,default="Process Timed Out"))



if __name__ == '__main__': 
    path_to_current_RFI_files = sys.argv[1]
    path_to_processed_RFI_files = sys.argv[2]
    # Find which file to be processed
    RFI_files_to_be_processed = determine_new_RFI_files(path_to_current_RFI_files,path_to_processed_RFI_files)
    # Get the data to be processed from each file
    data_to_be_processed = find_parameters_to_process_file(RFI_files_to_be_processed,path_to_current_RFI_files)
    #data_to_be_processed = find_parameters_to_process_file(["TRFI_051419_S21"],path_to_current_RFI_files)
    for file_to_process in data_to_be_processed:
        print("processing file: "+str(file_to_process['filename']))
        analyze_file(file_to_process)
        #print(timeout(analyze_file, args=(file_to_process,),timeout=3,default='File timed out in processing. Moving on to next file.'))
        print("file "+str(file_to_process['filename'])+" processed.")
        

    # Dummping that data to a csv to be read in by the IDL processing file
    #print("dumping parameter data to RFI_file_parameters.csv")
    #with open("RFI_file_parameters.csv","w") as outfile:
    #    writer = csv.writer(outfile)
    #    writer.writerows(data_to_be_processed)
    # Calling that IDL processing file
    #os.system("cd "+str(path_to_processed_RFI_files))
    #os.system("gbtidl -e \"automation_of_processing\"")
    print("All new files processed and loaded as .txt files")
    main_database = sys.argv[3]
    dirty_database = sys.argv[4]
    # RFI_input_for_SQL.write_to_database(main_database,dirty_database,path_to_current_RFI_files,files_to_process = RFI_files_to_be_processed)
    print("Uploading .txt files to database:")
    RFI_input_for_SQL.write_to_database(main_database,dirty_database,"./",files_to_process = RFI_files_to_be_processed)
    