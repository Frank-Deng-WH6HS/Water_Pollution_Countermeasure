#-*- coding:utf-8 -*-
#sklearn回归模型探索工具

#必要的依赖包: numpy, scikit-learn
#推荐与matplotlib一同使用

import numpy as np; 
import sklearn.base; 
from sklearn import cross_validation, grid_search; 

from sklearn.metrics import mean_squared_error as MSE, r2_score as R2; 

try: 
    from matplotlib import pyplot as plt; 
except ImportError: 
    pass; 

#回归模型探索工具对象
class RegressorExplorer(object): 
    
    def __init__(self): 
        self._estm_cls = sklearn.base.BaseEstimator; #回归模型的类
        self._param_fix = dict(); #模型中无需搜索的超参数, 及其取值
        self._param_var = dict(); #模型中需要搜索的超参数, 及其取值范围
        self._param_walker_cls = grid_search.BaseSearchCV; #用于超参数搜索的类
        self._param_walker_inst = None; #超参数搜索对象的实例
        self._cv = None; #交叉验证模式
        self._x_train = np.empty((0, )); #训练集指示变量
        self._yt_train = np.empty((0, )); #训练集预报变量实测值
        self._x_test = np.empty((0, )); #测试集指示变量
        self._yt_test = np.empty((0, )); #测试集预报变量实测值

    #属性 get/set: 使用的回归模型
    
    @property
    def estimator(self): 
        return self._estm_cls; 
    
    @estimator.setter
    def estimator(self, estm): 
        self._estm_cls = estm; 
        
    #属性 get/set: 无需搜索的超参数
    
    @property
    def fixed_parameters(self): 
        return self._param_fix; 
    
    @fixed_parameters.setter
    def fixed_parameters(self, params): 
        self._param_fix = params; 
            
    #属性 get/set: 需要搜索的超参数
    
    @property
    def variable_parameters(self): 
        return self._param_var; 
    
    @variable_parameters.setter
    def variable_parameters(self, params): 
        self._param_var = params; 
        
    #属性 get/set: 使用的超参数搜索方法
    
    @property
    def searching_method(self): 
        return self._param_walker_cls; 
    
    @searching_method.setter
    def searching_method(self, mthd): 
        self._param_walker_cls = mthd; 
        
    #属性 get/set: 超参数搜索过程中的交叉验证模式
    
    @property
    def cross_validation(self): 
         return self._cv; 
        
    @cross_validation.setter
    def cross_validation(self, cv_cfg): 
        self._cv = cv_cfg; 
     
    #属性 get/set: 训练集解释变量
    @property
    def training_set_x(self): 
        return self._x_train; 
        
    @training_set_x.setter
    def training_set_x(self, ts): 
        self._x_train = ts;  
        
    #属性 get/set: 训练集预报变量实测值
    @property
    def training_set_y_target(self): 
        return self._yt_train; 
        
    @training_set_y_target.setter
    def training_set_y_target(self, ts): 
        self._yt_train = ts;  
        
    #属性 get/set: 测试集解释变量
    @property
    def test_set_x(self): 
        return self._x_test; 
        
    @test_set_x.setter
    def test_set_x(self, ts): 
        self._x_test = ts; 
        
    #属性 get/set: 测试集预报变量实测值
    @property
    def test_set_y_target(self): 
        return self._yt_test; 
        
    @test_set_y_target.setter
    def test_set_y_target(self, ts): 
        self._yt_test = ts; 
    
    #实例方法: 利用数据集训练某种指定的模型. 其中超参数使用给定的方法搜索, 
    #使用交叉验证评估模型性能, 确定使模型性能最优的超参数组合
    
    def evaluate(self, **kw): 
        #指定模型中无需搜索的超参数
        estm = self._estm_cls(**self._param_fix); 
        #初始化超参数搜索器对象
        kwargs_rm_cv = kw; 
        try: 
            kwargs_rm_cv.pop("cv"); 
        except KeyError: 
            pass; 
        self._param_walker_inst = self._param_walker_cls(
            estm, self._param_var, cv=self._cv, 
            **kwargs_rm_cv
        ); 
        #搜索超参数组合, 训练模型并交叉验证
        self._param_walker_inst.fit(
            self._x_train, self._yt_train
        ); 
        #向当前实例添加训练结果
            #最佳模型及其参数搜索结果
        self._estm_optm = self._param_walker_inst.best_estimator_; 
        self._param_optm = self._param_walker_inst.best_params_; 
            #最佳模型通过交叉验证所得的评分: 各折评分及其均值
        grid_sco = self._param_walker_inst.grid_scores_; 
        self._score_optm = next(
            rec.__dict__ for rec in grid_sco 
            if rec.parameters == self._param_optm
        ); 
        self._score_optm.pop("parameters"); 
        
    #属性 get: 最佳模型
    
    @property
    def optimal_estimator(self): 
        return self._estm_optm; 
    
    #属性 get: 最佳模型对应的超参数组合
    
    @property
    def optimal_parameters(self): 
        return self._param_optm; 
    
    #属性 get: 最佳模型通过交叉验证所得的评分: 各折评分及其均值
    
    @property
    def optimal_score(self): 
        return self._score_optm; 
        
    #属性 get: 测试集在最佳模型下的预测结果
    
    @property
    def test_set_y_prediction(self): 
        return self._estm_optm.predict(self._x_test); 
    
    #在解释器中直接查看实例时的文本显示
    
    def __repr__(self): 
        return "{cls!s}(id={id})".format(
            cls=self.__class__.__name__, id=id(self)
        ); 