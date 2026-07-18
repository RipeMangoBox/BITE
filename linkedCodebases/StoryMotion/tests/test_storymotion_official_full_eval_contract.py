from __future__ import annotations

import sys
import unittest
from pathlib import Path


SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from storymotion_official_full_eval import build_parser  # noqa: E402


class OfficialFullEvalContractTests(unittest.TestCase):
    def test_nondefault_tokenizer_contract_requires_explicit_eval_opt_in(self) -> None:
        defaults = build_parser().parse_args(["--cache-dir", "cache", "--task", "human"])
        explicit = build_parser().parse_args(
            [
                "--cache-dir",
                "cache",
                "--task",
                "human",
                "--allow-nondefault-tokenizer-contract",
            ]
        )

        self.assertIs(defaults.allow_nondefault_tokenizer_contract, False)
        self.assertIs(explicit.allow_nondefault_tokenizer_contract, True)
