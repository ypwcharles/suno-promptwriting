# Anti-sawtooth strategy for electronic genres (from `suno.md` Chapter 14)

Problem: Suno often defaults to a bright, buzzy, generic **sawtooth synth** in electronic tracks.

Key insight: you usually can’t fix it with “no saws”. Redirect the model with **specific synthesis + motion + harmonic + spatial constraints**.

## What to inject (Prompt Style)

### Replace “synth bass” with synthesis types
- FM synthesis bass
- Wavetable movement
- Formant-driven bass
- Granular textures
- Spectral morphing
- Resonant bandpass motion

### Describe motion (not size)
- Evolving modulation
- LFO-driven movement
- Dynamic harmonic motion
- Non-repeating bass cycles

### Shape harmonics directly
- Rounded harmonic profile
- Asymmetric waveforms
- Odd-harmonic emphasis
- Band-limited synthesis

### Use bass archetypes that avoid saws
- Reese bass movement
- Neuro bass texture
- Growl bass modulation
- Sub-driven bass design

### Control the top end
- Smooth top end
- Controlled high harmonics
- Anti-aliasing character
- Clean high frequency rolloff

### Kill the stereo width
- Center-focused bass
- Mono-stable low end
- Phase-coherent layers

## Example anti-saw prompt snippet (from `suno.md`)

```text
FM and wavetable bass design, evolving modulation, non-repeating harmonic motion, rounded harmonic profile, controlled high end, phase-coherent low end, clean punch.
```

## “Realism” reminder

`suno.md` notes REALISM/REAL_INSTRUMENTS style constraints have minimal effect on purely electronic genres; focus effort on synthesis/motion/harmonics/space instead.

