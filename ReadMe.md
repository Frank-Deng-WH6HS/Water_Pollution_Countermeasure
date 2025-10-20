# Water_Pollution_Contermeasure

## 概述 / Overview

### 本项目的开发目的 / Aim of Development of This Repository

* 采取遥感数据与实测数据结合的方式, 探究光学, 红外遥感信息(波段反射率等)与水质相关组分间的定量关系; \
    Explore quantitative relationship between information derived from optical and infrared RS (e.g. band reflectance) and components related to water quality via combination of RS data and *in-situ* monitoring data. 
    * 初期复现其他已出版学术作品中的反演模型(统计模型或物理模型); \
        Initial target: reproduce inversion model documented in other published academic works. 
    * 后续将结合机器学习方法构造新模型; \
        Further target: Construct novel models conbined with machine learning. 

### 本项目主要涉及的第三方`Python`库 / Third-Party `Python` Libraries Mentioned in This Repository

* 数学建模, 通用科学数据计算相关库. \
    Libraries for mathematical modeling, data mining and general scientific data computation. 
    * `numpy`
    * `scipy`
* 数据挖掘, 机器学习相关库. \
     Libraries for data mining and machine learning. 
    * `pandas`
    * `scikit-learn`(`sklearn`)
* `IDL` / `ENVI`的`Python 2.x`接口 (Python to IDL Bridge). \
    `Python 2.x` interface of `IDL` / `ENVI` (Python to IDL Bridge). 
    * `idlpy`
    
## 运行环境信息 / Information of Environment for Execution

### 系统和程序包环境 / Environment of System and Packages

|项目<br>Item|值<br>Value|
|:-:|:-|
|处理器架构<br>Architecture of processor|Intel x86-64|
|操作系统内核<br>OS kernel version|Windows NT 6.1.7601|
|`Conda`管理器版本<br>`Conda` package manager version|`conda 4.7.12` (`python 3.7.4`, `requests 2.22.0`)|
|`Anaconda`发行版<br>`Anaconda` system release version|`anaconda 2019.10`|
|`ArcGIS`发行版<br>`ArcGIS` release version|`ArcGIS Desktop 10.5`|
|`ENVI`发行版<br>`ENVI` release version|`ENVI 5.3`|

### 配置`idlpy`, `sklearn`和`keras`集成环境 / Configure Integrated Environment of `idlpy`, `sklearn` and `keras`

本项目通过`anaconda`环境管理器, 创建一个名为`IDL_Machine_Intelligence_x64`的子环境, 集成`idlpy`, `sklearn`和`keras`以供数据处理和机器学习使用, 主要依据如下: \
This repository creates an environment named `IDL_Machine_Intelligence_x64` via `anaconda` environment manager, which intergrates `idlpy`, `sklearn` and `keras` for data processing and machine learning, criteria are as follow: 

* 遥感影像的覆盖范围内水体应当包含实测数据. \
    Waters covered by extent of RS images must contain *in-situ* monitoring data. 
    * 为后续的基于机器学习的反演模型建立和求解搭建编程计算环境; \
        Construct programming environment for further creation and solution of inversion model based on machine learning; 
    * 编程环境基于`python`, 以充分利用各类科学计算和机器学习程序包生态; \
        Programming environment is based on `python` for full usage of package ecosystem of scientific calculation and machine learning; 
    * 编程环境需与`ENVI/IDL`对接, 以实现高效的遥感数据的输入, 处理和输出工作流. \
        Programming environment docks to `ENVI/IDL`, allowing workflow of effecient input, processing and output of RS data. 

> [!IMPORTANT]
>
> 在执行后续操作前, 可能需要关闭反病毒软件和第三方防火墙软件, 因为上述软件可能会阻止`anaconda`从镜像源下载程序包. 
>
> Before execution of following operations, developers are supposed to disable anti-virus softwares and third-party firewalls, which may block `anaconda` from downloading packages from mirror websites. 

#### 确定`IDL`安装路径 / Verify Installation Path of `IDL` 

在`Anaconda prompt`命令行中, 将`IDL`安装目录设置为临时变量. \
In `Anaconda prompt`, set a temporary variable to store the installation path of `IDL` interpreter. 

```bash
set idl=D:\Exelis\IDL85
```

> [!NOTE]
> 上述路径**不是IDL的解释器**(`idl.exe`或者`idlrt.exe`)所在的路径. 
>
> 路径下包含`bin`, `examples`, `external`, `help`, `lib`, `resource`等子目录. 
>
> Path above is **NOT** the path where **the interpreters of IDL** (`idl.exe` or `idlrt.exe`) locate. 
>
> This path contains subdirectories including `bin`, `examples`, `external`, `help`, `lib`, `resource`. 

> [!IMPORTANT]
> 临时变量的值仅在**当前命令行会话**中有效, 命令行关闭后将被清理或者复原. 
>
> 执行上述命令后, 请勿关闭命令行界面, 以便在后续命令中继续使用临时变量. 后续操作均在**同一控制台**中执行. 
>
> Values of temporary variables are valid in CURRENT CLI SESSION ONLY and will be cleared or restored after closing the console. 
>
> After excuting command above, do NOT close CLI, so that variables can be reused in following commands. Further operations will be executed in THE SAME CONSOLE. 

#### 确定`anaconda`安装路径 / Verify Installation Path of `anaconda`

在`Anaconda prompt`命令行中, 将`anaconda`安装目录设置为临时变量. \
In `Anaconda prompt`, set a temporary variable to store the installation path of `anaconda`. 

```bash
set anacon=D:\Anaconda3
```

#### 建立并初始化环境 / Create and Initiallize Environment

1. 为建立新环境初始化`anaconda`系统参数. \
    Initialize parameters of `anaconda` for creation of new environment. 

```bash
conda clean -i
```

2. 建立并进入新环境`IDL_Machine_Intelligence_x64`. \
    Create and enter new environment `IDL_Machine_Intelligence_x64`. 

```bash
conda create -n IDL_Machine_Intelligence_x64 python==2.7.12 pip==8.1.1 wheel==0.29.0 six==1.10.0 setuptools==27.2.0 cycler==0.10.0 pyparsing==2.1.4 -y
conda activate IDL_Machine_Intelligence_x64
```
3. 在新环境中配置与数据处理和机器学习有关的包. \
    Configure packages related to data processing and machine learning. 
    
```bash
conda install numpy==1.11.1 scipy==0.18.1 matplotlib==1.5.3 python-dateutil==2.5.3 pytz==2016.6.1 pandas==0.18.1 -c conda-forge -y
conda install scikit-learn==0.17.1 scikit-image==0.12.3 networkx==1.11 pillow==3.3.1 -c conda-forge -y
conda install spectral==0.19 -c conda-forge -y
```

4. 在新环境中配置与`ipython`有关的包. \
    Configure packages related to `ipython` in new environment. 

```bash
conda install notebook==4.2.3 ipykernel==4.5.0 ipython_genutils==0.1.0 jinja2==2.8 jupyter_client==4.4.0 jupyter_core==4.2.0 nbconvert==4.2.0 nbformat==4.1.0 pygments==2.1.3 pyzmq==15.4.0 tornado==4.4.1 -c conda-forge -y
```

5. 在新环境下建立`idlpy`的路径配置文件. \
    Create path configuration file of `idlpy` in new environment. 

```bash
chdir /D %anacon%\envs\IDL_Machine_Intelligence_x64\Lib\site-packages
echo %idl%\bin\bin.x86-64 >IDL8.5.pth
echo %idl%\lib\bridges >>IDL8.5.pth
```

6. 在新环境下配置与天文计算有关的包. \
    Configure pacages related to astometry and astromechanics. 
    
```bash
pip install ephem==3.7.6 -i https://www.pypi.org/simple --force-reinstall
```
> [!TIP]
> 在遥感数据预处理流程中, 天文计算包`ephem`主要用于解析卫星轨道参数, 计算星下点轨迹, 卫星倾角, 以及观测地的太阳方位角, 高度角等工作. 

7. 在新环境下配置深度学习程序包及其支持库. \
    Configure deep-learning package and its supportive libraries. 

```bash
conda install h5py==2.6.0 hdf5==1.8.17 openssl -y
pip install keras==1.0.7 theano==0.8.2 pyyaml==5.1.2 -i https://www.pypi.org/simple --force-reinstall
```

8. 在新环境下配置`keras`所需的其他辅助库, 包括C++编译器, 自动测试工具等. \
    Configure other auxillary libraries for `keras`, including C++ compilers and automated testing tools. 
    
```bash
conda install m2w64-toolchain==5.3.0 -c conda-forge -y
conda install libpython==2.0 -c conda-forge -y
pip install nose==1.3.7 nose_parameterized -i https://www.pypi.org/simple --force-reinstall
```

9. 将新环境注册为`ipython`内核, 以便与`base`环境下的`Jupyter notebook`一同使用. \
    Register new environment as an `ipython` kernel for use with `Jupyter notebook` in `base` environment. 

```bash
pip install backports.functools_lru_cache
ipython kernelspec install-self
```
> [!NOTE]
> 如果内核注册不成功(发生报错), 一般是因为`pip`未能向环境内成功安装上述库, 如遇上述现象, 需要再通过`conda`安装该库. 
>
> The faliure of kernel registration is generally caused by faliure of installation of library above via `pip`, In case of phenomenon above, it is required to install this library via `conda` again. 
>
> ```bash
> conda install backports.functools_lru_cache -y
> ```

10. 完成新环境配置. \
    Finish configuration of new environment. 

```bash
conda deactivate
```
