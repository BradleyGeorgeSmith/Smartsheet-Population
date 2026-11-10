# Feynman Explainer (learn anything fast)

**Purpose**: understand a tool, concept or term properly by explaining it
simply, finding gaps, and filling them. Serves "learn all apps thoroughly",
"what is a JSON file", "critical thinking", "learn Substance 3D".
**When**: any time you meet a term you only half know.
**Inputs**: `{{topic}}`, `{{why_i_need_it}}`, `{{what_i_think_i_know}}`.

```text
Topic: {{topic}}
Why I need it: {{why_i_need_it}}
What I think I already know: {{what_i_think_i_know}}

Teach me using the Feynman technique:
1. PLAIN EXPLANATION: explain it in under 150 words as if to a sharp
   14-year-old. No jargon unless you define it in the same sentence.
2. ONE PICTURE: describe a single diagram or analogy I could sketch on my
   Remarkable that captures it.
3. GAPS: compare my "what I think I know" with the truth. List what I had
   right, what I had wrong, what I was missing.
4. HANDS ON: one 10-minute exercise I can do today on my own machine or
   files to prove I understand it.
5. THREE QUESTIONS: questions I should now be able to answer. Give the
   answers under a "Reveal" heading.
6. NEXT: the one adjacent concept to learn next and why.

Markdown. Prefer concrete examples from marketing, video production, file
management or AI tools, because that is my world.
```

**Output**: file under `30_Resources/Learning/<topic>.md`; add the three
questions to a flash-card deck using Fabric `create_flash_cards`.
**Source**: Feynman technique (public domain idea); prompt original.
