#-*- coding:utf-8 -*-

import io, sys, os; 

_ = sys.stdout; 
with io.BytesIO() as sys.stdout: import idlpy; 
sys.stdout = _; 

from . import ipy, ipym; 
from .idl_script_parse import idl_remove_comment

@ipym.magics_class
class IDLMagics(ipym.Magics): 
    
    @ipym.cell_magic
    def idl_exec(self, line, cell): 
        idl_sta = idl_remove_comment(cell); 
        idl_sta = idl_sta.split("\n"); 
        idl_sta = "\n".join(line.strip() for line in idl_sta); 
        idl_sta = idl_sta.replace("$\n", "\x20"); 
        idl_sta = idl_sta.replace("\n", "\x20&\x20"); 
        idlpy.IDL.run(idl_sta, stdout=True); 
        
def load_ipython_extension(ipy):
    ipy.register_magics(IDLMagics)