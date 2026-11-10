# Master Life Prompt Builder

**Purpose**: build the long "master prompt" Brad has asked for repeatedly: a
standing context document that any AI (Claude, ChatGPT, Gemini, Manus,
OpenClaw) reads first so every conversation starts informed. Serves "create
me a master prompt for my life", "master prompt for my role", "20 pages for
a master prompt", "Whisper Flow to answer the master prompt questions".
**When**: build once via dictated interview, revise quarterly.
**Inputs**: dictated answers to the interview below.

Step 1, the interview (dictate answers with Whisper Flow, 30 to 60 minutes):

```text
Ask me these in order, one at a time, waiting for my answer, probing once
if an answer is thin:
1. Who am I in one paragraph: roles at work, at home, in my fellowship.
2. What I am recovering from and what full recovery looks like to me.
3. My 2026 to 2030 goals, in my words.
4. My values and non-negotiables.
5. My work: what Hydralada expects of me, what I am best at, what drains me.
6. My ventures: NEXUS, mindfulmomentum.tech, Toop Street, Morley Studio,
   Substack, music. For each: status, next milestone.
7. My people: who I rely on, who relies on me, who I owe.
8. My tools: every app I pay for and what it is for.
9. My routines: morning, work day, evening, Sunday.
10. My health plan as my doctors have set it (no advice, just the plan).
11. How I like AI to talk to me: tone, length, formatting, what annoys me.
12. What I never want an AI to do on my behalf.
```

Step 2, the build:

```text
From the interview transcript below, write my Master Prompt as a Markdown
document with these sections: Identity, Mission and Values, Current
Projects (table: name, outcome, next milestone, PARA path), Areas (table),
People, Tools and where things live, Routines, Health plan summary (facts
only), Communication preferences, Hard limits, Twelve favourite problems,
How to update this document.
Target 2,500 to 4,000 words. First person. Quote me where my words are
strong. Mark gaps as [ADD]. End with a 300-word "short version" I can paste
into any chat.
<transcript>
{{transcript}}
</transcript>
```

**Output**: `00_Brief/02_master-life-prompt.md` (private) and the 300-word
short version pinned in Claude Projects, ChatGPT custom instructions and
Notion.
**Source**: original.
