#!/usr/bin/env python3
"""Validate MoDebug trace artifacts and compute forward deltas."""

from __future__ import annotations

import argparse
import csv
import json
import math
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import numpy as np


FORWARD_NPZ_KEYS = ("signal", "valid_mask", "meta_json", "axis_names_json")
DELTA_NPZ_KEYS = ("delta", "metric_value", "meta_json")

FORWARD_META_REQUIRED = (
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

DELTA_META_REQUIRED = (
    "run_id",
    "sample_id",
    "model",
    "condition_pair",
    "z_kind",
    "z_id",
    "f_name",
    "metric_name",
    "metric_value",
    "role",
    "used_for",
    "limitations",
)

FORWARD_MANIFEST_REQUIRED = (
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

DELTA_MANIFEST_REQUIRED = (
    "run_id",
    "sample_id",
    "model",
    "condition_pair",
    "z_kind",
    "z_id",
    "f_name",
    "metric_name",
    "metric_value",
    "delta_npz_path",
    "role",
    "used_for",
    "limitations",
)

EPS = 1.0e-12


class ValidationError(RuntimeError):
    """Contract validation failure."""


@dataclass(frozen=True)
class ForwardTrace:
    path: Path
    signal: np.ndarray
    valid_mask: np.ndarray
    meta: dict[str, Any]
    axis_names: list[str]


def _load_npz(path: Path) -> dict[str, np.ndarray]:
    if not path.exists():
        raise ValidationError(f"missing NPZ: {path}")
    try:
        with np.load(path, allow_pickle=False) as npz:
            return {key: npz[key] for key in npz.files}
    except Exception as exc:  # pragma: no cover - message wrapper only
        raise ValidationError(f"cannot read NPZ {path}: {exc}") from exc


def _require_keys(data: dict[str, Any], required: tuple[str, ...], where: str) -> None:
    missing = [key for key in required if key not in data]
    if missing:
        raise ValidationError(f"{where} missing required keys: {', '.join(missing)}")


def _scalar_to_python(value: Any, where: str) -> Any:
    array = np.asarray(value)
    if array.shape == ():
        item = array.item()
    elif array.size == 1:
        item = array.reshape(-1)[0].item()
    else:
        raise ValidationError(f"{where} must be a scalar value")
    if isinstance(item, bytes):
        return item.decode("utf-8")
    return item


def _parse_json_scalar(value: Any, where: str, expected_type: type) -> Any:
    text = _scalar_to_python(value, where)
    if not isinstance(text, str):
        raise ValidationError(f"{where} must be a UTF-8 JSON string")
    try:
        parsed = json.loads(text)
    except json.JSONDecodeError as exc:
        raise ValidationError(f"{where} is not valid JSON: {exc}") from exc
    if not isinstance(parsed, expected_type):
        raise ValidationError(f"{where} must decode to {expected_type.__name__}")
    return parsed


def _require_fields(row: dict[str, Any], fields: tuple[str, ...], where: str) -> None:
    missing = []
    for field in fields:
        if field not in row:
            missing.append(field)
            continue
        value = row[field]
        if value is None or (isinstance(value, str) and value == ""):
            missing.append(field)
    if missing:
        raise ValidationError(f"{where} missing required fields: {', '.join(missing)}")


def _validate_role(row: dict[str, Any], where: str) -> None:
    if row.get("role") != "diagnostic":
        raise ValidationError(f"{where} role must be diagnostic")
    if row.get("used_for") == "final_eval":
        raise ValidationError(f"{where} cannot use diagnostic trace as final_eval")


def _validate_numeric_array(array: np.ndarray, where: str) -> np.ndarray:
    if not np.issubdtype(array.dtype, np.number) or np.issubdtype(array.dtype, np.bool_):
        raise ValidationError(f"{where} must be a numeric array")
    array = np.asarray(array)
    if not np.all(np.isfinite(array)):
        raise ValidationError(f"{where} contains non-finite values")
    return array


def _validate_mask(mask: np.ndarray, signal_shape: tuple[int, ...], where: str) -> np.ndarray:
    mask = np.asarray(mask)
    if mask.dtype == np.bool_:
        bool_mask = mask
    elif np.issubdtype(mask.dtype, np.number):
        if not np.all(np.isfinite(mask)):
            raise ValidationError(f"{where} contains non-finite values")
        if not np.all((mask == 0) | (mask == 1)):
            raise ValidationError(f"{where} numeric mask values must be 0 or 1")
        bool_mask = mask.astype(bool)
    else:
        raise ValidationError(f"{where} must be boolean or 0/1 numeric")
    if bool_mask.shape == signal_shape[:-1]:
        bool_mask = np.expand_dims(bool_mask, axis=-1)
    try:
        return np.broadcast_to(bool_mask, signal_shape).astype(bool, copy=True)
    except ValueError as exc:
        raise ValidationError(
            f"{where} shape {mask.shape} is not broadcastable to signal shape {signal_shape}"
        ) from exc


def _validate_axis_names(axis_names: Any, signal_ndim: int, where: str) -> list[str]:
    if not isinstance(axis_names, list) or not all(isinstance(item, str) for item in axis_names):
        raise ValidationError(f"{where} must be a JSON list of strings")
    if len(axis_names) != signal_ndim:
        raise ValidationError(
            f"{where} length {len(axis_names)} does not match signal ndim {signal_ndim}"
        )
    return axis_names


def _metric_scalar(value: Any, where: str) -> float:
    try:
        scalar = float(_scalar_to_python(value, where))
    except (TypeError, ValueError) as exc:
        raise ValidationError(f"{where} must be a scalar float") from exc
    if not math.isfinite(scalar):
        raise ValidationError(f"{where} must be finite")
    return scalar


def validate_forward_file(path: Path) -> ForwardTrace:
    data = _load_npz(path)
    _require_keys(data, FORWARD_NPZ_KEYS, f"forward NPZ {path}")
    signal = _validate_numeric_array(data["signal"], f"{path}:signal")
    meta = _parse_json_scalar(data["meta_json"], f"{path}:meta_json", dict)
    axis_names = _parse_json_scalar(data["axis_names_json"], f"{path}:axis_names_json", list)
    _require_fields(meta, FORWARD_META_REQUIRED, f"{path}:meta_json")
    _validate_role(meta, f"{path}:meta_json")
    axis_names = _validate_axis_names(axis_names, signal.ndim, f"{path}:axis_names_json")
    mask = _validate_mask(data["valid_mask"], signal.shape, f"{path}:valid_mask")
    return ForwardTrace(path=path, signal=signal, valid_mask=mask, meta=meta, axis_names=axis_names)


def validate_delta_file(path: Path) -> dict[str, Any]:
    data = _load_npz(path)
    _require_keys(data, DELTA_NPZ_KEYS, f"delta NPZ {path}")
    _validate_numeric_array(data["delta"], f"{path}:delta")
    metric_value = _metric_scalar(data["metric_value"], f"{path}:metric_value")
    meta = _parse_json_scalar(data["meta_json"], f"{path}:meta_json", dict)
    _require_fields(meta, DELTA_META_REQUIRED, f"{path}:meta_json")
    _validate_role(meta, f"{path}:meta_json")
    meta_metric = _metric_scalar(meta["metric_value"], f"{path}:meta_json.metric_value")
    if not math.isclose(metric_value, meta_metric, rel_tol=1.0e-9, abs_tol=1.0e-12):
        raise ValidationError(f"{path}: metric_value differs between NPZ scalar and meta_json")
    return meta


def _read_manifest(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        raise ValidationError(f"missing manifest: {path}")
    rows: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, start=1):
            line = line.strip()
            if not line:
                continue
            try:
                row = json.loads(line)
            except json.JSONDecodeError as exc:
                raise ValidationError(f"{path}:{line_number} invalid JSONL: {exc}") from exc
            if not isinstance(row, dict):
                raise ValidationError(f"{path}:{line_number} JSONL row must be an object")
            rows.append(row)
    if not rows:
        raise ValidationError(f"{path} has no JSONL rows")
    return rows


def validate_manifest(path: Path, kind: str) -> list[dict[str, Any]]:
    rows = _read_manifest(path)
    required = FORWARD_MANIFEST_REQUIRED if kind == "forward" else DELTA_MANIFEST_REQUIRED
    for index, row in enumerate(rows, start=1):
        where = f"{path}:line {index}"
        _require_fields(row, required, where)
        _validate_role(row, where)
        if kind == "delta":
            _metric_scalar(row["metric_value"], f"{where}.metric_value")
    return rows


def _check_pair_compatibility(text: ForwardTrace, comparison: ForwardTrace) -> None:
    fields = ("run_id", "sample_id", "model", "model_family", "z_kind", "z_id", "f_name", "f_space")
    for field in fields:
        if text.meta.get(field) != comparison.meta.get(field):
            raise ValidationError(
                f"cannot compute delta: meta field {field} differs "
                f"({text.meta.get(field)!r} vs {comparison.meta.get(field)!r})"
            )
    if text.signal.shape != comparison.signal.shape:
        raise ValidationError(
            f"cannot compute delta: signal shape differs {text.signal.shape} vs {comparison.signal.shape}"
        )
    if text.axis_names != comparison.axis_names:
        raise ValidationError("cannot compute delta: axis_names_json differs")


def _valid_vectors(text_signal: np.ndarray, comparison_signal: np.ndarray, mask: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    if not np.any(mask):
        raise ValidationError("combined valid_mask has no valid entries")
    return text_signal[mask].astype(np.float64), comparison_signal[mask].astype(np.float64)


def _relative_l2(text_signal: np.ndarray, comparison_signal: np.ndarray, mask: np.ndarray) -> float:
    text_vec, comparison_vec = _valid_vectors(text_signal, comparison_signal, mask)
    denominator = np.linalg.norm(comparison_vec)
    if denominator <= EPS:
        raise ValidationError("relative_l2 denominator is zero on valid entries")
    return float(np.linalg.norm(text_vec - comparison_vec) / denominator)


def _cosine_distance(text_signal: np.ndarray, comparison_signal: np.ndarray, mask: np.ndarray) -> float:
    text_vec, comparison_vec = _valid_vectors(text_signal, comparison_signal, mask)
    denominator = np.linalg.norm(text_vec) * np.linalg.norm(comparison_vec)
    if denominator <= EPS:
        raise ValidationError("cosine distance undefined for a zero vector on valid entries")
    similarity = float(np.dot(text_vec, comparison_vec) / denominator)
    return float(1.0 - np.clip(similarity, -1.0, 1.0))


def _softmax_last_axis(values: np.ndarray) -> np.ndarray:
    shifted = values.astype(np.float64) - np.max(values, axis=-1, keepdims=True)
    exp_values = np.exp(shifted)
    return exp_values / np.sum(exp_values, axis=-1, keepdims=True)


def _looks_like_probabilities(values: np.ndarray) -> bool:
    values = values.astype(np.float64)
    if values.shape[-1] < 2 or np.any(values < -1.0e-6):
        return False
    sums = np.sum(values, axis=-1)
    return bool(np.allclose(sums, 1.0, rtol=1.0e-4, atol=1.0e-5))


def _as_probabilities(values: np.ndarray, signal_kind: str) -> np.ndarray:
    if values.ndim < 1 or values.shape[-1] < 2:
        raise ValidationError("distribution metrics require last axis size >= 2")
    if signal_kind == "probabilities":
        probabilities = values.astype(np.float64)
    elif signal_kind == "logits":
        probabilities = _softmax_last_axis(values)
    elif signal_kind == "auto":
        probabilities = values.astype(np.float64) if _looks_like_probabilities(values) else _softmax_last_axis(values)
    else:  # pragma: no cover - argparse prevents this
        raise ValidationError(f"unknown signal_kind: {signal_kind}")
    if np.any(probabilities < -1.0e-8):
        raise ValidationError("probabilities contain negative values")
    probabilities = np.clip(probabilities, EPS, None)
    probabilities /= np.sum(probabilities, axis=-1, keepdims=True)
    return probabilities


def _distribution_rows(
    text_signal: np.ndarray,
    comparison_signal: np.ndarray,
    mask: np.ndarray,
    signal_kind: str,
) -> tuple[np.ndarray, np.ndarray]:
    if text_signal.ndim < 1:
        raise ValidationError("distribution metrics require at least one signal axis")
    row_mask = np.all(mask, axis=-1)
    if not np.any(row_mask):
        raise ValidationError("distribution metrics require at least one fully valid last-axis row")
    text_prob = _as_probabilities(text_signal, signal_kind)[row_mask]
    comparison_prob = _as_probabilities(comparison_signal, signal_kind)[row_mask]
    width = text_signal.shape[-1]
    return text_prob.reshape(-1, width), comparison_prob.reshape(-1, width)


def _kl_rows(p: np.ndarray, q: np.ndarray) -> np.ndarray:
    return np.sum(p * (np.log(p) - np.log(q)), axis=-1)


def _distribution_metric(
    text_signal: np.ndarray,
    comparison_signal: np.ndarray,
    mask: np.ndarray,
    metric_name: str,
    signal_kind: str,
) -> float:
    p, q = _distribution_rows(text_signal, comparison_signal, mask, signal_kind)
    if metric_name == "kl":
        return float(np.mean(_kl_rows(p, q)))
    if metric_name == "js":
        midpoint = 0.5 * (p + q)
        return float(np.mean(0.5 * _kl_rows(p, midpoint) + 0.5 * _kl_rows(q, midpoint)))
    if metric_name == "entropy_change":
        entropy_p = -np.sum(p * np.log(p), axis=-1)
        entropy_q = -np.sum(q * np.log(q), axis=-1)
        return float(np.mean(entropy_p - entropy_q))
    raise ValidationError(f"unsupported distribution metric: {metric_name}")


def compute_metric(
    text_signal: np.ndarray,
    comparison_signal: np.ndarray,
    mask: np.ndarray,
    metric_name: str,
    signal_kind: str,
) -> float:
    if metric_name == "relative_l2":
        return _relative_l2(text_signal, comparison_signal, mask)
    if metric_name == "cosine":
        return _cosine_distance(text_signal, comparison_signal, mask)
    if metric_name in {"js", "kl", "entropy_change"}:
        return _distribution_metric(text_signal, comparison_signal, mask, metric_name, signal_kind)
    raise ValidationError(f"unsupported metric: {metric_name}")


def _compact_json(data: dict[str, Any]) -> str:
    return json.dumps(data, ensure_ascii=True, sort_keys=True, separators=(",", ":"))


def _append_jsonl(path: Path, row: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(_compact_json(row) + "\n")


def compute_delta(args: argparse.Namespace) -> None:
    text_trace = validate_forward_file(args.text_forward)
    comparison_trace = validate_forward_file(args.comparison_forward)
    _check_pair_compatibility(text_trace, comparison_trace)

    text_signal = text_trace.signal.astype(np.float64)
    comparison_signal = comparison_trace.signal.astype(np.float64)
    valid_mask = text_trace.valid_mask & comparison_trace.valid_mask
    delta = text_signal - comparison_signal
    delta[~valid_mask] = 0.0
    metric_value = compute_metric(
        text_signal,
        comparison_signal,
        valid_mask,
        args.metric,
        args.signal_kind,
    )
    if not math.isfinite(metric_value):
        raise ValidationError(f"metric {args.metric} produced a non-finite value")

    condition_pair = args.condition_pair or (
        f"{text_trace.meta['condition_id']}_vs_{comparison_trace.meta['condition_id']}"
    )
    delta_meta = {
        "run_id": text_trace.meta["run_id"],
        "sample_id": text_trace.meta["sample_id"],
        "model": text_trace.meta["model"],
        "model_family": text_trace.meta["model_family"],
        "condition_pair": condition_pair,
        "text_condition_id": text_trace.meta["condition_id"],
        "comparison_condition_id": comparison_trace.meta["condition_id"],
        "z_kind": text_trace.meta["z_kind"],
        "z_id": text_trace.meta["z_id"],
        "f_name": text_trace.meta["f_name"],
        "f_space": text_trace.meta["f_space"],
        "metric_name": args.metric,
        "metric_value": metric_value,
        "source_forward_npz_path": str(text_trace.path),
        "comparison_forward_npz_path": str(comparison_trace.path),
        "role": "diagnostic",
        "used_for": "observation",
        "limitations": "Internal trace delta only; not a final evaluator.",
    }

    args.output_npz.parent.mkdir(parents=True, exist_ok=True)
    np.savez_compressed(
        args.output_npz,
        delta=delta.astype(np.float32),
        metric_value=np.array(metric_value, dtype=np.float64),
        meta_json=np.array(_compact_json(delta_meta)),
        valid_mask=valid_mask,
        axis_names_json=np.array(json.dumps(text_trace.axis_names, ensure_ascii=True)),
    )

    manifest_row = {
        "run_id": delta_meta["run_id"],
        "sample_id": delta_meta["sample_id"],
        "model": delta_meta["model"],
        "condition_pair": condition_pair,
        "z_kind": delta_meta["z_kind"],
        "z_id": delta_meta["z_id"],
        "f_name": delta_meta["f_name"],
        "metric_name": args.metric,
        "metric_value": metric_value,
        "delta_npz_path": str(args.output_npz),
        "role": "diagnostic",
        "used_for": "observation",
        "limitations": delta_meta["limitations"],
    }
    _append_jsonl(args.manifest, manifest_row)
    print(f"OK compute-delta {args.output_npz} metric_value={metric_value:.10g}")


def summarize_manifest(manifest: Path, kind: str, output_tsv: Path) -> None:
    rows = validate_manifest(manifest, kind)
    fields = FORWARD_MANIFEST_REQUIRED if kind == "forward" else DELTA_MANIFEST_REQUIRED
    output_tsv.parent.mkdir(parents=True, exist_ok=True)
    with output_tsv.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, delimiter="\t", extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow(row)
    print(f"OK summarize-manifest rows={len(rows)} output={output_tsv}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    validate_forward = subparsers.add_parser("validate-forward", help="validate a forward NPZ and optional manifest")
    validate_forward.add_argument("--npz", required=True, type=Path)
    validate_forward.add_argument("--manifest", type=Path)

    compute = subparsers.add_parser("compute-delta", help="compute signal_text - signal_comparison")
    compute.add_argument("--text-forward", required=True, type=Path)
    compute.add_argument("--comparison-forward", required=True, type=Path)
    compute.add_argument("--output-npz", required=True, type=Path)
    compute.add_argument("--manifest", required=True, type=Path)
    compute.add_argument("--metric", default="relative_l2", choices=("relative_l2", "cosine", "js", "kl", "entropy_change"))
    compute.add_argument("--signal-kind", default="auto", choices=("auto", "logits", "probabilities"))
    compute.add_argument("--condition-pair")

    validate_delta = subparsers.add_parser("validate-delta", help="validate a delta NPZ and optional manifest")
    validate_delta.add_argument("--npz", required=True, type=Path)
    validate_delta.add_argument("--manifest", type=Path)

    summarize = subparsers.add_parser("summarize-manifest", help="validate JSONL and write a fixed-schema TSV")
    summarize.add_argument("--manifest", required=True, type=Path)
    summarize.add_argument("--kind", required=True, choices=("forward", "delta"))
    summarize.add_argument("--output-tsv", required=True, type=Path)
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        if args.command == "validate-forward":
            trace = validate_forward_file(args.npz)
            if args.manifest:
                rows = validate_manifest(args.manifest, "forward")
                print(f"OK validate-forward npz={args.npz} manifest_rows={len(rows)} shape={trace.signal.shape}")
            else:
                print(f"OK validate-forward npz={args.npz} shape={trace.signal.shape}")
        elif args.command == "compute-delta":
            compute_delta(args)
        elif args.command == "validate-delta":
            meta = validate_delta_file(args.npz)
            if args.manifest:
                rows = validate_manifest(args.manifest, "delta")
                print(
                    f"OK validate-delta npz={args.npz} manifest_rows={len(rows)} "
                    f"metric={meta['metric_name']} value={float(meta['metric_value']):.10g}"
                )
            else:
                print(f"OK validate-delta npz={args.npz} metric={meta['metric_name']}")
        elif args.command == "summarize-manifest":
            summarize_manifest(args.manifest, args.kind, args.output_tsv)
        else:  # pragma: no cover - argparse prevents this
            parser.error(f"unknown command: {args.command}")
    except ValidationError as exc:
        print(f"ERROR {exc}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
