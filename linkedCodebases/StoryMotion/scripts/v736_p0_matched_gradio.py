#!/usr/bin/env python3
"""Browse matched Unified-3 metrics and qualitative evidence."""
from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from pathlib import Path


DEFAULT_ROOT = Path("/data/public/ripemangobox/Motion/StoryMotion")
CFG_DIR = "std_cfg1.0_eta0.0"
P0_VIS_GROUP = "p0_matched_20260715"
L0_VIS_GROUP = "v738_l0_joint_strict_20260715"
L0_DIRECT_VIS_GROUP = "v738_l0_direct_tasks_strict_20260715"
PULP_VIS_GROUP = "v738_l0_pulp_official_20260715"
TOP_VIS_GROUP = "v738_l0_joint_top5_20260716/comparison_geometry_specialist"
TOP_PULP_VIS_GROUP = "v738_l0_joint_top5_20260716/comparison_geometry_pulp"
SINGLE_STEP_VIS_GROUP = "l0_single_step_gate_20260715"
SINGLE_STEP_EVAL_GROUP = "single_step_gate_20260715"
FIXED8_VIS_GROUP = "l0_fixed8_joint_parallel_20260719"
HUMANML_RUN_ID = "v7_40_humanml3d_adapter_vis_20260715"
HUMANML_VIS_GROUP = "humanml3d_stage1_adapted_20260715"
COMPLETION_REGISTRY = "completion_vis_registry.json"
SINGLE_STEP_TIMESTEPS = (999, 799, 599, 399, 199)

A_ID = "v7_36_p0a_asym_unified3_joint30k_seed17_4090g0_20260714"
B_ID = "v7_36_p0b_sym_unified3_joint30k_seed17_4090g1_20260714"
C_ID = "v7_36_p0c_asym_nojoint30k_seed17_5090g0_20260714"
L0_ID = "v7_38_l0_clean_lr3em5_105k_purefull_seed17_4090g0_20260715"
V747_ID = "v7_47_official_ae_unified_matched_seed17_5090g0_20260717"
V81A_ID = "v8_1a_diag_unified3_30k_seed17_4090g0_20260718"
JOINT_SPECIALIST_ID = "v7_42_l0_sameimpl_specialist_seed17_joint_exposure_matched"

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
.evidence-row > div { min-width: 0 !important; }
.evidence-cols-3 > div { flex: 1 1 calc(33.333% - 10px) !important; max-width: calc(33.333% - 10px); }
.evidence-cols-2 > div { flex: 1 1 calc(50% - 7px) !important; max-width: calc(50% - 7px); }
.evidence-cols-4 > div { flex: 1 1 calc(25% - 11px) !important; max-width: calc(25% - 11px); }
.evidence-row video {
  background: #151b1d;
  aspect-ratio: 16 / 10;
  object-fit: contain;
  border-radius: 2px !important;
}
.sync-play { max-width: 240px; margin: 4px 0 12px; }
.geometry-row { flex-wrap: wrap !important; gap: 10px; }
.geometry-row > div { flex: 1 1 calc(33.333% - 10px) !important; max-width: calc(33.333% - 10px); min-width: 275px !important; }
button.primary { background: var(--orange) !important; border-color: var(--orange) !important; }
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

    @property
    def runs(self) -> Path:
        return self.root / "runs" / "stage2"

    @property
    def stage1_runs(self) -> Path:
        return self.root / "runs" / "stage1"

    def run(self, run_id: str) -> Path:
        return self.runs / run_id

    def stage1_run(self, run_id: str) -> Path:
        return self.stage1_runs / run_id

    def eval(self, run_id: str, name: str) -> Path:
        return self.run(run_id) / "eval" / "official_pure4053_matched" / f"{name}.json"

    def vis(self, run_id: str, schedule: str, group: str = P0_VIS_GROUP) -> Path:
        return self.run(run_id) / "vis" / group / schedule / CFG_DIR

    def summary(self, run_id: str, schedule: str, group: str = P0_VIS_GROUP) -> Path:
        return self.run(run_id) / "vis" / group / schedule / "metrics" / CFG_DIR / "render_summary.json"

    def single_step_eval(self, task: str, source: str) -> Path:
        return self.run(L0_ID) / "eval" / SINGLE_STEP_EVAL_GROUP / task / f"{source}.json"

    def canonical_vis(self, run_id: str) -> Path:
        return self.root / "runs" / "vis" / "stage2" / run_id

    def fixed8(self, run_id: str, branch: str) -> Path:
        return self.canonical_vis(run_id) / FIXED8_VIS_GROUP / branch

    def v81a_eval(self, name: str) -> Path:
        return (
            self.root
            / "runs"
            / "legacy"
            / "eval"
            / "stage2"
            / V81A_ID
            / "official_pure4053_matched"
            / f"{name}.json"
        )

    def v747_eval(self, name: str) -> Path:
        return self.fixed8(V747_ID, "formal_metrics") / f"{name}.json"


def load_json(path: Path) -> dict:
    if not path.is_file():
        raise FileNotFoundError(f"missing required artifact: {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def load_completion_registry(ev: Evidence) -> dict:
    registry = load_json(ev.root / "configs" / COMPLETION_REGISTRY)
    if int(registry.get("schema_version", -1)) != 1:
        raise ValueError("completion visualization registry must use schema_version=1")
    modes = registry.get("modes")
    if not isinstance(modes, dict) or set(modes) != {"human", "camera"}:
        raise ValueError("completion visualization registry must define human and camera modes")
    for mode, record in modes.items():
        slots = record.get("slots")
        if not isinstance(slots, list) or len(slots) < 2:
            raise ValueError(f"completion mode {mode} must contain at least GT and StoryMotion slots")
        labels = [str(slot.get("label", "")) for slot in slots]
        if any(not label for label in labels) or len(labels) != len(set(labels)):
            raise ValueError(f"completion mode {mode} has empty or duplicate slot labels")
    return registry


def metric(payload: dict, key: str) -> float:
    value = payload["metrics"].get(key)
    return float(value) if value is not None else float("nan")


def completion_metrics(ev: Evidence, task: str) -> str:
    rows = []
    for label, run_id in (("A · asymmetric + joint", A_ID), ("B · symmetric control", B_ID), ("C · asymmetric no-joint", C_ID)):
        payload = load_json(ev.eval(run_id, task))
        if task == "human":
            rows.append(
                f"| {label} | {metric(payload, 'test/tmr/ftd'):.2f} | "
                f"{metric(payload, 'test/tmr/tmr_score'):.3f} | "
                f"{100 * metric(payload, 'test/tmr/coverage'):.1f}% |"
            )
        else:
            rows.append(
                f"| {label} | {metric(payload, 'test/clatr/fcd'):.2f} | "
                f"{metric(payload, 'test/clatr/clatr_score'):.3f} | "
                f"{100 * metric(payload, 'test/clatr/coverage'):.1f}% | "
                f"{metric(payload, 'test/captions/fscore'):.3f} |"
            )
    if task == "human":
        header = [
            "| version / run | FDTMR↓ | TMR↑ | HCov↑ |",
            "| --- | ---: | ---: | ---: |",
        ]
        note = "B observes camera and is a symmetric control; the desired human-text-only rows are A and C."
    else:
        header = [
            "| version / run | FDCLaTr↓ | CLaTr↑ | CCov↑ | Caption F1↑ |",
            "| --- | ---: | ---: | ---: | ---: |",
        ]
        note = "Camera completion uses observed human plus camera text in all three matched runs."
    return "\n".join(
        [f"**Official pure-4,053 · v7.36 step30k controls · `{task}` · DDIM50 · CFG1 · η0**", "", *header, *rows, "", note]
    )


def joint_metrics(ev: Evidence) -> str:
    rows = []
    variants = (
        ("A · parallel", A_ID, "joint_parallel"),
        ("A · human-first cascade", A_ID, "joint_cascade"),
        ("B · symmetric parallel", B_ID, "joint_parallel"),
        ("C · no-joint cascade", C_ID, "joint_cascade"),
    )
    for label, run_id, name in variants:
        payload = load_json(ev.eval(run_id, name))
        rows.append(
            f"| {label} | {metric(payload, 'test/tmr/ftd'):.2f} | "
            f"{metric(payload, 'test/tmr/tmr_score'):.3f} | "
            f"{100 * metric(payload, 'test/tmr/coverage'):.1f}% | "
            f"{metric(payload, 'test/clatr/fcd'):.2f} | "
            f"{metric(payload, 'test/clatr/clatr_score'):.3f} | "
            f"{100 * metric(payload, 'test/clatr/coverage'):.1f}% | "
            f"{100 * metric(payload, 'test/proj/outscreen'):.1f}% |"
        )
    return "\n".join(
        [
            "**Official pure-4,053 · matched joint schedules · DDIM50 · CFG1 · η0**",
            "",
            "| version / run | FDTMR↓ | TMR↑ | HCov↑ | FDCLaTr↓ | CLaTr↑ | CCov↑ | Out↓ |",
            "| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
            *rows,
            "",
            "A is the promoted checkpoint. Parallel and cascade are a Pareto pair from the same A weights; C proves cascade does not replace joint training.",
        ]
    )


def l0_metrics(ev: Evidence) -> str:
    rows = []
    for label, name in (("L0 · directed parallel", "joint_parallel"), ("L0 · human-first cascade", "joint_cascade")):
        payload = load_json(ev.eval(L0_ID, name))
        rows.append(
            f"| {label} | {metric(payload, 'test/tmr/ftd'):.2f} | "
            f"{metric(payload, 'test/tmr/tmr_score'):.3f} | "
            f"{100 * metric(payload, 'test/tmr/coverage'):.1f}% | "
            f"{metric(payload, 'test/clatr/fcd'):.2f} | "
            f"{metric(payload, 'test/clatr/clatr_score'):.3f} | "
            f"{100 * metric(payload, 'test/clatr/coverage'):.1f}% | "
            f"{metric(payload, 'test/captions/fscore'):.3f} | "
            f"{100 * metric(payload, 'test/proj/outscreen'):.1f}% |"
        )
    return "\n".join(
        [
            "**Official pure-4,053 · L0 joint schedules · DDIM50 · CFG1 · η0 · seed17**",
            "",
            "| version / run | FDTMR↓ | TMR↑ | HCov↑ | FDCLaTr↓ | CLaTr↑ | CCov↑ | Caption F1↑ | Out↓ |",
            "| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
            *rows,
            "",
            "Both schedules use checkpoint `ab474d…f35`; cascade is the explicit `text→H→C` path, while parallel generates H/C in one trajectory.",
        ]
    )


def l0_task_slice_metrics(ev: Evidence, task: str) -> str:
    variants = (
        (f"L0 · direct {task}", task),
        ("L0 · joint parallel", "joint_parallel"),
        ("L0 · joint cascade", "joint_cascade"),
    )
    rows = []
    for label, name in variants:
        payload = load_json(ev.eval(L0_ID, name))
        if task == "human":
            rows.append(
                f"| {label} | {metric(payload, 'test/tmr/ftd'):.2f} | "
                f"{metric(payload, 'test/tmr/tmr_score'):.3f} | "
                f"{100 * metric(payload, 'test/tmr/coverage'):.1f}% |"
            )
        else:
            out = payload["metrics"].get("test/proj/outscreen")
            out_text = f"{100 * float(out):.1f}%" if out is not None else "N/A"
            rows.append(
                f"| {label} | {metric(payload, 'test/clatr/fcd'):.2f} | "
                f"{metric(payload, 'test/clatr/clatr_score'):.3f} | "
                f"{100 * metric(payload, 'test/clatr/coverage'):.1f}% | "
                f"{metric(payload, 'test/captions/fscore'):.3f} | "
                f"{out_text} |"
            )
    if task == "human":
        header = [
            "| version / run | FDTMR↓ | TMR↑ | HCov↑ |",
            "| --- | ---: | ---: | ---: |",
        ]
        note = (
            "All rows use L0 step105k. Direct human is human-text-only; joint rows evaluate the human branch "
            "while also generating camera, so this is a matched-checkpoint task-difficulty comparison."
        )
    else:
        header = [
            "| version / run | FDCLaTr↓ | CLaTr↑ | CCov↑ | Caption F1↑ | Out↓ |",
            "| --- | ---: | ---: | ---: | ---: | ---: |",
        ]
        note = (
            "All rows use L0 step105k. Direct camera observes GT human; parallel generates both branches and "
            "cascade observes generated human, so source difficulty must remain explicit."
        )
    return "\n".join(
        [f"**Official pure-4,053 · L0 `{task}` target · DDIM50 · CFG1 · η0**", "", *header, *rows, "", note]
    )


def pulp_comparison_metrics(ev: Evidence, summary_map: dict[str, dict]) -> str:
    rows = []
    parallel = load_json(ev.eval(L0_ID, "joint_parallel"))
    rows.append(
        f"| L0 · directed parallel | {metric(parallel, 'test/tmr/ftd'):.2f} | "
        f"{metric(parallel, 'test/tmr/tmr_score'):.3f} | "
        f"{100 * metric(parallel, 'test/tmr/coverage'):.1f}% | "
        f"{metric(parallel, 'test/clatr/fcd'):.2f} | "
        f"{metric(parallel, 'test/clatr/clatr_score'):.3f} | "
        f"{100 * metric(parallel, 'test/clatr/coverage'):.1f}% | "
        f"{metric(parallel, 'test/captions/fscore'):.3f} | "
        f"{100 * metric(parallel, 'test/proj/outscreen'):.1f}% |"
    )
    direct_h = load_json(ev.eval(L0_ID, "human"))
    rows.append(
        f"| L0 · Direct H (human-only) | {metric(direct_h, 'test/tmr/ftd'):.2f} | "
        f"{metric(direct_h, 'test/tmr/tmr_score'):.3f} | "
        f"{100 * metric(direct_h, 'test/tmr/coverage'):.1f}% | N/A | N/A | N/A | N/A | N/A |"
    )
    for label, key in (("Pulp official · no-Aux", "pulp_no_aux"), ("Pulp official · Aux", "pulp_aux")):
        payload = summary_map["pulp_compare"]["official_metrics"][key]
        rows.append(
            f"| {label} | {metric(payload, 'test/tmr/ftd'):.2f} | "
            f"{metric(payload, 'test/tmr/tmr_score'):.3f} | "
            f"{100 * metric(payload, 'test/tmr/coverage'):.1f}% | "
            f"{metric(payload, 'test/clatr/fcd'):.2f} | "
            f"{metric(payload, 'test/clatr/clatr_score'):.3f} | "
            f"{100 * metric(payload, 'test/clatr/coverage'):.1f}% | "
            f"{metric(payload, 'test/captions/fscore'):.3f} | "
            f"{100 * metric(payload, 'test/proj/outscreen'):.1f}% |"
        )
    return "\n".join(
        [
            "**Official pure-4,053 · native-system joint-generation comparison**",
            "",
            "| version / run | FDTMR↓ | TMR↑ | HCov↑ | FDCLaTr↓ | CLaTr↑ | CCov↑ | Caption F1↑ | Out↓ |",
            "| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
            *rows,
            "",
            "Direct H is human-text-only and therefore has no camera/framing metrics. L0 parallel uses DDIM50 / CFG1 / η0; "
            "Pulp uses released DiT-xy DDPM50 / text-CFG11 with `w_z=0/0.25`. This remains a native-system display, "
            "not a single-variable loss or architecture ablation.",
        ]
    )


def top_aggregate_rows(ev: Evidence, pulp_summary: dict) -> list[str]:
    payloads = (
        ("v7.38 L0 · directed parallel", load_json(ev.eval(L0_ID, "joint_parallel"))),
        ("v7.42 · joint specialist", load_json(ev.eval(JOINT_SPECIALIST_ID, "joint_parallel"))),
        ("Pulp official · no-Aux", pulp_summary["official_metrics"]["pulp_no_aux"]),
        ("Pulp official · Aux", pulp_summary["official_metrics"]["pulp_aux"]),
    )
    return [
        f"| {label} | {metric(payload, 'test/tmr/ftd'):.2f} | "
        f"{metric(payload, 'test/tmr/tmr_score'):.3f} | "
        f"{100 * metric(payload, 'test/tmr/coverage'):.1f}% | "
        f"{metric(payload, 'test/clatr/fcd'):.2f} | "
        f"{metric(payload, 'test/clatr/clatr_score'):.3f} | "
        f"{100 * metric(payload, 'test/clatr/coverage'):.1f}% | "
        f"{metric(payload, 'test/captions/fscore'):.3f} | "
        f"{100 * metric(payload, 'test/proj/outscreen'):.1f}% |"
        for label, payload in payloads
    ]


def single_step_metrics(ev: Evidence, task: str) -> str:
    variants = [("raw GT reference", "raw_gt"), *[(f"t={timestep}", f"t{timestep}") for timestep in SINGLE_STEP_TIMESTEPS]]
    rows = []
    for label, source in variants:
        payload = load_json(ev.single_step_eval(task, source))
        if task == "human":
            rows.append(
                f"| L0 gate / {label} | {metric(payload, 'test/tmr/ftd'):.2f} | "
                f"{metric(payload, 'test/tmr/tmr_score'):.3f} | "
                f"{100 * metric(payload, 'test/tmr/coverage'):.1f}% |"
            )
        elif task == "camera":
            out = payload["metrics"].get("test/proj/outscreen")
            out_text = f"{100 * float(out):.1f}%" if out is not None else "N/A"
            rows.append(
                f"| L0 gate / {label} | {metric(payload, 'test/clatr/fcd'):.2f} | "
                f"{metric(payload, 'test/clatr/clatr_score'):.3f} | "
                f"{100 * metric(payload, 'test/clatr/coverage'):.1f}% | "
                f"{metric(payload, 'test/captions/fscore'):.3f} | "
                f"{out_text} |"
            )
        else:
            rows.append(
                f"| L0 gate / {label} | {metric(payload, 'test/tmr/ftd'):.2f} | "
                f"{metric(payload, 'test/tmr/tmr_score'):.3f} | "
                f"{100 * metric(payload, 'test/tmr/coverage'):.1f}% | "
                f"{metric(payload, 'test/clatr/fcd'):.2f} | "
                f"{metric(payload, 'test/clatr/clatr_score'):.3f} | "
                f"{100 * metric(payload, 'test/clatr/coverage'):.1f}% | "
                f"{metric(payload, 'test/captions/fscore'):.3f} | "
                f"{100 * metric(payload, 'test/proj/outscreen'):.1f}% |"
            )
    if task == "human":
        header = ("| version / run | FDTMR↓ | TMR↑ | HCov↑ |", "| --- | ---: | ---: | ---: |")
    elif task == "camera":
        header = (
            "| version / run | FDCLaTr↓ | CLaTr↑ | CCov↑ | Caption F1↑ | Out↓ |",
            "| --- | ---: | ---: | ---: | ---: | ---: |",
        )
    else:
        header = (
            "| version / run | FDTMR↓ | TMR↑ | HCov↑ | FDCLaTr↓ | CLaTr↑ | CCov↑ | Caption F1↑ | Out↓ |",
            "| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
        )
    return "\n".join(
        [
            f"**Diagnostic pure-4,053 · L0 `{task}` · teacher-forced single-step `pred_x0`**",
            "",
            *header,
            *rows,
            "",
            "Each `t` row starts from `q(z_gt,t)` with the same deterministic per-sample noise and performs one model forward. "
            "It is a no-training teacher-forced local-denoising diagnostic, not DDIM50 generation or a raw-data-space-loss experiment. "
            "Raw GT is passed directly to the official callback, not through Stage1. It cannot gate a raw-loss formulation or weight. "
            "Because pure-4,053 has now informed diagnosis, it is a development benchmark rather than an untouched final test.",
        ]
    )


def fixed8_summaries(ev: Evidence) -> dict[str, dict]:
    return {
        "v747_manifest": load_json(ev.fixed8(V747_ID, "comparison_manifest.json")),
        "v747_reconstruction": load_json(ev.fixed8(V747_ID, "reconstruction") / "render_summary.json"),
        "v747_generation": load_json(ev.fixed8(V747_ID, "generation") / CFG_DIR / "render_summary.json"),
        "v81a_manifest": load_json(ev.fixed8(V81A_ID, "comparison_manifest.json")),
        "v81a_reconstruction": load_json(ev.fixed8(V81A_ID, "reconstruction") / "render_summary.json"),
        "v81a_generation": load_json(ev.fixed8(V81A_ID, "generation") / CFG_DIR / "render_summary.json"),
    }


def fixed8_ids(summary_map: dict[str, dict], fixed_map: dict[str, dict]) -> list[str]:
    expected = sample_ids(summary_map)
    groups = []
    for key, payload in fixed_map.items():
        if key.endswith("_manifest"):
            groups.append([str(value) for value in payload.get("sample_ids", [])])
        else:
            groups.append([str(item["sample_id"]) for item in payload.get("samples", [])])
    if any(group != expected for group in groups):
        raise RuntimeError(f"fixed-8 assets do not match the ordered L0 single-step IDs: {groups}")
    return expected


def fixed8_active_metrics(ev: Evidence) -> str:
    systems = (
        ("L0 mainline · 105K", ev.eval(L0_ID, "human"), ev.eval(L0_ID, "camera"), ev.eval(L0_ID, "joint_parallel")),
        ("v7.47 system control · 105K", ev.v747_eval("human"), ev.v747_eval("camera"), ev.v747_eval("joint_parallel")),
        ("v8.1A diagnostic · 30K", ev.v81a_eval("human"), ev.v81a_eval("camera"), ev.v81a_eval("joint_parallel")),
    )
    payloads = [(label, load_json(h), load_json(c), load_json(j)) for label, h, c, j in systems]
    human_rows = [
        f"| {label} | {metric(human, 'test/tmr/ftd'):.3f} | "
        f"{metric(human, 'test/tmr/tmr_score'):.3f} | {100 * metric(human, 'test/tmr/coverage'):.2f}% |"
        for label, human, _, _ in payloads
    ]
    camera_rows = [
        f"| {label} | {metric(camera, 'test/clatr/fcd'):.3f} | "
        f"{metric(camera, 'test/clatr/clatr_score'):.3f} | {100 * metric(camera, 'test/clatr/coverage'):.2f}% | "
        f"{metric(camera, 'test/captions/fscore'):.3f} |"
        for label, _, camera, _ in payloads
    ]
    joint_rows = [
        f"| {label} | {metric(joint, 'test/tmr/ftd'):.3f} | {metric(joint, 'test/tmr/tmr_score'):.3f} | "
        f"{100 * metric(joint, 'test/tmr/coverage'):.2f}% | {metric(joint, 'test/clatr/fcd'):.3f} | "
        f"{metric(joint, 'test/clatr/clatr_score'):.3f} | {100 * metric(joint, 'test/clatr/coverage'):.2f}% | "
        f"{metric(joint, 'test/captions/fscore'):.3f} | {100 * metric(joint, 'test/proj/outscreen'):.2f}% |"
        for label, _, _, joint in payloads
    ]
    return "\n".join(
        [
            "**Stage1 reconstruction · formal pure-4,053 aggregate**",
            "",
            "| representation / owning decoder | H RA-MPJPE↓ | H global↓ | root ADE / FDE↓ | yaw↓ | Cam-ADE / FDE↓ | rotation↓ |",
            "| --- | ---: | ---: | ---: | ---: | ---: | ---: |",
            "| L0 · corrected v7.14 joint AE | 80.731 mm | 212.735 mm | 169.640 / 415.430 mm | 21.640° | 41.760 / 51.500 mm | 0.619° |",
            "| v7.47 · Pulp released official AE | 80.254 mm | 181.053 mm | 150.145 / 595.955 mm | — | 137.449 / 277.227 mm | 1.792° |",
            "| v8.1A · geometry-loss joint AE | 24.700 mm | 71.180 mm | 60.188 / 150.914 mm | 5.113° | 47.693 / 56.039 mm | 0.717° |",
            "",
            "**Direct-H · active formal metric**",
            "",
            "| version / run budget | FDTMR↓ | TMR↑ | HCov↑ |",
            "| --- | ---: | ---: | ---: |",
            *human_rows,
            "",
            "**Direct-C · active formal metric**",
            "",
            "| version / run budget | FDCLaTr↓ | CLaTr↑ | CCov↑ | Caption F1↑ |",
            "| --- | ---: | ---: | ---: | ---: |",
            *camera_rows,
            "",
            "**Joint parallel · active formal metric**",
            "",
            "| version / run budget | H FDTMR↓ | H TMR↑ | HCov↑ | C FDCLaTr↓ | C CLaTr↑ | CCov↑ | F1↑ | Out↓ |",
            "| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
            *joint_rows,
            "",
            "Stage2 rows share pure-4,053 IDs, DDIM50, CFG1, η0 and seed17, but the training budget is **105K / 105K / 30K**. "
            "The v8.1A row is a stopped diagnostic, not a same-budget promotion comparison. v7.47 is an audited system control; "
            "strict representation-only isolation from L0 was not established. Cascade is historical diagnostic evidence and is not an active evaluation standard.",
        ]
    )


def existing(path: Path) -> str | None:
    return str(path) if path.is_file() else None


def evidence_path(ev: Evidence, value: str) -> Path:
    path = Path(value)
    return path if path.is_absolute() else ev.root / path


def summaries(ev: Evidence) -> dict[str, dict]:
    return {
        "a_parallel": load_json(ev.summary(A_ID, "parallel")),
        "a_cascade": load_json(ev.summary(A_ID, "cascade")),
        "b_parallel": load_json(ev.summary(B_ID, "parallel")),
        "c_completion": load_json(ev.summary(C_ID, "completion")),
        "c_cascade": load_json(ev.summary(C_ID, "cascade")),
        "l0_parallel": load_json(ev.summary(L0_ID, "parallel", L0_VIS_GROUP)),
        "l0_cascade": load_json(ev.summary(L0_ID, "cascade", L0_VIS_GROUP)),
        "l0_completion": load_json(ev.summary(L0_ID, "completion", L0_DIRECT_VIS_GROUP)),
        "pulp_compare": load_json(ev.run(L0_ID) / "vis" / PULP_VIS_GROUP / "render_summary.json"),
        "single_step": load_json(ev.run(L0_ID) / "vis" / SINGLE_STEP_VIS_GROUP / "render_summary.json"),
        "humanml": load_json(ev.stage1_run(HUMANML_RUN_ID) / "vis" / HUMANML_VIS_GROUP / "render_summary.json"),
    }


def top_summary(ev: Evidence) -> dict:
    return load_json(ev.run(L0_ID) / "vis" / TOP_VIS_GROUP / "render_summary.json")


def top_pulp_summary(ev: Evidence) -> dict:
    return load_json(ev.run(L0_ID) / "vis" / TOP_PULP_VIS_GROUP / "render_summary.json")


def top_choices(summary: dict) -> list[tuple[str, str]]:
    labels = {"human_only": "Human only", "camera_only": "Camera only", "joint": "Joint"}
    choices = []
    for group in ("human_only", "camera_only", "joint"):
        for item in summary["rankings"]["groups"][group]:
            sample_id = str(item["sample_id"])
            value = f"{group}|{int(item['rank'])}|{sample_id}"
            choices.append((f"{labels[group]} · #{int(item['rank'])} · {sample_id}", value))
    return choices


def sample_ids(summary_map: dict[str, dict]) -> list[str]:
    groups = [
        [str(item["sample_id"]) for item in payload.get("samples", [])]
        for key, payload in summary_map.items()
        if key != "humanml"
    ]
    if not groups or not groups[0]:
        raise RuntimeError("render summaries contain no samples")
    if any(group != groups[0] for group in groups[1:]):
        raise RuntimeError(f"render sample IDs do not match: {groups}")
    return groups[0]


def humanml_for_l0(summary_map: dict[str, dict], sample_id: str) -> dict:
    return next(
        item
        for item in summary_map["humanml"]["samples"]
        if str(item.get("l0_reference_sample_id")) == sample_id
    )


def humanml_view(ev: Evidence, summary_map: dict[str, dict], sample_id: str):
    item = next(
        sample for sample in summary_map["humanml"]["samples"] if str(sample["sample_id"]) == sample_id
    )
    status = (
        f"### HumanML3D `{sample_id}` · {item['num_frames']} frames · fixed camera\n\n"
        f"**Text:** {item['caption']}  \n"
        f"**Split:** `{item['split']}` · **Paired:** `{str(item['paired']).lower()}` · "
        f"**v7.14 Stage1 joint MAE:** `{item['stage1_joint_mae']:.3f}` · "
        f"**normalized feature |z| max:** `{item['pulp_human199_normalized_abs_max']:.1f}`  \n"
        "Source and reconstruction use the same fixed-camera render control. This is an adapter diagnostic, not training-ready evidence."
    )
    return [
        status,
        existing(evidence_path(ev, item["fixed_camera_video"])),
        existing(evidence_path(ev, item["stage1_recon_fixed_camera_video"])),
    ]


def caption(summary: dict, sample_id: str) -> tuple[str, str, int | None]:
    item = next(sample for sample in summary["samples"] if str(sample["sample_id"]) == sample_id)
    return str(item.get("human_text", "")), str(item.get("camera_text", "")), item.get("valid_frames")


def video_name(task: str, view: str) -> str:
    suffix = "camera_projection.mp4" if view == "Camera projection" else "skeleton.mp4"
    return f"{task}_{suffix}"


def gt_name(view: str) -> str:
    return "gt_camera_projection.mp4" if view == "Camera projection" else "gt_skeleton.mp4"


def completion_view(ev: Evidence, summary_map: dict[str, dict], sample_id: str, task: str, view: str):
    human_text, camera_text, frames = caption(summary_map["a_parallel"], sample_id)
    roots = (
        ev.vis(A_ID, "parallel"),
        ev.vis(B_ID, "parallel"),
        ev.vis(C_ID, "completion"),
    )
    videos = [
        existing(roots[0] / sample_id / gt_name(view)),
        existing(roots[0] / sample_id / video_name(task, view)),
        existing(roots[1] / sample_id / video_name(task, view)),
        existing(roots[2] / sample_id / video_name(task, view)),
    ]
    images = [existing(root / sample_id / f"{task}_render.png") for root in roots]
    status = (
        f"### `{sample_id}` · {frames} frames · v7.36 step30k controls · `{task}` · {view}\n\n"
        f"**Human:** {human_text or 'unavailable'}  \n**Camera:** {camera_text or 'unavailable'}"
    )
    return [completion_metrics(ev, task), status, *videos, *images]


def joint_view(ev: Evidence, summary_map: dict[str, dict], sample_id: str, view: str):
    human_text, camera_text, frames = caption(summary_map["a_parallel"], sample_id)
    roots = (
        ev.vis(A_ID, "parallel"),
        ev.vis(A_ID, "cascade"),
        ev.vis(B_ID, "parallel"),
        ev.vis(C_ID, "cascade"),
    )
    videos = [
        existing(roots[0] / sample_id / gt_name(view)),
        *[existing(root / sample_id / video_name("joint", view)) for root in roots],
    ]
    images = [existing(root / sample_id / "joint_render.png") for root in roots]
    status = (
        f"### `{sample_id}` · {frames} frames · joint schedules · {view}\n\n"
        f"**Human:** {human_text or 'unavailable'}  \n**Camera:** {camera_text or 'unavailable'}"
    )
    return [joint_metrics(ev), status, *videos, *images]


def l0_view(ev: Evidence, summary_map: dict[str, dict], sample_id: str, view: str):
    human_text, camera_text, frames = caption(summary_map["l0_parallel"], sample_id)
    roots = (
        ev.vis(L0_ID, "parallel", L0_VIS_GROUP),
        ev.vis(L0_ID, "cascade", L0_VIS_GROUP),
    )
    videos = [
        existing(roots[0] / sample_id / gt_name(view)),
        *[existing(root / sample_id / video_name("joint", view)) for root in roots],
    ]
    images = [existing(root / sample_id / "joint_render.png") for root in roots]
    status = (
        f"### `{sample_id}` · {frames} frames · L0 schedules · {view}\n\n"
        f"**Human:** {human_text or 'unavailable'}  \n**Camera:** {camera_text or 'unavailable'}"
    )
    return [l0_metrics(ev), status, *videos, *images]


def l0_task_slice_view(ev: Evidence, summary_map: dict[str, dict], sample_id: str, task: str, view: str):
    human_text, camera_text, frames = caption(summary_map["l0_completion"], sample_id)
    completion_root = ev.vis(L0_ID, "completion", L0_DIRECT_VIS_GROUP)
    parallel_root = ev.vis(L0_ID, "parallel", L0_VIS_GROUP)
    cascade_root = ev.vis(L0_ID, "cascade", L0_VIS_GROUP)
    videos = [
        existing(completion_root / sample_id / gt_name(view)),
        existing(completion_root / sample_id / video_name(task, view)),
        existing(parallel_root / sample_id / video_name("joint", view)),
        existing(cascade_root / sample_id / video_name("joint", view)),
    ]
    images = [
        existing(completion_root / sample_id / f"{task}_render.png"),
        existing(parallel_root / sample_id / "joint_render.png"),
        existing(cascade_root / sample_id / "joint_render.png"),
    ]
    source_note = (
        "Direct human is human-text-only; no camera condition is consumed, and any projection uses GT camera only as an external display view."
        if task == "human"
        else "Direct camera observes GT human; parallel/cascade use generated human sources."
    )
    status = (
        f"### `{sample_id}` · {frames} frames · L0 step105k · `{task}` target · {view}\n\n"
        f"**Human:** {human_text or 'unavailable'}  \n**Camera:** {camera_text or 'unavailable'}  \n"
        f"{source_note} All generated columns use checkpoint `ab474d…f35`."
    )
    return [l0_task_slice_metrics(ev, task), status, *videos, *images]


def completion_peer_view(
    ev: Evidence,
    summary_map: dict[str, dict],
    registry: dict,
    sample_id: str,
    mode: str,
):
    if mode not in {"human", "camera"}:
        raise ValueError(f"unknown completion mode: {mode}")
    human_text, camera_text, frames = caption(summary_map["l0_completion"], sample_id)
    record = registry["modes"][mode]
    videos = []
    states = []
    for slot in record["slots"]:
        template = slot.get("path_template")
        path = None if not template else ev.root / str(template).format(sample_id=sample_id)
        resolved = existing(path) if path is not None else None
        videos.append(resolved)
        states.append(
            f"| {slot['label']} | {'ready' if resolved else slot.get('status', 'missing')} |"
        )
    target_note = (
        "Human target is human-text-only. Every ready clip uses the same fixed camera; camera text below is display-only paired context."
        if mode == "human"
        else "Camera target consumes complete GT-human latent plus camera text. Every generated camera is rendered on GT human."
    )
    status = "\n".join(
        [
            f"### `{sample_id}` · {frames} frames · {record['title']}",
            "",
            f"**Human text:** {human_text or 'unavailable'}  ",
            f"**Camera text:** {camera_text or 'unavailable'}  ",
            f"{target_note} {record['render_contract']}",
            "",
            "| visual slot | asset status |",
            "| --- | --- |",
            *states,
        ]
    )
    return [l0_task_slice_metrics(ev, mode), status, *videos]


def pulp_comparison_view(ev: Evidence, summary_map: dict[str, dict], sample_id: str, view: str):
    human_text, camera_text, frames = caption(summary_map["pulp_compare"], sample_id)
    comparison_root = ev.run(L0_ID) / "vis" / PULP_VIS_GROUP
    l0_parallel = ev.vis(L0_ID, "parallel", L0_VIS_GROUP)
    l0_direct = ev.vis(L0_ID, "completion", L0_DIRECT_VIS_GROUP)
    suffix = "joint_camera_projection.mp4" if view == "Camera projection" else "joint_skeleton.mp4"
    videos = [
        existing(comparison_root / "gt" / sample_id / gt_name(view)),
        existing(comparison_root / "stage1_identity" / sample_id / suffix),
        existing(l0_parallel / sample_id / suffix),
        existing(l0_direct / sample_id / video_name("human", view)),
        existing(comparison_root / "pulp_no_aux" / sample_id / suffix),
        existing(comparison_root / "pulp_aux" / sample_id / suffix),
    ]
    images = [
        existing(comparison_root / "stage1_identity" / sample_id / "joint_render.png"),
        existing(l0_parallel / sample_id / "joint_render.png"),
        existing(l0_direct / sample_id / "human_render.png"),
        existing(comparison_root / "pulp_no_aux" / sample_id / "joint_render.png"),
        existing(comparison_root / "pulp_aux" / sample_id / "joint_render.png"),
    ]
    status = (
        f"### `{sample_id}` · {frames} frames · Stage1/L0/Pulp · {view}\n\n"
        f"**Human:** {human_text or 'unavailable'}  \n**Camera:** {camera_text or 'unavailable'}  \n"
        "Direct H is human-text-only; its camera-projection view uses dataset GT camera only as an external display camera, not as model conditioning. "
        "Stage1 identity isolates the tokenizer ceiling. Pulp no-Aux/Aux share the released checkpoint and per-sample noise seed."
    )
    return [pulp_comparison_metrics(ev, summary_map), status, *videos, *images]


def top_sample_view(ev: Evidence, summary: dict, pulp_summary: dict, selection: str, view: str):
    group, rank_text, sample_id = selection.split("|", 2)
    rank = int(rank_text)
    ranking = next(
        item
        for item in summary["rankings"]["groups"][group]
        if int(item["rank"]) == rank and str(item["sample_id"]) == sample_id
    )
    sample = next(item for item in summary["samples"] if str(item["sample_id"]) == sample_id)
    pulp_sample = next(item for item in pulp_summary["samples"] if str(item["sample_id"]) == sample_id)
    view_key = "camera_projection" if view == "Camera projection" else "skeleton"
    videos = [
        existing(evidence_path(ev, sample["grid"]["storymotion"][column][view_key]))
        for column in ("gt", "recon", "gen")
    ] + [
        existing(evidence_path(ev, sample["grid"]["specialist"]["gen"][view_key])),
        existing(evidence_path(ev, pulp_sample["grid"]["pulp"]["recon"][view_key])),
        existing(evidence_path(ev, pulp_sample["grid"]["pulp"]["gen"][view_key])),
    ]
    quality_rows = []
    for label, record in (
        ("StoryMotion · GT", sample["quality"]["gt"]),
        ("StoryMotion · recon", sample["quality"]["stage1_identity"]),
        ("StoryMotion · gen", sample["quality"]["l0_parallel"]),
        ("v7.42 joint specialist · gen", sample["quality"]["specialist_parallel"]),
        ("Pulp official · recon", pulp_sample["quality"]["pulp_identity"]),
        ("Pulp official · gen (Aux)", pulp_sample["quality"]["pulp_aux"]),
    ):
        quality_rows.append(
            f"| {label} | {record['human_root_aligned_mpjpe']:.3f} | "
            f"{record['camera_center_ade']:.3f} | {record['human_tmr_score']:.2f} | "
            f"{record['camera_clatr_score']:.2f} | {100 * record['in_frame_rate']:.1f}% |"
        )
    group_label = {"human_only": "Human only", "camera_only": "Camera only", "joint": "Joint"}[group]
    metric_text = "\n".join(
        [
            "**Paired-GT geometry ranking · same pure sample**",
            "",
            "| system / column | H-MPJPE↓ | Cam-ADE↓ | TMR†↑ | CLaTr†↑ | In-frame†↑ |",
            "| --- | ---: | ---: | ---: | ---: | ---: |",
            *quality_rows,
            "",
            "Ranking uses only StoryMotion L0 joint-parallel H-MPJPE and Cam-ADE. † columns are display-only and do not affect selection.",
            "",
            "**Official pure-4,053 aggregate comparison**",
            "",
            "| version / run | FDTMR↓ | TMR↑ | HCov↑ | FDCLaTr↓ | CLaTr↑ | CCov↑ | F1↑ | Out↓ |",
            "| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
            *top_aggregate_rows(ev, pulp_summary),
        ]
    )
    status = (
        f"### {group_label} Top-5 · #{rank} · `{sample_id}` · {sample['valid_frames']} frames · {view}\n\n"
        f"**Human text:** {sample['human_text'] or 'unavailable'}  \n"
        f"**Camera text:** {sample['camera_text'] or 'unavailable'}  \n"
        f"**StoryMotion ranking score:** `{ranking['ranking_scores'][group]:.4f}` · "
        f"H-MPJPE `{ranking['human_root_aligned_mpjpe']:.3f}` · "
        f"Cam-ADE `{ranking['camera_center_ade']:.3f}`  \n"
        "Human-only ranks H-MPJPE; camera-only ranks camera-center ADE; joint equally combines their reverse percentiles. "
        "Text similarity and in-frame statistics do not affect selection. No length filter is applied. "
        "The second row is intentionally hybrid: specialist generation, Pulp AE reconstruction, and Pulp Aux generation."
    )
    return [metric_text, status, *videos]


def single_step_view(ev: Evidence, summary_map: dict[str, dict], sample_id: str, task: str, view: str):
    human_text, camera_text, frames = caption(summary_map["single_step"], sample_id)
    task_root = ev.run(L0_ID) / "vis" / SINGLE_STEP_VIS_GROUP / task / sample_id
    suffix = "camera_projection.mp4" if view == "Camera projection" else "skeleton.mp4"
    videos = [
        existing(task_root / f"gt_{suffix}"),
        *[existing(task_root / f"t{timestep}_{suffix}") for timestep in SINGLE_STEP_TIMESTEPS],
    ]
    images = [existing(task_root / f"t{timestep}_render.png") for timestep in SINGLE_STEP_TIMESTEPS]
    source_note = {
        "human": "Direct-H is human-text-only; no camera condition is consumed, and camera projection uses GT camera only as an external display view.",
        "camera": "Camera predicts C from GT human plus camera text.",
        "joint": "Joint predicts H/C in one teacher-forced forward from the same noised GT latent.",
    }[task]
    status = (
        f"### `{sample_id}` · {frames} frames · `{task}` · {view}\n\n"
        f"**Human:** {human_text or 'unavailable'}  \n**Camera:** {camera_text or 'unavailable'}  \n"
        f"{source_note} Every `t` column is `q(z_gt,t) → one pred_x0`; it is not a partial DDIM trajectory."
    )
    return [single_step_metrics(ev, task), status, *videos, *images]


def fixed8_view(
    ev: Evidence,
    summary_map: dict[str, dict],
    fixed_map: dict[str, dict],
    sample_id: str,
    view: str,
):
    human_text, camera_text, frames = caption(summary_map["l0_parallel"], sample_id)
    suffix = "joint_camera_projection.mp4" if view == "Camera projection" else "joint_skeleton.mp4"
    gt_suffix = "gt_camera_projection.mp4" if view == "Camera projection" else "gt_skeleton.mp4"
    l0_generation = ev.vis(L0_ID, "parallel", L0_VIS_GROUP)
    l0_reconstruction = ev.run(L0_ID) / "vis" / PULP_VIS_GROUP / "stage1_identity"
    v747_reconstruction = ev.fixed8(V747_ID, "reconstruction")
    v747_generation = ev.fixed8(V747_ID, "generation") / CFG_DIR
    v81a_reconstruction = ev.fixed8(V81A_ID, "reconstruction")
    v81a_generation = ev.fixed8(V81A_ID, "generation") / CFG_DIR
    videos = [
        existing(l0_generation / sample_id / gt_suffix),
        existing(l0_reconstruction / sample_id / suffix),
        existing(v747_reconstruction / sample_id / suffix),
        existing(v81a_reconstruction / sample_id / suffix),
        existing(l0_generation / sample_id / gt_suffix),
        existing(l0_generation / sample_id / suffix),
        existing(v747_generation / sample_id / suffix),
        existing(v81a_generation / sample_id / suffix),
    ]
    v747_protocol = fixed_map["v747_manifest"]["qualitative_protocol"]
    v81a_protocol = fixed_map["v81a_manifest"]["qualitative_protocol"]
    if v747_protocol != v81a_protocol:
        raise RuntimeError("v7.47 and v8.1A fixed-8 renders use different qualitative protocols")
    status = (
        f"### L0 single-step ID `{sample_id}` · {frames} frames · {view}\n\n"
        f"**Human text:** {human_text or 'unavailable'}  \n"
        f"**Camera text:** {camera_text or 'unavailable'}  \n"
        "第一行是同一 GT 与三种 owning-decoder joint reconstruction；第二行是同一 GT 与三个 Unified-3 joint-parallel generations。 "
        "Stage2 budget 为 `105K / 105K / 30K`。  \n"
        f"**Qualitative protocol:** {v747_protocol}。这些 clip 使用固定 ID 顺序下的 ordinal-seed renderer，"
        "不等同于 formal pure4053 的逐样本采样轨迹，也不产生或替换正式指标。"
    )
    return [fixed8_active_metrics(ev), status, *videos]


def validate(ev: Evidence) -> dict[str, int]:
    summary_map = summaries(ev)
    ids = sample_ids(summary_map)
    fixed_map = fixed8_summaries(ev)
    fixed_ids = fixed8_ids(summary_map, fixed_map)
    ranked_summary = top_summary(ev)
    pulp_ranked_summary = top_pulp_summary(ev)
    completion_registry = load_completion_registry(ev)
    required = []
    for run_id, name in (
        (A_ID, "human"), (A_ID, "camera"), (A_ID, "joint_parallel"), (A_ID, "joint_cascade"),
        (B_ID, "human"), (B_ID, "camera"), (B_ID, "joint_parallel"),
        (C_ID, "human"), (C_ID, "camera"), (C_ID, "joint_cascade"),
        (L0_ID, "human"), (L0_ID, "camera"), (L0_ID, "joint_parallel"), (L0_ID, "joint_cascade"),
        (JOINT_SPECIALIST_ID, "joint_parallel"),
    ):
        required.append(ev.eval(run_id, name))
    required.extend(ev.v747_eval(name) for name in ("human", "camera", "joint_parallel"))
    required.extend(ev.v81a_eval(name) for name in ("human", "camera", "joint_parallel"))
    for task in ("human", "camera", "joint"):
        required.append(ev.single_step_eval(task, "raw_gt"))
        required.extend(ev.single_step_eval(task, f"t{timestep}") for timestep in SINGLE_STEP_TIMESTEPS)
    render_specs = (
        (A_ID, P0_VIS_GROUP, "parallel", ("camera", "human", "joint")),
        (A_ID, P0_VIS_GROUP, "cascade", ("joint",)),
        (B_ID, P0_VIS_GROUP, "parallel", ("camera", "human", "joint")),
        (C_ID, P0_VIS_GROUP, "completion", ("camera", "human")),
        (C_ID, P0_VIS_GROUP, "cascade", ("joint",)),
        (L0_ID, L0_VIS_GROUP, "parallel", ("joint",)),
        (L0_ID, L0_VIS_GROUP, "cascade", ("joint",)),
        (L0_ID, L0_DIRECT_VIS_GROUP, "completion", ("human", "camera")),
    )
    for run_id, group, schedule, tasks in render_specs:
        root = ev.vis(run_id, schedule, group)
        for sample_id in ids:
            required.extend((root / sample_id / "gt_skeleton.mp4", root / sample_id / "gt_camera_projection.mp4"))
            for task in tasks:
                required.extend(
                    (
                        root / sample_id / f"{task}_skeleton.mp4",
                        root / sample_id / f"{task}_camera_projection.mp4",
                        root / sample_id / f"{task}_render.png",
                    )
                )
    comparison_root = ev.run(L0_ID) / "vis" / PULP_VIS_GROUP
    for sample_id in ids:
        required.extend(
            (
                comparison_root / "gt" / sample_id / "gt_skeleton.mp4",
                comparison_root / "gt" / sample_id / "gt_camera_projection.mp4",
            )
        )
        for variant in ("stage1_identity", "pulp_no_aux", "pulp_aux"):
            required.extend(
                (
                    comparison_root / variant / sample_id / "joint_skeleton.mp4",
                    comparison_root / variant / sample_id / "joint_camera_projection.mp4",
                    comparison_root / variant / sample_id / "joint_render.png",
                )
            )
    single_step_root = ev.run(L0_ID) / "vis" / SINGLE_STEP_VIS_GROUP
    for sample_id in ids:
        for task in ("human", "camera", "joint"):
            task_root = single_step_root / task / sample_id
            required.extend((task_root / "gt_skeleton.mp4", task_root / "gt_camera_projection.mp4"))
            for timestep in SINGLE_STEP_TIMESTEPS:
                required.extend(
                    (
                        task_root / f"t{timestep}_skeleton.mp4",
                        task_root / f"t{timestep}_camera_projection.mp4",
                        task_root / f"t{timestep}_render.png",
                    )
                )
        humanml = humanml_for_l0(summary_map, sample_id)
        required.extend(
            (
                evidence_path(ev, humanml["fixed_camera_video"]),
                evidence_path(ev, humanml["first_frame_png"]),
                evidence_path(ev, humanml["stage1_recon_fixed_camera_video"]),
                evidence_path(ev, humanml["stage1_recon_fixed_camera_first_frame_png"]),
                evidence_path(ev, humanml["joints_npz"]),
            )
        )
    expected_fixed8 = {
        "v747_manifest": (V747_ID, 105000, "b8c06913a5efdbaa0c178e452998352033174614aa0a60ad96920fe14a8acbb2"),
        "v81a_manifest": (V81A_ID, 30000, "becc2c11051bfd7857acb0602f61c755cd664969f34acef1f0232711feee5bb8"),
    }
    for key, (run_id, budget, checkpoint_sha256) in expected_fixed8.items():
        manifest = fixed_map[key]
        if manifest.get("status") != "completed":
            raise RuntimeError(f"{key} is not completed")
        if manifest.get("run_id") != run_id or int(manifest["stage2"]["budget_steps"]) != budget:
            raise RuntimeError(f"{key} has the wrong source run or Stage2 budget")
        if manifest["stage2"].get("checkpoint_sha256") != checkpoint_sha256:
            raise RuntimeError(f"{key} checkpoint does not match the audited source")
        if manifest["stage2"].get("sampler") != {"cfg_scale": 1.0, "eta": 0.0, "seed": 17, "steps": 50}:
            raise RuntimeError(f"{key} sampler is not DDIM50 / CFG1 / eta0 / seed17")
        if manifest.get("formal_metric_samples") != 4053 or manifest.get("render_samples") != 8:
            raise RuntimeError(f"{key} formal/render sample counts are invalid")
        if "not formal matched" not in str(manifest.get("qualitative_protocol", "")):
            raise RuntimeError(f"{key} does not declare the ordinal-seed qualitative boundary")
    for sample_id in fixed_ids:
        for run_id in (V747_ID, V81A_ID):
            reconstruction = ev.fixed8(run_id, "reconstruction") / sample_id
            generation = ev.fixed8(run_id, "generation") / CFG_DIR / sample_id
            required.extend(
                (
                    reconstruction / "gt_skeleton.mp4",
                    reconstruction / "gt_camera_projection.mp4",
                    reconstruction / "joint_skeleton.mp4",
                    reconstruction / "joint_camera_projection.mp4",
                    reconstruction / "joint_render.png",
                    generation / "gt_skeleton.mp4",
                    generation / "gt_camera_projection.mp4",
                    generation / "joint_skeleton.mp4",
                    generation / "joint_camera_projection.mp4",
                    generation / "joint_render.png",
                )
            )
    for record in completion_registry["modes"].values():
        for slot in record["slots"]:
            if slot.get("status") != "ready":
                continue
            template = slot.get("path_template")
            if not template:
                raise RuntimeError(f"ready completion slot has no path template: {slot['label']}")
            required.extend(ev.root / str(template).format(sample_id=sample_id) for sample_id in ids)
    if ranked_summary.get("rankings") is None:
        raise RuntimeError("Top-5 comparison summary is missing ranking provenance")
    ranked_ids = [str(sample["sample_id"]) for sample in ranked_summary.get("samples", [])]
    pulp_ranked_ids = [str(sample["sample_id"]) for sample in pulp_ranked_summary.get("samples", [])]
    if ranked_ids != pulp_ranked_ids:
        raise RuntimeError("specialist and Pulp Top-5 summaries use different sample IDs or order")
    pulp_by_id = {str(sample["sample_id"]): sample for sample in pulp_ranked_summary["samples"]}
    for sample in ranked_summary.get("samples", []):
        sample_id = str(sample["sample_id"])
        pulp_sample = pulp_by_id[sample_id]
        for column in ("gt", "recon", "gen"):
            for view_key in ("skeleton", "camera_projection"):
                required.append(evidence_path(ev, sample["grid"]["storymotion"][column][view_key]))
        for view_key in ("skeleton", "camera_projection"):
            required.append(evidence_path(ev, sample["grid"]["specialist"]["gen"][view_key]))
            required.append(evidence_path(ev, pulp_sample["grid"]["pulp"]["recon"][view_key]))
            required.append(evidence_path(ev, pulp_sample["grid"]["pulp"]["gen"][view_key]))
    missing = [path for path in required if not path.is_file()]
    if missing:
        preview = "\n".join(str(path) for path in missing[:20])
        raise RuntimeError(f"missing {len(missing)} required evidence files:\n{preview}")
    return {
        "runs": 4,
        "summaries": len(summary_map),
        "samples": len(ids),
        "completion_modes": len(completion_registry["modes"]),
        "top_samples": len(ranked_summary.get("samples", [])),
        "top_sources": 2,
        "fixed8_samples": len(fixed_ids),
        "fixed8_systems": 3,
        "required_files": len(required),
        "missing": 0,
    }


def build_demo(ev: Evidence):
    import gradio as gr

    summary_map = summaries(ev)
    ids = sample_ids(summary_map)
    fixed_map = fixed8_summaries(ev)
    fixed_ids = fixed8_ids(summary_map, fixed_map)
    completion_registry = load_completion_registry(ev)
    ranked_summary = top_summary(ev)
    pulp_ranked_summary = top_pulp_summary(ev)
    ranked_choices = top_choices(ranked_summary)
    humanml_ids = [str(item["sample_id"]) for item in summary_map["humanml"]["samples"]]

    def video_grid(labels: tuple[str, ...], columns: int | None = None) -> list:
        play = gr.Button("▶ 同步播放当前组", variant="primary", elem_classes="sync-play")
        play.click(fn=None, js=SYNC_PLAY_JS)
        videos = []
        columns = columns or (2 if len(labels) in {2, 4} else 3)
        for start in range(0, len(labels), columns):
            with gr.Row(elem_classes=["evidence-row", f"evidence-cols-{columns}"]):
                for label in labels[start : start + columns]:
                    with gr.Column():
                        gr.Markdown(f"### {label}")
                        videos.append(gr.Video(show_label=False, format="mp4"))
        return videos

    with gr.Blocks(title="StoryMotion Unified-3 evidence") as demo:
        gr.Markdown("# StoryMotion · Unified-3 evidence desk", elem_id="hero")
        gr.Markdown(
            "**当前裁决：L0 clean-105k 是 single-seed E0 主线。** "
            "Top-5 tab 从同一 L0 joint-parallel pure4053 输出按 paired-GT H-MPJPE/Cam-ADE 排序，"
            "第二行依次展示 v7.42 joint specialist generation、Pulp reconstruction 与 Pulp Aux generation；"
            "文本相似度与 set-level FID/coverage 不用于逐样本排名。Cascade 只保留为历史诊断，不再参与 promotion。",
            elem_classes="verdict",
        )
        with gr.Tabs():
            for mode, tab_name in (("human", "Human completion"), ("camera", "Camera completion")):
                record = completion_registry["modes"][mode]
                with gr.Tab(tab_name):
                    peer_sample = gr.Dropdown(ids, value=ids[0], label="Sample")
                    peer_metric = gr.Markdown(elem_classes="metric-strip")
                    peer_status = gr.Markdown()
                    peer_videos = video_grid(tuple(slot["label"] for slot in record["slots"]))
                    peer_outputs = [peer_metric, peer_status, *peer_videos]
                    peer_callback = (
                        lambda sample_id, selected_mode=mode: completion_peer_view(
                            ev, summary_map, completion_registry, sample_id, selected_mode
                        )
                    )
                    peer_sample.change(peer_callback, peer_sample, peer_outputs)
                    demo.load(peer_callback, peer_sample, peer_outputs)

            with gr.Tab("Joint Top-5 · 2×3"):
                with gr.Row():
                    top_sample = gr.Dropdown(
                        ranked_choices,
                        value=ranked_choices[0][1],
                        label="Dimension / rank / sample",
                    )
                    top_render = gr.Radio(
                        ("Camera projection", "World skeleton"),
                        value="Camera projection",
                        label="View",
                    )
                top_metric = gr.Markdown(elem_classes="metric-strip")
                top_status = gr.Markdown()
                top_videos = video_grid(
                    (
                        "StoryMotion · GT",
                        "StoryMotion · recon",
                        "StoryMotion · gen",
                        "v7.42 joint specialist · gen",
                        "Pulp official · recon",
                        "Pulp official · gen (Aux)",
                    )
                )
                top_outputs = [top_metric, top_status, *top_videos]
                top_inputs = [top_sample, top_render]
                top_callback = lambda selection, view: top_sample_view(
                    ev, ranked_summary, pulp_ranked_summary, selection, view
                )
                top_sample.change(top_callback, top_inputs, top_outputs)
                top_render.change(top_callback, top_inputs, top_outputs)
                demo.load(top_callback, top_inputs, top_outputs)

            with gr.Tab("L0 vs Pulp official"):
                with gr.Row():
                    compare_sample = gr.Dropdown(ids, value=ids[0], label="Sample")
                    compare_render = gr.Radio(("Camera projection", "World skeleton"), value="Camera projection", label="View")
                compare_metric = gr.Markdown(elem_classes="metric-strip")
                compare_status = gr.Markdown()
                compare_videos = video_grid(
                    (
                        "GT",
                        "v7.14 · Stage1 reconstruction",
                        "L0 · parallel",
                        "L0 · Direct H (human-text-only)",
                        "Pulp official · no-Aux",
                        "Pulp official · Aux",
                    )
                )
                gr.Markdown("### Geometry audit · camera and root trajectories")
                compare_images = []
                with gr.Row(elem_classes="geometry-row"):
                    for label in (
                        "Stage1 reconstruction",
                        "L0 · parallel",
                        "L0 · Direct H",
                        "Pulp · no-Aux",
                        "Pulp · Aux",
                    ):
                        with gr.Column():
                            gr.Markdown(f"#### {label}")
                            compare_images.append(gr.Image(show_label=False, type="filepath"))
                compare_outputs = [compare_metric, compare_status, *compare_videos, *compare_images]
                compare_inputs = [compare_sample, compare_render]
                compare_callback = lambda sample_id, view: pulp_comparison_view(ev, summary_map, sample_id, view)
                compare_sample.change(compare_callback, compare_inputs, compare_outputs)
                compare_render.change(compare_callback, compare_inputs, compare_outputs)
                demo.load(compare_callback, compare_inputs, compare_outputs)

            with gr.Tab("L0 single-step diagnostic"):
                with gr.Row():
                    gate_sample = gr.Dropdown(ids, value=ids[0], label="Sample")
                    gate_task = gr.Radio(("human", "camera", "joint"), value="human", label="Generated target")
                    gate_render = gr.Radio(("Camera projection", "World skeleton"), value="World skeleton", label="View")
                gate_metric = gr.Markdown(elem_classes="metric-strip")
                gate_status = gr.Markdown()
                gate_videos = video_grid(("Raw GT", "t = 999", "t = 799", "t = 599", "t = 399", "t = 199"))
                gr.Markdown("### One-step decoded geometry · same deterministic per-sample noise")
                gate_images = []
                with gr.Row(elem_classes="geometry-row"):
                    for timestep in SINGLE_STEP_TIMESTEPS:
                        with gr.Column():
                            gr.Markdown(f"#### t = {timestep}")
                            gate_images.append(gr.Image(show_label=False, type="filepath"))
                gate_outputs = [gate_metric, gate_status, *gate_videos, *gate_images]
                gate_inputs = [gate_sample, gate_task, gate_render]
                gate_callback = lambda sample_id, task, view: single_step_view(ev, summary_map, sample_id, task, view)
                gate_sample.change(gate_callback, gate_inputs, gate_outputs)
                gate_task.change(gate_callback, gate_inputs, gate_outputs)
                gate_render.change(gate_callback, gate_inputs, gate_outputs)
                demo.load(gate_callback, gate_inputs, gate_outputs)

            with gr.Tab("L0 fixed-8 · 2×4"):
                with gr.Row():
                    fixed_sample = gr.Dropdown(fixed_ids, value=fixed_ids[0], label="L0 single-step sample")
                    fixed_render = gr.Radio(
                        ("Camera projection", "World skeleton"),
                        value="Camera projection",
                        label="View",
                    )
                fixed_metric = gr.Markdown(elem_classes="metric-strip")
                fixed_status = gr.Markdown()
                fixed_videos = video_grid(
                    (
                        "GT · reconstruction reference",
                        "L0 · v7.14 recon",
                        "v7.47 · official AE recon",
                        "v8.1A · recon",
                        "GT · generation reference",
                        "L0 · 105K parallel gen",
                        "v7.47 · 105K parallel gen",
                        "v8.1A · 30K parallel gen",
                    ),
                    columns=4,
                )
                fixed_outputs = [fixed_metric, fixed_status, *fixed_videos]
                fixed_inputs = [fixed_sample, fixed_render]
                fixed_callback = lambda sample_id, view: fixed8_view(
                    ev, summary_map, fixed_map, sample_id, view
                )
                fixed_sample.change(fixed_callback, fixed_inputs, fixed_outputs)
                fixed_render.change(fixed_callback, fixed_inputs, fixed_outputs)
                demo.load(fixed_callback, fixed_inputs, fixed_outputs)

            with gr.Tab("L0 schedules"):
                with gr.Row():
                    l0_sample = gr.Dropdown(ids, value=ids[0], label="Sample")
                    l0_render = gr.Radio(("Camera projection", "World skeleton"), value="Camera projection", label="View")
                l0_metric = gr.Markdown(elem_classes="metric-strip")
                l0_status = gr.Markdown()
                l0_videos = video_grid(("GT", "L0 · directed parallel", "L0 · human-first cascade"))
                gr.Markdown("### Geometry audit · camera and root trajectories")
                l0_images = []
                with gr.Row(elem_classes="geometry-row"):
                    for label in ("L0 · directed parallel", "L0 · human-first cascade"):
                        with gr.Column():
                            gr.Markdown(f"#### {label}")
                            l0_images.append(gr.Image(show_label=False, type="filepath"))
                l0_outputs = [l0_metric, l0_status, *l0_videos, *l0_images]
                l0_inputs = [l0_sample, l0_render]
                l0_callback = lambda sample_id, view: l0_view(ev, summary_map, sample_id, view)
                l0_sample.change(l0_callback, l0_inputs, l0_outputs)
                l0_render.change(l0_callback, l0_inputs, l0_outputs)
                demo.load(l0_callback, l0_inputs, l0_outputs)

            with gr.Tab("HumanML3D"):
                humanml_sample = gr.Dropdown(humanml_ids, value=humanml_ids[0], label="HumanML3D sample")
                humanml_status = gr.Markdown()
                humanml_videos = video_grid(
                    ("HumanML3D source · fixed camera", "HumanML3D → v7.14 Stage1 · fixed camera")
                )
                humanml_outputs = [humanml_status, *humanml_videos]
                humanml_callback = lambda sample_id: humanml_view(ev, summary_map, sample_id)
                humanml_sample.change(humanml_callback, humanml_sample, humanml_outputs)
                demo.load(humanml_callback, humanml_sample, humanml_outputs)

            with gr.Tab("Joint schedules"):
                with gr.Row():
                    joint_sample = gr.Dropdown(ids, value=ids[0], label="Sample")
                    joint_render = gr.Radio(("Camera projection", "World skeleton"), value="Camera projection", label="View")
                joint_metric = gr.Markdown(elem_classes="metric-strip")
                joint_status = gr.Markdown()
                joint_videos = video_grid(("GT", "A · parallel", "A · cascade", "B · symmetric", "C · no-joint cascade"))
                gr.Markdown("### Geometry audit · camera and root trajectories")
                joint_images = []
                with gr.Row(elem_classes="geometry-row"):
                    for label in ("A · parallel", "A · cascade", "B · symmetric", "C · no-joint cascade"):
                        with gr.Column():
                            gr.Markdown(f"#### {label}")
                            joint_images.append(gr.Image(show_label=False, type="filepath"))
                joint_outputs = [joint_metric, joint_status, *joint_videos, *joint_images]
                joint_inputs = [joint_sample, joint_render]
                callback = lambda sample_id, view: joint_view(ev, summary_map, sample_id, view)
                joint_sample.change(callback, joint_inputs, joint_outputs)
                joint_render.change(callback, joint_inputs, joint_outputs)
                demo.load(callback, joint_inputs, joint_outputs)

            with gr.Tab("L0 task slices"):
                with gr.Row():
                    l0_task_sample = gr.Dropdown(ids, value=ids[0], label="Sample")
                    l0_task = gr.Radio(("human", "camera"), value="human", label="Generated target")
                    l0_task_render = gr.Radio(("Camera projection", "World skeleton"), value="World skeleton", label="View")
                l0_task_metric = gr.Markdown(elem_classes="metric-strip")
                l0_task_status = gr.Markdown()
                l0_task_videos = video_grid(("GT", "L0 · direct task", "L0 · joint parallel", "L0 · joint cascade"))
                gr.Markdown("### Geometry audit · camera and root trajectories")
                l0_task_images = []
                with gr.Row(elem_classes="geometry-row"):
                    for label in ("L0 · direct task", "L0 · joint parallel", "L0 · joint cascade"):
                        with gr.Column():
                            gr.Markdown(f"#### {label}")
                            l0_task_images.append(gr.Image(show_label=False, type="filepath"))
                l0_task_outputs = [l0_task_metric, l0_task_status, *l0_task_videos, *l0_task_images]
                l0_task_inputs = [l0_task_sample, l0_task, l0_task_render]
                l0_task_callback = lambda sample_id, task, view: l0_task_slice_view(ev, summary_map, sample_id, task, view)
                l0_task_sample.change(l0_task_callback, l0_task_inputs, l0_task_outputs)
                l0_task.change(l0_task_callback, l0_task_inputs, l0_task_outputs)
                l0_task_render.change(l0_task_callback, l0_task_inputs, l0_task_outputs)
                demo.load(l0_task_callback, l0_task_inputs, l0_task_outputs)

            with gr.Tab("v7.36 controls"):
                with gr.Row():
                    completion_sample = gr.Dropdown(ids, value=ids[0], label="Sample")
                    completion_task = gr.Radio(("human", "camera"), value="human", label="Generated target")
                    completion_render = gr.Radio(("Camera projection", "World skeleton"), value="World skeleton", label="View")
                completion_metric = gr.Markdown(elem_classes="metric-strip")
                completion_status = gr.Markdown()
                completion_videos = video_grid(("GT", "A · asymmetric + joint", "B · symmetric", "C · asymmetric no-joint"))
                gr.Markdown("### Geometry audit · camera and root trajectories")
                completion_images = []
                with gr.Row(elem_classes="geometry-row"):
                    for label in ("A", "B", "C"):
                        with gr.Column():
                            gr.Markdown(f"#### {label}")
                            completion_images.append(gr.Image(show_label=False, type="filepath"))
                completion_outputs = [completion_metric, completion_status, *completion_videos, *completion_images]
                completion_inputs = [completion_sample, completion_task, completion_render]
                completion_callback = lambda sample_id, task, view: completion_view(ev, summary_map, sample_id, task, view)
                completion_sample.change(completion_callback, completion_inputs, completion_outputs)
                completion_task.change(completion_callback, completion_inputs, completion_outputs)
                completion_render.change(completion_callback, completion_inputs, completion_outputs)
                demo.load(completion_callback, completion_inputs, completion_outputs)
    return demo


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=DEFAULT_ROOT)
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=7865)
    parser.add_argument("--validate-only", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    ev = Evidence(args.root.resolve())
    if args.validate_only:
        print(json.dumps(validate(ev), indent=2, sort_keys=True))
        return 0
    demo = build_demo(ev)
    allowed = [str(ev.run(run_id).resolve()) for run_id in (A_ID, B_ID, C_ID, L0_ID)]
    allowed.extend(str(ev.canonical_vis(run_id).resolve()) for run_id in (V747_ID, V81A_ID))
    allowed.append(str(ev.stage1_run(HUMANML_RUN_ID).resolve()))
    demo.launch(server_name=args.host, server_port=args.port, share=False, allowed_paths=allowed, css=CSS)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
