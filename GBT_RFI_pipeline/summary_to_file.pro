@/users/rmaddale/mypros/vectorTcals/scalUtils.pro
@/users/rmaddale/mypros/rfiDisplay.pro

pro summary_to_file
    parameters = READ_CSV('subdata.csv',HEADER=header_names)
    ymax_rcvr_list_100 = MAKE_ARRAY(dimension=1,/STRING)
    ymax_rcvr_list_100 = STRJOIN([ymax_rcvr_list_100, "Rcvr_342, ","Rcvr_450, ","Rcvr_600, ","Rcvr_800, ","RcvrPF_2, ","RcvrPF_1, ","Rcvr1_2"],/single)
    ymax_rcvr_list_10 = MAKE_ARRAY(dimension=1,/STRING)
    ymax_rcvr_list_10 = STRJOIN([ymax_rcvr_list_10, "Rcvr2_3, ","Rcvr4_6, ","Rcvr8_10, ","Rcvr12_18, ","RcvrArray18_26, ","Rcvr26_40, ","Rcvr40_52, ","Rcvr68_92, ","RcvrArray75_115"],/single)
    FOR filenum = 0, N_ELEMENTS(parameters.field1) - 1 DO BEGIN
        
        filename = parameters.field1[filenum]
        receiver = parameters.field2[filenum]
        number_of_scans = parameters.field3[filenum]
        number_of_feeds = parameters.field4[filenum]
        number_of_IFs = parameters.field5[filenum]

        ;extra_args = "/makefile /makegifs /blnkChans"
        ;IF (receiver eq 'Rcvr26_40') THEN BEGIN
        ;    ka_arg = " /ka"
        ;    extra_args = STRJOIN([extra_args, ka_arg], /single)
        ;ENDIF

        scanlist = MAKE_ARRAY(dimension=1, /string)
        FOR scan_num = 1,number_of_scans DO BEGIN
            IF scan_num EQ number_of_scans THEN BEGIN 
                scanlist = [scanlist, STRING(scan_num)]
            ENDIF ELSE BEGIN
            scanlist = [scanlist, STRING(scan_num), ","]
            ENDELSE
        ENDFOR
        remove, 0, scanlist ;; THERE'S AN EXTRA ZERO WHY

        


        IF (STRPOS(ymax_rcvr_list_100,receiver) NE -1) THEN BEGIN
            ymax = 100
        ENDIF ELSE IF (STRPOS(ymax_rcvr_list_10,receiver) NE -1) THEN BEGIN
            ymax = 10 
        ENDIF ELSE BEGIN
            print, "something wrong with setting the ymax value. Check if the receiver is in our list of standard receivers"
            print, receiver
        ENDELSE

        offline, filename
        FOR nzoom = 0, 3 DO BEGIN
            IF (receiver EQ "Rcvr26_40") THEN BEGIN
                rfiscans_mod, [scanlist], fdnum = number_of_feeds-1, ifmax = number_of_IFs-1, ymax = ymax, nzoom = nzoom, /blnkChans, /makegifs, /makefile, /ka
                print, 'ka receiver'
            ENDIF ELSE BEGIN
                print, 'not ka receiver'
                print, filename
                print, scanlist
                print, number_of_feeds -1 
                print, number_of_IFs - 1
                print, ymax
                print, nzoom
                rfiscans_mod, [scanlist], fdnum = number_of_feeds-1, ifmax = number_of_IFs-1, ymax = ymax, nzoom = nzoom, /blnkChans, /makegifs, /makefile
            ENDELSE
        ENDFOR



    ENDFOR
end
