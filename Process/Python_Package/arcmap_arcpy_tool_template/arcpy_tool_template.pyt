#-*-coding:utf-8-*-

import io, sys, os; 
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
        self.label = ""; 
        self.alias = ""; 
        self.tools = [
            GetToolboxPath
        ]; 

class GetToolboxPath(Tool): 

    def __init__(self): 
        super(type(self).__mro__[0], self).__init__(); 
        self.label = "Get Path of Current Toolbox"; 

    def getParameterInfo(self): 
        param_tbx_path = arcpy.Parameter(
            name="tbx_path", 
            displayName="Path of Current Toolbox", 
            datatype="DEFolder", 
            parameterType="Derived", 
            direction="Output", 
            enabled=False
        ); 
        params = [
            param_tbx_path
        ]; 
        return params; 

    def execute(self, parameters, messages):
        script_path = os.path.abspath(__file__); 
        tbx_path = os.path.dirname(script_path); 
        arcpy.AddMessage(tbx_path); 
        arcpy.SetParameterAsText(0, tbx_path); 
        return; 

