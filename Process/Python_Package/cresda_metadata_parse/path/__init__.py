#路径批量管理, 文件批量读写工具包

import os; 
import re; 

#基类: 文件名称匹配器

class FilenameMatcher(object): 
    
    #静态方法: 路径有效性检查
    
    @staticmethod
    def _path_validated(path, mkdir=False): 
        
        #标准化路径名称
        norm = os.path.normpath(path); 
        #检查路径存在性
        if os.path.isdir(norm): 
            #路径有效时, 返回标准化后的绝对路径
            return norm; 
        elif mkdir: 
            #路径无效时, 如果指定立即新建路径, 则在标准化
            #后的绝对路径新建空目录, 并返回该路径
            os.makedirs(norm); 
            return norm; 
        else: 
            #否则返回空字符串 (转换为bool的结果为False)
            return str(); 
    
    def __init__(self): 
        self._source_dir = os.getcwd(); 
        self._target_dir = os.getcwd(); 
        self._source_patt = re.compile(".*"); 
        self._target_patt = re.compile(".*"); 
        
    #设置源文件的存放路径
    
    @property
    def source_dir(self): 
        return self._source_dir; 
    @source_dir.setter
    def source_dir(self, path): 
        src = self._path_validated(path, mkdir=False); 
        if src: 
            self._source_dir = src; 

    #设置目标文件的存放路径

    @property
    def target_dir(self): 
        return self._target_dir; 
    @target_dir.setter
    def target_dir(self, path): 
        trg = self._path_validated(path, mkdir=True); 
        if trg: 
            self._target_dir = trg; 
            
    