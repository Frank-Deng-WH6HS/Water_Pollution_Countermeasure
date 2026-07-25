; GK-2B GOCI2 L2级大气校正产品读取工具

; 读取NetCDF反射率影像维数
; 输入: 当前IDL会话中, 处于打开状态的NetCDF文件号
; 输出: 结构体, 包含RhoC (或Rrs) 影像的行数, 列数, 波段数
; 
Function QUERY_DIM, cdfid
  grps_path_id = NCDF_GRPS_ID(cdfid)
  grp_root_name = "/"
  grp_root_id = grps_path_id[grp_root_name]
  att_nrows_name = "number_of_lines"
  att_ncolumns_name = "number_of_columns"
  att_nbands_name = "number_of_total_bands"
  Ncdf_AttGet, grp_root_id, att_nrows_name, att_nrows, /GLOBAL
  Ncdf_AttGet, grp_root_id, att_ncolumns_name, att_ncolumns, /GLOBAL
  Ncdf_AttGet, grp_root_id, att_nbands_name, att_nbands, /GLOBAL
  atts_dim = { $
    NRows: att_nrows, $
    NColumns: att_ncolumns, $
    NBands: att_nbands $
  }
  Return, atts_dim
End

; 读取NetCDF中的反射率影像
; 输入: 当前IDL会话中, 处于打开状态的NetCDF文件号
; 关键字: 
;   /RHOC: 读取RhoC: 经 Rayleigh 校正的地物反射率, 单位为1
;   /RRS: 读取Rrs: 经 Rayleigh 校正和气溶胶校正的水体遥感反射率. 
;     Rrs是在RhoC基础上除去气溶胶影响, 并进行角度归一化所得物理量, 
;     单位为 per steradian, 排除陆地, 云覆盖区域或极高浊度水域. 
;   每次调用本函数时, 关键字 /RHOC 和 /RRS 有且只有一个被指定
;     当 /RHOC 和 /RRS 同时启用时, 只读取RhoC, 此时 /RRS 无效; 
;     当 /RHOC 和 /RRS 均未启用时, 程序读取失败并报错. 
; 输出: 反射率影像EnviRaster接口对象, 可在Envi会话中操作. 
;   影像波段按照波长 (单位: nm) 升序排列. 
;   影像驻留在RAM中, 需手动导出为硬盘文件
; 
Function LOAD_FD_L2_AC_GEOPHY, cdfid, RHOC=rhoc, RRS=rrs
  e = Envi()
  grps_path_id = NCDF_GRPS_ID(cdfid)
  grp_refl_name = "/geophysical_data"
  Case 1 Of 
    Keyword_Set(RHOC): Begin
      If rhoc Then grp_refl_name += "/RhoC"
    End
    Keyword_Set(RRS): Begin
      If Rrs Then grp_refl_name += "/Rrs"
    End
  EndCase
  grp_refl_id = grps_path_id[grp_refl_name]
  vars_refl_id = NCDF_VARS_ID(grp_refl_id)
  vars_refl_name = vars_refl_id.keys()
  atts_dim = QUERY_DIM(cdfid)
  atts_wl = FltArr(atts_dim.NBands, /NOZERO)
  arr_refl = FltArr( $
    atts_dim.NColumns, atts_dim.NRows, atts_dim.NBands, $
    /NOZERO $
    )
  att_refl_band_wl_name = "radiation_wavelength"
  band_names = vars_refl_name.Sort()
  band_names = band_names.ToArray()
  ForEach band_name, band_names, idx Do Begin
    var_refl_band_id = vars_refl_id[band_name]
    Ncdf_AttGet, $
      grp_refl_id, var_refl_band_id, $
      att_refl_band_wl_name, att_refl_band_wl
    atts_wl[idx] = att_refl_band_wl
    Ncdf_VarGet, grp_refl_id, var_refl_band_id, var_refl_band
    arr_refl[*, *, idx] = var_refl_band
  EndForEach
  DelVar, var_refl_band
  Envi_Enter_Data, $
    arr_refl, $
    DATA_IGNORE_VALUE=-999.e, $
    BNAMES=band_names, $
    WL=atts_wl, $
    WAVELENGTH_UNIT=1, $
    R_FID=fid_raster
  raster = EnviFidToRaster(fid_raster)
  DelVar, arr_refl
  Return, raster
End

; 读取NetCDF中的RhoC影像
; 输入: 当前IDL会话中, 处于打开状态的NetCDF文件号
; 输出: RhoC影像EnviRaster接口对象
; 
Function LOAD_FD_L2_AC_RHOC, cdfid
  raster = LOAD_FD_L2_AC_GEOPHY(cdfid, /RHOC)
  Return, raster
End

; 读取NetCDF中的Rrs影像
; 输入: 当前IDL会话中, 处于打开状态的NetCDF文件号
; 输出: Rrs影像EnviRaster接口对象
; 
Function LOAD_FD_L2_AC_RRS, cdfid
  raster = LOAD_FD_L2_AC_GEOPHY(cdfid, /RRS)
  Return, raster
End

; 读取NetCDF中的经纬度影像
; 输入: 当前IDL会话中, 处于打开状态的NetCDF文件号
; 输出: 经纬度影像EnviRaster接口对象, 可在Envi会话中操作. 
;   影像每个像元的两通道取值, 分别为反射率影像对应位置像元的
;   经, 纬度, 单位为decimal degree, 空间基准为 WGS-84
;   可用于 Build GLT 或者 Georeference from GLT/IGM
; 
Function LOAD_FD_L2_AC_NAV, cdfid
  e = Envi()
  grps_path_id = NCDF_GRPS_ID(cdfid)
  grp_nav_name = "/navigation_data"
  grp_nav_id = grps_path_id[grp_nav_name]
  vars_nav_id = NCDF_VARS_ID(grp_nav_id)
  var_nav_lon_name = "longitude"
  var_nav_lat_name = "latitude"
  var_nav_lon_id = vars_nav_id[var_nav_lon_name]
  var_nav_lat_id = vars_nav_id[var_nav_lat_name]
  Ncdf_VarGet, grp_nav_id, var_nav_lon_id, var_nav_lon
  Ncdf_VarGet, grp_nav_id, var_nav_lat_id, var_nav_lat
  arr_nav = [[[var_nav_lon]], [[var_nav_lat]]]
  DelVar, var_nav_lon, var_nav_lat
  Envi_Enter_Data, $
    arr_nav, $
    DATA_IGNORE_VALUE=-999.e, $
    BNAMES=[var_nav_lon_name, var_nav_lat_name], $
    R_FID=fid_raster
  DelVar, arr_nav
  raster = EnviFidToRaster(fid_raster)
  Return, raster
End