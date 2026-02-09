; 数学函数
; Mathematical Function

; 取余运算, 要求除数必须为正, 余数强制非负, 与Python一致
; Modulo operation, forcing divisors and remainder to be positive and 
;   non-negative respectively. Consistent to Python. 
Function MOD_UNSIGNED, x, y
  m = x Mod y
  lt_pos = Where(m Lt 0, /NULL)
  If lt_pos Ne !Null Then Begin
    m[lt_pos] += y
  EndIf
  Return, m
End

; 取余运算, 要求除数必须为正, 余数的绝对值不超过除数的二分之一
; 当余数的绝对值恰为除数二分之一时, 余数取负值
; Modulo operator, forcing divisors to be positive and forcing remainder 
;   not to be more than half of divisors. 
; Remainder will be negative when its absolute value is exactly the 
;   half of divisors. 
Function MOD_SIGNED, x, y
  m = MOD_UNSIGNED(x, y)
  ge_pos = Where(m Ge (y / 2.d), /NULL)
  If ge_pos Ne !Null Then Begin
    m[ge_pos] -= y
  EndIf
  Return, m
End