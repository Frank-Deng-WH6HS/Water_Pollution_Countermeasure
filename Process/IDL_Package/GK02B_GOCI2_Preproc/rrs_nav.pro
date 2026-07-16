
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