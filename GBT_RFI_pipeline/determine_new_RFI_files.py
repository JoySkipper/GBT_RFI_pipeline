import sys
import numpy as np
import os
import csv
import pandas
from rfitrends import GBT_receiver_specs

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

    return(RFI_files_to_be_processed)

def find_parameters_to_process_file(RFI_files_to_be_processed: list,path_to_current_RFI_files):
    data_to_process = []
    data_to_process.append(["filename", "receiver", "number_of_scans", "number_of_feeds", "number_of_IFs"])
    
    for file_to_be_processed in RFI_files_to_be_processed:
        line_to_start_reader = 0
        with open(path_to_current_RFI_files+file_to_be_processed+"/"+file_to_be_processed+".raw.vegas/"+file_to_be_processed+".raw.vegas.index") as f:
            header = {}
            file_index = f.readline()
            
            while(file_index):
                if "=" in file_index: 
                    header_entry = file_index.strip().split("=")
                    header[header_entry[0]] = header_entry[1].strip()
                    
                elif "[" in file_index: 
                    pass
                else: 
                    break
                    
                file_index = f.readline()
                line_to_start_reader += 1
        with open(path_to_current_RFI_files+file_to_be_processed+"/"+file_to_be_processed+".raw.vegas/"+file_to_be_processed+".raw.vegas.index") as f:
            data = pandas.read_csv(f,delimiter="\s+|\t+|\s+\t+|\t+\s+",skiprows=line_to_start_reader,engine='python')
        if "Unknown" in data["SOURCE"]:
            continue
        number_of_scans = max(data["SCAN"]) #Scans are 1-indexed
        number_of_feeds = max(data["FDNUM"])+ 1 #FDNUM is zero-indexed
        number_of_IFs = max(data["IFNUM"]) + 1 #IFNUM is zero-indexed
        receiver_name = file_to_be_processed.split("_")[-1]

        verified_receiver_name = GBT_receiver_specs.FrontendVerification(receiver_name)
        oneline_data_to_be_processed = [
            str(file_to_be_processed), 
            str(verified_receiver_name),
            str(number_of_scans),
            str(number_of_feeds),
            str(number_of_IFs)
        ]
        data_to_process.append(oneline_data_to_be_processed)
        print(str(file_to_be_processed)+" processed")
        #os.system("gbtidl -e process")
        #os.system("gbtidl -e \"summary_to_file\" -args "+str(RFI_files_to_be_processed)+" "+str(number_of_scans)+" "+str(number_of_feeds)+" "+str(number_of_IFs))
    return(data_to_process)
    






if __name__ == '__main__': 
    RFI_files_to_be_processed = determine_new_RFI_files(sys.argv[1],sys.argv[2])
    data_to_be_processed = find_parameters_to_process_file(RFI_files_to_be_processed,sys.argv[1])
    print("dumping parameter data to RFI_file_parameters.csv")
    with open("RFI_file_parameters.csv","w") as outfile:
        writer = csv.writer(outfile)
        writer.writerows(data_to_be_processed)
    #os.system("gbtidl -e \"summary_to_file\"")