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

; 根据raster影像空间基准, 计算其四至点的投影坐标
; Calculate projected coord. of extreme points of raster according to spatial
;   references of imagery. 
Function MIN_MAX_XY, raster
  e = Envi()
  ; 读取总行数, 总列数
  n_rows = raster.NRows
  n_columns = raster.NColumns
  ; 获取影像左上, 右上, 左下, 右下 (包括data ignored区域) 顶点的图上坐标
  verteces_cr = [];
  Foreach r, Double([0.d, n_rows]) Do Begin
    Foreach c, Double([0.d, n_columns]) Do Begin
      verteces_cr = [[verteces_cr], [c, r]]
    Endforeach
  Endforeach
  ; 将图上坐标转换为投影坐标
  raster_cr2xy = Envitask("ConvertPixelToMapCoordinates")
  raster_cr2xy.Spatial_Reference = raster.SpatialRef
  raster_cr2xy.Input_Coordinate = verteces_cr
  raster_cr2xy.Execute
  verteces_xy = raster_cr2xy.Output_Coordinate
  res = { $
    XMin: Min(verteces_xy[0, *]), $
    XMax: Max(verteces_xy[0, *]), $
    YMin: Min(verteces_xy[1, *]), $
    YMax: Max(verteces_xy[1, *]) $
  }
  Return, res
End

; 根据raster影像成像时间和空间基准, 计算satangle采样点的投影坐标和观测几何
; Calculate projected coord. and obsv. geometries of each pixel according to
;   acquisition time and spatial references of imagery.
Function SAMPLE_OBSV_GEOM, raster, satangle
  e = Envi()
  ; 计算L2影像在satangle文件中, 每个样本点的投影坐标(x, y), 用于后续的空间插值
  raster_cr2xy = Envitask("ConvertPixelToMapCoordinates")
  raster_cr2xy.Spatial_Reference = raster.SpatialRef
  ; 注意: satangle文件中, L2Line和L2Sample取整数时表示像元中心点,
  ;   在EnviTask中转换为投影坐标前, 需要各减去0.5
  raster_cr2xy.Input_Coordinate = Transpose( [ $
    [satangle.L2Sample - 0.5d], [satangle.L2Line - 0.5d] $
    ] )
  raster_cr2xy.Execute
  l2_proj_x = raster_cr2xy.Output_Coordinate[0, *]
  l2_proj_x = l2_proj_x[*]
  l2_proj_y = raster_cr2xy.Output_Coordinate[1, *]
  l2_proj_y = l2_proj_y[*]
  ; 方位角标准化
  view_zenith = satangle.Zenith
  view_azimuth = AZIMUTH_STANDARDIZE(satangle.Azimuth)
  res = { $
    L2X: l2_proj_x, $
    L2Y: l2_proj_y, $
    ZenithSatellite: view_zenith, $
    AzimuthSatellite: view_azimuth $
  }
  Return, res
End
