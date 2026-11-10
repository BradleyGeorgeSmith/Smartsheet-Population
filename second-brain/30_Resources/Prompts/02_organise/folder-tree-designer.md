# Folder Tree Designer (PARA for a drive, NAS or Dropbox)

**Purpose**: design or repair a PARA folder tree for a specific storage
location, given a listing of what is already there.
**When**: setting up a new device, NAS share, Dropbox root or OneDrive.
**Inputs**: `{{listing}}` (output of `dir /s /b` or `tree` or a Dropbox
folder list), `{{location_name}}`, `{{projects}}`, `{{areas}}`.

```text
I am applying Tiago Forte's PARA method to {{location_name}}.

Existing folders (one per line, may be messy, may contain duplicates):
<listing>
{{listing}}
</listing>

Active projects: {{projects}}
Areas of responsibility: {{areas}}

Produce:
1. TARGET TREE: a PARA tree with these fixed roots: 00_Inbox, 10_Projects,
   20_Areas, 30_Resources, 40_Archives. Under 10_Projects use
   YYYY-MM_short-name. Under 40_Archives use YYYY_original-name. Two levels
   deep maximum. Show it as an indented list.
2. MOVE PLAN: a table of "existing folder -> target folder" covering every
   existing folder. Mark likely duplicates ("_Potential Duplicates",
   "(1)", "copy") as MERGE with the folder they merge into.
3. SYSTEM FOLDERS: list folders that look like OS or app clutter
   (System Volume Information, AppData, ProgramData, adobeTemp) and mark
   them LEAVE or DELETE-AFTER-CHECK. Never mark anything DELETE outright.
4. RISKS: anything where moving could break an app link (Adobe project
   folders, Premiere media, Sketchup assets). Suggest relink steps.
5. SCRIPT: a Windows PowerShell block and a bash block that create the
   TARGET TREE only (no moves). Moves stay manual until I approve.

Keep names short so OneDrive path length stays under 200 characters.
```

**Output**: tree, move plan, and creation scripts.
**Source**: original, informed by Forte's PARA and Brad's Dropbox listing.
