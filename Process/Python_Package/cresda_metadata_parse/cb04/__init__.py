#中巴地球资源卫星四号 (CBERS-04, CB04) 产品信息

import re; 

from .. import metadata, utils; 

#影像产品名格式

PRODUCT_NAME_FILTER = {
    "MUX": r"(?P<archive>CB04\-MUX\-[0-9]+\-[0-9]+\-2[0-9]{7}\-L2[0-9]{10})", 
    "IRS": r"(?P<archive>CB04\-IRS\-[0-9]+\-[0-9]+\-2[0-9]{7}\-L2[0-9]{10})", 
}; 
PRODUCT_NAME_FILTER = {
    key: re.compile(val) 
    for key, val in PRODUCT_NAME_FILTER.items()
}; 
