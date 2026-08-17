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
  ;   栅格像元大小, 旋转方向 (使用默认值) 等参数均对应相同时, 
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
    ; 注意: 不要手动指定重采样的栅格像元大小和旋转角, 
    ; 因为极有可能会额外引入位置误差
    /IN_MEMORY, R_FID=fid_glt
  raster_glt = EnviFidToRaster(fid_glt)
  raster_nav.Close
  Return, raster_glt
End

Function FD_L2_AC_GLT_EXPORT, $
  filename, output_dir, $
  COMPRESSION=compression
  ; 关键字参数取值初始化
  If Not Keyword_Set(COMPRESSION) Then compression = 0
  e = Envi()
  ; 影像的主名
  prod_base = File_basename(filename, '.nc')
  ; 输出结果的路径
  output_path = output_dir.Replace('\', '/') + $
    '/' + prod_base + "_glt.dat"
  ; 打开NetCDF
  nc = NCdf_Open(filename)
  ; 在RAM中构造GLT
  raster_glt = FD_L2_AC_GLT(nc)
  ; 将GLT另存为硬盘文件
  raster_glt_export = EXPORT_AS( $
    raster_glt, output_path, COMPRESSION=compression $
  )
  raster_glt.Close
  NCdf_Close, nc
  Return, raster_glt_export
End

Function FD_L2_AC_GEOREF, cdfid, raster_glt, _EXTRA=_extra
  e = Envi()
  raster_refl = LOAD_FD_L2_AC_GEOPHY(cdfid, _EXTRA=_extra)
  fid_refl = EnviRasterToFid(raster_refl)
  fid_glt = EnviRasterToFid(raster_glt)
  atts_dim = QUERY_DIM(cdfid)
  Envi_Georef_from_GLT_DoIt, $
    FID=fid_refl, POS=LindGen(atts_dim.nBands), $
    GLT_FID=fid_glt, BACKGROUND=-999.e, $
    /IN_MEMORY, R_FID=fid_georef
  raster_georef = EnviFidToRaster(fid_georef)
  raster_refl.Close
  Return, raster_georef
End

Function FD_L2_AC_GEOREF_EXPORT, $
  filename, glt_filename, output_dir, $
  COMPRESSION=compression, RHOC=rhoc, RRS=rrs
  ; 关键字参数取值初始化
  If Not Keyword_Set(COMPRESSION) Then compression = 0
  e = Envi()
  ; 影像的主名
  prod_base = File_Basename(filename, '.nc')
  ; 导出的文件类型
  If Keyword_Set(RHOC) Then Begin
    If rhoc Then refl_name = "RhoC"
  EndIf
  If Keyword_Set(RRS) Then Begin
    If rrs Then refl_name = "Rrs"
  EndIf
  ; 输出结果的路径
  output_path = output_dir.Replace('\', '/') + $
    '/' + prod_base.Replace('_AC', refl_name) + $
    "_georef.dat"
  ; 打开NetCDF
  nc = NCdf_Open(filename)
  ; 载入GLT
  raster_glt = e.OpenRaster(glt_filename)
  ; 利用GLT, 在RAM中生成配准结果
  raster_georef = FD_L2_AC_GEOREF( $
    nc, raster_glt, RHOC=rhoc, RRS=rrs $
  )
  ; 将配准结果另存为硬盘文件
  raster_georef_export = EXPORT_AS( $
    raster_georef, output_path, COMPRESSION=compression $
  )
  raster_georef.Close
  Return, raster_georef_export
End
