; Importing the current GBTIDL processing script
@/users/rmaddale/mypros/vectorTcals/scalUtils.pro
@/users/rmaddale/mypros/rfiDisplay.pro

pro automation_of_processing
    ; Read in the data gleaned from determine_new_RFI_files.py
    parameters = READ_CSV('subdata.csv',HEADER=header_names)

    ; Make arrays of the required ymax value containing the receivers that use that ymax value
    ymax_rcvr_list_100 = MAKE_ARRAY(dimension=1,/STRING)
    ymax_rcvr_list_100 = STRJOIN([ymax_rcvr_list_100, "Rcvr_342, ","Rcvr_450, ","Rcvr_600, ","Rcvr_800, ","RcvrPF_2, ","RcvrPF_1, ","Rcvr1_2"],/single)
    ymax_rcvr_list_10 = MAKE_ARRAY(dimension=1,/STRING)
    ymax_rcvr_list_10 = STRJOIN([ymax_rcvr_list_10, "Rcvr2_3, ","Rcvr4_6, ","Rcvr8_10, ","Rcvr12_18, ","RcvrArray18_26, ","Rcvr26_40, ","Rcvr40_52, ","Rcvr68_92, ","RcvrArray75_115"],/single)
    
    ; For each line in the csv data containing info on each file that needs to be processed, deal with that file
    FOR filenum = 0, N_ELEMENTS(parameters.field1) - 1 DO BEGIN
        
        ; Gleaning the values necessary for each filename from this line in the csv file
        filename = parameters.field1[filenum]
        receiver = parameters.field2[filenum]
        number_of_scans = parameters.field3[filenum]
        number_of_feeds = parameters.field4[filenum]
        number_of_IFs = parameters.field5[filenum]

        ; making a list of the scans in ascending order (i.e. if there are 3 scans, it will make 1,2,3)
        scanlist = MAKE_ARRAY(dimension=1, /string)
        FOR scan_num = 1,number_of_scans DO BEGIN
            ; If we are at the end of the number of scans, we append the last scan but don't add the comma
            IF scan_num EQ number_of_scans THEN BEGIN 
                scanlist = [scanlist, STRING(scan_num)]
            ENDIF ELSE BEGIN
            ; Otherwise, we want a comma delimiter
            scanlist = [scanlist, STRING(scan_num), ","]
            ENDELSE
        ENDFOR

        ; I DON'T KNOW WHY I NEED THIS
        remove, 0, scanlist ;; THERE'S AN EXTRA 1 WHY

        

        ; If the receiver name is in the ymax100 list, then ymax is 100
        IF (STRPOS(ymax_rcvr_list_100,receiver) NE -1) THEN BEGIN
            ymax = 100
        ; If the receiver name is in the ymax10 list, then ymax is 10
        ENDIF ELSE IF (STRPOS(ymax_rcvr_list_10,receiver) NE -1) THEN BEGIN
            ymax = 10 
        ; Otherwise this isn't a list of known receivers. Something is wrong. 
        ENDIF ELSE BEGIN
            print, "something wrong with setting the ymax value. Check if the receiver is in our list of standard receivers"
            print, receiver
        ENDELSE

        ; Finally, we're ready to start using GBTIDL to call the processing function
        ; Open the file
        offline, filename
        ; We have to make 4 .gifs, one for each zoom level
        FOR nzoom = 0, 3 DO BEGIN
            ; if the receiver is ka_band (also known as Rcvr26_40) then we need the /ka flag
            IF (receiver EQ "Rcvr26_40") THEN BEGIN
                rfiscans_mod, [scanlist], fdnum = number_of_feeds-1, ifmax = number_of_IFs-1, ymax = ymax, nzoom = nzoom, /blnkChans, /makegifs, /makefile, /ka
            ; Otherwise, we call rfiscans_mod (the GBTIDL processing script) the same way but without the /ka flag
            ENDIF ELSE BEGIN
                rfiscans_mod, [scanlist], fdnum = number_of_feeds-1, ifmax = number_of_IFs-1, ymax = ymax, nzoom = nzoom, /blnkChans, /makegifs, /makefile
            ENDELSE
        ENDFOR
    ENDFOR
end
