; 将影像另存为硬盘文件
; 输入: 
;   当前IDL会话中, 处于打开状态的影像EnviRaster接口对象; 
;   另存为硬盘文件的路径
; 关键字: 
;   /COMPRESSION: 另存为过程中, 将影像自动压缩为gzip
; 输出: 
;   另存为后重新在ENVI会话打开的影像EnviRaster接口对象
; 
Function EXPORT_AS, raster, filename, $
  COMPRESSION=compression
  e = Envi()
  fid_raster = EnviRasterToFid(raster)
  Envi_File_Query, fid_raster, $
    DIMS=dims_raster
  ; 读取空间参考系信息
  inherit = Envi_Set_Inheritance( $
    fid_raster, dims_raster, /SPATIAL $
  )
  ; 读取栅格数据组织形式
  interleave_optn = ['bsq', 'bil', 'bip']
  interleave = raster.Interleave
  interleave = Where(interleave_optn Eq interleave)
  ; 读取像元内容
  arr_raster = raster.GetData()
  ; 写入硬盘
  Envi_Write_Envi_File, arr_raster, $
    OUT_NAME=filename, $
    INHERIT=inherit, $
    INTERLEAVE=interleave, $
    COMPRESSION=compression, $
    R_FID=fid_export
  DelVar, arr_raster
  raster_export = EnviFidToRaster(fid_export)
  ; 将栅格数据的部分元数据复制到导出后的栅格
  mdata_names = [ $
    ; 数据质量信息
    'data ignore value', 'bbl', 'cloud cover', $
    ; 光谱信息 
    'band names', 'wavelength units', $
    'wavelength', 'fwhm', $
    'data gain values', 'data offset values', $
    'data reflectance gain values', $
    'data reflectance offset values', $
    'solar irradiance', $
    ; 观测几何
    'sun azimuth', 'sun elevation', $
    'dem file', 'dem band', 'sensor type', $
    ; 分类结果栅格特有元数据
    'classes', 'class names', 'class lookup' $
  ]
  ForEach mdata_name, mdata_names Do Begin
    If raster.Metadata.HasTag(mdata_name) Then Begin
      mdata_value = raster.Metadata[mdata_name]
      If raster_export.Metadata.HasTag(mdata_name) Then Begin
        raster_export.MetaData.UpdateItem, $
          mdata_name, mdata_value
      EndIf Else Begin
        raster_export.MetaData.AddItem, $
          mdata_name, mdata_value
      Endelse
    EndIf
  EndForEach
  raster_export.MetaData.RemoveItem, "description"
  raster_export.WriteMetadata
  ; 输出结果元数据文件的路径
  prod_base = File_Basename(filename, '.dat')
  ouput_dir = File_Dirname(filename)
  ouput_dir = ouput_dir.Replace('\', '/')
  output_hdr = ouput_dir + '/' + prod_base + ".hdr"
  ; 如果文件采用压缩方式保存, 需要单独在元数据文件末尾追加压缩标记
  If Keyword_Set(COMPRESSION) Then Begin
    If compression Then Begin
      Openu, lun_hdr, output_hdr, /APPEND, /GET_LUN
      Printf, lun_hdr, "file compression = 1"
      Close, lun_hdr
    EndIf
  EndIf
  Return, raster_export
End
