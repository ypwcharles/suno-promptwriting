# Model selection notes (from `suno.md`)

Use this when the user asks “which model should I use” or you need to adapt the prompting strategy to model behavior.

## Quick guidance

- **V5**: cleanest audio + most natural vocals + sophisticated tone shifts, but **more demanding** and “insists on adding weird intro vocals”; expect more iteration for best results.
- **V4.5**: reliable workhorse; excellent prompt following and smart mash-ups; good for heavy genres and long-form compositions.
- **V4.5+**: more creative/volatile; can throw in random elements; good when you want surprises or experimental fusion.

## Practical implications for prompting

- If using **V5** and intros/intro vocals are unwanted, still try `START_ON`, but set expectations: you may need multiple generations or to post-process with Cover workflows.
- If doing **experimental fusion**, consider **V4.5+** and allow higher Weirdness.
- If doing **release polish**, prefer **V5** and tighten constraints (Exclude Styles + persona + structured prompt).

