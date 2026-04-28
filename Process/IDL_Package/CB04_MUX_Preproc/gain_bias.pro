Pro CB04_MUX_METADATA_ACQ, filename, raster_rad_gain, raster_rad_bias
  e = Envi()
  ; 影像, 元数据的存放路径
  prod_path = File_dirname(filename)
  prod_path = prod_path.Replace('\', '/')
  ; 影像的主名
  prod_base = File_basename(filename, '.xml')
  ; 在ENVI会话中加载影像, 此操作依赖第三方控件"中国卫星支持工具". 
  ; 此时图像的元数据尚未持久化为ENVI原生支持的hdr格式.
  raster = EnviOpenChinaRaster(filename)
  ; 读取部分元数据, 在后续操作中一并写入hdr, 用于后续辐射定标和大气校正
  raster_mdin = EnviTask("RasterMetadataItem")
  raster_mdin.input_raster = raster
    ; 各波段中心波长 (FLAASH大气校正中需要从影像hdr自动读取)
  raster_mdin.key = "wavelength"
  raster_mdin.execute
  wl = raster_mdin.value
    ; 各波段半峰全宽 (FLAASH大气校正中需要从影像hdr自动读取)
  raster_mdin.key = "fwhm"
  raster_mdin.execute
  fwhm = raster_mdin.value
    ; 其他 (轨道高度, 成像时间, 太阳视位置等) 不需要, 
    ; 因为FLAASH需要在校正前手动指定轨道高度, 每景影像
    ; 中心点经纬度和成像时间, 并在校正过程中自动计算太阳
    ; 视位置. 另外FLAASH只接受绝对辐射定标所得辐亮度作为
    ; 输入, 因此波段太阳辐照度也不需要.
  raster_mdout = EnviTask("SetRasterMetadata")
  ; 设置影像元数据, 并持久化为同路径, 同主名的hdr文件.
  raster_mdout.input_raster = raster
    ; 数据组织形式
  raster_mdout.ncolumns = raster.ncolumns
  raster_mdout.nrows = raster.nrows
  raster_mdout.nbands = raster.nbands
  raster_mdout.data_type = raster.data_type
  raster_mdout.interleave = raster.interleave
  raster_mdout.byte_order = "Host (Intel)"
  raster_mdout.data_ignore_value = 0
    ; 空间特征
  raster_mdout.spatialref = raster.spatialref
    ; 光谱特征
  raster_mdout.wavelength = wl
  raster_mdout.wavelength_units = "Micrometers"
  raster_mdout.fwhm = fwhm
    ; 辐射定标系数
  raster_mdout.data_gain_values = raster_rad_gain
  raster_mdout.data_offset_values = raster_rad_bias
  ; 保存结果并关闭ENVI会话中的栅格
  raster_mdout.execute
End
