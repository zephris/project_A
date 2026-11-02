$ErrorActionPreference='Stop'
$taskSliceRoot=$PSScriptRoot
$taskSliceJob=Join-Path $taskSliceRoot 'work'
New-Item -ItemType Directory -Force -Path $taskSliceJob | Out-Null
$taskSliceArgs=@(
 '--load-settings',('"'+(Join-Path $taskSliceRoot 'presets/printer.json')+';'+(Join-Path $taskSliceRoot 'presets/process.json')+'"'),
 '--load-filaments',('"'+(Join-Path $taskSliceRoot 'presets/PLA.json')+';'+(Join-Path $taskSliceRoot 'presets/PETG_interface.json')+'"'),
 '--curr-bed-type','"Textured PEI Plate"','--arrange','0','--slice','0','--debug','2',
 '--outputdir',('"'+$taskSliceJob+'"'),'--export-3mf','sliced.3mf',
 ('"'+(Join-Path $taskSliceRoot 'reprint_stack.3mf')+'"'))
$taskSliceStart=[DateTime]::UtcNow
$taskSliceProcess=Start-Process -FilePath 'D:/Bambu Studio/bambu-studio.exe' -ArgumentList $taskSliceArgs -WorkingDirectory $taskSliceJob -WindowStyle Hidden -Wait -PassThru -RedirectStandardOutput (Join-Path $taskSliceJob 'stdout.log') -RedirectStandardError (Join-Path $taskSliceJob 'stderr.log')
$taskSliceResultFile=Join-Path $taskSliceJob 'result.json'
if ($taskSliceProcess.ExitCode -ne 0 -or -not (Test-Path -LiteralPath $taskSliceResultFile)) { throw ('Bambu Studio failed, exit '+$taskSliceProcess.ExitCode+'; see '+$taskSliceJob) }
if ((Get-Item -LiteralPath $taskSliceResultFile).LastWriteTimeUtc -lt $taskSliceStart.AddSeconds(-2)) { throw 'No fresh slice result; do not reuse old G-code.' }
$taskSliceResult=Get-Content -Raw -LiteralPath $taskSliceResultFile | ConvertFrom-Json
if ($taskSliceResult.return_code -ne 0) { throw $taskSliceResult.error_string }
Copy-Item -LiteralPath (Join-Path $taskSliceJob 'sliced.3mf') -Destination (Join-Path $taskSliceRoot 'reprint_stack.gcode.3mf')
Copy-Item -LiteralPath $taskSliceResultFile -Destination (Join-Path $taskSliceRoot 'review/slice-result.json')
$taskSliceResult.sliced_plates | Select-Object total_predication,filament_change_times,filaments | ConvertTo-Json -Depth 5
