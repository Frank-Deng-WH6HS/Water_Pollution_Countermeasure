#面向路径匹配任务的改版正则表达式
#REAP, Regular Expression Adapted for Path matching

import re; 

class Reap(object): 
    
    #由python re.pattern改造而得
    #大部分语法与re.pattern一致, 支持匹配结果编组引用, 位置匹配
    #匹配结果编组引用功能, 可用于在替换操作中保留部分匹配结果
    #位置匹配功能包括四种零宽断言
    #通配符与glob差异较大, 与re.pattern语法相近
    
    REGEX_METHOD = set(
        attr for attr in re.compile(r"").__dir__() 
        if not attr.startswith("__") and not attr.endswith("__")
    ); 
    
    #优化规则
        #正斜杠(/)匹配单个正斜杠或反斜杠
    SLASH_FILTER = re.compile(r"/"); 
    SLASH_REPLACE = r"[/\\\]"; 
        #未转义的句点(.)只匹配文件名支持的合法字符
        #句点表示其字面意义时, 无论是否放置在方括号内, 均必须用反斜杠转义
    DOT_FILTER = re.compile(r"(?<!\\)\."); 
    DOT_REPLACE = r"[^/\\\:\*\?\"\<\>\|]"; 
    
    def __init__(self, pattern): 
        p = pattern; 
        p = self.SLASH_FILTER.sub(self.SLASH_REPLACE, p); 
        p = self.DOT_FILTER.sub(self.DOT_REPLACE, p); 
        self._regex = re.compile(p); 
        
    def __repr__(self): 
        return "{cls:s}({patt:s})".format(
            cls=self.__class__.__name__, 
            patt=self._regex.pattern
        ); 
    
    #手动引入re.Pattern的方法, 因为re.Pattern类不可派生
    #注意: 此处应腹泻__getattr__方法, 方法中调用self.__getattribute__, 防止无限递归
    
    def __getattr__(self, attr): 
        if attr in self.REGEX_METHOD: 
            return self._regex.__getattribute__(attr); 
        else: 
            return self.__getattribute__(attr); 
    