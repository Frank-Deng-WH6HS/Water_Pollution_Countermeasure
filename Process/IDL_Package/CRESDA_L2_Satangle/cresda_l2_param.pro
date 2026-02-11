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
