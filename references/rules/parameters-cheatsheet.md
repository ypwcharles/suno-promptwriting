# Parameter Cheat Sheet (from `suno.md`)

Use these when the user asks for “more control”, “more faithful”, “more experimental”, “more consistent”, or you need repeatable results.

## Weirdness (0–100, default ~50)

Controls interpretive creativity vs faithful execution.

- **0–30**: safe/predictable; best for classic styles and fidelity (also covers/tributes).
- **40–60**: balanced creativity + control.
- **70–100**: experimental territory; more surprises.

Genre defaults suggested by `suno.md`:
- Classic (pop/rock/country): **30–50**
- Experimental (ambient/IDM/glitch): **60–80**
- Unusual fusions: **70–90**
- Covers/tributes: **10–30**

## Style Influence (0–100)

Controls how strictly Suno follows style tags.

- **0–30**: loose inspiration (max freedom)
- **40–60**: balanced
- **70–100**: strict adherence to tags

Tag-specific guidance from `suno.md`:
- **Vague tags** (e.g., “Pop”, “Rock”) → higher Style Influence **70–90**
- **Highly specific tags** → moderate Style Influence **40–60**
- **Want surprises** → low Style Influence **20–40**

## Vocal Gender (Male/Female)

If the user cares about vocal gender consistency, prefer setting the UI parameter (Male/Female) and support it with a persona.

## Audio Influence (0–100)

`suno.md` shows Cover workflows using **Audio Influence: 100** for maximum adherence to the original audio when doing quality-oriented transforms.
