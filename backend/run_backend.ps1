param(
    [string]$HostAddress = "127.0.0.1",
    [int]$Port = 8000
)

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path

& python -m uvicorn app.main:app --host $HostAddress --port $Port --app-dir $scriptDir
