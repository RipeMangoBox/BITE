#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable, Mapping, Sequence

import numpy as np


FORWARD_NPZ_REQUIRED_KEYS = (
    "signal",
    "valid_mask",
    "meta_json",
    "axis_names_json",
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

OPTIONAL_FORWARD_NPZ_KEYS = (
    "logits",
    "probabilities",
    "hidden_states",
    "attention_context",
    "condition_projection",
    "confidence",
)


@dataclass(frozen=True)
class TraceRequest:
    run_id: str
    sample_id: str
    model: str
    model_family: str
    condition_id: str
    condition_text: str
    paired_condition_id: str
    z_kind: str
    z_id: str
    f_name: str
    f_space: str
    motion_artifact_path: str = ""
    role: str = "diagnostic"
    used_for: str = "observation"
    limitations: str = "Internal trace only; not a final evaluator."
    output_name: str | None = None
    extra_meta: Mapping[str, Any] = field(default_factory=dict)

    def to_meta(self) -> dict[str, Any]:
        meta = {
            "run_id": self.run_id,
            "sample_id": self.sample_id,
            "model": self.model,
            "model_family": self.model_family,
            "condition_id": self.condition_id,
            "condition_text": self.condition_text,
            "paired_condition_id": self.paired_condition_id,
            "z_kind": self.z_kind,
            "z_id": self.z_id,
            "f_name": self.f_name,
            "f_space": self.f_space,
            "motion_artifact_path": self.motion_artifact_path,
            "role": self.role,
            "used_for": self.used_for,
            "limitations": self.limitations,
        }
        meta.update(dict(self.extra_meta))
        return meta


TraceCallable = Callable[[TraceRequest], Mapping[str, Any]]


class T5TraceAdapter:
    """Minimal writer for forward traces from external T5-family hook callables.

    Manifest `forward_npz_path` is written relative to this adapter's output root.
    """

    def __init__(self, output_dir: str | Path, manifest_name: str = "forward_manifest.jsonl") -> None:
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.manifest_path = self.output_dir / manifest_name

    def collect_forward(
        self,
        request: TraceRequest,
        trace_callable: TraceCallable,
        axis_names: Sequence[str] | None = None,
    ) -> Path:
        trace = dict(trace_callable(request))
        if "signal" not in trace:
            raise ValueError("trace_callable must return a 'signal' array")

        signal = np.asarray(trace["signal"])
        if signal.ndim == 0:
            raise ValueError("signal must have at least one axis")

        axis_names = list(axis_names or trace.get("axis_names") or [])
        if len(axis_names) != signal.ndim:
            raise ValueError(
                f"axis_names length {len(axis_names)} does not match signal.ndim {signal.ndim}"
            )

        valid_mask = self._coerce_valid_mask(trace.get("valid_mask"), signal)
        meta = request.to_meta()
        self._validate_meta(meta)

        npz_path = self.output_dir / self._output_name(request)
        meta["forward_npz_path"] = str(npz_path.resolve().relative_to(self.output_dir.resolve()))

        arrays: dict[str, Any] = {
            "signal": signal,
            "valid_mask": valid_mask,
            "meta_json": np.array(_json_dumps(meta)),
            "axis_names_json": np.array(_json_dumps(axis_names)),
        }
        for key in OPTIONAL_FORWARD_NPZ_KEYS:
            if key in trace and trace[key] is not None:
                arrays[key] = np.asarray(trace[key])

        np.savez(npz_path, **arrays)

        manifest_record = {field: meta.get(field, "") for field in FORWARD_MANIFEST_REQUIRED_FIELDS}
        self._validate_manifest_record(manifest_record)
        with self.manifest_path.open("a", encoding="utf-8") as handle:
            handle.write(_json_dumps(manifest_record) + "\n")

        return npz_path

    @staticmethod
    def _coerce_valid_mask(mask: Any, signal: np.ndarray) -> np.ndarray:
        if mask is None:
            shape = signal.shape[:-1] if signal.ndim > 1 else signal.shape
            return np.ones(shape, dtype=bool)

        valid_mask = np.asarray(mask).astype(bool)
        allowed_shapes = {signal.shape}
        if signal.ndim > 1:
            allowed_shapes.add(signal.shape[:-1])
        if valid_mask.shape not in allowed_shapes:
            raise ValueError(
                f"valid_mask shape {valid_mask.shape} is not compatible with signal shape {signal.shape}"
            )
        return valid_mask

    @staticmethod
    def _output_name(request: TraceRequest) -> str:
        if request.output_name:
            return request.output_name
        raw = (
            f"{request.run_id}_{request.sample_id}_{request.condition_id}_"
            f"{request.z_id}_{request.f_name}_forward.npz"
        )
        return re.sub(r"[^A-Za-z0-9_.-]+", "_", raw)

    @staticmethod
    def _validate_meta(meta: Mapping[str, Any]) -> None:
        missing = [field for field in FORWARD_META_REQUIRED_FIELDS if field not in meta]
        if missing:
            raise ValueError(f"meta_json missing required fields: {missing}")
        if meta.get("role") != "diagnostic":
            raise ValueError("Agent A traces must keep role='diagnostic'")

    @staticmethod
    def _validate_manifest_record(record: Mapping[str, Any]) -> None:
        missing = [
            field
            for field in FORWARD_MANIFEST_REQUIRED_FIELDS
            if field not in record or record.get(field) in (None, "")
        ]
        if missing:
            raise ValueError(f"forward manifest missing required fields: {missing}")
        if record.get("role") != "diagnostic":
            raise ValueError("forward manifest role must be diagnostic for this adapter")


def validate_forward_npz(npz_path: str | Path) -> dict[str, Any]:
    path = Path(npz_path)
    with np.load(path, allow_pickle=False) as data:
        missing = [key for key in FORWARD_NPZ_REQUIRED_KEYS if key not in data.files]
        if missing:
            raise ValueError(f"{path} missing required NPZ keys: {missing}")
        signal = np.asarray(data["signal"])
        valid_mask = np.asarray(data["valid_mask"])
        meta = _loads_npz_json(data["meta_json"])
        axis_names = _loads_npz_json(data["axis_names_json"])

    if len(axis_names) != signal.ndim:
        raise ValueError(
            f"{path} axis_names length {len(axis_names)} does not match signal.ndim {signal.ndim}"
        )
    T5TraceAdapter._coerce_valid_mask(valid_mask, signal)
    T5TraceAdapter._validate_meta(meta)

    return {
        "npz_path": str(path),
        "signal_shape": list(signal.shape),
        "valid_mask_shape": list(valid_mask.shape),
        "axis_names": axis_names,
        "meta": meta,
    }


def validate_manifest_jsonl(manifest_path: str | Path) -> list[dict[str, Any]]:
    path = Path(manifest_path)
    records = []
    with path.open("r", encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, start=1):
            if not line.strip():
                continue
            record = json.loads(line)
            try:
                T5TraceAdapter._validate_manifest_record(record)
            except ValueError as exc:
                raise ValueError(f"{path}:{line_number}: {exc}") from exc
            records.append(record)
    if not records:
        raise ValueError(f"{path} has no manifest records")
    return records


def _json_dumps(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True)


def _loads_npz_json(value: np.ndarray) -> Any:
    item = value.item()
    if isinstance(item, bytes):
        item = item.decode("utf-8")
    return json.loads(str(item))
