;..module: process_file.pro
    ;:synopsis: imports the necessary gbtidl dependencies and then calls rfiScansMod. Also closes the GBTIDL plot when it's finished
;..moduleauthor:: Joy Skipper <jskipper@nrao.edu>
;Code Origin: https://github.com/JoySkipper/GBT_RFI_pipeline

; Importing the current GBTIDL processing script



pro process_file,scanList, ifmax=ifmax, fdnum=fdnum, intnum=intnum, nzoom=nzoom, ymax=ymax, $
                zfactor=zfactor, instance=instance, makegifs=makegifs, makefile=makefile, ka=ka, $
                nbox=nbox, tau=tau, ap_eff=ap_eff, fltrParms=fltrParms, blnkWdth=blnkWdth, $
                blnkChans=blnkChans, blnkFreqs=blnkFreqs, flagFreqs=flagFreqs, colors=colors, pols=pols, $
                calseqList=calseqList,output_file=output_file
    CATCH, Error_status 
    if Error_status NE 0 then begin
        openw, status_file, output_file+'stat.txt',/GET_LUN
        printf, status_file, "bad_data"
        print,Error_status
        FREE_LUN, status_file
        CATCH,/CANCEL
    endif
    ;if there's an error, catch it and send it to bad data. 

    ;CD, output_file

    ; Run rfiscansmod, Ron's script which processes the file and produces a .txt file and 4 gif plots
    status = rfiscans_Mod(scanlist, fdnum = fdnum, ifmax = ifmax, ymax = ymax, nzoom = nzoom , blnkChans=blnkChans, makefile=makefile, ka=ka)
    common gbtplot_common, mystate, xarray 
    ; rfiscans mod opens a plot, which we need to close to go to the next plot
    widget_control, mystate.main, /DESTROY
    print, "plot closed" 
    ; open the next file
    openw, status_file, output_file+'stat.txt',/GET_LUN
    print, 'writing status to file '+output_file+'stat.txt...'
    ; print to file 
    if status then begin
        print,'printing'+status
        printf, status_file, status
        FREE_LUN, status_file
    endif else begin
        print, 'printing good data'
        printf, status_file, "good_data"
        FREE_LUN, status_file
    endelse
    
    
end

