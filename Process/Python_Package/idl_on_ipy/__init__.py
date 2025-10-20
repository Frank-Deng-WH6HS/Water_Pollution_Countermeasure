#-*- coding:utf-8 -*-

#ipython解释器的IDL魔术命令扩展包. 
#用于ipython命令行和jupyter notebook输入单元中, 执行IDL命令和代码

#必要的依赖包: ipython, pygments, idlpy
#推荐与numpy一同使用

import io, sys, os; 
import IPython as ipy, IPython.core.magic as ipym; 

from . import idl_script_parse; 
from . import idl_magics; 
    