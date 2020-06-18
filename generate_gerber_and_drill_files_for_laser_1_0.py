from pcbnew import *
import os
import  datetime

PLUGIN_VERSION = '1.0'

class GenLaser(ActionPlugin):
    def defaults(self):
        self.name = "Generate gerber and drill files for Laser at GEII Toulon "\
        +PLUGIN_VERSION
        self.category = "GEII TOULON"
        self.description = "Generate gerber and drill files for Laser"
        self.show_toolbar_button = True # Optional, defaults to False
        self.icon_file_name = os.path.join(os.path.dirname(__file__), 'dl300.png') # Optional, defaults to ""

    def genGerber(self,board,path):

        pctl = PLOT_CONTROLLER(board)
        popt = pctl.GetPlotOptions()
        popt.SetOutputDirectory(path)
        popt.SetPlotFrameRef(False)     #do not change it
        popt.SetLineWidth(FromMM(0.1))
        
        popt.SetAutoScale(False)        #do not change it
        popt.SetScale(1)                #do not change it
        popt.SetMirror(False)
        popt.SetUseGerberAttributes(False)
        popt.SetIncludeGerberNetlistInfo(True)
        #popt.SetCreateGerberJobFile(gen_job_file)
        popt.SetUseGerberProtelExtensions(False)
        popt.SetExcludeEdgeLayer(False);
        popt.SetScale(1)
        popt.SetUseAuxOrigin(False)
        # This by gerbers only
        popt.SetSubtractMaskFromSilk(False)
        # Disable plot pad holes
        popt.SetDrillMarksType( PCB_PLOT_PARAMS.NO_DRILL_SHAPE );
        # Skip plot pad NPTH when possible: when drill size and shape == pad size and shape
        # usually sel to True for copper layers
        
        popt.SetSkipPlotNPTH_Pads( False );
        
        # Once the defaults are set it become pretty easy...
        # I have a Turing-complete programming language here: I'll use it...
        # param 0 is a string added to the file base name to identify the drawing
        # param 1 is the layer ID
        # param 2 is a comment
#        plot_plan = [
#        ( "CuTop", F_Cu, "Top layer" ),
#        ( "CuBottom", B_Cu, "Bottom layer" ),
#        ( "PasteBottom", B_Paste, "Paste Bottom" ),
#        ( "PasteTop", F_Paste, "Paste top" ),
#        ( "SilkTop", F_SilkS, "Silk top" ),
#        ( "SilkBottom", B_SilkS, "Silk top" ),
#        ( "MaskBottom", B_Mask, "Mask bottom" ),
#        ( "MaskTop", F_Mask, "Mask top" ),
#        ( "EdgeCuts", Edge_Cuts, "Edges" ),
#        ]
        plot_plan = [
        ( "CuTop", F_Cu, "Top layer" ),
        ( "CuBottom", B_Cu, "Bottom layer" ),
        ( "EdgeCuts", Edge_Cuts, "Edges" ),
        ( "LaserFiducials",Eco1_User,"Laser Fiducials")
        ]
        for layer_info in plot_plan:

                if layer_info[1] <= B_Cu:
                    popt.SetSkipPlotNPTH_Pads( True )
                else:
                    popt.SetSkipPlotNPTH_Pads( False )
                if layer_info[1] ==Eco1_User :
                     popt.SetExcludeEdgeLayer(True)
                else :
                    popt.SetExcludeEdgeLayer(False)
                pctl.SetLayer(layer_info[1])
                pctl.OpenPlotfile(layer_info[0], PLOT_FORMAT_GERBER, layer_info[2])
        
                if pctl.PlotLayer() == False:
                    pass

        # At the end you have to close the last plot, otherwise you don't know when
        # the object will be recycled!
        pctl.ClosePlot()
      


    def genDrill(self,board, path, filename):
        
        drlwriter = EXCELLON_WRITER( board )
        drlwriter.SetMapFileFormat( PLOT_FORMAT_PDF )
        mirror = False
        minimalHeader = False
        mergeNPTH = True
        offset = wxPoint(0,0)
        drlwriter.SetOptions( mirror, minimalHeader, offset, mergeNPTH )
        drlwriter.SetRouteModeForOvalHoles(False) # G85 for oval shapes
        metricFmt = True
        drlwriter.SetFormat( metricFmt )
        genDrl = True
        genMap = True
  
        drlwriter.CreateDrillandMapFilesSet(path, genDrl, genMap );

        # One can create a text file to report drill statistics
        drlwriter.GenDrillReportFile( path+'/'+filename+'_drill_stat.txt' );
     
    def Run(self):
        # The entry function of the plugin that is executed on user action
        board = GetBoard()
        absoluteFileName=board.GetFileName()

        dirName =  os.path.dirname(absoluteFileName)
        fileName = os.path.basename(absoluteFileName)
        fileNameNoExt =  os.path.splitext(fileName)[0]
        outDir = dirName+'/'+ fileNameNoExt +'-Laser-Gerber'
         
        try :
            os.mkdir(outDir)
        except FileExistsError :
            #silently rewrite if already exists
            pass
        
        self.genDrill(board,outDir,fileNameNoExt)
        self.genGerber(board,outDir)

        now = datetime.datetime.now()
        strNow=now.strftime("%Y-%m-%d %H:%M:%S")
        try :
            f=open(outDir+'/'+fileNameNoExt+'_log.txt','w')
        except :
            return
        f.write('Manufacturing files for Laser at GEII Toulon\n' )
        f.write('Board : ' + fileNameNoExt +'\n')
        f.write('Generated on '+strNow+'\n')
        f.write('Pcbnew Version : '+GetBuildVersion()+'\n')
        f.write('Plugin version : '+ PLUGIN_VERSION+'\n')
        f.close()
        
GenLaser().register() # Instantiate and register to Pcbnew
