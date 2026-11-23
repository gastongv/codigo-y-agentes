# Corre UNA línea de comando con prioridad "por debajo de lo normal" (los hijos la heredan) y guarda su salida.
# Uso: powershell -NoProfile -ExecutionPolicy Bypass -File fuente/bajo.ps1 <archivo-salida> "<comando completo>"
param([Parameter(Mandatory = $true, Position = 0)][string]$Salida, [Parameter(Mandatory = $true, Position = 1)][string]$Linea)
$p = Start-Process -FilePath "cmd.exe" -ArgumentList "/d /c $Linea" -NoNewWindow -PassThru -RedirectStandardOutput $Salida -RedirectStandardError "$Salida.err"
try { $p.PriorityClass = 'BelowNormal' } catch {}
$p.WaitForExit()
exit $p.ExitCode
