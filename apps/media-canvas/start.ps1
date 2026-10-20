param([switch]$NoBrowser,[string]$DataDir,[ValidateRange(1,65535)][int]$Port=8961,[string]$Registry,[string]$WorkspaceRoot)
$ErrorActionPreference = 'Stop'
$canvasPython = if ($env:MEDIA_CANVAS_PYTHON) { $env:MEDIA_CANVAS_PYTHON } else { (Get-Command python -ErrorAction Stop).Source }
$canvasArgs = @('-B','-X','utf8',(Join-Path $PSScriptRoot 'launcher.py'),'--port',$Port)
if ($NoBrowser) { $canvasArgs += '--no-browser' }
if ($DataDir) { $canvasArgs += @('--data-dir',$DataDir) }
if ($Registry) { $canvasArgs += @('--registry',$Registry) }
if ($WorkspaceRoot) { $canvasArgs += @('--workspace-root',$WorkspaceRoot) }
& $canvasPython @canvasArgs
if ($LASTEXITCODE -ne 0) { throw 'Canvas could not start; see the error above.' }
