#多光谱数据后处理

#必要的依赖包: numpy

import io, sys, os; 
import itertools as it; 

import numpy as np; 

from .band_calc import BandMath, OptimumIndexFactor; 