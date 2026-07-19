param(
    [ValidateSet("cuas", "perimeter_ct_cuas", "generic")]
    [string]$Payload = "cuas",
    [ValidateSet("true", "false")]
    [string]$SimMode = "true"
)

$ErrorActionPreference = "Stop"

Write-Host "Starting ClearSky-OS with payload=$Payload sim_mode=$SimMode"
$env:CLEARSKY_PAYLOAD = $Payload
$env:CLEARSKY_SIM_MODE = $SimMode
docker compose -f docker/docker-compose.yml up --build clearsky-os
