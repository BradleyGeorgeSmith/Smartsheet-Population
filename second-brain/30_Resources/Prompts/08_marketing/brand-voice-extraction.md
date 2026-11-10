# Brand Voice Extraction

**Purpose**: derive a usable voice and tone guide from existing material so
every agent writes consistently. Pairs with the Hydralada BRANDING folder
and the Porsche-style rebrand idea.
**When**: once per brand, refresh yearly.
**Inputs**: `{{samples}}` (5 to 15 pieces of existing copy), `{{brand}}`,
`{{aspiration}}` (brands admired, for example Porsche for structure).

```text
Brand: {{brand}}
Brands I admire for structure and tone: {{aspiration}}
Existing copy samples:
<samples>
{{samples}}
</samples>

Produce a one-page voice guide in Markdown:
1. Voice in three adjectives, each with a sentence on what it means in
   practice and one quoted example from the samples.
2. Tone shifts: how the voice changes for a technical spec sheet, a social
   post, a customer email, a testimonial video script.
3. Vocabulary: 15 words and phrases we use; 10 we never use.
4. Sentence rhythm: typical length, use of questions, use of lists.
5. Proof habits: how we show evidence (numbers, named customers, demos).
6. Visual pairing notes: what the copy assumes about imagery (slant angle,
   colour, photography style), from the samples only.
7. Gap versus aspiration: three concrete changes that move us toward the
   admired brands without copying them.
8. A 60-word sample paragraph written in the recommended voice.
```

**Output**: `20_Areas/Hydralada-Marketing/voice-guide.md` (and one per
personal brand).
**Source**: original.
