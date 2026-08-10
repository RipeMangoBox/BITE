---
title: "StoryMotion Codebase Deconstruction"
aliases:
  - StoryMotion Code Map
tags:
  - StoryMotion
  - codebase
  - architecture
  - contracts
  - status/maintained
created: "2026-08-10T15:00:00+08:00"
updated: "2026-08-10T15:00:00+08:00"
status: maintained
source_host: "4090"
source_root: "/data/public/ripemangobox/Motion/StoryMotion"
source_branch: "agent/c1rel-stage2-ablation-20260804"
source_commit: "31e9df5b225208184f29a5b16d0c3c24561394fc"
mirror_root: "linkedCodebases/StoryMotion"
core_manifest_files: 89
core_manifest_bytes: 1062402
---

# StoryMotion codebase deconstruction

> [!important] 这是一份代码与合同地图，不是指标账本
> 本页解释 StoryMotion 的数据接口、表示、训练边界、采样、评测和代码调用关系。
> 不复制正式数值表、不替代运行日志，也不重新解释一次实验结果。正式数字和 artifact
> hash 只看 [[StoryMotion-valid-metric-ledger]]；指标定义和 I/O 只看
> [[StoryMotion-metric-computation-io]]；当前论文选择只看 [[current]]。

## 1. 阅读入口与可复现边界

本机阅读镜像位于 linkedCodebases/StoryMotion/，对应 4090 上
/data/public/ripemangobox/Motion/StoryMotion 的 Git HEAD。该镜像在 BITE 仓库中是
ignored development mirror，不应提交。同步只包含本页末尾 manifest 的 89 个源文件：
v9 Stage1 owner、C0 fixed-H Stage2、protected-H shared evaluator/contract、HT fresh、
C1REL representation/control、invariants、experiment contract 及其最小依赖。

没有复制：

- runs/、checkpoints、datasets、caches、logs、rendered media、venv；
- 任何完整仓库快照或实验 artifact；
- 任何会改变运行 provenance 的文件。

所有 manifest 文件在同步后均与 4090 HEAD 的 SHA256 一致；manifest 记录的是源码
快照而不是运行结果。仓库固定提交为
31e9df5b225208184f29a5b16d0c3c24561394fc，因此未改名代码链接可固定到同一提交。三组
`sm_` source namespace位于受审计commit `0cf5f91`，已推送到GitHub：

- [v9 Pulp-only Stage1 owner](https://github.com/RipeMangoBox/StoryMotion/blob/31e9df5b225208184f29a5b16d0c3c24561394fc/experiments/stage1_human_anchor_residual_pulp_only_r3/train.py)
- [Stage1 representation model](https://github.com/RipeMangoBox/StoryMotion/blob/31e9df5b225208184f29a5b16d0c3c24561394fc/experiments/stage1_human_anchor_residual/model.py)
- [C0 fixed-H model](https://github.com/RipeMangoBox/StoryMotion/blob/31e9df5b225208184f29a5b16d0c3c24561394fc/experiments/stage2_v11_fixed_h_camera/model.py)
- [C0 fixed-H training loop](https://github.com/RipeMangoBox/StoryMotion/blob/31e9df5b225208184f29a5b16d0c3c24561394fc/experiments/stage2_v11_fixed_h_camera/train.py)
- [protected-H shared evaluator](https://github.com/RipeMangoBox/StoryMotion/blob/31e9df5b225208184f29a5b16d0c3c24561394fc/experiments/stage2_protected_h_vimogen/evaluate.py)
- [C1REL geometry](https://github.com/RipeMangoBox/StoryMotion/blob/0cf5f9165e688f16b56a0d53b48ff15a0a1e8f0b/experiments/stage1_sm_representation_controls/geometry.py)
- [experiment contract](https://github.com/RipeMangoBox/StoryMotion/blob/31e9df5b225208184f29a5b16d0c3c24561394fc/docs/experiment-contract.md)

## 2. 研究问题：三个接口必须同时成立

StoryMotion 研究的是 capability-preserving 的非因果 asymmetric Human–Camera generation：

1. Human text 生成 Human motion；
2. Camera text 在给定 observed/generated Human 条件下生成 Camera；
3. Human、Camera 和共同 decoder 的 pair interface 能重建、投影并支持三种推理模式。

这里的核心不是把 Camera trajectory 当成 Human trajectory 的 anchor，而是保留原 Human
motion-generation capability，再把 Camera 生成分解为 fixed-H conditional branch。Camera
应能在 Direct-C 的真实 Human 和 sequential 的生成 Human 上使用同一条路径；因此
“Human-preserving”是方法边界，编辑能力不是当前第二主贡献。

[[analysis/arxiv_2026/Auteur_Language-Driven_Cinematographic_Framing_for_Human-Centric_Video_Generation|Auteur]] 的任务层核心差异是：Auteur 用 human trajectory 为 ViGen
锚定 camera trajectory；StoryMotion 关注 Human generation capability-preserving 的
Human–Camera generation。两者不能仅按“都有 Human 和 Camera”归为同一问题。

MotionRemix 只作为未来数据构造的参考：从独立有效的 Human–Camera 轨迹组合、hard/soft
边界处理和重编码，制作新的组合式 H–C pair。它不是“对 Human 做上下半身增广”，不改变
StoryMotion mainline，也不自动证明任意 Human、Camera、text 的自由替换成立。

## 3. 数据、表示与 mask

### 3.1 Stage1 的官方 pair

storymotion/training/joint_data.py 定义的 official contract 是
pulpmotion_official_normalized_human199_joint_camera14：

- Human 是 199 维，使用 Pulp train split 的统计；Camera 是 14 维；
- Camera14 由 FOV、human-relative distance、6D rotation、world-camera translation
  velocity 组成；第一帧 velocity 置零；
- Human 与 Camera 以 sample_id 配对，先按真实长度裁成共同有效长度，再在 batch 内 padding；
- projection/framing target 是由同一对 decoded Human + Camera 计算的 4 维 screen-center、
  log-scale、out-of-frame 几何字段，不是独立监督源；
- 所有 padding 都有 valid mask，不能进入 loss、normalization、metric 或 trajectory
  aggregation。

HumanML3D mixed branch 在早期 Stage1 wrapper 中保留，是历史探索和 anchor control；它不等于
v9 Pulp-only owner，也不能用来声称 Pulp 数据清洗或 Human capability 结论。

### 3.2 latent layout 与 H199/C14

v9 owner 的 Stage1 latent 固定为：

- H128：Human latent；
- I16：interaction latent，由 paired Human + Camera 产生；
- C48：Camera latent；
- 合计 192 维，decoder 输出 Human199、Camera14 和 framing4。

这里 H199/C14 是数据/decoder feature space，H128/I16/C48 是 latent space，不能互换
命名。C1REL-C48 仍是 48 维 Camera latent，但它的输入 Camera14 已改为
first-camera-frame-relative representation。

### 3.3 normalization 与 cache identity

统计只从 train split 估计；eval/test 只能复用 train statistics。Stage1 cache 与 Stage2
cache 都必须记录 latent order、feature dimensions、valid-length/mask policy、sample IDs、
normalization source/hash、decoder identity 和 is_causal=false。protected-H 分支还可以
在 z-score 后做 branch-local full-covariance whitening（Cholesky/ridge），但这不改变
source cache 的身份。

cache 的数值相同不够：ordered IDs、manifest、stats、checkpoint、owning decoder 和 code
commit 都是合同的一部分。任何 one-off cache、不同 padding 或错误 split 都必须形成新 run
identity。

## 4. Stage1：非因果表示与重建 owner

> [!important] 核心环节：v9 Pulp-only Stage1 owner
> 这是 C0-LAT 与 C0-GEO 共同且冻结的 representation/decoder/cache owner：
> non-causal Human199 + Camera14，latent layout 为 H128 + I16 + C48，配套 train-only
> statistics、owning decoder 和 Human 105K teacher。后续 Camera objective 不能绕过或
> 偷换这条 Stage1 support boundary。

### 4.1 架构与 D_h / D_c / D_f coupling

[Stage1 model](https://github.com/RipeMangoBox/StoryMotion/blob/31e9df5b225208184f29a5b16d0c3c24561394fc/experiments/stage1_human_anchor_residual/model.py)
使用 non-causal temporal blocks，并在构造、加载、训练和评测边界拒绝 causal tokenizer。

- Human encoder 输出 z_h ∈ H128；
- interaction encoder 输出 z_hc ∈ I16，其输入是 paired Human + Camera；
- Camera encoder 输出 z_c ∈ C48；
- D_h(z_h) 只解码 Human199；
- D_c([z_h, z_hc, z_c]) 解码 Camera14；
- D_f([z_h, z_hc, z_c]) 解码 framing4。

因此 Camera 和 framing 的 reconstruction support 依赖 H、interaction、Camera 三路。
这正是“保留 Human 同时生成 Camera”的接口基础，也是后续组合式 H–C pair 不能只在
Stage2 随意拼接的原因：decoder/interaction 已经在 Stage1 定义了 support。

encode_joint 返回 H/I/C；decode_joint 通过共同 latent layout 恢复三类输出。Human-only
forward 可以不提供 Camera，但 pair reconstruction、Camera generation 和 framing 都要
遵守成对的数据合同。

### 4.2 三阶段训练与 loss

基础 owner 训练分成三个角色清晰的 phase：

- Phase A：Human-only anchor。Human reconstruction 使用 full/root-local SmoothL1，
  temporal difference、很小的 integrated-yaw 与 root 项；
- Phase B：冻结 Human encoder/decoder，训练 Camera、framing、interaction 路径。Camera
  有 SmoothL1 与 temporal loss；framing 有小权重的 SmoothL1；interaction 有很小的
  energy regularizer；
- Phase C：joint reconstruction；Human 学习率是 Camera/interaction 路径的 0.1 倍，
  防止 Camera 支路破坏已获得的 Human prior。

base schedule 是 210K / 210K / 216K（合计 636K）的三 phase owner contract。v9
Pulp-only wrapper 将选定 owner 固定到 Pulp pair 和 Pulp Human anchor；旧 HML branch 的
名字不能被解读为当前 v9 数据来源。wrapper 调用链是：

~~~text
stage1_human_anchor_residual_pulp_only_r3/train.py
  -> stage1_human_anchor_residual_pulp_only_r2/train.py
  -> stage1_human_anchor_residual_pulp_only/train.py
  -> stage1_human_anchor_residual/train.py
  -> stage1_human_anchor_residual/{data,model,audit_normalization}.py
~~~

### 4.3 Stage1 contract 与 causal boundary

Stage1 contract 保存 phase exposure/checkpoint、train/eval IDs、normalization audit、
model/decoder files and hashes、no-optimizer gate 和 is_causal=false。固定 legacy
representation settings 的唯一代码 owner 是
storymotion/experiment_invariants.py；不要在 run script 中手填相同字段。

> [!warning] causal tokenizer 禁止
> StoryMotion Stage1/Stage2 的 constructors、checkpoint/cache loading、training、evaluation
> 必须断言 is_causal is False。唯一例外是仓库外、独立 owning contract 的 native
> MotionStreamer baseline；它不能创建、消费或 gate StoryMotion cache、Unified checkpoint
> 或 representation control。

## 5. C1REL：表示控制与 Stage1 support audit

C1REL 把 Camera14 的 world-relative geometric sequence 变为相对第一 camera frame 的
T_C1^-1 T_Ct：

- camera center 以第一帧 center 为原点并旋到第一帧 W2C frame；
- rotation 使用 first W2C 与 world C2W 的组合；
- velocity 用 finite difference；
- FOV 保留为 native feature；center/velocity 使用 train-only mean/std；
- invalid frames 继续由 mask 排除。

C1REL 的 Stage1 variants 包含 full H128+I16+C1REL-C48、去 I16 的
H128+C1REL-C48，以及 no-interaction/HREL sibling controls。I16 是否存在是 representation
factorization control，不是对 Human 做 upper/lower-body augmentation。

其 Stage1 decoder 的 Camera/framing support、C1REL stats、cache order 和 caption identity
必须一起冻结。当前 C1REL Stage2 代码是 raw-caption T0 的 diagnostic-only branch：
先 fresh Human teacher，再 frozen-H LAT Camera；canonical caption freeze 后如需正式 promotion
必须重新建立合同并训练，不能把 raw-T0 运行当成 mainline evidence。

> [!important] C1REL 的决策顺序
> 先做 Stage1 support audit（C1REL transform 的有效长度、mask、native Camera14
> reconstruction、owning decoder 输出与 framing support）；若 support 通过，优先冻结 H
> 通路，只做 pair-side Camera/adapter finetune；若 support 不通过，Stage2 无法补出
> 缺失的 Camera decoder support，应以新 run ID 从 Stage1 全量 retrain。两条路径都必须
> 保留旧合同和 hash，不能 patch/resume 一个已被判 invalid 的 run。

## 6. Stage2：frozen Human、Camera-only LAT 与 controls

### 6.1 protected-H shared infrastructure

experiments/stage2_protected_h_vimogen/ 是 shared evaluator/contract infrastructure
和历史诊断实现：

- H stream 是 non-causal Human flow；Camera stream 以 Camera text 和 Human context
  条件化；
- C|H loss 使用 clean、detached H；旧 HC diagnostic route 可使用 noisy H 与
  one-step predicted-clean H，但必须按其合同解释；
- freeze_human、generate_human、generate_camera 和旧 generate_joint 仍在代码中；
- four-term CFG 与 joint-parallel 只属于历史 protected-H diagnostic。v11 不能因此重新
  训练或评估 evolving-H parallel。

它提供参数 disjointness、gradient-isolation、decoder output、determinism 和 intervention
检查，是“protected H”概念的可读入口，不是 v11 mainline objective 的替代定义。

### 6.2 v11 C0-LAT mainline

> [!important] 核心环节：Camera-only fixed-H LAT
> v11 Stage2 的 Camera-side target 是 Camera64 = I16 + C48；H128 是冻结的 Human
> conditioning context，不是 Camera Stage2 optimizer target。Camera-only 表示只更新
> Camera branch，不能理解成去掉 interaction latent 或重新训练 Human。

C0-LAT 的 invariant 是 exact v9 Pulp-only Stage1 owner、owning decoder/cache/stats 和
frozen Human 105K teacher。Stage2 只优化 Camera branch：

1. build_v11_model 从 v9 Human 105K checkpoint 装载 Human/Camera，检查 non-causal 和
   exact endpoint；
2. Human 参数、Human text path 和 Stage1 decoder 均冻结；
3. batch route 在 GT-H 与 teacher-final-H 之间按 contract 组织，source ID embedding 区分
   两种 context；
4. Camera flow 只接受 Camera text + fixed Human latent，dropout/trust settings 由 contract
   固定；
5. loss 是 masked Camera flow MSE；invalid latent frames 不贡献；
6. sampling 使用一个 fully conditional Camera velocity 的 shifted-sigma explicit-Euler
   path，按 valid mask 清理尾部。

C0-LAT 的 formal system modes 是 Direct-H、Direct-C、sequential Human-then-Camera；
Direct-C 读取 observed/GT H，sequential 先生成 Human，再把最终 Human 固定给 Camera。
Human 不在 Camera backward 中更新；所有 H/decoder gradient guard 都是 hard gate。

### 6.3 C0-GEO objective boundary

C0-GEO 与 C0-LAT 共享 Stage1、Human teacher、data/cache 和训练边界，只把 Camera objective
扩展为 frozen owning decoder 的 decoded Camera14 reconstruction、temporal、以及 framing
auxiliary。lambda_geo 由 calibration 产生，Stage1 decoder 与 Human 不接收 optimizer
gradient。它是 audited objective alternate/control，不是第二个 mainline，也不能从不同
endpoint 拼一个“最好结果”。

### 6.4 HT fresh mechanism control

HT fresh 是完整 Camera branch 加 Human-text fusion 的机制 control：

- reference 是已审计 C0-GEO endpoint；
- Human、Stage1 decoder 与 factual Human path 冻结；
- Camera base 与 HT module 训练，合同固定 matching / cyclic shuffle / zero Human text；
- HT0、HT、HTS、HTZ 是机制诊断模式；
- pure4053 fresh audit 已完成，保留为 mechanism control/no promotion。

HT 的额外 Human text 只能作为 optional Stage2 injection control；不能据此修改 C0-LAT
“Camera-only conditional on fixed H”的主定义。

## 7. 采样与三模式 evaluator

| mode | input | generated output | claim boundary |
| --- | --- | --- | --- |
| Direct-H | Human text | Human199 | 保留 Human generation capability |
| Direct-C | observed/GT Human + Camera text | Camera14 + framing | Camera conditional branch |
| sequential | Human text → generated Human, then Camera text + fixed generated H | Human199 + Camera14 + framing | asymmetric sequential generation |
| joint_parallel | evolving H and C together | historical protected-H diagnostic | v11 forbidden unless separately authorized |

三模式必须共用 ordered IDs、true-length mask、decoder/cache/checkpoint identity 和
non-causal assertions。sampler 应记录 seed、step count、schedule、CFG/source IDs、eval
batch and sample order；不能用 first-128 smoke 或旧 joint-parallel 结果冒充 pure4053
formal.

### 7.1 evaluator 与指标语义

evaluator 的职责分层如下：

- storymotion/per_sample_quality.py：保留逐样本 Human/Camera/physical/framing quality
  的结构化输出；
- scripts/storymotion_official_bridge_smoke.py：检查官方 evaluator bridge 的输入输出
  与 callback contract；
- Stage2 evaluate_pure4053.py：验证 ordered IDs、sample count、decoder/cache/stats/
  teacher hashes，解码 true-length sequence 后调用官方 semantic、distribution、retrieval
  指标；
- paired geometry 包括 root-aligned/global Human position/trajectory、Camera center、
  rotation/yaw 等；physical diagnostics 包括 bone stability、speed/acceleration/jerk、
  contact/skate heuristic；framing 是 screen/projective diagnostics；
- 结果必须按 task/mode/representation/version/run 绑定。H199 root alignment 去掉 root
  translation 但不去掉 heading，不能把它简写为 local-pose error。

本页只说明语义，不给正式数值。数值与 uncertainty 只链接
[[StoryMotion-valid-metric-ledger]]，定义和 I/O 只链接 [[StoryMotion-metric-computation-io]]。

## 8. Contract、hash 与 non-causal fail-closed

docs/experiment-contract.md 是合同入口。一个可审计 run 至少固定：

- exact Stage1 checkpoint 和 owning decoder hash；
- train/eval cache、manifest、ordered sample IDs、split/count、valid-mask policy；
- train-only normalization source/hash、latent order、dimensions；
- seed、train/eval batch size、sampler、objective、source route、mode labels；
- model/config/code commit、host/GPU/device、checkpoint/EMA/scheduler/scaler/RNG/sampler
  state；
- stage boundary、optimizer exposure、halfway checkpoint and reload verification。

所有 constructors、cache/checkpoint loaders、train/eval preflight 必须 fail closed on
is_causal != false。joint_parallel 不是 v11 gate。任何 hash/ID/decoder/config mismatch
应新建 run ID；不能手工修 manifest，也不能继续一个已经判断为 invalid 的 run。

对于明确采用 matched Pulp/native 210K contract（total optimizer steps 210K、halfway
boundary 105K）的 Stage2 长训，合同要求在准确的 105K optimizer boundary 原子保存
immutable full-state checkpoint 并 reload-verify；其他 Stage2 run 不因本段自动继承
105K 边界，必须服从自己的显式合同。heartbeat 需同时记录 global step、epoch、exposures、
throughput、ETA、data-wait/H2D/compute/checkpoint timing、GPU utilization、memory；只有当
data-wait 明确占主导且 GPU idle 时，才可以把瓶颈归因于 IO。配置错、进度停滞或缺少合同
要求的 halfway checkpoint 时，保留旧 run 作为 invalid provenance，另建 run 从 step zero
重训。

## 9. 代码调用图

~~~text
Stage1 Pulp owner
  r3/train.py
    -> r2/train.py
      -> pulp_only/train.py
        -> base train.py
          -> data.py + packed_data.py + model.py
            -> exact Stage1 checkpoint / decoder / stats contract

C0 fixed-H LAT/GEO
  make_shared_contract.py -> make_run_contract.py -> preflight.py
    -> build_teacher_final_cache.py + data.py
      -> model.py (frozen H, Camera-only objective)
        -> train.py (GT-H / teacher-final route)
          -> evaluate_pure4053.py / audit_pure4053.py
            -> official bridge + per_sample_quality

protected-H shared diagnostics
  make_contract.py / make_eval_contract.py -> preflight.py
    -> data.py + model.py -> runner.py -> evaluate.py
      -> intervention / sequential / historical joint diagnostic

HT fresh control
  make_contract.py -> preflight.py -> model.py
    -> train.py / runtime.py -> evaluate_pure4053.py -> audit_pure4053.py

C1REL representation/control
  geometry.py + build_c1rel_stats.py -> model.py + run.py
    -> stage2_sm_c1rel/make_contract.py -> preflight.py
      -> frozen-H Camera diagnostic -> formal evaluator
~~~

Pinned source anchors for this graph are listed in Section 1 and in the manifest below.
The global fixed settings are read from storymotion/experiment_invariants.py, not duplicated
by individual run scripts.

## 10. Mainline、controls 与 closed exploration map

| code family / axis | status | interpretation |
| --- | --- | --- |
| v9 Pulp-only Stage1 owner | retained shared owner | C0-LAT and C0-GEO exact common representation/decoder/cache |
| v11 C0-LAT | mainline | operational default; frozen-H Camera-only LAT |
| v11 C0-GEO | audited alternate/control | same owner and endpoint boundary; GEO objective only |
| HT fresh | retained mechanism control | pure4053 completed; no promotion to mainline |
| C1REL full / C1REL without I16 | diagnostic representation controls | Stage1 support and factorization evidence; raw-T0 Stage2 diagnostic-only |
| protected-H Vimogen | shared historical diagnostic | evaluator/contract/gradient isolation; old joint route not v11 |
| v8.1C C3-25 | former-mainline system baseline | historical system boundary, not a single-variable control |
| stage1_human_relative_camera_v10 | closed/retired | v10 closure decision; no corrected endpoint or Stage2 continuation |
| stage2_human_relative_camera_v10 | closed/retired | v10 closure decision; historical name only |
| stage2_v11_camera_inpainting | hard-stop/diagnostic-only | Camera temporal editing failure axis closed |
| framing_control pure4053 | closed/diagnostic-only | no promotion to C0 mainline |
| MotionRemix-style pair construction | future support experiment | combinatorial H-C pair data only; separate contract and claim |

Version event rationale and immutable run names belong to [[version_family]]; current priority and
claim scope belong to [[current]]; formal reliability gates belong to
[[StoryMotion-iclr-reliability]].

## 11. 常见 debug 定位

| symptom | first inspect | likely boundary |
| --- | --- | --- |
| import or path error | mirror root, package path, exact script wrapper | never silently fall back to another repository |
| cache/sample-ID mismatch | Stage2 data loader, manifest, ordered IDs, source cache metadata | rebuild as a new cache/run; do not edit provenance |
| wrong output scale or drift | train-only stats, denormalization, decoder hash, true-length mask | normalization and owning decoder are one contract |
| latent shape/order error | H128/I16/C48, C1REL order, mask ceil-length | reject before train/eval |
| Human changes during Camera training | build_v11_model, optimizer parameter groups, gradient guards | Human and Stage1 decoder must remain frozen |
| causal flag or temporal leakage | tokenizer base and all preflight assertions | is_causal must be false |
| Direct-C differs from sequential unexpectedly | GT-H vs teacher-final-H route, source IDs, same Camera checkpoint | compare only matched route contracts |
| only first prefix passes | evaluator sample_count, ordered IDs, first-128 smoke settings | prefix is diagnostic, not pure4053 formal |
| HT has no effect | HT fusion activation and gradient guard on first steps | HT control must prove active/nonzero module before training |
| C1REL camera is unstable | first-frame transform, finite-difference velocity, train-only stats, native decoder reconstruction | Stage1 support audit precedes Stage2 promotion |
| reported IO bottleneck | heartbeat data-wait/H2D/compute/checkpoint time plus GPU utilization | call it IO only when measured data-wait dominates while GPU is idle |
| missing half-way checkpoint | run contract and atomic save/reload verification at 105K | invalidate run and retrain from zero with new ID |

For code-level inspection, start with the path named in the first-inspect column, then follow the
call graph. Do not delete or overwrite runs while debugging; immutable provenance is more useful
than a cleaner directory.

## 12. 编辑能力的最小、安全闭环

StoryMotion 现在解决的是 “generated Human remains usable as Camera condition”，不是任意
H/C/text swap。要增加可用的组合能力，建议的 causal sequence 是：

1. **Stage1 support audit**：对 MotionRemix-style composite pair 检查 C1REL/Camera14
   reconstruction、factual projection/framing、valid masks、decoder round-trip、Interaction16
   recomputation，以及 Human output是否仍由同一 H owner 支持；
2. **先做 pair-side finetune**：若 support 通过，冻结 H encoder/decoder 和已审计 H teacher，
   只让 Camera/pair-side adapter 在版本化 composite pairs 上学习。独立 Camera program
   必须针对目标 H_mix retarget/re-solve，重新计算 Camera14、projection/framing，并重算
   pair-dependent Interaction16 与 C48；不能保留失效的 C_A 或旧 latent；
3. **full Stage1 retrain if needed**：若 Camera native transform、D_c/D_f 或 interaction
   support 不通过，则新增 Stage1 contract，从 step zero 全量 retrain；Stage2 不能凭空创建
   Stage1 没有覆盖的 Camera support。

每一步都要保留原始 pair、组合规则、Human/Camera parent IDs、Camera retarget/re-solve
配置、reason code 和新 cache/hash，并用 many-to-many manifest 管理组合边。composition-
disjoint eval 必须按 Human、Camera program 和组合边拆分，避免同一 donor pair 或其旧
latent 泄漏到 eval。编辑 stress test 只有在存在 paired target 时才报告 paired metrics；
无 target 的自由替换只做 unpaired probe，不升级为第二主贡献。这样保持研究聚焦在
human-preserving sequential generation，同时给出可验证的有限 compositional utility。

## 13. 进一步阅读

- 当前 StoryMotion 状态：[[current]]
- 版本与关闭决定：[[version_family]]
- ICLR reliability / QA：[[StoryMotion-iclr-reliability]]
- 正式 metric ledger：[[StoryMotion-valid-metric-ledger]]
- metric definitions and I/O：[[StoryMotion-metric-computation-io]]
- Paper boundary and shared repository policy：[[paper-boundary]]
- C1REL historical diagnostic：[[archived/diagnostics/2026-07-28_storymotion-v9-protected-h-three-stage-implementation-camera-diagnosis]]
- contract source：linkedCodebases/StoryMotion/docs/experiment-contract.md

## 14. Core source manifest

The following is the exact file-level manifest copied for this deconstruction note. Every file
is relative to linkedCodebases/StoryMotion/; every SHA256 was measured against 4090 HEAD
31e9df5b225208184f29a5b16d0c3c24561394fc. `synced to 4090 HEAD` means the local mirror content
hash equals the audited 4090 source hash；它不表示复制了run artifact或checkpoint。表内
`stage1_sm_*`／`stage2_sm_*`路径按rename commit `0cf5f91`解析；rename未改变这些文件的
content hash；rename branch已推送，尚待review／merge。

| relative source path | SHA256 | status |
| --- | --- | --- |
| experiments/stage1_human_anchor_residual_pulp_only_r3/train.py | 8588e7b55692708d33a1ab78d819e55682c275039fae15ac28be84b0f6df0f83 | synced to 4090 HEAD |
| experiments/stage1_human_anchor_residual_pulp_only_r2/train.py | ee1b2719deb47f0cb8d361e86aa5302905e203c3b46bf18298efa8250c1fa175 | synced to 4090 HEAD |
| experiments/stage1_human_anchor_residual_pulp_only/train.py | 70556ff9e4997bca04e1a8ef213f7565f34fce75ff40b7823294b97a46608a5e | synced to 4090 HEAD |
| experiments/stage1_human_anchor_residual/audit_normalization.py | c4b67b91f3287be252615a9901ecd8844adcc944aaff806f90695a802613d3a8 | synced to 4090 HEAD |
| experiments/stage1_human_anchor_residual/data.py | e5948ba2d7f7d776fa308c93e4863e50d7ab7c3c5b7fd4e575a05ec95a20bed9 | synced to 4090 HEAD |
| experiments/stage1_human_anchor_residual/decisions/stage1_hanchor_pulp_vs_hml_gate_r3_true_length_20260727.json | 27eedeeca48a207fca03359c969505b82b777584154ad5646a79dfc0f56a1e36 | synced to 4090 HEAD |
| experiments/stage1_human_anchor_residual/model.py | 87d8d58d59b2506909627ec5bf2f39659ad8512765850f5bb614d5b9bf0cefd3 | synced to 4090 HEAD |
| experiments/stage1_human_anchor_residual/train.py | 9eb537195d39756cd2e5c7364d80e96e83c713ea8e2ed7685872e30a91694f1b | synced to 4090 HEAD |
| experiments/stage1_human_anchor_residual_packedio/packed_data.py | 4c0ad561f1506947291d72b3e3b62c0043dce0c0394194ae32da0c4acf945e69 | synced to 4090 HEAD |
| experiments/stage1_independent_conditional_camera/geometry.py | 16e100dee1437e7acecc2bd6c33cc021818e74c6aad02c2c97031151871d16aa | synced to 4090 HEAD |
| experiments/stage1_sm_representation_controls/__init__.py | f9d196fd06b5593c044b431c7d239e7e0b2036b19a9d48612436998af33833c7 | synced to 4090 HEAD |
| experiments/stage1_sm_representation_controls/build_c1rel_stats.py | bb0151368dc6f2969ac55fcd666a236396a763c8ea553acf1517fa2cbfdff66e | synced to 4090 HEAD |
| experiments/stage1_sm_representation_controls/compare_formal.py | c577b1d81d00200cdc24964994c15e7c1a62c53f49a43bf2dbbdfbc273c83e95 | synced to 4090 HEAD |
| experiments/stage1_sm_representation_controls/evaluate_formal.py | cd4a4054129813182a95debc10a4d7958cf7f1d405177336e1d46b6173530218 | synced to 4090 HEAD |
| experiments/stage1_sm_representation_controls/geometry.py | dc9dad6ef14b1e11571a21012911ef8d93a3b16bc83fa53cd478aa21151955d2 | synced to 4090 HEAD |
| experiments/stage1_sm_representation_controls/model.py | aa4b5e51736c495964f17d42dd6761a8e3f36e5398e79cc500d04117fe320152 | synced to 4090 HEAD |
| experiments/stage1_sm_representation_controls/run.py | 141fb9229b0b95cc5e8fbd42000a255244628e6587cc31092ea6313dc708eb05 | synced to 4090 HEAD |
| experiments/stage1_sm_representation_controls/test_compare_formal.py | b5843e4a550eb1ba850aa95173095f597e7c758dbc03213b67e17215fe7fe272 | synced to 4090 HEAD |
| experiments/stage1_sm_representation_controls/test_evaluate_formal.py | 443e152164b55d4c99a71169aa6487329a2b8a34819c5776905b0d79b417853a | synced to 4090 HEAD |
| experiments/stage1_sm_representation_controls/test_model.py | 037c4d47e574aa0223cd0c10710403a0cd9f08a8e0f36b2feb97e794ac93775a | synced to 4090 HEAD |
| experiments/stage2_v11_fixed_h_camera/__init__.py | be371d026026afe391d808b2bb4f8751c6e44e74610e736ec5d5167e0996bbf3 | synced to 4090 HEAD |
| experiments/stage2_v11_fixed_h_camera/audit_confirmation.py | a1ea4e3086dafeec6366cd0cbd39e8cd31981cd15cb34d12d504c518f677ad07 | synced to 4090 HEAD |
| experiments/stage2_v11_fixed_h_camera/audit_pure4053.py | 858bcdb4148d0efcf96beefd5a54b93bf33d8f3f1bf06b730a48b5a32e7f121d | synced to 4090 HEAD |
| experiments/stage2_v11_fixed_h_camera/audit_seed_repeat.py | 846a5b4d19f76697d58a22fdd8dd300cbd1f9b18cb27427a84e61da93414e05f | synced to 4090 HEAD |
| experiments/stage2_v11_fixed_h_camera/audit_v9_30k_comparator.py | c36bb3d5aa4c5046899d8af471c88b0c25d70185d64252fcc85aceb1274264ba | synced to 4090 HEAD |
| experiments/stage2_v11_fixed_h_camera/build_geo_targets.py | 2383926e54a56a5eed282c67631ec4449a55ae9e915db14321a557608f0d520f | synced to 4090 HEAD |
| experiments/stage2_v11_fixed_h_camera/build_teacher_final_cache.py | 9f781267fbd96da8b2e57a4e0cbc86aabeda87b9b6d8a8beb21fc870d692129b | synced to 4090 HEAD |
| experiments/stage2_v11_fixed_h_camera/calibrate_lambda.py | 0578a68e994aa33117824148bff2c112a86fcf376580af39a5f8d9d22e895496 | synced to 4090 HEAD |
| experiments/stage2_v11_fixed_h_camera/data.py | 231234d20ccce136faf6637abc2c3371ae22e84c60065c893bd962681bbb1eef | synced to 4090 HEAD |
| experiments/stage2_v11_fixed_h_camera/evaluate_confirmation.py | ac2f4e89d701faede7172785a764bb853a5110d4d94850958375a09eb36e36cc | synced to 4090 HEAD |
| experiments/stage2_v11_fixed_h_camera/evaluate_pure4053.py | a14f1bc1e1257e6e1967bef44d0974f5bf037aafb6326f2043c55bacf1cd39fd | synced to 4090 HEAD |
| experiments/stage2_v11_fixed_h_camera/evaluate_screen.py | 014e94890b99fd943e298b8a25b85a538549f0976fc4687d86d1e6545dc5a6f5 | synced to 4090 HEAD |
| experiments/stage2_v11_fixed_h_camera/evaluate_v9_30k_comparator.py | 272748041b40b4817e5341b3e28d7461f30095f9690d36bdaf20caef7e33e3ec | synced to 4090 HEAD |
| experiments/stage2_v11_fixed_h_camera/make_continuation_contract.py | 22109f0d08cfbda887bd914b82edbdaa807eae5bd0b5975af3a1458395df39ab | synced to 4090 HEAD |
| experiments/stage2_v11_fixed_h_camera/make_run_contract.py | 204529adce9eb0dc26f9610aa05e7788fd29430794baeb09ac0f90c0cd53e47f | synced to 4090 HEAD |
| experiments/stage2_v11_fixed_h_camera/make_shared_contract.py | 8e086f9ed41e2e37eb25c2ec12255099cd0f1879fd8bff5d80712a53462eb845 | synced to 4090 HEAD |
| experiments/stage2_v11_fixed_h_camera/model.py | c91f45e5e8bb31075aae1c3c01ef483025be2b872dd47e8033028bfd657aa8a8 | synced to 4090 HEAD |
| experiments/stage2_v11_fixed_h_camera/preflight.py | e6195bc2cb74dd8a8211b67e88b2a9a91f40ddee48d36f2781e0fd5463a3d2d7 | synced to 4090 HEAD |
| experiments/stage2_v11_fixed_h_camera/render_confirmation.py | b52cc9c051eba975fa8216ef3ae2ed17246389f410259eec064fe3d4a9619072 | synced to 4090 HEAD |
| experiments/stage2_v11_fixed_h_camera/test_v11.py | 676f42443de9a6306d0c12810d08e7dbba6e1f7652346c9764a11bb09419c7aa | synced to 4090 HEAD |
| experiments/stage2_v11_fixed_h_camera/train.py | 5c8edbf046f4b47dc8a693563401227f378bba4479a157417854d7f61383aa6b | synced to 4090 HEAD |
| experiments/stage2_protected_h_vimogen/__init__.py | 359ca9dd3b018661cd4344b3d218198c7c6a71a6c3abf1c1b9e8e60a270208db | synced to 4090 HEAD |
| experiments/stage2_protected_h_vimogen/build_cache.py | fe1fa7a618a81e994f6e3844736f0e59b9bf8f385bbe43fbedb679c36b0279fd | synced to 4090 HEAD |
| experiments/stage2_protected_h_vimogen/build_text_cache.py | 8cb5dbf1d191c585befbb172ab6558e440303b4844be5136f984446e4b714dad | synced to 4090 HEAD |
| experiments/stage2_protected_h_vimogen/data.py | f349f123e0424fe7f43316c953a323deac10b9e5ea416b63a9b474573089ee52 | synced to 4090 HEAD |
| experiments/stage2_protected_h_vimogen/evaluate.py | cefe0ca5de342022440f1b816e256381ababa0b4374be0d209be681935f3f107 | synced to 4090 HEAD |
| experiments/stage2_protected_h_vimogen/make_contract.py | c023e6bc0f3e297f9a14acfb461f2dc6375cb14ab6f2afacd4c2f5c62b5dc033 | synced to 4090 HEAD |
| experiments/stage2_protected_h_vimogen/make_eval_contract.py | 0bd02e1cbdd8845db86630a60fb51ad65a8dcdfc47ce1b34352117bbdb5ae94e | synced to 4090 HEAD |
| experiments/stage2_protected_h_vimogen/model.py | 52d4ce24eba5d5b590af59a04fa1cd976f0c3cb0cde1b2ef4f0766dd328a0f2d | synced to 4090 HEAD |
| experiments/stage2_protected_h_vimogen/preflight.py | 87fb7ccd1495b3625c6ca4c84a66d5d6ae5e48caefb908e2123a2d1cba53a975 | synced to 4090 HEAD |
| experiments/stage2_protected_h_vimogen/render_fixed_pair.py | 6ad21896b001ee30c0ab7e0a8b37123efa2edfd64847fa2447339203e06b8ab0 | synced to 4090 HEAD |
| experiments/stage2_protected_h_vimogen/runner.py | 938133eed6c444b441e5989f8c6c6527b72ba52aabd4723f06cdc3fdbe221d44 | synced to 4090 HEAD |
| experiments/stage2_protected_h_vimogen/test_build_cache.py | 930f6fb17298b9bf23a096d1828e39ff50ebbe9a2577141343439b827cc6a648 | synced to 4090 HEAD |
| experiments/stage2_protected_h_vimogen/test_build_text_cache.py | 03e423347f4c8698638045e49f2de416b7f76f64499433cf0a437025c1037405 | synced to 4090 HEAD |
| experiments/stage2_protected_h_vimogen/test_data.py | 019b45aaadcd6b7c0f7e42401ebec61838fde1153e6293b7e4fc126fbff5fbe0 | synced to 4090 HEAD |
| experiments/stage2_protected_h_vimogen/test_evaluate.py | c5901285afc54c1ec92f7c986ed06920e871b777351769e4bee626a46edc8689 | synced to 4090 HEAD |
| experiments/stage2_protected_h_vimogen/test_make_contract.py | 976edff9667beb52869382fbc86f0f7f733ad79b7f30d561b87fede1a9a55bbc | synced to 4090 HEAD |
| experiments/stage2_protected_h_vimogen/test_model.py | 1d42a87517dd7bf86d126397c085abff2251f51157da66798ac67d1e47b9ba11 | synced to 4090 HEAD |
| experiments/stage2_protected_h_vimogen/test_runner.py | aa4f0d360fec19e616568faf3e00c8e29105b802dc8cf0af403ffcaa7c4839a1 | synced to 4090 HEAD |
| experiments/stage2_protected_h_vimogen/unified_endpoint_diagnostic.py | db7b8300c72e040777cff29796325275a08e8740a9a2439e8f39097bd06f7c16 | synced to 4090 HEAD |
| experiments/stage2_backbone_upper_bound/e6_c3_vimogen_h/model.py | 1d6a9c7159decf594cd4e227f973d16f20d05d9a84bf0d6e4df3d33c23990374 | synced to 4090 HEAD |
| experiments/stage2_backbone_upper_bound/e6_c3_vimogen_h/text_cache.py | f8b809184bc1b2b544a3c97236b52464bb0a22f4790acfa3e70bd4785477d9bf | synced to 4090 HEAD |
| experiments/stage2_v11_human_text_camera/__init__.py | 960f08abd5a14ab2e73abce0f8ade4b4a0c607818f4bf0b5382a297449bd2549 | synced to 4090 HEAD |
| experiments/stage2_v11_human_text_camera/data.py | da9cf5bac84d19a2bf92b73c5ee987ea57baed8350380a6ebf566d507c2f3bc8 | synced to 4090 HEAD |
| experiments/stage2_v11_human_text_camera/model.py | 2e756d489a217dd3b3548a390366fb13d7387b0d8adf085d3ddc4e294c4e8db8 | synced to 4090 HEAD |
| experiments/stage2_v11_human_text_camera/runtime.py | 128cd95cc68638ac5330ab9f8882d7f7cfc628aec23c690233b9dade8c5dcc16 | synced to 4090 HEAD |
| experiments/stage2_v11_human_text_camera_fresh/__init__.py | 5b4bdd8bb520b7a5fd0c4ed72504537d665a8cc12824ee775a2bbed266d6cde2 | synced to 4090 HEAD |
| experiments/stage2_v11_human_text_camera_fresh/audit_pure4053.py | a43b51ce7c322e0076a34b2aff7abf579d60b3cb3a0d9faef0a2811f2a2010bf | synced to 4090 HEAD |
| experiments/stage2_v11_human_text_camera_fresh/evaluate_pure4053.py | 306e5d3e503195d9273521a26b29fec41ca553fa95645bcf48d77d8cf816c632 | synced to 4090 HEAD |
| experiments/stage2_v11_human_text_camera_fresh/make_contract.py | a8e6993cd133ecdcf488ae2f14780d98e3c7210cfb91262f197eeaaedf12f125 | synced to 4090 HEAD |
| experiments/stage2_v11_human_text_camera_fresh/model.py | 5d2700af3da92394ea027938680d49efe6e102d4198a1c52b7b0445987b0d2a8 | synced to 4090 HEAD |
| experiments/stage2_v11_human_text_camera_fresh/preflight.py | 7a598e5482f6af19a69b0932927ee3aaa52f12597f94846eee31a01bb67a8604 | synced to 4090 HEAD |
| experiments/stage2_v11_human_text_camera_fresh/render_pure4053_comparison.py | e1685d7f59f286beb794dbbb47c8eff18df2ca80c5ebb5677472c13d3c73df96 | synced to 4090 HEAD |
| experiments/stage2_v11_human_text_camera_fresh/runtime.py | 40e14a4e150f1847b03befaf6c31e2c3e70be63a0aa859831a207e0e8374c9d2 | synced to 4090 HEAD |
| experiments/stage2_v11_human_text_camera_fresh/test_fresh_human_text_camera.py | a8bab0a55c7bda691e1f4da96995538c0f63e064814af6d7b1c552c16a57b0d4 | synced to 4090 HEAD |
| experiments/stage2_v11_human_text_camera_fresh/train.py | 85401970eec23bd06c16356e72b024385e6654fc9b74c2b7e275f5b6005caea0 | synced to 4090 HEAD |
| experiments/stage2_sm_c1rel/__init__.py | c40f754c415c942be778978f615388c0c31689bb797ebb28e7c4138e70e98f85 | synced to 4090 HEAD |
| experiments/stage2_sm_c1rel/make_contract.py | 40b49111f16feaac2d929a59014c4a17757bbd58483ba32330cf1252796f96dd | synced to 4090 HEAD |
| experiments/stage2_sm_c1rel/preflight.py | 36f83828ecff97babd0a90fd0ef3f073ee454ec0d6ad70441fc039ad71ebb6f5 | synced to 4090 HEAD |
| experiments/stage2_sm_c1rel/test_contract.py | 0c932e334f834ecafbd9da7cef8d395325565534b553115cbff964694b1babb4 | synced to 4090 HEAD |
| storymotion/experiment_invariants.py | 3690778d743918dbf487bfa44f5b1b50c9fcf9623a1ca03d0cc46675923325d3 | synced to 4090 HEAD |
| storymotion/per_sample_quality.py | 7e356764c9bab74a7ae6afc51f65dc91e868536861dcd67a8c7a9c4fd4a18026 | synced to 4090 HEAD |
| storymotion/tokenizers/base.py | 72cef8f3e0463de0986780072e58bd4db4126e01a8b7c60d3a0e77f729761ecb | synced to 4090 HEAD |
| storymotion/training/joint_data.py | 6da5f24e3c801c62849736065e8843e81335e9f08b7bb912e776483fb8fd7c05 | synced to 4090 HEAD |
| docs/experiment-contract.md | 7976bb2b8add4414bf54e23d1dba2508703a4926f7908e70db6b729aa904722e | synced to 4090 HEAD |
| scripts/storymotion_run_layout.py | c650bfbe2d1113224e7fbb6144cadb78c6cf22e452f00364eb3127c7bc800628 | synced to 4090 HEAD |
| scripts/storymotion_stage1_contract_harness.py | c0b01c9382bd744db44f1a545de18267c4591803b887f6f6253ddb2a83e30158 | synced to 4090 HEAD |
| scripts/storymotion_official_bridge_smoke.py | 063dcbe4f7260313861df1939dea8342fba815f1b039e996c182ec16b437f365 | synced to 4090 HEAD |
| scripts/train_stage2_condmdi_human128_pulp_v3.py | 43898e866c5c63745c399325d3298f035a3face13a51506f1b324776a9a67485 | synced to 4090 HEAD |
