<#
.SYNOPSIS
    Starts a ToDo Task Brief document for one To Do entry and opens it in Word.

.DESCRIPTION
    Makes a dated folder for the task inside your "ToDo Task" folder in OneDrive, builds the
    Word document with your entry at the top, and opens it. In Word, open the Claude panel,
    start a new chat, and send the green prompt (or type / and choose todo-task-brief).

    Not yet run on a Windows machine. Try it once with -NoOpen and check the folder it makes.

.EXAMPLE
    .\New-TaskBrief.ps1 "garden timelapse vid?? 30 days tomatoes.. phone on tripod.. music"

.EXAMPLE
    .\New-TaskBrief.ps1 -Entry "ring D about the fridge light" -Notes "he is away until Friday" -Source "Todoist"
#>
param(
    [Parameter(Mandatory = $true, Position = 0)]
    [string]$Entry,
    [string]$Notes = "",
    [string]$Source = "Microsoft To Do",
    [string]$List = "",
    [string]$TaskId = "",
    [string]$Folder = "",
    [switch]$NoOpen
)

$ErrorActionPreference = "Stop"
$todoTask = Split-Path -Parent $PSScriptRoot

if (-not $Folder) {
    $base = if ($env:OneDrive) { $env:OneDrive } else { [Environment]::GetFolderPath("MyDocuments") }
    $Folder = Join-Path $base "ToDo Task"
}
New-Item -ItemType Directory -Force -Path $Folder | Out-Null

$document = $null
if (Get-Command python -ErrorAction SilentlyContinue) {
    # The entry goes through a file so that quotes and line breaks in it survive.
    $entryFile = Join-Path ([IO.Path]::GetTempPath()) ("todo-task-entry-" + [Guid]::NewGuid().ToString("N") + ".json")
    @{ text = $Entry; notes = $Notes; source = $Source; list = $List; task_id = $TaskId } |
        ConvertTo-Json | Set-Content -Path $entryFile -Encoding UTF8
    Push-Location $todoTask
    try {
        $printed = & python -X utf8 -m todotask new --from-json $entryFile --out $Folder
        if ($LASTEXITCODE -ne 0) { throw "The document could not be built. Run 'python -m pip install python-docx' and try again." }
    }
    finally {
        Pop-Location
        Remove-Item $entryFile -ErrorAction SilentlyContinue
    }
    $document = $printed | Where-Object { $_ -like "*.docx" } | Select-Object -First 1
}
else {
    # No Python on this computer: copy the blank template, and put the entry on the clipboard.
    $stamp = Get-Date -Format "yyyy-MM-dd-HHmm"
    $document = Join-Path $Folder "$stamp-todo-task-brief.docx"
    Copy-Item (Join-Path $todoTask "templates\ToDo-Task-Brief-TEMPLATE.docx") $document
    Set-Clipboard -Value $Entry
    Write-Host "Python was not found, so a blank copy was made. Your entry is on the clipboard: paste it under section 1."
}

Write-Host "Document: $document"
if (-not $NoOpen) { Start-Process $document }
