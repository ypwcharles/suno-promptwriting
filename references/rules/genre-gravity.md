# Genre Gravity + Countermeasures (from `suno.md`)

Suno blends co-occurring concepts (“genre clouds”). Many prompts drift toward defaults (especially **pop**) unless you actively constrain them.

## Major genre clouds (examples)

- **Rap cloud:** rap / trap / bass / hip hop / beat tend to blend.
- **Orchestral cloud:** orchestral / epic / cinematic / dramatic / piano cluster.
- **Indie cloud:** indie / pop / acoustic / dreamy / psychedelic cluster.
- **Dark electronic cloud:** dark / synth / electro / synthwave / futuristic cluster.

## Escaping genre gravity (3 strategies)

1) **Explicit exclusions**  
Carve out space by removing unwanted associations.

2) **Force weird combinations**  
Use rare pairings (“emo industrial”, “orchestral phonk”, “math rock gospel”) to push the model into less-default territory.

3) **Strategic contrast**  
Emphasize elements that repel what you’re trying to avoid (without naming the unwanted thing).

## The pop gravity well

Most genres gravitate toward pop mixing structures/hooks unless you counteract it.

Practical move: if the user says “less pop”, provide an **Exclude Styles** list that includes `Pop` (and other offenders), then reinforce the desired genre with specific instrumentation + production descriptors.

## Weak vs strong tags

Weak tags (often need reinforcement): `Grunge`, `Math rock`, `Swing`  
Strong tags (tend to dominate): `Pop`, `Rock`, `Electronic`

If combining weak + strong tags:
- Reinforce the weak tag with extra context (era, instrumentation, production, performance technique).
- Exclude the strong tag’s typical drift targets (often `Pop`).

