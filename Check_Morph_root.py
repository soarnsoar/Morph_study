#hww_lqq7_untag_13TeV_0_13TeV_ggH_HWWSBI_140_pdf_Higgs_ggUp
#hww_lqq7_bs_ggf_13TeV_0_13TeV_ggH_HWW_115
import ROOT

import sys
morphfile=sys.argv[1]
bkgfile=sys.argv[2]
#output/Full2017_indep/cmb/hww_inputsemi17.root


tfile=ROOT.TFile.Open(morphfile)

ObjList=ROOT.gDirectory.GetListOfKeys()
nscan=len(ObjList)
print "nscan=",nscan
nominal_name_list=[]
print "Get Nominal Name List"
for obj in ObjList:
    if obj.GetClassName()!="TH1D":continue
    name=obj.GetName()
    #print name
    #break
    if name.endswith('Up') or name.endswith('Down'):continue
    print name
    nominal_name_list.append(name)
print "[End] Get Nominal Name List"
nominal_name_list=list(set(nominal_name_list))
#for nominal in nominal_name_list:
#    ##---
#    print 'Parse',nominal
#    #hww_lqq7_bs_ggf_13TeV_0_13TeV_ggH_HWW_115
#    cutname=nominal.split('_ggH_HWW')[0].split('_qqH_HWW')[0]
#    print cutname
tfile_bkg=ROOT.TFile.Open(bkgfile)
nscan=len(ObjList)
idx=0   
for obj in ObjList:
    idx+=1
    if idx%10==0:print idx,'/',nscan
    if obj.GetClassName()!="TH1D":continue
    
    name=obj.GetName()
    #print name
    if not 'SBI' in name: continue
    nominalname=''
    for nominal in nominal_name_list:
        if nominal in name:
            if name.split(nominal)[1]=='' or name.split(nominal)[1].startswith('_'):
                nominalname=nominal
                systematic_suffix=name.split(nominal)[1]
    #print name,nominalname,systematic_suffix
    prod=''
    if 'ggH' in nominalname:
        prod='ggH'
    if 'qqH' in nominalname:
        prod='qqH'

    cutname=nominalname.split('_ggH_HWW')[0].split('_qqH_HWW')[0]
    
    mass=float(nominalname.split('HWWSBI_')[1].split('_')[0])

    ##--SBI
    nominal_SBI_rate=tfile.Get('interp_rate_'+cutname+'_'+prod+'_HWWSBI').Eval(mass)
    sys_SBI_rate=1.0
    nominal_S_rate=tfile.Get('interp_rate_'+cutname+'_'+prod+'_HWW').Eval(mass)
    sys_S_rate=1.0
    if systematic_suffix!='':
        direction=''
        UpDown=''
        if 'Up' in systematic_suffix:
            direction='hi'
            UpDown='Up'
        if 'Down' in systematic_suffix:
            direction='lo'
            UpDown='Down'
        sys_SBI_rate=tfile.Get('spline_'+direction+'_'+cutname+'_'+prod+'_HWWSBI'+systematic_suffix.replace(UpDown,'')).Eval(mass)
        #print 'spline_'+direction+'_'+cutname+'_'+prod+'_HWW'+systematic_suffix.replace(UpDown,'')
        try:
            sys_S_rate=tfile.Get('spline_'+direction+'_'+cutname+'_'+prod+'_HWW'+systematic_suffix.replace(UpDown,'')).Eval(mass)
        except:
            sys_S_rate=1.0
    SBI_rate=nominal_SBI_rate*sys_SBI_rate
    S_rate=nominal_S_rate*sys_S_rate
    #spline_hi_hww_lqq7_wj_vbf_13TeV_0_13TeV_qqH_HWWSBI_CMS_scale_e_2017;1


    ###--get bkgshape
    h125name=''
    bkgname=''
    if 'qqH' in nominalname:
        h125name='qqH_hww'
        bkgname='qqWWqq'
    if 'ggH' in nominalname:
        h125name='ggH_hww'
        bkgname='ggWW'
    try:
        #print cutname+'/'+h125name+systematic_suffix
        h_h125=tfile_bkg.Get(cutname+'/'+h125name+systematic_suffix)
        h_h125.Integral()
    except:
        #print cutname+'/'+h125name
        h_h125=tfile_bkg.Get(cutname+'/'+h125name)
    try:
        #print cutname+'/'+bkgname+systematic_suffix
        h_bkg=tfile_bkg.Get(cutname+'/'+bkgname+systematic_suffix)
        h_bkg.Integral()
    except:
        #print cutname+'/'+bkgname
        h_bkg=tfile_bkg.Get(cutname+'/'+bkgname)
    try:
        #print name.replace('HWWSBI','HWW')
        h_s=tfile.Get(name.replace('HWWSBI','HWW'))
        h_s.Integral()
    except:
        #print name.replace('HWWSBI','HWW').replace(systematic_suffix,'')
        h_s=tfile.Get(name.replace('HWWSBI','HWW').replace(systematic_suffix,''))
    h_sbi=tfile.Get(name)



    Nbins=h_sbi.GetNbinsX()
    for i in range(Nbins):
    
        y_sbi=h_sbi.GetBinContent(i)
        y_s=h_s.GetBinContent(i)
        try:
            y_h125=h_h125.GetBinContent(i)
        except:
            y_h125=0.
        try:
            y_bkg=h_bkg.GetBinContent(i)
        except:
            y_bkg=0.

        y_sbi*=SBI_rate
        y_s*=S_rate

        y_I=y_sbi-y_s-y_h125-y_bkg
        
        DET=y_I**2-4*y_s*(y_bkg+y_h125)
        if DET>0.0001 and y_I<0:
            print DET,'i=',i,name
            print 'y_sbi',y_sbi
            print 'y_s',y_s
            print 'y_bkg',y_bkg
            print 'y_h125',y_h125


            
