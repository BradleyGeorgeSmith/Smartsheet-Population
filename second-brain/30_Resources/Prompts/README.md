# Prompt Library

Every prompt here follows one shape: purpose, when to use, inputs, the prompt
in a fenced block, expected output, source. Copy the fenced block into Claude
(Code, Cowork, claude.ai), ChatGPT, Gemini or Fabric. Variables are written
`{{like_this}}`.

## Folders

| Folder | Stage | What is inside |
|---|---|---|
| `01_capture/` | CODE: Capture | Quick capture, voice-note to task, resonance filter, twelve favourite problems |
| `02_organise/` | CODE: Organise | PARA router, bulk file sorter, bookmark and tab-group classifier, folder-tree designer |
| `03_distil/` | CODE: Distil | Progressive summary, extract wisdom (Fabric), insight extraction, pattern finder |
| `04_express/` | CODE: Express | Intermediate packets, Substack post, LinkedIn post, brief writer, quote card copy |
| `05_agents/` | Operating agents | Agent system prompt template, master life prompt builder, prompt improver (Fabric), delegation brief |
| `06_journaling/` | Second brain journaling | Morning pages, evening shutdown, weekly reflection, gratitude and short accounts, impression capture from Remarkable |
| `07_learning/` | Knowledge and self-improvement | Feynman explainer, spaced-repetition cards (Fabric), reading plan (Fabric), video to notes, habit design |
| `08_marketing/` | Marketing capture and production | Swipe-file capture, campaign brief, brand voice extraction, testimonial interview, Hormozi offer (Fabric) |
| `09_visual-inspiration/` | Pinterest, architecture, manufacturing | Pin board audit, image tagging, mood-board brief, Pinterest to Dropbox run prompt |
| `10_quotes-inspiration/` | Quotes and imagery | Quote curator (architecture, manufacturing, innovation), quote card generator, aphorisms (Fabric) |
| `fabric-patterns/` | Verbatim MIT copies | 22 patterns from Daniel Miessler's Fabric, licence included |

## Sources and licences

- **Fabric** by Daniel Miessler, https://github.com/danielmiessler/fabric,
  MIT licence. Files in `fabric-patterns/` are verbatim `system.md` files.
- **Anthropic prompt engineering guidance**,
  https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices
  and the prompt library at https://platform.claude.com/docs/en/prompt-library/library.
  Techniques applied, text not copied.
- **Tiago Forte / Forte Labs**: PARA, CODE, Progressive Summarisation, Weekly
  Review. Paraphrased in `../Frameworks/`. Copyrighted, not copied.
- **awesome-chatgpt-prompts** (CC0), https://github.com/f/awesome-chatgpt-prompts,
  for persona phrasing ideas.
- Everything else in this library is original, written for this system.

## Conventions

- Prompts ask for Markdown output so results can be filed straight into PARA.
- Prompts never ask the model to invent URLs, prices or quotes. Where facts are
  needed they ask for a source or say "unknown".
- Health, finance and spiritual prompts are for reflection and organisation,
  not for medical, legal or financial advice.
