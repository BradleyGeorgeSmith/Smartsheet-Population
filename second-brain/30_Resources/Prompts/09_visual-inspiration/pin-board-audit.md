# Pinterest Board Audit and Tagging

**Purpose**: turn a Pinterest board export (from `scripts/pinterest_to_dropbox.py`
or a manual list) into a tagged, PARA-filed inspiration library covering
architecture, manufacturing, branding, interiors, vehicle graphics.
**When**: after each sync run.
**Inputs**: `{{pins}}` (one per line: board | pin title | description | link),
`{{purpose}}` (for example Toop Street alterations, Hydralada rebrand,
Morley Studio).

```text
Here are pins from my Pinterest boards:
<pins>
{{pins}}
</pins>
Purpose I am collecting for: {{purpose}}

1. Tag every pin with 3 to 6 tags from this controlled list, adding new tags
   only if nothing fits: architecture, interior, exterior, facade, timber,
   cedar, shiplap, concrete, steel, glass, landscape, slope, dam, houseboat,
   sauna, gym, studio, workshop, office, lighting, colour, typography, logo,
   brand_system, vehicle_graphic, industrial_design, manufacturing,
   machinery, factory, process, innovation, minimal, luxury, porsche_style,
   dashboard, ui, photography, mood.
2. Group pins into mood boards of 6 to 12 pins each. Name each board and
   write a two-sentence brief describing the shared idea and how it serves
   my purpose.
3. For each mood board, propose a Dropbox folder under
   30_Resources/Inspiration/<Architecture|Manufacturing|Branding|Innovation>/<board-name>/
4. List pins that are duplicates or off-purpose as ARCHIVE.
5. Write 5 design principles I can extract from the whole set, one line each.

Markdown. Work only from titles, descriptions and links; do not invent
visual details you cannot see.
```

**Output**: a tagging table and mood-board briefs filed next to the images.
**Source**: original.
