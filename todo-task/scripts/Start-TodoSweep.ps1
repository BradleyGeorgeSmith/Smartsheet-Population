<#
.SYNOPSIS
    Runs the ToDo Task sweep on this computer with Claude Code.

.DESCRIPTION
    Asks Claude Code to find every new Todoist task without a brief, expand each one, write
    the new title and description back, and start sessions for the ones Claude can act on.

    The scheduled task in the cloud (see automation\scheduled-task-prompt.md) does the same
    job without this computer being on, and is the recommended way to run the sweep daily.
    Use this script when you want a sweep now, from your own machine.

    Claude Code on this computer must be able to reach Todoist. Check by running 'claude',
    then '/mcp', and looking for Todoist in the list.

    Not yet run on a Windows machine. Start with -DryRun.

.EXAMPLE
    .\Start-TodoSweep.ps1 -DryRun

.EXAMPLE
    .\Start-TodoSweep.ps1 -Days 7 -Limit 5 -Model fable
#>
param(
    [switch]$DryRun,
    [int]$Days = 0,
    [int]$Limit = 0,
    [string]$Model = ""
)

$ErrorActionPreference = "Stop"
$repository = Split-Path -Parent (Split-Path -Parent $PSScriptRoot)

if (-not (Get-Command claude -ErrorAction SilentlyContinue)) {
    throw "Claude Code is not installed. In PowerShell run:  irm https://claude.ai/install.ps1 | iex"
}

$request = "/todo-task-sweep"
if ($DryRun) { $request += " dry-run" }
if ($Days -gt 0) { $request += " days=$Days" }
if ($Limit -gt 0) { $request += " limit=$Limit" }

$logFolder = Join-Path $repository "briefs"
New-Item -ItemType Directory -Force -Path $logFolder | Out-Null
$log = Join-Path $logFolder ("sweep-" + (Get-Date -Format "yyyy-MM-dd-HHmm") + ".log")

$arguments = @("-p", $request)
if ($Model) { $arguments += @("--model", $Model) }

Push-Location $repository
try {
    & claude @arguments 2>&1 | Tee-Object -FilePath $log
}
finally {
    Pop-Location
}
Write-Host "Log: $log"
