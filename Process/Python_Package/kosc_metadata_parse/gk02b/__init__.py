#-*- coding:utf-8 -*-
#中巴地球资源卫星四号 (CBERS-04, CB04) 产品信息

import re; 

import path_matcher; 

#地球同步卫星海洋水色成像仪-II (GOCI2) 全圆盘分块成像产品 L2级数据
class GOCI2_FD(path_matcher.FilenameMatcher): 
    
    PRODUCTS = {
        "AC", "IOP", 
        "Kd", "Zsd", "Chl", "CDOM", "TSS", 
        "FA", "CF"
    }; 
    
    SRC_ARX_BASENAME = \
        r"(?P<archive>" \
            "GK2B_GOCI2_L2_[0-9]{8}_[0-9]{6}" \
            "_FD_S[0-9]{3}_G[0-9]{3}" \
        ")";  
    
    @classmethod
    def _product_filter(cls, products): 
        if type(products) is str: 
            prods = {products}; 
        else: 
            prods = set(products); 
        if cls.PRODUCTS.issuperset(prods): 
            prod_filter = r"(?:{prods})".format(
                prods="\x7c".join(prods)
            ); 
            return prod_filter; 
        else: 
            prods = cls.PRODUCTS.difference(prods); 
            raise ValueError(
                "Unsupported product(s): {prods}".format(
                    prods=",\x20".join(prods)
                )
            ); 
    
    def __init__(self): 
        super(type(self).__mro__[0], self).__init__(); 
        self.products = self.PRODUCTS; 
        
    @property
    def products(self): 
        return self._products; 
    
    @products.setter
    def products(self, prods): 
        prod_filter = self._product_filter(prods); 
        self._products = prods; 
        self.source_pattern = r"{arx}_{prod}/(?P=archive)_{prod}\.nc".format(
            arx=self.SRC_ARX_BASENAME, prod=prod_filter
        ); 
        self.target_patterns = tuple(); 

    def reset(self): 
        self.__init__(); 
        