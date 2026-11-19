<#
.SYNOPSIS
    Sends one To Do entry to Claude Code, which expands it into a brief.

.DESCRIPTION
    Starts your ToDo Task scheduled task through its API trigger, with the entry as its text.
    Set these two environment variables first, using the address and token that the API
    trigger showed when you added it at claude.ai/code/routines:

        setx TODO_TASK_FIRE_URL   "https://api.anthropic.com/v1/claude_code/routines/<id>/fire"
        setx TODO_TASK_FIRE_TOKEN "<the token>"

    The token is a password. Never put it in a file in this repository.
    The API trigger is a research preview, so the address and headers may change.

    Not yet run on a Windows machine.

.EXAMPLE
    .\Send-ToDoEntry.ps1 "vid idea: why I stopped scrolling before bed"
#>
param(
    [Parameter(Mandatory = $true, Position = 0)]
    [string]$Entry
)

$ErrorActionPreference = "Stop"
$url = $env:TODO_TASK_FIRE_URL
$token = $env:TODO_TASK_FIRE_TOKEN
if (-not $url -or -not $token) {
    throw "Set TODO_TASK_FIRE_URL and TODO_TASK_FIRE_TOKEN first. Run 'Get-Help .\Send-ToDoEntry.ps1 -Full' to see how."
}

$headers = @{
    "Authorization"     = "Bearer $token"
    "anthropic-beta"    = "experimental-cc-routine-2026-04-01"
    "anthropic-version" = "2023-06-01"
}
$body = [System.Text.Encoding]::UTF8.GetBytes((@{ text = $Entry } | ConvertTo-Json))
$reply = Invoke-RestMethod -Method Post -Uri $url -Headers $headers -ContentType "application/json; charset=utf-8" -Body $body

Write-Host "Sent. Session: $($reply.claude_code_session_url)"
