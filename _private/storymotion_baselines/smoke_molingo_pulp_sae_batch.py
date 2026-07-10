#!/usr/bin/env python3
"""Disabled MoLingo SAE smoke test for PulpMotion.

PulpMotion human text is sequence-level and lacks the frame-level labels needed
for MoLingo SAE. This smoke test is intentionally disabled to prevent treating a
sequence-caption broadcast as a valid SAE adaptation.
"""

from __future__ import annotations


def main() -> None:
    raise SystemExit(
        "SAE smoke is disabled: PulpMotion human text is sequence-level and "
        "lacks frame-level labels required by MoLingo SAE."
    )


if __name__ == "__main__":
    main()
