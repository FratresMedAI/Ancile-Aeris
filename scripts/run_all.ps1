param(
    [ValidateSet("cuas", "conservation", "generic")]
    [string]$Payload = "cuas",
    [ValidateSet("true", "false")]
    [string]$SimMode = "true"
)

$ErrorActionPreference = "Stop"

Write-Host "Starting Ancile-Aeris with payload=$Payload sim_mode=$SimMode"
$env:ANCILE_PAYLOAD = $Payload
$env:ANCILE_SIM_MODE = $SimMode
docker compose -f docker/docker-compose.yml up --build ancile-aeris
