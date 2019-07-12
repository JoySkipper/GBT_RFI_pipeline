; Importing the current GBTIDL processing script

@/users/rmaddale/mypros/vectorTcals/scalUtils.pro
;@/users/rmaddale/mypros/rfiDisplay.pro
@/users/jskipper/Documents/scripts/RFI/GBT_RFI_pipeline/GBT_RFI_pipeline/rfiDisplay_wilsonedit.pro

pro process_file,scanList, ifmax=ifmax, fdnum=fdnum, intnum=intnum, nzoom=nzoom, ymax=ymax, $
                zfactor=zfactor, instance=instance, makegifs=makegifs, makefile=makefile, ka=ka, $
                nbox=nbox, tau=tau, ap_eff=ap_eff, fltrParms=fltrParms, blnkWdth=blnkWdth, $
                blnkChans=blnkChans, blnkFreqs=blnkFreqs, flagFreqs=flagFreqs, colors=colors, pols=pols, $
                calseqList=calseqList

    rfiscans_Mod, scanlist, fdnum = fdnum, ifmax = ifmax, ymax = ymax, nzoom = nzoom , blnkChans=blnkChans, makefile=makefile, ka=ka
    common gbtplot_common, mystate, xarray
    widget_control, mystate.main, /DESTROY
    print, "plot closed"
end

