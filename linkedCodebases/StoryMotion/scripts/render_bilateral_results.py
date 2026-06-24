#!/usr/bin/env python3
"""Render stage2 DDIM samples as static PNG and MP4 video."""
from __future__ import annotations

import argparse, ast, importlib.util, json, subprocess, sys, time
from pathlib import Path
from typing import Any

import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import torch

ROOT = Path('/data/public/ripemangobox/Motion/StoryMotion')
TRAIN_SCRIPT = ROOT / 'scripts/train_stage2_condmdi_pulp.py'
CACHE_SCRIPT = ROOT / 'scripts/build_stage2_pulp_latent_cache.py'

spec = importlib.util.spec_from_file_location('train_stage2_condmdi_pulp', TRAIN_SCRIPT)
mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)

cache_spec = importlib.util.spec_from_file_location('build_stage2_pulp_latent_cache', CACHE_SCRIPT)
cache_mod = importlib.util.module_from_spec(cache_spec)
sys.modules['build_stage2_pulp_latent_cache'] = cache_mod
cache_spec.loader.exec_module(cache_mod)

BONE_CONNECTIONS = [
    (0, 1), (0, 2), (0, 3), (1, 4), (2, 5), (3, 6),
    (4, 7), (5, 8), (6, 9), (7, 10), (8, 11), (9, 12),
    (9, 13), (9, 14), (12, 15), (13, 16), (14, 17),
    (16, 18), (17, 19), (18, 20), (19, 21),
]

try:
    import imageio_ffmpeg
    FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()
except ImportError:
    import os
    # Try known ffmpeg paths
    for candidate in ['/home/ripemangobox/miniconda3/envs/DART5/bin/ffmpeg', '/home/ripemangobox/miniconda3/envs/mogents/bin/ffmpeg', 'ffmpeg']:
        if os.path.exists(candidate):
            FFMPEG = candidate
            break
    else:
        FFMPEG = 'ffmpeg'


def load_model(ckpt_path, device):
    ckpt = torch.load(ckpt_path, map_location='cpu')
    meta_args = ckpt.get('meta', {}).get('args', {})
    width = int(meta_args.get('width', 384))
    dim_mults = tuple(int(v) for v in ast.literal_eval(meta_args.get('dim_mults', '[1,2,2]')))
    cond_mask_prob = float(meta_args.get('cond_mask_prob', 0.1))
    zero_final = str(meta_args.get('zero_final', 'True')).lower() == 'true'
    diffusion_steps = int(meta_args.get('diffusion_steps', 1000))
    noise_schedule = str(meta_args.get('noise_schedule', 'cosine'))
    model = mod.TemporalObsUNet(width, dim_mults, cond_mask_prob, zero_final).to(device)
    model.load_state_dict(ckpt['model']); model.eval()
    diffusion = mod.CondMDIDiffusion(diffusion_steps, noise_schedule, device)
    return model, diffusion, ckpt


def build_pulp(args, device):
    pulp_args = argparse.Namespace(
        pulp_root=cache_mod.DEFAULT_PULP_ROOT, data_root=cache_mod.DEFAULT_DATA_ROOT,
        model_dir=cache_mod.DEFAULT_MODEL_DIR, config_name='config_dit_xy', set_name='mixed_',
        train_split='train', val_split='test', out_dir=Path('/tmp'),
        device=str(device), batch_size=1, num_workers=0,
        limit_train=None, limit_val=None, dtype='float16',
        seed=args.seed, progress_every=0,
    )
    cfg = cache_mod.build_config(pulp_args)
    dataset = cache_mod.make_dataset(cfg, pulp_args.val_split)
    autoencoder = cache_mod.make_autoencoder(cfg, device)
    return cfg, dataset, autoencoder


def to_official_order(z_hum_cam):
    return torch.cat([z_hum_cam[:, mod.HUM_DIM:], z_hum_cam[:, :mod.HUM_DIM]], dim=1)


def deterministic_noise(shape, sample_indices, seed, device, dtype):
    parts = []
    for si in sample_indices:
        g = torch.Generator(device='cpu'); g.manual_seed(int(seed) + int(si) * 1_000_003)
        parts.append(torch.randn(shape[1:], generator=g, dtype=torch.float32))
    return torch.stack(parts, dim=0).to(device=device, dtype=dtype)


def make_timesteps(num_timesteps, num_steps, device):
    ts = torch.linspace(num_timesteps - 1, 0, num_steps, device=device).round().long()
    ts = torch.unique_consecutive(ts)
    if ts.numel() == 0 or int(ts[-1].item()) != 0:
        ts = torch.cat([ts, torch.zeros(1, dtype=torch.long, device=device)])
    return ts


def _as_tensor(value, field_name):
    if torch.is_tensor(value):
        return value
    if isinstance(value, np.ndarray):
        return torch.from_numpy(value)
    if isinstance(value, (list, tuple)):
        return torch.as_tensor(value)
    raise TypeError(f'{field_name} must be tensor-like, got {type(value).__name__}')


def _pick_mapping_value(mapping, keys, field_name):
    for key in keys:
        if key in mapping:
            return mapping[key]
    raise KeyError(f'{field_name} missing expected keys {keys}')


def get_gt_tensors(sample, device):
    x_raw = sample['x_raw']
    camera = x_raw['camera']
    intrinsics = x_raw.get('intrinsics')
    if isinstance(camera, dict):
        if intrinsics is None:
            intrinsics = _pick_mapping_value(camera, ('intrinsics', 'K'), 'x_raw.camera.intrinsics')
        camera = _pick_mapping_value(camera, ('c2w', 'camera', 'poses'), 'x_raw.camera')
    human = x_raw['human']
    joints = human['joints'] if isinstance(human, dict) else human.joints

    gt_c2w = _as_tensor(camera, 'x_raw.camera').unsqueeze(0).to(device)
    gt_intrinsics = _as_tensor(intrinsics, 'x_raw.intrinsics').unsqueeze(0).to(device)
    gt_joints = _as_tensor(joints, 'x_raw.human.joints').unsqueeze(0).to(device)
    return gt_c2w, gt_intrinsics, gt_joints


@torch.no_grad()
def ddim_sample_bilateral(model, diffusion, z, text, valid, task_id, sample_indices, seed, num_steps,
                          cfg_scale=1.0, cfg_human=None, cfg_camera=None, eta=0.0,
                          channel_gated_cfg=False):
    bilateral = cfg_human is not None and cfg_camera is not None
    task = torch.full((z.shape[0],), task_id, dtype=torch.long, device=z.device)
    obs_mask, _ = mod.make_branch_masks(z, valid, task)
    valid_bc = valid[:, None, :].expand_as(z)
    fixed_mask = obs_mask | (~valid_bc)
    base_noise = deterministic_noise(tuple(z.shape), sample_indices, seed, z.device, z.dtype)
    timesteps = make_timesteps(diffusion.num_timesteps, num_steps, z.device)

    empty_text = torch.zeros_like(text) if (cfg_scale != 1.0 or bilateral) else None
    half = text.shape[1] // 2
    cam_text = None
    hum_text = None
    if bilateral:
        cam_text = text.clone(); cam_text[:, half:] = 0
        hum_text = text.clone(); hum_text[:, :half] = 0

    def rand_noise(step_idx):
        return deterministic_noise(tuple(z.shape), sample_indices, seed + 1_000_000 + step_idx * 97, z.device, z.dtype)

    def q_gt(t_scalar):
        a = diffusion.sqrt_alphas_cumprod[t_scalar].to(device=z.device, dtype=z.dtype).view(1, 1, 1)
        b = diffusion.sqrt_one_minus_alphas_cumprod[t_scalar].to(device=z.device, dtype=z.dtype).view(1, 1, 1)
        return a * z + b * base_noise

    def model_forward(x_t, t_scalar, cond_text):
        t = torch.full((z.shape[0],), t_scalar, dtype=torch.long, device=z.device)
        return model(x_t, t, cond_text, obs_x0=z, obs_mask=obs_mask)

    x = torch.where(fixed_mask, q_gt(int(timesteps[0].item())), base_noise)
    pred_x0 = z
    for idx, t_scalar_tensor in enumerate(timesteps):
        t_scalar = int(t_scalar_tensor.item())
        x = torch.where(fixed_mask, q_gt(t_scalar), x)

        if bilateral:
            pu = model_forward(x, t_scalar, empty_text)
            pc = model_forward(x, t_scalar, cam_text)
            ph = model_forward(x, t_scalar, hum_text)
            if channel_gated_cfg:
                pred_x0 = pu.clone()
                pred_x0[:, :mod.HUM_DIM] = pu[:, :mod.HUM_DIM] + cfg_human * (ph[:, :mod.HUM_DIM] - pu[:, :mod.HUM_DIM])
                pred_x0[:, mod.HUM_DIM:] = pu[:, mod.HUM_DIM:] + cfg_camera * (pc[:, mod.HUM_DIM:] - pu[:, mod.HUM_DIM:])
            else:
                pred_x0 = pu + cfg_camera * (pc - pu) + cfg_human * (ph - pu)
        elif cfg_scale == 1.0:
            pred_x0 = model_forward(x, t_scalar, text)
        else:
            pc = model_forward(x, t_scalar, text)
            pu = model_forward(x, t_scalar, empty_text)
            pred_x0 = pu + cfg_scale * (pc - pu)

        pred_for_step = torch.where(fixed_mask, z, pred_x0)
        if idx == timesteps.numel() - 1:
            break
        next_t = int(timesteps[idx + 1].item())
        a_t = diffusion.sqrt_alphas_cumprod[t_scalar].to(device=z.device, dtype=z.dtype).view(1, 1, 1)
        b_t = diffusion.sqrt_one_minus_alphas_cumprod[t_scalar].to(device=z.device, dtype=z.dtype).view(1, 1, 1)
        a_next = diffusion.sqrt_alphas_cumprod[next_t].to(device=z.device, dtype=z.dtype).view(1, 1, 1)
        b_next = diffusion.sqrt_one_minus_alphas_cumprod[next_t].to(device=z.device, dtype=z.dtype).view(1, 1, 1)
        eps = (x - a_t * pred_for_step) / b_t.clamp_min(1e-8)
        if eta > 0.0:
            alpha_t = a_t.square(); alpha_next = a_next.square()
            sigma = eta * torch.sqrt((1.0 - alpha_next) / (1.0 - alpha_t).clamp_min(1e-8)) * torch.sqrt((1.0 - alpha_t / alpha_next).clamp_min(1e-8))
            x = a_next * pred_for_step + torch.sqrt((1.0 - alpha_next - sigma.square()).clamp_min(0.0)) * eps + sigma * rand_noise(idx)
        else:
            x = a_next * pred_for_step + b_next * eps
        x = torch.where(fixed_mask, q_gt(next_t), x)
    return torch.where(fixed_mask, z, pred_x0)


def decode_raw(autoencoder, dataset, z_hum_cam, intrinsics):
    feats = autoencoder.decode(to_official_order(z_hum_cam))
    return dataset.get_raw(feats, intrinsics)


def project_joints(human_joints, c2w, intrinsics):
    """Project 3D joints through camera matrix to 2D pixel coords (numpy)."""
    if hasattr(human_joints, 'cpu'):
        jt_np = human_joints.cpu().numpy(); c2w_np = c2w.cpu().numpy(); intr_np = intrinsics.cpu().numpy()
    else:
        jt_np = human_joints; c2w_np = c2w; intr_np = intrinsics
    frames = min(jt_np.shape[0], c2w_np.shape[0], intr_np.shape[0])
    joints = jt_np[:frames]
    c2w_np = c2w_np[:frames]
    intr_np = intr_np[:frames]

    rotation = c2w_np[:, :3, :3]
    translation = c2w_np[:, :3, 3]
    w2c_rotation = np.swapaxes(rotation, -1, -2)
    w2c_translation = -np.einsum('fij,fj->fi', w2c_rotation, translation)
    camera_joints = np.einsum('fij,fkj->fki', w2c_rotation, joints) + w2c_translation[:, None, :]

    fx, fy, cx, cy = [intr_np[:, i] for i in range(4)]
    safe_z = np.maximum(camera_joints[..., 2], np.finfo(np.float32).eps)
    x = fx[:, None] * (camera_joints[..., 0] / safe_z) + cx[:, None]
    y = fy[:, None] * (camera_joints[..., 1] / safe_z) + cy[:, None]
    return np.stack((x, y, camera_joints[..., 2]), axis=-1)


def render_context_from_joints(joint_sets):
    finite_sets = []
    for joints in joint_sets:
        arr = np.asarray(joints)
        if arr.size == 0:
            continue
        flat = arr.reshape(-1, 3)
        flat = flat[np.isfinite(flat).all(axis=1)]
        if flat.size:
            finite_sets.append(flat)
    if not finite_sets:
        return {'center_xy': np.zeros(2, dtype=np.float32), 'ground_z': 0.0, 'xy_limit': 1.0, 'z_limit': 1.0}
    all_joints = np.concatenate(finite_sets, axis=0)
    xy_min = all_joints[:, :2].min(axis=0)
    xy_max = all_joints[:, :2].max(axis=0)
    center_xy = ((xy_min + xy_max) * 0.5).astype(np.float32)
    ground_z = float(all_joints[:, 2].min())
    shifted_xy = all_joints[:, :2] - center_xy
    shifted_z = all_joints[:, 2] - ground_z
    horizontal = max(float(np.abs(shifted_xy).max()), 0.5)
    vertical = max(float(shifted_z.max()), 0.5)
    xy_limit = max(horizontal, vertical * 0.6, 0.5) * 1.25
    z_limit = max(vertical * 1.15, xy_limit * 1.25, 0.75)
    return {'center_xy': center_xy, 'ground_z': ground_z, 'xy_limit': float(xy_limit), 'z_limit': float(z_limit)}


def apply_render_context(joints, render_context):
    centered = np.asarray(joints).copy()
    centered[..., 0] -= render_context['center_xy'][0]
    centered[..., 1] -= render_context['center_xy'][1]
    centered[..., 2] -= render_context['ground_z']
    return centered


def render_3d_video(joints, render_context, output_path, fps, title):
    from matplotlib.animation import FFMpegWriter, FuncAnimation
    matplotlib.rcParams['animation.ffmpeg_path'] = FFMPEG
    render_joints = apply_render_context(joints, render_context)
    frames = render_joints.shape[0]
    margin = render_context['xy_limit']

    fig = plt.figure(figsize=(6, 6))
    ax = fig.add_subplot(111, projection='3d')
    lines, scatter = [], None

    def set_axes():
        ax.set_xlim(-margin, margin)
        ax.set_ylim(-margin, margin)
        ax.set_zlim(0, render_context['z_limit'])
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')
        ax.set_title(title, fontsize=8)
        ax.view_init(18.0, -65.0)
        ax.set_box_aspect((1, 1, 1))

    def init():
        nonlocal scatter
        set_axes()
        scatter = ax.scatter([], [], [], c='tab:red', s=18, zorder=5)
        for _ in BONE_CONNECTIONS:
            (line,) = ax.plot([], [], [], color='tab:blue', linewidth=1.5, alpha=0.9)
            lines.append(line)
        return [scatter] + lines

    def update(frame):
        jt = render_joints[frame]
        scatter._offsets3d = (jt[:, 0], jt[:, 1], jt[:, 2])
        for idx, (p, c) in enumerate(BONE_CONNECTIONS):
            lines[idx].set_data([jt[p, 0], jt[c, 0]], [jt[p, 1], jt[c, 1]])
            lines[idx].set_3d_properties([jt[p, 2], jt[c, 2]])
        set_axes()
        return [scatter] + lines

    output_path.parent.mkdir(parents=True, exist_ok=True)
    anim = FuncAnimation(fig, update, frames=frames, init_func=init, blit=False, interval=1000 / fps)
    anim.save(str(output_path), writer=FFMpegWriter(fps=fps, bitrate=2000), dpi=100)
    plt.close(fig)
    return output_path


def render_video(projection, intrinsics, output_path, fps, title):
    from matplotlib.animation import FFMpegWriter, FuncAnimation
    matplotlib.rcParams['animation.ffmpeg_path'] = FFMPEG
    frames = projection.shape[0]; intr = intrinsics[:frames]
    w = max(2, int(round(float((intr[:, 2] * 2.0).max()))))
    h = max(2, int(round(float((intr[:, 3] * 2.0).max()))))
    fig = plt.figure(figsize=(w / 100.0, h / 100.0))
    ax = fig.add_subplot(111)
    lines, scatter = [], None

    def init():
        nonlocal scatter
        ax.set_xlim(0, w); ax.set_ylim(h, 0); ax.set_aspect('equal', adjustable='box')
        ax.set_title(title, fontsize=8); ax.set_xticks([]); ax.set_yticks([])
        scatter = ax.scatter([], [], c='tab:red', s=10, zorder=5)
        for _ in BONE_CONNECTIONS:
            (line,) = ax.plot([], [], color='tab:blue', linewidth=1.5, alpha=0.9); lines.append(line)
        return [scatter] + lines

    def update(frame):
        jt = projection[frame]
        valid = np.isfinite(jt).all(axis=-1) & (jt[:, 2] > 0)
        scatter.set_offsets(jt[valid, :2])
        for idx, (p, c) in enumerate(BONE_CONNECTIONS):
            if valid[p] and valid[c]:
                lines[idx].set_data([jt[p, 0], jt[c, 0]], [jt[p, 1], jt[c, 1]])
            else:
                lines[idx].set_data([], [])
        ax.set_xlim(0, w); ax.set_ylim(h, 0)
        return [scatter] + lines

    output_path.parent.mkdir(parents=True, exist_ok=True)
    anim = FuncAnimation(fig, update, frames=frames, init_func=init, blit=False, interval=1000 / fps)
    anim.save(str(output_path), writer=FFMpegWriter(fps=fps, bitrate=2000), dpi=100)
    plt.close(fig)
    return output_path


def concat_videos(paths, output_path):
    if any(not p.exists() for p in paths): return None
    output_path.parent.mkdir(parents=True, exist_ok=True)
    cmd = [FFMPEG, '-y'] + [a for p in paths for a in ['-i', str(p)]]
    cmd.extend(['-filter_complex', f'hstack=inputs={len(paths)}', '-c:v', 'libx264', '-pix_fmt', 'yuv420p', str(output_path)])
    subprocess.run(cmd, check=True, capture_output=True)
    return output_path


def plot_render_png(out_path, mode, sample_id, gt_cam_3d, pred_cam_3d, gt_joints, pred_joints, valid_frames):
    n = max(1, min(valid_frames, gt_cam_3d.shape[0], pred_cam_3d.shape[0]))
    gt_cam = gt_cam_3d[:n]; pred_cam = pred_cam_3d[:n]
    gt_root = gt_joints[:n, 0, :]; pred_root = pred_joints[:n, 0, :]
    frame_ids = sorted({0, n // 2, n - 1})

    fig, axes = plt.subplots(1, 3, figsize=(13.5, 4.2))
    axes[0].plot(gt_cam[:, 0], gt_cam[:, 2], color='black', linewidth=2, label='GT')
    axes[0].plot(pred_cam[:, 0], pred_cam[:, 2], color='#d1495b', linewidth=1.5, label='pred')
    axes[0].set_title('camera trajectory XZ'); axes[0].set_xlabel('x'); axes[0].set_ylabel('z'); axes[0].legend()
    _set_equal_aspect(axes[0], [gt_cam, pred_cam])

    axes[1].plot(gt_root[:, 0], gt_root[:, 2], color='black', linewidth=2, label='GT')
    axes[1].plot(pred_root[:, 0], pred_root[:, 2], color='#00798c', linewidth=1.5, label='pred')
    axes[1].set_title('human root trajectory XZ'); axes[1].set_xlabel('x'); axes[1].legend()
    _set_equal_aspect(axes[1], [gt_root, pred_root])

    for frame in frame_ids:
        axes[2].scatter(gt_joints[frame, :, 0], gt_joints[frame, :, 2], s=9, color='black', alpha=0.5)
        axes[2].scatter(pred_joints[frame, :, 0], pred_joints[frame, :, 2], s=9, alpha=0.6)
    axes[2].set_title('human joints XZ frames'); axes[2].set_xlabel('x'); axes[2].set_ylabel('z')
    _set_equal_aspect(axes[2], [gt_joints[:n].reshape(-1, 3), pred_joints[:n].reshape(-1, 3)])

    fig.suptitle(f'{mode}: {sample_id}'); fig.tight_layout()
    out_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_path, dpi=180); plt.close(fig)


def _set_equal_aspect(ax, arrays):
    chunks = []
    for arr in arrays:
        arr = np.asarray(arr)
        if arr.size == 0 or arr.shape[-1] < 3:
            continue
        xy_arr = arr.reshape(-1, arr.shape[-1])[:, [0, 2]]
        xy_arr = xy_arr[np.isfinite(xy_arr).all(axis=1)]
        if xy_arr.size:
            chunks.append(xy_arr)
    if not chunks:
        ax.set_aspect('equal', adjustable='box')
        return
    xy = np.concatenate(chunks, axis=0)
    mins = xy.min(axis=0); maxs = xy.max(axis=0)
    center = (mins + maxs) / 2
    radius = max(float((maxs - mins).max()) / 2, 1.0)
    ax.set_xlim(center[0] - radius, center[0] + radius)
    ax.set_ylim(center[1] - radius, center[1] + radius)
    ax.set_aspect('equal', adjustable='box')


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--ckpt', type=Path, default=ROOT / 'runs/train/stage2/pulp_official_full_mixed_20260611/gpu3_branchmean_jointheavy6_ft_b512_102688_20260612_2151/last.pt')
    p.add_argument('--cache-dir', type=Path, default=ROOT / 'runs/train/stage2/pulp_official_full_mixed_20260611/cache_mixed_full_nw0_20260611_2110')
    p.add_argument('--out-dir', type=Path, default=ROOT / 'runs/eval/bilateral_cfg_renders_20260614')
    p.add_argument('--metrics-out-dir', type=Path, default=None)
    p.add_argument('--cfg-scale', type=float, default=2.0)
    p.add_argument('--cfg-human', type=float, default=None)
    p.add_argument('--cfg-camera', type=float, default=None)
    p.add_argument('--eta', type=float, default=0.0)
    p.add_argument('--num-steps', type=int, default=50)
    p.add_argument('--fps', type=int, default=12)
    p.add_argument('--num-samples', type=int, default=3)
    p.add_argument('--start-index', type=int, default=0)
    p.add_argument('--sample-ids', nargs='*')
    p.add_argument('--tasks', nargs='+', choices=['camera', 'human', 'joint'], default=['camera', 'human', 'joint'])
    p.add_argument('--seed', type=int, default=20260614)
    p.add_argument('--channel-gated-cfg', action='store_true',
                   help='For bilateral CFG, apply camera text guidance only to camera latent channels and human text guidance only to human latent channels.')
    args = p.parse_args()

    device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
    torch.manual_seed(args.seed); np.random.seed(args.seed)

    print('Loading model...')
    model, diffusion, ckpt = load_model(args.ckpt, device)
    _, dataset, autoencoder = build_pulp(args, device)
    cache = mod.PulpLatentCache(args.cache_dir / 'val.pt')

    if args.sample_ids:
        target_ids = [str(sample_id) for sample_id in args.sample_ids]
    else:
        target_ids = [str(cache[i]['sample_id']) for i in range(args.start_index, min(args.start_index + args.num_samples, len(cache)))]
    task_items = [(task_id, task_name) for task_id, task_name in mod.TASK_NAMES.items() if task_name in set(args.tasks)]

    is_bilateral = args.cfg_human is not None and args.cfg_camera is not None
    if (args.cfg_human is None) != (args.cfg_camera is None):
        raise ValueError('--cfg-human and --cfg-camera must be set together')
    cfg_label = f'bi_h{args.cfg_human}_c{args.cfg_camera}_eta{args.eta}' if is_bilateral else f'std_cfg{args.cfg_scale}_eta{args.eta}'
    args.out_dir = args.out_dir / cfg_label
    args.out_dir.mkdir(parents=True, exist_ok=True)
    metrics_out_dir = (args.metrics_out_dir / cfg_label) if args.metrics_out_dir else args.out_dir
    metrics_out_dir.mkdir(parents=True, exist_ok=True)

    results = {'samples': [], 'cfg_mode': 'bilateral' if is_bilateral else 'standard',
               'cfg_scale': args.cfg_scale, 'cfg_human': args.cfg_human, 'cfg_camera': args.cfg_camera,
               'cfg_channel_gated': bool(args.channel_gated_cfg), 'eta': args.eta, 'tasks': args.tasks}
    start_time = time.time()

    for si, sample_id in enumerate(target_ids):
        print(f'Rendering {si+1}/{len(target_ids)}: {sample_id}')
        cache_idx = next(i for i in range(len(cache)) if str(cache[i]['sample_id']) == sample_id)
        item = cache[cache_idx]
        z = item['z'].unsqueeze(0).to(device)
        text = item['text'].unsqueeze(0).to(device)
        valid = item['valid'].unsqueeze(0).to(device)

        # Get GT data from dataset
        sample = dataset.get_sample(sample_id)
        gt_c2w, gt_intrinsics, gt_joints = get_gt_tensors(sample, device)
        valid_frames = int(sample['padding_mask'].long().sum().item())

        gt_c2w_np = gt_c2w[0, :valid_frames].cpu().numpy()
        gt_intr_np = gt_intrinsics[0, :valid_frames].cpu().numpy()
        gt_joints_np = gt_joints[0, :valid_frames].cpu().numpy()
        gt_cam_xyz = gt_c2w_np[:, :3, 3]  # [T, 3]

        sample_record = {'sample_id': sample_id, 'valid_frames': valid_frames, 'modes': {}}
        task_outputs = []

        for task_id, task_name in task_items:
            sample_indices = [args.seed + si * 1000 + task_id]
            completion = ddim_sample_bilateral(
                model, diffusion, z, text, valid, task_id, sample_indices,
                args.seed + {'camera': 11, 'human': 23, 'joint': 37}[task_name],
                args.num_steps,
                cfg_scale=args.cfg_scale, cfg_human=args.cfg_human, cfg_camera=args.cfg_camera, eta=args.eta,
                channel_gated_cfg=args.channel_gated_cfg,
            )

            # Decode predicted latent through autoencoder
            raw_output = decode_raw(autoencoder, dataset, completion, gt_intrinsics)

            # Extract predicted camera translation and human joints
            pred_cam_xyz = raw_output['camera'][0, :valid_frames, :3, 3].cpu().numpy()  # [T, 3]
            pred_joints_out = raw_output['human'].joints[0, :valid_frames].cpu().numpy()  # [T, 22, 3]

            # For rendering with correct joint positions:
            # Mode A (camera completion): GT human; camera path is shown in PNG.
            # Mode B/C: predicted human skeleton in world coordinates.
            if task_name == 'camera':
                render_joints = gt_joints_np
            else:
                render_joints = pred_joints_out

            task_outputs.append({
                'task_name': task_name,
                'pred_cam_xyz': pred_cam_xyz,
                'pred_joints_out': pred_joints_out,
                'render_joints': render_joints,
            })

        render_context = render_context_from_joints([gt_joints_np] + [out['render_joints'] for out in task_outputs])
        sample_record['render_context'] = {
            'center_xy': [float(x) for x in render_context['center_xy']],
            'ground_z': float(render_context['ground_z']),
            'xy_limit': float(render_context['xy_limit']),
            'z_limit': float(render_context['z_limit']),
        }

        gt_video = args.out_dir / sample_id / 'gt_skeleton.mp4'
        render_3d_video(gt_joints_np, render_context, gt_video, args.fps, f'{sample_id} [GT]')

        for output in task_outputs:
            task_name = output['task_name']
            pred_cam_xyz = output['pred_cam_xyz']
            pred_joints_out = output['pred_joints_out']
            render_joints = output['render_joints']

            # Static PNG
            png_path = args.out_dir / sample_id / f'{task_name}_render.png'
            plot_render_png(png_path, task_name, sample_id, gt_cam_xyz, pred_cam_xyz, gt_joints_np, pred_joints_out, valid_frames)

            # MP4 video: world-coordinate 3D skeleton. Camera completion is
            # represented in the camera trajectory PNG above.
            mp4_path = args.out_dir / sample_id / f'{task_name}_skeleton.mp4'
            render_3d_video(render_joints, render_context, mp4_path, args.fps, f'{sample_id} [{task_name}]')

            # Concat video: GT left, pred right
            concat_path = args.out_dir / sample_id / f'{task_name}_concat.mp4'
            concat_videos([gt_video, mp4_path], concat_path)

            print(f'  {task_name}: done (PNG+MP4+Concat)')
            sample_record['modes'][task_name] = {'png': str(png_path), 'mp4': str(mp4_path), 'concat': str(concat_path)}

        results['samples'].append(sample_record)

    results['elapsed_sec'] = time.time() - start_time
    results['out_dir'] = str(args.out_dir)
    results['metrics_out_dir'] = str(metrics_out_dir)
    (metrics_out_dir / 'render_summary.json').write_text(json.dumps(results, indent=2, sort_keys=True, default=str))
    print(json.dumps({'ok': True, 'out_dir': str(args.out_dir), 'metrics_out_dir': str(metrics_out_dir), 'samples': len(target_ids), 'elapsed': results['elapsed_sec']}))


if __name__ == '__main__':
    main()
