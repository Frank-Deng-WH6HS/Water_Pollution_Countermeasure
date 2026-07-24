Function FD_L2_AC_GEOREF_BY_IGM, cdfid, _EXTRA=_extra
  e = Envi()
  raster_nav = LOAD_FD_L2_AC_NAV(cdfid)
  fid_nav = EnviRasterToFid(raster_nav)
  Envi_File_Query, fid_nav, DIMS=dims_nav
  csys_nav = Envi_Proj_Create( $
    PE_COORD_SYS_CODE=4326, $ ; WGS-84
    TYPE=1 $
  )
  Envi_GLT_DoIt, $
    X_FID=fid_nav, X_POS=[0], $
    Y_FID=fid_nav, Y_POS=[1], $
    DIMS=dims_nav, I_PROJ=csys_nav, O_PROJ=csys_nav, $
    ROTATION=0, /IN_MEMORY, R_FID=fid_glt
  raster_glt = EnviFidToRaster(fid_glt)
  raster_nav.Close
  raster_refl = LOAD_FD_L2_AC_GEOPHY(cdfid, _EXTRA=_extra)
  fid_refl = EnviRasterToFid(raster_refl)
  atts_dim = QUERY_DIM(cdfid)
  Envi_Georef_from_GLT_DoIt, $
    FID=fid_refl, POS=LindGen(atts_dim.nBands), $
    GLT_FID=fid_glt, BACKGROUND=-999.e, $
    /IN_MEMORY, R_FID=fid_georef
  raster_georef = EnviFidToRaster(fid_georef)
  raster_refl.Close
  raster_glt.Close
  Return, raster_georef
End