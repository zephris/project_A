$ErrorActionPreference='Stop'
$taskProjectRoot=$PSScriptRoot
$taskPython=Join-Path $taskProjectRoot '../heatsink_2026-10-08/.venv/Scripts/python.exe'
$env:CADGEN_DAEMON='0'
$env:OPENBLAS_NUM_THREADS='1'
$env:OMP_NUM_THREADS='1'
$env:CADGEN_CACHE_DIR=Join-Path $taskProjectRoot '../heatsink_2026-10-08/.ocp-cache'
$env:PLAYWRIGHT_BROWSERS_PATH=Join-Path $taskProjectRoot '../heatsink_2026-10-08/.browser'
Push-Location $taskProjectRoot
try {
  foreach($taskModel in @('assembly','exploded','top_acrylic_cut','bottom_acrylic_cut','switch_plate_cut','foam_cut','upper_foam_cut','switch_coupon','switch_coupon_cut','port_seals_cut','port_detail')) {
    & $taskPython ('src/'+$taskModel+'.py')
    if($LASTEXITCODE -ne 0){throw $taskModel}
  }
  & $taskPython checks/check_fit.py
  if($LASTEXITCODE -ne 0){throw 'Fit checks'}
  & $taskPython checks/check_usb_recess.py
  if($LASTEXITCODE -ne 0){throw 'USB recess checks'}
  & $taskPython checks/check_roof_shield.py
  if($LASTEXITCODE -ne 0){throw 'Connector roof shield check'}
  & $taskPython checks/check_cut_profiles.py
  if($LASTEXITCODE -ne 0){throw 'Cut profile checks'}
  & $taskPython checks/check_option_caps.py
  if($LASTEXITCODE -ne 0){throw 'Option cap checks'}
  & $taskPython checks/check_port_integration.py
  if($LASTEXITCODE -ne 0){throw 'Integrated port cover checks'}
  & $taskPython checks/check_port_seals.py
  if($LASTEXITCODE -ne 0){throw 'Port seal projection checks'}
} finally {Pop-Location}
