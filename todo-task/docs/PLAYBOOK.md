---
title: ToDo Task Playbook
subtitle: From a few words in To Do to finished work
---

# What this is

You capture an idea in a few words on your phone. This playbook is what happens next, every
time, so that no entry is left as a one-line note.

Each entry moves through five stages:

| Stage | What exists at the end of it |
|-------|------------------------------|
| **Captured** | The entry in Microsoft To Do or Todoist, exactly as you typed it. |
| **Briefed** | A full brief in a Word document, and a proper title and description on the task. |
| **In session** | A Claude Code session working from the brief. |
| **Waiting on me** | First results delivered, with a short list of what only you can supply. |
| **Done** | Everything the brief asked for exists, and you can point to it. |

You can write anything in To Do, however short or rough. The procedure below is what gives it
context afterwards, so capturing never needs more than a few seconds.

# The three ways to run it

All three produce the same brief. Use whichever suits the moment.

| Way | Best for | What you do |
|-----|----------|-------------|
| **1. The phone page** | One entry, right now, from your phone | Type the entry, press one button. |
| **2. Word, by hand** | When you want to shape the brief yourself | Copy the template, paste the entry, send the green prompt. |
| **3. The daily sweep** | Everything you captured, without touching it | Nothing. It runs on a schedule. |

## Way 1: the phone page

The page is called **ToDo Task Builder** and is in your Claude artifacts.

1. Type or paste the entry under **Step 1**, or press **Pull from Todoist** and choose one.
2. Press **Expand into a brief**. The first time, Claude asks for permission to be used by
   the page.
3. Read the brief under **Step 2**. Press **Edit** to change anything. Fix what is marked
   "(to confirm)".
4. Under **Step 3**, press **Update the task in Todoist**, or copy the title and description
   into Microsoft To Do.
5. Under **Step 4**, press **Start a Claude Code session**, or **Open Claude Code with this
   brief**.
6. **Save as a Word document** gives you the same document as Way 2.

Every brief you make is listed at the bottom of the page with its stage.

## Way 2: Word, by hand

This is the procedure the template was built for. It needs Word on a computer or Word on
the web, because Claude for Word does not run in Word on a phone.

1. **Copy the template.** Make a copy of `ToDo-Task-Brief-TEMPLATE.docx` and name it for the
   task. Never type into the template itself. On Windows, `New-TaskBrief.ps1` does this step
   and the next one for you.
2. **Paste the entry.** Put it under "1 · Original To Do entry", exactly as you captured it.
3. **Open Claude in Word and start a new chat.** The panel reopens the last conversation it
   had in a document, so always press New chat first.
4. **Send the green prompt.** Copy all of the green text into the panel and send it. If you
   have added the skill (see Setting up), type `/` and choose **todo-task-brief** instead.
5. **Read the yellow brief.** Claude replaces the example with a brief about your entry and
   fills in "4 · To Do write-back". Correct anything marked "(to confirm)".
6. **Write back.** Paste the title and description from section 4 into the task in To Do or
   Todoist. Keep your original entry underneath.
7. **Start the session.** Copy all of the yellow text into a new Claude Code session.
8. **Log it.** Add a row to "5 · Progress log" for every update.

## Way 3: the daily sweep

A scheduled task in Claude Code runs once a day. It:

1. finds Todoist tasks added in the last three days that have no brief;
2. writes a brief for each and has a second agent check it against your entry;
3. puts the new title and description on the task, keeps your original entry underneath,
   adds the full brief as a comment, and adds the label `briefed`;
4. starts a Claude Code session for the briefs Claude can act on, up to three a day;
5. reports what it changed, with the task and session ids as evidence.

It leaves alone: tasks labelled `skip-ai`, tasks labelled `from-email` (another automation
writes those and they already have their own detail), recurring tasks, and anything outside
the Inbox. Add the label `skip-ai` to any entry you want kept exactly as it is.

The limits are in `todo-task/config.json`. Change the numbers there.

# The Word document

| Section | Colour | What it is for |
|---------|--------|----------------|
| 1 · Original To Do entry | Grey box | Your raw entry. It is never edited. |
| 2 · Expansion prompt | **Green** | The instruction you send to Claude in Word. It never changes. |
| 3 · Task brief | **Yellow** | The brief. Claude rewrites it. You paste it into Claude Code. |
| 4 · To Do write-back | Table | The title and description for the task. |
| 5 · Progress log | Table | One row per update: Completed, Waiting on, Next action, Completion evidence. |
| Task record | Table | Where the task lives, so the three places stay linked. |

The yellow section sits between two marker lines, "TASK BRIEF STARTS" and "TASK BRIEF ENDS".
The green prompt points at those lines, so Claude finds the brief even if it cannot see the
highlight colour.

# The brief

Every brief has the same six parts, in the same order.

1. **Working rules for Claude.** One fixed paragraph. It is what makes the brief work as a
   prompt, and it is never reworded.
2. **Title.** Starts with an action word.
3. **Description, Status and Calendar date**, on one line. The description names the outcome.
4. **Context.** One to four short paragraphs, written as you.
5. **Information Needed and Next Actions.** A numbered list. Item 1 starts "Next action:".
6. **Execution Plan for Claude.** Output, Steps, Tools, Rhythm, Done when.

It closes with your original entry, word for word.

The rules the brief is written under:

- **It stays with what you meant.** Grammar is fixed and the idea is filled out. It is not
  swapped for a tidier idea.
- **Nothing is invented.** No names, dates, numbers, people or places you did not mention.
  What is unknown is written as "Not supplied". A best guess is followed by "(to confirm)".
- **It is written as you**, plainly, with no judgement and no warnings you did not ask for.
- **The outcome is simple**: a piece of writing, a plan, video ideas or learning notes.
- **Health**: information and questions are organised for your clinician. No diagnosis and
  no treatment advice.

Not every entry needs a session. How much the brief does depends on the entry:

| The entry is | The brief is | A session? |
|--------------|--------------|------------|
| An idea, a plan, something to learn, something to make | Full | Yes |
| A health question or an appointment | Full, organised for the clinician | Yes, to organise only |
| An errand: buy, pay, book, call, reply | Short | No |
| A thought or a note to self that asks for nothing | Short. Your thought is kept as you wrote it. | No |
| Unreadable, or cut off | Short. Item 1 asks what you meant. | Not until you answer |

# Starting the work in Claude Code

The yellow brief is the whole prompt. Paste it into a new session and send it.

- **From your phone:** press **Start a Claude Code session** or **Open Claude Code with this
  brief** on the phone page. Or open the Code tab in the Claude app, choose the repository,
  paste the brief and send.
- **The model:** choose the most capable model before you send the first message. In a
  session that is already running, send `/model fable` as a message.
- **The project:** if your account has Projects at claude.ai/code, create one called "Ideas
  to Contextual Development using ToDo, Word and Claude" and paste
  `automation/project-instructions.md` into its instructions. Each brief you paste there
  becomes a thread. Project threads do not load this repository's skills, which is why the
  instructions are written to stand alone.

In the session, Claude:

1. does every step that does not depend on you, using a separate agent for each output;
2. leaves the steps that start "When I supply" waiting, instead of guessing;
3. has a checking agent compare the outputs with the brief before anything is reported;
4. saves the files and, when the brief names a Todoist task, adds the result to it as a comment;
5. ends with four lines:

        Completed: what was actually produced, by name
        Waiting on: what you have to supply or decide
        Next action: the single next step, and who takes it
        Completion evidence: the files, tasks or links that show it

An update without evidence is not finished.

# Microsoft To Do

Claude's Microsoft 365 connector does not reach To Do, so To Do needs one of these bridges.

| Bridge | What it does | What it needs |
|--------|--------------|---------------|
| **By hand** | You paste the entry into the phone page or the Word document, and paste the title and description back. | Nothing. |
| **Power Automate, into Todoist** | Every new To Do task is sent to your Todoist Inbox, where the daily sweep picks it up. | A Power Automate flow with standard connectors. |
| **PowerShell** | `Sync-MicrosoftToDo.ps1` reads new To Do tasks into Word documents and writes finished briefs back. | A Windows computer and one sign-in. |

**The Power Automate flow.** In Power Automate, create an automated cloud flow.

1. Trigger: **When a new to-do in a specific folder is created**, from the connector
   "Microsoft To-Do (Business)" for a work account or "Microsoft To-Do (Consumer)" for a
   personal one. Choose the list you capture into.
2. Action: **Send an email (V2)** to your Todoist Inbox's own email address. To find it,
   open the Inbox in Todoist, open the three-dots menu at the top right, choose the option
   for emailing tasks to the project, and copy the address. Put the To Do title in the
   subject: Todoist makes the subject the task name and attaches the body as a comment, so
   anything that matters belongs in the subject. Check that your Todoist plan includes
   forwarding emails.

Do not use Power Automate's own Todoist connector: Microsoft's page for it says its actions
and triggers cannot be used.

Writing the brief back into To Do is done by hand or with the PowerShell script. Power
Automate's "Update to-do" action can set the title and the note if you want to build that
flow yourself.

# Without Claude Code: the command line

The same sweep can run as a plain program, for example from Windows Task Scheduler. It needs
Python and two secrets, set as environment variables and never written into a file:

| Variable | Where it comes from |
|----------|---------------------|
| `TODOIST_API_TOKEN` | Todoist in a browser: your avatar, Settings, Integrations, Developer, "Copy API token". |
| `ANTHROPIC_API_KEY` | An Anthropic API key. Only `expand` and `sweep` use it. |

Run these from the `todo-task` folder:

| Command | What it does |
|---------|--------------|
| `python -m todotask new "the entry"` | Starts the Word document for one entry. |
| `python -m todotask todoist-pull` | Starts a document for every new Todoist entry. |
| `python -m todotask expand brief.json` | Has Claude write the brief. |
| `python -m todotask render brief.json` | Builds the Word document, the prompt and the write-back text. |
| `python -m todotask todoist-writeback brief.json` | Puts the title and description on the task. |
| `python -m todotask sweep` | All of the above for every new entry. Add `--dry-run` to change nothing in Todoist. |

`expand` asks for Claude Fable 5.2 and turns on Anthropic's default fallback, so that if the
first model declines an entry, the recommended fallback model answers in the same request.
Set `TODOTASK_MODEL` to use a different model.

# Setting up, once

Do these in order. Each one is independent, so stop wherever you have enough.

1. **Put the template where Word autosaves.** Save `ToDo-Task-Brief-TEMPLATE.docx` in a
   folder called "ToDo Task" in OneDrive. Documents there save themselves as you work.
   If you only use Word on a computer, you can also put `ToDo-Task-Brief-TEMPLATE.dotx` in
   your Custom Office Templates folder and start each brief from File, New, Personal. Do not
   open the `.dotx` from OneDrive or Word on the web: that edits the template itself.
2. **Install Claude for Word.** Get "Claude for Microsoft 365" from Microsoft AppSource, open
   Word, and sign in with your Claude account. It needs a paid Claude plan. It runs in Word
   for Windows with a Microsoft 365 subscription, Word for Mac, and Word on the web.
3. **Add the skill to Claude.** In Claude, open Customize, then Skills, and upload
   `word-skill/todo-task-brief.zip`. "Code execution and file creation" must be on. In Word
   you can then type `/` and choose **todo-task-brief** instead of copying the green text.
4. **Check the highlight once.** Run the procedure on one entry and look at the result. If
   the new brief is not highlighted yellow, select everything between the two marker lines
   and highlight it. Then tell Claude in Word to keep text it writes there highlighted.
5. **Add the labels to Todoist.** `briefed`, `in-session`, `waiting-on-me`, `content-done`
   and `skip-ai`. The sweep adds any that are missing on its first run.
6. **Turn on the daily sweep.** At claude.ai/code/routines, create a new task. Paste the
   prompt from `automation/scheduled-task-prompt.md`, choose this repository and a daily
   time, keep the Todoist connector and remove the connectors it does not need. The
   repository's skills must be on its default branch for the task to find them.
7. **Windows scripts, if you want them.** Install Claude Code with
   `irm https://claude.ai/install.ps1 | iex` in PowerShell, then see `scripts/`.

# Privacy

- The repository that holds this system is public. Your entries, briefs, Word documents and
  finished content are never committed to it. They live in your Todoist, in your OneDrive,
  and on the phone page, whose saved briefs only you can read.
- The sweep reads every new Inbox entry, including private ones. Label an entry `skip-ai`
  to keep it out.
- Claude does not contact anyone, post anything or spend money for you unless a brief asks.

# When something goes wrong

| What you see | What to do |
|--------------|-----------|
| Claude in Word continues an old conversation | Press New chat in the panel, then send the green prompt again. |
| The edit in Word stops part-way | Send "Continue". If it stops again, ask for the brief first and section 4 second. |
| The new brief is not yellow | Select between the two marker lines and highlight it. |
| The brief says things you did not write | Delete them, or press Try again on the phone page. Tell Claude what was invented. |
| The phone page says Claude cannot be reached | Use **Copy the request**, paste it into any Claude chat, and paste the reply back into the page. |
| The phone page says Todoist is not allowed | Allow it when Claude asks. If it does not ask, reconnect Todoist in Claude under Settings, Connectors. |
| The sweep changed a task you wanted left alone | Your original entry is in the task's description under "Original entry:". Put it back and add `skip-ai`. |
| A session reports something as done with no evidence | Reply: "Show the completion evidence." The working rules require it. |

# One-page reference

**Capture:** type it into To Do or Todoist. Short is fine.

**Brief:** phone page, or Word with the green prompt, or wait for the daily sweep.

**Write back:** new title, new description, original entry kept underneath, label `briefed`.

**Session:** paste the yellow brief into Claude Code. Most capable model.

**Every update ends with:** Completed; Waiting on; Next action; Completion evidence.

**Labels:** `briefed` → `in-session` → `waiting-on-me` → `content-done`. `skip-ai` opts out.
