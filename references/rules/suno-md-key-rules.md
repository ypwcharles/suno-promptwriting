# Suno Promptwriting — Key Rules (from `suno.md`)

This file is a compact, load-on-demand reference distilled from `suno.md`. When in doubt, re-open the source file and follow it strictly.

## Prompt Style: structured formats

### Format A (Colon + Quotes)
- Use clear categories (`genre`, `vocal`, `instrumentation`, `production`, `mood`, `mastering`).
- Keep descriptors inside quotes, comma-separated **inside the field**.
- Prefer ending conceptual units with **periods**.

### Format B (MAX Mode Stack)
- Use the exact bracket formatting shown in the guide.
- Works best for acoustic/country/folk/singer-songwriter/orchestral; minimal impact for purely electronic.

### Format C (Producer run-on)
- Dense, metadata-like, “un-singable” phrasing.
- Prefer `and` / `with` chaining over comma lists.

## Critical formatting rules

- Do not use simple comma-separated lists as the whole prompt.
- Prefer **periods** to separate conceptual units.
- Commas can signal “optional” / skippable ideas; use conjunctions (`and`, `with`) to make elements feel essential.

## Lyric bleed prevention

Prompt text can get sung if it looks singable. Common triggers:
- Short poetic lines in Prompt Style
- Brackets that look like stage directions
- ALL CAPS slogans / chants
- Quoted singable phrases
- Empty Lyrics box

Mitigation:
- Keep Prompt Style metadata-like and dense.
- Avoid quotes unless in structured fields.
- Always put something in Lyrics.

## Lyrics box divider technique

At the very top of Lyrics, add:
```text
///*****///
```

## START_ON / duet controls

- `START_ON` to skip intros and begin at your lyric start phrase.
- Duet controls exist but are not guaranteed; effectiveness is genre-dependent.

## Exclude Styles (preferred over negation)

Translate “no X” requirements into Exclude Styles entries instead of relying on negation language inside Prompt Style.

## Meta tags and section control

- Meta tags belong in **Lyrics**, at the beginning of each section.
- Use pipes to stack detail: `[Chorus | anthemic chorus | stacked harmonies | modern pop polish]`.

Essential structure tags:
- `[Intro]` `[Verse]` `[Chorus]` `[Pre-Chorus]` `[Bridge]` `[Build]` `[Drop]` `[Breakdown]` `[Outro]`

## Lyrics formatting (performance cues)

- Separate sections with blank lines.
- Use parentheses for background vocals: `(fading away...)`, `(RISE UP NOW!)`.
- Use capitalization to imply intensity (ALL CAPS = loud/intense; sentence case = calm/quiet).
- Extended vowels can work but often break pronunciation; use sparingly.

## Lyric-writing discipline

- Plan before writing: genre, emotional space, constraints.
- Keep a coherent storyline.
- One metaphor rule (don’t jump motifs every section).
- Rough target: 6–10 syllables per line; keep consistency within sections (±1–2).
