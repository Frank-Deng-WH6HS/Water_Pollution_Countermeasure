#路径批量管理, 文件批量读写工具包

import os; 
import re; 

from .reap import Reap; 

#基类: 文件名称匹配器

class FilenameMatcher(object): 
    
    #静态方法: 路径有效性检查
    
    @staticmethod
    def _path_validated(path, mkdir=False): 
        
        #标准化路径名称
        norm = path; 
        norm = os.path.normcase(norm); 
        norm = os.path.normpath(path); 
        norm += os.sep; 
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
        self._source_dir = None;  
        self._target_dir = None;  
        self._source_patt = None; 
        self._target_patt = None; 
        self.source_dir = os.getcwd(); 
        self.target_dir = os.getcwd(); 
        self.source_pattern = r".*"; 
        self.target_pattern = r".*"; 
        
    #设置源文件的存放路径
    
    @property
    def source_dir(self): 
        return self._source_dir; 
    @source_dir.setter
    def source_dir(self, path): 
        src = self._path_validated(path, mkdir=False); 
        if src: self._source_dir = src; 

    #设置目标文件的存放路径

    @property
    def target_dir(self): 
        return self._target_dir; 
    @target_dir.setter
    def target_dir(self, path): 
        trg = self._path_validated(path, mkdir=True); 
        if trg: self._target_dir = trg; 
    
    #设置源文件的路径模式
    
    @property
    def source_pattern(self): 
        root = re.escape(self._source_dir); 
        root = re.escape(root); 
        p = self._source_patt.input_pattern; 
        p = re.sub(r"\A\\A", str(), p); 
        p = re.sub(r"\A{root}".format(root=root), str(), p); 
        p = re.sub(r"\\Z\Z", str(), p); 
        return p; 
    @source_pattern.setter
    def source_pattern(self, pattern): 
        root = re.escape(self._source_dir); 
        p = r"\A{patt}\Z".format(patt=root + pattern)
        self._source_patt = Reap(p); 
    
    #设置目标文件的路径模式
    
    @property
    def target_pattern(self): 
        root = re.escape(self._target_dir); 
        root = re.escape(root); 
        p = self._target_patt.input_pattern; 
        p = re.sub(r"\A\\A", str(), p); 
        p = re.sub(r"\A{root}".format(root=root), str(), p); 
        p = re.sub(r"\\Z\Z", str(), p); 
        return p; 
    @source_pattern.setter
    def target_pattern(self, pattern): 
        root = re.escape(self._target_dir); 
        p = r"\A{patt}\Z".format(patt=root + pattern)
        self._target_patt = Reap(p); 

