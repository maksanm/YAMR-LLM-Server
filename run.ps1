$env:SERVER_HOST = "localhost"
$env:SERVER_PORT = "2334"

$ErrorActionPreference = "Stop"

# Get all Python executables in PATH
$pythonExecutables = (Get-Command -All -Name python*).Source

# Check if Python 3.8 to 3.11 is installed
$pythonInstalled = $false
$pythonPath = ""
Write-Host -ForegroundColor green "Looking for a compatible Python installation..."
foreach ($pythonExe in $pythonExecutables) {
    $pythonVersionString = & $pythonExe --version 2>&1
    if ($pythonVersionString -match "Python (\d+)\.(\d+)(\.(\d+))?") {
        $majorVersion = [int]$Matches[1]
        $minorVersion = [int]$Matches[2]
        if ($majorVersion -eq 3 -and 8 -le $minorVersion -and $minorVersion -le 11) {
            Write-Host -ForegroundColor green "Python $majorVersion.$minorVersion detected. Proceeding with this version..."
            $pythonInstalled = $true
            $pythonPath = $pythonExe
            break
        }
    }
}

if (-not $pythonInstalled) {
    Write-Host -ForegroundColor red "No suitable Python version detected. Halting the process... Only versions 3.8 to 3.11 are permitted."
    exit
}

$venvExists = Test-Path "./.venv"
if (-not $venvExists) {
    Write-Host -ForegroundColor green "Creating virtual environment..."
    & $pythonPath -m venv .venv

    Write-Host -ForegroundColor green "Activating virtual environment..."
    . .venv/Scripts/Activate.ps1

    Write-Host -ForegroundColor green "Installing packages from requirements.txt..."
    & python -m pip install -r requirements.txt
}
else {
    Write-Host -ForegroundColor green "An existing virtual environment found. Activating..."
    . .venv/Scripts/Activate.ps1
}

Write-Host -ForegroundColor green "Starting server with Uvicorn..."
& python src/server.py