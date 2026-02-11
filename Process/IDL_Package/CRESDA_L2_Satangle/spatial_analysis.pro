; 空间分析
; Spatial Analysis

; 方位角离散采样结果的的标准化
; 要求: 当连续变化的方位  (太阳方位角 / 光学卫星视线方位角) 跨越正北或者正南时, 
;   使方位角取值不发生突变
; Standardization of discrete sample of azimuth angles
; Requirement: Make values of azimuth angles NOT variate abruptly 
;   when continuously-variating azimuth angles span true north or 
;   true south. 
Function AZIMUTH_STANDARDIZE, az
  az_unsigned = MOD_UNSIGNED(az, 360)
  az_signed = MOD_SIGNED(az, 360)
  az_unsigned_sd = Stdev(az_unsigned)
  az_signed_sd = Stdev(az_signed)
  If az_unsigned_sd Le az_signed_sd Then Begin
    Return, az_unsigned
  EndIf Else Begin
    Return, az_signed
  EndElse
End

; 根据raster影像成像时间和空间基准, 计算satangle采样点的投影坐标和观测几何
; Calculate projected coord. and obsv. geometries of each pixel according to
;   acquisition time and spatial references of imagery.
Function SAMPLE_OBSV_GEOM, raster, satangle
  e = Envi()
  ; 计算L2影像在satangle文件中, 每个样本点的投影坐标(x, y), 用于后续的空间插值
  raster_rc2xy = Envitask("ConvertPixelToMapCoordinates")
  raster_rc2xy.Spatial_Reference = raster.SpatialRef
  ; 注意: satangle文件中, L2Line和L2Sample取整数时表示像元中心点,
  ;   在EnviTask中转换为投影坐标前, 需要各减去0.5
  raster_rc2xy.Input_Coordinate = Transpose( [ $
    [satangle.L2Sample - 0.5], [satangle.L2Line - 0.5] $
    ] )
  raster_rc2xy.Execute
  l2_proj_x = raster_rc2xy.Output_Coordinate[0, *]
  l2_proj_x = l2_proj_x[*]
  l2_proj_y = raster_rc2xy.Output_Coordinate[1, *]
  l2_proj_y = l2_proj_y[*]
  ; 获取影像采集时刻的GMT时间
  acq_time = raster.Time
  TimeStampToValues, acq_time.Acquisition, $
    YEAR=yr, MONTH=mo, DAY=d, HOUR=hr, MINUTE=min, SECOND=sec, OFFSET=tz
  hr -= tz ; 时区校正
  gmt = 100d * hr + min + sec / 60.d
  ; 根据satangle中提供的经纬度和raster的成像时间, 计算太阳视位置, 以degree为单位
  ; ENVI内置的Envi_Compute_Sun_Angles只接受十进制度格式的经纬度,
  ;   因此直接使用satangle.Lon和satangle.Lat, 不通过投影逆变换求解
  n_smp = N_elements(satangle.L1Sample)
  sun_zenith = Dblarr(n_smp)
  sun_azimuth = Dblarr(n_smp)
  For idx_smp = 0, n_smp - 1 Do Begin
    lon = satangle.Lon[idx_smp]
    lat = satangle.Lat[idx_smp]
    sun_pos = Envi_compute_sun_angles(d, mo, yr, gmt, lat, lon)
    ; Envi_Compute_Sun_Angles所得数组中, 位次为0的元素是太阳高度角, 需要转化为天顶角
    sun_zenith[idx_smp] = 90.d - sun_pos[0]
    sun_azimuth[idx_smp] = sun_pos[1]
  Endfor
  ; 方位角标准化
  sun_azimuth = AZIMUTH_STANDARDIZE(sun_azimuth)
  view_zenith = satangle.Zenith
  view_azimuth = AZIMUTH_STANDARDIZE(satangle.Azimuth)
  res = { $
    L2X: l2_proj_x, $
    L2Y: l2_proj_y, $
    Zenith_Sun: sun_zenith, $
    Azimuth_Sun: sun_azimuth, $
    Zenith_Satellite: view_zenith, $
    Azimuth_Satellite: view_azimuth $
  }
  Return, res
End
