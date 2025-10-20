#-*- coding:utf-8 -*-

#识别并删除IDL代码中的注释
#需要识别的干扰内容: 字符串

#注释: 一行内分号至行尾之间的内容. 前提: 分号不是字符串的一部分; 
#    IDL不支持在代码中跨行书写注释, 
#    多行注释需要在每一行的注释开头分别添加分号. 

#字符串: 使用一对半角双引号或半角单引号括注的内容, 允许空串; 
#    IDL不支持在代码中跨行书写字符串, 需要拼接; 
#    用双引号括注的字符串可以直接包含单引号, 反之亦然. 
#    字符串中如需包含与其定界符相同的符号, 需要将其重复. 

#注释解析和删除功能, 使用pygments程序包中的对象模型, 自定义语法分析器实现. 
#    该分析器只将字符串, 注释同其他部分相区分. 

#参考文献: 
#[1] NV5 GEOSPATIAL. Defining and Using Constants[EB/OL]. 
#    https://www.nv5geospatialsoftware.com/docs/Defining_and_Using_Const.html.
#[2] NV5 GEOSPATIAL. Special Characters[EB/OL].
#    https://www.nv5geospatialsoftware.com/docs/specchars.html.


from pygments import lexer, token; 

str_delim = {"quote": "\x22", "prime": "\x27"}; 

#IDL注释和字符串语法分析器

class IdlStrRemLexer(lexer.RegexLexer): 
    
    name = "IDL"; 
    
    #语法分析器状态: 
    #    字符串外普通代码, 双引号字符串文本, 
    #    单引号字符串文本, 注释文本. 
    #
    #状态转换规则: 
    #字符串外普通代码: 检测到分号 -> 进入"注释文本", 
    #    分号(含)至换行符(不含)之间均为注释
    #字符串外普通代码: 检测到双引号 -> 进入"双引号字符串文本"
    #字符串外普通代码: 检测到单引号 -> 进入"单引号字符串文本"
    #
    #双引号字符串文本: 检测到连续两个双引号 -> 继续解释为"双引号字符串文本"
    #双引号字符串文本: 检测到单个双引号 -> 返回"字符串外普通代码"
    #
    #单引号字符串文本规则与之相似
    #
    #注释文本: 检测到换行符 -> 返回"字符串外普通代码" (原因: IDL注释不跨行), 
    #    下一行的代码文本重新解释
    
    tokens = {
        "root": [
            (r'{quote}'.format(**str_delim), 
                token.String.Delimiter, "str_quoted"
            ), (r'{prime}'.format(**str_delim), 
                token.String.Delimiter, "str_primed"
            ), (r';', 
                token.Comment.Single, "rem"
            ), (r'[^;{quote}{prime}]+'.format(**str_delim), 
                token.Other
            )
        ], 
        "str_quoted": [
            (r'{quote}{{2}}|{prime}'.format(**str_delim), 
                token.String.Double
            ), (r'{quote}(?!{quote})'.format(**str_delim), 
                token.String.Delimiter, "#pop"
            ), (r'[^\n{quote}]+'.format(**str_delim), 
                token.String.Double
            ), (r'\n', 
                token.Error.SyntaxError, "#pop"
            )
        ], 
        "str_primed": [
            (r'{prime}{{2}}|{quote}'.format(**str_delim), 
                token.String.Single
            ), (r'{prime}(?!{prime})'.format(**str_delim), 
                token.String.Delimiter, "#pop"
            ), (r'[^\n{prime}]+'.format(**str_delim), 
                token.String.Single
            ), (r'\n', 
                token.Error.SyntaxError, "#pop"
            )
        ], 
        "rem": [
            (r'[^\n]+', 
                token.Comment.Single
            ), (r'\n', 
                token.Other, "#pop"
            )
        ]
    }; 
    
lexer = IdlStrRemLexer(); 

#删除IDL代码中的注释, 输入和返回结果均为str, 支持多行文本
  
def idl_remove_comment(code):
    res = str().join(
        tok[1] 
        for tok in lexer.get_tokens(code) 
        if tok[0] is not token.Comment.Single
    ); 
    return res; 