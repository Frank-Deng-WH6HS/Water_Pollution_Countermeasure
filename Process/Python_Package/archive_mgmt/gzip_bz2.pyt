#-*-coding:utf-8-*-

import io, sys, os; 
import gzip, bz2, shutil; 
import arcpy; 

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
        self.label = "GZIP / BZIP2 (De)compressor"; 
        self.alias = ""; 
        self.tools = [
            ToGzip, 
            ToBz2, 
        ]; 

class ToGzip(Tool): 

    def __init__(self): 
        super(type(self).__mro__[0], self).__init__(); 
        self.label = "Create GZIP Archive"; 

    def getParameterInfo(self): 
        param_in_path = arcpy.Parameter(
            name="in_path", 
            displayName="Input File", 
            datatype="DEFile", 
            parameterType="Required", 
            direction="Input", 
            enabled=True
        ); 
        param_out_path = arcpy.Parameter(
            name="out_path", 
            displayName="Output File", 
            datatype="DEFile", 
            parameterType="Required", 
            direction="Output", 
            enabled=True
        ); 
        param_comp_lvl = arcpy.Parameter(
            name="comp_lvl", 
            displayName="Compress Level", 
            datatype="GPLong", 
            parameterType="Required", 
            direction="Input", 
            enabled=True
        ); 
        param_comp_lvl.value = 9; 
        param_comp_lvl.filter.list = list(range(0, 10)); 
        params = [
            param_in_path, 
            param_out_path, 
            param_comp_lvl
        ]; 
        return params; 

    def execute(self, parameters, messages): 
        
        path_input = parameters[0].valueAsText; 
        path_output = parameters[1].valueAsText; 
        comp_lvl = parameters[2].value; 
        
        with io.open(
            path_input, mode='rb', 
            buffering=io.DEFAULT_BUFFER_SIZE
        ) as f_in: 
            
            total_size = os.path.getsize(path_input); 
            arcpy.SetProgressor(type="default"); 
            
            with gzip.GzipFile(
                path_output, mode='wb', 
                compresslevel=comp_lvl
            ) as f_out: 
                
                while f_in.tell() < total_size: 
                    chunk = f_in.read(io.DEFAULT_BUFFER_SIZE); 
                    f_out.write(chunk); 
                    arcpy.SetProgressorPosition(None); 
        
        return; 

class ToBz2(Tool): 

    def __init__(self): 
        super(type(self).__mro__[0], self).__init__(); 
        self.label = "Create BZIP2 Archive"; 

    def getParameterInfo(self): 
        param_in_path = arcpy.Parameter(
            name="in_path", 
            displayName="Input File", 
            datatype="DEFile", 
            parameterType="Required", 
            direction="Input", 
            enabled=True
        ); 
        param_out_path = arcpy.Parameter(
            name="out_path", 
            displayName="Output File", 
            datatype="DEFile", 
            parameterType="Required", 
            direction="Output", 
            enabled=True
        ); 
        param_comp_lvl = arcpy.Parameter(
            name="comp_lvl", 
            displayName="Compress Level", 
            datatype="GPLong", 
            parameterType="Required", 
            direction="Input", 
            enabled=True
        ); 
        param_comp_lvl.value = 9; 
        param_comp_lvl.filter.list = list(range(0, 10)); 
        params = [
            param_in_path, 
            param_out_path, 
            param_comp_lvl
        ]; 
        return params; 

    def execute(self, parameters, messages): 
        path_input = parameters[0].valueAsText; 
        path_output = parameters[1].valueAsText; 
        comp_lvl = parameters[2].value; 
        
        with io.open(
            path_input, mode='rb', 
            buffering=io.DEFAULT_BUFFER_SIZE
        ) as f_in: 
            
            total_size = os.path.getsize(path_input); 
            arcpy.SetProgressor(type="default"); 
            
            with bz2.BZ2File(
                path_output, mode='wb', 
                compresslevel=comp_lvl
            ) as f_out: 
                
                while f_in.tell() < total_size: 
                    chunk = f_in.read(io.DEFAULT_BUFFER_SIZE); 
                    f_out.write(chunk); 
                    arcpy.SetProgressorPosition(None); 
        
        return; 
