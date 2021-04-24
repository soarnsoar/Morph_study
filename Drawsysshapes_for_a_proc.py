##--
import optparse
import os
import ROOT
from copy import deepcopy
def GetGraphsList(proc,filename,binname,nuisanceList):
    print "<GetGraphsList>"
    grlist={}
    tf=ROOT.TFile.Open(filename)
    path="_".join([binname,proc])
    gr=tf.Get(path)
    gr.SetDirectory(0)
    grlist['nominal']=deepcopy(gr)


    for nuisance in nuisanceList:
        
        path_up=''+("_".join([binname,proc,nuisance]))+'Up'
        path_down=("_".join([binname,proc,nuisance]))+'Down'
        print path_up
        print path_down

        gr_up=(tf.Get(path_up).Clone())
        gr_down=(tf.Get(path_down).Clone())
        #print type(gr_up)
        gr_up.SetDirectory(0)
        gr_down.SetDirectory(0)
        grlist[nuisance+'Up']=deepcopy(gr_up)
        grlist[nuisance+'Down']=deepcopy(gr_down)
        
        #print type(grlist[nuisance+'Up'])
    #print type(grlist[nuisance+'Up'])
    tf.Close()
    return grlist


def TestNominalBetweenUpDown(gr_nom,gr_up,gr_down,nuisance):
    Nbins=gr_nom.GetNbinsX()
    for b in range(1,Nbins):
        nom=gr_nom.GetBinContent(b)
        up=gr_up.GetBinContent(b)
        down=gr_down.GetBinContent(b)

        if (nom-up)*(nom-down)>0:
            print '<',nuisance,'>',"nominal is not between up,down-->bin#=",b
            print "nom=",nom
            print "up=",up
            print "down=",down
def Draw(grlist,title,nuisances):
    c=ROOT.TCanvas()
    
    idx=1
    for nuisance in nuisances:


        #print type(grlist[nuisance+'Up'])

        idx+=1
        grlist[nuisance+'Up'].Draw("sames")
        grlist[nuisance+'Down'].Draw("sames")
            
            
        grlist[nuisance+'Up'].SetTitle(title)
        grlist[nuisance+'Down'].SetTitle(title)
        
        grlist[nuisance+'Up'].SetStats(0)
        grlist[nuisance+'Down'].SetStats(0)
        
        grlist[nuisance+'Up'].SetLineColor(idx)
        grlist[nuisance+'Down'].SetLineColor(idx)
        
        grlist[nuisance+'Up'].SetMarkerColor(idx)
        grlist[nuisance+'Down'].SetMarkerColor(idx)
        
        grlist[nuisance+'Down'].SetLineWidth(2)
        grlist[nuisance+'Down'].SetLineStyle(2)
        
        TestNominalBetweenUpDown(grlist['nominal'],grlist[nuisance+'Up'],grlist[nuisance+'Down'],nuisance)



    grlist['nominal'].SetTitle(title)
    grlist['nominal'].Draw("sames")
    grlist['nominal'].SetStats(0)

    c.SetLogx()
    c.SetLogy()
    #print "a"
    leg=ROOT.TLegend(0.1,0.6,0.48,0.9)
    leg.AddEntry(grlist['nominal'],'nominal')

    leg.AddEntry(grlist[nuisance+'Up'],nuisance)
    
            
    leg.Draw()
    #print "b"
    os.system('mkdir -p plots/')
    c.SaveAs('plots/'+title+'.pdf')
if __name__ == '__main__':
    usage = 'usage: %prog [options]'
    parser = optparse.OptionParser(usage)
    parser.add_option("-p","--proc",   dest="proc", help="process name")
    parser.add_option("-f","--filename",   dest="filename", help="submit")
    parser.add_option("-b","--bin",   dest="binname", help="binname")
    parser.add_option("-n","--nui",   dest="nuisances", help="nuisance")

    (options, args) = parser.parse_args()
    
    proc=options.proc
    filename=options.filename
    binname=options.binname
    nuisances=str(options.nuisances).split(',')

    grlist=GetGraphsList(proc,filename,binname,nuisances)

    
    title='histo_'+("_".join([proc,binname]+nuisances))

    Draw(grlist,title,nuisances)

