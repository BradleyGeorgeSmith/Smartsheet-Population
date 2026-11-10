# Marketing Brief (campaign, video or asset)

**Purpose**: a one-page brief for any Hydralada or personal-brand asset so
work starts from a clear target, not a blank timeline.
**When**: before any video edit, brochure, email blast or social campaign.
**Inputs**: `{{asset}}`, `{{audience}}`, `{{goal}}`, `{{inputs_available}}`,
`{{brand_rules}}` (link to BRANDING folder), `{{deadline}}`.

```text
Write a one-page creative brief in Markdown.

Asset: {{asset}}
Audience: {{audience}}
Business goal: {{goal}}
Inputs I already have: {{inputs_available}}
Brand rules: {{brand_rules}}
Deadline: {{deadline}}

Sections, each 1 to 4 lines:
1. Objective (one sentence, measurable)
2. Audience and the one thing they must feel or know afterwards
3. Key message (one sentence) and three supporting proof points
4. Mandatory elements (logo, slant angle, colours, legal lines, CTA)
5. Format and specs (dimensions, duration, versions: extra long, long,
   short, social short, vertical)
6. Tone (three adjectives, three words to avoid)
7. Reference examples (from my inputs only)
8. Production steps with owner and date
9. Distribution plan (HubSpot, socials, YouTube, DAM, NAS) and approver
10. Done means: the acceptance checklist

Where I gave no information, write [DECIDE] rather than guessing.
```

**Output**: `10_Projects/<campaign>/brief.md`.
**Source**: original; version list reflects Brad's note that each video
project needs extra long, long, short, social short and vertical cuts.
