#-*- coding:utf-8 -*-
#面向路径匹配任务的改版正则表达式
#REAP, Regular Expression Adapted for Path matching

import re; 

from pygments import lexer, token; 

#从扩展词法分析器派生类, 使得解析结果中包含中间状态

class RegexLexerConservingStata(lexer.ExtendedRegexLexer): 
    
    def __init__(self): 
        super(type(self).__mro__[1], self).__init__(); 
    
    #实例方法: 同时获取token的类型, 内容和状态
    def get_tokens_and_stata(self, text=None): 
        ctx = lexer.LexerContext(text, 0); 
        for pos, syn, txt in self.get_tokens_unprocessed(
            text=text, context=ctx
        ): 
            states = ctx.stack[-1]
            yield syn, txt, states; 

#Python内置正则表达式 (sr, Secret Labs' Regular Expression) 
#通配符和字符集语法分析器

class SreCharSetLexer(RegexLexerConservingStata): 
    
    syntax_regex = token.String.Regex; 
    
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
            ), (r".+?", #其他部分
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
            ), (r".+?", #其他部分
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
            ), (r".+?", #其他部分
                syntax_regex.Other
            )
        ]
    }; 
    
#面向路径匹配任务的 sr 正则表达式改编
    
class Reap(object): 
    
    #Reap 语法以 python 内置正则表达式 (sr) 语法为基础, 经改造而得, 
        #用于简化文件路径匹配过程中的路径模式编写过程. 
    #大部分语法与 sr 一致, 支持匹配结果编组引用, 位置匹配. 
        #匹配结果编组引用功能, 可用于在替换操作中保留部分匹配结果. 
        #位置匹配功能包括四种零宽断言. 
        #通配符与glob差异较大, 与 sr 语法相近. 
    
    REGEX_METHODS = set(
        attr for attr in dir(re.compile(str())) 
        if not attr.startswith("_")
    ); 
    
    #文件名中的非法字符: 
        #正斜杠 (Linux路径分隔符, Windows远程路径分隔符)
        #反斜杠 (DOS, Windows本地路径分隔符), 
        #半角冒号 (DOS, Windows卷标)
        #半角星号, 问号 (Windows文件名通配符)
        #半角双引号 (Windows路径字符串定界符)
        #小于号, 大于号 (Linux, Windows程序I/O流重定向输入, 重定向输出标识)
        #管道符 (Linux, Windows程序I/O流管道连接标识)
        #不同OS对非法字符的限制范围不同, 但为保证REAP匹配结果在不同平台的一致性, 
        #因此在任何OS下均考虑所有的非法字符
    CHAR_ILLEGAL = r"/\\\:\*\?\"\<\>\|"; 
    
    #优化规则
        #正斜杠 r"/" 匹配单个正斜杠或反斜杠
            #替换为 r"[/\\]"
        #r"\D", r"\W", r"\S"同时排除文件名不支持的字符
            #如 r"\W" 替换为 r"[^\w{char}]".format(char=CHAR_ILLEGAL)
            #r"\D", r"\W", r"\S"位于字符集 r"[bar]" 时, 应先将 r"[bar\W]" 
            #转换为 r"(?:[bar]|\W)", 之后继续替换r"\D", r"\W", r"\S"
            #r"\D", r"\W", r"\S"位于取反字符集 r"[^bar]" 时, 不作处理
            #因为非法字符均在r"\D", r"\W", r"\S"内
        #取反字符集同时排除文件名不支持的字符
            #当左方括号 r"[", 右方括号 r"]", 插入符 r"^" 表示其字面意义时, 
            #无论是否放置在方括号内, 均必须用反斜杠转义
        #未转义的句点 r"." 排除文件名不支持的字符
            #替换为 r"[^{char}]".format(char=CHAR_ILLEGAL)
    
    #词法分析器, 作为类的公共属性, 在类定义阶段即创建, 无需在每次构造实例时重新创建
    LEX = SreCharSetLexer(); 
    
    #部分字符的转换函数
    
    @classmethod
    def _left_bracket_caret_conv(cls, syn, txt, sta): 
        txt_mod = r"[^{char}".format(char=cls.CHAR_ILLEGAL); 
        return syn, txt_mod, sta; 
    
    @classmethod
    def _left_bracket_conv(cls, syn, txt, sta): 
        txt_mod = r"(?:["; 
        return syn, txt_mod, sta; 
    
    @classmethod
    def _wildcard_conv(cls, syn, txt, sta): 
        txt_mod = r"[^{wild}{char}]".format(
            wild=txt.lower(), char=cls.CHAR_ILLEGAL
        ); 
        return syn, txt_mod, sta; 
    
    @classmethod
    def _slash_conv(cls, syn, txt, sta): 
        txt_mod = r"[/\\]"; 
        return syn, txt_mod, sta; 
    
    @classmethod
    def _dot_conv(cls, syn, txt, sta): 
        txt_mod = r"[^{char}]".format(char=cls.CHAR_ILLEGAL); 
        return syn, txt_mod, sta; 
    
    #实例方法: 初始化, 对传入的正则表达式语法进行改造后, 构建REAP
    
    def __init__(self, pattern): 
        p = self._to_reap_pattern(pattern); 
        self._regex = re.compile(p); 
        self._input_pattern = pattern; 
       
    #正则表达式语法改造
    
    @classmethod
    def _to_reap_pattern(cls, pattern): 
        p = str(); 
        token_gen = cls.LEX.get_tokens_and_stata(pattern); 
        for syn, txt, sta in token_gen: 
            #处理取反字符集
            if (syn, txt, sta) == (
                cls.LEX.syntax_regex.Delimiter, "[^", "root"
            ):
                syn, txt, sta = cls._left_bracket_caret_conv(syn, txt, sta); 
            #处理字符集内的三种通配符
            if (syn, txt, sta) == (
                cls.LEX.syntax_regex.Delimiter, "[", "root"
            ): 
                syn, txt, sta = cls._left_bracket_conv(syn, txt, sta); 
                wildcards = list(); 
                while (syn, txt, sta) != (
                    cls.LEX.syntax_regex.Delimiter, "]", "charset_incl"
                ): 
                    #收集字符集内的三种通配符, 并将其从字符集方括号内移出
                    if re.match(r"\\[DSW]", txt): 
                        wildcards.append(txt); 
                    else: 
                        p += txt; 
                    syn, txt, sta = next(token_gen); 
                #在字符集方括号以外, 重新添加前述过程收集的通配符
                #如 r"[b\Sar\W]" 转换为 r"(?:[bar]|\S|\W)", 再将通配符替换为目标语法
                for wildcard in wildcards: 
                    syn, wildcard, sta = cls._wildcard_conv(
                        syn, wildcard, sta
                    ); 
                    txt += "|"; 
                    txt += wildcard; 
                txt += ")"
            #处理字符集外的斜杠
            if (syn, txt, sta) == (
                cls.LEX.syntax_regex.Other, "/", "root"
            ): 
                syn, txt, sta = cls._slash_conv(syn, txt, sta); 
            #处理字符集外的点
            if (syn, txt, sta) == (
                cls.LEX.syntax_regex.Wildcard, ".", "root"
            ): 
                syn, txt, sta = cls._dot_conv(syn, txt, sta); 
            #处理字符集外的三种通配符
            elif (syn, sta) == (cls.LEX.syntax_regex.Wildcard, "root"): 
                if re.match(r"\\[DSW]", txt): 
                    syn, txt, sta = cls._wildcard_conv(syn, txt, sta); 
            p += txt; 
        return p; 
         
    @property
    def input_pattern(self):
        return self._input_pattern; 
        
    def __repr__(self): 
        return "{cls!s}({input!r}) -> {comp!r}".format(
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
    