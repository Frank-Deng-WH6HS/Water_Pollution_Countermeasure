#-*- coding:utf-8 -*-
#IDL 并行计算管理工具包 - 辅助工具

import sys; 

import re; 

#Python 2.x / 3.x 兼容性管理

PY_2X = (sys.version_info.major == 2); 
PY_3X = (sys.version_info.major == 3); 

if PY_3X: 
    
    import importlib; 
    def isidentifier(s): 
        return s.isidentifier(); 
    
elif PY_2X: 
    
    import importlib, imp; 
    imp.import_module = importlib.import_module; 
    import imp as importlib; 
    def isidentifier(s): 
        return re.match(r"\A[A-Za-z_][0-9A-Za-z_]*\Z", s); 
       