"""Compatibility entry point for the working local Bambu Studio CLI runner."""
from pathlib import Path
import shutil, subprocess, sys
HERE=Path(__file__).resolve().parent
name=sys.argv[1] if len(sys.argv)>1 else 'stacked_kit_inset'
if name not in ('stacked_kit_inset','separator_trial'):
    raise SystemExit('The original stacked_kit is superseded; use stacked_kit_inset.')
shell=shutil.which('pwsh') or shutil.which('powershell')
if not shell:raise SystemExit('PowerShell is required for the local Bambu CLI runner.')
raise SystemExit(subprocess.run([shell,'-NoProfile','-File',str(HERE/'slice_stack.ps1'),'-Model',name]).returncode)
