---
name: suno-promptwriting
description: Use when a user wants help with Suno song generation or Suno quality-upgrade workflows: Prompt Style, Exclude Styles, lyrics, section meta tags, personas, model/parameter suggestions, Cover-based remastering, or “make this existing song sound better.” Trigger on requests to write Suno prompts, fix lyric bleed, reduce pop-gravity drift, structure sections, pick tags, tune settings, remaster via Cover, or improve consistency/pro quality.
---

# Suno Promptwriting

## Overview

Generate copy/paste-ready Suno inputs (Prompt Style + Exclude Styles + Lyrics) using the exact structures and rules in the bundled [`references/suno.md`](./references/suno.md) guide.

**Source of truth:** If any other advice conflicts with this skill, follow the bundled [`references/suno.md`](./references/suno.md). If the user explicitly provides a different project-specific `suno.md`, treat that as an override for that task.

## Task Modes

Choose the task mode before doing anything else:
- `initial`: new-song generation, lyrics-first generation, prompt writing, drift correction, tag selection, persona design
- `cover_remaster`: existing-song quality upgrade, Cover-based remastering, “make this song sound cleaner/better/more professional”

If the user is asking to improve an existing Suno song or audio result, default to `cover_remaster`.
Otherwise default to `initial`.

## Quick Start (copy/paste deliverable)

Deliver at most 1-5 small blocks, based on task mode. Do not dump long tag lists.

For `initial`:
- Prompt Style (Format A/B/C; must fit the user’s field limit, default target <= 1000 chars)
- Exclude Styles
- Lyrics (start with `///*****///` + section meta tags)
- Optional: Settings (Weirdness/Style Influence/Audio Influence), Persona

For `cover_remaster`:
- Cover Prompt (minimal)
- Settings (Weirdness / Style Influence / Audio Influence)
- Optional: Exclude Styles, Persona

## Quick Reference

| Need | Use |
|---|---|
| Browse all references | `references/index.md` |
| Pick a few tags (no overload) | `references/libraries/tag-index-curated.md` |
| Look up tags by keyword | `python3 scripts/suno_tag_lookup.py -q <keyword>` |
| Prompt Style templates | `references/templates/prompt-style-templates.md` |
| Lyrics templates | `references/templates/lyrics-templates.md` |
| Anti-saw electronic logic | `references/rules/anti-sawtooth-electronic.md` |
| Cover remaster template | `references/templates/cover-remaster-template.md` |
| Model selection notes | `references/rules/model-selection.md` |
| Persona stack | `references/rules/persona-stack.md` |
| Parameter cheat sheet | `references/rules/parameters-cheatsheet.md` |
| Keep a generation log | `references/templates/session-notes-template.md` |
| Formatter script (YAML → blocks) | `python3 scripts/suno_prompt_builder.py --config <file.yaml>` |

## Workflow (Strict)

### 1) Detect task mode, then collect inputs (ask only what’s missing)

First decide whether this is `initial` or `cover_remaster`.

For `initial`, minimum:
- Target genre + era references (2–6 tags)
- Target model (V4.5 / V4.5+ / V5)
- Emotional space (intimate/anthemic/nostalgic/raw/etc.)
- Vocal intent (male/female/duet/none) + delivery notes
- Song structure (Verse/Chorus/Bridge, etc.)
- Lyrics language + theme/story constraint

For `cover_remaster`, minimum:
- Original genre or strongest genre anchors
- Whether the goal is fidelity/cleanup vs intentional stylistic drift
- Whether the user wants strict adherence to the original audio
- Any explicit no-go items for Exclude Styles

Power controls (optional but recommended when the user cares about repeatability):
- Exclude Styles list (for “no X” constraints; prefer Exclude over negation)
- Persona (4-layer dossier; see reference)
- START_ON / DUET_START_ON (skip intro / control duet starts)
- Weirdness / Style Influence (if the user wants tuning knobs)
- Realism stack vocabulary (for acoustic realism)

**Model selection (from `suno.md`):**
- If the user wants release-ready polish / cleanest audio: prefer **V5**, but warn it “insists on adding weird intro vocals” and may require more iteration; START_ON might not fully suppress intros.
- If the user wants controlled chaos / surprises / unstable creativity: prefer **V4.5+**.
- If the user wants a reliable workhorse with solid prompt following (esp. heavy/long-form): prefer **V4.5**.

Reference: `references/rules/model-selection.md`

### 2) Choose a prompt format (A/B/C)

Use the guide’s three proven styles:
- **Format A (Colon + Quotes)**: default for clarity and reliable parsing
- **Format B (MAX Mode Stack)**: use when genre benefits (acoustic/country/folk/singer-songwriter/orchestral)
- **Format C (Producer run-on)**: fastest, but keep it metadata-like and un-singable

**Hard exclusion:** NEVER use **Format B (MAX Mode)** for Electronic / EDM / Trap / Hip-Hop beats / Synthwave. `suno.md` notes MAX Mode shows minimal improvement there.

### 2.5) Counter genre gravity (when prompts drift)

If the user complains about drift (especially “too pop”, “trap keeps appearing”, “cinematic keeps creeping in”), apply `suno.md`’s countermeasures:
- Prefer **Exclude Styles** over negation language
- Reinforce weak tags with extra context
- Use weird pairings or strategic contrast when needed

Reference: `references/rules/genre-gravity.md`

### 3) Write Prompt Style (obey formatting rules)

Hard rules from the guide:
- Don’t use simple comma-separated lists as the whole prompt.
- Use **structure** (headers/lines), and prefer **periods** to separate conceptual units.
- Treat commas as “optional”; for required elements, connect them with `and` / `with`.
- Avoid lyric-bleed triggers: poetic short lines, stage-direction brackets, ALL CAPS slogans, “singable” quoted phrases.
- Keep Prompt Style **metadata-like**; dense technical phrasing is safer.

### 3.5) Enforce Prompt Style character limits (hard constraint; common: 1000 chars)

Many Suno UIs enforce a hard character limit for the **Prompt Style** field (often **1000 characters**, including newlines). Treat this as a **hard constraint** for *all* prompt formats (**Format A/B/C**, and any MAX Mode lines if used).

Rules:
- If the user states a limit, obey it.
- If the user doesn’t state a limit, **default to ≤ 1000 characters** to be safe.
- Count **everything** in the Prompt Style block (newlines, quotes, punctuation).
- Never return a Prompt Style block that exceeds the limit; compress or change format until it fits.

Compression order (when you’re over the limit):
1) Drop low-signal keys first: `mood`, `arrangement` (keep the essence in `production`), and any optional extras.
2) Shorten phrasing: remove adjectives, keep concrete nouns and engineer language.
3) Merge categories: fold `arrangement` → `production`, fold `instrumentation` details into fewer phrases.
4) If still long, switch to a **compact prompt format** (below).

Compact Format A template (safe default under 1000 chars):
```text
genre: "<anchors, era, harmony>"
tempo: "<BPM, meter, pocket>"
vocal: "<gender, tone, delivery, 1–2 constraints>"
instrumentation: "<drums, bass, keys, guitar, 1 optional>"
production: "<hi-fi, warmth, reverb, stereo, mastering, no-go>"
```

Compact Format C template (one paragraph, still metadata-like):
```text
Mandarin R&B/neo-soul at <BPM> in a relaxed pocket with <core instruments> and <2–3 production cues>. <vocal constraint>. Exclude: <1–3 no-go>.
```

MAX Mode note:
- MAX Mode lines consume characters quickly. If you’re near the limit, prefer Format A or C instead of MAX Mode.

Optional verification (terminal):
```bash
python3 - <<'PY'
text = """<paste Prompt Style block here>"""
print(len(text))
PY
```

**Electronic / Trap / Hip-Hop beats special case (from `suno.md` Chapter 14):**
- Don’t overuse “realism” tags; they do little for purely electronic aesthetics.
- To avoid generic sawtooth synth wash, inject anti-saw synthesis constraints: FM / wavetable / formant / granular / spectral; describe motion (LFO/modulation), harmonic shaping (rounded profile, odd-harmonic emphasis), and limit stereo width / keep mono-stable low end.

Reference: `references/rules/anti-sawtooth-electronic.md`

Templates: `references/templates/prompt-style-templates.md`

**Realism stack (when you need acoustic authenticity):** use engineer language (not “realistic”).  
Reference: `references/rules/realism-vocabulary.md`

### 4) Exclude Styles (prefer Exclude over negation)

When the user says “no X”, convert it into an **Exclude Styles** list instead of relying on “no …” inside the style prompt.

Examples from the guide:
- Only female voices → Exclude: `Male Vocal`
- Rap without singing → Exclude: `Singing`, `Melodic Vocals`
- “Acoustic only” → Exclude: `Electronic`, `Synthesizer`, `Drum Machine`
- “Pure rock” → Exclude: `Electronic`, `Hip Hop`, `Pop`

Output Exclude Styles as a plain list the user can paste into the Exclude field:
```text
Male Vocal
Pop
Electronic
```

### 5) Write Lyrics (formatting + meta tags)

**Always put something in the lyrics box** (empty lyrics encourages prompt text to get sung).

At the very top of Lyrics, place the guide’s divider:
```text
///*****///
```

**Section formatting rules (from the guide):**
- Use bracketed section headers; separate sections with blank lines.
- Use parentheses for background vocals: `(fading away...)`, `(RISE UP NOW!)`.
- Use capitalization to imply vocal intensity (ALL CAPS = loud/forceful; sentence case = calm).

**Meta tags (guide Part Five):**
- Put meta tags in the **lyrics field**, at the beginning of each section.
- Use `|` pipes to stack detail.

Essential structure tags (use as needed): `[Intro]`, `[Verse]`, `[Chorus]`, `[Pre-Chorus]`, `[Bridge]`, `[Build]`, `[Drop]`, `[Breakdown]`, `[Outro]`.

Template: `references/templates/lyrics-templates.md`

**Lyric-writing discipline (guide Part Eight):**
- Plan first: pick genre, emotional space, and constraints.
- Avoid “AI soup”: keep a coherent storyline and use the **one metaphor rule**.
- Keep lines singable (breath); target roughly **6–10 syllables per line**, consistent within a section.

### 6) Add START_ON / DUET_START_ON only when needed

To skip an intro and start immediately on lyrics:
```text
[START_ON: TRUE]
[START_ON: "type the first few words of your lyrics here"]
```

For duets, use the guide’s duet controls (note: not guaranteed; genre-dependent):
```text
[DUET_START_ON: TRUE]
[MALE_START_ON: "type first few words of lyrics to start on"]
[FEMALE_START_ON: "type first few words of lyrics to start on"]
```

## Personas (when you want consistent vocals)

Use the 4-layer persona stack (dossier, not a label).  
Reference + template: `references/rules/persona-stack.md`

## Parameter Suggestions (when asked)

Use `suno.md` ranges for:
- Weirdness
- Style Influence
- Vocal Gender

Reference: `references/rules/parameters-cheatsheet.md`

## Quality Upgrade Modes (existing song)

If the user already has a song and wants “better quality”:

### Remaster (metadata tags)

Use a small stack of fidelity tags in **Displayed Lyrics** before hitting Remaster.
Reference: `references/libraries/remaster-tags.md`

### Cover-based remastering (preferred)

For quality improvement, `suno.md` recommends using **Cover** instead of Remaster.

Rules:
- Keep the prompt **minimal**: genre + high fidelity recording + professional mastering.
- Avoid extra style descriptors unless you want drift.

Minimal Cover prompt template (from `suno.md`):
```text
Genre: <original genre> with high fidelity recording and professional mastering.
```

If you need parameter guidance (from `suno.md`’s Cover workflow examples):
- Weirdness: 0
- Style Influence: 100
- Audio Influence: 100

Template: `references/templates/cover-remaster-template.md`

## Output Format (what to deliver to the user)

Return only the blocks that match the task mode.

For `initial`, return:
- **Prompt Style** (Format A/B/C, **must fit the user’s field limit; default target <= 1000 chars**)
- **Exclude Styles**
- **Lyrics** (with `///*****///` divider + meta tags)

Optionally add:
- **Settings** (Weirdness / Style Influence / Audio Influence)
- **Persona** (4-layer dossier) if the user wants consistent vocals

For `cover_remaster`, return:
- **Cover Prompt (minimal)**
- **Settings** (Weirdness / Style Influence / Audio Influence)

Optionally add:
- **Exclude Styles** if the user gives “no X” constraints
- **Persona** only if vocal identity control is explicitly useful

Do not force a Lyrics block for `cover_remaster`. The deliverable should stay minimal unless the user explicitly asks for extra structure.

## Quality Gate (fail if any of these are true)

For `initial`, fail if any of these are true:
- Prompt Style is a single comma-separated list (no structure).
- Prompt Style includes short poetic lines, singable quoted phrases, or bracket “stage directions” (lyric bleed risk).
- Prompt Style exceeds the user’s stated character limit (common: **1000 chars**, including newlines).
- Lyrics field is empty or missing `///*****///` divider.
- Meta tags are scattered inside Prompt Style instead of placed at the start of lyric sections.
- Sections aren’t separated by blank lines.
- User asked “no X” but Exclude Styles wasn’t provided.

For `cover_remaster`, fail if any of these are true:
- The output does not include a **Cover Prompt** block.
- The Cover prompt is overloaded with stylistic detail instead of staying minimal.
- Settings are missing when the user asks for parameter guidance or wants strict adherence.
- User asked “no X” but Exclude Styles wasn’t provided.

## Resources (examples)

- Initial generation: `references/examples/example_full_config.yaml`
- MAX Mode (acoustic-only): `references/examples/example_max_mode_config.yaml`
- Duet START_ON: `references/examples/example_duet_config.yaml`
- Cover remaster: `references/examples/example_cover_remaster_config.yaml`

## Common Mistakes (from baseline behavior)

| Mistake | Fix |
|---|---|
| “I’ll write a poetic style prompt” | Keep Prompt Style metadata-like; move poetry into Lyrics. |
| “My Prompt Style is over the character limit” | Apply Step 3.5 compression order; use Compact Format A if needed. |
| “I used ‘no pop’ inside the prompt” | Put unwanted elements in **Exclude Styles** instead. |
| “I left Lyrics empty to let Suno write them” | Always put something in Lyrics; start with `///*****///`. |
| “I sprinkled meta tags in the style prompt” | Meta tags go at the start of each lyric section. |
| “I used commas everywhere” | Use periods to separate units; inside quoted fields, commas are OK. |
| “I want better quality, so I wrote a huge Cover prompt” | For `cover_remaster`, keep the Cover prompt minimal and use settings for adherence. |

## Red Flags (STOP and fix before generating)

- Prompt Style looks like lyrics (short lines, rhyming, slogans, quotes).
- Lyrics missing divider or section breaks.
- “No X” constraints not translated into Exclude Styles.
- Meta tags not placed at section starts.

## Tag Selection (avoid overload)

When the user asks “give me tags /风格参考/有哪些标签”:

1) Pick **1–2 genre anchors** + **2–4 production/mastering descriptors** + **1–3 vocal/instrument constraints**. Avoid long lists.
2) Put global sound in **Prompt Style** (Format A/B/C).
3) Put section-specific behavior in **Lyrics meta tags** (`[Chorus | ...]`).
4) Use references for lookup, but only output a small coherent set:
   - `references/libraries/tag-index-curated.md`
   - Full index is inside `references/suno.md` at `## Index`.

Quick lookup from terminal:
```bash
python3 scripts/suno_tag_lookup.py -q reverb
python3 scripts/suno_tag_lookup.py -q "high" -q "fidelity"
```
