<#
.SYNOPSIS
    Makes Windows run the ToDo Task sweep every day at a set time.

.DESCRIPTION
    Adds a task to Windows Task Scheduler that runs Start-TodoSweep.ps1 daily. The computer
    has to be on and signed in at that time. To stop it, run with -Remove.

    The scheduled task in the cloud does the same job without this computer being on.

    Not yet run on a Windows machine.

.EXAMPLE
    .\Register-TodoSweepTask.ps1 -At "07:30"

.EXAMPLE
    .\Register-TodoSweepTask.ps1 -Remove
#>
param(
    [string]$At = "07:30",
    [string]$TaskName = "ToDo Task sweep",
    [switch]$Remove
)

$ErrorActionPreference = "Stop"

if ($Remove) {
    Unregister-ScheduledTask -TaskName $TaskName -Confirm:$false
    Write-Host "Removed '$TaskName'."
    return
}

$script = Join-Path $PSScriptRoot "Start-TodoSweep.ps1"
$action = New-ScheduledTaskAction -Execute "powershell.exe" -Argument "-NoProfile -ExecutionPolicy Bypass -File `"$script`""
$trigger = New-ScheduledTaskTrigger -Daily -At $At
Register-ScheduledTask -TaskName $TaskName -Action $action -Trigger $trigger -Force `
    -Description "Expands new Todoist tasks into briefs with Claude Code." | Out-Null

Write-Host "'$TaskName' will run every day at $At. Run it once now from Task Scheduler to check it works."
