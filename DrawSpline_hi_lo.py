##--
import optparse
import os
import ROOT
def GetGrphas(proc,filename,binname,nuisance):
    tf=ROOT.TFile.Open(filename)
    path_lo="_".join["spline_lo",binname,proc,nuisance]
    path_hi="_".join["spline_hi",binname,proc,nuisance]

    gr_lo=tf.Get(path_lo).Clone()
    gr_hi=tf.Get(path_hi).Clone()
    tf.Close()
    return gr_lo,gr_hi

def Draw(gr_lo,gr_hi,title):
    c=ROOT.TCanvas()
    gr_lo.Draw()
    gr_hi.Draw("sames")
    gr_hi.SetLineColor(3)
    c.SetLogx()
    c.SaveAs(title+'.pdf')
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

    gr_lo,gr_hi=GetGrphas(proc,filename,binname,nuisance)

    
    title="_".join([proc,binname,nuisance])+'.pdf'

    Draw(gr_lo,gr_hi,title)
