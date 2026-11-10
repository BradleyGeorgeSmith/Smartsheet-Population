# YouTube Playlist or History to Curriculum

**Purpose**: turn a list of saved videos (watch later, history, pinned tabs)
into an ordered learning path with a note template for each. Serves "find
pinned tabs with important YouTube videos", "rewatch videos that improve
productivity", "Dan Martell and Huberman".
**When**: monthly, or when a playlist exceeds 30 items.
**Inputs**: `{{video_list}}` (title | channel | url | duration).

```text
Here is a list of videos I have saved:
<videos>
{{video_list}}
</videos>

1. Group them into 4 to 8 learning tracks (for example: AI agents and
   automation, video editing craft, health and memory, business and sales,
   faith and character, design). Name each track.
2. Inside each track, order the videos from foundation to advanced and
   remove near-duplicates (say which were removed and why).
3. For each track write: the outcome I should be able to do afterwards, the
   total watch time, and the single best video to start with.
4. Suggest a weekly plan: which track on which day, 30 minutes a day.
5. Give me a note template for watching: Title, Source, One-sentence
   summary, Three ideas, One action, Quote, PARA home.
6. Mark any video that is pure entertainment or outdated as SKIP.

Markdown. Do not describe video content you cannot see; work from titles
and channels only and say so.
```

**Output**: `30_Resources/Learning/curriculum.md`; run Fabric
`extract_wisdom` on each video as you watch.
**Source**: original.
