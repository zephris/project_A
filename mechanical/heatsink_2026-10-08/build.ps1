param(
    [string]$KiCadPython = 'D:/Program Files/bin/python.exe',
    [string]$KiCadCli = 'D:/Program Files/bin/kicad-cli.exe'
)
$ErrorActionPreference = 'Stop'
$modelRoot = $PSScriptRoot
$repoRoot = (Resolve-Path (Join-Path $modelRoot '../..')).Path
$cadPython = Join-Path $modelRoot '.venv/Scripts/python.exe'
$env:CADGEN_CACHE_DIR = Join-Path $modelRoot '.cache'
$env:PLAYWRIGHT_BROWSERS_PATH = Join-Path $modelRoot '.browser'
function RunChecked {
    param([string]$Program, [string[]]$Arguments)
    & $Program @Arguments
    if ($LASTEXITCODE -ne 0) { throw "Failed: $Program $Arguments" }
}
Push-Location $repoRoot
try {
    RunChecked $KiCadPython @((Join-Path $modelRoot 'extract_constraints.py'))
    RunChecked $KiCadCli @('pcb','export','step','--force','--subst-models','--user-origin','0x0mm',
        '--define-var','KICAD10_3DMODEL_DIR=D:/Program Files/share/kicad/3dmodels',
        '--define-var','KICAD9_3DMODEL_DIR=D:/Program Files/share/kicad/3dmodels',
        '--define-var','KICAD7_3DMODEL_DIR=D:/Program Files/share/kicad/3dmodels',
        '-o',(Join-Path $modelRoot 'reference/board.step'),(Join-Path $repoRoot 'Flatbox-rev8.kicad_pcb'))
    foreach ($modelScript in @('inspect_reference.py','src/heatsink_plate.py','src/heatsink_fit.py',
                             'checks/check_fit.py','src/heatsink_mounting.py','checks/check_mounting.py',
                             'checks/check_usb_top.py','src/mounting_dimensions.py')) {
        RunChecked $cadPython @((Join-Path $modelRoot $modelScript))
    }
    RunChecked $cadPython @((Join-Path $modelRoot 'thermal_mass.py'))
    RunChecked $cadPython @('-m','cadgen.cli','step','snapshot',
        (Join-Path $modelRoot 'STEP/heatsink_plate.step'),(Join-Path $modelRoot 'review/underside.png'),
        '--camera','135:-35')
    RunChecked $cadPython @('-m','cadgen.cli','step','snapshot',
        (Join-Path $modelRoot 'STEP/heatsink_fit.step'),(Join-Path $modelRoot 'review/fit-top.png'),
        '--camera','top')
    foreach ($variant in @('heatsink_mounting','heatsink_mounting_exploded','mounting_dimensions')) {
        RunChecked $cadPython @('-m','cadgen.cli','step','snapshot',
            (Join-Path $modelRoot "STEP/$variant.step"),(Join-Path $modelRoot "review/$variant.png"),
            '--camera','iso')
    }
} finally { Pop-Location }
