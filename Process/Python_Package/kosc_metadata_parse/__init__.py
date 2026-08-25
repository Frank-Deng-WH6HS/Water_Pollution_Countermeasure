#-*- coding:utf-8 -*-
#KOSC 卫星光学影像产品信息访问包

_satellites = ["gk02b"]; 

#根据支持的卫星范围, 依次导入当前程序包中, 对应名称的子模块

from .utils import importlib, isidentifier as _isidentifier; 

for _satellite in _satellites: 
    if _isidentifier(_satellite): 
        importlib.import_module("." + _satellite, package=__name__); 

