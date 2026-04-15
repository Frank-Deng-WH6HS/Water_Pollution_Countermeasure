#-*- coding:utf-8 -*-
#CRESDA 卫星光学影像产品信息访问包 - 辅助工具

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
       
#将标识符名称从"驼式"转换为"蛇式"

CAMEL_FILTER = re.compile(r"(?P<caps>(?<=[^A-Z])[A-Z])"); 

def camel_to_snake(camel): 
    snake = CAMEL_FILTER.sub("_\g<caps>", camel).lower(); 
    return snake; 
