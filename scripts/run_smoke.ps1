$ErrorActionPreference = 'Stop'
$python = Join-Path $PSScriptRoot '..\.venv\Scripts\python.exe'
& $python -m pytest -q
& $python -m veo_nyu.cli smoke
