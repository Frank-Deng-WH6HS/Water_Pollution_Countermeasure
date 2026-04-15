#-*- coding:utf-8 -*-
#CRESDA 卫星光学影像产品 元数据模型

import re; 
import xml.etree.ElementTree as xmlet; 

from .. import utils; 

class CresdaMetadataFormatter(object): 
    
    def __init__(self): 
        
        #默认的小数格式
        self.decimal_filter = re.compile(
            r"\A[0-9]+\.[0-9]*\Z"
        ); 
        #默认的日期-时间格式
        self.date_time_filter = re.compile(
            r"\A[0-9]{4}(?:\-[0-9]{2}){2} "
            r"[0-9]{2}(?:\:[0-9]{2}){2}\Z"
        )
        #默认的精确日期-时间格式
        self.precise_date_time_filter = re.compile(
            r"\A[0-9]{4}(?:\-[0-9]{2}){2} "
            r"[0-9]{2}(?:\:[0-9]{2}){2}\.[0-9]{2}\Z"
        )

class CresdaProductMetadata(object): 
    
    #类方法: 通过存放元数据的XML文件导入属性
    
    @classmethod
    def from_xml(cls, f): 
        
        #创建新实例, 以便存放属性读取结果
        metadata = cls(); 
        #读取XML, 解析标签及其中内容, 构造键值对
        rs_meta = xmlet.parse(
            f, parser=xmlet.XMLParser(encoding="utf-8")
        ).getroot()[0]; 
        record = {
            utils.camel_to_snake(item.tag): item.text 
            for item in rs_meta
        }; 
        #利用键值对设置实例的有关属性
        metadata.__dict__ = record; 
        return metadata; 
