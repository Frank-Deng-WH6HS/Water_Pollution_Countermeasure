; CBERS-04 卫星 MUX 载荷辐亮度数据大气校正
; 输入数据为 ENVI 辐射定标后的辐亮度
; 需要采用"Apply FLAASH Settings"选项 

; ENVI 5.3 / IDL 8.5 预留了 flaash_batch 接口, 后续的更高版本
;     进一步开放了 FLAASH 大气校正的 ENVITask, 但在 ENVI 5.3 
;     中不能通过 IDL 调用此 ENVITask, 该版本的文档中也未告知
;     用户通过 IDL 编程调用 flaash_batch 接口的手段. 

; 声明: 本程序部分内容参考赵冠华 (CNKI: https://kns.cnki.net/
;     kcms2/author/detail?v=uxn9QsgV9c97KMcCchqj0toB383
;     k4bt0GaTHQEovTbdtdf_g4zXYvPr1FfTnWAizvGvznh20foAt
;     rsXj4t4ohq-j3oXj_l8BNNxzuRi-LXPzBFw3aFw3vl8mhIlOB
;     uWs7k4eDl8r2AxSjPDS81CaDQ/ ) (GitHub: https://www.
;     github.com/Zhaoguanhua) 的代码

; 参考文献: 
; [1] ZHAO G. ProgramLearning/IDL/ENVI_FLAASH_Batch/
;     test_flaash_object_class_multi2.pro at 3b329826
;     38ff16cb5e71c7f7f7ce150c936b5bc7 · Zhaoguanhua/
;     ProgramLearning[EB/OL]. (2017-10-27). https://
;     www.github.com/Zhaoguanhua/ProgramLearning/blob/
;     3b32982638ff16cb5e71c7f7f7ce150c936b5bc7/IDL/
;     ENVI_FLAASH_Batch/test_flaash_object_class_multi2.pro

Function FLAASH_PATH_PROC, uri_input, uri_output
  ; 大气校正前, 辐亮度影像路径
  rad_path = File_Expand_Path(uri_input)
  ; 大气校正后, 地表反射率影像路径
  boar_path = File_Expand_Path(uri_output)
  boar_base = File_basename(boar_path, '.dat')
  ; 大气校正过程的 FLAASH 中间数据存放路径
  flaash_dir = File_dirname(boar_path)
  flaash_dir = flaash_dir
  flaash_dir = flaash_dir + Path_Sep() + boar_base + Path_Sep()
  ; 大气校正过程的 FLAASH 中间数据文件前缀
  flaash_prefix = boar_base + "_"
  ; 组合结果
  flaash_paths = { $
    input_radiance: rad_path, $
    output_reflectance: boar_path, $
    intermediate_dir: flaash_dir, $
    intermediate_prefix: flaash_prefix $
  }
  return, flaash_paths
End

Function HMS_TO_FLAASH_GMT, hms_ut
  hms_diff = hms_ut / [1., 60., 3600.]
  gmt = Total(hms_diff)
  Return, gmt
End

Pro CB04_MUX_FLAASH, $
  uri_input, $ ; 输入文件路径
  uri_output, $ ; 输出文件路径
  SCENE_CENTER_LAT=scene_center_lat, $ ; 影像中心纬度 (十进制度)
  SCENE_CENTER_LONG=scene_center_long, $ ; 影像中心经度 (十进制度)
  GROUND_ELEVATION=ground_elevation, $ ; 影像平均海拔 (公里)
  SCENE_DATE_TIME=scene_date_time, $ ; 成像时间 (年月日时分秒)
  ATMOSPHERIC_MODEL=atmospheric_model, $ ; 大气模型
  AEROSOL_MODEL=aerosol_model, $ ; 气溶胶模型
  FILTER_FUNCTION_FILE=filter_function_file ; 光谱响应函数路径

  e = Envi()
  
  ; 初始化 FLAASH 大气校正接口实例
  flaash = Obj_New("flaash_batch")
  
  ; 设置 CB04 MUX 大气校正中的固定参数
    ; 传感器模式: 多光谱
    ;   因为 CB04 MUX 为多光谱传感器
  flaash->SetProperty, hyper=0
    ; 光谱卷积方法: 快速 Fourier 变换
    ;   FLAASH 默认值
  flaash->SetProperty, convolution_method="fft"
    ; 传感器高度: 778 km
    ;   CBERS-04 卫星轨道标称高度
  flaash->SetProperty, sensor_altitude=778.e
    ; 水汽反演 (Water Retrieval): 禁用
    ;   因为 CB04 MUX 波段中, 近红外波段 FHWM 过大
  flaash->SetProperty, water_retrieval=0
    ; 水汽等效厚度因数 (Water Column Multiplier): 1.00
    ;   FLAASH 在禁用水汽反演时的默认值
  flaash->SetProperty, water_column_multiplier=1.00e
    ; 气溶胶反演  (Aerosol Retrieval): 禁用
    ;   因为 CB04 MUX 波段中, 未包含 2.1 μm 短波红外波段
  flaash->SetProperty, aerosol_retrieval=0
    ; 初始能见度: 40.00 km
    ;   FLAASH 默认值
  flaash->SetProperty, visvalue=40.00e
    ; 传感器类型: 未知多光谱传感器
    ;   CB04 MUX 技术参数未被 ENVI 5.3 原生收录
  flaash->SetProperty, sensor_name='UNKNOWN-MSI'
    ; 光谱响应函数首波段索引值: 0
    ;   手动指定的光谱响应函数 sli 文件中, 第 0 项即为首波段
  flaash->SetProperty, filter_func_file_index=0
    ; 气溶胶缩放高度 (Aerosol Scale Height): 1.50 km
    ;   FLAASH 默认值
  flaash->SetProperty, aerosol_scaleht=1.50e
    ; 二氧化碳体积分数: 390.00 ppm
    ;   FLAASH 默认值
  flaash->SetProperty, co2mix=390.00e
    ; 使用"矩形窗函数" (Use Square Slit Function): 禁用
    ;   FLAASH 默认值
  flaash->SetProperty, use_square_slit_function=0
    ; 使用"邻近像元校正": 启用
    ;   FLAASH 默认值
  flaash->SetProperty, use_adjacency=1
    ; 复用之前的 MODTRAN 计算结果: 禁用
    ;   FLAASH 默认值
  flaash->SetProperty, reuse_modtran_calcs=0
    ; MODTRAN 模型光谱分辨率: 15 cm^{-1}
    ;   FLAASH 在采用多光谱传感器时的默认值
  flaash->SetProperty, f_resolution=15
    ; MODTRAN 多重散射模型: Scaled DISORT
    ;   FLAASH 默认值
  flaash->SetProperty, multiscatter_model=2
    ; DISORT / Scaled DISORT 模型的散射方向数目: 8
    ;   FLAASH 默认值
  flaash->SetProperty, disort_streams=8
    ; 卫星天顶角: 180.00000000°
    ;   FLAASH 默认值, 卫星垂直观测 (无侧摆)
    ;   同一景影像不同像元的卫星天顶角, 方位角差异无法输入至 FLAASH
  flaash->SetProperty, view_zenith_angle=180.00000000e
    ; 卫星方位角: 0.00000000°
    ;   FLAASH 默认值
  flaash->SetProperty, view_azimuth=0.00000000e
    ; 分块处理: 禁用
    ;   因为 CB04 MUX 标准景 4 波段数据, 经辐射定标为 fp32 形式
    ;   的辐亮度影像后, 每景影像大小约 500~1000 MB, 在 RAM 大于 
    ;   4 GB 的计算机上处理时可一次完成, 无需分块
  flaash->SetProperty, use_tiling=0
    ; 反射率缩放系数: 10000.0000
    ;   FLAASH 默认值, 因为 FLAASH 输出结果存储为 signed int16
    ;   考虑到 CB04 MUX 的每波段量化等级只有 8 位, 此设置绰绰有余
  flaash->SetProperty, output_scale=10000.0000e
  
  ; 处理输入输出路径
  flaash_path = FLAASH_PATH_PROC(uri_input, uri_output)
  File_Mkdir, File_Dirname(flaash_path.output_reflectance)
  File_Mkdir, flaash_path.intermediate_dir
  ; 加载影像, 读取与影像有关的参数
  rad = e.OpenRaster(uri_input)
  ; 初始化元数据读取接口
  raster_mdin = EnviTask("RasterMetadataItem")
  raster_mdin.input_raster = rad
  ; 参与校正的影像范围
  n_rows = rad.nrows
  n_columns = rad.ncolumns
  ; 像元的数据类型
  fid_rad = EnviRasterToFid(rad)
  Envi_File_Query, fid_rad, DATA_TYPE=data_type
  ; 辐亮度缩放倍数数组, 元素数量等于波段数量, 每个波段的缩放
  ; 倍数均为 1, 因为其单位符合 FLAASH 输入要求
  n_bands = rad.nbands
  input_scale = Make_Array(n_bands, VALUE=1.d)
  ; 像元大小, 如果 X 和 Y 方向像元大小不同, 取较小者
  spatref = rad.spatialref
  pixel_size = spatref.pixel_size
  pixel_size = Min(pixel_size)
  ; 波长单位
  raster_mdin.key = "wavelength units"
  raster_mdin.execute
  wl_unit = raster_mdin.value
  ; 各波段中心波长
  raster_mdin.key = "wavelength"
  raster_mdin.execute
  wl = raster_mdin.value
  ; 各波段半峰全宽
  raster_mdin.key = "fwhm"
  raster_mdin.execute
  fwhm = raster_mdin.value
  rad.close
  
  ; 设置 CB04 MUX 大气校正中, 与影像路径, 元数据有关的参数
    ; 输入输出路径
  flaash->SetProperty, $
    radiance_file=flaash_path.input_radiance
  flaash->SetProperty, $
    reflect_file=flaash_path.output_reflectance
  flaash->SetProperty, $
    modtran_directory=flaash_path.intermediate_dir
  flaash->SetProperty, $
    user_stem_name=flaash_path.intermediate_prefix
    ; 影像数据组织形式
  flaash->SetProperty, nspatial=n_columns
  flaash->SetProperty, nlines=n_rows
  flaash->SetProperty, data_type=data_type
    ; 影像空间信息
  flaash->SetProperty, pixel_size=pixel_size
    ; 影像光谱信息
  flaash->SetProperty, wavelength_units=wl_unit
  flaash->SetProperty, lambda=wl
  flaash->SetProperty, fwhm=fwhm
    ; 影像辐射信息
  flaash->SetProperty, input_scale=input_scale
  
  ; 设置 CB04 MUX 大气校正中, 由传入的关键字参数指定的参数
  year = scene_date_time[0]
  month = scene_date_time[1]
  day = scene_date_time[2]
  gmt = HMS_TO_FLAASH_GMT(scene_date_time[3:5])
  flaash->SetProperty, latitude=scene_center_lat
  flaash->SetProperty, longitude=scene_center_long
  flaash->SetProperty, ground_elevation=ground_elevation
  flaash->SetProperty, year=year
  flaash->SetProperty, month=month
  flaash->SetProperty, day=day
  flaash->SetProperty, gmt=gmt
  flaash->SetProperty, atmosphere_model=atmospheric_model
  flaash->SetProperty, aerosol_model=aerosol_model
  flaash->SetProperty, filter_func_filename=filter_function_file
  
  ; 执行大气校正
  flaash->ProcessImage
  
  ; 大气校正完成后, 大部分中间文件将被 ENVI 自动删除, 但仍需另行
  ;   执行代码删除部分残留文件
  modtran_solve_path = $
    flaash_path.intermediate_dir + Path_Sep() + "mod5root.in" 
  File_Delete, modtran_solve_path, $
    /ALLOW_NONEXISTENT, /QUIET
  ; 如果存放中间文件的目录为空目录, 说明该目录系本次大气校正期间
  ;   临时创建, 可删除
  intermediate_dir = $
    File_Expand_Path(flaash_path.intermediate_dir)
  File_Delete, intermediate_dir, $
    /ALLOW_NONEXISTENT, /QUIET
  
  ; 更新元数据, 并关闭 FLAASH 大气校正输入和输出文件 
  flaash->GetResults, rad_fid=rad_fid
  flaash->GetResults, reflect_fid=reflect_fid
  rad = EnviFidToRaster(rad_fid)
  band_names = rad.metadata["band names"]
  rad.close
  reflect = Envifidtoraster(reflect_fid)
  mdata = reflect.metadata
  mdata.RemoveItem, 'description'
  mdata.RemoveItem, 'sensor type'
  mdata.RemoveItem, 'data units'
  mdata.RemoveItem, 'bbl'
  mdata.RemoveItem, 'calibration scale factor'
  mdata.UpdateItem, 'band names', band_names
  mdata.AddItem, 'data ignore value', 0
  reflect.WriteMetadata
  reflect.close
  
  ; 销毁 FLAASH 大气校正接口实例, 回收RAM资源
  Obj_Destroy, flaash
  
End