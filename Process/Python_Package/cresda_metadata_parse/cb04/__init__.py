#-*- coding:utf-8 -*-
#中巴地球资源卫星四号 (CBERS-04, CB04) 产品信息

import re; 

from .. import auxiliary as aux; 
import path_matcher; 

#20米多光谱相机 (MUX)
class MUX(path_matcher.FilenameMatcher, aux.OpticalL2): 
    
    SRC_ARX_BASENAME = \
        r"(?P<archive>" \
            "CB04\-MUX(?:\-[0-9]+){2}\-[0-9]{8}" \
            "\-L20*(?P<prod>[1-9][0-9]{,9})" \
        ")";  
    SRC_ARX_PREFIX = SRC_ARX_BASENAME + r"/(?P=prod)/(?P=archive)\.TIF"; 
    TRG_ARX_BASENAME = r"\g<archive>/\g<prod>/"; 
    TRG_MATADATA_SUFFIX = r"\g<archive>.XML"; 
    
    def __init__(self): 
        super(type(self).__mro__[0], self).__init__(); 
        self.source_pattern = self.SRC_ARX_PREFIX; 
        self.target_patterns = (
            self.TRG_ARX_BASENAME + self.TRG_MATADATA_SUFFIX, 
            self.TRG_ARX_BASENAME + self.VIEW_GEOM
        ); 

    def reset(self): 
        self.__init__(); 
        
    
#10米多光谱相机 (P10)
class P10(path_matcher.FilenameMatcher, aux.OpticalL2): 
    
    SRC_ARX_BASENAME = \
        r"(?P<archive>" \
            "CB04\-P10(?:\-[0-9]+){2}\-[A-Z][0-9]\-[0-9]{8}" \
            "\-L20*(?P<prod>[1-9][0-9]{,9})" \
        ")";  
    SRC_ARX_PREFIX = SRC_ARX_BASENAME + r"/(?P=prod)/(?P=archive)\.TIF"; 
    TRG_ARX_BASENAME = r"\g<archive>/\g<prod>/"; 
    TRG_MATADATA_SUFFIX = r"\g<archive>.XML"; 
    
    def __init__(self): 
        super(type(self).__mro__[0], self).__init__(); 
        self.source_pattern = self.SRC_ARX_PREFIX; 
        self.target_patterns = (
            self.TRG_ARX_BASENAME + self.TRG_MATADATA_SUFFIX, 
            self.TRG_ARX_BASENAME + self.VIEW_GEOM
        ); 

    def reset(self): 
        self.__init__();       
    