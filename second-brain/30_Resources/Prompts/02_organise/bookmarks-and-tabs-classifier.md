# Bookmarks, Tabs and History Classifier

**Purpose**: turn a Chrome bookmark export, tab-group list or Google Takeout
search history into a PARA folder tree and a learning map. Directly serves
Brad's tasks about turning history and bookmarks into structure.
**When**: once for the initial clean-up, then monthly.
**Inputs**: `{{export}}` (bookmarks HTML converted to a list of "title | url",
or history as "date | query | url"). Chunk at about 300 lines per run.

```text
Here is a chunk of my browser bookmarks or search history:
<export>
{{export}}
</export>

Step 1. Cluster the lines into topics. Name each cluster in 2 to 4 words.
Step 2. Map each cluster to PARA: Project (name it), Area, Resource or Archive.
Step 3. For each cluster give: count of lines, the 3 most representative
        entries, and one sentence on what I was clearly trying to learn or do.
Step 4. Propose a bookmark folder tree, max two levels, using the PARA
        numbering 10_Projects, 20_Areas, 30_Resources, 40_Archives.
Step 5. List entries that are stale (dead tools, old versions, resolved
        questions) under "Archive candidates".
Step 6. List repeated searches that suggest an unanswered question. Phrase
        each as a question I could add to my twelve favourite problems.

Output Markdown. Do not visit the URLs. Do not invent entries.
```

**Output**: a cluster report plus a folder tree you can recreate in Chrome
and mirror in Dropbox.
**Source**: original.
