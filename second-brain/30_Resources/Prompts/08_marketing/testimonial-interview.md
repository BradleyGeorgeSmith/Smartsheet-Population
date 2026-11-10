# Testimonial Interview Planner and Rehearsal

**Purpose**: prepare customer testimonial shoots and rehearse likely answers,
the idea behind Brad's "dummy run of a testimonial with AI voice" app.
**When**: before every testimonial shoot (Steve Cartwright, James Williamson,
Attika, Paul Burnside and similar).
**Inputs**: `{{customer}}`, `{{product}}`, `{{what_we_know}}`, `{{goal_of_video}}`.

```text
Customer: {{customer}}
Product they use: {{product}}
What we know about them: {{what_we_know}}
Goal of the video: {{goal_of_video}}

Part 1. Question set: 12 open questions in the order I should ask them,
grouped as Before (their problem), During (choosing and using the product),
After (results, numbers, feelings), Advice (what they would tell a peer).
Each question under 15 words, conversational, no yes/no questions.

Part 2. Rehearsal: for each question, write a plausible 2 to 3 sentence
answer in the customer's likely voice based only on what we know. Mark each
as [rehearsal, not real].

Part 3. Shot list: 8 B-roll shots that would illustrate the likely answers.

Part 4. Soundbite targets: 5 phrases we hope to hear, to listen for in the
edit.

Part 5. Versions: how the final piece cuts to extra long, long, short,
social short, vertical, with target durations.
Markdown.
```

**Output**: `10_Projects/<customer>-testimonial/plan.md`.
**Source**: original.
