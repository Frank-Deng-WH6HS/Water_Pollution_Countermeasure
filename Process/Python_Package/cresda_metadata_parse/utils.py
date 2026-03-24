#CRESDA 卫星光学影像产品信息访问包 - 辅助工具

import re; 

CAMEL_FILTER = re.compile(r"(?P<caps>(?<=[^A-Z])[A-Z])"); 

#将标识符名称从"驼式"转换为"蛇式"

def camel_to_snake(camel): 
    snake = CAMEL_FILTER.sub("_\g<caps>", camel).lower(); 
    return snake; 
