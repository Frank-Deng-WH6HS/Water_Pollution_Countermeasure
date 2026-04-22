# Water_Pollution_Contermeasure

## 概述 / Overview

### 本项目的开发目的 / Aim of Development of This Repository

* 采取遥感数据与实测数据结合的方式, 探究光学, 红外遥感信息(波段反射率等)与水质相关组分间的定量关系; \
    Explore quantitative relationship between information derived from optical and infrared RS (e.g. band reflectance) and components related to water quality via combination of RS data and *in-situ* monitoring data. 
    
* 初期任务: 复现其他已出版学术作品中的反演模型(统计模型或物理模型); \
    Initial target: reproduce inversion model documented in other published academic works. 
    
* 后续任务: 结合机器学习方法构造新模型; \
   Further target: Construct novel models conbined with machine learning or deep learning. 

### 本项目主要涉及的第三方`Python`库 / Third-Party `Python` Libraries Mentioned in This Repository

* 数学建模, 通用科学数据计算相关库. \
    Libraries for mathematical modeling and general scientific data computation. 
    * `numpy`
    * `scipy`
* 数据挖掘, 机器学习, 深度学习相关库. \
     Libraries for data mining, machine learning, and deep learning. 
    * `pandas`
    * `scikit-learn`(`sklearn`)
    * `pytorch`(`torch`)
* `IDL` / `ENVI`的`Python 2.x`接口 (Python to IDL Bridge). \
    `Python 2.x` interface of `IDL` / `ENVI` (Python to IDL Bridge). 
    * `idlpy`
    
## 运行环境需求和限制 / Requirement and Limitation of Environments for Execution

### 系统和程序包配置 / Configuration of System and Packages

|项目<br>Item|值<br>Value|
|:-:|:-|
|CPU架构<br>Architecture of CPU|x86-64|
|GPU架构<br>Architecture of GPU|Nvidia Fermi|
|GPU CUDA计算容量<br>CUDA Compute Campacity of GPU|2.1|
|操作系统内核<br>OS kernel version|Windows NT 6.1.7601|
|`CUDA`版本<br>`CUDA` version|8.0|
|`Conda`管理器版本<br>`Conda` package manager version|`conda 4.7.12` (`python 3.7.4`, `requests 2.22.0`)|
|`Anaconda`发行版<br>`Anaconda` system release version|`anaconda 2019.10`|
|`ArcGIS`发行版<br>`ArcGIS` release version|`ArcGIS Desktop 10.5`|
|`ENVI`/`IDL`发行版<br>`ENVI`/`IDL` release version|`ENVI 5.3`/`IDL 8.5`|

### 环境的主要用途 / Usage of Environments

本项目通过`anaconda`环境管理器, 创建两个环境, 分别名为`idlpy_x64`和`Sklearn_Torch_x64`. 其中`idlpy_x64`集成`idlpy`, `Sklearn_Torch_x64`集成`sklearn`和`torch`的CPU版本 (未适配`CUDA`), 主要依据如下: \
This repository uses `anaconda` environment manager to create two environments named `idlpy_x64` and `Sklearn_Torch_x64` respectively, where `idlpy_x64` intergrates `idlpy`, meanwhile `Sklearn_Torch_x64` integrates `sklearn` and "CPU-only" version `pytorch` which is not compatible with `CUDA`. Criteria are as follow: 

* 遥感影像的覆盖范围内水体应当包含实测数据. \
    Waters covered by extent of RS images must contain *in-situ* monitoring data. 
    * 为后续的基于机器学习的反演模型建立和求解搭建编程计算环境; \
        Construct programming environment for further creation and solution of inversion model based on machine learning; 
    * 编程环境基于`python`, 以充分利用各类科学计算和机器学习程序包生态; \
        Programming environment is based on `python` for full usage of package ecosystem of scientific calculation and machine learning; 
    * 编程环境需与`ENVI/IDL`对接, 以实现高效的遥感数据的输入, 处理和输出工作流. \
        Programming environment docks to `ENVI/IDL`, allowing workflow of effecient input, processing and output of RS data. 
* `torch`程序包支持的`python`解释器版本, 与`idlpy`支持的解释器版本不重叠. \
    `python` intepreter versions, supported by `torch` and `idlpy` respectively, are not overlapped. 
    * `ENVI 5.3` / `IDL 8.5` 提供的`idlpy` 仅可通过`python 2.7`和`python 3.4`解释器调用. \
        `idlpy` provided by `ENVI 5.3` / `IDL 8.5` can be invoked by `python 2.7` and `python 3.4` intepreters. 
    * 可在Windows系统运行的**所有**`pytorch`版本 (0.4版或更高版本), 均不支持上述解释器. \
        **ALL** `pytorch` version supported by Windows platform (version 0.4 or later) fail to be invoked by intepreters above. 
* 硬件条件限制. \
    Restrictions due to hardware conditions. 
    * `pytorch`的部分GPU版本在CU80下编译, 但编译的程序中部分指令未包含在2.1版的指令集内. \
        Certain GPU-supported versions of `pytorch` were compiled based on CUDA 8.0, however, several instructions in compiled programs were not included in the instruction sets of GPU architectures whose computation capacity are 2.1. 
    * `pytorch` 1.x及更高版本中, 除一个特定的1.0.0编译后版本兼容CC 2.0以外, 其他版本兼容的最低CC均在3.0以上; \
        Except for one specific 1.0.0 compiled version supporting computation capacity of 2.0, for **ALL** releases of `pytorch` w/ version 1.x and later, the minimum CC required is 3.0 or higher.
    * `pytorch`社区自0.3版本起, 其兼容性维护的重心就已不再向CC低于3.x的GPU倾斜. \ 
        Since the release of version 0.3, the forum of `pytorch` has shifted its focus of compatibility maintenance away from GPUs with CC versions lower than 3.x. 

> [!IMPORTANT]
>
> 在执行后续操作前, 可能需要关闭反病毒软件和第三方防火墙软件, 因为上述软件可能会阻止`anaconda`从镜像源下载程序包. 
>
> Before execution of following operations, developers are supposed to disable anti-virus softwares and third-party firewalls, which may block `anaconda` from downloading packages from mirror websites. 

## 配置`idlpy_x64`环境 / Configure Integrated Environment of `idlpy_x64`

### 确定`IDL`安装路径 / Verify Installation Path of `IDL` 

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

### 确定`anaconda`安装路径 / Verify Installation Path of `anaconda`

在`Anaconda prompt`命令行中, 将`anaconda`安装目录设置为临时变量. \
In `Anaconda prompt`, set a temporary variable to store the installation path of `anaconda`. 

```bash
set anacon=D:\Anaconda3
```

### 建立并初始化环境 / Create and Initiallize Environment

1. 为建立新环境初始化`anaconda`系统参数. \
    Initialize parameters of `anaconda` for creation of new environment. 

```bash
conda clean -i
```

2. 建立并进入新环境`idlpy_x64`. \
    Create and enter new environment `idlpy_x64`. 

```bash
conda create -n idlpy_x64 python==2.7.12 pip==8.1.1 wheel==0.29.0 six==1.10.0 setuptools==27.2.0 cycler==0.10.0 pyparsing==2.1.4 -y
conda activate idlpy_x64
```

3. 在环境`idlpy_x64`中配置与数据处理有关的包. \
    Configure packages related to data processing in environment `idlpy_x64`. 
    
```bash
conda install numpy==1.11.1 scipy==0.18.1 matplotlib==1.5.3 python-dateutil==2.5.3 pytz==2016.6.1 xlrd==1.0.0 pandas==0.18.1 -c conda-forge -y
conda install scikit-learn==0.17.1 scikit-image==0.12.3 pillow==3.3.1 networkx==1.11 spectral==0.19 -c conda-forge -y
```

4. 在环境`idlpy_x64`中配置与`ipython`有关的包. \
    Configure packages related to `ipython` in environment `idlpy_x64`. 

```bash
conda install notebook==4.2.3 ipykernel==4.5.0 ipython_genutils==0.1.0 jinja2==2.8 jupyter_client==4.4.0 jupyter_core==4.2.0 nbconvert==4.2.0 nbformat==4.1.0 pygments==2.1.3 pyzmq==15.4.0 tornado==4.4.1 -c conda-forge -y
```

5. 在环境`idlpy_x64`下建立`idlpy`的路径配置文件. \
    Create path configuration file of `idlpy` in environment `idlpy_x64`. 

```bash
chdir /D %anacon%\envs\IDL_Machine_Intelligence_x64\Lib\site-packages
echo %idl%\bin\bin.x86-64 >IDL8.5.pth
echo %idl%\lib\bridges >>IDL8.5.pth
```

6. 将环境`idlpy_x64`注册为`ipython`内核, 以便与`base`环境下的`Jupyter notebook`一同使用. \
    Register environment `idlpy_x64` as an `ipython` kernel for use with `Jupyter notebook` in `base` environment. 

```bash
conda install backports.functools_lru_cache -c conda-forge -y
python -m ipykernel install --name idlpy_x64 --display-name "Python 2 (idlpy)"
```

7. 完成环境`idlpy_x64`配置. \
    Finish configuration of environment `idlpy_x64`. 

```bash
conda deactivate
```

## 配置`Sklearn_Torch_x64`环境 / Configure Integrated Environment of `Sklearn_Torch_x64`

### 确定`anaconda`安装路径 / Verify Installation Path of `anaconda`

在`Anaconda prompt`命令行中, 将`anaconda`安装目录设置为临时变量. \
In `Anaconda prompt`, set a temporary variable to store the installation path of `anaconda`. 

```bash
set anacon=D:\Anaconda3
```

### 建立并初始化环境 / Create and Initiallize Environment

1. 为建立新环境初始化`anaconda`系统参数. \
    Initialize parameters of `anaconda` for creation of new environment. 

```bash
conda clean -i
```

2. 建立并进入新环境`Sklearn_Torch_x64`. \
    Create and enter new environment `Sklearn_Torch_x64`. 

```bash
conda create -n Sklearn_Torch_x64 python==3.7.4 pip==19.2.3 setuptools==41.4.0 wheel==0.33.6 -y
conda activate Sklearn_Torch_x64 
```

3. 在环境`Sklearn_Torch_x64`中配置与数据处理有关的包. \
    Configure packages related to data processing in environment `Sklearn_Torch_x64`. 
    
```bash
pip install numpy==1.16.5 scipy==1.3.1 matplotlib==3.1.1 six==1.12.0 --progress-bar ascii
pip install pandas==0.25.1 xlrd==1.2.0 python-dateutil==2.8.0 pytz==2019.3 --progress-bar ascii
pip install scikit-image==0.15.0 pillow==6.2.0 imageio==2.6.0 PyWavelets==1.0.3 networkx==2.3 --progress-bar ascii
pip install spectral==0.20 --progress-bar ascii
```

4. 在环境`Sklearn_Torch_x64`中配置与`ipython`有关的包. \
    Configure packages related to `ipython` in environment `Sklearn_Torch_x64`. 

```bash
pip install notebook==6.0.1 ipykernel==5.1.2 ipython_genutils==0.2.0 jinja2==2.10.3 jupyter_client==5.3.3 jupyter_core==4.5.0 nbconvert==5.6.0 nbformat==4.4.0 prometheus_client==0.7.1 pyzmq==18.1.0 send2trash==1.5.0 terminado==0.8.2 tornado==6.0.3 traitlets==4.3.3 --progress-bar ascii
pip install backports.functools-lru-cache==1.5 --progress-bar ascii
```

5. 在环境`Sklearn_Torch_x64`中配置与机器学习, 深度学习有关的包. \
    Configure packages related to machine learning and deep learning in environment `Sklearn_Torch_x64`. 

```bash
pip install scikit-learn==0.21.3 joblib==0.13.2 --progress-bar ascii
pip install torch==1.7.1+cpu torchvision==0.8.2+cpu -f https://download.pytorch.org/whl/torch_stable.html --progress-bar ascii
```

6. 将环境`Sklearn_Torch_x64`注册为`ipython`内核, 以便与`base`环境下的`Jupyter notebook`一同使用. \
    Register environment `Sklearn_Torch_x64` as an `ipython` kernel for use with `Jupyter notebook` in `base` environment. 

```bash
python -m ipykernel install --name Sklearn_Torch_x64 --display-name "Python 3 (sklearn & torch)"
```

7. 完成环境`Sklearn_Torch_x64`配置. \
    Finish configuration of environment `Sklearn_Torch_x64`. 

```bash
conda deactivate
```
