; NetCDF 读取工具

; 递归地获取当前打开的NetCDF的每个编组的路径和对应的识别码
; 输入: 当前IDL会话中, 处于打开状态的NetCDF文件号
; 输出: 键值对, 键的内容是每个编组的完整相对路径, 
;   对应的值是该编组在当前IDL会话的识别码
; 
; 注意: 如果同一个NetCDF在同一IDL会话中关闭后重新打开, 
;   即使内容无改动, 其文件号和各编组识别码将发生变化
; 
Function NCDF_GRPS_LOC, cdfid
  node = cdfid
  node_map = Hash()
  leaves = [node]
  Repeat Begin
    leaves_next = !Null
    ForEach node, leaves Do Begin
      node_path = Ncdf_FullGroupName(node)
      node_path = Strjoin( $
        [node_path], "/" $
      )
      node_map[node_path] = node
      branch = Ncdf_GroupsInq(node)
      If branch Ne [-1] Then Begin
        leaves_next = [leaves_next, branch]
      EndIf
    EndForEach
    If leaves_next Ne !Null Then Begin
      leaves = leaves_next
    EndIf
  EndRep Until leaves_next Eq !Null
  Return, node_map
End

; 获取NetCDF特定编组中每个数据集的路径和对应的识别码, 
;   但不包括其各级子编组中的数据集 (不递归)
; 输入: 当前IDL会话中, 处于打开状态的NetCDF编组的识别码
; 输出: 键值对, 键的内容是每个数据集的完整相对路径,
;   对应的值是该数据集在当前IDL会话的识别码
; 
Function NCDF_VARS_LOC, grpid
  grp_path = Ncdf_FullGroupName(grpid)
  node_map = Hash()
  nodes = Ncdf_VarIdsInq(grpid)
  If nodes Eq [-1] Then Begin
    Return, node_map
  EndIf
  ForEach node, nodes Do Begin
    node_info = Ncdf_VarInq(grpid, node)
    node_name = node_info.name
    node_path = StrJoin( $
      [grp_path, node_name], "/" $
    )
    node_map[node_path] = node
  EndForEach
  Return, node_map
End

; 获取NetCDF特定编组或其数据集中, 每个属性的路径和对应的识别码
;   但不包括其各级子编组 (及其数据集) 中的属性 (不递归)
; 输入: 当前IDL会话中, 处于打开状态的NetCDF编组的识别码, 
;   数据集的识别码 (可选参数, 无默认值)
; 输出: 键值对, 键的内容是每个属性的完整相对路径,
;   对应的值是该属性在当前IDL会话的识别码
; 
Function NCDF_ATTS_LOC, grpid, varid
  grp_path = Ncdf_fullgroupname(grpid)
  node_map = Hash()
  If N_Params() Eq 1 Then Begin
    ; 检索编组的全局属性
    grp_inq = Ncdf_Inquire(grpid)
    n_att = grp_inq.ngatts
    For idx_att = 0, n_att - 1 Do Begin
      att_name = Ncdf_Attname(grpid, idx_att, /GLOBAL)
      If grp_path Eq "/" Then grp_path = ""
      att_path = Strjoin( $
        [grp_path, att_name], "/" $
        )
      node_map[att_path] = idx_att
    EndFor
  EndIf Else Begin
    ; 检索数据集的属性
    var_inq = Ncdf_VarInq(grpid, varid)
    var_name = var_inq.name
    n_att = var_inq.natts
    For idx_att = 0, n_att - 1 Do Begin
      att_name = Ncdf_Attname(grpid, varid, idx_att)
      att_path = Strjoin( $
        [grp_path, var_name, att_name], "/" $
        )
      node_map[att_path] = idx_att
    Endfor
  EndElse
  Return, node_map
End