---
title: "StoryMotion Redesign Stage1 × ViMoGen-CLIP Stage2 — 精简接力稿"
status: handoff_ready
hypothesis: |
  先用 redesign Stage1 建立 Camera-invariant Human anchor 与显式
  Human–Camera relation，再把 ViMoGen-light CLIP 扩展为受保护的 Human
  stream、独立 Camera stream 和有界 relation coupling，可以同时保留
  Human generation 优势并支持 Direct-H、Direct-C 与 joint parallel。
tags:
  - StoryMotion
  - stage1
  - stage2
  - architecture
  - handoff
  - status/active
aliases:
  - StoryMotion-Redesign-ViMoGen-Handoff
source_notes:
  - "[[ideas/StoryMotion/current]]"
  - "[[ideas/StoryMotion/StoryMotion-valid-metric-ledger]]"
  - "[[ideas/StoryMotion/StoryMotion-metric-computation-io]]"
  - "[[ideas/StoryMotion/StoryMotion_Checkmate]]"
  - "[[ideas/StoryMotion/2026-07-27_storymotion-stage1-human-anchor-residual-control]]"
created: 2026-07-27T17:55:26+08:00
updated: 2026-07-27T21:00:00+08:00
---

# StoryMotion Redesign Stage1 × ViMoGen-CLIP Stage2

> [!abstract] 接力任务
> 只推进一条主线：完成 redesign Stage1 的 Human-first asymmetric
> decoupling，再把已验证较强的 ViMoGen-light CLIP Human generator
> 适配成 protected-H dual-stream 三模式模型。不要把 Human 与 Camera
> latent 直接拼接进单一共享 backbone；不要使用失真的 HML+Pulp
> checkpoint；所有晋升结论必须来自 decoded canonical metrics 与同步视觉证据。

> [!note] 文档边界
> 本页是设计与实验接力稿，不复制完整指标表。精确数值、run artifact 与
> SHA256 只读 [[ideas/StoryMotion/StoryMotion-valid-metric-ledger]]；指标定义只读
> [[ideas/StoryMotion/StoryMotion-metric-computation-io]]。下方 optimization
> objective 是方法设计，不是 formal metric。

## 1. 已有证据与当前裁决

### 1.1 Redesign Stage1

redesign 的目标不是让 Human 与 Camera 完全独立，而是建立有方向的依赖：

$$
z_h=E_h(H),\qquad
z_{hc}=E_{hc}(H,C),\qquad
z_c=E_c(C\mid z_h,z_{hc}),
$$

$$
\hat H=D_h(z_h),\qquad
(\hat C,\hat F)=D_{c,f}(z_h,z_{hc},z_c).
$$

- `z_h` 是 Camera-free Human anchor，维度 `128`；`D_h` 只读取 `z_h`。
- `z_{hc}` 是 interaction residual，维度 `16`。
- `z_c` 是 Camera state，维度 `48`；Camera/framing decoder仍可读取 Human。
- 所有 Stage1/Stage2 路径必须显式断言 `is_causal is False`。

已完成的两个 fresh `636K` endpoints：

- Pulp-only：`stage1_hanchor_pulp_only_matched_r3_636k_seed17_4090g0_20260726`。
- HML-root-local + Pulp-full：`stage1_hanchor_hmlrootlocal_pulpfull_packedio_r3_636k_seed17_5090g2_20260726`。

结构性 preflight 已验证：固定 Human、随机替换 Camera 后，`z_h` 逐元素不变。
这证明 `C \nrightarrow H` 的表示隔离；它不否认 Camera 与 projective geometry
仍依赖 Human。

现有实验的最窄结论：

- Pulp-only 是两个 redesign arms 中的视觉胜者；fixed-8 中相对 C3-25
  Stage1 未见明显视觉恶化，且独立控制感更强。
- canonical reconstruction 仍显示 C3-25 的 Pulp Human geometry 总体更强；
  redesign 尚不是全面 Pareto win，也尚未替换 C3-25 mainline。
- Pulp-only 与 mixed arm 的 GT-Human-origin Camera trajectory 近似，而 Human
  与 projection 明显分离，支持 Camera branch insulation；不能据此宣称联合
  geometry 已完全解耦。
- C3-25 与 redesign Pulp-only 都在部分样本最后一帧出现 Camera jump，随即
  导致 owning-camera projection 骤变。这是共享 terminal-boundary failure，
  必须单独定位，不能先归因于 redesign。
- Pulp 训练没有 fixed-first-64 裁切；动态有效长度中的第 65 帧以后参与训练。

HML+Pulp arm 的正式裁决：

- HumanML RIC263 的 IK-derived rotations 与 Pulp TRAM/SMPL local rotations
  不是同源观测。joint positions 到 rotations 非单射，bone-axis twist、leaf
  rotation、rest pose、shape 与部分 root orientation 无法从规范化 joints
  唯一恢复。
- 旧 adapter 把 HML 的 `4:136` 写成 Pulp mean、没有 availability mask，
  同时又排除该块 supervision；这把 unknown 伪装成 observed mean pose。
- 因此 mixed checkpoint 只能保留为 root/local retrospective diagnostic，
  禁止构建正式 Stage2 cache、训练 Stage2 或参与 promotion。
- 若继续 HML，必须回到 provenance-closed 的 HumanML/AMASS source
  SMPL-family rotations并完成 FK/geodesic/坐标审计，或显式使用 missingness
  mask 与独立 root/local encoder；不得再次 mean-fill full-Human input。

### 1.2 ViMoGen-light CLIP Stage2

已完成 fixed-C3 Human-only endpoint：

- training：`e6_c3_vimogen_light_clipseq_h_0_105000_seed17_4090g1_20260726`。
- formal eval：`e6_c3_vimogen_light_clipseq_h_105k_eval_r2_canonical512_euler50_seed17_4090g1_20260727`。
- mode：Direct-H；`N=512`；ordered cohort
  `6b9c92a533d2d0aff76cce6c7ad23361733fb38d3157128bf7eee56cdc33d8df`。
- sampler：deterministic shifted-sigma Euler50；representation/decoder：固定
  C3 Human128 与 owning decoder。

正式结论：ViMoGen-light CLIP 是本轮综合 canonical Human endpoint 与 fixed-8
视觉的最强 Human-only system。其优势最可能来自以下组合，而非单一因素：

1. full temporal self-attention 直接建模全序列 root、heading 与动作 phase；
2. 完整 CLIP token sequence 逐层 cross-attention，而不是 pooled text bias；
3. shifted continuous flow 更直接地拟合稠密连续 motion latent 的 vector field；
4. Human-only exposure 避免 Camera/joint task 对 Human prior 的梯度竞争。

边界同样明确：它没有 Camera/joint branch，strict Human physical gate 尚未闭合；
相对 C3 同时改变 topology、objective、sampler、condition interface 与 task
exposure。因此目前只能称为 **ViMoGen-light CLIP system-task fit 胜出**，不能称为
pure-backbone 上限证据。

## 2. 核心设计原则

禁止采用：

$$
\operatorname{concat}(z_h,z_c)
\rightarrow
\text{single shared backbone}
\rightarrow
\text{single shared head}.
$$

这种结构会让 Camera objective、Camera text 和 joint exposure 持续改写 Human
self-attention、normalization、FFN 与 text–motion alignment；Direct-C 还可能借
GT Human 形成 shortcut，Direct-H 则被迫经过无关的 Camera pathway。

推荐原则是：

$$
\boxed{
\text{protected Human prior}
+\text{Camera-specific flow}
+\text{bounded relation coupling}
}
$$

依赖方向应为：

$$
H\rightarrow C\ \text{可以强依赖},\qquad
(C,R)\rightarrow H\ \text{必须不存在或弱、有界且可验证}.
$$

## 3. Stage1 应向 Stage2 暴露什么

理想的 redesign latent contract 是：

$$
z_h^{\mathrm{base}},\qquad
z_c^{\mathrm{base}},\qquad
r_{hc}.
$$

最终解码可写为：

$$
\widetilde z_h=z_h^{\mathrm{base}}+A_h(r_{hc}),\qquad
\widetilde z_c=z_c^{\mathrm{base}}+A_c(r_{hc}),
$$

并要求：

$$
\lVert A_h(r_{hc})\rVert\ll\lVert z_h^{\mathrm{base}}\rVert,
$$

而 `A_c` 可以更强，因为 Camera trajectory 本就需要依赖 Human framing。

三模式对应：

$$
\text{Direct-H}:\quad T_h\rightarrow z_h^{\mathrm{base}},
$$

$$
\text{Direct-C}:\quad z_h^{\mathrm{obs}}+T_c
\rightarrow z_c^{\mathrm{base}},r_{hc},
$$

$$
\text{joint}:\quad T_h+T_c
\rightarrow z_h^{\mathrm{base}},z_c^{\mathrm{base}},r_{hc}.
$$

若 `r_{hc}=R_{hc}(z_h,z_c)` 是确定性 relation bridge，不必为它建立第三条
flow；它可作为 relation objective、sampling guidance、framing constraint 或
Camera condition encoder。只有当它包含独立随机性时，才与 Camera 一起建模：

$$
(z_c,r_{hc})\sim p_C(z_c,r_{hc}\mid H,T_c),
$$

且 Direct-H 永远不能依赖它。

## 4. Protected-H Dual-Stream ViMoGen

### 4.1 Human stream：冻结的 foundation prior

先在通过 gate 的 redesign Stage1 latent 上重新训练 Human-only ViMoGen-light
CLIP teacher：

$$
v_h=f_H(x_h,t,T_h).
$$

旧 E6 checkpoint 绑定 C3 Human128，不能假设可直接迁移到 redesign latent。
新 teacher 通过验证后，固定为三模式系统的 Human anchor。

严格保护要求：

- Direct-H 使用与 teacher 完全相同的 forward path。
- Camera tokens 在该路由中不存在，而不是用零 tensor 占位。
- Camera text 不进入 Human cross-attention。
- Human projection、Transformer、normalization、FFN 与 head 均独立。
- strict MVP 中 Human stream 完全冻结。

因此：

$$
f_H^{\mathrm{unified}}(x_h,t,T_h,m=H)
\equiv f_H(x_h,t,T_h).
$$

### 4.2 Camera stream：独立 vector field

Camera 使用独立参数：

$$
v_c=f_C(x_c,t,T_c,C_H,C_R),
$$

其中 `C_H` 是 Human motion context，`C_R` 是 framing/relative-geometry
context。Camera 必须拥有独立 input projection、timestep modulation、
normalization、self-attention、text cross-attention、FFN 和 output head。

### 4.3 Camera 读取 predicted-clean Human

采用 rectified-flow 参数化：

$$
x_h=(1-t)\epsilon_h+t z_h,\qquad
v_h^{\mathrm{target}}=z_h-\epsilon_h.
$$

teacher 的单步 clean estimate 为：

$$
\widehat z_h^{\mathrm{clean}}=x_h+(1-t)v_h.
$$

joint Camera context 使用：

$$
C_H^{\mathrm{joint}}
=g_H(t)E_{HC}\!\left(
\operatorname{sg}[\widehat z_h^{\mathrm{clean}}]
\right),
$$

而不是 noisy `x_h`。`sg` 只阻断 Camera objective 向 Human teacher 回传，
不会阻止 context 随采样状态演化。

trust gate 可取：

$$
g_H(t)=t^\gamma
\quad\text{或}\quad
g_H(t)=\sigma(at+b),\ a>0.
$$

本参数化中小 `t` 噪声更大，因此早期少信任 Human，随 `t` 增大再加强
framing condition；Direct-C 使用 observed/GT Human 时令 `g_H=1`。

### 4.4 三模式必须显式路由

| mode | 生成目标 | 条件 | Human path |
| --- | --- | --- | --- |
| Direct-H | Human | Human text | teacher 原路径；Camera 完全 bypass |
| Direct-C | Camera/relation | observed Human + Camera text | Human 仅作 stop-gradient condition |
| joint parallel | Human + Camera/relation | Human text + Camera text | teacher 生成 Human；Camera 读取 evolving predicted-clean Human |

mode tag 为：

$$
m\in\{H,\ C\mid H,\ HC\}.
$$

缺失模态必须由计算图和 attention topology 表示，不能以全零 tensor 伪装。
observed-Human completion 与 free joint generation 必须分开训练、评测和列表。

### 4.5 Strict triangular MVP

MVP 的 joint flow 为：

$$
\frac{\mathrm d}{\mathrm dt}
\begin{bmatrix}x_{h,t}\\x_{c,t}\end{bmatrix}
=
\begin{bmatrix}
f_H(x_{h,t},t,T_h)\\
f_C(x_{c,t},t,T_c,E_{HC}(\operatorname{sg}[\widehat z_h^{\mathrm{clean}}]),C_R)
\end{bmatrix}.
$$

这是 block-triangular coupling：

$$
H\rightarrow C,\qquad C\nrightarrow H,
$$

从而：

$$
p_{\mathrm{joint}}(H\mid T_h,T_c)=p_{\mathrm{teacher}}(H\mid T_h).
$$

它的优点是可从结构上证明 Human non-degradation；缺点是容易被评价为
`generate Human → conditionally generate Camera` 的 sequential factorization，
而不是真正双向 joint generation。因此它是必须先建立的可靠 MVP/上界，不一定
是最终论文模型。

### 4.6 可选 bounded relation residual

strict MVP 稳定后，才允许 joint-only Human residual：

$$
v_h^{\mathrm{joint}}
=f_H(x_h,t,T_h)
+\alpha(t)P_{\mathrm{rel}}\Delta_H(x_h,x_c,t,T_h,T_c,C_R).
$$

约束必须同时满足：

- `Delta_H` 采用 LoRA、低秩 adapter 或小 residual MLP；
- output projection zero-init；Direct-H 永久 bypass；
- `0 <= alpha(t) <= alpha_max`，且 `alpha_max` 很小；
- `P_rel` 仅允许影响 root translation、global heading、coarse timing/phase
  与 framing-relevant 低频姿态；
- Human backbone保持冻结，或学习率仅为 Camera branch 的 `0.02–0.1`；
- residual norm clipping，并使用 teacher/vector-field 与 decoded Human
  preservation。

此时形成 near-triangular coupling：Human 对 Camera 强依赖，Camera/relation
对 Human 只有弱、有界的反向调节。它只在显著改善 framing 或 joint interaction，
且通过 Human preservation gate 时保留；否则删除，退回 strict MVP。

## 5. Transformer 拓扑与初始化

推荐 dual-stream blocks：

```text
Human tokens
  ├─ Human self-attention
  ├─ Human-text cross-attention
  ├─ Human FFN
  └─ protected Human head

Camera tokens
  ├─ Camera self-attention
  ├─ Camera-text cross-attention
  ├─ H-to-C cross-attention
  ├─ relation/framing adapter
  ├─ Camera FFN
  └─ independent Camera head
```

joint attention topology：

| Query / Key | Human | Camera | Relation |
| --- | --- | --- | --- |
| Human | full | none | none in MVP; optional weak link later |
| Camera | full | full | full |
| Relation | full | full | full |

初始化规则：

- Human blocks/projection/norm/head 从 redesign Direct-H teacher 完整加载并冻结。
- Camera blocks可复制 Human blocks作初始化，但此后参数完全独立。
- Camera input/output projection重新初始化。
- H-to-C cross-attention output projection zero-init。
- C/R-to-H adapter zero-init，第一轮不开启。
- Human text 与 Camera text projection使用独立参数。
- mode embedding只做路由/对应分支调制，不能改变 Direct-H 计算图。

## 6. 分阶段训练路线

### Phase 0：先闭合 redesign Stage1 与 Human teacher

1. 只使用合规 Pulp-only redesign Stage1；mixed HML+Pulp checkpoint 禁用。
2. 先量化并定位 terminal Camera jump；完成 true-length Stage1 Human、Camera、
   projection gate后再冻结 encoder/owning decoder。
3. 在新 redesign latent 上重新训练 ViMoGen-light CLIP Direct-H teacher。
4. 以 canonical Human metrics、fixed cohort visual 和跨 seed复核其优势；通过后
   固定为 protected anchor。

### Phase 1：Direct-C specialist

冻结全部 Human stream，训练：

$$
z_h^{\mathrm{GT}}+T_c\rightarrow z_c,r_{hc}.
$$

只更新 Camera projection/blocks/norm/head、H-to-C adapter 与 relation/framing
module。Camera text必须独立 dropout，防止模型只读 GT Human trajectory而忽略
Camera text。

### Phase 2：Joint triangular training

同时构造 noisy Human/Camera states，由 frozen teacher 得到
`predicted-clean Human`，再只训练 Camera/relation stream。这样 Camera 在训练时
看到与推理一致的 evolving Human error，而不是永远完美的 GT Human。

可从较高的 GT-Human condition概率开始，随后衰减，使 Camera 最终主要在
predicted-Human condition下训练。

### Phase 3：统一三模式 checkpoint

初始采样比例可用 `Direct-H : Direct-C : joint = 2 : 2 : 1`，稳定后再改为
`1 : 1 : 1`。Human冻结时，Direct-H batch只作 exact regression与路由监控，
不应为不存在的可训练 Human gradient重复计入 objective。

### Phase 4：可选 bounded bidirectional coupling

只有 strict triangular 三模式全部过门，才打开 joint-only `Delta_H`。先放在
Transformer最后三分之一 blocks；zero-init、低秩、小学习率、norm clipping。
若 framing/joint gain不足或 Human non-inferiority失败，立即删除该路径。

## 7. Optimization objective 与 guidance

Human/Camera flow objective分别基于：

$$
L_{\mathrm{RF}}^h
=\mathbb E\lVert f_H(x_h,t,T_h)-(z_h-\epsilon_h)\rVert_2^2,
$$

$$
L_{\mathrm{RF}}^c
=\mathbb E\lVert f_C(x_c,t,T_c,C_H,C_R)-(z_c-\epsilon_c)\rVert_2^2.
$$

可逐步加入：

- latent relation objective：在 predicted-clean latents 上匹配 Stage1 relation bridge；
- decoded framing objective：subject screen center/scale、head room、relative
  azimuth、Camera distance、visibility 与 out-of-frame；
- bounded residual阶段的 vector-field preservation 与 decoded Human pose/root/
  velocity/contact preservation。

不要在训练初期对所有高噪声 timestep频繁解码完整 Human/Camera。先用 latent
relation，稳定后只在中低噪声区域低频加入 decoded projection supervision，使用
例如 `I[t >= t_min] * t^eta` 的 timestep weighting。

CFG 与 condition dropout必须按模态拆分：

- `s_h`：Human text guidance；
- `s_c`：Camera text guidance；
- `s_H`：Human-condition guidance；
- `s_r`：Human–Camera relation guidance。

Camera training必须实际出现 Camera text、Human context、relation context的独立
dropout组合，否则推理时无法可靠分解 guidance。尤其要避免 Camera text从不
dropout或 Human context从不dropout造成 shortcut。

## 8. 必须预注册的验证与消融

### 8.1 Direct-H exact regression

固定 text、initial noise、sampler、steps、CFG、precision与 seed，比较 teacher和
unified `m=H` 输出：

$$
\max_i\left|\widehat z_i^{\mathrm{teacher}}
-\widehat z_i^{\mathrm{unified},m=H}\right|
\leq\epsilon_{\mathrm{fp}}.
$$

失败说明 router、normalization、cache、mixed precision或共享参数污染了
protected path，必须停止。

### 8.2 Human non-inferiority

- strict MVP 的 Direct-H 与 joint-H 应逐样本完全相同或只有浮点误差。
- bounded residual必须预声明每项 canonical Human metric的 non-inferiority
  margin，并报告 bootstrap confidence interval与同步盲视觉偏好。
- 不得用 optimization objective下降替代 decoded Human gate。

### 8.3 Camera 与 joint gate

- Direct-C：在 observed Human + Camera text 条件下评测完整 Camera trajectory、
  framing/out-of-frame、CLaTr与 projective geometry。
- joint parallel：同一 checkpoint自由生成 Human+Camera，完整报告 Human、Camera
  与 joint/projective metrics；不得与 Direct-C 混表。
- 固定 Human/text/noise，只改变 Camera text（如 dolly、orbit、static close-up、
  track-behind）：strict MVP应满足 Human不变、Camera显著且语义一致地变化。

可定义 intervention sensitivity：

$$
S_H=\operatorname{mean}_{i\ne j}d_H(H^{(i)},H^{(j)}),\qquad
S_C=\operatorname{mean}_{i\ne j}d_C(C^{(i)},C^{(j)}).
$$

strict MVP期望 `S_H ≈ 0` 且 `S_C >> 0`；bounded residual只允许 root/heading/
timing的受限变化，并且这些变化必须对应可测的 framing improvement。

### 8.4 Stage1 terminal Camera probe

从现有 fixed samples读取最后两步 Camera center displacement、SO(3) geodesic与
projection delta，并与倒数第二步、GT、sequence-length modulo分组比较；再做
last-frame hold/clamp replay。只有 spike稳定对应 decoder phase、crop或 Camera14
velocity endpoint，才能判断根因。

### 8.5 ViMoGen attribution ladder

固定 Stage1 representation、ordered IDs、CLIP cache、owning decoder、参数量级与
training exposure，逐项切换：

1. pooled CLIP → token-sequence cross-attention；
2. Conv1d U-Net → full Transformer，objective/sampler不变；
3. diffusion → shifted flow，topology/text不变；
4. Unified exposure → Human-only exposure，backbone不变。

若预算只够一个 probe，优先做同一 ViMoGen Transformer 的 pooled-CLIP 对照。
在 ladder闭合前，结论保持为 system-task fit，而不是 pure-backbone capacity。

## 9. 接力 Agent 的最小交付

1. 把上述方案转成新的、可审计 experiment contract；不要复用任何旧 eval/run root。
2. 先完成 redesign Pulp-only Stage1 gate与 terminal Camera probe。
3. 在冻结的 redesign Stage1 上训练并验证 ViMoGen-light CLIP Human teacher。
4. 依次完成 Direct-C specialist、strict triangular joint与 unified routing。
5. 通过 exact Direct-H regression、Direct-C、joint parallel和 Camera intervention
   后，才决定是否尝试 bounded residual。
6. 结果只写入 canonical owners：数值进 ledger，当前决策进 `current.md`，版本事件
   进 `version_family.md`；本页不扩展为第二份运行日志。

最终模型应保持：

$$
\boxed{
\begin{aligned}
v_h&=f_H(x_{h,t},t,T_h)
+\underbrace{\alpha(t)P_{\mathrm{rel}}\Delta_H(\cdot)}_{
\text{仅在通过 strict MVP 后可选}},\\
v_c&=f_C\!\left(
x_{c,t},t,T_c,
g_H(t)E_{HC}(\operatorname{sg}[\widehat z_h^{\mathrm{clean}}]),
C_R
\right).
\end{aligned}
}
$$

一句话原则：**Human prior 必须被结构性保护；Camera 可以强依赖 Human；Camera
对 Human 的反向影响必须弱、有界且通过 intervention 验证。**
