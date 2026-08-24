#-*- coding:utf-8 -*-
#IDL 并行计算调度进程和计算进程 对象模型

import io, sys, os; 

import enum; 

from . import idlpy; 

class IdlSession(object): 
    
    #判断当前IDL会话的解释器是idlpy接口会话, 还是IDL_IDLBridge子会话. 
    #idlpy启动的IDL会话与调用该模块的python解释器属于同一进程; 
    #idlpy的IDL会话中构建的IDL_IDLBridge对象, 控制的IDL子会话使用
    #    独立的进程. 
    
    class Mode(enum.Enum): 
    
        IDL_PARENT = 0; 
        IDL_CHILD = 1; 
        
    #枚举IDL_IDLBridge状态   
        
    class Status(enum.Enum): 

        IDLE = 0; 
        EXECUTING = 1; 
        COMPLETED = 2; 
        ERROR = 3; 
        ABORTED = 4; 
    
    IDL_HOST = idlpy.IDL; 
    
    #属性get: IDL会话解释器
    
    @property
    def interpreter(self): 
        return self._interp; 
    
    #属性get: IDL会话类型
    
    @property
    def mode(self): 
        return self._interp_mode; 
    
    #实例方法: 解析文件路径的绝对路径形式, 移除os.curdir和os.pardir. 
    #当路径是相对于IDL会话工作目录的相对路径时, 解析为从根目录出发的
    #    绝对路径, 因为IDL会话和python解释器的工作目录设置相互独立, 
    #如果不解析为绝对路径, 则os.isfile, os.isdir等函数的执行结果
    #    将出现错误
       
    def abspath(self, path): 
        pwd = self.getcwd(); 
        try: 
            rel_path = os.path.relpath(path, start=pwd); 
        except ValueError: 
            abs_path = path; 
        else: 
            abs_path = os.path.join(pwd, path); 
        abs_path = os.path.normpath(abs_path); 
        return abs_path; 
    
    #实例方法: 指挥IDL解释器加载特定源代码文件中的所有过程和函数, 
    #    但不运行任何过程或函数. 
    
    def compile(self, path): 
        if os.path.isfile(self.abspath(path)): 
            path_esc = path.replace("\x22", "\x22\x22"); 
            self.execute(
                ".compile -v \x22{path!s}\x22".format(path=path_esc)
            ); 
        else: 
            raise IOError("The system cannot find the file specified. "); 
        
    #静态方法: 获取指定的动态链接库 (DLL) 名, 函数名, 用于调用"获取当前
    #    进程PID"函数
    
    @staticmethod
    def _lib_getpid(): 
        #判断操作系统类型, 确认调用的动态链接库及其中函数名称
        #可用性: Windows; 后续将引入对linux的支持
        if sys.platform in ('win32', 'cygwin'): 
            dll_name = 'kernel32.dll'; 
            func_name = 'GetCurrentProcessId'; 
        elif sys.platform.startswith('linux'): 
            raise OSError("Unsupported Operating System"); 
            #当前分支的下述代码尚未在IDL linux版测试过有效性
            #因此本方法暂不支持linux, linux系统执行当前分支
            #将直接抛出上述异常
            #dll_name = 'libc.so.6'; 
            #func_name = 'getpid'; 
        else: 
            raise OSError("Unsupported Operating System"); 
        return dll_name, func_name; 
    
class IdlHost(IdlSession): 
    
    def __init__(self, interp): 
        if interp is self.IDL_HOST: 
            self._interp = interp; 
            self._interp_mode = self.Mode.IDL_PARENT; 
        else: 
            raise RuntimeError(
                "{interp!s} is not a valid IDL session".format(
                    interp=interp
                )
            ); 
    
    #实例方法: 在当前IDL会话执行任意IDL语句
    #生产环境中调用此方法时, 需防范命令注入攻击
    
    def execute(self, command):
        result = self.interpreter.run(command); 
        return result; 
    
    #实例方法: 获取当前IDL会话的工作目录
    
    def getcwd(self): 
        dir_ = self.interpreter.file_expand_path(str()); 
        return dir_; 
    
    #实例方法: 修改当前IDL会话的工作目录
    
    def chdir(self, path): 
        if os.path.isdir(self.abspath(path)): 
            self.interpreter.cd(path); 
        else: 
            raise IOError("The system cannot find the file specified. "); 
            
    #实例方法: 获取当前IDL会话的进程PID
    
    def getpid(self): 
        dll_name, func_name = self._lib_getpid(); 
        pid = self.interpreter.call_external(dll_name, func_name); 
        return pid; 
    
class IdlBridge(IdlSession): 
    
    def __init__(self, interp): 
        if self.IDL_HOST.isa(interp, "IDL_IDLBridge"): 
            self._interp = interp; 
            self._interp_mode = self.Mode.IDL_CHILD; 
        else: 
            raise RuntimeError(
                "{interp!s} is not a valid IDL_IDLBridge".format(
                    interp=interp
                )
            ); 
          
    #实例方法: 在当前IDL会话执行任意IDL语句
    #生产环境中调用此方法时, 需防范命令注入攻击
        
    def execute(self, command, nowait=False):
        result = self.interpreter.execute(command, nowait=nowait); 
        return result; 
    
    #实例方法: 获取当前IDL_IDLBridgeIDL会话的状态
    
    def status(self): 
        num = self.interpreter.status(); 
        sta = self.Status(num); 
        return sta; 

    #实例方法: 获取当前IDL会话的工作目录
    
    def getcwd(self): 
        self.execute("file_expand_path = file_expand_path('')"); 
        dir_ = self.interpreter.getvar("file_expand_path"); 
        return dir_; 
    
    #实例方法: 修改当前IDL会话的工作目录

    def chdir(self, path): 
        if os.path.isdir(self.abspath(path)): 
            self.interpreter.setvar("cd", path); 
            self.execute("cd, cd"); 
        else: 
            raise IOError("The system cannot find the file specified. "); 
    
    #实例方法: 获取当前IDL会话的进程PID
    
    def getpid(self): 
        dll_name, func_name = self._lib_getpid(); 
        self.interpreter.setvar("make_dll", dll_name); 
        self.interpreter.setvar("call_external", func_name); 
        self.execute(
            "call_external = call_external(make_dll, call_external)"
        ); 
        pid = self.interpreter.getvar("call_external"); 
        return pid; 
    