# PowerShell launcher for CE-2 (Windows-native, per the user's preference)
param(
    [int]$Scenarios = 12,
    [int]$Seed = 12345
)

$ErrorActionPreference = "Stop"

$ProjectDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $ProjectDir

$env:ANONYMIZED_TELEMETRY = "False"
$env:HF_HUB_OFFLINE = "1"

Write-Host "Running CE-2: $Scenarios scenarios, seed $Seed" -ForegroundColor Cyan
python -u runner/ce2_runner.py

Write-Host ""
Write-Host "Running tests..." -ForegroundColor Cyan
python -m pytest -q