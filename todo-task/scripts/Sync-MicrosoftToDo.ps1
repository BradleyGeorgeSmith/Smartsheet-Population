<#
.SYNOPSIS
    Moves entries between Microsoft To Do and the ToDo Task pipeline.

.DESCRIPTION
    -Do Lists      shows your To Do lists, so you can pick the one you capture into.
    -Do Pull       finds tasks added to that list in the last few days that are not yet
                   marked "Briefed", and starts a ToDo Task Brief document for each.
    -Do WriteBack  takes a finished brief.json and puts its title and description on the
                   task in To Do, keeps your original entry underneath, and marks the task
                   "Briefed".

    Needs the Microsoft Graph PowerShell module, once:
        Install-Module Microsoft.Graph.Authentication -Scope CurrentUser
    The first run opens a Microsoft sign-in and asks for permission to read and change your
    tasks (Tasks.ReadWrite). Sign in with the account your To Do lists belong to.

    Not yet run on a Windows machine, and sign-in with a personal Microsoft account through
    this module is not confirmed by Microsoft's documentation. Run -Do Lists first: if your
    lists appear, the rest will work with the same sign-in.

.EXAMPLE
    .\Sync-MicrosoftToDo.ps1 -Do Lists

.EXAMPLE
    .\Sync-MicrosoftToDo.ps1 -Do Pull -ListName "Tasks" -Days 3

.EXAMPLE
    .\Sync-MicrosoftToDo.ps1 -Do WriteBack -Brief "C:\Users\me\OneDrive\ToDo Task\2026-11-19-plan-a-video\brief.json"
#>
param(
    [ValidateSet("Lists", "Pull", "WriteBack")]
    [string]$Do = "Lists",
    [string]$ListName = "Tasks",
    [int]$Days = 3,
    [string]$Brief = "",
    [string]$Folder = "",
    [switch]$DryRun
)

$ErrorActionPreference = "Stop"
$marker = "Briefed"
$api = "https://graph.microsoft.com/v1.0/me/todo/lists"

if (-not (Get-Module -ListAvailable Microsoft.Graph.Authentication)) {
    throw "Run this once first:  Install-Module Microsoft.Graph.Authentication -Scope CurrentUser"
}
Import-Module Microsoft.Graph.Authentication
if (-not (Get-MgContext)) { Connect-MgGraph -Scopes "Tasks.ReadWrite" -NoWelcome }

function Get-All($uri) {
    # Follows the paging links until every item has been read.
    $items = @()
    while ($uri) {
        $page = Invoke-MgGraphRequest -Method GET -Uri $uri
        $items += $page.value
        $uri = $page.'@odata.nextLink'
    }
    return $items
}

$lists = Get-All $api

if ($Do -eq "Lists") {
    $lists | ForEach-Object { [pscustomobject]@{ Name = $_.displayName; Id = $_.id } } | Format-Table -AutoSize
    return
}

if ($Do -eq "Pull") {
    $list = $lists | Where-Object { $_.displayName -eq $ListName } | Select-Object -First 1
    if (-not $list) { throw "No To Do list is called '$ListName'. Run with -Do Lists to see the names." }

    $since = (Get-Date).ToUniversalTime().AddDays(-$Days)
    $tasks = Get-All "$api/$($list.id)/tasks?`$top=100" | Where-Object {
        $_.status -ne "completed" -and
        ([datetime]$_.createdDateTime).ToUniversalTime() -ge $since -and
        -not ($_.categories -contains $marker)
    }
    if (-not $tasks) { Write-Host "No new entries in '$ListName' in the last $Days days."; return }

    foreach ($task in $tasks) {
        Write-Host "Entry: $($task.title)"
        if ($DryRun) { continue }
        $notes = if ($task.body -and $task.body.contentType -eq "text") { [string]$task.body.content } else { "" }
        $arguments = @{
            Entry  = $task.title
            Notes  = $notes.Trim()
            Source = "Microsoft To Do"
            List   = $ListName
            TaskId = "$($list.id)|$($task.id)"
            NoOpen = $true
        }
        if ($Folder) { $arguments.Folder = $Folder }
        & (Join-Path $PSScriptRoot "New-TaskBrief.ps1") @arguments
    }
    return
}

if ($Do -eq "WriteBack") {
    if (-not $Brief -or -not (Test-Path $Brief)) { throw "Give the path of a finished brief.json with -Brief." }
    $data = Get-Content -Raw -Encoding UTF8 $Brief | ConvertFrom-Json
    $ids = ([string]$data.entry.task_id).Split("|")
    if ($ids.Count -ne 2) { throw "This brief did not come from Microsoft To Do, so there is no task to write back to." }
    if (-not $data.writeback.title) { throw "This brief has not been expanded yet: its write-back title is empty." }

    $text = $data.writeback.description + "`n`nOriginal entry: " + $data.entry.text
    if ($data.entry.notes) { $text += "`n`nOriginal notes: " + $data.entry.notes }
    # To Do stores the note as HTML, so the text is escaped and its line breaks kept.
    $html = [System.Net.WebUtility]::HtmlEncode($text).Replace("`n", "<br>")

    $taskUri = "$api/$($ids[0])/tasks/$($ids[1])"
    $current = Invoke-MgGraphRequest -Method GET -Uri $taskUri
    $categories = @($current.categories | Where-Object { $_ }) + $marker | Select-Object -Unique

    $change = @{
        title      = [string]$data.writeback.title
        body       = @{ content = $html; contentType = "html" }
        categories = @($categories)
    }

    Write-Host "Task:  $($current.title)"
    Write-Host "Title: $($data.writeback.title)"
    if ($DryRun) { Write-Host "Dry run: nothing was changed."; return }

    Invoke-MgGraphRequest -Method PATCH -Uri $taskUri -Body $change | Out-Null
    $after = Invoke-MgGraphRequest -Method GET -Uri $taskUri
    Write-Host "Written. The task is now titled: $($after.title)"
}
