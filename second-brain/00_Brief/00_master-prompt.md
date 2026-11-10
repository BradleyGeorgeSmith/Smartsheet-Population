# Master Brief: Build Brad's AI-Operated Second Brain

> This is the rewritten, expanded version of the original request. It is the
> prompt that drives this whole system. Re-run it (or any section of it) in a
> Claude Code session opened on this repository to extend or repair the system.

## 1. Role and standards

You are a senior knowledge-systems architect and AI-operations engineer. You
combine Tiago Forte's *Building a Second Brain* (CODE: Capture, Organise,
Distil, Express) and *The PARA Method* (Projects, Areas, Resources, Archives)
with modern agentic tooling (Claude Code, scheduled tasks, MCP connectors,
Fabric patterns). Work to the standard of a careful colleague: finish the whole
job, cite sources, write things a future reader can act on without you.

## 2. Context you must respect

- Owner: Brad Smith, marketing and content lead at Hydralada (NZ), running
  personal ventures (NEXUS app, mindfulmomentum.tech, Toop Street property,
  Morley Studio) and a long recovery from serious illness.
- Existing stack: Todoist (migrated from Microsoft To Do, roughly 1,000 open
  items), ClickUp, Smartsheet, Notion, Dropbox (team "Hydralada", personal
  folder `/Brad Smith`), OneDrive, QNAP NAS, Remarkable tablet, Reflect,
  Morgen calendar, Adobe suite, Lovable, Replit, Fabric, Pinterest, Substack.
- Preferred organising principle: PARA everywhere (Todoist already has
  `01 Capture`, `02 Organise`, `04 Reflect/Distil`, `04 Express`, `07 Projects`,
  `07 Areas`, `07 Resource`, `07 Archive`). Mirror the same numbering across
  Dropbox, NAS, bookmarks, YouTube playlists and notebooks.
- Privacy: tasks include medical, financial and spiritual material. Keep the
  repository private, never paste personal identifiers into third-party
  services, and keep health items in `20_Areas/Health` only.

## 3. Deliverables

1. **Prompt library** (`30_Resources/Prompts`). Collect the strongest publicly
   licensed prompts for: productivity systems, self-improvement and habit
   design, accelerated learning, second-brain journaling, efficiency and
   time-blocking, marketing material capture, visual inspiration capture
   (Pinterest to Dropbox), and inspirational quotes and imagery for
   architecture, manufacturing and innovation. Attribute every source. Where a
   source is copyrighted, link and summarise rather than copy. Where it is
   MIT or CC0 (for example Daniel Miessler's Fabric patterns), copy the text
   verbatim with the licence beside it. Write original prompts to fill gaps.
2. **PARA folder structure** (`00_Inbox`, `10_Projects`, `20_Areas`,
   `30_Resources`, `40_Archives`) with a README in each explaining the filing
   rule, plus a script that recreates the same tree on Windows, the NAS and
   Dropbox.
3. **Agents** (`agents/`). One specification per agent: purpose, triggers,
   inputs, tools and connectors, step-by-step procedure, outputs, guardrails,
   and the exact prompt to paste into a Claude Code session or scheduled task.
   Required agents: Capture, Organise (PARA router), Distil (progressive
   summarisation), Express (content and marketing output), Pinterest-to-
   Dropbox, Quote and Image Curator, Marketing Material Capture, To-do Triage,
   Journal, Weekly Review.
4. **Routines and loops** (`routines/`). Daily morning plan, daily shutdown,
   weekly review (Forte's nine-step checklist adapted), monthly PARA
   re-sort, quarterly archive sweep. Give each one a cron expression, the
   `/schedule` command for a cloud scheduled task, the `/loop` form for an
   open session, and a `.claude/loop.md` default prompt.
5. **Scripts** (`scripts/`). Pinterest board to Dropbox sync using the
   official Pinterest API v5 and Dropbox API, with a dry-run mode; a quote
   fetcher for architecture, manufacturing and innovation themes with
   attribution; the folder scaffolder; and the to-do prompt generator.
6. **A prompt for every saved to-do** (`todo-prompts/`). Pull every open
   Todoist task. For each one write: the task as captured, its PARA home,
   a category, a contextual elaboration (why it matters, what done looks
   like), a ready-to-run prompt tailored to the task type, and concrete next
   steps. Group them so related items can be run as one session. Produce an
   index.
7. **Operating manual** (`README.md`, `CLAUDE.md`) so any future session knows
   where everything lives and how to extend it.

## 4. Method

1. Research first: Forte Labs (PARA, CODE, progressive summarisation, weekly
   review), Anthropic's prompt engineering guidance, Fabric patterns, Claude
   Code scheduled tasks and `/loop` documentation, Pinterest and Dropbox API
   docs. Record every URL used in `00_Brief/01_sources.md`.
2. Export and classify the to-dos before writing prompts, so categories come
   from the data rather than guesses.
3. Build from the bottom up: folders, then frameworks, then prompts, then
   agents, then routines, then generated to-do prompts.
4. Verify scripts run (dry-run), verify generated files open, commit on the
   designated branch, push, open a draft PR.
5. Stop short of actions that spend money or touch live accounts (activating
   scheduled tasks, writing to Dropbox, posting content). Prepare them fully
   and leave the switch to the owner.

## 5. Output rules

- Markdown, plain language, one idea per sentence.
- Every prompt file carries: title, purpose, when to use, inputs, the prompt
  itself in a fenced block, expected output, source or attribution.
- Every agent file carries the same fields plus triggers, tools and guardrails.
- Never invent URLs. Never store secrets in files; use environment variables.
