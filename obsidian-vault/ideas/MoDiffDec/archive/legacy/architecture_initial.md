# MoDiffDec: 详细架构设计

> 从 PiD 到 Motion 的逐组件迁移方案

---

## 1. 架构总览

```
                          ┌─────────────────────────┐
                          │   MoLingo SAE Encoder    │  ← FROZEN (from baseline)
                          │   CausalCNN + ResNet     │
                          │   down_t=2, stride_t=2   │
                          └───────────┬─────────────┘
                                      │
                                      ▼
                          ┌─────────────────────────┐
                          │   Motion Latent z        │
                          │   [B, T/4, 32]           │
                          └───────────┬─────────────┘
                                      │
                    ┌─────────────────┼─────────────────┐
                    │   训练时: 加噪   │   推理时: 可直接使用 │
                    │   z̃_σ = (1-σ)z + σξ  │   partially denoised z │
                    └─────────────────┼─────────────────┘
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────┐
│                   MotionDiffDecoder                          │
│                                                             │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  z_proj: Linear(32, d_model)                         │  │
│  │  sigma_embed: Sinusoidal(d_model)                    │  │
│  └──────────────────────────────────────────────────────┘  │
│                           │                                 │
│                           ▼                                 │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  x_t [B,T,263] + PosEmbed + SigmaEmbed              │  │
│  └──────────────────────────────────────────────────────┘  │
│                           │                                 │
│              ┌────────────┴────────────┐                    │
│              ▼                         ▼                    │
│  ┌──────────────────────┐  ┌──────────────────────┐       │
│  │  Layer 0..N-1:       │  │  Text Cond (T5)      │       │
│  │  - Self-Attention    │◄─│  via cross-attention │       │
│  │  - Cross-Attention   │  └──────────────────────┘       │
│  │  - SigmaAwareGate    │                                  │
│  │  - FFN               │                                  │
│  └──────────┬───────────┘                                  │
│             ▼                                              │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  Output Proj: LayerNorm → Linear(d_model, 263)       │  │
│  └──────────────────────────────────────────────────────┘  │
│                                                             │
│  Output: v_θ(x_t, t, c, z̃_σ, σ) → motion velocity field    │
└─────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
                          ┌─────────────────────────┐
                          │  Rectified Flow Sampling │
                          │  Euler 4~32 steps         │
                          └───────────┬─────────────┘
                                      │
                                      ▼
                          ┌─────────────────────────┐
                          │  Reconstructed Motion    │
                          │  [B, T, 263]             │
                          └─────────────────────────┘
```

## 2. 核心组件详解

### 2.1 MotionDiffDecoderLayer

```python
class MotionDiffDecoderLayer(nn.Module):
    """
    Single decoder layer with:
    1. Self-attention over temporal dimension
    2. Cross-attention to text condition
    3. Sigma-aware latent gate injection
    4. Feed-forward network
    """
    def __init__(self, d_model, nhead, latent_dim, 
                 dim_feedforward=2048, dropout=0.1):
        super().__init__()
        # Self-attention (causal for autoregressive variant, 
        #           or bidirectional for full sequence)
        self.self_attn = nn.MultiheadAttention(
            d_model, nhead, dropout=dropout, batch_first=True)
        self.self_attn_norm = nn.LayerNorm(d_model)
        
        # Cross-attention to text embedding
        self.cross_attn = nn.MultiheadAttention(
            d_model, nhead, dropout=dropout, batch_first=True)
        self.cross_attn_norm = nn.LayerNorm(d_model)
        
        # Sigma-aware latent gate
        self.latent_gate = SigmaAwareGate(d_model, latent_dim)
        self.gate_norm = nn.LayerNorm(d_model)
        
        # Feed-forward
        self.ffn = nn.Sequential(
            nn.Linear(d_model, dim_feedforward),
            nn.GELU(),
            nn.Dropout(dropout),
            nn.Linear(dim_feedforward, d_model),
            nn.Dropout(dropout),
        )
        self.ffn_norm = nn.LayerNorm(d_model)
    
    def forward(self, h, text_kv, latent_tokens, sigma):
        # h: [B, T, d_model]
        # text_kv: [B, T_text, d_model] — key/value for cross-attention
        
        # 1. Self-attention
        h = h + self.self_attn(
            self.self_attn_norm(h), 
            self.self_attn_norm(h), 
            self.self_attn_norm(h)
        )[0]
        
        # 2. Cross-attention to text
        if text_kv is not None:
            h_norm = self.cross_attn_norm(h)
            h = h + self.cross_attn(
                h_norm, text_kv, text_kv
            )[0]
        
        # 3. Sigma-aware latent gate
        h_norm = self.gate_norm(h)
        h = self.latent_gate(h_norm, latent_tokens, sigma)
        
        # 4. FFN
        h = h + self.ffn(self.ffn_norm(h))
        
        return h
```

### 2.2 Sigma-Aware Gate — Motion 适配版

PiD 原版 gate 公式：
```
g_i(h_i, l_i, σ) = sigmoid(Linear_i([h_i, l_i]) - α·σ)
```

**Motion 适配的考虑**：
- 图像中，h_i 和 l_i 是空间对齐的（latent token 与 pixel patch 对应）
- Motion 中，latent 是 temporally downsampled 的（T/4 vs T），需要时序对齐
- 使用 interpolation 将 latent 上采样到 motion 时间分辨率

```python
class SigmaAwareGate(nn.Module):
    def __init__(self, d_model, latent_dim, alignment='interpolate'):
        super().__init__()
        self.latent_proj = nn.Sequential(
            nn.Linear(latent_dim, d_model),
            nn.SiLU(),
            nn.Linear(d_model, d_model),
        )
        # Gate prediction: [h, l_proj] → gate value
        self.gate_net = nn.Sequential(
            nn.Linear(d_model * 2, d_model // 4),
            nn.SiLU(),
            nn.Linear(d_model // 4, 1),
        )
        self.alpha = nn.Parameter(torch.tensor(1.0))
        self.alignment = alignment
    
    def temporal_align(self, latent_tokens, target_len):
        """
        将 latent tokens [B, T_lat, d] 对齐到 target_len
        """
        if latent_tokens.size(1) == target_len:
            return latent_tokens
        # Linear interpolation along time dim
        return F.interpolate(
            latent_tokens.transpose(1, 2),
            size=target_len,
            mode='linear',
            align_corners=False
        ).transpose(1, 2)
    
    def forward(self, h, latent_tokens, sigma):
        """
        h: [B, T, d_model] — decoder hidden state
        latent_tokens: [B, T_lat, latent_dim] — noise latent
        sigma: [B] or scalar — noise level
        """
        # Project and align latent
        l_proj = self.latent_proj(latent_tokens)  # [B, T_lat, d_model]
        l_proj = self.temporal_align(l_proj, h.size(1))  # [B, T, d_model]
        
        # Compute gate
        gate_input = torch.cat([h, l_proj], dim=-1)  # [B, T, 2*d_model]
        gate_raw = self.gate_net(gate_input)  # [B, T, 1]
        
        # Sigma-aware bias
        sigma = sigma.view(-1, 1, 1).expand(-1, h.size(1), 1)
        gate = torch.sigmoid(gate_raw - self.alpha * sigma)
        
        # Gated injection
        return h + gate * l_proj
```

### 2.3 Noise Schedule for Motion Latent

PiD 用 σ ~ U(0, 0.8)，需要验证 motion latent 的特性：

```python
def noise_latent(z_clean, sigma_mode='uniform', sigma_max=0.8):
    """
    向 clean latent 注入噪声
    
    Args:
        z_clean: [B, T, dim] clean latent from SAE encoder
        sigma_mode: 'uniform' | 'log_normal' | 'beta'
        sigma_max: max noise level
    Returns:
        z_noisy: noise-corrupted latent
        sigma: actual noise levels
    """
    B = z_clean.size(0)
    device = z_clean.device
    
    if sigma_mode == 'uniform':
        sigma = torch.rand(B, device=device) * sigma_max
    elif sigma_mode == 'log_normal':
        # 偏向低噪声区域，对应 LDM 后期步
        sigma = torch.exp(torch.randn(B, device=device) * 0.5 - 2.0)
        sigma = sigma.clamp(0.0, sigma_max)
    elif sigma_mode == 'beta':
        # Beta distribution，集中在中等噪声
        sigma = torch.distributions.Beta(2, 2).sample((B,)).to(device)
        sigma = sigma * sigma_max
    
    noise = torch.randn_like(z_clean)
    z_noisy = (1 - sigma.view(-1, 1, 1)) * z_clean + sigma.view(-1, 1, 1) * noise
    
    return z_noisy, sigma
```

**验证实验**：训练不同 σ 分布下 decoder 的重建质量，确定最优分布。

### 2.4 Rectified Flow Training

MoLingo 已经使用 Rectified Flow（在 `mogen/models/molingo/flowloss.py` 中定义）。MoDiffDec 复用相同的 flow matching 框架但适配到 decoder 场景：

```python
class MoDiffDecFlowLoss(nn.Module):
    """
    Rectified Flow loss for motion diffusion decoder.
    与 MoLingo 的 FLowLoss 兼容，但增加了 sigma conditioning。
    """
    def __init__(self, target_channels=263, z_channels=512, 
                 width=1024, depth=8, sample_steps=32):
        super().__init__()
        self.target_channels = target_channels
        self.sample_steps = sample_steps
        
        # 使用 MotionDiffDecoder 作为 denoiser backbone
        # （替代 MoLingo 中基于 DiT 的 flow network）
    
    def forward(self, x0, text_cond, z_sigma, sigma):
        """
        x0: [B, T, 263] clean motion
        text_cond: [B, T_text, d_model] text embeddings
        z_sigma: [B, T_lat, 32] noise-corrupted latent
        sigma: [B] noise levels
        """
        B, T, _ = x0.shape
        device = x0.device
        
        # Sample time t
        t = torch.rand(B, device=device)
        
        # Sample noise
        eps = torch.randn_like(x0)
        x_t = t.view(-1, 1, 1) * x0 + (1 - t).view(-1, 1, 1) * eps
        
        # Predict velocity
        v_pred = self.network(x_t, t, text_cond, z_sigma, sigma)
        
        # Target velocity
        v_target = x0 - eps
        
        return F.mse_loss(v_pred, v_target)
```

## 3. 参数量估算

| 组件 | 参数 | 计算 |
|------|------|------|
| SAE Encoder (frozen) | ~15M | 不变 |
| z_proj | 32 × 512 = 16K | Linear |
| sigma_embed | ~1K | Sinusoidal |
| pos_embed | ~100K | Learned positional |
| 6 × DecoderLayer | 6 × (4 × 512² + 512×32) ≈ 6 × 1.1M ≈ 6.6M | Self-attn + Cross-attn + Gate + FFN |
| output_proj | 512 × 263 = 135K | Linear |
| **Total Decoder** | **~7M** | 约为 encoder 的 47% |
| **Total MoDiffDec** | **~22M** | Encoder (15M) + Decoder (7M) |

对比：PiD 使用 FLUX.1 的 PixelDiT (~2.6B) 作为骨干，我们的 decoder 仅 ~7M，适合 motion 低维特性。

## 4. 推理流程

```python
@torch.no_grad()
def decode_motion(sae_encoder, diff_decoder, motion_latent, 
                  text_cond, num_steps=16, sigma_latent=0.0):
    """
    从 motion latent 解码生成 motion features
    
    Args:
        sae_encoder: frozen SAE encoder (仅用于 reference)
        diff_decoder: MotionDiffDecoder
        motion_latent: [B, T_lat, 32] latent from SAE encoder (或 LDM 输出)
        text_cond: [B, T_text, 1024] T5 text embeddings
        num_steps: 推理步数
        sigma_latent: latent 的噪声水平 
                      (0=clean latent, >0=partially denoised)
    """
    B = motion_latent.size(0)
    T_target = motion_latent.size(1) * 4  # 4x upsampling
    device = motion_latent.device
    
    # 添加 latent 噪声（用于早期退出场景）
    if sigma_latent > 0:
        z_sigma = noise_latent(motion_latent, sigma=sigma_latent)
    else:
        z_sigma = motion_latent
    
    # Rectified flow sampling (Euler method)
    x_t = torch.randn(B, T_target, 263, device=device)
    dt = 1.0 / num_steps
    
    for step in range(num_steps):
        t = step * dt
        t_tensor = torch.full((B,), t, device=device)
        sigma_tensor = torch.full((B,), sigma_latent, device=device)
        
        v_pred = diff_decoder(x_t, t_tensor, text_cond, 
                             z_sigma, sigma_tensor)
        x_t = x_t + v_pred * dt
    
    return x_t  # [B, T_target, 263] reconstructed motion features
```

## 5. 关键设计决策

### 5.1 为什么用 Transformer 而不是 CNN？

- PiD 使用 MMDiT（Transformer）
- Motion 的时序特性适合 Transformer 的 self-attention
- CNN 的 receptive field 有限，Transformer 可以捕获全局时序依赖
- MoLingo 本身的 T2M 部分也使用 Transformer decoder

### 5.2 为什么不做 Pixel-space Diffusion（直接在 joint rotation space）？

- Motion latent 已经做了压缩（T/4 × 32-dim）
- 在 latent space 做 diffusion 计算量小
- 在 motion feature space（263-dim, T frames）做 diffusion decoder — 这是 "pixel diffusion" 在 motion 领域的 direct analogue
- 263-dim 的 "pixel space" 远小于图像（3×2048²），可以直接用 Transformer

### 5.3 与 DC-Motion 的差异

| | DC-Motion | MoDiffDec |
|---|-----------|-----------|
| Decoder 类型 | Lightweight residual diffusion | Sigma-aware transformer diffusion |
| Latent 注入 | 简单拼接 | Sigma-aware gate |
| 先验 | 从零训练 | 利用预训练 T2M 先验 |
| 早期退出 | 不支持 | 支持 |
| 核心哲学 | Tokenizer 设计 | Decoder 作为生成器 |

### 5.4 为什么需要 T2M 先验？

PiD Table 4 显示：移除 T2I 先验 → MUSIQ 从 73.26 降至 59.52。Motion 领域同理——预训练 text-to-motion 模型的 text encoder 和 motion prior 是高质量 decoding 的基础。

**实现方案**：
1. 使用 MoLingo 的 T5 text encoder（已训练好）
2. 在 decoder 的 cross-attention 中注入 text condition
3. 可选：loading MoLingo 的 T2M checkpoint 作为 decoder 初始化

## 6. PiD 组件迁移检查清单

| PiD 组件 | Motion 对应 | 状态 |
|----------|-----------|------|
| PixelDiT backbone | MotionDiffDecoder (Transformer) | 待实现 |
| Noise latent conditioning | z̃_σ = (1-σ)z + σξ | 待实现 |
| Sigma-aware gate | SigmaAwareGate | 待实现 |
| DMD2 distillation | 可选后期添加 | 暂缓 |
| Early termination | 支持 partially denoised latent | 设计完成 |
| ControlNet-style adapter | Cross-attention + gate injection | 设计完成 |
| T2I prior | T5 text encoder (from MoLingo) | 已有 |
| Frequency-aware loss | DWT + weighted subbands | 增强选项 |

---

*Next: implementation.md — 代码变更清单与实现步骤*
