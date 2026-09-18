$ErrorActionPreference = "Stop"

$ProjectRoot = Split-Path -Parent $PSScriptRoot
Set-Location $ProjectRoot
$env:PYTHONIOENCODING = "utf-8"
$env:PYTHONPATH = Join-Path $ProjectRoot "src"
$Python = "E:\anaconda\envs\dl\python.exe"

& $Python -m defect_detection.cli prepare-data --source data\raw\neu-det-source --output data\processed\neu-det --report reports\neu-det-stats.json --force
if ($LASTEXITCODE -ne 0) { throw "Dataset preparation failed." }

& $Python -m defect_detection.cli validate --data data\processed\neu-det\data.yaml
if ($LASTEXITCODE -ne 0) { throw "Dataset validation failed." }

Write-Host "NEU-DET dataset preparation completed."