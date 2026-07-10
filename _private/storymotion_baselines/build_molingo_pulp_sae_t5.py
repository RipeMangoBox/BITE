#!/usr/bin/env python3
"""Disabled PulpMotion -> MoLingo SAE teacher builder.

PulpMotion human text is sequence-level and does not provide the frame-level
labels required by MoLingo's SAE objective. Do not construct
`babel_272_annotation_t5` from sequence captions; doing so would create a
misleading SAE adaptation.
"""

from __future__ import annotations


def main() -> None:
    raise SystemExit(
        "SAE adaptation is disabled: PulpMotion human text is sequence-level "
        "and lacks frame-level labels required by MoLingo SAE."
    )


if __name__ == "__main__":
    main()
