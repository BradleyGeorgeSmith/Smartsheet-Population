---
name: todo-task-brief
description: Expand the short To Do entry at the top of a ToDo Task Brief document into the full task brief. Use in Word when the open document has a section called 'Original To Do entry' and the lines 'TASK BRIEF STARTS' and 'TASK BRIEF ENDS', or when asked to expand a To Do entry into a brief.
---

# ToDo Task brief

The open Word document is a ToDo Task Brief. The person's raw To Do entry is under
"1 · Original To Do entry". Expand it into a full task brief inside the document, by
following every step below. The steps are written by the person, so "I" and "my" in them
mean the person.

1. Read the paragraph under "1 · Original To Do entry". It is my raw capture. It may be short, misspelt or hard to follow. Do not edit or delete it.

2. Rewrite everything between the lines "TASK BRIEF STARTS" and "TASK BRIEF ENDS" (the yellow section) so that it is about this entry. The text there now is only a model for structure, length and tone. Replace all of its content, and do not carry over its subject, its deliverables or its steps. Keep the paragraph that starts "Working rules for Claude:" word for word.

3. Keep these parts, in this order: a title that starts with an action word; one line with Description, Status and Calendar date (a real date, or exactly "Not supplied"); a heading made of a topic word and "Context" (as in "Video Context"), followed by two to four short paragraphs; "Information Needed and Next Actions" as a numbered list of three to six items, where item 1 starts with "Next action:" and the last item says what to produce; "Execution Plan for Claude" with Output, Steps, Tools, skills and apps, Rhythm, and Done when; and a last line "Original entry (word for word):" followed by my entry copied exactly, mistakes included.

4. Stay with the motive of my entry. Fix grammar and spelling and expand what I clearly meant. Do not invent facts, names, dates, numbers or results, or people, groups and places I did not mention. Do not state what I have or have not done, own or believe beyond what I wrote. Where something is unknown, write "Not supplied" or list it once under Information Needed. Status says what is true now.

5. Where the entry is unclear, give your best reading in a short sentence and put "(to confirm)" straight after it, every time that reading appears, including in the title and the write-back. A link you add between two of my sentences, such as "so" or "because", is also a guess. Do not draw conclusions from a guess.

6. Write the Context as me. "I" is always me: never write about "my entry", "this brief", your reading or your assumptions. Use short sentences. Do not add words about how I should behave or feel, such as respectful, proper or comfortable, and do not add cautions or limits I did not write.

7. If the entry holds several separate ideas, build the brief around the main one. If I did not make clear which is the main one, make item 1 "Next action: Confirm that [idea] is the main idea". List the other ideas in one item, as short quoted phrases to capture separately, with no commentary.

8. Rewrite the idea so that Claude Code can act on it. Name the outcome once in the Description after "Outcome:", and use the same words in the last item and in Output. It will usually be a piece of writing, a plan, video ideas or learning notes. Keep anything I asked for by name, such as a format or a tool. Put the steps Claude can do without me first; a step that waits on me starts "When I supply". List only the tools, skills and apps that help. Done when names things that can be shown, such as a file saved or a task added, and everything in it must appear in Output. If my entry names a quantity or a format, such as "as many as you can" or "in Excel", put it in Output, in a step that does not wait for me, and in Done when.

9. If the entry is a simple errand (buy, pay, book, call, reply), keep the brief short. The title and item 1 are the errand itself. Write one Context paragraph and two or three actions. The Execution Plan says "No Claude session needed", with "None" under Steps and under Tools, skills and apps. What I did not write down may be something I already know, so do not say that I am waiting on it.

10. If the entry cannot be read with confidence, keep the brief just as short. Item 1 is "Next action: Confirm what I meant by" followed by the unclear words, and the Execution Plan says "No Claude session needed until I confirm the reading". In every other case, item 1 is the first thing I really have to do or supply, not a request to confirm your reading. A reflection or a note to self that asks for nothing gets the same short brief: keep my thought as I wrote it, tidied but not softened or answered, with item 1 "Next action: Decide whether this needs anything done" and "No Claude session needed".

11. For health topics, organise information and questions for the clinician; do not diagnose or recommend treatment. Do not assume I have a clinician, and do not turn something I said I will do into a question of whether to do it.

12. Keep the brief about as long as the model: roughly 400 words after the Working rules paragraph. Ask me for at most three things.

13. Fill "4 · To Do write-back": a Title of at most 90 characters (the brief's title, shortened if needed) and a Description of at most 600 characters in plain text that repeats the brief's Description, Status and item 1 without changing what they say.

14. Keep the yellow highlight on the brief. Change nothing else in the document. When you finish, tell me in the chat only what you marked "(to confirm)" and what you need from me.

## The fixed first paragraph

The brief always begins with this paragraph, word for word. If it is missing or has been
changed, put it back exactly:

Working rules for Claude: Treat this brief as the complete instruction for this session. Stay with the motive of my original entry; do not swap it for a different idea. Work out which tools, skills, agents and loops are needed, then start on every step that does not depend on me. Keep the outcome simple and effective: a piece of writing, a plan, video ideas or learning notes. Do not contact anyone, post anything or spend money on my behalf unless this brief asks for it. If the plan says no Claude session is needed, confirm that and stop. Report what was actually done instead of claiming that an action was completed. End each update with: Completed; Waiting on; Next action; and Completion evidence. Retain relevant decisions and lessons in the brief so future work builds on existing context. For health-related tasks, organise information and questions for the clinician without diagnosing or recommending treatment.

## If something goes wrong

- If the document has no "TASK BRIEF STARTS" line, say so and stop. Do not write the brief
  anywhere else.
- If the entry under section 1 is still the placeholder in square brackets, ask for the
  entry and stop.
- If an edit times out, finish the brief first, then fill "4 · To Do write-back" as a
  second edit.
