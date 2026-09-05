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

#装饰器, 将类转换为单例模式
#仅对被装饰的类本身生效, 其派生类不受影响
#声明: 本函数部分代码由 DeepSeek-V4-Pro 辅助编写, 经适当修改而得.
    
def singleton(cls): 
    instances = dict(); 
    sgl_cls = cls; 
    init_flag = "_singleton_initialized"; 
    #保存原始的 __new__ 和 __init__
    orig_new = cls.__new__; 
    orig_init = cls.__init__; 
    
    def __new__(cls, *pos, **kw): 
        if cls is sgl_cls: 
            #单例逻辑: 若实例不存在则创建, 否则直接返回缓存实例
            if cls not in instances: 
                #创建新实例 (区分 object.__new__ 以处理参数)
                if orig_new is object.__new__: 
                    instance = object.__new__(cls); 
                else: 
                    instance = orig_new(cls, *pos, **kw); 
                #设置初始化标志为 False, 等待 __init__ 完成首次初始化
                setattr(instance, init_flag, False); 
                instances[cls] = instance; 
            return instances[cls]; 
        else: 
            #派生类: 正常创建实例, 不使用缓存
            if orig_new is object.__new__: 
                return object.__new__(cls); 
            else: 
                return orig_new(cls, *pos, **kw); 
            
    #包装 __init__ 以跳过重复初始化 (仅对原始单例类有效)
    if orig_init is not None: 
        def __init__(self, *pos, **kw): 
            if self.__class__ is sgl_cls: 
                #原始单例类: 仅在首次初始化时执行原 __init__
                if getattr(self, init_flag, False): 
                    return None; #已初始化, 跳过
                orig_init(self, *pos, **kw); 
                setattr(self, init_flag, True); 
            else:
                #派生类: 正常执行(继承的 __init__ 逻辑)
                orig_init(self, *pos, **kw); 
    else: 
        #若未定义 __init__, 则使用空操作, 
        #避免调用 object.__init__ 时出错
        def __init__(self, *pos, **kw): 
            pass; 
        
    #替换类的 __new__ 和 __init__
    cls.__new__ = staticmethod(__new__); 
    cls.__init__ = __init__; 
    return cls; 
