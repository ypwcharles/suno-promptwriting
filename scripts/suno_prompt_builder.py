#!/usr/bin/env python3
"""
Suno workflow formatter + sanity checker.

Goal: produce copy/paste blocks for either initial generation or cover remaster
that match the bundled `suno.md` guide.
This script formats; it does not "create" lyrics.
"""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml


LYRICS_DIVIDER = "///*****///"
RESTRICTED_MAX_MODE_KEYWORDS = {
    "electronic",
    "edm",
    "trap",
    "hip-hop",
    "hip hop",
    "synthwave",
}


def _die(message: str) -> None:
    print(f"error: {message}", file=sys.stderr)
    raise SystemExit(2)


def _load_yaml(path: Path) -> dict[str, Any]:
    try:
        raw = path.read_text(encoding="utf-8")
    except FileNotFoundError:
        _die(f"config not found: {path}")
    try:
        data = yaml.safe_load(raw)
    except Exception as exc:  # noqa: BLE001
        _die(f"failed to parse yaml: {exc}")
    if not isinstance(data, dict):
        _die("config must be a YAML mapping/object at the top level")
    return data


def _as_str(value: Any, *, field: str) -> str:
    if not isinstance(value, str) or not value.strip():
        _die(f"`{field}` must be a non-empty string")
    return value.strip()


def _as_bool(value: Any, *, field: str) -> bool:
    if not isinstance(value, bool):
        _die(f"`{field}` must be a boolean")
    return value


def _as_list_str(value: Any, *, field: str) -> list[str]:
    if value is None:
        return []
    if not isinstance(value, list) or not all(isinstance(x, str) for x in value):
        _die(f"`{field}` must be a list of strings")
    return [x.strip() for x in value if x.strip()]


def _as_int(value: Any, *, field: str) -> int:
    if not isinstance(value, int):
        _die(f"`{field}` must be an integer")
    return value


def _approx_syllables(line: str) -> int:
    # Very rough heuristic (English-focused). Used only for warnings.
    normalized = re.sub(r"[^a-zA-Z']", " ", line).lower()
    tokens = [t for t in normalized.split() if t]
    count = 0
    for token in tokens:
        groups = re.findall(r"[aeiouy]+", token)
        count += max(1, len(groups)) if groups else 0
    return count


@dataclass(frozen=True)
class LyricSection:
    header: str
    meta: list[str]
    lines: list[str]

    def render(self) -> str:
        meta_suffix = ""
        if self.meta:
            meta_suffix = " | " + " | ".join(self.meta)
        out = [f"[{self.header}{meta_suffix}]"]
        out.extend(self.lines)
        return "\n".join(out)


def _parse_sections(data: dict[str, Any]) -> list[LyricSection]:
    lyrics = data.get("lyrics") or {}
    if not isinstance(lyrics, dict):
        _die("`lyrics` must be an object")

    sections = lyrics.get("sections")
    if not isinstance(sections, list) or not sections:
        _die("`lyrics.sections` must be a non-empty list")

    parsed: list[LyricSection] = []
    for idx, section in enumerate(sections, start=1):
        if not isinstance(section, dict):
            _die(f"`lyrics.sections[{idx}]` must be an object")

        header = _as_str(section.get("header"), field=f"lyrics.sections[{idx}].header")
        meta = _as_list_str(section.get("meta"), field=f"lyrics.sections[{idx}].meta")
        lines = section.get("lines")
        if not isinstance(lines, list) or not all(isinstance(x, str) for x in lines):
            _die(f"`lyrics.sections[{idx}].lines` must be a list of strings")
        lines_clean = [x.rstrip() for x in lines if x.strip()]
        if not lines_clean:
            _die(f"`lyrics.sections[{idx}].lines` must contain at least 1 non-empty line")

        parsed.append(LyricSection(header=header, meta=[m for m in meta if m], lines=lines_clean))
    return parsed


def _render_cover_prompt(cover_prompt: dict[str, Any]) -> str:
    if not isinstance(cover_prompt, dict):
        _die("`cover_prompt` must be an object")

    genre = _as_str(cover_prompt.get("genre"), field="cover_prompt.genre")
    instrumentation = cover_prompt.get("instrumentation")
    mastering = cover_prompt.get("mastering")
    instrumentation_s = _as_str(instrumentation, field="cover_prompt.instrumentation") if instrumentation is not None else None
    mastering_s = _as_str(mastering, field="cover_prompt.mastering") if mastering is not None else None

    lines = [f"Genre: {_ensure_period(genre)}"]
    if instrumentation_s:
        lines.append(f"Instrumentation: {_ensure_period(instrumentation_s)}")
    # Keep mastering explicit and minimal; avoid extra style descriptors.
    if mastering_s:
        lines.append(f"Mastering: {_ensure_period(mastering_s)}")
    return "\n".join(lines).rstrip() + "\n"


def _normalize_hint_text(text: str) -> str:
    return re.sub(r"[\s_]+", " ", text).strip().lower()


def _max_mode_restriction_warning(format_name: str, hints: dict[str, Any] | None, prompt_style: dict[str, Any]) -> str | None:
    if format_name.upper() != "B":
        return None

    hay = []
    if hints:
        for key in ("genre_family", "primary_genre", "genre"):
            value = hints.get(key)
            if isinstance(value, str) and value.strip():
                hay.append(value)
            if isinstance(value, list) and all(isinstance(x, str) for x in value):
                hay.extend(value)
    # Also check prompt_style.genre if present.
    genre_field = prompt_style.get("genre")
    if isinstance(genre_field, str) and genre_field.strip():
        hay.append(genre_field)

    normalized = " ".join(_normalize_hint_text(x) for x in hay if x)
    if any(k in normalized for k in RESTRICTED_MAX_MODE_KEYWORDS):
        return (
            "Format B (MAX Mode) selected, but hints/genre suggest Electronic/EDM/Trap/Hip-Hop/Synthwave; "
            "`suno.md` notes MAX Mode has minimal improvement there. Prefer Format A/C."
        )
    return None


def _render_prompt_style(
    format_name: str,
    prompt_style: dict[str, Any],
    start_on_phrase: str | None,
    duet_start_on: tuple[str, str] | None,
) -> str:
    f = format_name.upper()
    if f not in {"A", "B", "C"}:
        _die("`format` must be one of: A, B, C")

    if not isinstance(prompt_style, dict):
        _die("`prompt_style` must be an object")

    def get(field: str) -> str | None:
        value = prompt_style.get(field)
        if value is None:
            return None
        return _as_str(value, field=f"prompt_style.{field}")

    # Keep ordering stable and aligned to the guide’s “core sections”.
    fields = [
        ("genre", get("genre")),
        ("vocal", get("vocal")),
        ("instrumentation", get("instrumentation")),
        ("production", get("production")),
        ("mastering", get("mastering")),
        ("mood", get("mood")),
    ]

    if f == "C":
        # Format C is freeform; prefer a single dense line.
        text = get("text")
        if not text:
            # Allow a fallback build if user provided structured fields.
            parts = [v for _, v in fields if v]
            if not parts:
                _die("for format C, set `prompt_style.text` (or provide at least one structured field)")
            text = " and ".join(parts)
        if not text.endswith("."):
            text += "."
        return text

    lines: list[str] = []
    if f == "B":
        # The guide’s MAX Mode stack; keep exact formatting.
        lines.extend(
            [
                "[Is_MAX_MODE: MAX](MAX)",
                "[QUALITY: MAX](MAX)",
                "[REALISM: MAX](MAX)",
                "[REAL_INSTRUMENTS: MAX](MAX)",
            ]
        )
        if duet_start_on:
            male_phrase, female_phrase = duet_start_on
            lines.extend(
                [
                    "[DUET_START_ON: TRUE]",
                    f'[MALE_START_ON: "{male_phrase}"]',
                    f'[FEMALE_START_ON: "{female_phrase}"]',
                ]
            )
        elif start_on_phrase:
            lines.extend(["[START_ON: TRUE]", f'[START_ON: "{start_on_phrase}"]'])
        lines.append("")

        # The guide’s example uses `instruments:` and `style tags:` (not necessarily `instrumentation`/`production`).
        genre = get("genre")
        instruments = get("instruments") or get("instrumentation")
        style_tags = get("style tags") or get("style_tags") or get("production")

        if genre:
            lines.append(f'genre: "{_ensure_period(genre)}"')
        if instruments:
            lines.append(f'instruments: "{_ensure_period(instruments)}"')
        if style_tags:
            lines.append(f'style tags: "{_ensure_period(style_tags)}"')

        return "\n".join(lines).strip() + "\n"

    # Format A
    for key, value in fields:
        if not value:
            continue
        lines.append(f'{key}: "{_ensure_period(value)}"')
        lines.append("")
    if not lines:
        _die("format A requires at least one `prompt_style.*` field (genre/vocal/instrumentation/production/mastering/mood)")
    return "\n".join(lines).rstrip() + "\n"


def _ensure_period(text: str) -> str:
    t = text.strip()
    return t if t.endswith(".") else t + "."


def _render_exclude_styles(exclude_styles: list[str]) -> str:
    return "\n".join(exclude_styles).strip() + ("\n" if exclude_styles else "")


def _render_lyrics(sections: list[LyricSection], *, divider: bool) -> str:
    parts: list[str] = []
    if divider:
        parts.append(LYRICS_DIVIDER)
        parts.append("")
    parts.append("\n\n".join(s.render() for s in sections))
    return "\n".join(parts).rstrip() + "\n"


def _qa_checks(prompt_style_text: str, lyrics_text: str) -> list[str]:
    warnings: list[str] = []

    # Lyric-bleed triggers in Prompt Style (heuristic).
    # Warn on bracketed "stage directions" (but not the guide’s MAX/START_ON style parameters).
    for line in prompt_style_text.splitlines():
        line = line.strip()
        if not line.startswith("[") or not line.endswith("]"):
            continue
        if re.match(
            r"^\[(Is_MAX_MODE|QUALITY|REALISM|REAL_INSTRUMENTS|START_ON|DUET_START_ON|MALE_START_ON|FEMALE_START_ON):\s*",
            line,
        ):
            continue
        if re.match(r"^\[(Is_MAX_MODE|QUALITY|REALISM|REAL_INSTRUMENTS):\s*MAX\]\(MAX\)$", line):
            continue
        warnings.append(
            "Prompt Style contains bracketed lines that may look like performable stage directions; move performable text to Lyrics (lyric-bleed risk)."
        )
        break

    # Quotes are normal in Format A (colon + quotes) and appear in START_ON lines.
    # Only warn if a line contains quotes but doesn't look like a structured field or START_ON parameter.
    for line in prompt_style_text.splitlines():
        if '"' not in line:
            continue
        if re.match(r'^\w[\w ]*:\s*".*"\s*$', line.strip()):
            continue
        if re.match(r'^\[START_ON:\s*".*"\]\s*$', line.strip()):
            continue
        if re.match(r'^\[(MALE_START_ON|FEMALE_START_ON):\s*".*"\]\s*$', line.strip()):
            continue
        warnings.append(
            'Prompt Style contains quotes in a non-structured line; keep quotes inside structured fields only (lyric-bleed risk).'
        )
        break

    # Lyrics divider.
    if not lyrics_text.lstrip().startswith(LYRICS_DIVIDER):
        warnings.append("Lyrics does not start with the guide divider `///*****///`.")

    # Section separation (blank line between headers).
    if re.search(r"\]\n[^\n]", lyrics_text):
        # Header immediately followed by line is fine; this check is for missing blank lines between sections.
        pass
    if re.search(r"\n\[[^\]]+\]\n[^\n]+\n\[[^\]]+\]", lyrics_text):
        warnings.append("Lyrics sections may be missing a blank line between them (guide recommends clear separation).")

    # Syllable guideline (rough).
    lyric_lines = [
        ln.strip()
        for ln in lyrics_text.splitlines()
        if ln.strip() and not ln.strip().startswith("[") and ln.strip() != LYRICS_DIVIDER
    ]
    for ln in lyric_lines[:20]:
        if ln.startswith("(") and ln.endswith(")"):
            continue
        s = _approx_syllables(ln)
        if s < 5 or s > 12:
            warnings.append(f"Line may be hard to sing (approx syllables={s}): {ln}")
            break

    return warnings


def _render_settings(settings: dict[str, Any]) -> str:
    lines: list[str] = []

    def add(label: str, value: Any) -> None:
        if value is None:
            return
        lines.append(f"{label}: {value}")

    add("Weirdness", settings.get("weirdness"))
    add("Style Influence", settings.get("style_influence"))
    add("Vocal Gender", settings.get("vocal_gender"))
    add("Audio Influence", settings.get("audio_influence"))

    return "\n".join(lines).strip() + ("\n" if lines else "")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Format/check Suno initial-generation or cover-remaster blocks from YAML config."
    )
    parser.add_argument("--config", required=True, help="Path to YAML config.")
    parser.add_argument("--out", help="Write combined output to this file (defaults to stdout).")
    parser.add_argument("--qa-only", action="store_true", help="Only print QA warnings (exit 1 if any).")
    args = parser.parse_args()

    cfg_path = Path(args.config).expanduser().resolve()
    data = _load_yaml(cfg_path)

    mode = data.get("mode", "initial")
    if not isinstance(mode, str) or not mode.strip():
        _die("`mode` must be a non-empty string")
    mode = mode.strip().lower()
    if mode not in {"initial", "cover_remaster"}:
        _die("`mode` must be one of: initial, cover_remaster")

    format_name = _as_str(data.get("format", "A"), field="format")

    exclude_styles = _as_list_str(data.get("exclude_styles"), field="exclude_styles")

    start_on_phrase: str | None = None
    start_on = data.get("start_on")
    if start_on is not None:
        if not isinstance(start_on, dict):
            _die("`start_on` must be an object")
        enabled = _as_bool(start_on.get("enabled", False), field="start_on.enabled")
        if enabled:
            start_on_phrase = _as_str(start_on.get("phrase"), field="start_on.phrase")

    duet_start_on: tuple[str, str] | None = None
    duet = data.get("duet_start_on")
    if duet is not None:
        if not isinstance(duet, dict):
            _die("`duet_start_on` must be an object")
        enabled = _as_bool(duet.get("enabled", False), field="duet_start_on.enabled")
        if enabled:
            male_phrase = _as_str(duet.get("male_phrase"), field="duet_start_on.male_phrase")
            female_phrase = _as_str(duet.get("female_phrase"), field="duet_start_on.female_phrase")
            duet_start_on = (male_phrase, female_phrase)
            if start_on_phrase:
                print("warning: `duet_start_on` enabled; ignoring `start_on`.", file=sys.stderr)

    prompt_style = data.get("prompt_style") or {}
    prompt_style_text = ""
    if mode == "initial":
        prompt_style_text = _render_prompt_style(format_name, prompt_style, start_on_phrase, duet_start_on)

    hints = data.get("hints")
    if hints is not None and not isinstance(hints, dict):
        _die("`hints` must be an object")

    persona = data.get("persona")
    if persona is not None and (not isinstance(persona, str) or not persona.strip()):
        _die("`persona` must be a non-empty string when provided")
    persona_text = persona.strip() if isinstance(persona, str) else None

    settings_text = ""
    settings = data.get("settings")
    if settings is not None:
        if not isinstance(settings, dict):
            _die("`settings` must be an object")

        weirdness = settings.get("weirdness")
        if weirdness is not None:
            weirdness = _as_int(weirdness, field="settings.weirdness")
            if weirdness < 0 or weirdness > 100:
                _die("`settings.weirdness` must be between 0 and 100")

        style_influence = settings.get("style_influence")
        if style_influence is not None:
            style_influence = _as_int(style_influence, field="settings.style_influence")
            if style_influence < 0 or style_influence > 100:
                _die("`settings.style_influence` must be between 0 and 100")

        audio_influence = settings.get("audio_influence")
        if audio_influence is not None:
            audio_influence = _as_int(audio_influence, field="settings.audio_influence")
            if audio_influence < 0 or audio_influence > 100:
                _die("`settings.audio_influence` must be between 0 and 100")

        vocal_gender = settings.get("vocal_gender")
        if vocal_gender is not None:
            vocal_gender = _as_str(vocal_gender, field="settings.vocal_gender")
            if vocal_gender.lower() not in {"male", "female"}:
                _die("`settings.vocal_gender` must be 'Male' or 'Female'")

        settings_text = _render_settings(
            {
                "weirdness": weirdness,
                "style_influence": style_influence,
                "audio_influence": audio_influence,
                "vocal_gender": vocal_gender,
            }
        )

    cover_prompt_text = ""
    lyrics_text = ""
    sections: list[LyricSection] = []
    if mode == "cover_remaster":
        cover_prompt = data.get("cover_prompt") or {}
        cover_prompt_text = _render_cover_prompt(cover_prompt)
        # If user didn't set settings, apply `suno.md`-aligned defaults for Cover workflows.
        if not settings_text:
            settings_text = _render_settings({"weirdness": 0, "style_influence": 100, "audio_influence": 100})
    else:
        sections = _parse_sections(data)
        divider = True
        lyrics_cfg = data.get("lyrics") or {}
        if isinstance(lyrics_cfg, dict) and "divider" in lyrics_cfg:
            divider = _as_bool(lyrics_cfg.get("divider"), field="lyrics.divider")
        lyrics_text = _render_lyrics(sections, divider=divider)

    warnings: list[str] = []
    if mode == "initial":
        max_mode_warning = _max_mode_restriction_warning(format_name, hints, prompt_style)
        if max_mode_warning:
            warnings.append(max_mode_warning)

    if mode == "initial":
        warnings.extend(_qa_checks(prompt_style_text, lyrics_text))
    if persona_text and len(persona_text) < 40:
        warnings.append("Persona looks short; `suno.md` recommends a dossier, not a label.")

    if mode == "initial":
        # Lyric structure heuristics from `suno.md` (warnings only).
        section_warnings = 0
        for section in sections:
            if section_warnings >= 3:
                break

            line_count = len([ln for ln in section.lines if ln.strip()])
            if line_count not in {4, 8}:
                warnings.append(
                    f"Section '{section.header}' has {line_count} lines; `suno.md` notes 4 lines is standard (8 for longer sections)."
                )
                section_warnings += 1
                continue

            syllable_counts = []
            for ln in section.lines:
                stripped = ln.strip()
                if not stripped or (stripped.startswith("(") and stripped.endswith(")")):
                    continue
                syllable_counts.append(_approx_syllables(stripped))
            # The guide recommends ±1–2; this script uses an approximate syllable counter,
            # so we warn only on larger variance to reduce false positives.
            if len(syllable_counts) >= 4 and (max(syllable_counts) - min(syllable_counts) > 3):
                warnings.append(
                    f"Section '{section.header}' lines may have inconsistent syllable counts; `suno.md` recommends ±1–2 variance within a section."
                )
                section_warnings += 1
    if args.qa_only:
        if warnings:
            for w in warnings:
                print(f"QA: {w}", file=sys.stderr)
            raise SystemExit(1)
        return

    out_parts: list[str] = []
    if mode == "initial":
        out_parts.extend(["## Prompt Style", prompt_style_text.rstrip()])
        if settings_text:
            out_parts.extend(["", "## Settings (manual)", settings_text.rstrip()])
        if persona_text:
            out_parts.extend(["", "## Persona", persona_text])
        out_parts.extend(["", "## Exclude Styles", _render_exclude_styles(exclude_styles).rstrip(), "", "## Lyrics", lyrics_text.rstrip(), ""])
    else:
        # Cover-based remastering: deliver the minimal cover prompt + suggested settings.
        if settings_text:
            out_parts.extend(["## Settings (manual)", settings_text.rstrip()])
        out_parts.extend(["", "## Cover Prompt (minimal)", cover_prompt_text.rstrip()])
        if persona_text:
            out_parts.extend(["", "## Persona", persona_text])
        if exclude_styles:
            out_parts.extend(["", "## Exclude Styles", _render_exclude_styles(exclude_styles).rstrip()])
    output = "\n".join(out_parts).rstrip() + "\n"

    if args.out:
        Path(args.out).expanduser().resolve().write_text(output, encoding="utf-8")
    else:
        print(output, end="")

    if warnings:
        print("\nQA warnings:", file=sys.stderr)
        for w in warnings:
            print(f"- {w}", file=sys.stderr)


if __name__ == "__main__":
    main()
