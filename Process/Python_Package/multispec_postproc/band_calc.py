#波段计算工具

from . import it, np; 

#波段四则运算器

class BandMath(object): 
    
    OPERATIONS = {
        np.add: "+", np.subtract: "-", 
        np.multiply: "*", np.true_divide: "/"
    }; 
    
    #实例初始化
    #    BandMath(x): 只使用第 (x + 1) 波段的值; 
    #    BandMath(x, oper, y): 将第 (x + 1) 波段和第 (y + 1) 波段进行四则运算; 
    #    x 和 y 为 np.ndarray 的索引下标, 第一个元素的索引为0. 
    #    支持的四则运算符: 加, 减, 乘, 浮点除. 
    
    def __init__(self, operand_1=0, operation=None, operand_2=None): 
        op_1 = operand_1; 
        op_2 = operand_2; 
        oper = operation; 
        if op_2 == None: #一元运算
            if oper is not None: 
                raise ValueError; 
            self.expr = "b{op_1}".format(
                op_1=op_1 + 1
            ); 
            self._func = lambda x: x[op_1]; 
        else: #二元运算
            if oper not in self.OPERATIONS: 
                raise ValueError; 
            self.expr = "b{op_1} {op} b{op_2}".format(
                op_1=op_1 + 1, op_2=op_2 + 1, 
                op=self.OPERATIONS[oper]
            ); 
            self._func = lambda x: oper(x[op_1], x[op_2]); 
            
    #实例方法: 显示形式
    #    BandMath(0) 在解释器 CLI 会话中显示为 BandMath(b1)
    #    BandMath(0, np.add, 1) 在解释器 CLI 会话中显示为 BandMath(b1 + b2)
    
    def __repr__(self): 
        return "{cls!s}({expr})".format(
            cls=self.__class__.__name__, expr=self.expr
        ); 
    
    #实例方法: 调用波段运算功能
    #    输入类型: list, tuple, array.array 或 np.ndarray
    #    输入类型为 np.ndarray 时, 若 ndim == 2 (矩阵), 要求矩阵形状为 n 行 m 列, 
    #    其中, n为波段数, m为样本数, 样本使用列向量表示, 每行代表一个波段. 
    #    此时将利用 np 的向量化机制实现批量计算. 
        
    def __call__(self, spec): 
        return self._func(spec); 
       
#波段最优指数因子 (OIF) 运算器

class OptimumIndexFactor(object): 
    
    #实例初始化
    
    def __init__(self, bands): 
        if len(bands) == 0: 
            raise ValueError; 
        self.bands = np.array(bands, dtype=np.uint16); 
        self.bands.sort(); 
    
    #实例方法: 调用OIF计算功能    
    #    输入类型需要具有转化为 np.ndarray 的能力, 
    #    且转换后的 np.ndarray 满足 ndim == 2 (矩阵), 形状为 n 行 m 列, 
    #    其中, n为波段数, m为样本数, 样本使用列向量表示, 每行代表一个波段. 
    #    此时将利用 np 的向量化机制实现批量计算. 
    
    def __call__(self, spec): 
        spec_arr = np.array(spec)[self.bands]; 
        if spec_arr.ndim != 2: 
            raise ValueError; 
        #计算每个波段的标准差
        stdev_by_bands = np.std(spec_arr, axis=1); 
        #计算波段两两组合的相关系数之绝对值
        comb_2 = it.combinations(range(len(self.bands)), 2); 
        corr_by_2_bands = np.array([
            np.corrcoef(spec_arr[[band_i, band_j]])[0, 1]
            for band_i, band_j in comb_2
        ] ); 
        abs_corr_by_2_bands = np.abs(corr_by_2_bands)
        #计算OIF
        oif = np.sum(stdev_by_bands) / np.sum(abs_corr_by_2_bands); 
        return oif; 