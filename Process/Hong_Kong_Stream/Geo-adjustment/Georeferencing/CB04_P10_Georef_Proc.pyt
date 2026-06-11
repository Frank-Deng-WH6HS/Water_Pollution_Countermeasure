#-*-coding:utf-8-*-

import io, sys, os; 
import arcpy; 

_tbx_path = os.path.abspath(__file__); 
_tbx_dir = os.path.dirname(_tbx_path); 

"""Basic Type for ArcGIS Desktop Tools"""
class Tool(object): 

    def __init__(self): 
        self.label = self.__class__.__name__; 
        self.description = ""; 
        self.canRunInBackground = False; 

    def getParameterInfo(self): 
        params = None; 
        return params; 

    def isLicensed(self): 
        return True; 

    def updateParameters(self, parameters): 
        return; 

    def updateMessages(self, parameters): 
        return; 

    def execute(self, parameters, messages): 
        return; 

class Toolbox(object): 

    def __init__(self): 
        self.label = ""; 
        self.alias = ""; 
        self.tools = [
            WarpReprojectedRaster
        ]; 

class WarpReprojectedRaster(Tool): 

    def __init__(self): 
        super(type(self).__mro__[0], self).__init__(); 
        self.label = "Warp Reprojected CBERS-04 P10 Raster"; 
    
    def getParameterInfo(self): 
        param_tif_out_path = arcpy.Parameter(
            name="tif_out_path", 
            displayName="Path of Output Raster File", 
            datatype="DEFile", 
            parameterType="Derived", 
            direction="Output", 
            enabled=False
        ); 
        params = [
            param_tif_out_path
        ]; 
        return params; 

    def execute(self, parameters, messages): 
        input_path = os.path.abspath(os.path.join(
            _tbx_dir, os.pardir, "Reprojection", 
            "CB04-P10-371-75-A1-20241107-L20005253293_UTM49N.dat"
        ) ); 
        output_path = os.path.abspath(os.path.join(
            _tbx_dir,  
            "CB04-P10-371-75-A1-20241107-L20005253293_Spline"
        ) ); 
        link_file = os.path.abspath(os.path.join(
            _tbx_dir,  
            "CB04-P10-371-75-20241107_LINK.txt"
        ) ); 
        output_tif = output_path + ".tif"; 
        arcpy.env.compression = "LZW"; 
        arcpy.WarpFromFile_management(
            input_path, output_tif, 
            link_file, "SPLINE", "BILINEAR"
        ); 
        arcpy.SetParameterAsText(0, output_tif); 
        return; 
    