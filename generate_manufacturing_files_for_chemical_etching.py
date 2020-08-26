import pcbnew
import os
import logging
import platform
import shutil
import datetime

PLUGIN_VERSION = '1.0'

# set to logging.INFO for normal usage
# set to logging.DEBUG for debugging
loggingLevel = logging.INFO 

class SimplePlugin(pcbnew.ActionPlugin):
    def defaults(self):
        self.name = "Generate manufacturing_files for chemical etching at GEII Toulon"\
        +PLUGIN_VERSION
        self.category = "GEII Toulon plugins"
        self.description = "Generate manufacturing files for chemical etching at GEII Toulon"
        self.show_toolbar_button = True
        self.icon_file_name = os.path.join(os.path.dirname(__file__), 'chemical.png')  

    def Run(self):
        board = pcbnew.GetBoard()
        absoluteFileName=board.GetFileName()
        
        # save the current board
        board.Save(absoluteFileName)
        
        dirName =  os.path.dirname(absoluteFileName)
        fileName = os.path.basename(absoluteFileName)
        fileNameNoExt =  os.path.splitext(fileName)[0]
        outDir = dirName+'/'+ fileNameNoExt +'-Chemical-Files'
        logName = outDir +'/'+ fileNameNoExt + '.log'
        try :
            os.mkdir(outDir)
        except :  # ugly but FileExistsError is not available en python 2.x
            #silently rewrite if already exists
            pass
        logging.basicConfig(filename=logName,filemode='w',level=loggingLevel,\
                            format='%(levelname)s:%(message)s')
      
        logging.info(' Board :'+ fileName)  
        now = datetime.datetime.now()
        strNow=now.strftime("%Y-%m-%d %H:%M:%S")
        logging.info('Generated on '+strNow)
        
        self.genPostscript(board,outDir)
        self.genDrill(board,outDir,fileNameNoExt)
        # also copy board to outDir if we need to merge multiple board
        shutil.copy2(absoluteFileName,outDir)

    def genPostscript(self,board,path):
         pc = pcbnew.PLOT_CONTROLLER(board)
         po = pc.GetPlotOptions()
         # set global options
         po.SetPlotFrameRef(False)
         po.SetOutputDirectory(path)
         po.SetA4Output(True)
         po.SetScale(1.0)
         po.SetExcludeEdgeLayer(False)
         po.SetDrillMarksType(po.SMALL_DRILL_SHAPE)
         # Set options for front Copper layer 
         pc.SetLayer(pcbnew.F_Cu)
         po.SetMirror(True)
        # Plot front Copper
         pc.OpenPlotfile("CuTOP", pcbnew.PLOT_FORMAT_POST, "front_copper")
         pc.PlotLayer()
         pc.ClosePlot()
         #Plot bottom Copper
         # Set options for Bottom Copper layer 
         pc.SetLayer(pcbnew.B_Cu)
         po.SetMirror(False)
         pc.OpenPlotfile("CuBOT", pcbnew.PLOT_FORMAT_POST, "bottom_copper")
         pc.PlotLayer()
         pc.ClosePlot()
         
         logging.info('Postcripts done')  
         
    def genDrill(self,board, path, filename):
        
        drlwriter = pcbnew.EXCELLON_WRITER( board )
        drlwriter.SetMapFileFormat( pcbnew.PLOT_FORMAT_PDF )
        mirror = False
        minimalHeader = False
        mergeNPTH = True
        offset = pcbnew.wxPoint(0,0)
        drlwriter.SetOptions( mirror, minimalHeader, offset, mergeNPTH )
        drlwriter.SetRouteModeForOvalHoles(False) # G85 for oval shapes
        metricFmt = False
        drlwriter.SetFormat( metricFmt , drlwriter.KEEP_ZEROS)
        genDrl = True
        genMap = True
  
        drlwriter.CreateDrillandMapFilesSet(path, genDrl, genMap );
        
        # convert to DOS format when run on Linux
        if platform.system() == 'Linux':
            f=open(path+'/'+filename+'.drl','r')
            content = f.read()
            content = self.toDOS(content)
            f=open(path+'/'+filename+'.drl','w')
            f.write(content)
            f.close()
        
        # One can create a text file to report drill statistics
        drlwriter.GenDrillReportFile( path+'/'+filename+'_drill_stat.txt' );
        
        
        logging.info('Drill file done')  
        
    # convert to DOS format    
    def toDOS(self,text):
        return text.replace('\n', '\r\n')
        
        

        
SimplePlugin().register() # Instantiate and register to Pcbnew
