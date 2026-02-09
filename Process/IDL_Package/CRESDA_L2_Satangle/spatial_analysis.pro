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
