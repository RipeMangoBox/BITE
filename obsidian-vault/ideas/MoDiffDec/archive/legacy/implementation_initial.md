# MoDiffDec: 实现细节与代码变更清单

---

## 1. 代码变更总览

### 1.1 新增文件

```
mogen/models/motion_diff_decoder/
├── __init__.py                    # 模块入口
├── sigma_aware_gate.py            # Sigma-aware gate
├── motion_diff_decoder.py         # 主 decoder 模型
├── decoder_trainer.py             # 独立 decoder 训练器
└── config.py                      # 默认配置

mogen/
├── train_diff_decoder.py          # 训练入口脚本
└── options/diff_decoder_option.py # 命令行参数
```

### 1.2 修改文件

```
mogen/models/vae/vae.py            # 添加 freeze_encoder() 方法
mogen/core/sae_trainer.py          # 导出 encoder checkpoint（供 diff decoder 使用）
```

## 2. 详细实现

### 2.1 `mogen/models/motion_diff_decoder/__init__.py`

```python
from .sigma_aware_gate import SigmaAwareGate
from .motion_diff_decoder import MotionDiffDecoder, MotionDiffDecoderLayer
from .decoder_trainer import MoDiffDecTrainer
from .config import MoDiffDecConfig

__all__ = [
    'SigmaAwareGate',
    'MotionDiffDecoder',
    'MotionDiffDecoderLayer',
    'MoDiffDecTrainer',
    'MoDiffDecConfig',
]
```

### 2.2 `mogen/models/motion_diff_decoder/config.py`

```python
from dataclasses import dataclass
from typing import Optional

@dataclass
class MoDiffDecConfig:
    # Decoder architecture
    d_model: int = 512
    num_layers: int = 6
    num_heads: int = 8
    dim_feedforward: int = 2048
    dropout: float = 0.1
    
    # Latent
    latent_dim: int = 32
    latent_temporal_ratio: int = 4  # T_latent = T_motion / 4
    
    # Motion
    motion_dim: int = 263
    max_seq_len: int = 200
    
    # Text condition
    text_dim: int = 1024  # T5-large output dim
    use_text_condition: bool = True
    
    # Sigma-aware gate
    sigma_max: float = 0.8
    sigma_mode: str = 'uniform'  # 'uniform' | 'log_normal' | 'beta'
    
    # Training
    learning_rate: float = 1e-4
    adam_beta1: float = 0.9
    adam_beta2: float = 0.999
    weight_decay: float = 0.0
    max_grad_norm: float = 1.0
    
    # Loss weights
    flow_loss_weight: float = 1.0
    freq_loss_weight: float = 0.1
    velocity_loss_weight: float = 0.1
    
    # Frequency loss
    wavelet: str = 'haar'  # 'haar' | 'db2' | 'bior2.2'
    high_freq_weight: float = 2.0  # 高频子带权重
    
    # GPU
    device: str = 'cuda'
    gpu_id: int = 0
    
    @classmethod
    def from_dict(cls, d):
        return cls(**{k: v for k, v in d.items() if k in cls.__dataclass_fields__})
```

### 2.3 `mogen/models/motion_diff_decoder/sigma_aware_gate.py`

见 [architecture.md](architecture.md) Section 2.2

### 2.4 `mogen/models/motion_diff_decoder/motion_diff_decoder.py`

```python
import math
import torch
import torch.nn as nn
import torch.nn.functional as F
from .sigma_aware_gate import SigmaAwareGate


class SinusoidalEmbedding(nn.Module):
    """Sinusoidal time/sigma embedding (standard diffusion embedding)"""
    def __init__(self, dim):
        super().__init__()
        self.dim = dim
    
    def forward(self, x):
        device = x.device
        half_dim = self.dim // 2
        emb = math.log(10000) / (half_dim - 1)
        emb = torch.exp(torch.arange(half_dim, device=device) * -emb)
        emb = x.float()[:, None] * emb[None, :]
        emb = torch.cat([emb.sin(), emb.cos()], dim=-1)
        return emb


class MotionDiffDecoderLayer(nn.Module):
    """见 architecture.md Section 2.1"""
    def __init__(self, d_model, nhead, latent_dim, 
                 dim_feedforward=2048, dropout=0.1):
        super().__init__()
        self.self_attn = nn.MultiheadAttention(
            d_model, nhead, dropout=dropout, batch_first=True)
        self.norm1 = nn.LayerNorm(d_model)
        
        self.cross_attn = nn.MultiheadAttention(
            d_model, nhead, dropout=dropout, batch_first=True)
        self.norm2 = nn.LayerNorm(d_model)
        
        self.latent_gate = SigmaAwareGate(d_model, latent_dim)
        self.norm3 = nn.LayerNorm(d_model)
        
        self.ffn = nn.Sequential(
            nn.Linear(d_model, dim_feedforward),
            nn.GELU(),
            nn.Dropout(dropout),
            nn.Linear(dim_feedforward, d_model),
            nn.Dropout(dropout),
        )
        self.norm4 = nn.LayerNorm(d_model)
    
    def forward(self, h, text_kv, latent_tokens, sigma):
        # Self-attention
        h_norm = self.norm1(h)
        h = h + self.self_attn(h_norm, h_norm, h_norm, need_weights=False)[0]
        
        # Cross-attention to text
        if text_kv is not None:
            h_norm = self.norm2(h)
            h = h + self.cross_attn(h_norm, text_kv, text_kv, need_weights=False)[0]
        
        # Sigma-aware gate
        h_norm = self.norm3(h)
        h = self.latent_gate(h_norm, latent_tokens, sigma)
        
        # FFN
        h_norm = self.norm4(h)
        h = h + self.ffn(h_norm)
        
        return h


class MotionDiffDecoder(nn.Module):
    def __init__(self, config):
        super().__init__()
        self.config = config
        
        # Time + sigma embedding
        self.time_embed = nn.Sequential(
            SinusoidalEmbedding(config.d_model),
            nn.Linear(config.d_model, config.d_model),
            nn.SiLU(),
            nn.Linear(config.d_model, config.d_model),
        )
        self.sigma_embed = nn.Sequential(
            SinusoidalEmbedding(config.d_model),
            nn.Linear(config.d_model, config.d_model),
            nn.SiLU(),
            nn.Linear(config.d_model, config.d_model),
        )
        
        # Input projection
        self.input_proj = nn.Linear(config.motion_dim, config.d_model)
        
        # Positional embedding
        self.pos_embed = nn.Parameter(
            torch.randn(1, config.max_seq_len, config.d_model) * 0.02)
        
        # Latent projection
        self.latent_proj = nn.Linear(config.latent_dim, config.d_model)
        
        # Text projection (if text dim != d_model)
        if config.text_dim != config.d_model:
            self.text_proj = nn.Linear(config.text_dim, config.d_model)
        else:
            self.text_proj = nn.Identity()
        
        # Decoder layers
        self.layers = nn.ModuleList([
            MotionDiffDecoderLayer(
                d_model=config.d_model,
                nhead=config.num_heads,
                latent_dim=config.latent_dim,
                dim_feedforward=config.dim_feedforward,
                dropout=config.dropout,
            )
            for _ in range(config.num_layers)
        ])
        
        # Output projection
        self.output_proj = nn.Sequential(
            nn.LayerNorm(config.d_model),
            nn.Linear(config.d_model, config.motion_dim),
        )
        
        self._init_weights()
    
    def _init_weights(self):
        for module in self.modules():
            if isinstance(module, nn.Linear):
                nn.init.xavier_uniform_(module.weight)
                if module.bias is not None:
                    nn.init.zeros_(module.bias)
    
    def forward(self, x_t, t, text_emb, z_sigma, sigma):
        """
        Args:
            x_t: [B, T, 263] noisy motion features
            t: [B] diffusion timestep [0, 1]
            text_emb: [B, T_text, text_dim] text embeddings (or None)
            z_sigma: [B, T_lat, 32] noise-corrupted latent
            sigma: [B] noise level
        Returns:
            v_pred: [B, T, 263] predicted velocity field
        """
        B, T, _ = x_t.shape
        device = x_t.device
        
        # Embed time and sigma
        t_emb = self.time_embed(t).unsqueeze(1)    # [B, 1, d_model]
        s_emb = self.sigma_embed(sigma).unsqueeze(1)  # [B, 1, d_model]
        
        # Project input and add embeddings
        h = self.input_proj(x_t)  # [B, T, d_model]
        h = h + self.pos_embed[:, :T, :]
        h = h + t_emb + s_emb
        
        # Project latent
        latent_tokens = self.latent_proj(z_sigma)  # [B, T_lat, d_model]
        
        # Project text
        if text_emb is not None:
            text_kv = self.text_proj(text_emb)  # [B, T_text, d_model]
        else:
            text_kv = None
        
        # Pass through decoder layers
        for layer in self.layers:
            h = layer(h, text_kv, latent_tokens, sigma)
        
        # Output projection
        v_pred = self.output_proj(h)
        
        return v_pred
```

### 2.5 `mogen/models/motion_diff_decoder/decoder_trainer.py`

```python
import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np
from torch.utils.tensorboard import SummaryWriter
from tqdm.auto import tqdm
import os
import pywt  # for wavelet decomposition

class MoDiffDecTrainer:
    def __init__(self, config, decoder, sae_encoder, 
                 dataloader, text_encoder=None):
        self.config = config
        self.decoder = decoder
        self.sae_encoder = sae_encoder  # frozen
        self.dataloader = dataloader
        self.text_encoder = text_encoder  # frozen T5
        
        self.optimizer = torch.optim.AdamW(
            decoder.parameters(),
            lr=config.learning_rate,
            betas=(config.adam_beta1, config.adam_beta2),
            weight_decay=config.weight_decay,
        )
        
        self.device = config.device
        self.decoder.to(self.device)
        self.sae_encoder.to(self.device)
        
        if self.text_encoder is not None:
            self.text_encoder.to(self.device)
    
    def noise_latent(self, z_clean):
        """向 clean latent 注入噪声"""
        B = z_clean.size(0)
        device = z_clean.device
        
        sigma = torch.rand(B, device=device) * self.config.sigma_max
        noise = torch.randn_like(z_clean)
        z_noisy = (1 - sigma.view(-1, 1, 1)) * z_clean + sigma.view(-1, 1, 1) * noise
        
        return z_noisy, sigma
    
    def wavelet_loss(self, pred, target):
        """
        Frequency-aware loss via wavelet decomposition
        借鉴 RealisVSR 的 wavelet-weighted HR-Loss
        """
        # 对每个 joint 轨迹做 1D DWT
        # pred/target: [B, T, 263] → reshape to [B, T, J, 3] → per-channel DWT
        
        # 简化版：对整个序列做 DWT
        loss = 0.0
        # LL (低频): weight=1.0
        # LH/HL/HH (高频): weight=2.0
        # 仅在 wavelet 库可用时使用，否则 fallback 到 FFT loss
        
        try:
            # Per-joint per-coordinate DWT
            B, T, D = pred.shape
            for d in range(D):
                coeffs_pred = pywt.wavedec(pred[:, :, d].cpu().numpy(), 
                                           self.config.wavelet, level=2)
                coeffs_target = pywt.wavedec(target[:, :, d].cpu().numpy(), 
                                             self.config.wavelet, level=2)
                for i, (cp, ct) in enumerate(zip(coeffs_pred, coeffs_target)):
                    w = self.config.high_freq_weight if i > 0 else 1.0
                    loss += w * F.l1_loss(
                        torch.tensor(cp).to(pred.device),
                        torch.tensor(ct).to(target.device))
            loss = loss / D
        except:
            # Fallback: high-pass filter loss
            from torch.nn.functional import conv1d
            kernel = torch.tensor([-1., 2., -1.], device=pred.device).view(1, 1, -1)
            high_pred = conv1d(pred.transpose(1, 2).reshape(-1, 1, T), 
                              kernel, padding=1).reshape(B, D, T).transpose(1, 2)
            high_target = conv1d(target.transpose(1, 2).reshape(-1, 1, T), 
                                kernel, padding=1).reshape(B, D, T).transpose(1, 2)
            loss = F.l1_loss(high_pred, high_target)
        
        return loss
    
    def velocity_loss(self, pred, target):
        """时序速度一致性损失"""
        pred_vel = pred[:, 1:, :] - pred[:, :-1, :]
        target_vel = target[:, 1:, :] - target[:, :-1, :]
        return F.l1_loss(pred_vel, target_vel)
    
    def train_step(self, batch):
        motion_gt = batch['motion'].to(self.device)  # [B, T, 263]
        text_tokens = batch.get('text_tokens')  # optional text
        
        B, T, _ = motion_gt.shape
        device = self.device
        
        # 1. Encode with frozen SAE encoder
        with torch.no_grad():
            if self.sae_encoder.ae:
                z_clean = self.sae_encoder.ae_encode(motion_gt)
            else:
                z_clean, _ = self.sae_encoder.encode(motion_gt)
        
        # 2. Noise latent
        z_sigma, sigma = self.noise_latent(z_clean)
        
        # 3. Rectified flow training
        t = torch.rand(B, device=device)
        eps = torch.randn_like(motion_gt)
        x_t = t.view(-1, 1, 1) * motion_gt + (1 - t).view(-1, 1, 1) * eps
        
        # 4. Text encoding
        text_emb = None
        if text_tokens is not None and self.text_encoder is not None:
            with torch.no_grad():
                text_emb = self.text_encoder(text_tokens)
        
        # 5. Forward
        v_pred = self.decoder(x_t, t, text_emb, z_sigma, sigma)
        v_target = motion_gt - eps
        
        # 6. Losses
        flow_loss = F.mse_loss(v_pred, v_target)
        
        # Predict x0 from v_pred for auxiliary losses
        x0_pred = x_t - t.view(-1, 1, 1) * v_pred  # simple Euler inversion
        
        total_loss = flow_loss * self.config.flow_loss_weight
        
        if self.config.freq_loss_weight > 0:
            freq_loss = self.wavelet_loss(x0_pred, motion_gt)
            total_loss = total_loss + freq_loss * self.config.freq_loss_weight
        
        if self.config.velocity_loss_weight > 0:
            vel_loss = self.velocity_loss(x0_pred, motion_gt)
            total_loss = total_loss + vel_loss * self.config.velocity_loss_weight
        
        return total_loss, {
            'flow_loss': flow_loss.item(),
            'total_loss': total_loss.item(),
        }
    
    def train_epoch(self, epoch):
        self.decoder.train()
        total_loss = 0
        pbar = tqdm(self.dataloader, desc=f'Epoch {epoch}')
        
        for batch in pbar:
            self.optimizer.zero_grad()
            loss, loss_dict = self.train_step(batch)
            loss.backward()
            torch.nn.utils.clip_grad_norm_(
                self.decoder.parameters(), self.config.max_grad_norm)
            self.optimizer.step()
            
            total_loss += loss.item()
            pbar.set_postfix({'loss': f'{loss.item():.4f}'})
        
        return total_loss / len(self.dataloader)
```

## 3. 训练脚本

### 3.1 `mogen/train_diff_decoder.py`

```python
"""
MoDiffDec Training Script
用法:
    python mogen/train_diff_decoder.py \
        --sae_ckpt mogen/checkpoints/ms/sae_baseline/model.pth \
        --dataset_name ms \
        --batch_size 16 \
        --max_epoch 500 \
        --d_model 512 --num_layers 6 \
        --sigma_max 0.8 \
        --gpu_id 0
"""

import argparse
import torch
from mogen.models.motion_diff_decoder import (
    MotionDiffDecoder, MoDiffDecConfig, MoDiffDecTrainer
)
from mogen.models.vae.vae import VAE
from mogen.data.t2m_dataset import T2MDataset
from mogen.utils.get_opt import get_opt


def main():
    parser = argparse.ArgumentParser()
    
    # SAE checkpoint
    parser.add_argument('--sae_ckpt', type=str, required=True,
                        help='Path to trained SAE checkpoint')
    parser.add_argument('--ae', action='store_true',
                        help='SAE was trained in AE mode (no KL)')
    
    # Data
    parser.add_argument('--dataset_name', type=str, default='ms')
    parser.add_argument('--data_root', type=str, 
                        default='/data/public/ripemangobox/Motion/datasets')
    parser.add_argument('--batch_size', type=int, default=16)
    parser.add_argument('--max_motion_length', type=int, default=200)
    
    # Model
    parser.add_argument('--d_model', type=int, default=512)
    parser.add_argument('--num_layers', type=int, default=6)
    parser.add_argument('--num_heads', type=int, default=8)
    parser.add_argument('--dim_feedforward', type=int, default=2048)
    
    # Sigma
    parser.add_argument('--sigma_max', type=float, default=0.8)
    parser.add_argument('--sigma_mode', type=str, default='uniform')
    
    # Training
    parser.add_argument('--max_epoch', type=int, default=500)
    parser.add_argument('--lr', type=float, default=1e-4)
    parser.add_argument('--freq_loss_weight', type=float, default=0.1)
    parser.add_argument('--velocity_loss_weight', type=float, default=0.1)
    
    # System
    parser.add_argument('--gpu_id', type=int, default=0)
    parser.add_argument('--exp_name', type=str, default='modiffdec')
    parser.add_argument('--save_every_e', type=int, default=50)
    
    args = parser.parse_args()
    
    # Build config
    config = MoDiffDecConfig(
        d_model=args.d_model,
        num_layers=args.num_layers,
        num_heads=args.num_heads,
        dim_feedforward=args.dim_feedforward,
        sigma_max=args.sigma_max,
        sigma_mode=args.sigma_mode,
        learning_rate=args.lr,
        freq_loss_weight=args.freq_loss_weight,
        velocity_loss_weight=args.velocity_loss_weight,
        device=f'cuda:{args.gpu_id}',
    )
    
    # Load frozen SAE encoder
    sae_vae = VAE(
        input_width=263,
        output_emb_width=32,
        down_t=2, stride_t=2,
        width=1024, depth=3,
        ae=args.ae,
    )
    ckpt = torch.load(args.sae_ckpt, map_location='cpu')
    sae_vae.load_state_dict(ckpt['state_dict'])
    sae_vae.eval()
    for p in sae_vae.parameters():
        p.requires_grad_(False)
    
    # Build decoder
    decoder = MotionDiffDecoder(config)
    
    # Data
    dataset = T2MDataset(
        dataset_name=args.dataset_name,
        data_root=args.data_root,
        max_motion_length=args.max_motion_length,
    )
    dataloader = torch.utils.data.DataLoader(
        dataset, batch_size=args.batch_size, shuffle=True,
        num_workers=4, pin_memory=True,
    )
    
    # Trainer
    trainer = MoDiffDecTrainer(
        config=config,
        decoder=decoder,
        sae_encoder=sae_vae,
        dataloader=dataloader,
    )
    
    # Train
    for epoch in range(1, args.max_epoch + 1):
        avg_loss = trainer.train_epoch(epoch)
        print(f'Epoch {epoch}: avg_loss = {avg_loss:.4f}')
        
        if epoch % args.save_every_e == 0:
            torch.save({
                'epoch': epoch,
                'decoder_state_dict': decoder.state_dict(),
                'config': config,
            }, f'checkpoints/modiffdec_{args.exp_name}_e{epoch}.pth')


if __name__ == '__main__':
    main()
```

## 4. 与 MoLingo T2M 集成

### 4.1 替换 decoder

在 `mogen/models/molingo/molingo.py` 中，MoLingo 的 T2M 生成流程是：

```python
# 当前流程（简化的）
z = vae.encode(motion)  # GT encoding
# ... T2M generation ...
motion_hat = vae.decode(z_hat)  # vae.decoder() ← 要替换这个
```

修改为：

```python
# 新流程
motion_hat = diff_decoder.decode_motion(
    sae_encoder=vae,
    motion_latent=z_hat,
    text_cond=text_emb,
    num_steps=16,
)
```

### 4.2 端到端微调

Stage 2: 将 MoDiffDec 接入 MoLingo T2M pipeline，端到端训练：

```python
# 固定 SAE encoder
# 训练: MoLingo T2M (可选微调) + MoDiffDec (主要训练目标)
# 损失: T2M loss + decoding quality loss
```

## 5. 实现检查清单

- [ ] 创建 `mogen/models/motion_diff_decoder/` 目录
- [ ] 实现 `config.py`
- [ ] 实现 `sigma_aware_gate.py`
- [ ] 实现 `motion_diff_decoder.py`
- [ ] 实现 `decoder_trainer.py`
- [ ] 创建 `mogen/train_diff_decoder.py`
- [ ] 创建 `mogen/options/diff_decoder_option.py`
- [ ] 训练 SAE baseline，导出 encoder checkpoint
- [ ] 训练 MoDiffDec Stage 1（frozen encoder）
- [ ] 与 CNN decoder 对比重建质量
- [ ] 接入 MoLingo T2M pipeline
- [ ] 端到端评估生成质量

---

*Next: experiments.md — 实验设计矩阵与评估方案*
