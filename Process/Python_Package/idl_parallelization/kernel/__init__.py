#-*- coding:utf-8 -*-
#IDL 并行计算调度进程和计算进程 对象模型

class IdlSession(object): 
    
    class Mode(enum.Enum): 
    
        IDL_PARENT = 0; 
        IDL_CHILD = 1; 
        
    class Status(enum.Enum): 

        IDLE = 0; 
        EXECUTING = 1; 
        COMPLETED = 2; 
        ERROR = 3; 
        ABORTED = 4; 
    
    IDL_HOST = idlpy.IDL; 
    
    @property
    def interpreter(self): 
        return self._interp; 
    
    @property
    def mode(self): 
        return self._interp_mode; 
       
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
    
    def compile(self, path): 
        if os.path.isfile(self.abspath(path)): 
            path_esc = path.replace("\x22", "\x22\x22"); 
            self.execute(
                ".compile -v \x22{path!s}\x22".format(path=path_esc)
            ); 
        else: 
            raise IOError("The system cannot find the file specified. "); 
        
    def _lib_getpid(self): 
        #判断操作系统类型, 确认调用的动态链接库及其中函数名称
        #可用性: Windows; 后续将引入对linux的支持
        if sys.platform in ('win32', 'cygwin'): 
            dll_name = 'kernel32.dll'; 
            func_name = 'GetCurrentProcessId'; 
        elif sys.platform.startswith('linux'): 
            raise OSError("Unsupported Operating System"); 
            #当前分支的下述代码尚未在IDL linux版测试过有效性
            #因此本方法暂不支持linux, linux系统执行当前分支将直接抛出上述异常
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
            
    def execute(self, command):
        result = self.interpreter.run(command); 
        return result; 
    
    def getcwd(self): 
        dir_ = self.interpreter.file_expand_path(str()); 
        return dir_; 
    
    def chdir(self, path): 
        if os.path.isdir(self.abspath(path)): 
            self.interpreter.cd(path); 
        else: 
            raise IOError("The system cannot find the file specified. "); 
            
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
            
    def execute(self, command, nowait=False):
        result = self.interpreter.execute(command, nowait=nowait); 
        return result; 
    
    def status(self): 
        num = self.interpreter.status(); 
        sta = self.Status(num); 
        return sta; 
    
    def getcwd(self): 
        self.execute("file_expand_path = file_expand_path('')"); 
        dir_ = self.interpreter.getvar("file_expand_path"); 
        return dir_; 
    
    def chdir(self, path): 
        if os.path.isdir(self.abspath(path)): 
            self.interpreter.setvar("cd", path); 
            self.execute("cd, cd"); 
        else: 
            raise IOError("The system cannot find the file specified. "); 
    
    def getpid(self): 
        dll_name, func_name = self._lib_getpid(); 
        self.interpreter.setvar("make_dll", dll_name); 
        self.interpreter.setvar("call_external", func_name); 
        self.execute(
            "call_external = call_external(make_dll, call_external)"
        ); 
        pid = self.interpreter.getvar("call_external"); 
        return pid; 
    