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

Function LOAD_FD_L2_AC_RRS, cdfid
  e = Envi()
  grps_path_id = NCDF_GRPS_ID(cdfid)
  grp_rrs_name = "/geophysical_data/Rrs"
  grp_rrs_id = grps_path_id[grp_rrs_name]
  vars_rrs_id = NCDF_VARS_ID(grp_rrs_id)
  vars_rrs_name = vars_rrs_id.keys()
  atts_dim = QUERY_DIM(cdfid)
  atts_wl = FltArr(atts_dim.NBands, /NOZERO)
  arr_rrs = FltArr( $
    atts_dim.NColumns, atts_dim.NRows, atts_dim.NBands, $
    /NOZERO $
  )
  att_rrs_band_wl_name = "radiation_wavelength"
  band_names = vars_rrs_name.Sort()
  band_names = band_names.ToArray()
  ForEach band_name, band_names, idx Do Begin
    var_rrs_band_id = vars_rrs_id[band_name]
    Ncdf_AttGet, $
      grp_rrs_id, var_rrs_band_id, $
      att_rrs_band_wl_name, att_rrs_band_wl
    atts_wl[idx] = att_rrs_band_wl
    Ncdf_VarGet, grp_rrs_id, var_rrs_band_id, var_rrs_band
    arr_rrs[*, *, idx] = var_rrs_band
  EndForEach
  DelVar, var_rrs_band
  Envi_Enter_Data, $
    arr_rrs, $
    DATA_IGNORE_VALUE=-999.e, $
    BNAMES=band_names, $
    WL=atts_wl, $
    WAVELENGTH_UNIT=1, $
    R_FID=fid_raster
  raster = EnviFidToRaster(fid_raster)
  DelVar, arr_rrs
  Return, raster
End

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