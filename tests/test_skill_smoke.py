from __future__ import annotations

import json
import subprocess
import tempfile
import unittest
from pathlib import Path


SKILL_DIR = Path(__file__).resolve().parent.parent
SCRIPT = SKILL_DIR / "scripts" / "suno_prompt_builder.py"
EVALS = SKILL_DIR / "evals" / "evals.json"
EXAMPLES = SKILL_DIR / "references" / "examples"


def run_builder(config_name: str) -> str:
    with tempfile.NamedTemporaryFile("w+", suffix=".txt") as tmp:
        subprocess.run(
            ["python3", str(SCRIPT), "--config", str(EXAMPLES / config_name), "--out", tmp.name],
            check=True,
            capture_output=True,
            text=True,
        )
        return Path(tmp.name).read_text(encoding="utf-8")


class SunoPromptwritingSmokeTests(unittest.TestCase):
    def test_initial_example_outputs_generation_blocks(self) -> None:
        output = run_builder("example_prompt_config.yaml")
        self.assertIn("## Prompt Style", output)
        self.assertIn("## Exclude Styles", output)
        self.assertIn("## Lyrics", output)
        self.assertIn("///*****///", output)

    def test_cover_example_outputs_remaster_blocks_only(self) -> None:
        output = run_builder("example_cover_remaster_config.yaml")
        self.assertIn("## Cover Prompt (minimal)", output)
        self.assertIn("## Settings (manual)", output)
        self.assertNotIn("## Lyrics", output)
        self.assertNotIn("## Prompt Style", output)

    def test_each_eval_has_discriminating_expectations(self) -> None:
        data = json.loads(EVALS.read_text(encoding="utf-8"))
        evals = data.get("evals", [])
        self.assertGreaterEqual(len(evals), 3)
        for eval_case in evals:
            expectations = eval_case.get("expectations")
            self.assertIsInstance(expectations, list, f"missing expectations for eval {eval_case.get('id')}")
            self.assertGreaterEqual(
                len(expectations), 2, f"need at least two expectations for eval {eval_case.get('id')}"
            )
            for expectation in expectations:
                self.assertIsInstance(expectation, str)
                self.assertTrue(expectation.strip())


if __name__ == "__main__":
    unittest.main()
