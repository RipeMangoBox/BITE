#!/usr/bin/env python3
"""Serve the C3-25 architecture-view completion and denoising evidence desk."""
from __future__ import annotations

import argparse
import hashlib
import json
import math
from dataclasses import dataclass
from pathlib import Path
from typing import Any


DEFAULT_ROOT = Path("/data/public/ripemangobox/Motion/StoryMotion")
CFG_DIR = "std_cfg1.0_eta0.0"
C325_ID = "v8_1c_c3_25_diag_unified3_105k_seed17_4090g0_20260719"
L0_ID = "v7_38_l0_clean_lr3em5_105k_purefull_seed17_4090g0_20260715"
C325_FULL_GROUP = "c3_25_gradio_full_20260721"
L0_BASELINE_GROUP = "c3_25_gradio_l0_baseline_20260721"
C325_SINGLE_STEP_GROUP = "c3_25_single_step_20260721"
C325_SINGLE_STEP_EVAL_GROUP = "c3_25_single_step_20260721"
PARENT_SCREEN_GROUP = "condition_robustness_standard_n512_20260722"
ARCH_SCREEN_GROUP = "architecture_view_standard_n512_20260723"
ARCH_FULL_GROUP = "architecture_view_gradio_full_r3_20260723"
ARCH_SINGLE_STEP_GROUP = "architecture_view_single_step_r3_20260723"
ARCH_SINGLE_STEP_EVAL_GROUP = "architecture_view_single_step_full4053_20260723"
HVIEW_FULL_ID = "p0_c3_25_unified3_hview_full_0_105k_seed17_4090g0_20260722"
HVIEW_ISOLATED_ID = "p0_c3_25_unified3_hview_isolated_0_105k_seed17_4090g1_20260722"
HVIEW_RUNS = (
    ("H-FULL", HVIEW_FULL_ID),
    ("H-ISOLATED", HVIEW_ISOLATED_ID),
)
HVIEW_CHECKPOINT_SHA256 = {
    HVIEW_FULL_ID: "63c2e96dc685c1b1d447de334c77f1df18867d9b5243b114fbfb857da879999a",
    HVIEW_ISOLATED_ID: "04ad0044870498f1c5a49e9048b02b6792c0b2644cf878df354e299bb53649e4",
}
HUMAN_ONLY_ID = "p0_c3_25_human_only_native_0_105k_seed17_5090g2_20260723"
HUMAN_ONLY_PARENT_SCREEN_GROUP = "parent_heading_backfill_n512_20260724"
HUMAN_ONLY_SCREEN_GROUP = "human_only_learning_curve_n512_r3_20260724"
HUMAN_ONLY_FULL_GROUP = "human_only_learning_curve_gradio_r3_20260724"
HUMAN_ONLY_STEPS = (35006, 58339, 70005, 105000)
HUMAN_ONLY_CHECKPOINT_SHA256 = {
    35006: "0776a69c18df6362450c152b632c66b6a20970697da9d04875af3cbc09bed6bc",
    58339: "e1737608ebe980b3352b9ecf45f0568fb71078b4b07aa3e8959a12c1a1825cb5",
    70005: "86894b7871c23235b45674fb5ddc368f228c59740393bfa8f2bace4c5a39ba2d",
    105000: "84949319ca605c6847ebbbcd71e9e38dc3e2bc8c46dc521e6d11037d9cc679b5",
}
HUMAN_ONLY_VIEW = {
    "mode": "mixed",
    "direct_h": {"latent": "[H_t,C_t]", "text": "[0,e_H]"},
    "joint_h": {"latent": "[H_t,0]", "text": "[0,e_H]"},
    "direct_c": {"latent": "[H_0,C_t]", "text": "[e_C,0]"},
    "joint_c": {"latent": "[H_t,C_t]", "text": "[e_C,e_H]"},
    "task_ids_unchanged": True,
    "task_embeddings_unchanged": True,
}
HVIEW_CONTRACTS = {
    HVIEW_FULL_ID: {
        "mode": "full",
        "direct_h": {"latent": "[H_t,C_t]", "text": "[e_C,e_H]"},
        "joint_h": {"latent": "[H_t,C_t]", "text": "[e_C,e_H]"},
        "direct_c": {"latent": "[H_0,C_t]", "text": "[e_C,0]"},
        "joint_c": {"latent": "[H_t,C_t]", "text": "[e_C,e_H]"},
        "task_ids_unchanged": True,
        "task_embeddings_unchanged": True,
    },
    HVIEW_ISOLATED_ID: {
        "mode": "isolated",
        "direct_h": {"latent": "[H_t,0]", "text": "[0,e_H]"},
        "joint_h": {"latent": "[H_t,0]", "text": "[0,e_H]"},
        "direct_c": {"latent": "[H_0,C_t]", "text": "[e_C,0]"},
        "joint_c": {"latent": "[H_t,C_t]", "text": "[e_C,e_H]"},
        "task_ids_unchanged": True,
        "task_embeddings_unchanged": True,
    },
}
HUMANML_RUN_ID = "v7_40_humanml3d_adapter_vis_20260715"
HUMANML_VIS_GROUP = "humanml3d_stage1_adapted_20260715"
HUMAN_SIXWAY_ID = "human_stage2_sixway_fixed8_r1_seed17_4090g1_20260726"
HUMAN_SIXWAY_ORDERED_IDS_SHA256 = (
    "6b9c92a533d2d0aff76cce6c7ad23361733fb38d3157128bf7eee56cdc33d8df"
)
STAGE1_RECON_ID = "stage1_c3_hanchor_gradio_fixed8_r1_seed17_4090g0_20260727"
STAGE1_PULP_ORDERED_IDS_SHA256 = (
    "a0d7627ee827e36a229d33f9975f8417ae78b504cd5a6db1edf62cb1a9266b93"
)
STAGE1_HML_ORDERED_IDS_SHA256 = (
    "f1db6dc6c0ee2e8b8919d754cfc64657bf5ef5a46d48263c005302a8b93a60f3"
)
V9_PROTECTED_ID = "v9_hanchor_protected_vimogen_u3_diag_seed17_4090g1_20260727"
V9_HUMAN_EVAL_GROUP = "human_teacher_105k_direct_h_n512_20260728"
V9_HUMAN_VIS_GROUP = "human_teacher_105k_direct_h_fixed8_20260728"
V9_UNIFIED_EVAL_GROUPS = {
    "direct_h": "unified_210k_direct_h_n512_r2_20260728",
    "direct_c": "unified_210k_direct_c_n512_20260728",
    "joint_parallel": "unified_210k_joint_parallel_n512_r2_20260728",
}
V9_CAMERA_VIS_GROUP = "unified_210k_direct_c_joint_parallel_fixed8_20260728"
V10_HUMAN_TEACHER_ID = "v10_hrelcam_phasea210k_human_teacher105k_seed17_4090g1_20260729"
V10_HUMAN_COMPARE_GROUP = "gt_hrecon_v10v9_teacher_cfg1_cfg3_fixed8_r4_20260729"
V10_STAGE1_ENDPOINT_CHECKPOINT_SHA256 = (
    "60f7ca14cd9e80f062b67d2eeae340c8f28ff9ed76b613f1529dbdbd57a969fb"
)
V10_HUMAN_TEACHER_CHECKPOINT_SHA256 = (
    "5bd3b06c2078a96d45f7915a3f1bd35cc6ddbc8926d661b9bdc99c56126e3bc4"
)
V9_HUMAN_TEACHER_CHECKPOINT_SHA256 = (
    "3efd59481f8052b401889fce6559e31f96cb88f51dfb6c466464cf05ec6c2c50"
)
V10_HUMAN_OWNER_SHA256 = (
    "aade19d4948e51ae635fb2dec712d1e4e63cef6cd4386f4c1c5b49b55e2493c3"
)
V9_HUMAN_OWNER_SHA256 = (
    "51233f6a032c779e66b6eed4bb22b7f61c41d9b4a5a0a1ffc7dade7d3d86d4df"
)
SINGLE_STEP_TIMESTEPS = (999, 799, 599, 399, 199)
DISPLAY_SAMPLE_IDS = (
    "2015_iL1JlXnbnt0_00000_000_a",
    "2019_vcdDRblTOmM_00038_001_a",
    "2016_4wPqQUl2y5A_00000_000_b",
    "2012_FZ1f-u8RqBU_00008_000_a",
    "2011_kk2HQ0hCGTE_00006_000_a",
    "2016_4MTf0k1vqTk_00016_000_a",
    "2012_OsJKdxPwZdk_00043_000_a",
    "2011_d-kcczAff40_00007_000_a",
)

CSS = """
:root {
  --paper: #ece8de;
  --ink: #202628;
  --muted: #657074;
  --line: #b9b5aa;
  --orange: #d85b32;
  --cyan: #167b82;
}
.gradio-container {
  max-width: 1900px !important;
  color: var(--ink);
  background-color: var(--paper);
  background-image:
    linear-gradient(rgba(32, 38, 40, .035) 1px, transparent 1px),
    linear-gradient(90deg, rgba(32, 38, 40, .035) 1px, transparent 1px);
  background-size: 24px 24px;
  font-family: "IBM Plex Sans", "Avenir Next", sans-serif;
}
#hero {
  border-left: 10px solid var(--orange);
  padding: 4px 0 4px 20px;
  margin-bottom: 8px;
}
#hero h1 { font-family: Charter, Georgia, serif; letter-spacing: -.025em; }
.verdict {
  border: 1px solid var(--line);
  border-top: 5px solid var(--cyan);
  background: rgba(247, 244, 236, .92);
  padding: 12px 16px;
  box-shadow: 5px 5px 0 rgba(32, 38, 40, .08);
}
.metric-strip {
  border: 1px solid var(--line);
  background: rgba(247, 244, 236, .94);
  padding: 10px 14px;
}
.evidence-row { flex-wrap: nowrap !important; gap: 14px; align-items: flex-start; }
.evidence-row > div { min-width: 0 !important; flex: 1 1 calc(33.333% - 10px) !important; }
.evidence-row.two-column-row > div { flex-basis: calc(50% - 7px) !important; }
.evidence-row video {
  background: #151b1d;
  aspect-ratio: 16 / 10;
  object-fit: contain;
  border-radius: 2px !important;
}
.sync-play { max-width: 240px; margin: 4px 0 12px; }
button.primary { background: var(--orange) !important; border-color: var(--orange) !important; }
@media (max-width: 780px) {
  .evidence-row { flex-wrap: wrap !important; }
  .evidence-row > div { flex-basis: 100% !important; }
}
"""

SYNC_PLAY_JS = """() => {
  const videos = [...document.querySelectorAll('video')].filter((video) => video.offsetParent !== null);
  videos.forEach((video) => { video.pause(); video.currentTime = 0; });
  Promise.allSettled(videos.map((video) => video.play()));
  return [];
}"""


@dataclass(frozen=True)
class Evidence:
    root: Path

    def legacy_run(self, run_id: str) -> Path:
        return self.root / "runs" / "stage2" / run_id

    def canonical_eval(self, run_id: str) -> Path:
        return self.root / "runs" / "eval" / "stage2" / run_id

    def canonical_vis(self, run_id: str) -> Path:
        return self.root / "runs" / "vis" / "stage2" / run_id

    def c325_metric(self, task: str) -> Path:
        return self.canonical_eval(C325_ID) / "formal_105k" / f"{task}.json"

    def l0_metric(self, task: str) -> Path:
        return self.legacy_run(L0_ID) / "eval" / "official_pure4053_matched" / f"{task}.json"

    def c325_geometry(self) -> Path:
        return self.canonical_eval(C325_ID) / "paired_geometry_105k" / "joint_parallel.json"

    def full_vis(self, run_id: str, group: str) -> Path:
        return self.canonical_vis(run_id) / group / CFG_DIR

    def c325_single_step_vis(self) -> Path:
        return self.canonical_vis(C325_ID) / C325_SINGLE_STEP_GROUP

    def c325_single_step_metric(self, task: str, timestep: int) -> Path:
        return (
            self.canonical_eval(C325_ID)
            / C325_SINGLE_STEP_EVAL_GROUP
            / task
            / f"t{timestep}.json"
        )

    def screen_metric(self, run_id: str, profile: str) -> Path:
        group = PARENT_SCREEN_GROUP if run_id == C325_ID else ARCH_SCREEN_GROUP
        return self.canonical_eval(run_id) / group / f"{profile}.json"

    def screen_manifest(self, run_id: str) -> Path:
        group = PARENT_SCREEN_GROUP if run_id == C325_ID else ARCH_SCREEN_GROUP
        return self.canonical_eval(run_id) / group / "screen_manifest.json"

    def architecture_full_vis(self, run_id: str) -> Path:
        return self.full_vis(run_id, ARCH_FULL_GROUP)

    def architecture_single_step_vis(self, run_id: str) -> Path:
        return self.canonical_vis(run_id) / ARCH_SINGLE_STEP_GROUP

    def architecture_single_step_metric(self, run_id: str, task: str, timestep: int) -> Path:
        return (
            self.canonical_eval(run_id)
            / ARCH_SINGLE_STEP_EVAL_GROUP
            / task
            / f"t{timestep}.json"
        )

    def architecture_single_step_manifest(self, run_id: str) -> Path:
        return (
            self.canonical_eval(run_id)
            / ARCH_SINGLE_STEP_EVAL_GROUP
            / "single_step_manifest.json"
        )

    def human_only_metric(self, step: int) -> Path:
        return (
            self.canonical_eval(HUMAN_ONLY_ID)
            / HUMAN_ONLY_SCREEN_GROUP
            / f"step_{step}"
            / "direct_h.json"
        )

    def human_only_parent_metric(self) -> Path:
        return (
            self.canonical_eval(C325_ID)
            / HUMAN_ONLY_PARENT_SCREEN_GROUP
            / "direct_h.json"
        )

    def human_only_parent_screen_manifest(self) -> Path:
        return (
            self.canonical_eval(C325_ID)
            / HUMAN_ONLY_PARENT_SCREEN_GROUP
            / "screen_manifest.json"
        )

    def human_only_screen_manifest(self) -> Path:
        return self.canonical_eval(HUMAN_ONLY_ID) / HUMAN_ONLY_SCREEN_GROUP / "screen_manifest.json"

    def human_only_full_vis(self, step: int) -> Path:
        return (
            self.canonical_vis(HUMAN_ONLY_ID)
            / HUMAN_ONLY_FULL_GROUP
            / f"step_{step}"
            / CFG_DIR
        )

    def humanml_summary(self) -> Path:
        return (
            self.root
            / "runs"
            / "stage1"
            / HUMANML_RUN_ID
            / "vis"
            / HUMANML_VIS_GROUP
            / "render_summary.json"
        )

    def human_sixway_root(self) -> Path:
        return self.canonical_vis(HUMAN_SIXWAY_ID)

    def human_sixway_manifest(self) -> Path:
        return self.human_sixway_root() / "manifest.json"

    def stage1_recon_root(self) -> Path:
        return self.root / "runs" / "vis" / "stage1" / STAGE1_RECON_ID

    def stage1_recon_manifest(self) -> Path:
        return self.stage1_recon_root() / "manifest.json"

    def v9_eval_result(self, group: str) -> Path:
        return self.canonical_eval(V9_PROTECTED_ID) / group / "results.json"

    def v9_human_vis_root(self) -> Path:
        return self.canonical_vis(V9_PROTECTED_ID) / V9_HUMAN_VIS_GROUP

    def v9_camera_vis_root(self) -> Path:
        return self.canonical_vis(V9_PROTECTED_ID) / V9_CAMERA_VIS_GROUP

    def v10_human_compare_root(self) -> Path:
        return self.canonical_vis(V10_HUMAN_TEACHER_ID) / V10_HUMAN_COMPARE_GROUP

    def v10_human_compare_manifest(self) -> Path:
        return self.v10_human_compare_root() / "visual_manifest.json"


def load_json(path: Path) -> dict[str, Any]:
    if not path.is_file():
        raise FileNotFoundError(f"missing required artifact: {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def ordered_record_ids_sha256(path: Path, expected_count: int = 512) -> str:
    digest = hashlib.sha256()
    count = 0
    with path.open(encoding="utf-8") as handle:
        for index, line in enumerate(handle):
            record = json.loads(line)
            if record.get("sample_index") != index:
                raise RuntimeError(f"non-contiguous sample_index in {path}")
            sample_id = record.get("sample_id")
            if not isinstance(sample_id, str) or not sample_id:
                raise RuntimeError(f"missing sample_id in {path} at index {index}")
            digest.update(sample_id.encode("utf-8"))
            digest.update(b"\n")
            count += 1
    if count != expected_count:
        raise RuntimeError(f"expected {expected_count} records in {path}, found {count}")
    return digest.hexdigest()


def existing(path: Path) -> str | None:
    return str(path) if path.is_file() else None


def evidence_path(ev: Evidence, value: str) -> Path:
    path = Path(value)
    return path if path.is_absolute() else ev.root / path


def metric(payload: dict[str, Any], key: str) -> float:
    value = payload.get("metrics", {}).get(key)
    return float(value) if value is not None else float("nan")


def geometry_metric(payload: dict[str, Any], key: str) -> float:
    value = payload.get("paired_geometry", {}).get("overall_mean", {}).get(key)
    return float(value) if value is not None else float("nan")


def number(value: float, digits: int = 3, percent: bool = False) -> str:
    if not math.isfinite(value):
        return "N/A"
    if percent:
        return f"{100 * value:.2f}%"
    return f"{value:.{digits}f}"


def eval_scope(payload: dict[str, Any]) -> tuple[str, int]:
    split = str(payload.get("split", "test"))
    count = int(payload.get("evaluated_samples", payload.get("samples", 4053)))
    return split, count


def architecture_screen_payloads(
    ev: Evidence,
    profile: str,
) -> list[tuple[str, str, dict[str, Any]]]:
    return [
        ("Parent C3-105K", C325_ID, load_json(ev.screen_metric(C325_ID, profile))),
        ("H-FULL-105K", HVIEW_FULL_ID, load_json(ev.screen_metric(HVIEW_FULL_ID, profile))),
        (
            "H-ISOLATED-105K",
            HVIEW_ISOLATED_ID,
            load_json(ev.screen_metric(HVIEW_ISOLATED_ID, profile)),
        ),
    ]


def completion_metrics(ev: Evidence, task: str) -> str:
    profile = "direct_h" if task == "human" else "direct_c_clean_h"
    payloads = architecture_screen_payloads(ev, profile)
    split, count = eval_scope(payloads[0][2])
    if task == "human":
        header = (
            "| version / run | FDTMR↓ | TMR↑ | HCov↑ | H global MPJPE↓ |",
            "| --- | ---: | ---: | ---: | ---: |",
        )
        rows = [
            f"| {label} / `{run_id}` | {number(metric(payload, 'test/tmr/ftd'), 2)} | "
            f"{number(metric(payload, 'test/tmr/tmr_score'))} | "
            f"{number(metric(payload, 'test/tmr/coverage'), percent=True)} | "
            f"{number(geometry_metric(payload, 'human_global_mpjpe'), 4)} |"
            for label, run_id, payload in payloads
        ]
        contract = (
            "H-FULL gives Direct-H and joint-H full Camera latent/text context; "
            "H-ISOLATED removes Camera latent/text from both Human slices."
        )
    else:
        header = (
            "| version / run | FDCLaTr↓ | CLaTr↑ | CCov↑ | Caption F1↑ | Cam-ADE↓ |",
            "| --- | ---: | ---: | ---: | ---: | ---: |",
        )
        rows = [
            f"| {label} / `{run_id}` | {number(metric(payload, 'test/clatr/fcd'), 2)} | "
            f"{number(metric(payload, 'test/clatr/clatr_score'))} | "
            f"{number(metric(payload, 'test/clatr/coverage'), percent=True)} | "
            f"{number(metric(payload, 'test/captions/fscore'))} | "
            f"{number(geometry_metric(payload, 'camera_center_ade'), 3)} |"
            for label, run_id, payload in payloads
        ]
        contract = (
            "All three rows retain the mainline Direct-C view: clean GT-H plus Camera text, "
            "Camera-only loss, and the same GT Human for projection."
        )
    return "\n".join(
        [
            f"**Architecture screen only · `{split}` first {count:,} ordered samples · DDIM50 · CFG1 · η0 · seed17**",
            "",
            *header,
            *rows,
            "",
            contract,
            "The v7.38 L0 media row is retained as historical visual context but is not mixed into this matched N=512 table. "
            "C3-105K remains the formal mainline.",
        ]
    )


def joint_metrics(ev: Evidence) -> str:
    payloads = architecture_screen_payloads(ev, "joint_parallel")
    split, count = eval_scope(payloads[0][2])
    rows = []
    for label, run_id, payload in payloads:
        rows.append(
            f"| {label} / `{run_id}` | {number(metric(payload, 'test/tmr/ftd'), 2)} | "
            f"{number(metric(payload, 'test/tmr/tmr_score'))} | "
            f"{number(metric(payload, 'test/tmr/coverage'), percent=True)} | "
            f"{number(metric(payload, 'test/clatr/fcd'), 2)} | "
            f"{number(metric(payload, 'test/clatr/clatr_score'))} | "
            f"{number(metric(payload, 'test/clatr/coverage'), percent=True)} | "
            f"{number(metric(payload, 'test/captions/fscore'))} | "
            f"{number(metric(payload, 'test/proj/outscreen'), percent=True)} | "
            f"{number(geometry_metric(payload, 'human_global_mpjpe'), 4)} | "
            f"{number(geometry_metric(payload, 'camera_center_ade'), 3)} |"
        )
    return "\n".join(
        [
            f"**Joint parallel architecture screen only · `{split}` first {count:,} ordered samples · DDIM50 · CFG1 · η0 · seed17**",
            "",
            "| version / run | H FDTMR↓ | H TMR↑ | HCov↑ | C FDCLaTr↓ | C CLaTr↑ | CCov↑ | F1↑ | Out↓ | H global↓ | Cam-ADE↓ |",
            "| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
            *rows,
            "",
            "Top-5 IDs remain frozen from the parent C3-25 paired-geometry ranking and are reused for both arms. "
            "They are a best-case diagnostic, not a blind or random qualitative estimate.",
        ]
    )


def single_step_metrics(ev: Evidence, task: str) -> str:
    payloads = [
        (
            timestep,
            load_json(ev.c325_single_step_metric(task, timestep)),
        )
        for timestep in SINGLE_STEP_TIMESTEPS
    ]
    split, count = eval_scope(payloads[0][1])
    if task == "human":
        header = (
            "| version / run | FDTMR↓ | TMR↑ | HCov↑ | H global↓ (m) | H RA↓ (m) |",
            "| --- | ---: | ---: | ---: | ---: | ---: |",
        )
        rows = [
            f"| C3-25 / `{C325_ID}` / t={timestep} | {number(metric(payload, 'test/tmr/ftd'), 2)} | "
            f"{number(metric(payload, 'test/tmr/tmr_score'))} | "
            f"{number(metric(payload, 'test/tmr/coverage'), percent=True)} | "
            f"{number(geometry_metric(payload, 'human_global_mpjpe'), 4)} | "
            f"{number(geometry_metric(payload, 'human_root_aligned_mpjpe'), 4)} |"
            for timestep, payload in payloads
        ]
    elif task == "camera":
        header = (
            "| version / run | FDCLaTr↓ | CLaTr↑ | CCov↑ | Caption F1↑ | Cam-ADE↓ (m) | Rot↓ (°) |",
            "| --- | ---: | ---: | ---: | ---: | ---: | ---: |",
        )
        rows = [
            f"| C3-25 / `{C325_ID}` / t={timestep} | {number(metric(payload, 'test/clatr/fcd'), 2)} | "
            f"{number(metric(payload, 'test/clatr/clatr_score'))} | "
            f"{number(metric(payload, 'test/clatr/coverage'), percent=True)} | "
            f"{number(metric(payload, 'test/captions/fscore'))} | "
            f"{number(geometry_metric(payload, 'camera_center_ade'), 4)} | "
            f"{number(geometry_metric(payload, 'camera_rotation_deg'), 3)} |"
            for timestep, payload in payloads
        ]
    else:
        header = (
            "| version / run | H FDTMR↓ | H TMR↑ | HCov↑ | C FDCLaTr↓ | C CLaTr↑ | CCov↑ | F1↑ | Out↓ | H global↓ (m) | Cam-ADE↓ (m) | Rot↓ (°) |",
            "| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
        )
        rows = [
            f"| C3-25 / `{C325_ID}` / t={timestep} | {number(metric(payload, 'test/tmr/ftd'), 2)} | "
            f"{number(metric(payload, 'test/tmr/tmr_score'))} | "
            f"{number(metric(payload, 'test/tmr/coverage'), percent=True)} | "
            f"{number(metric(payload, 'test/clatr/fcd'), 2)} | "
            f"{number(metric(payload, 'test/clatr/clatr_score'))} | "
            f"{number(metric(payload, 'test/clatr/coverage'), percent=True)} | "
            f"{number(metric(payload, 'test/captions/fscore'))} | "
            f"{number(metric(payload, 'test/proj/outscreen'), percent=True)} | "
            f"{number(geometry_metric(payload, 'human_global_mpjpe'), 4)} | "
            f"{number(geometry_metric(payload, 'camera_center_ade'), 4)} | "
            f"{number(geometry_metric(payload, 'camera_rotation_deg'), 3)} |"
            for timestep, payload in payloads
        ]
    return "\n".join(
        [
            f"**C3-25 teacher-forced single-step metrics · `{split}` · {count:,} samples**",
            "",
            *header,
            *rows,
            "",
            "H-FULL and H-ISOLATED are shown below as render-only groups; their full-4053 "
            "single-step metric grids are not complete and are therefore not reported.",
            "Each row is `q(z_gt,t) → one pred_x0` with deterministic per-sample noise. "
            "It is not DDIM50 generation or a training curve, and it does not replace the formal mainline metrics.",
            "At high noise, TMR must be read jointly with FDTMR and coverage; a high scalar with collapsed coverage is not an improvement.",
        ]
    )


def human_only_metrics(ev: Evidence) -> str:
    payloads = [
        ("Parent C3-105K", C325_ID, load_json(ev.human_only_parent_metric())),
        *[
            (f"Human-only step {step:,}", HUMAN_ONLY_ID, load_json(ev.human_only_metric(step)))
            for step in HUMAN_ONLY_STEPS
        ],
    ]
    split, count = eval_scope(payloads[0][2])
    rows = [
        f"| {label} / `{run_id}` | {number(metric(payload, 'test/tmr/ftd'), 2)} | "
        f"{number(metric(payload, 'test/tmr/tmr_score'))} | "
        f"{number(metric(payload, 'test/tmr/coverage'), percent=True)} | "
        f"{number(geometry_metric(payload, 'human_global_mpjpe'), 4)} | "
        f"{number(geometry_metric(payload, 'human_root_aligned_mpjpe'), 4)} | "
        f"{number(geometry_metric(payload, 'human_root_ade'), 4)} | "
        f"{number(geometry_metric(payload, 'human_integrated_yaw_geodesic_deg'), 2)} |"
        for label, run_id, payload in payloads
    ]
    return "\n".join(
        [
            f"**Human-only learning-curve screen · `{split}` first {count:,} ordered samples · DDIM50 · CFG1 · η0 · seed17**",
            "",
            "| version / run | FDTMR↓ | TMR↑ | HCov↑ | H global↓ (m) | H RA↓ (m) | Root ADE↓ (m) | mean yaw↓ (°) |",
            "| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
            *rows,
            "",
            "All rows use the same ordered IDs and sampler. Human-only uses the native 192D network "
            "with Direct-H `[H_t,C_t] + [0,e_H]`; it never trains Camera or joint outputs.",
            "This is screen-only evidence: global/root-trajectory geometry improves, root-aligned "
            "pose does not beat Parent, and distribution/semantic metrics remain substantially behind.",
        ]
    )


def ranked_joint_records(payload: dict[str, Any]) -> list[dict[str, Any]]:
    records = [
        record
        for record in payload["paired_geometry"]["records"]
        if math.isfinite(float(record["human_root_aligned_mpjpe"]))
        and math.isfinite(float(record["camera_center_ade"]))
    ]
    human_order = sorted(records, key=lambda record: float(record["human_root_aligned_mpjpe"]))
    camera_order = sorted(records, key=lambda record: float(record["camera_center_ade"]))
    denominator = max(len(records) - 1, 1)
    human_rank = {str(record["sample_id"]): index / denominator for index, record in enumerate(human_order)}
    camera_rank = {str(record["sample_id"]): index / denominator for index, record in enumerate(camera_order)}
    for record in records:
        sample_id = str(record["sample_id"])
        record["joint_rank_score"] = (human_rank[sample_id] + camera_rank[sample_id]) / 2
    return sorted(records, key=lambda record: (float(record["joint_rank_score"]), str(record["sample_id"])))[:5]


def render_ids(ev: Evidence) -> list[str]:
    top_ids = [str(record["sample_id"]) for record in ranked_joint_records(load_json(ev.c325_geometry()))]
    return list(dict.fromkeys([*DISPLAY_SAMPLE_IDS, *top_ids]))


def summary_index(payload: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {str(item["sample_id"]): item for item in payload["samples"]}


def summary_ids(payload: dict[str, Any]) -> list[str]:
    return [str(item["sample_id"]) for item in payload["samples"]]


def caption(item: dict[str, Any]) -> tuple[str, str, int | None]:
    return (
        str(item.get("human_text", "")),
        str(item.get("camera_text", "")),
        item.get("valid_frames"),
    )


def full_video(ev: Evidence, run_id: str, group: str, sample_id: str, task: str, view: str) -> str | None:
    suffix = "camera_projection.mp4" if view == "Camera projection" else "skeleton.mp4"
    return existing(ev.full_vis(run_id, group) / sample_id / f"{task}_{suffix}")


def gt_video(ev: Evidence, run_id: str, group: str, sample_id: str, view: str) -> str | None:
    suffix = "camera_projection.mp4" if view == "Camera projection" else "skeleton.mp4"
    return existing(ev.full_vis(run_id, group) / sample_id / f"gt_{suffix}")


def completion_view(ev: Evidence, c325_index: dict[str, dict[str, Any]], sample_id: str, task: str):
    human_text, camera_text, frames = caption(c325_index[sample_id])
    view = "World skeleton" if task == "human" else "Camera projection"
    source = (
        "C3-25 uses its mainline Direct-H view; H-FULL consumes full Camera latent plus dual text; "
        "H-ISOLATED consumes zero Camera latent plus Human-only text."
        if task == "human"
        else "All three architecture rows retain GT-H plus Camera-only text; every camera is rendered on the same GT Human."
    )
    status = (
        f"### `{sample_id}` · {frames} frames · {view}\n\n"
        f"**Human text:** {human_text or 'unavailable'}  \n"
        f"**Camera text:** {camera_text or 'unavailable'}  \n{source}"
    )
    return [
        completion_metrics(ev, task),
        status,
        gt_video(ev, C325_ID, C325_FULL_GROUP, sample_id, view),
        full_video(ev, C325_ID, C325_FULL_GROUP, sample_id, task, view),
        full_video(ev, L0_ID, L0_BASELINE_GROUP, sample_id, task, view),
        gt_video(ev, C325_ID, C325_FULL_GROUP, sample_id, view),
        full_video(ev, C325_ID, C325_FULL_GROUP, sample_id, task, view),
        full_video(ev, HVIEW_FULL_ID, ARCH_FULL_GROUP, sample_id, task, view),
        gt_video(ev, C325_ID, C325_FULL_GROUP, sample_id, view),
        full_video(ev, C325_ID, C325_FULL_GROUP, sample_id, task, view),
        full_video(ev, HVIEW_ISOLATED_ID, ARCH_FULL_GROUP, sample_id, task, view),
    ]


def joint_view(
    ev: Evidence,
    c325_index: dict[str, dict[str, Any]],
    ranking: dict[str, dict[str, Any]],
    sample_id: str,
):
    item = c325_index[sample_id]
    record = ranking[sample_id]
    human_text, camera_text, frames = caption(item)
    status = (
        f"### Joint Top-5 · `{sample_id}` · {frames} frames\n\n"
        f"**Human text:** {human_text or 'unavailable'}  \n"
        f"**Camera text:** {camera_text or 'unavailable'}  \n"
        f"**C3 paired geometry:** H RA-MPJPE `{float(record['human_root_aligned_mpjpe']):.4f} m` · "
        f"Cam-ADE `{float(record['camera_center_ade']):.4f} m` · "
        f"mean rank `{float(record['joint_rank_score']):.5f}`."
    )
    return [
        joint_metrics(ev),
        status,
        gt_video(ev, C325_ID, C325_FULL_GROUP, sample_id, "Camera projection"),
        gt_video(ev, C325_ID, C325_FULL_GROUP, sample_id, "World skeleton"),
        full_video(ev, C325_ID, C325_FULL_GROUP, sample_id, "joint", "Camera projection"),
        full_video(ev, C325_ID, C325_FULL_GROUP, sample_id, "joint", "World skeleton"),
        full_video(ev, L0_ID, L0_BASELINE_GROUP, sample_id, "joint", "Camera projection"),
        full_video(ev, L0_ID, L0_BASELINE_GROUP, sample_id, "joint", "World skeleton"),
        full_video(ev, HVIEW_FULL_ID, ARCH_FULL_GROUP, sample_id, "joint", "Camera projection"),
        full_video(ev, HVIEW_FULL_ID, ARCH_FULL_GROUP, sample_id, "joint", "World skeleton"),
        full_video(ev, HVIEW_ISOLATED_ID, ARCH_FULL_GROUP, sample_id, "joint", "Camera projection"),
        full_video(ev, HVIEW_ISOLATED_ID, ARCH_FULL_GROUP, sample_id, "joint", "World skeleton"),
    ]


def single_step_view(
    ev: Evidence,
    single_index: dict[str, dict[str, Any]],
    sample_id: str,
    task: str,
    view: str,
):
    human_text, camera_text, frames = caption(single_index[sample_id])
    suffix = "camera_projection.mp4" if view == "Camera projection" else "skeleton.mp4"
    source = {
        "human": "Each six-video group uses that run's frozen Human view; projection uses GT camera only as an external view.",
        "camera": "Each group predicts Camera from that run's Direct-C view; the two Human-view arms retain the mainline Direct-C binding.",
        "joint": "Each group predicts H/C in one teacher-forced forward using that run's frozen joint view.",
    }[task]
    status = (
        f"### `{sample_id}` · {frames} frames · `{task}` · {view}\n\n"
        f"**Human text:** {human_text or 'unavailable'}  \n"
        f"**Camera text:** {camera_text or 'unavailable'}  \n{source}"
    )
    roots = [
        ev.c325_single_step_vis() / task / sample_id,
        ev.architecture_single_step_vis(HVIEW_FULL_ID) / task / sample_id,
        ev.architecture_single_step_vis(HVIEW_ISOLATED_ID) / task / sample_id,
    ]
    videos: list[str | None] = []
    for task_root in roots:
        videos.extend(
            [
                existing(task_root / f"gt_{suffix}"),
                *[
                    existing(task_root / f"t{timestep}_{suffix}")
                    for timestep in SINGLE_STEP_TIMESTEPS
                ],
            ]
        )
    return [
        single_step_metrics(ev, task),
        status,
        *videos,
    ]


def human_only_view(
    ev: Evidence,
    c325_index: dict[str, dict[str, Any]],
    sample_id: str,
):
    human_text, camera_text, frames = caption(c325_index[sample_id])
    status = (
        f"### `{sample_id}` · {frames} frames · Human-only learning curve\n\n"
        f"**Human text:** {human_text or 'unavailable'}  \n"
        f"**Paired Camera text (display context only):** {camera_text or 'unavailable'}  \n"
        "Human-only is the native 192D `[H_t,C_t] + [0,e_H]` Direct-H task. "
        "No Camera or joint output from this run is displayed."
    )
    return [
        human_only_metrics(ev),
        status,
        gt_video(ev, C325_ID, C325_FULL_GROUP, sample_id, "World skeleton"),
        full_video(ev, C325_ID, C325_FULL_GROUP, sample_id, "human", "World skeleton"),
        *[
            existing(ev.human_only_full_vis(step) / sample_id / "human_skeleton.mp4")
            for step in HUMAN_ONLY_STEPS
        ],
    ]


def humanml_view(ev: Evidence, payload: dict[str, Any], sample_id: str):
    item = next(record for record in payload["samples"] if str(record["sample_id"]) == sample_id)
    status = (
        f"### HumanML3D `{sample_id}` · {item['num_frames']} frames · fixed camera\n\n"
        f"**Text:** {item['caption']}  \n"
        "This is a Stage1 adapter diagnostic retained outside the C3-25 Stage2 evidence tabs."
    )
    return [
        status,
        existing(evidence_path(ev, item["fixed_camera_video"])),
        existing(evidence_path(ev, item["stage1_recon_fixed_camera_video"])),
    ]


def human_sixway_view(ev: Evidence, payload: dict[str, Any], sample_id: str):
    item = next(record for record in payload["records"] if str(record["sample_id"]) == sample_id)
    videos = item["videos"]
    status = (
        f"### Fixed-ID #{payload['sample_ids'].index(sample_id) + 1} · `{sample_id}` · "
        f"{item['valid_frames']} raw frames\n\n"
        f"**Human text:** {item['human_text'] or 'unavailable'}  \n"
        "六路均使用同一 Pulp sample 和 raw-length。GT、Stage1 reconstruction、C3-25 "
        "共享 C3-25 owning non-causal decoder；MARDM 与两条 ViMoGen-light 读取各自 "
        "105K fixed-sample artifact。播放键会把当前六个视频同时归零并启动。"
    )
    return [
        status,
        *[
            existing(evidence_path(ev, videos[key]["path"]))
            for key in (
                "gt",
                "stage1_recon",
                "c3_25",
                "mardm",
                "vimogen_clip",
                "vimogen_t5",
            )
        ],
    ]


def stage1_recon_view(
    ev: Evidence,
    payload: dict[str, Any],
    group_name: str,
    sample_id: str,
):
    group = payload["groups"][group_name]
    item = next(record for record in group["records"] if str(record["sample_id"]) == sample_id)
    videos = item["videos"]
    if group_name == "pulp":
        order = ("gt", "c3_25", "redesign_pulp", "redesign_hml_pulp")
        scope = (
            "Pulp full Human199 + Camera14；每路同时展示 global skeleton / owning Camera "
            "与 projective geometry。四路共享 sample、raw length 与 render context。"
        )
    else:
        order = ("gt", "redesign_pulp", "redesign_hml_pulp")
        scope = (
            "HumanML3D root/local-only；rot6D channels 4:136 为 Pulp-mean imputation，"
            "未参与 HML supervision 或评价。三路共享 sample、raw length 与 render context。"
        )
    status = (
        f"### Fixed-ID #{group['sample_ids'].index(sample_id) + 1} · `{sample_id}` · "
        f"{item['valid_frames']} raw frames\n\n"
        f"{scope} 所有 Stage1 source 均显式 `is_causal=false`；播放键会把当前组视频同时归零并启动。"
    )
    return [
        status,
        *[existing(evidence_path(ev, videos[key]["path"])) for key in order],
    ]


def v10_human_compare_view(
    ev: Evidence,
    payload: dict[str, Any],
    sample_id: str,
):
    item = next(
        record for record in payload["records"] if str(record["sample_id"]) == sample_id
    )
    index = payload["sample_ids"].index(sample_id)
    videos = item["videos"]
    status = (
        f"### Fixed-ID #{index + 1} · `{sample_id}` · {item['valid_frames']} raw frames\n\n"
        "**GT：** Pulp pure-test reference。  \n"
        "**H recon：** v10 Phase-A `210K` frozen Human owner；文件来自完成的 Phase-B "
        "旧三项 loss `210K` endpoint round trip；这里只使用未改变的 Human block，不作为 "
        "Camera 证据。  \n"
        "**v10 teacher CFG1 / CFG3：** Phase-A `210K` Human owner（`aade19d4…`）上的同一个 "
        "Human-text-only ViMoGen-light EMA `105K`；两列只改变 inference CFG。  \n"
        "**v9 teacher CFG1 / CFG3：** Phase-C `636K` Human owner（`51233f6a…`）上的同一个 "
        "EMA `105K`；两列也只改变 inference CFG。v9/v10 latent cache / train-only "
        "normalization 不同，不能复用权重。  \n"
        "六路使用相同 ID、raw length 与 world display bounds；本页不包含 v10 Camera "
        "generation、Direct-C 或 joint evidence。"
    )
    return [
        status,
        *[
            existing(evidence_path(ev, videos[key]["path"]))
            for key in (
                "gt",
                "human_reconstruction",
                "v10_human_teacher_cfg1",
                "v9_human_teacher_cfg1",
                "v10_human_teacher_cfg3",
                "v9_human_teacher_cfg3",
            )
        ],
    ]


def v9_protected_view(
    ev: Evidence,
    human_vis: dict[str, Any],
    camera_vis: dict[str, Any],
    sample_id: str,
):
    human_index, human = next(
        (index, record)
        for index, record in enumerate(human_vis["paired_records"])
        if record["sample_id"] == sample_id
    )
    blind = human_vis["blind_records"][human_index]
    camera = next(
        record for record in camera_vis["records"] if record["sample_id"] == sample_id
    )
    status = (
        f"### Fixed-ID #{human_index + 1} · `{sample_id}` · {human['valid_frames']} raw frames\n\n"
        "**Human Stage:** 105K teacher endpoint，Direct-H N=512 eval + fixed-8 vis 已完成；"
        f"盲看编号 `{blind['anonymous_id']}`。  \n"
        "**Camera Stage:** Unified-3 210K endpoint，Direct-H / Direct-C / joint-parallel "
        "N=512 eval 已完成；视频并列 Ground truth、Direct-C 与 joint-parallel。"
    )
    return [
        status,
        existing(evidence_path(ev, human["video"])),
        existing(evidence_path(ev, blind["video"])),
        existing(evidence_path(ev, camera["video"])),
    ]


def v9_eval_metrics(ev: Evidence) -> str:
    human = load_json(ev.v9_eval_result(V9_HUMAN_EVAL_GROUP))
    direct_h = load_json(ev.v9_eval_result(V9_UNIFIED_EVAL_GROUPS["direct_h"]))
    direct_c = load_json(ev.v9_eval_result(V9_UNIFIED_EVAL_GROUPS["direct_c"]))
    joint = load_json(ev.v9_eval_result(V9_UNIFIED_EVAL_GROUPS["joint_parallel"]))

    def value(payload: dict[str, Any], task: str, key: str) -> float:
        result = payload.get("official_metrics", {}).get(task, {}).get(key)
        return float(result) if result is not None else float("nan")

    rows = (
        (
            "Human teacher 105K · Direct-H",
            human,
            "human",
            None,
        ),
        ("Unified 210K · Direct-C", direct_c, None, "camera"),
        ("Unified 210K · joint-parallel", joint, "joint", "joint"),
    )
    table = []
    for label, payload, human_task, camera_task in rows:
        table.append(
            f"| v9 / `{V9_PROTECTED_ID}` / {label} | "
            f"{number(value(payload, human_task, 'test/tmr/ftd'), 2) if human_task else 'N/A'} | "
            f"{number(value(payload, human_task, 'test/tmr/tmr_score')) if human_task else 'N/A'} | "
            f"{number(value(payload, camera_task, 'test/clatr/fcd'), 2) if camera_task else 'N/A'} | "
            f"{number(value(payload, camera_task, 'test/clatr/clatr_score')) if camera_task else 'N/A'} | "
            f"{number(value(payload, camera_task, 'test/captions/fscore')) if camera_task else 'N/A'} |"
        )
    return "\n".join(
        [
            "**Diagnostic-only · pure-test N=512 · Euler50 · seed17 · non-causal owning decoder**",
            "",
            "| version / run / mode | H FTD↓ | H TMR↑ | C FCD↓ | C CLaTr↑ | Caption F1↑ |",
            "| --- | ---: | ---: | ---: | ---: | ---: |",
            *table,
            "",
            f"Final Unified Direct-H protected routing max abs: "
            f"`{direct_h['direct_h_exact_regression_max_abs']}`; Human parameter state exact: "
            f"`{str(direct_h['checkpoint']['human_parameter_state_exact']).lower()}`.",
        ]
    )


def validate(ev: Evidence) -> dict[str, Any]:
    expected_ids = render_ids(ev)
    c325_summary = load_json(ev.full_vis(C325_ID, C325_FULL_GROUP) / "render_summary.json")
    l0_summary = load_json(ev.full_vis(L0_ID, L0_BASELINE_GROUP) / "render_summary.json")
    single_summary = load_json(ev.c325_single_step_vis() / "render_summary.json")
    architecture_full = {
        run_id: load_json(ev.architecture_full_vis(run_id) / "render_summary.json")
        for _, run_id in HVIEW_RUNS
    }
    architecture_single = {
        run_id: load_json(ev.architecture_single_step_vis(run_id) / "render_summary.json")
        for _, run_id in HVIEW_RUNS
    }
    human_only_full = {
        step: load_json(ev.human_only_full_vis(step) / "render_summary.json")
        for step in HUMAN_ONLY_STEPS
    }
    human_sixway = load_json(ev.human_sixway_manifest())
    stage1_recon = load_json(ev.stage1_recon_manifest())
    v9_human_vis = load_json(ev.v9_human_vis_root() / "visual_manifest.json")
    v9_camera_vis = load_json(ev.v9_camera_vis_root() / "visual_manifest.json")
    v10_human_compare = load_json(ev.v10_human_compare_manifest())
    v9_eval_results = {
        "human_teacher": load_json(ev.v9_eval_result(V9_HUMAN_EVAL_GROUP)),
        **{
            mode: load_json(ev.v9_eval_result(group))
            for mode, group in V9_UNIFIED_EVAL_GROUPS.items()
        },
    }
    for name, payload in v9_eval_results.items():
        if payload.get("status") != "evaluated" or payload.get("samples") != 512:
            raise RuntimeError(f"v9 {name} N=512 evaluation is incomplete")
    if (
        v9_human_vis.get("status") != "rendered"
        or v9_human_vis.get("samples") != 8
        or v9_human_vis.get("is_causal") is not False
    ):
        raise RuntimeError("v9 Human fixed-8 visualization is incomplete or causal")
    if (
        v9_camera_vis.get("status") != "rendered"
        or v9_camera_vis.get("samples") != 8
        or v9_camera_vis.get("is_causal") is not False
    ):
        raise RuntimeError("v9 Camera fixed-8 visualization is incomplete or causal")
    v9_human_ids = [str(record["sample_id"]) for record in v9_human_vis["paired_records"]]
    if v9_human_ids != [str(record["sample_id"]) for record in v9_camera_vis["records"]]:
        raise RuntimeError("v9 Human and Camera fixed-8 sample IDs are not aligned")
    if len(v9_human_vis.get("blind_records", [])) != len(v9_human_ids):
        raise RuntimeError("v9 Human paired and blind visualization counts differ")
    if (
        v10_human_compare.get("status") != "rendered"
        or v10_human_compare.get("samples") != 8
        or v10_human_compare.get("is_causal") is not False
        or v10_human_compare.get("camera_output_branch") != "none"
    ):
        raise RuntimeError("v10 Human comparison is incomplete, causal, or contains Camera output")
    if v10_human_compare.get("sample_ids") != [
        str(record.get("sample_id")) for record in v10_human_compare.get("records", [])
    ]:
        raise RuntimeError("v10 Human comparison IDs and records are misaligned")
    v10_sources = v10_human_compare.get("sources", {})
    if (
        v10_sources.get("stage1_endpoint_fixed", {}).get("checkpoint_sha256")
        != V10_STAGE1_ENDPOINT_CHECKPOINT_SHA256
    ):
        raise RuntimeError("v10 Human comparison Stage1 endpoint SHA256 mismatch")
    if (
        v10_sources.get("v10_human_teacher_cfg1_fixed", {}).get("checkpoint_sha256")
        != V10_HUMAN_TEACHER_CHECKPOINT_SHA256
    ):
        raise RuntimeError("v10 CFG1 Human comparison teacher SHA256 mismatch")
    if (
        v10_sources.get("v10_human_teacher_cfg1_fixed", {}).get("owning_decoder_sha256")
        != V10_HUMAN_OWNER_SHA256
    ):
        raise RuntimeError("v10 CFG1 Human comparison owner SHA256 mismatch")
    if (
        v10_sources.get("v10_human_teacher_cfg3_fixed", {}).get("checkpoint_sha256")
        != V10_HUMAN_TEACHER_CHECKPOINT_SHA256
    ):
        raise RuntimeError("v10 CFG3 Human comparison teacher SHA256 mismatch")
    if (
        v10_sources.get("v10_human_teacher_cfg3_fixed", {}).get("owning_decoder_sha256")
        != V10_HUMAN_OWNER_SHA256
    ):
        raise RuntimeError("v10 CFG3 Human comparison owner SHA256 mismatch")
    if (
        float(v10_sources.get("v10_human_teacher_cfg1_fixed", {}).get("cfg_scale", -1.0))
        != 1.0
        or float(v10_sources.get("v10_human_teacher_cfg3_fixed", {}).get("cfg_scale", -1.0))
        != 3.0
    ):
        raise RuntimeError("v10 Human comparison CFG contract mismatch")
    if (
        v10_sources.get("v9_human_teacher_cfg1_fixed", {}).get("checkpoint_sha256")
        != V9_HUMAN_TEACHER_CHECKPOINT_SHA256
    ):
        raise RuntimeError("v9 CFG1 Human comparison teacher SHA256 mismatch")
    if (
        v10_sources.get("v9_human_teacher_cfg1_fixed", {}).get("owning_decoder_sha256")
        != V9_HUMAN_OWNER_SHA256
    ):
        raise RuntimeError("v9 CFG1 Human comparison owner SHA256 mismatch")
    if (
        v10_sources.get("v9_human_teacher_cfg3_fixed", {}).get("checkpoint_sha256")
        != V9_HUMAN_TEACHER_CHECKPOINT_SHA256
    ):
        raise RuntimeError("v9 CFG3 Human comparison teacher SHA256 mismatch")
    if (
        v10_sources.get("v9_human_teacher_cfg3_fixed", {}).get("owning_decoder_sha256")
        != V9_HUMAN_OWNER_SHA256
    ):
        raise RuntimeError("v9 CFG3 Human comparison owner SHA256 mismatch")
    if (
        float(v10_sources.get("v9_human_teacher_cfg1_fixed", {}).get("cfg_scale", -1.0))
        != 1.0
        or float(v10_sources.get("v9_human_teacher_cfg3_fixed", {}).get("cfg_scale", -1.0))
        != 3.0
    ):
        raise RuntimeError("v9 Human comparison CFG contract mismatch")
    if human_sixway.get("status") != "rendered":
        raise RuntimeError("Human six-way comparison bundle is incomplete")
    if human_sixway.get("samples") != 8:
        raise RuntimeError("Human six-way comparison must contain exactly fixed-8")
    if human_sixway.get("sample_ids") != [
        str(record.get("sample_id")) for record in human_sixway.get("records", [])
    ]:
        raise RuntimeError("Human six-way comparison IDs and records are misaligned")
    if human_sixway.get("ordered_parent_eval_ids_sha256") != HUMAN_SIXWAY_ORDERED_IDS_SHA256:
        raise RuntimeError("Human six-way comparison parent ordered-ID SHA256 mismatch")
    if stage1_recon.get("status") != "rendered" or stage1_recon.get("is_causal") is not False:
        raise RuntimeError("Stage1 reconstruction comparison bundle is incomplete or causal")
    expected_stage1_groups = {
        "pulp": (8, STAGE1_PULP_ORDERED_IDS_SHA256, 4),
        "hml": (8, STAGE1_HML_ORDERED_IDS_SHA256, 3),
    }
    for group_name, (samples, ordered_hash, variants) in expected_stage1_groups.items():
        group = stage1_recon.get("groups", {}).get(group_name, {})
        if group.get("samples") != samples or group.get("ordered_ids_sha256") != ordered_hash:
            raise RuntimeError(f"Stage1 {group_name} cohort contract mismatch")
        if group.get("sample_ids") != [
            str(record.get("sample_id")) for record in group.get("records", [])
        ]:
            raise RuntimeError(f"Stage1 {group_name} IDs and records are misaligned")
        if any(len(record.get("videos", {})) != variants for record in group.get("records", [])):
            raise RuntimeError(f"Stage1 {group_name} variant count mismatch")
    for source_name, source in stage1_recon.get("sources", {}).items():
        if source.get("is_causal") is not False:
            raise RuntimeError(f"Stage1 source {source_name} is not explicitly non-causal")
    if summary_ids(c325_summary) != expected_ids:
        raise RuntimeError("C3-25 full-render IDs do not match the frozen display and Top-5 IDs")
    if summary_ids(l0_summary) != expected_ids:
        raise RuntimeError("L0 baseline render IDs do not match C3-25")
    if summary_ids(single_summary) != list(DISPLAY_SAMPLE_IDS):
        raise RuntimeError("C3-25 single-step render IDs do not match the fixed diagnostic IDs")
    for label, run_id in HVIEW_RUNS:
        if summary_ids(architecture_full[run_id]) != expected_ids:
            raise RuntimeError(f"{label} full-render IDs do not match the frozen comparison IDs")
        if summary_ids(architecture_single[run_id]) != list(DISPLAY_SAMPLE_IDS):
            raise RuntimeError(f"{label} single-step render IDs do not match the fixed diagnostic IDs")
        for payload in (architecture_full[run_id], architecture_single[run_id]):
            if payload.get("checkpoint_sha256") != HVIEW_CHECKPOINT_SHA256[run_id]:
                raise RuntimeError(f"{label} render checkpoint SHA256 mismatch")
            if payload.get("human_view") != HVIEW_CONTRACTS[run_id]:
                raise RuntimeError(f"{label} render human_view contract mismatch")
            expected_conditioning = run_id == HVIEW_FULL_ID
            for key in (
                "human_task_camera_conditioning",
                "human_task_camera_latent_conditioning",
                "human_task_camera_text_conditioning",
            ):
                if payload.get(key) is not expected_conditioning:
                    raise RuntimeError(f"{label} render {key} mismatch")
    for step, payload in human_only_full.items():
        if summary_ids(payload) != expected_ids:
            raise RuntimeError(f"Human-only step {step} render IDs do not match the frozen comparison IDs")
        if payload.get("checkpoint_sha256") != HUMAN_ONLY_CHECKPOINT_SHA256[step]:
            raise RuntimeError(f"Human-only step {step} render checkpoint SHA256 mismatch")
        if payload.get("checkpoint_step") != step:
            raise RuntimeError(f"Human-only render checkpoint step mismatch: {step}")
        if payload.get("tasks") != ["human"]:
            raise RuntimeError(f"Human-only step {step} render contains non-Human tasks")
        if payload.get("task_routing") != "human_first":
            raise RuntimeError(f"Human-only step {step} task routing mismatch")
        if payload.get("human_view") != HUMAN_ONLY_VIEW:
            raise RuntimeError(f"Human-only step {step} Human-view contract mismatch")
        if (
            payload.get("human_task_camera_conditioning") is not True
            or payload.get("human_task_camera_latent_conditioning") is not True
            or payload.get("human_task_camera_text_conditioning") is not False
        ):
            raise RuntimeError(f"Human-only step {step} Direct-H conditioning flags mismatch")

    screen_manifests = {
        run_id: load_json(ev.screen_manifest(run_id))
        for run_id in (C325_ID, HVIEW_FULL_ID, HVIEW_ISOLATED_ID)
    }
    def screen_ordered_ids(run_id: str, payload: dict[str, Any]) -> str:
        declared = payload.get("ordered_ids_sha256") or payload.get("artifacts", {}).get(
            "direct_h", {}
        ).get("ordered_ids_sha256")
        return declared or ordered_record_ids_sha256(
            ev.screen_metric(run_id, "direct_h").with_suffix(".records.jsonl")
        )

    ordered_ids = screen_ordered_ids(C325_ID, screen_manifests[C325_ID])
    for run_id, payload in screen_manifests.items():
        if payload.get("status") != "complete_screen_only":
            raise RuntimeError(f"incomplete architecture screen for {run_id}: {payload.get('status')!r}")
        if payload.get("formal_evidence") is not False:
            raise RuntimeError(f"architecture screen is incorrectly labeled formal: {run_id}")
        if screen_ordered_ids(run_id, payload) != ordered_ids:
            raise RuntimeError(f"architecture screen ordered IDs mismatch: {run_id}")
    human_only_parent_screen = load_json(ev.human_only_parent_screen_manifest())
    if human_only_parent_screen.get("status") != "complete_screen_only":
        raise RuntimeError("Human-only Parent backfill screen is incomplete")
    if human_only_parent_screen.get("formal_evidence") is not False:
        raise RuntimeError("Human-only Parent backfill screen is incorrectly labeled formal")
    if human_only_parent_screen.get("ordered_ids_sha256") != ordered_ids:
        raise RuntimeError("Human-only Parent backfill screen ordered IDs mismatch")
    human_only_screen = load_json(ev.human_only_screen_manifest())
    if human_only_screen.get("status") != "complete_screen_only":
        raise RuntimeError("Human-only learning-curve screen is incomplete")
    if human_only_screen.get("formal_evidence") is not False:
        raise RuntimeError("Human-only learning-curve screen is incorrectly labeled formal")
    if human_only_screen.get("ordered_ids_sha256") != ordered_ids:
        raise RuntimeError("Human-only learning-curve screen ordered IDs mismatch")
    if human_only_screen.get("snapshots") != list(HUMAN_ONLY_STEPS):
        raise RuntimeError("Human-only learning-curve screen snapshot list mismatch")
    for step in HUMAN_ONLY_STEPS:
        artifact = human_only_screen.get("artifacts", {}).get(str(step), {})
        if artifact.get("checkpoint_sha256") != HUMAN_ONLY_CHECKPOINT_SHA256[step]:
            raise RuntimeError(f"Human-only step {step} screen checkpoint SHA256 mismatch")
    required: list[Path] = []
    for task in ("human", "camera", "joint_parallel"):
        required.extend((ev.c325_metric(task), ev.l0_metric(task)))
    for run_id in (C325_ID, HVIEW_FULL_ID, HVIEW_ISOLATED_ID):
        for profile in ("direct_h", "direct_c_clean_h", "joint_parallel"):
            required.append(ev.screen_metric(run_id, profile))
    for task in ("human", "camera", "joint"):
        for timestep in SINGLE_STEP_TIMESTEPS:
            required.append(ev.c325_single_step_metric(task, timestep))
    required.extend(
        (
            ev.human_only_parent_metric(),
            ev.human_only_parent_screen_manifest(),
            ev.human_only_screen_manifest(),
        )
    )
    for step in HUMAN_ONLY_STEPS:
        required.extend(
            (
                ev.human_only_metric(step),
                ev.human_only_full_vis(step) / "render_summary.json",
            )
        )
    for sample_id in expected_ids:
        for run_id, group in (
            (C325_ID, C325_FULL_GROUP),
            (L0_ID, L0_BASELINE_GROUP),
            (HVIEW_FULL_ID, ARCH_FULL_GROUP),
            (HVIEW_ISOLATED_ID, ARCH_FULL_GROUP),
        ):
            root = ev.full_vis(run_id, group) / sample_id
            required.extend(
                root / name
                for name in (
                    "gt_skeleton.mp4",
                    "gt_camera_projection.mp4",
                    "human_skeleton.mp4",
                    "camera_camera_projection.mp4",
                    "joint_skeleton.mp4",
                    "joint_camera_projection.mp4",
                )
            )
    for sample_id in DISPLAY_SAMPLE_IDS:
        for task in ("human", "camera", "joint"):
            roots = [
                ev.c325_single_step_vis() / task / sample_id,
                *[
                    ev.architecture_single_step_vis(run_id) / task / sample_id
                    for _, run_id in HVIEW_RUNS
                ],
            ]
            for root in roots:
                required.extend((root / "gt_skeleton.mp4", root / "gt_camera_projection.mp4"))
                for timestep in SINGLE_STEP_TIMESTEPS:
                    required.extend(
                        (
                            root / f"t{timestep}_skeleton.mp4",
                            root / f"t{timestep}_camera_projection.mp4",
                        )
                    )
    for step in HUMAN_ONLY_STEPS:
        for sample_id in expected_ids:
            required.append(ev.human_only_full_vis(step) / sample_id / "human_skeleton.mp4")
    for record in human_sixway["records"]:
        for key in ("gt", "stage1_recon", "c3_25", "mardm", "vimogen_clip", "vimogen_t5"):
            video = record.get("videos", {}).get(key, {})
            path = evidence_path(ev, str(video.get("path", "")))
            required.append(path)
            if path.is_file() and hashlib.sha256(path.read_bytes()).hexdigest() != video.get("sha256"):
                raise RuntimeError(f"Human six-way video SHA256 mismatch: {path}")
    for group_name, group in stage1_recon["groups"].items():
        for record in group["records"]:
            for video in record["videos"].values():
                path = evidence_path(ev, str(video.get("path", "")))
                required.append(path)
                if path.is_file() and hashlib.sha256(path.read_bytes()).hexdigest() != video.get("sha256"):
                    raise RuntimeError(f"Stage1 {group_name} video SHA256 mismatch: {path}")
    required.extend(
        [
            ev.v10_human_compare_manifest(),
            ev.v9_human_vis_root() / "visual_manifest.json",
            ev.v9_camera_vis_root() / "visual_manifest.json",
            *[
                ev.v9_eval_result(group)
                for group in (
                    V9_HUMAN_EVAL_GROUP,
                    *V9_UNIFIED_EVAL_GROUPS.values(),
                )
            ],
        ]
    )
    for record in v10_human_compare["records"]:
        videos = record.get("videos", {})
        if set(videos) != {
            "gt",
            "human_reconstruction",
            "v10_human_teacher_cfg1",
            "v9_human_teacher_cfg1",
            "v10_human_teacher_cfg3",
            "v9_human_teacher_cfg3",
        }:
            raise RuntimeError("v10 Human comparison does not contain exactly six video roles")
        for video in videos.values():
            path = evidence_path(ev, video["path"])
            required.append(path)
            if path.is_file() and hashlib.sha256(path.read_bytes()).hexdigest() != video["sha256"]:
                raise RuntimeError(f"v10 Human comparison video SHA256 mismatch: {path}")
    for record in [*v9_human_vis["paired_records"], *v9_human_vis["blind_records"]]:
        path = evidence_path(ev, record["video"])
        required.append(path)
        if path.is_file() and hashlib.sha256(path.read_bytes()).hexdigest() != record["video_sha256"]:
            raise RuntimeError(f"v9 Human video SHA256 mismatch: {path}")
    for record in v9_camera_vis["records"]:
        path = evidence_path(ev, record["video"])
        required.append(path)
        if path.is_file() and hashlib.sha256(path.read_bytes()).hexdigest() != record["video_sha256"]:
            raise RuntimeError(f"v9 Camera video SHA256 mismatch: {path}")
    missing = [path for path in required if not path.is_file()]
    if missing:
        preview = "\n".join(str(path) for path in missing[:20])
        raise RuntimeError(f"missing {len(missing)} required evidence files:\n{preview}")
    return {
        "c325_run": C325_ID,
        "baseline_run": L0_ID,
        "display_samples": len(DISPLAY_SAMPLE_IDS),
        "joint_top5": 5,
        "render_ids": len(expected_ids),
        "architecture_arms": [label for label, _ in HVIEW_RUNS],
        "human_only_snapshots": len(HUMAN_ONLY_STEPS),
        "human_sixway_samples": human_sixway["samples"],
        "stage1_pulp_samples": stage1_recon["groups"]["pulp"]["samples"],
        "stage1_hml_samples": stage1_recon["groups"]["hml"]["samples"],
        "v9_human_camera_samples": len(v9_human_ids),
        "v10_human_compare_samples": v10_human_compare["samples"],
        "screen_ordered_ids_sha256": ordered_ids,
        "single_step_timesteps": len(SINGLE_STEP_TIMESTEPS),
        "single_step_groups": 3,
        "required_files": len(required),
        "missing": 0,
    }


def build_demo(ev: Evidence):
    import gradio as gr

    c325_summary = load_json(ev.full_vis(C325_ID, C325_FULL_GROUP) / "render_summary.json")
    single_summary = load_json(ev.c325_single_step_vis() / "render_summary.json")
    humanml_summary = load_json(ev.humanml_summary())
    human_sixway = load_json(ev.human_sixway_manifest())
    stage1_recon = load_json(ev.stage1_recon_manifest())
    v9_human_vis = load_json(ev.v9_human_vis_root() / "visual_manifest.json")
    v9_camera_vis = load_json(ev.v9_camera_vis_root() / "visual_manifest.json")
    v10_human_compare = load_json(ev.v10_human_compare_manifest())
    c325_index = summary_index(c325_summary)
    single_index = summary_index(single_summary)
    top_records = ranked_joint_records(load_json(ev.c325_geometry()))
    ranking = {str(record["sample_id"]): record for record in top_records}
    top_choices = [
        (
            f"#{index} · {record['sample_id']} · rank {float(record['joint_rank_score']):.5f}",
            str(record["sample_id"]),
        )
        for index, record in enumerate(top_records, start=1)
    ]
    humanml_ids = [str(item["sample_id"]) for item in humanml_summary["samples"]]
    stage1_pulp_ids = [str(value) for value in stage1_recon["groups"]["pulp"]["sample_ids"]]
    stage1_hml_ids = [str(value) for value in stage1_recon["groups"]["hml"]["sample_ids"]]

    def video_grid(labels: tuple[str, ...], columns: int = 3) -> list[Any]:
        play = gr.Button("▶ 同步播放当前组", variant="primary", elem_classes="sync-play")
        play.click(fn=None, js=SYNC_PLAY_JS)
        videos = []
        for start in range(0, len(labels), columns):
            row_classes = ["evidence-row", *(["two-column-row"] if columns == 2 else [])]
            with gr.Row(elem_classes=row_classes):
                for label in labels[start : start + columns]:
                    with gr.Column():
                        gr.Markdown(f"### {label}")
                        videos.append(gr.Video(show_label=False, format="mp4"))
        return videos

    with gr.Blocks(title="StoryMotion Stage1 and Stage2 evidence") as demo:
        gr.Markdown("# StoryMotion · Stage1 / Stage2 evidence desk", elem_id="hero")
        gr.Markdown(
            "**对照：C3-25 mainline、H-FULL 与 H-ISOLATED，均为 seed17 · fresh Stage2 105K。** "
            "三者共享 exact Stage1/cache/normalization、task allocation 与 owning decoder；"
            "H-FULL/H-ISOLATED 只改变 Human slice 的 Camera latent/text view。"
            "独立 Human-only 页固定展示 native 192D Direct-H 的四个训练快照；"
            "六路 Human 页并排显示同 ID 的 GT、Stage1、C3-25、MARDM 与两条 ViMoGen-light；"
            "Stage1 页分别提供 Pulp 四路与 HumanML root/local 三路 exact-length reconstruction；"
            "v9 页汇总 protected-H Human 105K 与 Camera 210K 的 matched fixed-8；"
            "v10 页按同一 fixed-8 分组展示 GT/reconstruction、v10/v9 CFG1、v10/v9 CFG3 Human teacher；"
            "N=512 数字是 screen-only，v7.38 L0 只保留为历史视觉参照；"
            "Top-5 与八样本 single-step 不构成 blind quality claim。",
            elem_classes="verdict",
        )
        with gr.Tabs():
            with gr.Tab("v10 · GT / H recon / teacher"):
                sample = gr.Dropdown(
                    list(v10_human_compare["sample_ids"]),
                    value=v10_human_compare["sample_ids"][0],
                    label="v10 matched fixed-8 sample",
                )
                status = gr.Markdown(elem_classes="metric-strip")
                videos = video_grid(
                    (
                        "v10 · Ground truth",
                        "v10 · Phase-A 210K Human reconstruction",
                        "v10 · Stage2 Human teacher 105K · CFG1",
                        "v9 · Stage2 Human teacher 105K · CFG1",
                        "v10 · Stage2 Human teacher 105K · CFG3",
                        "v9 · Stage2 Human teacher 105K · CFG3",
                    ),
                    columns=2,
                )
                outputs = [status, *videos]
                callback = lambda sample_id: v10_human_compare_view(
                    ev, v10_human_compare, sample_id
                )
                sample.change(callback, sample, outputs)
                demo.load(callback, sample, outputs)

            with gr.Tab("v9 · Human + Camera"):
                gr.Markdown(v9_eval_metrics(ev), elem_classes="metric-strip")
                sample = gr.Dropdown(
                    [record["sample_id"] for record in v9_human_vis["paired_records"]],
                    value=v9_human_vis["paired_records"][0]["sample_id"],
                    label="Protected-H fixed-8 sample",
                )
                status = gr.Markdown(elem_classes="metric-strip")
                videos = video_grid(
                    (
                        "Human 105K · GT vs Direct-H",
                        "Human 105K · blind Direct-H",
                        "Camera 210K · GT / Direct-C / joint-parallel",
                    )
                )
                outputs = [status, *videos]
                callback = lambda sample_id: v9_protected_view(
                    ev, v9_human_vis, v9_camera_vis, sample_id
                )
                sample.change(callback, sample, outputs)
                demo.load(callback, sample, outputs)

            with gr.Tab("Human · Six-way 105K"):
                sample = gr.Dropdown(
                    list(human_sixway["sample_ids"]),
                    value=human_sixway["sample_ids"][0],
                    label="Canonical pure-test fixed sample",
                )
                status = gr.Markdown(elem_classes="metric-strip")
                videos = video_grid(
                    (
                        "Ground truth",
                        "C3-25 · Stage1 reconstruction",
                        "C3-25 · Direct-H 105K",
                        "MARDM · Human-only 105K",
                        "ViMoGen-light · CLIP 105K",
                        "ViMoGen-light · UMT5 105K",
                    )
                )
                outputs = [status, *videos]
                callback = lambda sample_id: human_sixway_view(ev, human_sixway, sample_id)
                sample.change(callback, sample, outputs)
                demo.load(callback, sample, outputs)

            with gr.Tab("Stage1 · Pulp four-way"):
                sample = gr.Dropdown(
                    stage1_pulp_ids,
                    value=stage1_pulp_ids[0],
                    label="Pulp pure-test fixed sample",
                )
                status = gr.Markdown(elem_classes="metric-strip")
                videos = video_grid(
                    (
                        "Ground truth",
                        "C3-25 · Stage1",
                        "Redesign Stage1 · Pulp-only",
                        "Redesign Stage1 · HML+Pulp",
                    ),
                    columns=2,
                )
                outputs = [status, *videos]
                callback = lambda sample_id: stage1_recon_view(
                    ev, stage1_recon, "pulp", sample_id
                )
                sample.change(callback, sample, outputs)
                demo.load(callback, sample, outputs)

            with gr.Tab("Stage1 · HML root/local"):
                sample = gr.Dropdown(
                    stage1_hml_ids,
                    value=stage1_hml_ids[0],
                    label="HumanML3D validation fixed sample",
                )
                status = gr.Markdown(elem_classes="metric-strip")
                videos = video_grid(
                    (
                        "HumanML3D reference · root/local",
                        "Redesign Stage1 · Pulp-only",
                        "Redesign Stage1 · HML+Pulp",
                    )
                )
                outputs = [status, *videos]
                callback = lambda sample_id: stage1_recon_view(
                    ev, stage1_recon, "hml", sample_id
                )
                sample.change(callback, sample, outputs)
                demo.load(callback, sample, outputs)

            for task, tab_name, gt_label, output_label in (
                ("human", "H Completion · Architecture", "GT human", "Direct-H"),
                ("camera", "C Completion · Architecture", "GT camera + GT human", "Direct-C"),
            ):
                with gr.Tab(tab_name):
                    sample = gr.Dropdown(list(DISPLAY_SAMPLE_IDS), value=DISPLAY_SAMPLE_IDS[0], label="Sample")
                    metric_box = gr.Markdown(elem_classes="metric-strip")
                    status = gr.Markdown()
                    gr.Markdown("### Frozen baseline row · GT / C3-25 / former-mainline L0")
                    videos = video_grid(
                        (
                            gt_label,
                            f"C3-25 mainline · {output_label}",
                            f"v7.38 L0 · {output_label}",
                        )
                    )
                    gr.Markdown("---\n### H-FULL row · full Camera latent + dual text for both Human slices")
                    videos.extend(
                        video_grid(
                            (
                                gt_label,
                                f"C3-25 mainline · {output_label}",
                                f"H-FULL · {output_label}",
                            )
                        )
                    )
                    gr.Markdown("---\n### H-ISOLATED row · zero Camera latent/text for both Human slices")
                    videos.extend(
                        video_grid(
                            (
                                gt_label,
                                f"C3-25 mainline · {output_label}",
                                f"H-ISOLATED · {output_label}",
                            )
                        )
                    )
                    outputs = [metric_box, status, *videos]
                    callback = lambda sample_id, selected_task=task: completion_view(
                        ev, c325_index, sample_id, selected_task
                    )
                    sample.change(callback, sample, outputs)
                    demo.load(callback, sample, outputs)

            with gr.Tab("Human-only · Learning Curve"):
                sample = gr.Dropdown(
                    render_ids(ev),
                    value=DISPLAY_SAMPLE_IDS[0],
                    label="Frozen fixed-8 + Parent Top-5 sample",
                )
                metric_box = gr.Markdown(elem_classes="metric-strip")
                status = gr.Markdown()
                videos = video_grid(
                    (
                        "GT human",
                        "Parent C3-105K · Direct-H",
                        "Human-only · step 35,006",
                        "Human-only · step 58,339",
                        "Human-only · step 70,005",
                        "Human-only · step 105,000",
                    )
                )
                outputs = [metric_box, status, *videos]
                callback = lambda sample_id: human_only_view(ev, c325_index, sample_id)
                sample.change(callback, sample, outputs)
                demo.load(callback, sample, outputs)

            with gr.Tab("Joint Top-5 · Architecture"):
                sample = gr.Dropdown(top_choices, value=top_choices[0][1], label="C3-25 paired-geometry rank")
                metric_box = gr.Markdown(elem_classes="metric-strip")
                status = gr.Markdown()
                gr.Markdown("### Ground truth")
                videos = video_grid(
                    ("GT · camera projection", "GT · world skeleton"),
                    columns=2,
                )
                gr.Markdown("---\n### C3-25 mainline")
                videos.extend(
                    video_grid(
                        ("C3-25 · joint projection", "C3-25 · joint skeleton"),
                        columns=2,
                    )
                )
                gr.Markdown("---\n### v7.38 L0 · historical visual reference")
                videos.extend(
                    video_grid(
                        ("v7.38 L0 · joint projection", "v7.38 L0 · joint skeleton"),
                        columns=2,
                    )
                )
                gr.Markdown("---\n### H-FULL")
                videos.extend(
                    video_grid(
                        ("H-FULL · joint projection", "H-FULL · joint skeleton"),
                        columns=2,
                    )
                )
                gr.Markdown("---\n### H-ISOLATED")
                videos.extend(
                    video_grid(
                        ("H-ISOLATED · joint projection", "H-ISOLATED · joint skeleton"),
                        columns=2,
                    )
                )
                outputs = [metric_box, status, *videos]
                callback = lambda sample_id: joint_view(ev, c325_index, ranking, sample_id)
                sample.change(callback, sample, outputs)
                demo.load(callback, sample, outputs)

            with gr.Tab("Single-step · Architecture"):
                with gr.Row():
                    sample = gr.Dropdown(list(DISPLAY_SAMPLE_IDS), value=DISPLAY_SAMPLE_IDS[0], label="Sample")
                    task = gr.Radio(("human", "camera", "joint"), value="human", label="Target")
                    view = gr.Radio(("Camera projection", "World skeleton"), value="World skeleton", label="View")
                metric_box = gr.Markdown(elem_classes="metric-strip")
                status = gr.Markdown()
                step_labels = ("Raw GT", "t = 999", "t = 799", "t = 599", "t = 399", "t = 199")
                gr.Markdown("### C3-25 mainline · six-video teacher-forced group")
                videos = video_grid(step_labels)
                gr.Markdown("---\n### H-FULL · six-video teacher-forced group")
                videos.extend(video_grid(step_labels))
                gr.Markdown("---\n### H-ISOLATED · six-video teacher-forced group")
                videos.extend(video_grid(step_labels))
                outputs = [metric_box, status, *videos]
                inputs = [sample, task, view]
                callback = lambda sample_id, selected_task, selected_view: single_step_view(
                    ev, single_index, sample_id, selected_task, selected_view
                )
                sample.change(callback, inputs, outputs)
                task.change(callback, inputs, outputs)
                view.change(callback, inputs, outputs)
                demo.load(callback, inputs, outputs)

            with gr.Tab("HumanML3D · Stage1"):
                sample = gr.Dropdown(humanml_ids, value=humanml_ids[0], label="HumanML3D sample")
                status = gr.Markdown()
                videos = video_grid(
                    ("HumanML3D source · fixed camera", "HumanML3D → v7.14 Stage1 · fixed camera"),
                    columns=2,
                )
                outputs = [status, *videos]
                callback = lambda sample_id: humanml_view(ev, humanml_summary, sample_id)
                sample.change(callback, sample, outputs)
                demo.load(callback, sample, outputs)
    return demo


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=DEFAULT_ROOT)
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=7865)
    parser.add_argument("--validate-only", action="store_true")
    parser.add_argument("--list-render-ids", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    ev = Evidence(args.root.resolve())
    if args.list_render_ids:
        top = [str(record["sample_id"]) for record in ranked_joint_records(load_json(ev.c325_geometry()))]
        print(json.dumps({"display": list(DISPLAY_SAMPLE_IDS), "top5": top, "all": render_ids(ev)}, indent=2))
        return 0
    if args.validate_only:
        print(json.dumps(validate(ev), indent=2, sort_keys=True))
        return 0
    demo = build_demo(ev)
    allowed = [
        str(ev.canonical_vis(C325_ID).resolve()),
        str(ev.canonical_vis(L0_ID).resolve()),
        str(ev.canonical_vis(HVIEW_FULL_ID).resolve()),
        str(ev.canonical_vis(HVIEW_ISOLATED_ID).resolve()),
        str(ev.canonical_vis(HUMAN_ONLY_ID).resolve()),
        str((ev.root / "runs" / "stage1" / HUMANML_RUN_ID).resolve()),
        str(ev.human_sixway_root().resolve()),
        str(ev.stage1_recon_root().resolve()),
        str(ev.v9_human_vis_root().resolve()),
        str(ev.v9_camera_vis_root().resolve()),
        str(ev.v10_human_compare_root().resolve()),
    ]
    demo.launch(server_name=args.host, server_port=args.port, share=False, allowed_paths=allowed, css=CSS)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
