#CRESDA 卫星光学影像产品信息访问包

#注意: 本软件包只适用于由 CRESDA 直接托管和分发的中国光学卫星产品. 
#无法用于访问其他部门分发的同种卫星 / 传感器产品

import importlib; 

#当前支持的卫星范围

_satellites = ["cb04"]; 

#根据支持的卫星范围, 依次导入当前程序包中, 对应名称的子模块

for _satellite in _satellites: 
    if _satellite.isidentifier(): 
        importlib.import_module("." + _satellite, package=__name__); 
