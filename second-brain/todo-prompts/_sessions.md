# Priority sessions

The generated files cover every task. These twelve sessions group the tasks
that matter most to the brief (prompts, agents, PARA, journaling, capture,
inspiration) and to money and safety. Each session is one Claude Code
conversation on this repository. Run them in order.

## Session 1: Money and safety this week (30 minutes)

Tasks: failed subscription payments on the company card; remove the company
card from Google Play AI Ultra and tell Jason; Initio insurance card; Apple TV
billing; Yorke's four website questions by 12 Nov; Waterford Press advert;
Grant's approval for NAS access; PayPal changes check.

```text
Open second-brain/todo-prompts/finance-admin/ and the [MONEY] and [ACTION]
files dated 2026-11-06 to 2026-11-10 in it-devices-storage and
marketing-content. For each, produce the exact message or steps and a
Morgen calendar line. Make no payments and send nothing; put drafts in
second-brain/00_Inbox/_drafts/. Finish with a 10-line checklist I can clear
today.
```

## Session 2: Save all prompts (the task that started this)

Tasks: SAVE ALL PROMPTS, RESEARCH NEW PROMPT LISTS; Search for prompts to
copy; Transfer ChatGPT prompts and folder structure to Claude; Prompts for my
new book (saved); Notes when vibe coding; Prompt ideas for Replit, Lovable,
OpenClaw.

```text
The prompt library is at second-brain/30_Resources/Prompts. Read its README.
Then: (1) export my ChatGPT and Claude.ai saved prompts when I paste them in,
normalise each to the library format, file by stage; (2) add a
"book-writing" folder with prompts for memoir structure, chapter outline
from journal entries, and voice consistency; (3) add a "vibe-coding" folder
with design-brief, bug-report and feature-request prompts for Lovable and
Replit; (4) update the library README table.
```

## Session 3: Master prompt for my life and role

Tasks: Create a master prompt for my life; 20 pages for a master prompt;
Master prompt for my role; Whisper Flow to answer the master prompt
questions; Master prompt is a document you create for your role; Help me
create a master prompt, ask me the questions, save as PDF.

```text
Run the interview in
second-brain/30_Resources/Prompts/05_agents/master-life-prompt-builder.md
with me, one question at a time. I will dictate answers. Then build
second-brain/00_Brief/02_master-life-prompt.md and the 300-word short
version. Also build second-brain/00_Brief/03_master-role-prompt.md for my
Hydralada marketing role from the same transcript plus the Hydralada
voice guide. Export both to PDF in 00_Brief/exports/.
```

## Session 4: PARA everywhere

Tasks: Amerigo, OneCommander, Opus, Fabric, bookmarks, YouTube playlists on
the same PARA framework; Build the folder template structure for video
projects plus CODE and PARA; Re-organise folder structures on work and home
NAS; Work out a solid plan for filing; Do file audit once migrated to NAS;
Tidy up Google Bookmarks using CODE and PARA; Use Python to automate my
bookmark structure.

```text
Using second-brain/30_Resources/Frameworks/PARA.md and
second-brain/scripts/para_scaffold.py: (1) produce the PARA tree for the
home NAS, the work NAS personal area, OneDrive personal, Dropbox /Brad Smith,
Chrome bookmarks and YouTube playlists, with identical names; (2) run the
Folder Tree Designer prompt against the Dropbox /Brad Smith listing I paste
in and produce the move plan; (3) write a video-project folder template
under 30_Resources/Templates/video-project/ (01_Brief, 02_Footage, 03_Audio,
04_Graphics, 05_Project-Files, 06_Exports/{extra-long,long,short,social-short,vertical},
07_Delivered); (4) write scripts/bookmarks_to_para.py that reads a Chrome
bookmarks HTML export and writes a re-foldered one. No moves on live stores.
```

## Session 5: Journal every day

Tasks: Journal every day; Start bullet journalling; Keep a journal/diary;
One location for all journaling; Plan my day the night before; Start saving
each day's tasks with the current date; Have a theme for each day; Voice to
text for journalling; Use Remarkable for impressions and set up a system.

```text
Set up the journaling flow: confirm second-brain/20_Areas/Journal exists with
the year folder, test the Morning Pages and Evening Shutdown prompts on a
sample dictation I paste in, write the Remarkable export procedure
(reMarkable app > export as text > drop in 00_Inbox/_dictation/), and give me
the exact /schedule commands for the Journal Agent from
second-brain/routines/schedules.md. Then draft the first weekly reflection
from whatever entries exist.
```

## Session 6: Agents and loops

Tasks: Workflows for AI agents; Set up AI agents using OpenClaw; Have
OpenClaw read and do my to-do tasks; Have Claude Cowork read and action my
To Do tasks; Use AI agents to add context to each To Do task; Start creating
loops instead of just prompting Claude; Automate task creation from WhatsApp
into To Do, ClickUp, Morgen, Notion, Smartsheet; Agents set up to do my
to-dos.

```text
Read second-brain/agents/README.md and routines/schedules.md. Activate the
Weekly Review Agent as a cloud scheduled task with Todoist and Google
Calendar read-only. Then write agents/11-whatsapp-capture-agent.md: WhatsApp
export file in 00_Inbox/_dictation/ to tasks and notes, using the Voice Note
to Tasks prompt. Then write the OpenClaw and n8n equivalents of the Capture
Agent as JSON workflow stubs under agents/runtimes/, read-only on Todoist.
```

## Session 7: Pinterest to Dropbox and the inspiration library

Tasks: FOCUS ON BRAND DESIGN EXAMPLES ON PINTEREST, MIND ARCHITECTURE, BRAND
ARCHITECTURE; FOCUS ON PORSCHE BRANDING; Remarkable for architecture;
Alterations ideas for Morley; Houseboat and dam ideas; Put Pinterest on the
software stack Smartsheet; Fetch all data from Pinterest, Awwwards, Behance
and regenerate for Instagram.

```text
Guide me through creating the Pinterest and Dropbox tokens per
second-brain/scripts/README.md, then run scripts/pinterest_to_dropbox.py
--dry-run and show the boards. Run the Pin Board Audit prompt on the dry-run
manifest. Create the mood-board briefs for Toop Street alterations, the
houseboat and the Hydralada rebrand using the Mood Board Brief prompt, saved
under 10_Projects. Never delete; never post.
```

## Session 8: Quotes and cards

Tasks: Add quotes (routine); 360 quote cover images; Set up personal LinkedIn
for inspirational quotes and images; Create pithy statements with depth
(spreadsheet); Post "Let go and let God" script; Good Measure quote cards.

```text
Run the Quote Curator for the first four themes in
second-brain/routines/quote-themes.md, then the Quote Card Generator for the
best eight per theme in the Good Measure style used in /cards. Save spec
sheets to 30_Resources/Inspiration/Quote-Cards/ and a two-week Metricool
schedule table. Draft (do not post) the LinkedIn caption for the "Let go and
let God" script image from the Todoist description.
```

## Session 9: Marketing material capture and the content pipeline

Tasks: Fibreglass cage video; 50 Years video; Steve Cartwright and TBX
testimonials; Spring Hill machines on Preowned page; LV cage brochure;
Mango spec sheet reprint; Trimmer brochure; each video in five versions;
Checklist for video creation; Boast.io for testimonials; Blogs as a knowledge
base; AEO research.

```text
For every file in second-brain/todo-prompts/marketing-content/ with a due
date or a named customer, run the Marketing Brief prompt and save
10_Projects/<name>/brief.md. Build 30_Resources/Templates/video-checklist.md
from the briefs (shoot, edit on local SSD, five versions, approval,
distribution via HubSpot, DAM and NAS). List the Dropbox Hydralada Marketing
"DUMP - TO BE SORTED" files I paste in and propose their homes. Drafts only.
```

## Session 10: IT, storage and the one PARA tree on the NAS

Tasks: OneDrive to NAS migrations; T9 recovery; two SSDs in home NAS;
Backblaze plan; Canto DAM decision; "managed by your organisation";
Streamline removal; Claude Code history from the Legion to the HP; CrowdStrike
connector; SSL and proxy for Claude Code.

```text
Work through second-brain/todo-prompts/it-devices-storage/ but only the
files mentioning NAS, OneDrive, T9, backup, Canto, Backblaze, Claude Code
history or managed-device policy. Produce one runbook at
20_Areas/IT-Devices-and-Storage/runbook.md: verified backup first, then
migration order, then de-sync, with checkpoints. Separate "things I control
on my own device" from "things to raise with OneHQ or First Focus". No
deletions proposed until two verified copies exist.
```

## Session 11: Health logistics (private)

Tasks: everything in todo-prompts/health-medical/. Logistics only.

```text
Read second-brain/todo-prompts/health-medical/ and produce three files under
20_Areas/Health: questions-for-clinicians.md grouped by specialist,
appointments.md with every date found, supplies.md listing what is on repeat
and who orders it. Propose which Todoist items collapse into one recurring
"monthly supplies" task. Give no medical advice. Keep everything inside this
repository.
```

## Session 12: Google account consolidation and NEXUS launch

Tasks: the Google Account Consolidation project (passkeys, 2SV, forwarding,
imports, archive mode) and the NEXUS to Google Play project (PWA layer,
Bubblewrap, testers, store listing, compliance pack).

```text
These two Todoist projects already carry detailed runbooks in their task
descriptions. Pull the tasks from second-brain/todo-prompts/ with project
"Google Account Consolidation" and "NEXUS to Google Play Store", order them
into a dependency sequence, and write 10_Projects/2026-04_google-account-consolidation/plan.md
and 10_Projects/2026-03_nexus-google-play/plan.md with checkboxes, owners
(Brad or Claude) and the first three actions for each. Flag anything that
needs a decision from Brad before Claude can proceed.
```
