---
title: "StoryMotion Stage1/Stage2 Redesign Handoff — 2026-07-27"
status: handoff_ready
hypothesis: |
  StoryMotion should preserve a Camera-invariant Human prior, model Camera and
  Human–Camera relations through explicit bounded paths, and evaluate every
  Stage/mode with decoded canonical evidence rather than optimizer objectives.
tags:
  - StoryMotion
  - stage1
  - stage2
  - handoff
  - architecture
  - status/active
aliases:
  - StoryMotion-Stage1-Stage2-Redesign-Handoff
source_notes:
  - "[[ideas/StoryMotion/current]]"
  - "[[ideas/StoryMotion/StoryMotion-valid-metric-ledger]]"
  - "[[ideas/StoryMotion/StoryMotion-metric-computation-io]]"
  - "[[ideas/StoryMotion/version_family]]"
  - "[[ideas/StoryMotion/StoryMotion_Checkmate]]"
  - "[[ideas/StoryMotion/2026-07-27_storymotion-stage1-human-anchor-residual-control]]"
  - "[[ideas/StoryMotion/2026-07-18_storymotion-latent-generatability-stage2-diagnostic-ladder]]"
created: 2026-07-27T17:55:26+08:00
updated: 2026-07-27T17:55:26+08:00
---

# StoryMotion Stage1/Stage2 Redesign Handoff

> [!abstract] 接力摘要
> v8.1C C3-25 seed17 non-causal Stage1 与 Unified-3 `105K` 仍是唯一完成三模式 formal audit 的 mainline。ViMoGen-light CLIP 是本轮 fixed-C3 Human-only canonical + fixed-8 视觉综合胜者，但没有 Camera/joint branch且 strict physical gate未闭合。redesign Pulp-only 证明 Human-first asymmetric decoupling具有结构价值；HML+Pulp mixed checkpoint 因把非同源 rot6D 均值填充为无 missingness 的输入而正式 invalid for Stage2。下一位 agent 应先把下方架构草稿收敛为 matched、分阶段、可审计的实验合同，不能直接从 mixed checkpoint 启动 Stage2。

## 给接力 Agent 的完整 Prompt

你接力 StoryMotion Stage1 redesign、Stage2 protected dual-stream ViMoGen 与统一三模式评测任务。

当前日期：`2026-07-27`

工作目录：

`/home/ripemangobox/Coding/Github/OpenSource/On_Process/BITE_Process`

### 1. 接力目标

把本会话已经闭合的 metric、Stage1 representation、Stage2 external-backbone 与 visual evidence转化为下一轮**最小 matched 实验设计**：

1. 不破坏现有 C3-25 Human prior与三模式 mainline。
2. 将 redesign Stage1 的 Human-first asymmetric decoupling保留下来，但先解决 HML rot6D provenance 与 terminal Camera jump，再讨论 promotion。
3. 将 ViMoGen-light CLIP 的 Human-only优势扩展为 protected Human stream + independent Camera stream + bounded relation coupling，而不是直接拼接 H/C latent共用单一 backbone。
4. Direct-H、Direct-C、joint parallel必须显式路由、分别评测；observed-Human Camera completion不得与 free joint generation混表。
5. 所有正式判断只使用 decoded canonical metrics与同步/盲视觉证据；训练目标、optimizer标量和 TensorBoard仅作 run provenance。

### 2. 开始前必须完整阅读

1. 根目录 `AGENTS.md`。
2. `linkedCodebases/StoryMotion/AGENTS.md`。
3. `linkedCodebases/StoryMotion/docs/experiment-contract.md`。
4. [[ideas/StoryMotion/current]]。
5. [[ideas/StoryMotion/StoryMotion-valid-metric-ledger]]。
6. [[ideas/StoryMotion/StoryMotion-metric-computation-io]]。
7. [[ideas/StoryMotion/version_family]]。
8. [[ideas/StoryMotion/StoryMotion_Checkmate]]，重点阅读 §10–§12。
9. [[ideas/StoryMotion/2026-07-27_storymotion-stage1-human-anchor-residual-control]]。
10. [[ideas/StoryMotion/2026-07-18_storymotion-latent-generatability-stage2-diagnostic-ladder]]。
11. 本页下方“原始架构草稿”全文；它是待审计 proposal，不是已授权 contract。
12. 完整读取并使用 `rf-obsidian-markdown` skill；若进行研究方案设计，同时使用 `research-thinking`。

编辑任何 Obsidian Markdown 前后都运行：

```bash
python3 linkedCodebases/StoryMotion/scripts/storymotion_experiment_harness.py audit-doc \
  obsidian-vault/ideas/StoryMotion/StoryMotion-valid-metric-ledger.md
```

修改其他 StoryMotion owner 时，也分别对该文件执行 `audit-doc`。不要让 BlackBoard 成为第二个 metric、decision 或 version owner。

### 3. 当前 worktree、同步与部署快照

- 本地 BITE：branch `main`，HEAD `72916358223db2c57c01edd7ceac494d49077ad5`；存在大量任务外既有 dirty/untracked 内容。只处理明确目标，禁止 blanket add/commit、reset、checkout覆盖或全目录 rsync。
- 4090 StoryMotion：branch `agent/integrate-20260718`，HEAD `35872ce5b463a318d336c2ff7dd43261307e91d7`，clean。
- 5090 StoryMotion：同 branch、同 HEAD、clean；两边已 commit + push并同步。
- 统一 Gradio 在4090 `0.0.0.0:7865`，当前 PID `3539069`，HTTP 200。Mac访问：

```bash
ssh -N -L 17867:127.0.0.1:7865 4090
```

- 当前页位于被 `.gitignore` 覆盖的 `obsidian-vault/*` 新文件区域；不要因为 `git status` 看不到本页就误判文件不存在，也不要未经用户要求强制加入 Git。

任何新 run、checkpoint、fixed samples、records、metrics、visual或失败日志都必须使用新 root，禁止覆盖、复用或补写旧 root。StoryMotion Stage1/Stage2 全路径必须显式断言 `is_causal is False`。

### 4. 已完成的核心任务

#### 4.1 Metric ledger统一

- [[ideas/StoryMotion/StoryMotion-valid-metric-ledger]] 已删除所有 loss 数值、loss表和 loss-based ranking。
- 正式数值只保留 Human、Camera、joint/projective decoded canonical metrics；训练 objective 名称只作方法 provenance。
- C3-25、MARDM、ViMoGen-light CLIP、ViMoGen-light UMT5 的适用 Human schema已补齐；Human-only specialist没有伪造 Camera/joint 字段。
- Direct-C 是 decoded observed Human + Camera text completion；joint parallel 是同 checkpoint自由生成 H+C；两者已分开。
- ledger当前 `loss/MSE` 全文搜索无结果；39个 Markdown tables列数一致，36个 `version / run` 表逐行非空。

#### 4.2 Stage2 external Human-only controls

E5 MARDM formal N=512：

`e5_c3_mardm_sit_xl_human128_105k_eval_r2_pure512_mar18_seed17_4090g0_20260726`

E6 ViMoGen-light CLIP formal N=512：

`e6_c3_vimogen_light_clipseq_h_105k_eval_r1_pure512_euler50_seed17_4090g1_20260726`

E6 ViMoGen-light UMT5 formal N=512：

`e6_c3_vimogen_light_umt5base_h_105k_eval_r2_pure512_euler50_seed17_5090g2_20260726`

三者与 C3 comparator使用同一 first-512 ordered cohort：

`6b9c92a533d2d0aff76cce6c7ad23361733fb38d3157128bf7eee56cdc33d8df`

结论：

- ViMoGen-light CLIP 是本轮 Human-only 综合 canonical endpoint与 fixed-8 视觉胜者。
- UMT5 只在 HCov更好，不能据此称其优于 CLIP；“更大语言编码器”不是当前已证明瓶颈。
- MARDM、CLIP、UMT5 都未通过 strict Human physical-quality gate。
- MARDM/ViMoGen相对 C3 同时改变 topology、objective、sampler或condition；只能叫 system-task fit，不能叫 pure-backbone capacity证据。
- 三条都是 Human-only specialist，没有 Camera/joint能力，不替换 C3-25 Unified-3 mainline。
- E5 fixed-8 root/body interchange只支持 root/heading 是该 fixed cohort 的主要全局误差放大器；不能外推 population prevalence或 MARDM topology根因。

#### 4.3 Stage1 redesigned Human-anchor residual control

有效 training endpoints：

- Pulp-only：`stage1_hanchor_pulp_only_matched_r3_636k_seed17_4090g0_20260726`。
- HML-root-local + Pulp-full：`stage1_hanchor_hmlrootlocal_pulpfull_packedio_r3_636k_seed17_5090g2_20260726`。

两者均为 fresh `636K`、同 redesigned architecture：

`human_anchor_interaction_residual_199_14_128_16_48_v1`

结构为：

$$
z_h=E_h(H),\qquad z_{hc}=E_{hc}(H,C),\qquad z_c=E_c(C\mid z_h,z_{hc})
$$

$$
\hat H=D_h(z_h),\qquad (\hat C,\hat F)=D_{c,f}(z_h,z_{hc},z_c)
$$

已验证的核心不变量：`z_h=E_h(H)` 不读取 Camera；preflight随机替换 Camera 后 `z_h` 逐元素不变。它证明的是 `C↛H` 的 Human-first asymmetric decoupling，不是双向完全独立；Camera和projection仍按设计依赖 Human。

formal eval：

- C3-25 Stage1 Pulp true4053：`v8_1c_c3_25_stage1_636k_eval_r1_canonical_true4053_seed17_4090g0_20260727`。
- Pulp-only true4053：`stage1_hanchor_pulp_only_matched_r3_636k_eval_r4_true4053_seed17_4090g0_20260727`。
- mixed true4053：`stage1_hanchor_hmlrootlocal_pulpfull_packedio_r3_636k_eval_r4_true4053_seed17_5090g2_20260727`。
- 两条 HML true-val1460 eval均为 `r2_true_hmlval1460` lineage；精确 IDs、hash与结果只读 ledger。

正式解释：

- C3-25 的 Pulp Human reconstruction总体更强；redesign Pulp-only 的 Camera trajectory/rotation有局部优势，但 projective/Human不是全面 Pareto win。
- Pulp-only 与 mixed 的 GT-H Camera trajectory近似，Human/projective却显著分离，支持 Camera branch insulation，但不证明 joint geometry解耦。
- HML `N=1,460` 与 Pulp `N=4,053` 的优势反转来自 eval domain与训练 exposure对齐反转，不是 sample count本身。
- mixed改善 HML root/local、严重损害 Pulp Human/projective；更重要的是其 HML rot6D处理已被判为不合规，所以只能保留 retrospective diagnostic。

#### 4.4 fixed-first-64 与 `rN` 已澄清

- C3-25 与 redesigned Stage1 的 Pulp训练都没有 fixed-first-64裁切；Pulp使用动态有效长度，长 sample 的第65帧以后参与训练。
- HML adapter对超长动作使用最大300帧、stride240的重叠窗口，并补 tail-aligned窗口，不是只取首窗。
- formal eval逐样本 exact-valid-length进入 non-causal encoder/decoder，batch padding不可见。
- run名的 `r2/r3/r4` 是各自 artifact lineage内部 revision/retry ordinal；不是 setting、seed、epoch、模型代际或排名。完整语义只由 full run ID与相邻 contract决定。

### 5. 本轮新增的关键结论

#### 5.1 HML rot6D 的真实边界

rot6D 编码本身可以经 SO(3) 可靠转换；不可逆的是当前 RIC263上游：

- HumanML RIC263 的21-joint rotations来自规范化 joints上的 fixed-skeleton IK；Pulp `4:136` 来自 TRAM/SMPL 的22-joint local rotations。
- joint positions到rotations非单射：bone-axis twist不改变子关节位置，leaf rotation不改变任何 joint；IK只能依靠 prior/smoothing选一个解。
- uniform skeleton、floor/origin/facing canonicalization还丢失个体 rest offsets、shape与部分 root orientation。
- 因而不能从现有 RIC263恢复“Pulp/TRAM会观测到的那组旋转”；当前 adapter的 IK rot6D只能叫 retarget pseudo-label。

禁止的旧处理：把 HML `4:136` 写成 Pulp-normalized mean且没有 availability mask，再从 HML objective排除该块。这把 unknown伪装成 observed mean pose。

正式裁决：

- mixed HML+Pulp checkpoint invalid for Stage2/cache/promotion。
- immutable artifacts与 root/local decoded diagnostics保留，不删除、不改写。
- Pulp-only checkpoint不受该训练伪观测污染，但只保留为 architecture control；尚未晋升替代 C3。

可行修复：优先回到 HumanML/AMASS source SMPL-family axis-angle/matrix，统一 body model、joint hierarchy/order、rest pose、坐标、root-yaw factorization，并在 SO(3) 上做20→30 fps插值；必须以 FK/SMPL round-trip、逐关节 geodesic和分布审计闭合。若 source pose不可得，则使用显式 availability mask、独立 root/local encoder或 geometry auxiliary，不得 mean fill full-Human input。

4090 MotionStreamer272只读完整性审计：

- split唯一 ID `28,764`；实际可读 arrays `26,846`；缺 `1,918`。
- 现有 arrays均 finite `[T,272]`，但下载目录没有与 source-pose builder闭合的逐文件 provenance。
- 相邻 `MotionPatches-main/scripts/build_humanml3d_272_self.py` 证明可从 HumanML source `pose_data` axis-angle构造22-joint rotations；这是候选路线，不是当前数据已获准使用的证明。

#### 5.2 视觉结论

- Stage2核心：ViMoGen-light CLIP显著胜出。
- Stage1核心：redesign Pulp-only是 redesign两臂的视觉胜者；相对 C3-25 Stage1未见明显视觉质量恶化，并展示更强的 Human-first independent-control观感。不要把 fixed-8偏好改写成全面 canonical metric胜出。
- C3-25 与 redesign Pulp-only在若干 fixed sample的最后一帧都有明显 Camera jump，导致 owning-camera projection骤变。这是待量化 terminal-boundary failure，不能直接归因于 redesign。
- HML OOD diagnostic：Pulp-only已能 zero-shot重建若干 in-domain HML动作，HML+Pulp root/local更好；二者都随时间出现整人异常旋转。HML visualizer不读取 decoded rot6D，所以直接可见责任通道是累计 root/yaw；mean-imputation只能作为未证实的 shared-encoder/domain-cue间接机制。

#### 5.3 为什么 ViMoGen-light CLIP 更适配

已有代码证据支持的组合解释：

1. full temporal self-attention让每个 Human latent frame直接访问全序列，更适合累计 root/heading与动作phase一致性。
2. 每层使用完整 CLIP token sequence cross-attention，而 C3把 pooled Camera/Human CLIP embedding经 MLP合成全局 condition；token-to-token接口更适合动作、方向、节奏与顺序。
3. shifted continuous flow直接学习 dense continuous Human latent的 velocity field；相对 MARDM mask-fill与 C3 `START_X` diffusion更匹配是合理假设，但尚未单变量证明。
4. E6是 Human-only specialist，不承受 Camera/joint exposure与梯度竞争；这可能贡献了相当部分收益。
5. CLIP胜过同 topology/objective/sampler的 UMT5说明 condition geometry与 motion/action数据对齐比文本编码器规模更关键，但仍是 single-seed system结果。

必须做的 matched attribution顺序：固定 C3 Human128、CLIP token cache、ordered IDs、owning decoder、预算与参数量级，分别只切换 pooled→token condition、U-Net→Transformer、diffusion→flow、Unified→Human-only exposure。未完成前只称 system-task fit。

### 6. 当前 Gradio 与 visual artifacts

Stage2 six-way bundle：

`/data/public/ripemangobox/Motion/StoryMotion/runs/vis/stage2/human_stage2_sixway_fixed8_r1_seed17_4090g1_20260726`

manifest SHA256：

`a6206cf7184ec768ab3eccb0251ad69772e54c4a324094e4128dcfede7ac403d`

Stage1 C3/redesign/HML bundle：

`/data/public/ripemangobox/Motion/StoryMotion/runs/vis/stage1/stage1_c3_hanchor_gradio_fixed8_r1_seed17_4090g0_20260727/`

bundle manifest / asset builder / merged Gradio SHA256：

`39f649a2d074f1bffab607d70fbaf54d087263164498e898cadcfb7f7b7404fe` / `d996e04c5f5eed45fa65d35ced2e2261dd416e85e5f4005579ef0c6c629146c0` / `ad7f275348397b80dd44bb327681ca55329a01c2f529820eb4e4ef7761a6a50c`

统一 app tabs：

- `Human · Six-way 105K`：GT、Stage1 recon、C3-25、MARDM、ViMoGen CLIP、ViMoGen UMT5。
- `Stage1 · Pulp four-way`：GT、C3-25、redesign Pulp-only、redesign HML+Pulp。
- `Stage1 · HML root/local`：HML reference、redesign Pulp-only、redesign HML+Pulp。
- 各 tab均有统一播放按钮；不要覆盖现有 bundle或改写 manifest。

### 7. 下一位 agent 的推荐执行顺序

#### 7.1 先审计下方架构草稿，不启动 optimizer

下方 raw LaTeX提出 `Protected-H Dual-Stream ViMoGen`，核心方向与当前证据一致，但包含一个尚未授权的前提：**直接在 redesign Stage1 上重新训练 Human teacher并进入三模式。** 当前只有 C3-25获正式 promotion；Pulp-only redesign只是 architecture control，mixed明确 invalid。

先把 proposal拆成：

1. 已由代码/metric/visual支持的事实。
2. 可执行但未验证的 architecture hypothesis。
3. 必须先闭合的 Stage1 gate。
4. 需要用户明确授权的新 optimizer run。

默认推荐：第一版 protected dual-stream Stage2继续固定 C3-25 representation/decoder/cache，避免同时更换 Stage1与Stage2；只有 redesign Pulp-only通过独立 Stage1 gate后，才为它重建 cache并从零重训 Human teacher。若要偏离该顺序，必须明确指出 multi-axis confound并请用户选择。

#### 7.2 Stage1 前置 gate

1. 用现有 fixed samples建立新的 read-only terminal Camera probe root，不重采样：比较最后一步与倒数第二步的 Camera center displacement、rotation geodesic、projection delta，并按 GT、模型与 `length mod 4` 分组；做 last-frame hold/clamp replay定位 Camera14 endpoint或 ConvTranspose/crop boundary。
2. 对 Pulp-only redesign做固定 H 改 C、固定 C 改 H、latent swap与 cross-Jacobian/invariance matrix；证明的目标是 Human path insulation与Camera text controllability，不是双向独立。
3. HML修复是独立 representation axis：先补齐 source pose/272 provenance与数据完整性，再构建新 adapter、manifest、round-trip audit；禁止复用 mixed checkpoint。
4. 只有新的 Stage1 candidate通过完整 Pulp Human、Camera、projective、physical、visual gate，才能生成新的 Stage2 cache；C3 mainline不回写。

#### 7.3 Stage2 protected dual-stream MVP

第一版采用 strict triangular coupling：

$$
H\rightarrow C,\qquad C\nrightarrow H
$$

- Human stream使用已验证 ViMoGen-light CLIP path；Direct-H route中 Camera tokens/module必须不存在，而不是全零占位。
- Camera stream拥有独立 input projection、normalization、self-attention、Camera-text cross-attention、output head与flow state。
- Direct-C读取 observed/GT Human latent + Camera text；joint读取 evolving predicted-clean Human context。
- Camera loss对 Human teacher stop-gradient；Human context使用 predicted-clean estimate并可加随time增强的 trust gate。
- 同一 checkpoint显式实现 `Direct-H`、`Direct-C`、`joint parallel`；mode routing不得改变 Direct-H计算图。
- Camera text、Human context、relation context分别做 condition dropout，防止 GT-H shortcut吞掉 Camera text。
- MVP先不打开 C/R→H residual。只有 strict triangular通过后，才测试 zero-init、低秩、子空间受限的 bounded Human residual。

#### 7.4 必须预注册的关键 gates

- **Direct-H exact regression：** 固定 text/noise/sampler/precision/CFG，teacher与unified Direct-H输出只能有浮点误差。
- **Direct-H canonical gate：** 完整 Human semantic/distribution/global/root/yaw/physical fields。
- **Direct-C gate：** 完整 Camera semantic/coverage/framing/trajectory/rotation与 observed-H projective geometry。
- **joint parallel gate：** 同 checkpoint完整 Human、Camera、Human–Camera projective geometry；不得用cascade或observed-H completion替代。
- **Camera intervention：** 固定 Human motion，仅改变 Camera text；Camera显著变化，strict triangular Human保持不变。
- **terminal Camera gate：** 末帧跳变不能在新的 Stage1/Stage2 candidate中静默保留。
- visual/blind cohort与canonical cohort必须记录 ordered IDs、hash、sampler、decoder和sample count。

### 8. 禁止事项与 claim boundary

- 禁止把 HML mean-imputed mixed checkpoint投入 Stage2。
- 禁止把 RIC263 IK rot6D称为 Pulp/TRAM同源观测。
- 禁止把 Pulp-only fixed-8视觉胜出称为全面 Stage1 metric胜出。
- 禁止把 ViMoGen CLIP称为 Camera/joint system、已解决 Human physical blocker或 pure-backbone upper-bound证明。
- 禁止将 Human/Camera latent直接拼接进单一共享 input/output head后用零模态模拟三模式，除非它只作为明确失败风险 control且另立 contract。
- 禁止用 loss下降、TensorBoard曲线或 latent objective数值判断生成质量。
- 禁止把 observed-Human Camera completion与joint parallel混表。
- 禁止在 dirty worktree pull/rebase/reset/checkout覆盖、全目录 rsync或无选择 commit。
- 禁止覆盖/删除/重用旧 run、checkpoint、records、fixed samples、hash、失败日志或 visual bundle。

### 9. 文档 owner 与最终交付

- 当前 mainline、短决策、active blocker：[[ideas/StoryMotion/current]]。
- 正式数值、artifact/checkpoint/record hashes与不可比边界：[[ideas/StoryMotion/StoryMotion-valid-metric-ledger]]。
- evaluator schema、decoded semantics与I/O：[[ideas/StoryMotion/StoryMotion-metric-computation-io]]。
- version事件、完成 milestone、bug/invalidation provenance：[[ideas/StoryMotion/version_family]]。
- architecture causal reasoning与可迁移经验：[[ideas/StoryMotion/StoryMotion_Checkmate]]。
- H-anchor matched contract与closed invalidation：[[ideas/StoryMotion/2026-07-27_storymotion-stage1-human-anchor-residual-control]]。
- 本页只作接力与草稿，不复制新的正式 metric table。

下一轮至少交付：

1. 对下方 architecture proposal 的 evidence/hypothesis/risk审计结果。
2. 一份最小 matched experiment ladder及逐臂唯一变量、预算、stop/go gate。
3. Stage1 terminal Camera probe方案；若执行，使用新 eval root并登记 contract/manifest/SHA256。
4. HML common-source rot6D adapter的可行性与 blocker；禁止猜测填值。
5. protected dual-stream三模式的代码接口、cache/decoder owner与 non-causal assertions。
6. 完整 canonical Human/Camera/joint evaluator映射与 visual plan。
7. 所有 StoryMotion Markdown post-audit、Markdown table检查、`git diff --check` 与远端 branch/HEAD/status。

## 原始架构草稿（非授权参考附录）

> [!warning] 使用边界
> 下列 LaTeX是会话中形成的详细 architecture proposal，尚未完成 matched-variable、Stage1 promotion、run contract和预算授权。下一位 agent可以抽取其中的 protected Human、independent Camera、predicted-clean context、strict triangular与 bounded residual思想，但不得按 Phase 0–4 直接启动训练。

```latex
\section{三模式 ViMoGen-light 应该如何适配}

首先需要明确：不应将 human latent 与 camera latent 直接拼接后，对同一个 ViMoGen backbone 进行全模型联合微调。

最危险的实现方式是
\[
\operatorname{concat}\!\left(
    [\zh,\zc]
\right)
\longrightarrow
\text{single motion embedding}
\longrightarrow
\text{single ViMoGen backbone}
\longrightarrow
\text{single output head},
\]
再通过全零输入或 branch mask 实现 direct-H、direct-C 和 joint 三种模式。

这种实现会重新制造 redesign Stage-1 试图解决的耦合问题：

\begin{itemize}
    \item camera loss 会持续改写 human self-attention 和 human motion prior；
    \item camera text 会污染已经验证有效的 human text--motion 对齐；
    \item direct-C 中的 GT human condition 可能形成 shortcut，使 camera branch 忽略 camera text；
    \item joint mode 的梯度可能导致 human marginal distribution 退化；
    \item direct-H 也必须经过其训练时并不需要的 camera pathway，从而造成结构性分布偏移；
    \item human 与 camera 的数值尺度、频率特征和语义空间不同，共享输入输出映射会引入额外的表示冲突。
\end{itemize}

因此，三模式模型应遵循以下设计原则：
\[
\boxed{
\text{protected human prior}
+
\text{camera-specific flow}
+
\text{bounded relation coupling}
}
\]

\section{推荐架构：Protected-H Dual-Stream ViMoGen}

\subsection{Human stream：受保护的 human foundation prior}

首先基于 redesign Stage-1 单独训练一个新的 human-only ViMoGen-light：
\[
\vh
=
\fH\!\left(
    \xh,t,\Th
\right),
\]
其中 $\fH$ 表示已经完成 human-only 训练并通过验证的 teacher checkpoint。

该模型是后续三模式系统中的 human teacher 和 foundation prior。为了从结构上保护 direct-H 能力，必须满足以下规则：

\begin{itemize}
    \item direct-H 调用时，使用与 human teacher 完全相同的 forward path；
    \item camera tokens 在 direct-H 路由中应当不存在，而不是使用全零 camera tensor；
    \item camera text 不进入 human cross-attention；
    \item camera modules 不参与 human self-attention、normalization 和 FFN；
    \item human input projection、transformer blocks、normalization 和 output head 均保持独立；
    \item 在严格保护阶段，human stream 参数完全冻结。
\end{itemize}

因此，在 direct-H 模式下应满足
\[
f_{H}^{\mathrm{unified}}
\!\left(
    \xh,t,\Th,m=H
\right)
\equiv
\fH\!\left(
    \xh,t,\Th
\right),
\]
其中
\[
m\in\{H,\ C{\mid}H,\ HC\}
\]
是显式的 mode tag。

这里的保护不是通过额外 loss ``鼓励''模型保持 human 能力，而是通过完全相同的计算图保证 direct-H 不受 camera branch 干扰。

\subsection{Camera stream：独立的 camera-specific vector field}

camera 使用独立的条件流：
\[
\vc
=
\fC\!\left(
    \xc,
    t,
    \Tc,
    \CH,
    \CR
\right),
\]
其中：

\begin{itemize}
    \item $\Tc$ 表示 camera text condition；
    \item $\CH$ 表示由 human motion 提供的条件上下文；
    \item $\CR$ 表示 framing、relative geometry 或其他 human--camera relation context。
\end{itemize}

camera stream 应具有独立的：

\begin{itemize}
    \item input projection；
    \item timestep modulation；
    \item normalization；
    \item self-attention blocks；
    \item text cross-attention；
    \item output projection 和 output head。
\end{itemize}

human motion 与 camera trajectory 的数值范围、动态频率和语义结构存在显著差异，因此不应共享同一个输入投影或输出头。

\subsection{Human-to-camera 应使用 predicted clean human}

采用如下 rectified-flow 参数化：
\[
\xh
=
(1-t)\epsh+t\zh,
\qquad
t\in[0,1],
\]
其中 $t=0$ 对应纯噪声，$t=1$ 对应 clean data，速度监督为
\[
\bm v_{h}^{\mathrm{target}}
=
\zh-\epsh.
\]

human teacher 输出
\[
\vh
=
\fH\!\left(
    \xh,t,\Th
\right).
\]

由
\[
\xh=(1-t)\epsh+t\zh
\]
和
\[
\bm v_h=\zh-\epsh
\]
可得到 clean human latent 的单步估计：
\[
\widehat{\zh}_{\mathrm{clean}}
=
\xh+(1-t)\vh.
\]

camera stream 应读取
\[
\CH
=
\EHC\!\left(
    \sg\!\left[
        \widehat{\zh}_{\mathrm{clean}}
    \right]
\right),
\]
而不是直接读取 noisy human state $\xh$。

如果 camera 在训练和采样过程中直接依赖 $\xh$，那么在 $t$ 较小时，它看到的主要是：

\begin{itemize}
    \item 高噪声 root translation；
    \item 高噪声 heading；
    \item 不确定的动作 phase；
    \item 不稳定的身体尺度和局部姿态；
    \item 与最终 human trajectory 偏差较大的临时状态。
\end{itemize}

这会使 camera branch 学到对 noisy/generated human 极度敏感的脆弱耦合。

可以进一步加入 timestep-dependent trust gate：
\[
g_H(t)
=
\sigma(at+b),
\qquad a>0,
\]
或者
\[
g_H(t)=t^{\gamma},
\qquad \gamma>0.
\]

joint mode 中的 human context 定义为
\[
\CH^{\mathrm{joint}}
=
g_H(t)\,
\EHC\!\left(
    \sg\!\left[
        \widehat{\zh}_{\mathrm{clean}}
    \right]
\right).
\]

由于本参数化中较小的 $t$ 对应更高噪声，$g_H(t)$ 应当随 $t$ 增大而增强：

\begin{itemize}
    \item 高噪声阶段少信任 human prediction；
    \item 随着 human latent 逐渐清晰，再增强 framing 和 interaction condition；
    \item direct-C 输入 GT/observed human 时，直接令 $g_H=1$。
\end{itemize}

需要注意，$\sg[\cdot]$ 只阻断 camera loss 向 human teacher 的反向传播，不阻止 human prediction 随采样状态变化。

\section{三种模式的显式路由}

\begin{table}[htbp]
    \centering
    \renewcommand{\arraystretch}{1.35}
    \begin{tabularx}{\textwidth}{
        >{\centering\arraybackslash}p{2.2cm}
        >{\raggedright\arraybackslash}p{3.0cm}
        >{\raggedright\arraybackslash}X
        >{\raggedright\arraybackslash}X
    }
        \toprule
        模式
        & 需要生成
        & 条件
        & Human path
        \\
        \midrule
        direct-H
        & $\zh$
        & $\Th$
        & 使用原始 teacher path；camera stream 完全 bypass
        \\
        direct-C
        & $\zc$，以及可选 relation
        & $\zh^{\mathrm{obs/GT}},\Tc$
        & human 只作为 frozen condition；对 human context 使用 stop-gradient
        \\
        joint
        & $\zh,\zc$，以及可选 relation
        & $\Th,\Tc$
        & human teacher 生成 human；camera 读取 evolving predicted-clean human
        \\
        \bottomrule
    \end{tabularx}
\end{table}

严格保护版本的 joint vector field 为
\[
\frac{\mathrm d}{\mathrm dt}
\begin{bmatrix}
    \bm x_{h,t}\\[2pt]
    \bm x_{c,t}
\end{bmatrix}
=
\begin{bmatrix}
    \fH\!\left(
        \bm x_{h,t},t,\Th
    \right)
    \\[4pt]
    \fC\!\left(
        \bm x_{c,t},
        t,
        \Tc,
        \EHC\!\left(
            \sg[
                \widehat{\zh}_{\mathrm{clean}}
            ]
        \right),
        \CR
    \right)
\end{bmatrix}.
\]

这是一个 block-triangular coupled flow：
\[
H\longrightarrow C,
\qquad
C\nrightarrow H.
\]

因此，严格保护模型满足
\[
p_{\mathrm{joint}}
\!\left(
    H\mid \Th,\Tc
\right)
=
p_{\mathrm{teacher}}
\!\left(
    H\mid \Th
\right).
\]

从模型结构上看，camera text、camera noise 和 camera loss 均不可能改变 human generation。

\section{严格三角结构的论文风险}

严格三角结构对应如下条件分解：
\[
p(H,C\mid \Th,\Tc)
=
p_H(H\mid\Th)\,
p_C(C\mid H,\Tc).
\]

审稿人可能据此提出：

\begin{quote}
该方法是否只是先生成 human，再条件生成 camera 的 sequential pipeline，而非真正的 joint generation？
\end{quote}

这一质疑具有合理性。因此，应当区分 MVP 模型和最终论文模型。

\subsection{MVP：strict protected triangular flow}

MVP 阶段的目标是：

\begin{itemize}
    \item 快速验证 direct-H、direct-C 和 joint 三种模式；
    \item 保证 direct-H 和 joint-H 不退化；
    \item 验证 ViMoGen-light 是否适合作为 camera flow backbone；
    \item 建立可靠的 camera specialist 和严格保护实验上界；
    \item 排除数据清洗和额外数据增强带来的混杂因素。
\end{itemize}

\subsection{论文模型：protected base 加 bounded relation residual}

在 frozen human teacher 之外增加一个零初始化的 joint residual：
\[
\bm v_{h}^{\mathrm{joint}}
=
\fH\!\left(
    \xh,t,\Th
\right)
+
\alpha(t)\,
\Delta_H\!\left(
    \xh,
    \xc,
    t,
    \Th,
    \Tc,
    \CR
\right).
\]

其中应满足：

\begin{itemize}
    \item $\Delta_H$ 是低秩 adapter、LoRA 或其他参数受限模块；
    \item $\Delta_H$ 的 output projection 使用 zero initialization；
    \item $\Delta_H$ 只在 joint mode 中激活；
    \item direct-H 永远 bypass $\Delta_H$；
    \item $\alpha(t)$ 有界，例如
    \[
    0\leq \alpha(t)\leq \alpha_{\max},
    \qquad
    \alpha_{\max}\ll 1;
    \]
    \item residual 仅作用于 framing-relevant human subspace，而不是重写完整 body semantics。
\end{itemize}

更严格地，可以引入子空间投影 $P_{\mathrm{rel}}$：
\[
\bm v_{h}^{\mathrm{joint}}
=
\fH\!\left(
    \xh,t,\Th
\right)
+
\alpha(t)\,
P_{\mathrm{rel}}
\Delta_H\!\left(
    \xh,\xc,t,\Th,\Tc,\CR
\right).
\]

$P_{\mathrm{rel}}$ 可以约束 residual 只影响：

\begin{itemize}
    \item root translation；
    \item global heading；
    \item coarse timing 或动作 phase；
    \item 与镜头构图直接相关的低频姿态分量。
\end{itemize}

camera vector field 仍然为
\[
\bm v_{c}^{\mathrm{joint}}
=
\fC\!\left(
    \xc,
    t,
    \Tc,
    \widehat{\zh}_{\mathrm{clean}},
    \CR
\right).
\]

由此得到 near-triangular coupling：
\[
H\longrightarrow C
\quad\text{为强耦合},
\qquad
(C,R)\longrightarrow H
\quad\text{为弱且有界的耦合}.
\]

这种设计允许有限的真实 joint interaction，例如：

\begin{itemize}
    \item 为保持 medium shot，human root trajectory 发生小幅调整；
    \item 为完成 orbit shot，human heading 与 camera orbit direction 协调；
    \item 为维持构图，动作 timing 或 movement amplitude 发生有限变化；
    \item 在不改变动作语义的情况下优化 human--camera relative geometry。
\end{itemize}

但它不会允许 camera branch 任意重写已经验证有效的 human motion prior。

\section{如何利用 redesign Stage-1 的 flexible coupling}

redesign Stage-1 最重要的作用，是为 human、camera 和 relation 提供可分离但可组合的 latent representation。

理想情况下，可以将 Stage-1 latent 表示为
\[
\zh^{\mathrm{base}},
\qquad
\zc^{\mathrm{base}},
\qquad
\bm r_{hc},
\]
其中 $\bm r_{hc}$ 表示 human--camera relation 或 coupling representation。

最终参与解码的 latent 可表示为
\[
\widetilde{\zh}
=
\zh^{\mathrm{base}}
+
A_h(\bm r_{hc}),
\]
\[
\widetilde{\zc}
=
\zc^{\mathrm{base}}
+
A_c(\bm r_{hc}).
\]

为保护 human prior，应当满足
\[
\norm{
    A_h(\bm r_{hc})
}
\ll
\norm{
    \zh^{\mathrm{base}}
},
\]
而 $A_c(\bm r_{hc})$ 可以具有更强的作用，因为 camera trajectory 本身就高度依赖 human framing。

对应的三种模式为
\[
\text{direct-H}:
\qquad
\Th
\longrightarrow
\zh^{\mathrm{base}},
\]
\[
\text{direct-C}:
\qquad
\zh^{\mathrm{obs}}+\Tc
\longrightarrow
\zc^{\mathrm{base}},\bm r_{hc},
\]
\[
\text{joint}:
\qquad
\Th+\Tc
\longrightarrow
\zh^{\mathrm{base}},
\zc^{\mathrm{base}},
\bm r_{hc}.
\]

如果 redesign Stage-1 中的 coupling 只是确定性的 relation bridge：
\[
\bm r_{hc}
=
\Rhc(\zh,\zc),
\]
则不必将 $\bm r_{hc}$ 建模为第三个独立 diffusion/flow stream。此时可以将其用于：

\begin{itemize}
    \item auxiliary relation loss；
    \item sampling guidance；
    \item framing consistency constraint；
    \item camera condition encoder 的中间表示。
\end{itemize}

如果 coupling 是具有独立随机性的 residual latent，则应将其放入 camera/relation stream：
\[
(\zc,\bm r_{hc})
\sim
p_C(\zc,\bm r_{hc}\mid H,\Tc),
\]
而不应让 direct-H 依赖该 residual latent。

\section{具体 Transformer 结构}

推荐使用 dual-stream blocks，而不是在 token、feature 或 channel 维度直接拼接。

\begin{verbatim}
Human tokens H_t
    |-- Human self-attention
    |-- Human-text cross-attention
    |-- Human FFN
    `-- Frozen/protected human teacher path

Camera tokens C_t
    |-- Camera self-attention
    |-- Camera-text cross-attention
    |-- H-to-C cross-attention
    |-- Relation/framing adapter
    |-- Camera FFN
    `-- Independent camera head
\end{verbatim}

joint mode 中推荐的 attention topology 如下：

\begin{table}[htbp]
    \centering
    \renewcommand{\arraystretch}{1.3}
    \begin{tabular}{c|ccc}
        \toprule
        Query $\backslash$ Key
        & Human
        & Camera
        & Relation
        \\
        \midrule
        Human
        & $\checkmark$
        & $\times$
        & 可选弱连接
        \\
        Camera
        & $\checkmark$
        & $\checkmark$
        & $\checkmark$
        \\
        Relation
        & $\checkmark$
        & $\checkmark$
        & $\checkmark$
        \\
        \bottomrule
    \end{tabular}
\end{table}

初始模型中不应让
\[
H\leftrightarrow C
\]
在所有层进行完全对称的双向交互。

更稳妥的初始化策略为：

\begin{itemize}
    \item human blocks：从 direct-H checkpoint 完整加载；
    \item human input projection、normalization 和 head：从 direct-H checkpoint 加载并冻结；
    \item camera blocks：可以复制 human blocks 作为初始化，但后续使用独立参数；
    \item H-to-C cross-attention：output projection 使用 zero initialization；
    \item C-to-H relation adapter：zero initialization，第一轮训练不开启；
    \item camera input projection 和 camera output head：重新初始化；
    \item human text projection 与 camera text projection：使用独立参数；
    \item mode embedding：只用于路由或调制对应分支，不得使 direct-H 经过 camera 模块。
\end{itemize}

如果 redesigned Stage-1 改变了 human latent 的维度、尺度或统计分布，则应：

\begin{itemize}
    \item 保留 ViMoGen 中间 transformer blocks；
    \item 重新初始化 human input projection 和 output head；
    \item 在 redesign Stage-1 latent 上重新训练 direct-H；
    \item 先确认 direct-H 重新收敛，再构建三模式模型；
    \item 不应假设基于旧 Stage-1 的 Stage-2 checkpoint 可以无缝迁移。
\end{itemize}

\section{基于原始 Pulp 的训练顺序}

当前阶段忽略数据清洗和 HumanML3D 增强是合理的，因为目标是完成架构归因和三模式机制验证，避免将数据收益与方法收益混在一起。

\subsection{Phase 0：建立 redesign Stage-1 上的 human teacher}

训练任务为
\[
\Th
\longrightarrow
\zh.
\]

具体要求：

\begin{itemize}
    \item 使用与已验证旧 Stage-1 实验相同的 ViMoGen-light CLIP 配置；
    \item 冻结 redesign Stage-1 encoder 和 decoder；
    \item 建立 direct-H 的定量指标、可视化结果和随机种子基线；
    \item 确认 redesign latent 上仍然保留 ViMoGen-light 的 human generation 优势；
    \item 将该 checkpoint 固定为后续实验的 protected anchor。
\end{itemize}

在该阶段，human rectified-flow loss 为
\[
\mathcal{L}_{\mathrm{RF}}^{h}
=
\mathbb{E}
\left[
    \norm{
        \fH(\xh,t,\Th)
        -
        (\zh-\epsh)
    }_2^2
\right].
\]

\subsection{Phase 1：训练 direct-C specialist}

冻结全部 human stream，训练
\[
\zh^{\mathrm{GT}}+\Tc
\longrightarrow
\zc.
\]

只更新：

\begin{itemize}
    \item camera input embedding；
    \item camera transformer blocks；
    \item camera normalization 和 output head；
    \item H-to-C adapter；
    \item relation/framing module。
\end{itemize}

human context 定义为
\[
\CH^{\mathrm{direct-C}}
=
\EHC\!\left(
    \sg[
        \zh^{\mathrm{GT}}
    ]
\right).
\]

同时应对 camera text 进行独立的 condition dropout，防止 camera branch 仅通过 GT human root、heading 或 trajectory 建立 shortcut，而忽略 $\Tc$。

direct-C 阶段的 camera flow 为
\[
\xc
=
(1-t)\epsc+t\zc,
\]
\[
\bm v_{c}^{\mathrm{target}}
=
\zc-\epsc,
\]
\[
\mathcal{L}_{\mathrm{RF}}^{c}
=
\mathbb{E}
\left[
    \norm{
        \fC(
            \xc,t,\Tc,\CH,\CR
        )
        -
        (\zc-\epsc)
    }_2^2
\right].
\]

\subsection{Phase 2：加入 joint triangular training}

训练数据同时构造
\[
\xh=(1-t)\epsh+t\zh,
\]
\[
\xc=(1-t)\epsc+t\zc.
\]

首先由 frozen human teacher 得到
\[
\vh
=
\fH(\xh,t,\Th),
\]
\[
\widehat{\zh}_{\mathrm{clean}}
=
\xh+(1-t)\vh.
\]

随后训练 camera：
\[
\vc
=
\fC\!\left(
    \xc,
    t,
    \Tc,
    g_H(t)\,
    \EHC\!\left(
        \sg[
            \widehat{\zh}_{\mathrm{clean}}
        ]
    \right),
    \CR
\right).
\]

这一阶段仅更新 camera 和 relation modules。

这样，camera 在训练阶段看到的是：

\begin{itemize}
    \item 不同 timestep 下的 predicted human；
    \item 具有真实 teacher prediction error 的 human condition；
    \item 与 joint inference 一致的 evolving human-condition distribution；
    \item 而不是始终完美的 GT human latent。
\end{itemize}

为了进一步减小 train--test gap，可以混合使用 GT human 和 predicted human：
\[
\widetilde{\zh}_{\mathrm{cond}}
=
\begin{cases}
\zh^{\mathrm{GT}},
& \text{概率 }p_{\mathrm{GT}},\\
\widehat{\zh}_{\mathrm{clean}},
& \text{概率 }1-p_{\mathrm{GT}}.
\end{cases}
\]

训练初期可以使用较高的 $p_{\mathrm{GT}}$，随后逐渐衰减，但最终应保证 camera 主要在 predicted-human condition 下训练。

\subsection{Phase 3：统一三模式}

初始 batch 比例可以设为
\[
\text{direct-H}:
\text{direct-C}:
\text{joint}
=
2:2:1.
\]

此时 human stream 仍然冻结，因此 direct-H batch 的主要作用是：

\begin{itemize}
    \item regression test；
    \item 数值一致性监控；
    \item 检查统一 checkpoint 的 direct-H route 是否发生意外变化；
    \item 检查 mode router、normalization 和 condition cache 是否引入副作用。
\end{itemize}

如果 direct-H batch 不产生任何可训练参数的梯度，则不应将其重复计入总训练 loss，只需将其作为周期性验证任务。

模型稳定后，数据采样比例可以调整为
\[
1:1:1.
\]

三种模式必须使用显式 mode tag：
\[
m\in
\left\{
    H,\,
    C{\mid}H,\,
    HC
\right\}.
\]

缺失模态应当通过计算图路由和 attention topology 表示，而不是通过全零 tensor 伪装成存在的模态。

\subsection{Phase 4：可选 bounded bidirectional coupling}

只有在 strict triangular 模型已经稳定收敛后，才打开
\[
\Delta_H(C,R).
\]

推荐配置为：

\begin{itemize}
    \item 只将 relation adapter 放入最后三分之一的 transformer blocks；
    \item 使用 LoRA、低秩 adapter 或小型 residual MLP；
    \item 使用 zero initialization；
    \item human backbone 保持冻结，或使用远低于 camera branch 的学习率；
    \item 若解冻 human backbone，其学习率建议为 camera branch 的
    \[
    0.02\sim0.1
    \]
    倍；
    \item 对 residual output 进行 norm clipping；
    \item 使用强 teacher distillation 和 decoded-motion preservation。
\end{itemize}

vector-field preservation loss 为
\[
\mathcal{L}_{\mathrm{pres}}
=
\mathbb{E}
\left[
    \norm{
        \bm v_{h}^{\mathrm{joint}}
        -
        \sg\!\left[
            \fH(\xh,t,\Th)
        \right]
    }_2^2
\right].
\]

joint human 的 clean-latent estimate 为
\[
\widehat{\zh}_{\mathrm{clean}}^{\mathrm{joint}}
=
\xh
+
(1-t)\bm v_{h}^{\mathrm{joint}},
\]
teacher clean-latent estimate 为
\[
\widehat{\zh}_{\mathrm{clean}}^{\mathrm{teacher}}
=
\xh
+
(1-t)\fH(\xh,t,\Th).
\]

decoded preservation loss 可以写为
\[
\mathcal{L}_{\mathrm{decoded\text{-}pres}}
=
\mathbb{E}
\left[
    d_h\!\left(
        \Dh(
            \widehat{\zh}_{\mathrm{clean}}^{\mathrm{joint}}
        ),
        \Dh(
            \sg[
                \widehat{\zh}_{\mathrm{clean}}^{\mathrm{teacher}}
            ]
        )
    \right)
\right],
\]
其中 $d_h$ 可以由以下部分组成：
\[
d_h
=
\lambda_{\mathrm{pose}}d_{\mathrm{pose}}
+
\lambda_{\mathrm{root}}d_{\mathrm{root}}
+
\lambda_{\mathrm{vel}}d_{\mathrm{vel}}
+
\lambda_{\mathrm{contact}}d_{\mathrm{contact}}.
\]

如果 relation adapter 没有显著改善 framing、camera alignment 或 joint interaction，应删除该模块。严格三角模型虽然交互能力较弱，但更加简单、可靠且容易证明 human non-degradation。

\section{损失函数建议}

完整训练目标可以写为
\[
\mathcal{L}
=
\lambda_h\mathcal{L}_{\mathrm{RF}}^{h}
+
\lambda_c\mathcal{L}_{\mathrm{RF}}^{c}
+
\lambda_r\mathcal{L}_{\mathrm{relation}}
+
\lambda_f\mathcal{L}_{\mathrm{framing}}
+
\lambda_p\mathcal{L}_{\mathrm{pres}}
+
\lambda_d\mathcal{L}_{\mathrm{decoded\text{-}pres}}.
\]

其中
\[
\mathcal{L}_{\mathrm{RF}}^{h}
=
\mathbb{E}
\left[
    \norm{
        \vh-(\zh-\epsh)
    }_2^2
\right],
\]
\[
\mathcal{L}_{\mathrm{RF}}^{c}
=
\mathbb{E}
\left[
    \norm{
        \vc-(\zc-\epsc)
    }_2^2
\right].
\]

camera clean-latent estimate 为
\[
\widehat{\zc}_{\mathrm{clean}}
=
\xc+(1-t)\vc.
\]

如果 Stage-1 提供确定性的 relation bridge
\[
\bm r_{hc}
=
\Rhc(\zh,\zc),
\]
则可以在 predicted clean latents 上定义
\[
\mathcal{L}_{\mathrm{relation}}
=
\mathbb{E}
\left[
    \norm{
        \Rhc\!\left(
            \widehat{\zh}_{\mathrm{clean}},
            \widehat{\zc}_{\mathrm{clean}}
        \right)
        -
        \bm r_{hc}
    }_1
\right].
\]

framing loss 可以定义为
\[
\mathcal{L}_{\mathrm{framing}}
=
\mathbb{E}
\left[
    d_f\!\left(
        \Pi\!\left[
            \Dh(
                \widehat{\zh}_{\mathrm{clean}}
            ),
            \Dc(
                \widehat{\zc}_{\mathrm{clean}}
            )
        \right],
        \bm y_{\mathrm{frame}}
    \right)
\right],
\]
其中 $\Pi[\cdot]$ 表示将解码后的 human 和 camera 投影到图像平面，$\bm y_{\mathrm{frame}}$ 表示 GT framing target，例如：

\begin{itemize}
    \item subject screen-space center；
    \item subject projected scale；
    \item head room；
    \item camera--human relative azimuth；
    \item camera distance；
    \item visibility 和 out-of-frame penalty。
\end{itemize}

不建议在训练初期、所有高噪声 timestep 上频繁解码完整 SMPL 和 camera trajectory。更稳妥的顺序是：

\begin{enumerate}
    \item 先使用 latent relation loss；
    \item 模型稳定后，加入低频计算的 decoded projection loss；
    \item 对 decoded loss 使用 timestep weighting；
    \item 主要在中低噪声区域计算 framing supervision。
\end{enumerate}

例如：
\[
w_f(t)
=
\mathbb{I}[t\geq t_{\min}]
\cdot
t^{\eta},
\]
\[
\mathcal{L}_{\mathrm{framing}}
=
\mathbb{E}
\left[
    w_f(t)\,
    d_f(\cdot)
\right].
\]

在 Phase 1--3 中，如果 human stream 完全冻结，可以令
\[
\lambda_h=\lambda_p=\lambda_d=0,
\]
只优化 camera 和 relation 相关损失。只有在 Phase 4 打开 bounded human residual 后，才需要启用 preservation losses。

\section{Classifier-Free Guidance 应按模态拆分}

不应只使用单一的统一 guidance scale。至少需要区分：

\[
s_h:
\text{human text guidance},
\]
\[
s_c:
\text{camera text guidance},
\]
\[
s_r:
\text{human--camera relation guidance}.
\]

human branch 的 CFG 只处理 human text：
\[
\bm v_h^{\mathrm{cfg}}
=
\bm v_h(\varnothing)
+
s_h
\left[
    \bm v_h(\Th)
    -
    \bm v_h(\varnothing)
\right].
\]

camera branch 应分别对以下 condition 执行独立 dropout：

\begin{itemize}
    \item camera text $\Tc$；
    \item human context $\CH$；
    \item relation context $\CR$。
\end{itemize}

可以将 camera guidance 写成分解形式：
\begin{align}
\bm v_c^{\mathrm{cfg}}
={}&
\bm v_c(\varnothing,\varnothing,\varnothing)
\\
&+
s_c
\left[
    \bm v_c(\Tc,\varnothing,\varnothing)
    -
    \bm v_c(\varnothing,\varnothing,\varnothing)
\right]
\\
&+
s_H
\left[
    \bm v_c(\varnothing,\CH,\varnothing)
    -
    \bm v_c(\varnothing,\varnothing,\varnothing)
\right]
\\
&+
s_r
\left[
    \bm v_c(\varnothing,\varnothing,\CR)
    -
    \bm v_c(\varnothing,\varnothing,\varnothing)
\right],
\end{align}
其中 $s_H$ 表示 human-condition guidance。

实际实现中也可以使用联合条件分支，但必须保证训练时确实出现过对应的 condition-dropout 组合，否则推理时无法稳定地独立控制各 guidance component。

如果 camera text 从不单独 dropout，camera branch 很容易完全依赖 GT human trajectory；如果 human context 从不 dropout，camera text 对 trajectory 的可控性通常会显著下降。

必须进行固定 human 的反事实实验：

\begin{center}
\begin{tabular}{l}
same human motion $H$ + ``slow dolly in''\\
same human motion $H$ + ``orbit clockwise''\\
same human motion $H$ + ``static close-up''\\
same human motion $H$ + ``track from behind''
\end{tabular}
\end{center}

期望结果是：

\begin{itemize}
    \item camera trajectory 随 camera text 显著变化；
    \item human motion 在 strict triangular 模型中保持完全不变；
    \item framing 和 visibility 仍然合理；
    \item camera text 与 human context 都对输出具有不可替代的贡献。
\end{itemize}

这是 StoryMotion 最直观的 controllability 和 application demonstration 之一。

\section{如何证明没有损害 Human 能力}

不能只报告 unified model 的 human FID 与 teacher ``看起来差不多''。至少需要完成以下三层验证。

\subsection{Direct-H exact regression}

固定以下所有因素：

\begin{itemize}
    \item human text；
    \item initial noise；
    \item sampler；
    \item sampling step 数；
    \item CFG scale；
    \item numerical precision；
    \item random seed。
\end{itemize}

比较 human teacher 和 unified model 的输出：
\[
\widehat{\zh}^{\mathrm{teacher}}
\quad\text{vs.}\quad
\widehat{\zh}^{\mathrm{unified},\,m=H}.
\]

严格 protected route 应满足
\[
\max_i
\left|
    \widehat z_i^{\mathrm{teacher}}
    -
    \widehat z_i^{\mathrm{unified},\,m=H}
\right|
\leq
\varepsilon_{\mathrm{fp}},
\]
其中 $\varepsilon_{\mathrm{fp}}$ 只来自浮点误差。

如果两者差异明显，则说明 mode router、normalization、condition cache、dropout、mixed precision 或共享参数仍然污染了 direct-H path。

\subsection{Joint-H non-inferiority}

比较
\[
H_{\mathrm{direct}}
\quad\text{和}\quad
H_{\mathrm{joint}}.
\]

应至少报告：

\begin{itemize}
    \item FID 或对应 motion-distribution metric；
    \item TMR/R-Precision 或 text--motion alignment；
    \item diversity 和 multimodality；
    \item foot skating、penetration、velocity、acceleration 等 physical metrics；
    \item root translation 和 heading statistics；
    \item visual preference；
    \item bootstrap confidence interval。
\end{itemize}

严格 triangular 模型中，应有
\[
H_{\mathrm{joint}}
\equiv
H_{\mathrm{direct}}
\]
或仅存在数值误差。

对于 bounded residual 模型，不应只进行传统显著性检验，而应预先设定 non-inferiority margin $\delta$，检验
\[
M(H_{\mathrm{joint}})
-
M(H_{\mathrm{direct}})
\geq
-\delta
\]
是否成立，其中 $M$ 表示越大越好的 human metric。

对于越小越好的指标，则应检验
\[
M(H_{\mathrm{joint}})
-
M(H_{\mathrm{direct}})
\leq
\delta.
\]

\subsection{Camera intervention sensitivity}

固定 human text、human initial noise 和其他采样条件，仅改变 camera text：
\[
\Tc^{(1)},\Tc^{(2)},\ldots,\Tc^{(K)}.
\]

应验证：

\begin{itemize}
    \item camera trajectory 随 $\Tc$ 发生显著且符合语义的变化；
    \item strict triangular 模型中的 human output 完全不变；
    \item bounded residual 模型中的 human semantic identity 和动作类型保持稳定；
    \item human 的变化只集中于 root、heading、timing 或其他 framing-relevant dimensions；
    \item human physical quality 不因 camera intervention 显著下降。
\end{itemize}

可以定义 human intervention sensitivity：
\[
S_H
=
\frac{1}{K(K-1)}
\sum_{i\neq j}
d_H\!\left(
    H^{(i)},H^{(j)}
\right),
\]
以及 camera intervention sensitivity：
\[
S_C
=
\frac{1}{K(K-1)}
\sum_{i\neq j}
d_C\!\left(
    C^{(i)},C^{(j)}
\right).
\]

strict triangular 模型的理想结果为
\[
S_H\approx 0,
\qquad
S_C\gg 0.
\]

bounded residual 模型则应满足
\[
S_H^{\mathrm{semantic}}\approx 0,
\]
同时允许
\[
S_H^{\mathrm{root/timing}}>0,
\]
但该变化必须与 framing improvement 显著相关。

\section{最终推荐路线}

完整实验路线应按照以下顺序推进：

\begin{enumerate}
    \item 在 redesign Stage-1 上重新训练并确认 human-only ViMoGen-light teacher；
    \item 冻结 human teacher，建立 direct-C specialist；
    \item 使用 predicted-clean human condition 训练 strict triangular joint model；
    \item 通过 exact regression 证明 direct-H 计算路径没有变化；
    \item 通过 joint-H non-inferiority 和 camera intervention sensitivity 验证三模式；
    \item 在严格三角模型稳定后，再尝试 zero-init、低秩、子空间受限的 C/R-to-H residual；
    \item 只有当 bounded residual 显著改善 framing 或 joint interaction，且通过 human preservation test 时，才将其保留为最终论文模型。
\end{enumerate}

因此，推荐的核心模型不是
\[
\operatorname{concat}(H,C)
\longrightarrow
\text{shared backbone},
\]
而是
\[
\boxed{
\begin{aligned}
\bm v_h
&=
\fH(\bm x_{h,t},t,\Th)
+
\underbrace{
    \alpha(t)P_{\mathrm{rel}}\Delta_H(\cdot)
}_{\text{仅在最终 joint 模型中可选}},
\\
\bm v_c
&=
\fC\!\left(
    \bm x_{c,t},
    t,
    \Tc,
    g_H(t)\EHC(
        \sg[
            \widehat{\zh}_{\mathrm{clean}}
        ]
    ),
    \CR
\right).
\end{aligned}
}
\]

其基本原则可以概括为：
\[
\boxed{
\text{Human prior 必须被结构性保护；}
\quad
\text{Camera 可以强依赖 Human；}
\quad
\text{Camera 对 Human 的反向影响必须弱、有界且可验证。}
}
\]

```
