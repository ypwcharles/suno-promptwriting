# Prompt Style templates (from `suno.md`)

Use these templates to create **metadata-like** Prompt Style text that is unlikely to be sung.

## Format A (Colon + Quotes) — recommended default

```text
genre: "<primary genre>, <secondary>, <era>, <reference vibe>."
vocal: "<timbre>, <delivery>, <technique>, <comparison anchor>."
instrumentation: "<top instruments in order>, <how played>."
production: "<recording setup>, <space>, <mixing>, <stereo image>."
mastering: "<hi-fi/lo-fi>, <dynamics>, <tone>, <clarity>."
mood: "<emotional space>, <imagery discipline>."
```

## Format B (MAX Mode stack) — acoustic-focused only

Use only when the genre benefits (acoustic/country/folk/singer-songwriter/orchestral). `suno.md` notes minimal improvement for purely electronic genres.

```text
[Is_MAX_MODE: MAX](MAX)
[QUALITY: MAX](MAX)
[REALISM: MAX](MAX)
[REAL_INSTRUMENTS: MAX](MAX)
[START_ON: TRUE]
[START_ON: "write out the first few words of lyrics here"]

genre: "<...>."
instruments: "<...>."
style tags: "<...>."
```

## Format C (Producer run-on) — dense & un-singable

```text
<genre fusion> with <core instruments> and <recording/production descriptors> and <mastering targets> and <constraints>.
```

## Electronic / Trap / Hip-Hop beats: anti-saw injection

See: `../rules/anti-sawtooth-electronic.md`
