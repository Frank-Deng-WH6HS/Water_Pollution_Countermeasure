#-*- coding:utf-8 -*-
#IDL 并行计算管理工具包

import io, sys, os; 

_ = sys.stdout; 
with io.BytesIO() as sys.stdout: import idlpy; 
sys.stdout = _; 

from .utils import importlib, isidentifier as _isidentifier; 
from .kernel import IdlHost, IdlBridge; 
IdlHost(); 