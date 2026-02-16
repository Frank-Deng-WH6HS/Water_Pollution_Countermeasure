; CRESDA L2级光学影像产品参数读取工具
; Parameter reader for CRESDA Level 2 optical imagery products

; 读取satangle.txt文件
; Read satangle.txt file
Function READ_SATANGLE_TXT, filename
  field_cfg = { $
    Version: 1.e, $
    DataStart: 3, $
    Delimiter: " ", $
    MissingValue: !Values.F_NaN, $
    CommentSymbol: "#", $
    FieldCount: 8, $
    FieldTypes: [3, 3, 5, 5, 5, 5, 5, 5], $
    FieldNames: [ $
    "L1Line", "L1Sample", "L2Line", "L2Sample", $
    "Lon", "Lat", "Zenith", "Azimuth" $
    ], $ ; 和文件的第三行保持一致
    FieldLocations: Intarr(8), $ ; 配置了Delimiter后, 此项将被Read_Ascii自动忽略
    FieldGroups: Indgen(8) $ ; 不编组
  }
  res = Read_Ascii(filename, TEMPLATE=field_cfg)
  Return, res
End

; 根据影像的元数据文件名主名, 构建观测几何样本的空间插值数据
; Construct spatial interpolation data of obsv. geometries
;   according to base name of metadata file of imagery.
Pro CRESDA_L2_OBSV_GEOM, filename, output_path
  e = Envi()
  ; 影像, 元数据和satangle文件的存放路径
  prod_path = File_dirname(filename)
  prod_path = prod_path.Replace('\', '/')
  ; 影像的主名
  prod_base = File_basename(filename, '.xml')
  ; 在ENVI会话中加载影像, 此操作依赖第三方控件"中国卫星支持工具"
  raster = EnviOpenChinaRaster(filename.Replace('\', '/'))
  ; 读取总行数, 总列数
  n_rows = raster.NRows
  n_columns = raster.NColumns
  ; 获取影像左上, 右上, 左下, 右下顶点的投影坐标, 计算X, Y的最小和最大值
  xy_corner = MIN_MAX_XY(raster)
  ; 读取satangle.txt文件内容
  satangle = READ_SATANGLE_TXT( $
    prod_path + '/' + prod_base + '-SatAngle.txt' $
    )
  ; 读取空间参考系信息
  ; 注意: L2级数据是在L1A级数据基础上经正射校正所得, 已经重投影,
  ;   因此既包含参考椭球信息 (始终为WGS-84), 又有投影变换信息 (始终
  ;   为特定分带的UTM投影)
  spat_ref = raster.SpatialRef
  coord_sys_classic = Envi_Proj_Create( $
    PE_COORD_SYS_CODE=spat_ref.Coord_Sys_Code, $
    PE_COORD_SYS_STR=spat_ref.Coord_Sys_Str, $
    TYPE=42, /UTM $
    )
  px_size = spat_ref.Pixel_Size
  ; 计算采样点的投影坐标和观测几何
  smp_obsv_geom = SAMPLE_OBSV_GEOM(raster, satangle)
  ; 在RAM新建影像, 用于临时存放空间插值结果
  ; 太阳天顶角
  Envi_doit, "Envi_Grid_Doit", $
    ; 输入数据配置
    X_PTS=smp_obsv_geom.L2X, Y_PTS=smp_obsv_geom.L2Y, $
    Z_PTS=smp_obsv_geom.ZenithSun, I_PROJ=coord_sys_classic, $
    ; 输出数据空间特征配置
    O_PROJ=coord_sys_classic, PIXEL_SIZE=px_size, $
    XMIN=xy_corner.XMin, XMAX=xy_corner.XMax, $
    YMIN=xy_corner.YMin, YMAX=xy_corner.YMax, $
    ; 输出数据属性特征配置
    INTERP=0, OUT_DT=4, $
    ; 输出数据文件参数配置
    /IN_MEMORY, R_FID=fid_sun_z
  sun_z = Envifidtoraster(fid_sun_z)
  data_stk = sun_z.GetData()
  sun_z.Close
  ; 太阳方位角
  Envi_doit, "Envi_Grid_Doit", $
    X_PTS=smp_obsv_geom.L2X, Y_PTS=smp_obsv_geom.L2Y, $
    Z_PTS=smp_obsv_geom.AzimuthSun, I_PROJ=coord_sys_classic, $
    O_PROJ=coord_sys_classic, PIXEL_SIZE=px_size, $
    XMIN=xy_corner.XMin, XMAX=xy_corner.XMax, $
    YMIN=xy_corner.YMin, YMAX=xy_corner.YMax, $
    INTERP=0, OUT_DT=4, $
    /IN_MEMORY, R_FID=fid_sun_a
  sun_a = Envifidtoraster(fid_sun_a)
  data_stk = [[[data_stk]], [[sun_a.GetData()]]]
  sun_a.Close
  ; 卫星天顶角
  Envi_doit, "Envi_Grid_Doit", $
    X_PTS=smp_obsv_geom.L2X, Y_PTS=smp_obsv_geom.L2Y, $
    Z_PTS=smp_obsv_geom.ZenithSatellite, I_PROJ=coord_sys_classic, $
    O_PROJ=coord_sys_classic, PIXEL_SIZE=px_size, $
    XMIN=xy_corner.XMin, XMAX=xy_corner.XMax, $
    YMIN=xy_corner.YMin, YMAX=xy_corner.YMax, $
    INTERP=0, OUT_DT=4, $
    /IN_MEMORY, R_FID=fid_sat_z
  sat_z = Envifidtoraster(fid_sat_z)
  data_stk = [[[data_stk]], [[sat_z.GetData()]]]
  sat_z.Close
  ; 卫星方位角
  Envi_doit, "Envi_Grid_Doit", $
    X_PTS=smp_obsv_geom.L2X, Y_PTS=smp_obsv_geom.L2Y, $
    Z_PTS=smp_obsv_geom.AzimuthSatellite, I_PROJ=coord_sys_classic, $
    O_PROJ=coord_sys_classic, PIXEL_SIZE=px_size, $
    XMIN=xy_corner.XMin, XMAX=xy_corner.XMax, $
    YMIN=xy_corner.YMin, YMAX=xy_corner.YMax, $
    INTERP=0, OUT_DT=4, $
    /IN_MEMORY, R_FID=fid_sat_a
  sat_a = Envifidtoraster(fid_sat_a)
  data_stk = [[[data_stk]], [[sat_a.GetData()]]]
  sat_a.Close
  ; 插值结果叠加
  res = Enviraster(data_stk, $
    URI=output_path.Replace('\', '/') + '/' + prod_base + "_obsv_geom.dat", $
    SPATIALREF=spat_ref, TIME=raster.Time, $
    DATA_TYPE=4, INTERLEAVE='bsq', DATA_IGNORE_VALUE=0.e $
  ) 
  raster.Close
  res.Save
  res.Metadata.UpdateItem, "band names", [ $
    "Sun Zenith", "Sun Azimuth", $
    "Satellite Zenith", "Satellite Azimuth" $    
  ]
  Delvar, data_stk
End