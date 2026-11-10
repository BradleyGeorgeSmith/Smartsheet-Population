# Progressive Summarisation

Source: Tiago Forte,
https://fortelabs.com/blog/progressive-summarization-a-practical-technique-for-designing-discoverable-notes/
Paraphrased.

## Layers

| Layer | What you do | How much survives |
|---|---|---|
| 0 | The original source (article, video, PDF, transcript) | 100 percent |
| 1 | Capture: paste or clip the parts that resonate | Roughly 10 to 20 percent of the source |
| 2 | Bold the key phrases and sentences that carry the idea | A fraction of layer 1 |
| 3 | Highlight only the best of the bold, the truly unique or valuable | A fraction of layer 2 |
| 4 | Write a two to four sentence executive summary at the top, in your own words | A small number of notes only |
| 5 | Remix: turn the note into something new (post, slide, sketch, video) | A tiny minority |

Forte gives no fixed percentages. The rule is that each layer is a stricter
subset of the one before, and earlier layers stay intact so you can always
go back for context.

## Rules of thumb

1. Summarise opportunistically. Add a layer only when you are already in the
   note for a real reason. Never batch-summarise everything.
2. Design for Future You, who is impatient and sceptical. The note must prove
   its value in the first glance (discoverability) and still hold enough
   context to be useful (understanding).
3. Compress carefully. Over-compressed notes lose meaning. Over-detailed notes
   cannot be scanned.
4. Keep the layers visible. Bold and highlight are formatting, not deletion.
5. Layer 4 is rare. If you are writing executive summaries on most notes, you
   are capturing too much.

## How the Distil agent applies this

The Distil agent (`agents/03-distil-agent.md`) runs layers 2 to 4 on demand
using the prompt in `30_Resources/Prompts/03_distil/progressive-summary.md`,
and never on more than ten notes in one pass.
