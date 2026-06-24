---
created: 2026-04-10
updated: 2026-04-11T10:30
status: proposal-v3
title: TAMR Stage4.1 Patch-Event Diag Alignment Design V3
model_name: TAMR
tags:
  - tamr
  - stage4.1
  - patch-event-alignment
  - diag-alignment
  - temporal-grounding
source:
  - /home/ripemangobox/Coding/Github/Motion/TMR/ResearchWY/paperIDEAs/TAMR/2026-04-06_tamr-v3-event-abstraction-centered-design.md
  - /home/ripemangobox/Coding/Github/Motion/TMR/ResearchWY/paperIDEAs/TAMR/Temporal_Alignment/2026-04-10_temporal-alignment-scheme-evolution.md
  - /home/ripemangobox/Coding/Github/Motion/TMR/ResearchWY/paperIDEAs/TAMR/eval_summary/2026-04-10_tamr-motionpatches-stage4-first-pass-eval-summary.md
---
# TAMR Stage4.1 Patch-Event Diag Alignment Design V3

> Post-Claude repositioning:
> 这份文档现在应理解为 `full mechanism blueprint`，不是当前 immediate execution plan。
> 当前真正执行应以 `V4 narrow-scope` 为准：先做最小 event-time head 诊断，再决定是否进入 `BASMA+`。
> `V1 / V2 / review` 草稿已在 `2026-04-11` 合并进 `2026-04-10_temporal-alignment-scheme-evolution.md`；本文是保留的完整机制蓝图版本。

## 0. Final Recommendation (Why this over V1/V2)

We keep V1 的核心优点（time-band + patch-support）并采纳 V2 的修正（background-aware、soft monotonic、可证伪诊断），形成 **BASMA+**：

1. 内容驱动的 event-time support（保留 time-band 解释力）。
2. 弱顺序偏置 + 软单调正则，而非强制分段（避免“天生对角线”假对齐）。
3. 独立 background gate + null-event abstention（允许 no-evidence / transition）。
4. per-event 时间归一化 + 多部位受控激活 patch-support（保留 patch-level 可解释性）。
5. masked InfoNCE（避免同样本 event 互为强负例）。
6. 可复现的诊断指标 + 破坏性 sanity checks（防止“热图好看但是先验”）。

优于 V1：去掉强覆盖 / 结构锁死顺序，增加 background & abstain 能力。

优于 V2：重新强调 patch-support 的可解释性与目标熵带，同时把实验顺序、go/no-go、升级路径写清，方便在 Stage4.1 直接执行。

---
## 1. 最终机制：BASMA+

**输入与表示**
- `H ∈ R^{B×T×P×D}`：14×5 patch grid token；`H_bar[t] = mean_p H[t,p]`；`H_cls` 全局。
- `E ∈ R^{B×K×D}`：event embeddings（来自 GT decomposed events）。

**时间支持（content-first + weak order）**
- 内容项：`S_content(k,t) = ⟨W_e E_k, W_t H_bar[t]⟩ / sqrt(D)`。
- 弱顺序偏置：`mu_prior = (k+0.5)·T/K`；`mu_hat = mu_prior + MLP_mu([E_k, H_cls])`；`sigma_hat = sigma_min + softplus(MLP_sigma([E_k, H_cls]))`；`S_order(k,t) = - (t - mu_hat)^2 / (2·sigma_hat^2)`。
- 事件门：`Q_evt(k,t) = sigmoid(α·S_content + β·S_order)`（不在 k 维 softmax）。
- 背景门：`Q_bg(t) = sigmoid(w_bg^T H_bar[t])`。
- per-event 归一：`A_time(k,t) = Q_evt(k,t) / sum_t Q_evt(k,t)`（若 sum 很小则跳过该 event）。
- 诊断占用：`Occ(t) = 1 - ∏_k (1 - Q_evt(k,t))`；`Abstain(t) = Q_bg(t)·(1-Occ(t))`。

**patch 支持（受控多激活）**
- 相似度：`S_patch(k,t,p) = ⟨U_e E_k, U_p H[t,p]⟩ / sqrt(D)`。
- 推荐实现：`Q_patch = sigmoid(S_patch)`，按 p 归一后用于 pooling，并用目标熵带正则（允许 2-3 个 patch 同时高）。
- 池化：`A_patch(k,t,p) = A_time(k,t) * normalize_p(Q_patch(k,t,p))`。
- 事件表征：`Z_k = Σ_{t,p} A_patch(k,t,p)·H[t,p]`。

**对齐监督（masked InfoNCE）**
- 正例：同样本 `(b,k)` 的 `(Z_k, E_k)`。
- 负例：其他样本的 events 为主；同样本其他 events 仅作低权 hard negatives（可选）。

---
## 2. 训练目标（losses）

必选（Stage4.1 必做）
1. `L_global`: 原有 global retrieval loss（主路径保持）。
2. `L_evt_align`: masked InfoNCE（event pooled motion ↔ event text）。
3. `L_order_soft`: 对 `mu(k)` 的软单调 margin；基于 `A_time` 而非结构硬编码。
4. `L_cont`: TV/平滑，避免碎片化时间支持。
5. `L_bg_sep`: `mean_t Occ(t)·Q_bg(t)`，防止 background 与 event 同时全亮。
6. `L_evt_mass`: GT event 最小质量约束，防止塌到 0 但不强制覆盖全段。
7. `L_null_abstain`: 对伪负/随机/替换事件要求低总质量（支撑 existence/negation/no-evidence）。
8. `L_patch_band`: patch 熵目标带，鼓励“受控多激活”。

可选（future upgrade）
- `L_adapter_align`: 若后续开启 adapter guidance，再用 `A_time` 软标签监督 adapter；当前默认关闭。
- `L_multi_span`: 若要支持明显并行事件，可加 mixture-of-Gaussians 时间门或多峰稀疏正则。
- `L_ctf`: coarse-to-fine token compressor / DTW-style path（不在 Stage4.1）。

---
## 3. 诊断指标（可复现且可反证）

核心指标
- `abstention_rate = mean_t Abstain(t)`
- `background_leakage = mean_t Occ(t)·Q_bg(t)`
- `order_sensitivity_delta`: 原顺序 vs shuffle 后的 (A_time 变化 + mu 排序变化 + L_evt_align / retrieval 差值)
- `prior_copy_ratio`: corr(A_time, S_order_only)
- `patch_entropy`: 与目标熵带的偏差
- `event_mass`: `sum_t Q_evt(k,t)`（含伪负事件）
- `coverage_gap`: mean_t (1 - Occ(t))（留意不要被强覆盖压成 0）

可视化
- `K×T` A_time 热力图（含 background channel）
- `K×T×P` A_patch 支持图

---
## 4. Sanity Checks（必须执行）

S1 Motion time shuffle：打乱时间轴，应使 A_time 失稳、L_evt_align 变差、order_sensitivity_delta ↑。
S2 Event text shuffle/replace：事件顺序/内容扰动应让对应 event_mass ↓，中心/跨度改变，检索/对齐分数下降。
S3 Prior vs Content：content-only、order-only、full 三组对照，确认提升源自内容而非先验。
S4 Null-event：对伪负事件，检查 event_mass 是否接近 0、Abstain 是否上升。
S5 Patch collapse：监控 patch_entropy 是否落在目标带内，防止 one-hot 或全均匀。

---
## 5. 最小实验顺序（Stage4.1 执行版）

B0 当前实现 baseline（independent softmax + gaussian + summed target）。
B1 content-only BASMA+（S_content + background gate，禁用 order/patch）。
B2 B1 + L_order_soft（软单调 regularizer）。
B3 B2 + weak S_order bias（完整 BASMA+ time）。
B4 B3 + patch support + L_patch_band（恢复 patch 解释力）。
B5 B4 + L_null_abstain（加入 existence/negation 能力）。
B6 B5 + 全部 sanity checks（若失败，停在 B5，不开 adapter）。
B7 （可选）B5/B6 + adapter guidance 探索；若伤主检索或 sanity 失效，立即回退。

---
## 6. Go / No-Go Gate（执行前即声明）

Must-pass
1. 主检索无灾难性回撤；content-only → full 的提升不是纯 prior-copy。
2. reorder / replacement 下对齐图和分数显著变化（order_sensitivity_delta > 预设阈值）。
3. background_leakage 低于阈值；abstention_rate 不塌到 0 或 1。
4. patch_entropy 落在目标带；无大面积 patch collapse。
5. relation 面板（ordering/duration/existence/negation）至少在 paired 诊断上有可解释差异。

Immediate stop
1. prior-only ≈ full；或 order_sensitivity_delta ≈ 0。
2. background 占据绝大部分 bins 或与 event 高重叠。
3. patch 支持 one-hot 或全均匀且无法靠 L_patch_band 修正。
4. sanity checks（S1-S5）中任一显著失败。

---
## 7. Stage4.1 必做 vs Future Upgrade

必做（在本轮完成）
- BASMA+ 核心：content-first time support + weak order bias + background gate + per-event norm + patch entropy band + masked InfoNCE。
- 核心 losses：L_global, L_evt_align, L_order_soft, L_cont, L_bg_sep, L_evt_mass, L_null_abstain, L_patch_band。
- 核心诊断 + S1-S5 sanity checks。
- B0~B6 实验序列，输出诊断图与指标。

Future upgrade（不在本轮）
- coarse-to-fine / DTW-style soft path（降低 T 依赖或长序列扩展）。
- multi-peak event gate（显式支持 while/overlap，更复杂才开启）。
- adapter guidance & evidence head（仅在 BASMA+ 通过 gates 后再试）。
- window proposals / hierarchical token compression（接近 PST/CONE 路线）。

---
## 8. 交付物与接口

- 代码改动优先集中在 `models/clip.py`（保留 patch grid、替换对齐逻辑、输出诊断）、`train.py/test.py`（cfg 增参 + diag 导出）。
- 配置新增 `alignment.mode = basma_plus`，显式开关 background/patch entropy band/order bias/abstention。
- 诊断导出统一写入新目录，避免覆盖历史结果。

---
## 9. 一句话总结

> BASMA+ = content-first time support + weak order bias + background-aware abstention + controlled multi-patch support + masked InfoNCE + falsifiable diagnostics；先保主检索与诊断可信度，再谈 adapter/grounding 升级。
