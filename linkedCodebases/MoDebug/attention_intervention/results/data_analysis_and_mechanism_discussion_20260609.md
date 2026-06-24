# 数据分析与机制讨论

## 证据边界

本讨论基于：

- Attention intervention: MotionCLR/MotionGPT formal eval；MoLingo 20260609 official-setting representative rerun。
- LDO/DSO: formal root `/data/public/ripemangobox/Motion/experiments/MoDebug/ldo_dso/formal_20260608`。
- 阅读清单: `obsidian-vault/ideas/MoDebug/2026-06-09_training-dynamics-reading-list.md`。KMM/FunPhase 在本地 analysis notes 中未核到完整 note，不作为硬证据。
- DeepSeek max 复核边界：跨模型 late `CFG_CA` 退化是 hard evidence；“通用 CFG cond/uncond 深层融合脆弱性”是 hypothesis，不是已证明机制。

## 支持的结论

| 标签 | 结论 | 证据 |
|---|---|---|
| Hard evidence | MotionCLR `CFG_CA` 在 layer 12-15 存在严重退化。 | layer 14 FID 4.4429 / Top3 0.1694，layer 15 FID 3.3691 / Top3 0.0996；layer 16/17 恢复近 baseline。 |
| Hard evidence | MoLingo `CFG_CA/layer_15` 存在严重退化。 | FID_TMR 7.7003、Top1 0.7240、Top3 0.9165、Matching 15.7381；hook/replacement counts 均为 6850，missed/shape mismatch 为 0。 |
| Hard evidence | MotionGPT 支持的 SA/CA intervention 对 aggregate metrics 无显著冲击。 | baseline FID 0.1945；SA mean 0.2013；CA mean 0.1954；CFG family 是 unsupported，不是漏跑。 |
| Diagnostic proxy | MotionCLR DSO 显示 quality/alignment 从 step 4 到 step 7 大幅形成。 | FID 27.2832 -> 0.1703，Top3 0.1774 -> 0.7414。 |
| Diagnostic proxy | MoLingo LDO endpoint 4/10 移除后续层会显著改变输出数组。 | early L2 mean 6570.3259；middle L2 mean 5096.3232。 |

## 不支持的结论

- late `CFG_CA` 退化尚未证明来自通用 CFG 机制；跨模型现象只支持该 hypothesis，成因仍需 cond/uncond 表征、scale sweep、swap/restore、natural-representation check。
- MotionCLR DSO step10 不能与 attention baseline 直接比较成“优于 baseline”；协议一致性未确认，它只作为 DSO formation curve proxy。
- MoLingo LDO late endpoint 0 距离不能解释成 layer 15 恒等、冗余或 early-exit；这是“最后一层后无层可替换”的构造性结果。
- MotionGPT SA/CA 不敏感不能推出“MotionGPT 没有层分工”；只能说明该 intervention/evaluator 组合未观测到显著影响。

## 核心结论

- MotionCLR 与 MoLingo 都出现 late `CFG_CA` 退化，是最强跨模型发现。
- MoLingo `CFG_CA/layer_15` 是 MoLingo representative layers 中最严重退化点，并显著拉高 `CFG_CA` family mean。
- MotionGPT 的 SA/CA 不敏感和 CFG unsupported 是有效对照，但不能证明或反驳 late-CFG hypothesis。
- LDO/DSO 只作为 diagnostic proxy，不作为 official quality ranking。

## 可借鉴的数据分析思路

1. **模型无关 late-CFG branch diagnosis。**

   抽取 MotionCLR 与 MoLingo 的 cond/uncond hidden、attention output 和 replacement 前后输出，统一计算 cosine、norm ratio、attention entropy、MMD/EMD、representation drift。目标是区分“相同表征模式崩坏”和“不同架构各自脆弱”。

2. **CFG scale sweep。**

   对 MotionCLR layer 12-15 与 MoLingo layer 10/12/14/15 做 `cfg=1.0/3.0/5.5/7.5/10.0` sweep。若退化随 scale 单调增强，支持 CFG overdrive；若非单调或只在特定层出现，说明存在 layer-specific branch coupling。

3. **DSO 作为 formation curve。**

   MotionCLR step 1/4/7/10 显示可解释跳变。后续 adapter、CFG scale sweep、loss repair 都应对比 DSO 曲线，但需先确认协议是否和 attention baseline 可比。

4. **Frame × joint/body-part delta。**

   参考 ReMoGPT 的六部位 ontology，将 intervention 输出差异聚合到 root/spine/left arm/right arm/left leg/right leg，再和文本中的 body-part phrase 对齐。全局 FID/R-Precision 无法解释 left/right、hand/leg、direction 类错误。

5. **Token/codebook 统计。**

   对可重新编码的输出统计 codebook perplexity、dead-code usage、base token vs residual token change、token distance、transition token distance。MoMask/T2M-GPT/M2D2M 的共同启发是：base/RVQ token 更接近动作语义，residual/transition token 更接近局部质量和转场。

## 机制设计建议

### P0: 机制证据

- MotionCLR `CFG_CA` 12-15: cond/uncond cosine、norm ratio、attention entropy、MMD/EMD、CFG scale sweep、swap/restore。
- MoLingo `CFG_CA` layer 10/12/14/15: 同样诊断，其中 layer 15 是最高优先级。
- 记录 natural-representation check：若 metric 变化伴随巨大 off-manifold drift，只能说干预破坏自然表征，不能直接声称该层负责语义。

### P1: Attention Buffer Router

在已定位的危险层插入轻量 router/adapter，输入 cond/uncond attention output 或差值，输出 `alpha in [0,1]`，以可学习方式调节 `cond - uncond` 注入强度。

最小验证：

- MotionCLR 先做 layer 14/15；MoLingo 先做 layer 15。
- 与固定降低 CFG scale 对照。
- 成功标准：危险层 intervention FID/Top3 回到接近 baseline，同时正常层和 baseline generation 不变坏。

风险：

- 若崩溃来自 off-manifold hidden，不是 scale 问题，router 可能只学会关闭干预，解释力有限。
- 跨模型 router 若共享设计，必须证明它不是只拟合某个 evaluator 或某个 layer index。

### P2: Spatial-Temporal Guided Adapter/Loss

使用两个弱耦合模块，而不是预设 `CA=alignment`、`SA=quality`：

- `AlignAdapter`: 放在 probe 显示 text-motion alignment 敏感的 block，loss 使用 TMR/MoLingo-SAE similarity、caption-action phrase match、R-Precision proxy。
- `QualityAdapter`: 放在 contact/smoothness/jerk/high-energy window 敏感 block，loss 使用 foot skating、smoothness、jerk、root trajectory、transition error。

最小验证：

- spatial 使用 ReMoGPT 六部位。
- temporal 先用 motion energy / transition windows。
- loss weight 保守，例如归一化后 `0.8-1.3` 范围。
- 必须有 shuffled body-part groups 和 shuffled temporal windows 对照。

风险：

- 若 evaluator 对 motion-text alignment 不敏感，alignment loss 可能优化 proxy 而不改善真实语义。
- 若 spatial/temporal 权重过强，可能导致 codebook usage 偏斜或局部动作过拟合。

### P3: Probe-first LDO 替代强解码

MotionCLR/MotionGPT 的 LDO 已合理 blocked。下一步不是强行 decode hidden，而是训练 probe：

- alignment probe: TMR/MoLingo-SAE similarity、text-action phrase classifier。
- quality probe: contact、smoothness、jerk、root velocity、phase/frequency。
- token probe: codebook index/reconstruction error。

目标是把 intervention 不敏感拆解为“表示没有承载信息”还是“decoder/evaluator 读不出来”。

## 优先级

1. MotionCLR 与 MoLingo 并行做 late-CFG branch diagnosis。
2. 做 CFG scale sweep，检查退化是否 scale-dependent。
3. 开发 Attention Buffer Router 最小原型，先在最坏层上验证。
4. 进入 spatial-temporal adapter/loss 前，先完成成因诊断与对照。
