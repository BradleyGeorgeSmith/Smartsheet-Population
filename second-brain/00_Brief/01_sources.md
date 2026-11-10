# Sources used to build this system

Research was done on 2026-11-10. Where a source is copyrighted it is linked
and paraphrased, not copied. Where a source is openly licensed, the licence
is stated and the text is included verbatim.

## Frameworks (paraphrased)

- Tiago Forte, "The PARA Method", https://fortelabs.com/blog/para/
- Tiago Forte, "Progressive Summarization: A Practical Technique for Designing Discoverable Notes", https://fortelabs.com/blog/progressive-summarization-a-practical-technique-for-designing-discoverable-notes/
- Tiago Forte, "The Weekly Review is an Operating System", https://fortelabs.com/blog/the-weekly-review-is-an-operating-system/
- Tiago Forte, *Building a Second Brain* (2022) and *The PARA Method* (2023), for CODE, Intermediate Packets and the twelve favourite problems (via Richard Feynman).
- James Clear, *Atomic Habits* (2018): the four laws and habit stacking, paraphrased in the habit-design prompt.
- Hal Elrod, *The Miracle Morning*: gratitude and intention in the morning page.

## Prompts (verbatim, licensed)

- Daniel Miessler, Fabric, https://github.com/danielmiessler/fabric, MIT licence.
  Copied patterns: analyze_claims, create_5_sentence_summary (as create_summary),
  create_aphorisms, create_flash_cards, create_hormozi_offer, create_idea_compass,
  create_micro_summary, create_quiz, create_reading_plan, create_tags,
  extract_article_wisdom, extract_business_ideas, extract_ideas, extract_insights,
  extract_main_idea, extract_patterns, extract_recommendations, extract_wisdom,
  improve_prompt, rate_content, summarize, write_essay. Licence text is in
  `30_Resources/Prompts/fabric-patterns/LICENSE-fabric-MIT.txt`.
- awesome-chatgpt-prompts, https://github.com/f/awesome-chatgpt-prompts, CC0.
  Consulted for persona phrasing; no text copied.

## Prompting guidance (techniques applied)

- Anthropic, "Prompting best practices", https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices
- Anthropic prompt library, https://platform.claude.com/docs/en/prompt-library/library

## Scheduling and agents (product documentation)

- Claude Code, "Run prompts on a schedule" (`/loop`, CronCreate, loop.md), https://code.claude.com/docs/en/scheduled-tasks
- Claude Code, "Automate work with scheduled tasks" (cloud routines, `/schedule`, limits), https://code.claude.com/docs/en/routines

## APIs

- Pinterest API v5, https://developers.pinterest.com/docs/api/v5/ (boards and pins listing, OAuth scopes `boards:read`, `pins:read`)
- Dropbox API v2, https://www.dropbox.com/developers/documentation/http/documentation (files/upload, files/get_metadata, create_folder_batch, Dropbox-API-Path-Root header for team spaces)
- ZenQuotes, https://zenquotes.io (free tier needs attribution link); Quotable, https://github.com/lukePeavey/quotable (open source)

## Second-brain agent projects reviewed for ideas (none copied)

- Rowboat (Markdown and Obsidian knowledge graph), COG second brain (huytieu, MIT), Personal Operating System (ztnkv), Minimal Second Brain (gokhanarkan), Meowary (retran), agent-second-brain (smixs). Found via web search; used only to confirm that a Markdown-first, agent-maintained vault is the common pattern.

## Brad's own material

- Todoist export (2,500 or so open tasks across 155 projects), read through the Todoist connector on 2026-11-10.
- Dropbox listing of `/Brad Smith` and `/Hydralada Marketing` (folder names only).
- Existing repository content: `cards/` and `album02/` quote cards.
