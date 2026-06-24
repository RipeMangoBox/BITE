"""Minimal forward trace writer for CLIP/discrete motion-token models.

The skeleton intentionally has no dependency on MoMask, MoGenTS, or torch. A
real integration should pass a callable that captures one already-computed hook
tensor and returns numpy-compatible arrays.
"""

from __future__ import annotations

from dataclasses import dataclass, field
import json
from pathlib import Path
import re
from typing import Any, Callable, Mapping

import numpy as np


FORWARD_NPZ_REQUIRED_KEYS = ("signal", "valid_mask", "meta_json", "axis_names_json")

FORWARD_META_REQUIRED_FIELDS = (
    "run_id",
    "sample_id",
    "model",
    "model_family",
    "condition_id",
    "condition_text",
    "z_kind",
    "z_id",
    "f_name",
    "f_space",
    "role",
    "limitations",
)

FORWARD_MANIFEST_REQUIRED_FIELDS = (
    "run_id",
    "sample_id",
    "model",
    "model_family",
    "condition_id",
    "condition_text",
    "paired_condition_id",
    "z_kind",
    "z_id",
    "f_name",
    "f_space",
    "forward_npz_path",
    "motion_artifact_path",
    "role",
    "used_for",
    "limitations",
)


@dataclass(frozen=True)
class TraceSpec:
    run_id: str
    sample_id: str
    model: str
    condition_id: str
    condition_text: str
    paired_condition_id: str
    z_kind: str
    z_id: str
    f_name: str
    f_space: str
    axis_names: tuple[str, ...]
    model_family: str = "clip_discrete"
    role: str = "diagnostic"
    used_for: str = "observation"
    limitations: str = "Internal trace only; not a final evaluator."
    motion_artifact_path: str = ""
    extra_meta: Mapping[str, Any] = field(default_factory=dict)
    npz_name: str | None = None


def run_forward_trace(
    hook_callable: Callable[[TraceSpec], Mapping[str, Any]],
    spec: TraceSpec,
    output_dir: str | Path,
    manifest_name: str = "forward_manifest.jsonl",
) -> dict[str, Any]:
    """Run a hook callable once and write one forward NPZ plus manifest row.

    The callable must return at least ``{"signal": array_like}``. It should
    normally return ``valid_mask`` whose shape matches the signal's non-channel
    prefix, for example [B, T] for [B, T, vocab] logits or [B, T, J] for
    [B, T, J, code_dim] expected embeddings.
    """

    _validate_spec(spec)
    record = dict(hook_callable(spec))
    if "signal" not in record:
        raise ValueError("hook_callable must return a 'signal' array")

    signal = np.asarray(record.pop("signal"))
    if signal.size == 0:
        raise ValueError("signal must be non-empty")

    valid_mask = np.asarray(record.pop("valid_mask", np.ones(signal.shape[:-1], dtype=bool)))
    if valid_mask.size == 0:
        raise ValueError("valid_mask must be non-empty")
    valid_mask = valid_mask.astype(bool, copy=False)

    _validate_signal_layout(signal, valid_mask, spec.axis_names)

    meta = _build_meta(spec)
    axis_names_json = json.dumps(list(spec.axis_names), ensure_ascii=False)
    meta_json = json.dumps(meta, ensure_ascii=False, sort_keys=True)

    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    npz_path = output_path / (spec.npz_name or _default_npz_name(spec))

    optional_arrays = {
        key: np.asarray(value)
        for key, value in record.items()
        if value is not None and not key.startswith("_")
    }

    np.savez_compressed(
        npz_path,
        signal=signal,
        valid_mask=valid_mask,
        meta_json=np.array(meta_json),
        axis_names_json=np.array(axis_names_json),
        **optional_arrays,
    )

    manifest_path = output_path / manifest_name
    manifest_row = _build_manifest_row(spec, npz_path)
    with manifest_path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(manifest_row, ensure_ascii=False, sort_keys=True) + "\n")

    return {
        "npz_path": npz_path,
        "manifest_path": manifest_path,
        "meta": meta,
        "manifest_row": manifest_row,
    }


def _validate_spec(spec: TraceSpec) -> None:
    base = _base_meta(spec)
    missing = [field for field in FORWARD_META_REQUIRED_FIELDS if field not in base]
    if missing:
        raise ValueError(f"missing required meta fields: {missing}")

    empty = [
        field
        for field in FORWARD_META_REQUIRED_FIELDS
        if field != "condition_text" and base.get(field) in (None, "")
    ]
    if empty:
        raise ValueError(f"required meta fields must be non-empty: {empty}")

    if spec.role != "diagnostic":
        raise ValueError("Agent B traces must keep role='diagnostic'")
    if not spec.used_for:
        raise ValueError("used_for must be non-empty")
    if not spec.axis_names:
        raise ValueError("axis_names must be non-empty")

    collisions = sorted(set(spec.extra_meta).intersection(base))
    if collisions:
        raise ValueError(f"extra_meta cannot override required fields: {collisions}")


def _validate_signal_layout(
    signal: np.ndarray,
    valid_mask: np.ndarray,
    axis_names: tuple[str, ...],
) -> None:
    if len(axis_names) != signal.ndim:
        raise ValueError(
            f"axis_names length {len(axis_names)} must equal signal.ndim {signal.ndim}"
        )
    if valid_mask.ndim > signal.ndim:
        raise ValueError("valid_mask cannot have more dimensions than signal")
    if valid_mask.shape != signal.shape[: valid_mask.ndim]:
        raise ValueError(
            "valid_mask shape must match a prefix of signal shape: "
            f"valid_mask={valid_mask.shape}, signal={signal.shape}"
        )


def _build_meta(spec: TraceSpec) -> dict[str, Any]:
    meta = _base_meta(spec)
    meta.update(spec.extra_meta)
    return meta


def _base_meta(spec: TraceSpec) -> dict[str, Any]:
    return {
        "run_id": spec.run_id,
        "sample_id": spec.sample_id,
        "model": spec.model,
        "model_family": spec.model_family,
        "condition_id": spec.condition_id,
        "condition_text": spec.condition_text,
        "z_kind": spec.z_kind,
        "z_id": spec.z_id,
        "f_name": spec.f_name,
        "f_space": spec.f_space,
        "role": spec.role,
        "limitations": spec.limitations,
    }


def _build_manifest_row(spec: TraceSpec, npz_path: Path) -> dict[str, Any]:
    row = {
        "run_id": spec.run_id,
        "sample_id": spec.sample_id,
        "model": spec.model,
        "model_family": spec.model_family,
        "condition_id": spec.condition_id,
        "condition_text": spec.condition_text,
        "paired_condition_id": spec.paired_condition_id,
        "z_kind": spec.z_kind,
        "z_id": spec.z_id,
        "f_name": spec.f_name,
        "f_space": spec.f_space,
        "forward_npz_path": npz_path.as_posix(),
        "motion_artifact_path": spec.motion_artifact_path,
        "role": spec.role,
        "used_for": spec.used_for,
        "limitations": spec.limitations,
    }
    missing = [
        field
        for field in FORWARD_MANIFEST_REQUIRED_FIELDS
        if field not in row or row.get(field) in (None, "")
    ]
    if missing:
        raise ValueError(f"missing required manifest fields: {missing}")
    return row


def _default_npz_name(spec: TraceSpec) -> str:
    raw = "__".join(
        [spec.run_id, spec.sample_id, spec.model, spec.condition_id, spec.z_id, spec.f_name]
    )
    return _safe_filename(raw) + ".npz"


def _safe_filename(value: str) -> str:
    value = re.sub(r"[^A-Za-z0-9_.-]+", "_", value)
    return value.strip("._") or "trace"
