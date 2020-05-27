# Making Changes to GBT_RFI_pipeline

## If a receiver is added to the RFI list: 

Under GBT_RFI_pipelin/process_new_RFI_files.py, you will need to add the y maximum needed for your given receiver under the 'ymax_determiner' dictionary. 

Changes will need to be made to the dependent repository, GBT_RFI_Analysis_Tool, but GBT_RFI_pipeline should remain stable as long as you uninstall and re-install the GBT_RFI_pipeline installation. 

This is done in your environment as follows: 

pip uninstall rfitrends

pip install git+https://github.com/TapasiGhosh/GBT_RFI_Analysis_Tool

## Structure of code: 

The primary script is process_new_RFI_files.py. This firest connects to the database, then collects the filepaths of the files that need to be processed. 
It then goes through each file, one by one, reading in the data, verifying that the data is not corrupted, and then attempts to upload that data. If it gets a duplicate entry response, it uploads that data to the duplicate table. Otherwise, it uploads to the main table. 
It updates both the latest project, the receiver table, the main table, and the Flagged table if there is bad data. 

