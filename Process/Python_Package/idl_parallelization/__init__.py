#-*- coding:utf-8 -*-
#IDL 并行计算管理工具包

import io, sys, os; 

import numpy as np; 

from .utils import importlib, isidentifier as _isidentifier; 
from .kernel import idlpy, IdlHost, IdlBridge; 
IdlHost(); 