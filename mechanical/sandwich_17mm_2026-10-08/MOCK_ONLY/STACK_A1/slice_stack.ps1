param([ValidateSet('stacked_kit_inset','separator_trial')][string]$Model = 'stacked_kit_inset')
$ErrorActionPreference = 'Stop'
$taskSliceRoot = $PSScriptRoot
$taskSliceJob = Join-Path $taskSliceRoot ('jobs/' + $Model)
New-Item -ItemType Directory -Path $taskSliceJob -Force | Out-Null
$taskSliceProcessName = if ($Model -eq 'stacked_kit_inset') { 'stack_inset.json' } else { 'stack.json' }
$taskSliceArgs = @(
    '--load-settings', ('"' + (Join-Path $taskSliceRoot 'presets/printer.json') + ';' + (Join-Path $taskSliceRoot ('presets/' + $taskSliceProcessName)) + '"'),
    '--load-filaments', ('"' + (Join-Path $taskSliceRoot 'presets/PLA.json') + ';' + (Join-Path $taskSliceRoot 'presets/PETG_interface.json') + '"'),
    '--curr-bed-type', '"Textured PEI Plate"', '--arrange', '0', '--slice', '0', '--debug', '2',
    '--outputdir', ('"' + $taskSliceJob + '"'), '--export-3mf', 'sliced.3mf',
    ('"' + (Join-Path $taskSliceRoot ($Model + '.3mf')) + '"')
)
# Start-Process completed successfully on this host where Python's direct
# child-process launch failed. This is local CLI slicing, never a print dispatch.
$taskSliceStartedAt = [DateTime]::UtcNow
$taskSliceProc = Start-Process -FilePath 'D:/Bambu Studio/bambu-studio.exe' -ArgumentList $taskSliceArgs -WorkingDirectory $taskSliceJob -WindowStyle Hidden -Wait -PassThru -RedirectStandardOutput (Join-Path $taskSliceJob 'stdout.log') -RedirectStandardError (Join-Path $taskSliceJob 'stderr.log')
$taskSliceResultPath = Join-Path $taskSliceJob 'result.json'
if ($taskSliceProc.ExitCode -ne 0 -or -not (Test-Path -LiteralPath $taskSliceResultPath)) {
    throw ('Bambu Studio failed, exit ' + $taskSliceProc.ExitCode + '; inspect ' + $taskSliceJob)
}
if ((Get-Item -LiteralPath $taskSliceResultPath).LastWriteTimeUtc -lt $taskSliceStartedAt.AddSeconds(-2)) {
    throw 'Bambu Studio did not produce a fresh result; previous output must not be reused.'
}
$taskSliceResult = Get-Content -LiteralPath $taskSliceResultPath -Raw | ConvertFrom-Json
if ($taskSliceResult.return_code -ne 0) { throw $taskSliceResult.error_string }
Copy-Item -LiteralPath (Join-Path $taskSliceJob 'sliced.3mf') -Destination (Join-Path $taskSliceRoot ($Model + '.gcode.3mf'))
Copy-Item -LiteralPath $taskSliceResultPath -Destination (Join-Path $taskSliceRoot ('review/' + $Model + '-slice.json'))
$taskSliceResult.sliced_plates | Select-Object total_predication,filament_change_times,filaments | ConvertTo-Json -Depth 5
