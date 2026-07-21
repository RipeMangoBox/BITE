#!/usr/bin/env python3
"""Serve the C3-25 completion, joint Top-5, and single-step evidence desk."""
from __future__ import annotations

import argparse
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
HUMANML_RUN_ID = "v7_40_humanml3d_adapter_vis_20260715"
HUMANML_VIS_GROUP = "humanml3d_stage1_adapted_20260715"
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


def load_json(path: Path) -> dict[str, Any]:
    if not path.is_file():
        raise FileNotFoundError(f"missing required artifact: {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def existing(path: Path) -> str | None:
    return str(path) if path.is_file() else None


def evidence_path(ev: Evidence, value: str) -> Path:
    path = Path(value)
    return path if path.is_absolute() else ev.root / path


def metric(payload: dict[str, Any], key: str) -> float:
    value = payload.get("metrics", {}).get(key)
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


def completion_metrics(ev: Evidence, task: str) -> str:
    c325 = load_json(ev.c325_metric(task))
    l0 = load_json(ev.l0_metric(task))
    split, count = eval_scope(c325)
    if task == "human":
        header = (
            "| version / run | FDTMR↓ | TMR↑ | HCov↑ |",
            "| --- | ---: | ---: | ---: |",
        )
        rows = [
            f"| C3-25 / `{C325_ID}` | {number(metric(c325, 'test/tmr/ftd'), 2)} | "
            f"{number(metric(c325, 'test/tmr/tmr_score'))} | {number(metric(c325, 'test/tmr/coverage'), percent=True)} |",
            f"| v7.38 L0 / `{L0_ID}` | {number(metric(l0, 'test/tmr/ftd'), 2)} | "
            f"{number(metric(l0, 'test/tmr/tmr_score'))} | {number(metric(l0, 'test/tmr/coverage'), percent=True)} |",
        ]
        contract = "Direct-H is human-text-only; camera text is paired display context and is not consumed."
    else:
        header = (
            "| version / run | FDCLaTr↓ | CLaTr↑ | CCov↑ | Caption F1↑ |",
            "| --- | ---: | ---: | ---: | ---: |",
        )
        rows = [
            f"| C3-25 / `{C325_ID}` | {number(metric(c325, 'test/clatr/fcd'), 2)} | "
            f"{number(metric(c325, 'test/clatr/clatr_score'))} | "
            f"{number(metric(c325, 'test/clatr/coverage'), percent=True)} | "
            f"{number(metric(c325, 'test/captions/fscore'))} |",
            f"| v7.38 L0 / `{L0_ID}` | {number(metric(l0, 'test/clatr/fcd'), 2)} | "
            f"{number(metric(l0, 'test/clatr/clatr_score'))} | "
            f"{number(metric(l0, 'test/clatr/coverage'), percent=True)} | "
            f"{number(metric(l0, 'test/captions/fscore'))} |",
        ]
        contract = "Direct-C consumes complete GT-human latent plus camera text; every video projects that same GT human."
    return "\n".join(
        [
            f"**Formal `{split}` · {count:,} samples · DDIM50 · CFG1 · η0 · seed17**",
            "",
            *header,
            *rows,
            "",
            contract,
            "C3-25 remains `diagnostic_only=true` and `promotion_eligible=false`.",
        ]
    )


def joint_metrics(ev: Evidence) -> str:
    c325 = load_json(ev.c325_metric("joint_parallel"))
    l0 = load_json(ev.l0_metric("joint_parallel"))
    split, count = eval_scope(c325)
    rows = []
    for label, run_id, payload in (
        ("C3-25", C325_ID, c325),
        ("v7.38 L0", L0_ID, l0),
    ):
        rows.append(
            f"| {label} / `{run_id}` | {number(metric(payload, 'test/tmr/ftd'), 2)} | "
            f"{number(metric(payload, 'test/tmr/tmr_score'))} | "
            f"{number(metric(payload, 'test/tmr/coverage'), percent=True)} | "
            f"{number(metric(payload, 'test/clatr/fcd'), 2)} | "
            f"{number(metric(payload, 'test/clatr/clatr_score'))} | "
            f"{number(metric(payload, 'test/clatr/coverage'), percent=True)} | "
            f"{number(metric(payload, 'test/captions/fscore'))} | "
            f"{number(metric(payload, 'test/proj/outscreen'), percent=True)} |"
        )
    return "\n".join(
        [
            f"**Joint parallel · formal `{split}` · {count:,} samples · DDIM50 · CFG1 · η0 · seed17**",
            "",
            "| version / run | H FDTMR↓ | H TMR↑ | HCov↑ | C FDCLaTr↓ | C CLaTr↑ | CCov↑ | F1↑ | Out↓ |",
            "| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
            *rows,
            "",
            "Top-5 is a paired-geometry best-case diagnostic selected only from C3-25 output. It is not a blind or random qualitative estimate.",
        ]
    )


def single_step_metrics(ev: Evidence, task: str) -> str:
    payloads = [(timestep, load_json(ev.c325_single_step_metric(task, timestep))) for timestep in SINGLE_STEP_TIMESTEPS]
    split, count = eval_scope(payloads[0][1])
    if task == "human":
        header = ("| version / run | FDTMR↓ | TMR↑ | HCov↑ |", "| --- | ---: | ---: | ---: |")
        rows = [
            f"| C3-25 / t={timestep} | {number(metric(payload, 'test/tmr/ftd'), 2)} | "
            f"{number(metric(payload, 'test/tmr/tmr_score'))} | "
            f"{number(metric(payload, 'test/tmr/coverage'), percent=True)} |"
            for timestep, payload in payloads
        ]
    elif task == "camera":
        header = (
            "| version / run | FDCLaTr↓ | CLaTr↑ | CCov↑ | Caption F1↑ |",
            "| --- | ---: | ---: | ---: | ---: |",
        )
        rows = [
            f"| C3-25 / t={timestep} | {number(metric(payload, 'test/clatr/fcd'), 2)} | "
            f"{number(metric(payload, 'test/clatr/clatr_score'))} | "
            f"{number(metric(payload, 'test/clatr/coverage'), percent=True)} | "
            f"{number(metric(payload, 'test/captions/fscore'))} |"
            for timestep, payload in payloads
        ]
    else:
        header = (
            "| version / run | H FDTMR↓ | H TMR↑ | C FDCLaTr↓ | C CLaTr↑ | Out↓ |",
            "| --- | ---: | ---: | ---: | ---: | ---: |",
        )
        rows = [
            f"| C3-25 / t={timestep} | {number(metric(payload, 'test/tmr/ftd'), 2)} | "
            f"{number(metric(payload, 'test/tmr/tmr_score'))} | "
            f"{number(metric(payload, 'test/clatr/fcd'), 2)} | "
            f"{number(metric(payload, 'test/clatr/clatr_score'))} | "
            f"{number(metric(payload, 'test/proj/outscreen'), percent=True)} |"
            for timestep, payload in payloads
        ]
    return "\n".join(
        [
            f"**C3-25 teacher-forced single-step · `{split}` · {count:,} samples**",
            "",
            *header,
            *rows,
            "",
            "Each row is `q(z_gt,t) → one pred_x0` with deterministic per-sample noise. "
            "It is not DDIM50 generation, a training curve, or promotion evidence.",
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
        "Human text only; camera text is display-only paired context."
        if task == "human"
        else "GT human latent plus camera text; every camera is rendered on the same GT human."
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
        full_video(ev, C325_ID, C325_FULL_GROUP, sample_id, "joint", "Camera projection"),
        full_video(ev, L0_ID, L0_BASELINE_GROUP, sample_id, "joint", "Camera projection"),
        gt_video(ev, C325_ID, C325_FULL_GROUP, sample_id, "World skeleton"),
        full_video(ev, C325_ID, C325_FULL_GROUP, sample_id, "joint", "World skeleton"),
        full_video(ev, L0_ID, L0_BASELINE_GROUP, sample_id, "joint", "World skeleton"),
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
    task_root = ev.c325_single_step_vis() / task / sample_id
    source = {
        "human": "Direct-H is human-text-only; projection uses GT camera only as an external view.",
        "camera": "Direct-C predicts camera from GT human plus camera text.",
        "joint": "Joint predicts H/C in one teacher-forced forward.",
    }[task]
    status = (
        f"### `{sample_id}` · {frames} frames · `{task}` · {view}\n\n"
        f"**Human text:** {human_text or 'unavailable'}  \n"
        f"**Camera text:** {camera_text or 'unavailable'}  \n{source}"
    )
    return [
        single_step_metrics(ev, task),
        status,
        existing(task_root / f"gt_{suffix}"),
        *[existing(task_root / f"t{timestep}_{suffix}") for timestep in SINGLE_STEP_TIMESTEPS],
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


def validate(ev: Evidence) -> dict[str, Any]:
    expected_ids = render_ids(ev)
    c325_summary = load_json(ev.full_vis(C325_ID, C325_FULL_GROUP) / "render_summary.json")
    l0_summary = load_json(ev.full_vis(L0_ID, L0_BASELINE_GROUP) / "render_summary.json")
    single_summary = load_json(ev.c325_single_step_vis() / "render_summary.json")
    if set(summary_index(c325_summary)) != set(expected_ids):
        raise RuntimeError("C3-25 full-render IDs do not match the frozen display and Top-5 IDs")
    if set(summary_index(l0_summary)) != set(expected_ids):
        raise RuntimeError("L0 baseline render IDs do not match C3-25")
    if set(summary_index(single_summary)) != set(DISPLAY_SAMPLE_IDS):
        raise RuntimeError("C3-25 single-step render IDs do not match the fixed diagnostic IDs")
    required: list[Path] = []
    for task in ("human", "camera", "joint_parallel"):
        required.extend((ev.c325_metric(task), ev.l0_metric(task)))
    for task in ("human", "camera", "joint"):
        for timestep in SINGLE_STEP_TIMESTEPS:
            required.append(ev.c325_single_step_metric(task, timestep))
    for sample_id in expected_ids:
        for run_id, group in ((C325_ID, C325_FULL_GROUP), (L0_ID, L0_BASELINE_GROUP)):
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
            root = ev.c325_single_step_vis() / task / sample_id
            required.extend((root / "gt_skeleton.mp4", root / "gt_camera_projection.mp4"))
            for timestep in SINGLE_STEP_TIMESTEPS:
                required.extend((root / f"t{timestep}_skeleton.mp4", root / f"t{timestep}_camera_projection.mp4"))
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
        "single_step_timesteps": len(SINGLE_STEP_TIMESTEPS),
        "required_files": len(required),
        "missing": 0,
    }


def build_demo(ev: Evidence):
    import gradio as gr

    c325_summary = load_json(ev.full_vis(C325_ID, C325_FULL_GROUP) / "render_summary.json")
    single_summary = load_json(ev.c325_single_step_vis() / "render_summary.json")
    humanml_summary = load_json(ev.humanml_summary())
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

    def video_grid(labels: tuple[str, ...], columns: int = 3) -> list[Any]:
        play = gr.Button("▶ 同步播放当前组", variant="primary", elem_classes="sync-play")
        play.click(fn=None, js=SYNC_PLAY_JS)
        videos = []
        for start in range(0, len(labels), columns):
            with gr.Row(elem_classes=["evidence-row"]):
                for label in labels[start : start + columns]:
                    with gr.Column():
                        gr.Markdown(f"### {label}")
                        videos.append(gr.Video(show_label=False, format="mp4"))
        return videos

    with gr.Blocks(title="StoryMotion C3-25 evidence") as demo:
        gr.Markdown("# StoryMotion · C3-25 evidence desk", elem_id="hero")
        gr.Markdown(
            "**展示主角：v8.1C C3-25 seed17 · Stage2 105K。** "
            "Direct-H、Direct-C 与 joint parallel 均使用 exact C3-25 checkpoint/cache/owning decoder；"
            "v7.38 L0 仅作为 matched 105K baseline。C3-25 仍是 diagnostic-only candidate，"
            "本页的视频、Top-5 与 single-step 结果不构成 promotion 或 blind quality claim。",
            elem_classes="verdict",
        )
        with gr.Tabs():
            for task, tab_name, labels in (
                ("human", "Human completion", ("GT human", "C3-25 · Direct-H", "v7.38 L0 · Direct-H")),
                ("camera", "Camera completion", ("GT camera + GT human", "C3-25 · Direct-C", "v7.38 L0 · Direct-C")),
            ):
                with gr.Tab(tab_name):
                    sample = gr.Dropdown(list(DISPLAY_SAMPLE_IDS), value=DISPLAY_SAMPLE_IDS[0], label="Sample")
                    metric_box = gr.Markdown(elem_classes="metric-strip")
                    status = gr.Markdown()
                    videos = video_grid(labels)
                    outputs = [metric_box, status, *videos]
                    callback = lambda sample_id, selected_task=task: completion_view(
                        ev, c325_index, sample_id, selected_task
                    )
                    sample.change(callback, sample, outputs)
                    demo.load(callback, sample, outputs)

            with gr.Tab("Joint Top-5 · 2×3"):
                sample = gr.Dropdown(top_choices, value=top_choices[0][1], label="C3-25 paired-geometry rank")
                metric_box = gr.Markdown(elem_classes="metric-strip")
                status = gr.Markdown()
                videos = video_grid(
                    (
                        "GT · camera projection",
                        "C3-25 · joint projection",
                        "v7.38 L0 · joint projection",
                        "GT · world skeleton",
                        "C3-25 · joint skeleton",
                        "v7.38 L0 · joint skeleton",
                    )
                )
                outputs = [metric_box, status, *videos]
                callback = lambda sample_id: joint_view(ev, c325_index, ranking, sample_id)
                sample.change(callback, sample, outputs)
                demo.load(callback, sample, outputs)

            with gr.Tab("C3-25 single-step diagnostic"):
                with gr.Row():
                    sample = gr.Dropdown(list(DISPLAY_SAMPLE_IDS), value=DISPLAY_SAMPLE_IDS[0], label="Sample")
                    task = gr.Radio(("human", "camera", "joint"), value="human", label="Target")
                    view = gr.Radio(("Camera projection", "World skeleton"), value="World skeleton", label="View")
                metric_box = gr.Markdown(elem_classes="metric-strip")
                status = gr.Markdown()
                videos = video_grid(("Raw GT", "t = 999", "t = 799", "t = 599", "t = 399", "t = 199"))
                outputs = [metric_box, status, *videos]
                inputs = [sample, task, view]
                callback = lambda sample_id, selected_task, selected_view: single_step_view(
                    ev, single_index, sample_id, selected_task, selected_view
                )
                sample.change(callback, inputs, outputs)
                task.change(callback, inputs, outputs)
                view.change(callback, inputs, outputs)
                demo.load(callback, inputs, outputs)

            with gr.Tab("HumanML3D"):
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
        str((ev.root / "runs" / "stage1" / HUMANML_RUN_ID).resolve()),
    ]
    demo.launch(server_name=args.host, server_port=args.port, share=False, allowed_paths=allowed, css=CSS)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
