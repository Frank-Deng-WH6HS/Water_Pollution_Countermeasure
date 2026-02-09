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
    FieldLocations: IntArr(8), $ ; 配置了Delimiter后, 此项将被Read_Ascii自动忽略
    FieldGroups: IndGen(8) $ ; 不编组
  }
  res = Read_Ascii(filename, TEMPLATE=field_cfg)
  Return, res
End

; 获取影像的空间基准, 影像需要为TIFF格式, 或者附带Hdr头文件的ENVI Dat格式. 
; Acquire spatial datum of imagery which is required to be of TIFF format
;   or ENVI Dat format with Hdr header file. 
Function PARSE_SPATIAL_DATUM, raster
  e = Envi()
  ; 读取总行数, 总列数
  n_rows = raster.NRows
  n_columns = raster.NColumns
  ; 读取空间参考系信息. 注意: L2级数据是在L1A级数据基础上经正射校正所得, 已经重投影, 
  ; 因此既包含参考椭球信息 (始终为WGS-84), 又有投影变换信息 (始终为特定分带的UTM投影)
  spat_ref = raster.SpatialRef.Dehydrate()
  spat_ref = spat_ref.ToStruct()
  spat_ref_reconst = EnviStandardRasterSpatialRef( $
    COORD_SYS_CODE=spat_ref.Coord_Sys_Code, $
    PIXEL_SIZE=spat_ref.Pixel_Size, $
    ROTATION=spat_ref.Rotation, $
    TIE_POINT_MAP=spat_ref.Tie_Point_Map, $
    TIE_POINT_PIXEL=spat_ref.Tie_Point_Pixel $
  )
  datum = { $
    SpatialRef: spat_ref_reconst, $
    NRows: n_rows, $
    NColumns: n_columns $
  }
  Return, datum
End

; 根据影像成像时间和空间基准, 计算satangle采样点的太阳方位角和天顶角
; Calculate sun azimuth and zenith angle of each pixel according to 
;   acquisition time and spatial references of imagery. 
Function SUN_POSITION, raster, res_satangle
  e = Envi()
  ; 读取影像采集时刻的GMT时间
  acq_time = raster.Time
  TimeStampToValues, acq_time.Acquisition, $
    YEAR=yr, MONTH=mo, DAY=d, HOUR=hr, MINUTE=min, SECOND=sec, OFFSET=tz
  hr -= tz ; 时区校正
  gmt = 100d * hr + min + sec / 60.d
  n_smp = n_elements(res_satangle.L1Sample)
  sun_zenith = DblArr(n_smp)
  sun_azimuth = Dblarr(n_smp)
  For idx_smp = 0, n_smp - 1 Do Begin
    lon = res_satangle.Lon[idx_smp]
    lat = res_satangle.Lat[idx_smp]
    ; 根据经纬度和成像时间, 计算太阳视位置, 以degree为单位
    sun_pos = Envi_compute_sun_angles(d, mo, yr, gmt, lat, lon)
    sun_zenith[idx_smp] = 90.d - sun_pos[0]
    sun_azimuth[idx_smp] = sun_pos[1]
  EndFor
  res = { $
    Lon: res_satangle.Lon, $
    Lat: res_satangle.Lat, $
    Zenith_Sun: sun_zenith, $
    Azimuth_Sun: sun_azimuth $
  }
  Return, res
End