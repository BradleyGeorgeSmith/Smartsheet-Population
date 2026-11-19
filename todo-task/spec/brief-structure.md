# The ToDo Task Brief: structure and rules

One brief is written for every To Do entry. The brief is the yellow section of the Word
document, and it is also the prompt that is pasted into a new Claude Code session. It has
to work on its own, with nothing else attached.

## The six parts, in order

| # | Part | What it holds | Rules |
|---|------|---------------|-------|
| 1 | **Working rules for Claude** | One fixed paragraph (`working-rules.txt`). | Never reworded. It is what makes the brief a usable prompt. |
| 2 | **Title** | `Verb the thing: scope`. | Starts with an action word. 120 characters at most. |
| 3 | **Description / Status / Calendar date** | One line holding all three. | Description names the outcome. Status usually starts "Waiting for". Calendar date is a real date or "Not supplied". |
| 4 | **[Topic] Context** | Two to four short paragraphs in the first person. | What I noticed or meant; why it matters to me; what is not yet known. |
| 5 | **Information Needed and Next Actions** | Numbered list, three to six items. | Item 1 starts "Next action:". The last item says what to produce from the information. |
| 6 | **Execution Plan for Claude** | Output; Steps; Tools, skills and apps; Rhythm; Done when. | Only tools that help. "No Claude session needed" is a valid plan. |

## Rules that never bend

1. **The original entry is never edited.** It stays at the top of the document, word for word.
2. **Stay with the motive.** Expand what was meant. Do not swap in a better-sounding idea.
3. **Invent nothing.** No made-up names, dates, numbers, results or quotes. Unknown things are
   written as "Not supplied" or listed under Information Needed.
4. **Mark guesses.** A best reading of an unclear phrase is followed by "(to confirm)".
5. **Simple outcomes.** A piece of writing, a plan, video ideas or learning notes.
6. **Health.** Organise information and questions for the clinician. No diagnosis, no treatment advice.
7. **Personal, family, money and faith topics.** Respectful, no judgement, keep to what was written.
8. **Evidence.** Every update ends with: Completed; Waiting on; Next action; Completion evidence.

## How deep to go

| Entry type | Examples | Brief | Claude session? |
|------------|----------|-------|-----------------|
| content, idea, learning, plan | a video idea, a question, a goal | Full brief | Yes |
| health, appointment | a symptom to raise, a booking | Full brief, clinician rule applies | Yes, to organise only |
| errand, purchase, person | buy, pay, call, reply | Short brief: one Context paragraph, two or three actions | Usually no |
| reflection | a feeling, a thought, a note to self that asks for nothing | Short brief that keeps the thought, tidied but not softened or answered | No |
| unclear | cannot be read with confidence | Short brief, first action is "Confirm what I meant by ..." | No, until clarified |

## To Do write-back

After the brief is written, the task in Microsoft To Do or Todoist is updated:

- **Title** becomes the brief title, shortened to 90 characters.
- **Description / note** becomes: description, status and next action (600 characters at most),
  followed by the original entry kept word for word under "Original entry:".

## The stages a task moves through

`Captured` → `Briefed` → `In session` → `Waiting on me` → `Done`

In Todoist these are labels: `briefed`, `in-session`, `waiting-on-me`, `content-done`.
A task with the label `skip-ai` is never expanded.
