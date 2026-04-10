# Suno Promptwriting

A self-contained Codex skill for writing Suno inputs across the full workflow:

- new-song generation
- prompt repair when results drift toward the wrong genre
- lyrics and section meta tags
- persona and parameter guidance
- Cover-based remastering for existing songs

The skill ships with its own `suno.md` reference guide, curated reference files, helper scripts, example configs, and smoke tests.

> [!NOTE]
> This repository is designed as a skill directory. The main entrypoint is [`SKILL.md`](./SKILL.md).

## What It Does

This skill treats Suno work as two task modes:

- `initial`: write Prompt Style, Exclude Styles, lyrics, and optional persona/settings for a new song
- `cover_remaster`: write a minimal Cover prompt and adherence-focused settings for improving an existing song

It is designed to avoid the common failure modes in Suno prompting:

- lyric bleed from overly poetic prompt text
- genre gravity toward generic pop or trap
- overlong tag dumps
- misuse of MAX mode for electronic genres
- bloated Cover prompts that drift away from the source song

## Repository Layout

```text
suno-promptwriting/
├── SKILL.md
├── README.md
├── suno.md
├── agents/
├── evals/
├── references/
├── scripts/
└── tests/
```

Key files:

- `SKILL.md`: skill behavior, task modes, output contract, quality gates
- `suno.md`: bundled source-of-truth guide for this skill
- `references/`: focused templates, rule summaries, curated tags, and examples
- `scripts/suno_prompt_builder.py`: formats YAML configs into copy/paste-ready Suno blocks
- `scripts/suno_tag_lookup.py`: searches the curated tag index
- `evals/evals.json`: regression prompts and expectations
- `tests/test_skill_smoke.py`: smoke tests for both task modes

## Install

Place this directory in your Codex skills path:

```bash
mkdir -p ~/.codex/skills
cp -R suno-promptwriting ~/.codex/skills/
```

If your environment reads skills from a different location, install it wherever your skill loader expects a standard skill directory with `SKILL.md` at the root.

## Usage

Ask for the skill in natural language or by name when you want Suno help.

Examples:

- “Use `suno-promptwriting` to write a Mandarin city pop prompt with lyrics.”
- “Fix this Suno prompt, it keeps drifting into pop-trap.”
- “Give me a Cover prompt to make this song cleaner without changing its identity.”

### Output Modes

For `initial`, the skill returns:

- `Prompt Style`
- `Exclude Styles`
- `Lyrics`
- optional `Settings` and `Persona`

For `cover_remaster`, the skill returns:

- `Cover Prompt (minimal)`
- `Settings`
- optional `Exclude Styles` and `Persona`

## Helper Scripts

Format an example config into final Suno blocks:

```bash
python3 scripts/suno_prompt_builder.py \
  --config references/examples/example_prompt_config.yaml
```

Generate a Cover/remaster output:

```bash
python3 scripts/suno_prompt_builder.py \
  --config references/examples/example_cover_remaster_config.yaml
```

Search curated tags:

```bash
python3 scripts/suno_tag_lookup.py -q pop
python3 scripts/suno_tag_lookup.py -q "high" -q "fidelity"
```

The helper scripts require Python 3 and `PyYAML`.

## Quality Checks

Run the smoke tests:

```bash
python3 -m unittest discover -s tests -p 'test_*.py'
```

Validate the eval definitions:

```bash
python3 -m json.tool evals/evals.json >/dev/null
```

The current tests check:

- `initial` outputs include `Prompt Style`, `Exclude Styles`, and `Lyrics`
- `cover_remaster` outputs include `Cover Prompt` and `Settings`, without forcing lyrics
- each eval case contains explicit expectations instead of prompt-only placeholders

## Included References

The bundled references are intentionally split so the skill can load only what it needs:

- model selection
- genre gravity countermeasures
- anti-saw electronic guidance
- persona stack guidance
- parameter cheat sheet
- prompt and lyric templates
- Cover/remaster templates
- curated tag library

Open [`references/index.md`](./references/index.md) for the reference map.
