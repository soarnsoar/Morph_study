##--
import optparse
import os
import ROOT
def GetGraphs(proc,filename,binname,nuisance):
    tf=ROOT.TFile.Open(filename)
    path_lo="_".join(["spline_lo",binname,proc,nuisance])
    path_hi="_".join(["spline_hi",binname,proc,nuisance])
    path="_".join(["spline_hi",binname,proc])

    gr_lo=tf.Get(path_lo).Clone()
    gr_hi=tf.Get(path_hi).Clone()
    #gr=tf.Get(path)
    tf.Close()
    return gr_lo,gr_hi

def Draw(gr_lo,gr_hi,title):
    c=ROOT.TCanvas()
    gr_hi.SetTitle(title)
    gr_lo.SetTitle(title)


    gr_hi.Draw("AL")
    gr_lo.Draw("L")
    

    xlist_hi=gr_hi.GetX()
    ylist_hi=gr_hi.GetY()
    ylist_lo=gr_lo.GetY()
    for idx in range(len(ylist_hi)):
        nom=1
        hi=ylist_hi[idx]
        lo=ylist_lo[idx]

        if (nom-hi)*(nom-lo)>0:
            print "<",title,">nominal is not between hi,lo"
            print "x=",xlist_hi[idx]
            print 'nom=',nom
            print 'hi=',hi
            print 'lo=',lo
            
    gr_hi.SetLineColor(2)
    gr_hi.SetLineWidth(2)
    gr_lo.SetLineColor(4)
    gr_lo.SetLineWidth(2)

    c.SetLogx()
    
    leg=ROOT.TLegend(0.1,0.9,0.28,1.0)
    leg.AddEntry(gr_hi,"high")
    leg.AddEntry(gr_lo,"low")

    leg.Draw()
    os.system('mkdir -p plots/')
    c.SaveAs('plots/'+title+'.pdf')
if __name__ == '__main__':
    usage = 'usage: %prog [options]'
    parser = optparse.OptionParser(usage)
    parser.add_option("-p","--proc",   dest="proc", help="process name")
    parser.add_option("-f","--filename",   dest="filename", help="submit")
    parser.add_option("-b","--bin",   dest="binname", help="binname")
    parser.add_option("-n","--nui",   dest="nuisance", help="nuisance")

    (options, args) = parser.parse_args()
    
    proc=options.proc
    filename=options.filename
    binname=options.binname
    nuisance=options.nuisance

    gr_lo,gr_hi=GetGraphs(proc,filename,binname,nuisance)

    
    title="_".join([proc,binname,nuisance])

    Draw(gr_lo,gr_hi,title)
