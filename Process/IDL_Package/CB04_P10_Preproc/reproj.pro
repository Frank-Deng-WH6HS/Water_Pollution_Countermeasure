Pro CB04_P10_REPROJ, uri_input, uri_output, $
  TYPE=type, EPSG=epsg
  e = Envi(/HEADLESS)
  raster = e.OpenRaster(uri_input)
  spatref = raster.spatialref
  fid_raster = Envirastertofid(raster)
  Envi_File_Query, fid_raster, DIMS=dims, NB=nb
  pos = Lindgen(nb)
  o_proj = Envi_proj_create( $
    TYPE=type, PE_COORD_SYS_CODE=epsg $
    )
  o_pixel_size = spatref.pixel_size
  ; 逐像元重投影, 此处时间开销不是制约因素, 因为仅需一景P10即可基本覆盖整个特区.
  ; P10作为MUX配准的基准影像, 其自身的配准需要依赖矢量数据, 配准点对通过目视判读确定.
  ; 位置信息必须精确, 重投影的计算必须逐像元, 精确配准将使用 ArcMap 的样条算法实现.
  ; 光谱和辐射信息的精度要求相对低, 仅要求不影响目视辨析, 以及MUX的同名点自动匹配.
  ; 因此P10无需辐射校正; 重投影过程中的重采样, 可使用双线性插值.
  Envi_Convert_File_Map_Projection, $
    FID=fid_raster, OUT_NAME=uri_output, $
    POS=pos, DIMS=dims, O_PROJ=o_proj, $
    WARP_METHOD=3, O_PIXEL_SIZE=o_pixel_size, $
    RESAMPLING=1, BACKGROUND=0, R_FID=fid_reproj
  ; 更新元数据, 确保输出结果的元数据中, 
  ; 除数据组织形式, 空间基准以外的其他元数据与输入一致
  reproj = EnviFidToRaster(fid_reproj)
  band_names = raster.metadata["band names"]
  raster.close
  mdata = reproj.metadata
  mdata.RemoveItem, 'description'
  mdata.RemoveItem, 'sensor type'
  mdata.UpdateItem, 'band names', band_names
  reproj.WriteMetadata
  reproj.close
End
