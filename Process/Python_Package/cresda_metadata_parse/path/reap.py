#面向路径匹配任务的改版正则表达式
#REAP, Regular Expression Adapted for Path matching

import re; 
import copy; 

from pygments import lexer, token; 

#从扩展词法分析器派生类, 使得解析结果中包含中间状态

class RegexLexerConservingStata(lexer.ExtendedRegexLexer): 
    
    def __init__(self): 
        super().__init__(); 
    
    #实例方法: 同时获取token的类型, 内容和状态
    def get_tokens_and_states(self, text=None): 
        ctx = lexer.LexerContext(text, 0); 
        for pos, syn, txt in self.get_tokens_unprocessed(
            text=text, context=ctx
        ): 
            states = ctx.stack[-1]
            yield syn, txt, states; 

#Python正则表达式通配符和字符集语法分析器

class SreCharSetLexer(RegexLexerConservingStata): 
    
    syntax_regex = token.String.Regex; 

    syntax_regex.subtypes.clear(); 
    
    tokens = {
        "root": [
            (r'\[\^', #进入取反字符集
                syntax_regex.Delimiter, "charset_excl"
            ), (r'\[(?!\^)', #进入字符集
                syntax_regex.Delimiter, "charset_incl"
            ), (r'\\[\(\)\[\]\{\}\\\|\*\?\+\-\^\$\.]', #元字符转义
                syntax_regex.Escape
            ), (r'(?<!\\)\\[DSWdsw]', #通配符
                syntax_regex.Wildcard
            ), (r'(?<!\\)\.', #点
                syntax_regex.Wildcard
            ), (r".+?", 
                syntax_regex.Other
            )
        ], 
        "charset_excl": [
            (r'(?<!\\)]', #退出取反字符集
                syntax_regex.Delimiter, "#pop"
            ), (r'\\[\(\)\[\]\{\}\\\|\*\?\+\-\^\$\.]', #元字符转义
                syntax_regex.Escape
            ), (r'(?<!\\)\\[DSWdsw]', #通配符
                syntax_regex.Wildcard
            ), (r".+?", 
                syntax_regex.Other
            )
        ], 
        "charset_incl": [
            (r'(?<!\\)]', #退出字符集
                syntax_regex.Delimiter, "#pop"
            ), (r'\\[\(\)\[\]\{\}\\\|\*\?\+\-\^\$\.]', #元字符转义
                syntax_regex.Escape
            ), (r'(?<!\\)\\[DSWdsw]', #通配符
                syntax_regex.Wildcard
            ), (r".+?", 
                syntax_regex.Other
            )
        ]
    }; 
    
class Reap(object): 
    
    #由python re.Pattern改造而得. 
    #大部分语法与re.Pattern一致, 支持匹配结果编组引用, 位置匹配. 
    #匹配结果编组引用功能, 可用于在替换操作中保留部分匹配结果. 
    #位置匹配功能包括四种零宽断言. 
    #通配符与glob差异较大, 与re.Pattern语法相近. 
    
    REGEX_METHODS = set(
        attr for attr in re.compile(r"").__dir__() 
        if not attr.startswith("__") and not attr.endswith("__")
    ); 
    
    CHAR_ILLEGAL = r"/\\\:\*\?\"\<\>\|"; 
    
    #优化规则
        #正斜杠(/)匹配单个正斜杠或反斜杠
        #\D, \W, \S同时排除文件名不支持的字符
            #如 r"\W" 替换为 r"[^\w{char}]".format(char=CHAR_ILLEGAL)
            #\D, \W, \S位于字符集 r"[bar]" 时, 应将 r"[bar\W]" 转换为 r"(?:[bar]|\W)"
            #之后继续替换\D, \W, \S
            #\D, \W, \S位于取反字符集 r"[^bar]" 时, 不转换, 不替换, 因为非法字符均在\W和\S内
        #取反字符集同时排除文件名不支持的字符
            #当左 r"[", 右方括号 r"]", 插入符 r"^" 表示其字面意义时, 无论是否放置在
            #方括号内, 均必须用反斜杠转义
        #未转义的句点 r"." 只匹配文件名支持的合法字符
            #替换为 r"[^\d{char}]".format(char=CHAR_ILLEGAL)
            #句点表示其字面意义时, 无论是否放置在方括号内, 均必须用反斜杠转义
    
    def __init__(self, pattern): 
        p = pattern; 
        self._input_pattern = p; 
        
        pass; #需要引入pygments
        
        self._regex = re.compile(p); 
        
    @property
    def input_pattern(self):
        return self._input_pattern; 
        
    def __repr__(self): 
        return "{cls:s}({input:s}) -> {comp}".format(
            cls=self.__class__.__name__, 
            input=self._input_pattern, 
            comp=self._regex.pattern
        ); 
    
    #手动引入re.Pattern的方法, 因为re.Pattern类不可派生
    #注意: 此处应覆写__getattr__方法, 方法中调用self.__getattribute__, 防止无限递归
    
    def __getattr__(self, attr): 
        if attr in self.REGEX_METHODS: 
            return self._regex.__getattribute__(attr); 
        else: 
            return self.__getattribute__(attr); 
    