#-*- coding:utf-8 -*-
#路径批量管理, 文件批量读写工具包

import os; 
import re; 

import collections as coll; 

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
        self.source_pattern = r"(.*)"; 
        self.target_patterns = (r"\g<1>", ); 
        
    #设置源文件的存放路径
    
    @property
    def source_dir(self): 
        return self._source_dir; 
    @source_dir.setter
    def source_dir(self, path): 
        src = self._path_validated(path, mkdir=False); 
        if src: 
            self._source_dir = src; 
        else: 
            raise FileNotFoundError(path); 

    #设置目标文件的存放路径

    @property
    def target_dir(self): 
        return self._target_dir; 
    @target_dir.setter
    def target_dir(self, path): 
        trg = self._path_validated(path, mkdir=True); 
        if trg: 
            self._target_dir = trg; 
        else: 
            raise FileNotFoundError(path); 
    
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
    
    #设置目标文件的路径模式, 必须是list或tuple; 
    #bytes将被解码为str, str将转换为一元tuple, 其他类型将报错. 
    #已知的问题: 此模式在用于替换的过程中, 可能将source_pattern匹配得到的编组复用, 
        #拼接, 构造得到包含 os.pardir 的路径, 实现文件遍历攻击. 
    #在实际的软件开发中, 不建议在source_pattern或target_pattern属性接收用户输入. 
    
    @property
    def target_patterns(self): 
        return self._target_patt; 
    @source_pattern.setter
    def target_patterns(self, pattern): 
        p = pattern; 
        if type(p) is bytes: 
            p = p.decode(encoding="iso-8859-1"); 
        if type(p) is str: 
            p = (p, ); 
        if type(p) not in {list, tuple}: 
            raise typeError(type(p)); 
        self._target_patt = p; 
        

    #在源文件所在目录下遍历符合条件的路径, 返回源文件路径, 目标文件路径和编组捕获结果
    
    TRV_REC_FLD = ("source", "target", "groupdict"); 
    TraverseRecord = coll.namedtuple("TraverseRecord", TRV_REC_FLD); 
    
    def traverse(self): 
        for node, dirs, files in os.walk(self._source_dir): 
            items = files; 
            for item in items: 
                path = os.path.join(node, item); 
                match = self._source_patt.match(path); 
                if not match: 
                    continue; 
                #匹配结果输出
                source = match.group(0); #源文件路径
                target = tuple(
                    self._target_dir + self._source_patt.sub(
                        p, match.string
                    ) for p in self._target_patt
                ); #目标文件路径
                groupdict = match.groupdict(); #编组捕获结果
                rec = self.TraverseRecord(
                    source=source, target=target, groupdict=groupdict
                ); 
                yield rec; 