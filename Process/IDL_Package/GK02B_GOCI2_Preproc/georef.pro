Function FD_L2_AC_GLT, cdfid
  e = Envi()
  raster_nav = LOAD_FD_L2_AC_NAV(cdfid)
  fid_nav = EnviRasterToFid(raster_nav)
  Envi_File_Query, fid_nav, DIMS=dims_nav
  csys_nav = Envi_Proj_Create( $
    /GEOGRAPHIC, DATUM="WGS-84" , $
    UNITS=Envi_Translate_Projection_Units("Degrees") $
  )
  ; 
  ; 目前已知的问题: 
  ;   Envi_GLT_DoIt的运行结果本身可以稳定复现, 但使用该过程生成的
  ;   GLT栅格, 和通过ENVI 5.x工具箱内置"Build GLT"或者"Georefer-
  ;   ence from IGM"工具生成的GLT栅格内容不完全一致. 
  ;   具体体现为: 当输入的经纬度影像, 使用的输入/输出空间基准, 输出
  ;   栅格像元大小 (使用默认值), 旋转方向等参数均对应相同时, 
  ;   Envi_GLT_DoIt的输出结果GLT, 和"Build GLT"输出结果 (或者
  ;   "Georeference from IGM"中间结果GLT) 栅格数据相比较, 发现
  ;   二者空间基准和覆盖范围一致, 行/列标相同的像元位置重合 (可以在
  ;   两个栅格之间直接执行Band Math而无需重投影/重采样), 但两种
  ;   GLT栅格部分像元的GLT结果取值不同. 
  ; 
  Envi_GLT_DoIt, $
    X_FID=fid_nav, X_POS=[0], DIMS=dims_nav, $
    Y_FID=fid_nav, Y_POS=[1], $
    I_PROJ=csys_nav, O_PROJ=csys_nav, $
    ROTATION=0.e, /IN_MEMORY, R_FID=fid_glt
  raster_glt = EnviFidToRaster(fid_glt)
  raster_nav.Close
  Return, raster_glt
End