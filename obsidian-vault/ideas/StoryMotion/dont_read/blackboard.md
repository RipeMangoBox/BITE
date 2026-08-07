1。Direct Human/camera 的实验目标/核心 setting 是什么？
2。gradio的 top 标签页只是把第二行的 gt 单个视频改为 specialist，保持后两个为 pulp 的 recon/gen；指标也添加 pulpmotion baseline对比
3。（高优先）https://github.com/robincourant/pulp-motion/issues/7是关于 stage1 的问答，目前没有完整公开。local 实现的 64 frame crop 是否会导致长序列处理能力缺失？测试的证据说话，比如找长序列数据 整个序列 recon 测 mpjpe；
4。（高优先）condmdi 虽然有all mask的训练，但占比极低，可见纯 text-to-motion 对 condmdi 是难任务（如果数据集是 humanml3d，可以下载其 ckpt 闭环测试；如果不是则不测），本身应该更多服务于 temporal inpainting。至少 storymotion 对于 mask 的比例没有像 condmdi 按照 mask 量 分配不同ratio。
5。（高优先）之前casual 导致的低质是 stage1 trainig还是 stage2？如果是 stage1，是否能重新尝试 joint ae casual-tokenizer 的 stage2？尤其是 molingo+rf stage2。更合理的做法是否是单纯将 pulp data 用 molingo 的 vae/ae train stage1，通过 stage1 的 reon 指标能直接确定是否需要进一步适配 storymotion stage2？基于目前 non-casual local stage1，能否直接接入 AR 范式的 molingo stage2？为什么？
6。motionstreamer 适配 pulp data，train stage1。

---


1. official pulp stage1 是规定最大长度，然后 mask 无覆盖区域的做法，与 storymotion 不同。这种做法对动作mpjpe 更优吗（短序列和长序列分析）；
2。随意可用 gpu（长程任务）：4090 gpu1，5090 gpu0；可并行任务的 gpu： 4090 gpu0和 5090 gpu3；
3。待分配任务：
（1）storymotion non-causal v7.14 接入 离线 AR model，你来选择合适的。online 和 offline 的核心区别是什么？结合 molingo stage2 说明，能否改写为 offline版本并训练？
（2）motionstreamer 双阶段适配 pulp data 作为 direct H baseline（独立存在，不作为 storymotion 适配），改写 agents 放行。只进行 stage1 train，注意sample exposure相比 storymotion stage1的公平，bs 合理，记录训练过程的指标和 loss；
（3）鉴于 storymotion stage1 在超过 64 帧序列上的 mpjpe 显著不如 pulp，storymotion v7。14 的 stage 是否有必要增加 pulp stage1 处理variant 并 new train：定 max length+mask？有必要则 train，不明确是否被可靠 history exp 覆盖。human rep 质量高了，才能支撑 stage2 的 direct H 和 joint。
（4）frozen official Pulp AE × 同一Unified Stage2 短程 matched screen，最快隔离 representation。为什么只是短训不是长训？有必要则短测试后长训。

上述任务你先评估，并更新文档，然后4 卡部署实验（选择有必要的实验），/goal 直到完成所有实验部署才goal achieved。


---
晚

• 已完成接力、实测、Gradio 部署和文档固
  化。总裁决是：下一轮优先查 non-causal
  Stage1 representation 与 latent
  generatability；不恢复 causal
  tokenizer，也不启动 MotionStreamer
  causal Stage1。

  ### 核心结论

  1. Direct Human / Camera

  - Direct H：仅输入 human text，H/C
    observation mask 全空，只预测 human
    latent，是纯 text-to-motion。

  - Direct C：输入 complete GT-H latent +
    camera text，只预测 camera latent，是
    理想 human source 下的 camera
    completion。

  - 两者共享 v7.38 L0、corrected v7.14
    non-causal joint AE、owning decoder、
    cache、normalization 和 evaluator。
    v7.42 specialist 只用于 shared-vs-
    specialist 归因。

  2. Gradio Top 页已按要求上线

  - 第一行：StoryMotion GT / recon / gen。
  - 第二行：v7.42 joint specialist gen /
    Pulp recon / Pulp Aux gen。

  - aggregate 指标表新增 Pulp no-Aux、Pulp
    Aux。

  - 15 samples × 2 views 的 30 个 callback
    全通过；浏览器实测六个视频可见，page/
    console error 均为 0。

  - 服务 PID 1379105，端口
    127.0.0.1:7865。转发：

  ssh -N -L 7865:127.0.0.1:7865 4090

  3. 64-frame 问题已有实证

  Pulp issue #7
  (https://github.com/robincourant/pulp-motion/issues/7)
  仍不能提供完整官方 Stage1
  recipe。代码核验确认：v7.14 的
  seq_len=64 只用于 synthetic 分支；真实
  Pulp 训练是完整变长序列，没有 64-frame
  crop。

  pure4053 整段重建、最长 251 帧的结果：

  - v7.14 root-aligned MPJPE：70.8 mm（1–
    64）→ 132.0 mm（193–251）。

  - v7.14 global MPJPE：146.8 → 428.7 mm。
  - 同样本 Pulp official AE：root-aligned
    85.4 → 78.0 mm，global 194.5 → 186.7
    mm。

  - local camera ADE 基本不随长度增长。

  所以不是“crop 导致无法处理长序列”，而是
  local human tokenizer 能运行长序列，但存
  在明显 length generalization / root-
  velocity drift。

  4. CondMDI all-mask 已闭环

  使用官方 CondMDI
  (https://github.com/setarehc/diffusion-motion-inbetweening)
  HumanML3D random-frames 750k
  checkpoint：

  - edit_mode=uncond
  - observed-mask sum=0
  - 有效长度 72 帧
  - motion 全 finite
  - temporal std=0.2573
  - root displacement=1.108

  采样及 results.npy 保存成功；之后官方
  renderer 因 zero keyframe 报错，不是模型
  采样失败。

  比例上，CondMDI 的 text 保留 +
  observation 全空约为 0.9 × 0.1 = 9%；
  StoryMotion Direct H 约占三分之一
  slots，因此 StoryMotion 的 all-mask 暴露
  并不少。真正差异是 CondMDI 还覆盖
  partial observation；其 released
  random_frames 当前固定 20 keyframes，也
  不是显式的多密度 bucket 课程。

  5. causal 低质归因

  历史 v7.15–v7.16 不是 causal Stage1
  training：

  - checkpoint 本身是 non-causal v7.14；
  - cache builder 错误按 causal encoder 重
    建权重；

  - evaluator 又用了错误的 official
    decoder。

  因此问题首先位于 Stage1→Stage2 cache/
  decoder boundary，修复后剩余部分才是
  Stage2 learnability。v7.40 MoLingo+RF 已
  使用正确 non-causal v7.14，结果是
  semantic/recall Pareto，但 coverage、
  joint、framing 未通过。

  当前 non-causal v7.14 可以训练新的离线
  AR generator，但不能直接接入官方 MoLingo
  (https://github.com/hynann/MoLingo)
  checkpoint：latent
  dim、downsample、human-only layout 和
  text/operator contract
  都不匹配。必须从零训练
  projection/generator；non-causal Stage1
  不妨碍离线 AR，但不能声称 streaming。

  6. MotionStreamer

  MotionStreamer
  (https://github.com/zju3dv/MotionStreamer)
  的 native TAE/streaming generator 依赖
  causal semantics。当前 StoryMotion
  invariant 明确禁止 temporal causal
  tokenizer，因此这项实验标记为
  contract-blocked，未启动。除非显式修改
  AGENTS.md 和 experiment
  invariants，否则不能把它当普通 control
  偷渡运行。

  ### 下一实验优先级

  1. frozen official Pulp AE × 同一
     Unified Stage2 短程 matched screen，
     最快隔离 representation。

  2. 在完整 162,760 train IDs 上训练 non-
     causal MoLingo-style AE/VAE；先看
     full-sequence length bins，再测
     latent generatability。

  3. 通过 Stage1 gate 后，训练 from-
     scratch human-only AR/MoLingo
     operator。

  4. 只有 human-only 通过，才设计 camera/
     joint integration。

  5. causal joint AE 与 MotionStreamer 保
     持 blocked。

  我把“16w train”解释为精确的 162,760 个训
  练 IDs，而不是 160k optimizer steps；
  Stage1 与 Stage2 cache 使用同一 train
  split，pure4053 不进入训练或 checkpoint
  selection。

  关键文档与代码：

  - obsidian-vault/ideas/StoryMotion/2026-
    07-17_storymotion-stage1-length-
    condmdi-causal-priority.md

  - obsidian-vault/ideas/StoryMotion/
    version.md

  - obsidian-vault/ideas/StoryMotion/
    StoryMotion_Gradio_Render.md

  - linkedCodebases/StoryMotion/scripts/
    eval_stage1_long_sequence_geometry.py

  - linkedCodebases/StoryMotion/scripts/
    v736_p0_matched_gradio.py

    -----



    • 结论先行：4090 双卡任务已全部完成；5090 gpu0 只完成了 105K 训练，正式 eval
  因部署缺文件而失败；现有 30K 主线基线足以做 matched screen，但不能替代 105K
  的正式晋级结论。

  🧭 StoryMotion 接力（2026-07-17—07-18）
  Progress: 4090 上 v8.1A、v8.1B、v8.2 均完成 636K steps / 81.38M exposures 和
  pure4053 Stage1 geometry eval；5090 v7.47 完成 step105K，10K N64 screen 通
  过。
  Plans: 先修复并完成 v7.47 正式 eval/分析，再决定是否启动非晋级性质的 30K
  Stage2 diagnostic。
  Problems: 三个 v8 Stage1 candidate 都未通过全部预注册 promotion gate；v7.47
  缺少模块且 experiment contract 当前审计失败。

  ## 1. 4090 双卡实际完成时间

  截至 2026-07-18 10:48 CST，4090 两张卡均空闲，无 StoryMotion 训练或评测进
  程。

   Run             训练完成    pure4053 eval 完成
  ━━━━━━━━━━━━━━  ━━━━━━━━━━  ━━━━━━━━━━━━━━━━━━━━
   v8.2 / GPU1     03:44       03:46
  ──────────────  ──────────  ────────────────────
   v8.1A / GPU0    04:42       04:44
  ──────────────  ──────────  ────────────────────
   v8.1B / GPU0    08:57       08:59

  因此原 ETA 已被实际时间取代：最终队列在 08:59 CST 以 failures=0 闭合，原先三
  个 ETA 窗口基本准确。

  ## 2. 4090 Stage1 分析结论

  预注册阈值见 obsidian-vault/ideas/StoryMotion/2026-07-17_storymotion-v8-yaw-
  quality-nonar-diffusion.md:117。

   Run        Overall     193+ RA/    slope RA/     Cam-ADE    结论
            RA/global    global mm       global        mm /
             MPJPE mm                   mm/100f    rotation
  ━━━━━━━  ━━━━━━━━━━━  ━━━━━━━━━━━  ━━━━━━━━━━━  ━━━━━━━━━━  ━━━━━━━━━━━━━━━━
   v8.1A      24.70 /      33.70 /      +2.89 /     47.69 /    Fail：global
                71.18       117.18       +31.10      0.717°    slope > 20
  ───────  ───────────  ───────────  ───────────  ──────────  ────────────────
   v8.1B      28.24 /      23.41 /      −8.07 /     50.71 /    Fail：两项
                76.65        79.50        −1.12      1.170°    camera gate
  ───────  ───────────  ───────────  ───────────  ──────────  ────────────────
   v8.2       13.00 /       8.97 /      −4.52 /     53.03 /    Fail：Cam-ADE
                68.71        52.46       −17.27      0.569°    > 50

  结论边界：

  - 三条训练都有效完成，human geometry 均显著优于旧 v7.14，但严格 gate 是合取
    条件，因此目前没有可晋级 candidate。

  - 不得把任一 checkpoint 改名为 mainline，也不得据此构建 promotion-bearing
    Unified Stage2 cache。

  - 不建议事后按 pure4053 geometry 挑选 best_top* 来绕过 endpoint gate；当前合
    同明确归属 last.pt。

  - 若只做研究诊断，v8.1A 可隔离“同 human199 + geometry loss”，v8.2 可测试
    non-integrative human200 上限，但必须标为 non-promotion control。

  ## 3. 5090 gpu0：训练完成，eval/分析未完成

  若“实验已完成，eval，分析”的意思是“训练已完成，下一步做 eval 和分析”，当前状
  态与之吻合；若意思是“eval 也完成了”，则需要纠正。

  Run：

  v7_47_official_ae_unified_matched_seed17_5090g0_20260717

  已确认：

  - step105K 于 2026-07-18 00:07 完成。
  - last.pt SHA256：
    b8c06913a5efdbaa0c178e452998352033174614aa0a60ad96920fe14a8acbb2

  - 10K、每任务 64 样本的 structural screen 通过，决策为 continue_to_105k。
  - GPU0 当前空闲。

  未完成原因：

  ModuleNotFoundError: No module named 'storymotion.training.human200'

  5090 缺少 storymotion/training/human200.py；本地与 4090 上该文件一致，SHA256
  为：

  67725b89acd738b8f6ce23936638ec329776828207c0c5ebc08ee35ac549f69c

  此外，当前 experiment_contract.json 不能通过审计，缺少 stage、data.*、
  train.*、eval.* 等必填字段，manifest 仍停留在 status=training。因此不能直接
  把后续 JSON 写入正式账本。

  ## 4. Stage2 是否只跑 30K

  可以，但只能作为 matched screen，不能替代 105K formal endpoint。

  已有精确 30K 基线：

  v7_36_p0a_asym_unified3_joint30k_seed17_4090g0_20260714

  它满足：

  - 是 v7.38 L0 105K 的直接父 checkpoint，SHA256 7dcf3b19…3382c0b。
  - 已有 pure4053 human、camera、directed parallel、human-first cascade 四套完
    整 JSON 和 records。

  - ordered ID SHA、seed17、DDIM50、CFG1、eta0、cache、decoder及协议均有记录。
  - v7.38 正是从该 step30K 严格恢复 optimizer，再训练到 105K。完整证据见
    obsidian-vault/ideas/StoryMotion/StoryMotion-valid-metric-ledger.md:461。

  但 105K 对 30K 是系统性提升：

  - Direct-H：FDTMR 399.73 → 333.88，TMR 11.391 → 13.294，HCov 33.11% →
    40.54%。

  - Direct-C：FDCLaTr 114.57 → 33.29，CLaTr 35.07 → 55.64，CCov 61.56% →
    73.23%。

  - Parallel 与 cascade 的 human、camera、coverage、caption 和 outscreen 指标
    也全面改善。

  所以推荐采用两阶段预算：

  1. 新 representation 的 Stage2 从零训练到 30K，与 v7.36 A30 做完整 matched
     comparison。

  2. 只有达到预注册 retention / improvement gate，才从同一 checkpoint 和
     optimizer 继续到 105K，与 v7.38 L0 比较。

  3. 若 30K 无有效信号，停止，节省后续 75K。

  不要因 latent 仍为 192 channels 就恢复 v7.36 权重；Stage1 checkpoint、latent
  语义或 cache 改变后必须从零训练。

  实测耗时参考：

  - 4090：0→30K 约 3小时52分；30K→105K 约 9小时40分。
  - 加完整四 profile eval，单 run 的 30K 决策约需 4.5小时；105K 总计约 14小
    时。

  - 两张 4090 可并行各跑一条，以上不含新 cache 构建时间。
  - 当前证据只有 training seed17；“完整且有明显效应”成立，但若“显著”指统计显著
    性，仍需 paired bootstrap 或额外训练 seed。

  ## 5. 下一位 agent 的执行顺序

  1. P0 — 5090 v7.47 收尾
     核验 endpoint/cache 哈希；补齐缺失模块且确认 SHA；用现有事实补全 contract
     并先通过 audit；不要重新训练。随后完成 pure4053 Direct-H、Direct-C、
     parallel、human-first cascade，以及 decoded geometry，再逐项 audit。

  2. P0 — v7.47 分析
     与 v7.38 L0 105K 做显式 version / run 对比，列出唯一允许变化的
     representation、cache、owning decoder；不得把 official Pulp AE control 写
     成 corrected v7.14 joint AE 结果。

  3. P1 — 4090 结果入账
     将 v8.1A/B/v8.2 从 training 更新为 completed_no_promotion，写入上述 gate

  5. P2 — 可选 30K Stage2 diagnostic
     仅在明确标为 non-promotion control 后启动；完整复刻 v7.36 A30 的 phase-1
     训练和四 profile 评测协议。30K 过门后才续至 105K。

     ---



1。 后续实验不关注 cascaded，不作为评估标准；
2。 gradio 赞同安排和三卡分工，注意标签页添加指标；
3。 fresh screen是什么？
4。 在渲染之余，需要你聚焦思考 （1）stage1 保持 human 优化的同时，提高 camera，这是 stage2 三模式都优秀的关键；（2）v8.1A的 stage2 为什么会显著放大 camera 的不足？是stage1 manifold 问题，还是 stage2 没能正确处理 stage1 的变化，还是本身的训练约束不足以很好地收敛 camera 能力？


---
StoryMotion_Checkmate.md 用于记录 storymotion 迭代过程中遇到的核心问题、分析与解决路径，帮助我积累失败-解决经验，辅助后续研究解决相似问题。

遇到的问题、验证思路、如何从结果分析，得出结论或细化结论的过程，脉络清晰写入obsidian-vault/ideas/StoryMotion/StoryMotion_Checkmate.md，总分结构，先用箭头图画出脉络。


第一层机制证据已经很明确：v8.1A 与 v7.36 的
  Stage2 训练配置、样本 IDs、任务曝光（各约
  512 万）、非因果缓存、full-cov whitening 都
  是匹配的；而且 v8.1A 在 30K 的 camera 标准化
  latent eval loss 反而更低（0.109 vs
  0.155），但正式 Direct-C 指标显著更差。这基
  本排除了“只是 camera 没训练够 / loss 没收
  敛”作为首要解释，当前首嫌是：相同 latent MSE
  在 v8.1A 的 camera manifold/decoder 中不再等
  价于相同物理与语义误差。我正在继续算
  whitening 逆变换谱与 D4 raw→decoded 放大率。

“fresh screen”具体指：用新的 run ID、相同
  seed=17 和完全匹配的数据/架构/优化器，从随机
  初始化的模型与优化器状态训练到 10,176
  steps；只改变预注册的 camera-center dose。它
  不读取旧 step-214 的模型、optimizer 或 RNG，
  也不是继续训练，更不是完整 636K endpoint；用
  途只是低成本比较 dose 是否同时守住 human 与
  改善 camera。这个定义已写入当前 diagnostic
  ladder，避免以后再把 “fresh” 误解成清缓存或
  换数据。

D4 已经给出决定性结果：这是“Stage1 manifold
  局部敏感性 × Stage2 错误代理”共同作用，不是二
  选一。

  - t50：v8.1A 的 whitened residual 只高 8.4%，
    进入 owning decoder 前已高 21.4%，最终 Cam-
    ADE/FDE 高 55.0%/60.4%。

  - t500：1.022× → 1.147× → 1.207×/1.248×。
  - t950：只有轻度差异，rotation 反而 0.956×。

  也就是说，v8.1A 的误差方向更对齐 camera
  manifold 的高增益方向，尤其低噪、近流形阶段；
  Stage2 的 element_mean whitened x0 loss 看不
  见这些方向，decoder 又在 t50 进一步放大。结论
  明确反对“只训到 105K”或“纯 high-noise prior
  崩坏”。我现在复核代码/records/hash，并把完整
  D4 数值写入 metric ledger，把下一条实验收窄到
  camera-sensitive objective，而不是盲目加曝
  光。


  1。whitening 逆变换谱，D4 raw→decoded 放大率，owning decoder 分别是什么？
  2。fresh screen 意思是只改变模型初始参数/优化器（有啥可随机化）/RNG （是啥），其余均不变，相同环境和条件 retrain 吗？目的是测试 setting 是否能得出稳定的结论吗？为什么还有 25%/50% fresh scree 一说？A10是原本的 v8.1A的别称吗？目前的描述容易分不清楚 stage1/2。C3/D4 是什么实验？全部写入versions table
  3。5090 问题是 hdd 同时有 io 密集和计算密集（除了数据读取）时候，计算密集会被拖累吗？你是如何解决的？在 系统盘构建 cache ，还是将数据cp 到系统盘？还是没处理？如果涉及数据的迁移，更新 agents 规定每个服务器 storymotion 后续的数据读取。
  4。遇到的问题、验证思路、如何从结果分析，得出结论或细化结论的过程，脉络清晰写入obsidian-vault/ideas/StoryMotion/StoryMotion_Checkmate.md，总分结构，先用箭头图画出脉络。
  5。5090 gpu0 已完成，分析，更新文档，然后重构优化。


  ---
讨论：
1. 5K matched screen：
（1）是在 C3-105K 基础上 continue-training吗？
（2）是否比从零按照 Direct—C 的 clean—H 和 generated—H 混合能更快看到效果？
（3）5K 训练量是否足够？
（4）q(H_gt,t)是Director-H 的t step 单步 denoise 结果吗？是否有必要见到不同 t 的 q(H_gt,t)？是否有必要引入 joint 下的H？
2. Screen eval：
（1）打算验证什么？实现方式是什么？
3. P1
（1）calllibration，holdout，double-view 分别指什么？
（2）数据增强如果需要 manual label需要写清楚目标/标准/操作流程。人标至多百级数据，主要还是自动化构建和评估质量，人工负责抽查构造质量。
（3）pulpmotion dataset 基于CondensedMovies dataset，本身是 movie 数据，因此天然包含了导演设计的人物-镜头语言。因此构造后的新数据也需要包含人物-镜头匹配度的评估，这里需要设计新的指标来衡量。可参考obsidian-vault/ideas/camera/2026-06-05_camera-movement-generation-system-survey-llm-audit-merged.md
（4）目前 TMR 和物理筛选后，分别保留了多少？两边取交还剩多少？具体的筛选机制、阈值、结果更新到obsidian-vault/ideas/StoryMotion/2026-07-17_storymotion-v8-2333-data-curation-plan.md。

---
先 4090/5090 所有修改按目标分批同步，然后完成：
1. （1）5K matched screen: 赞同三分支的 105-110K的 5K 训练，部署在 4090 双卡和 5090 gpu2，预估单任务完成时间；（2）2. Screen eval是在 110K 完成后，连带 C3-25，和三分支共 4 个分支进行 profile吗？
2. P1:
（1）已完成的只是 tmr、物理的计算，没有具体施加阈值是吗？先利用完成的双分支+分层阈值给出初步的独立和求交筛选结果（两个分支各自的多阈值独立筛选，以及两边多组求交的各自结果）。目前
（2）暂不进行人工标记，因为目前要做的只是筛选不是创造。
3. 数据增广（结合 humanml3d 是否有设计和实质实验？如果没有，先生成 plan 到obsidian-vault/ideas/StoryMotion）

----
1. 四分支需补充 human/camera completion，然后三模式统一给出指标变化分析，然后 Tq 分层归因。409 双卡，5090 gpu1/2 可用
2. obsidian-vault/ideas/StoryMotion/2026-07-17_storymotion-v8-2333-data-curation-plan.md清除已经更正的错误的处理，保留未解决的，md保持干净核心信息。我没理解全 pair 为什么会有 32w，不应该只有 <camera, motion> 共 16w 左右 pair吗？
3. 数据清洗新要求：obsidian-vault/ideas/StoryMotion/sft-data-prepare.md，判断合理性后落实

---0722 15：48

1. 执行 matched 5K arm：clean-H 75% + q(H_gt,t) 25%，仅采样 t∈[399,799]。但我有个深层担忧：camera completion 和 joint 可能存在训练梯度分配的冲突：camera completion目标支持 clean H + camera text，目的是学习如何从 clean H + camera text 去噪 camera；joint 是从 camera text + concate 去噪的 noisy H 联合去噪 human-camera. completion 中 H 是 input 且 clean；joint 中 H 是 concate 且 noisy。目前 arm 是实际是将梯度贡献分配给 completion 和 joint 模式，所以很可能一个提高另一个降低。我的判断是否合理？先部署实验再分析有没有更合理的做法兼顾两者，同时不影响 human 质量。
2. obsidian-vault/ideas/StoryMotion/2026-07-17_storymotion-v8-2333-data-curation-plan.md 更新了更细粒度的数据清洗和训练分配，评估合理性，重构v8-2333，然后落实清洗，咱不训练。
3. 更新 current 的 todo list 与优先级

---0722 18：43
1. `Direct-C 与 joint-C 在 shared trunk、Camera path、output head 上均为正向或结构性正交`结论如何得出的？
2. obsidian-vault/ideas/StoryMotion/2026-07-17_storymotion-v8-2333-data-curation-plan.md和obsidian-vault/ideas/StoryMotion/sft-data-prepare.md重构为一个正式文档包含核心信息和进度；目前两份文档都没看见具体的分档标准以及分档结果
3. 目前 stage2 在三模式下使用的是相同的 network，只是修改输入和 mask 吗？三个模式具体的数据流说明写入obsidian-vault/ideas/StoryMotion/StoryMotion-iclr-reliability.md。例如，joint 是对 concat 的 human-camera latent 去噪且输入接收的是 human 和 camera text；那 human/camera completion 时候，是对没有使用的 latent dim mask 吗？另一 branch 的 text embedding 如何占位？


---0722 19：40
1. 我发现导致 joint 和 direct 不一致优异的高可疑因素，4090 双卡/5090 gpu1 开启三组实验的 105K。
记 `1` 为 valid frames 上启用、`0` 为关闭：

｜ line | mode / task ID | `obs_mask(H,C)` | 进入 U-Net 的 latent state | routed text | `loss_mask(H,C)` | 最终任务输出 |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | Direct-H / 1 | `(0,0)` | `[H_t,C_t]` | `[0,e_H]` | `(1,0)` | Human |
| 2 | Direct-C / 0 | `(1,0)` | `[H_0,C_t]` | `[e_C,0]` | `(0,1)` | Camera；Human 固定为 observed branch |
| 3 | joint parallel / 2 | `(0,0)` | Human view 与 Camera view 见下节 | `[e_C,e_H]` | `(1,1)` | Human + Camera |
| 4 | Joint-H / 2  | `(0,0)` | `[H_t,0]` | `[0,e_H]` | `(1,0)` | Human |
| 5 | Joint-C / 2  | `(0,0)` | `[H_t,C_t]` | `[e_C,e_H]` | `(0,1)` | Camera |

其中 line3 joint 可以分解为 line4+line5，与 line1 和 line2 对比可得以下不一致点：
显式不一致：
（1） routed text差异：Direct-H 的 `[0,e_H]` 对 Joint-H 的 `[e_C,e_H]`；
（2） latent state差异：Direct-C 的 `[H_0,C_t]` 对 Joint-C 的 `[H_t,C_t]`；
隐式风险：
（1）routed text差异：没有尝试Direct-H，Direct-C，Joint-H 都使用 `[e_C,e_H]`（虽然可能违反 `单向H->C`规定）；

---0722 20：24
`Direct-C 与 joint-C 则同时存在四个差异`除开 task embedding（这条估计作用不大，但不做额外的验证，默认 task embedding 设置）实际只有两个核心差异：
- H_0 vs H_t
- [e_C,0] vs [e_C,e_H]

其中，(`[H_0,C_t]`, `[e_c, 0]`) 是不合理的绑定；(`[H_0,C_t]`, `[e_c, 0]`), (`[H_t,C_t]`, `[e_c, e_h]`) 是合理的绑定。
因此，为了完备性，实际需要补充单项实验：
（1）Direct-H 的 `[H_t,C_t]`, `[0,e_H]` 换成 Joint-H 的 `[H_t,C_t]`, `[e_C,e_H]`；
（2）Joint-H 的 `[H_t,C_t]`, `[e_C,e_H]` 换成 `[H_t,0]`, `[0,e_H]`；
（3）Direct-C 的 `[H_0,C_t]`, `[e_c, 0]` 换成 Joint-C 的 `[H_t,C_t]`, `[e_c, e_h]`；
（4）line1/2/4/5 的 routed text 全换成 `[e_C,e_H]`, latent 全换成 `[H_t,C_t]`；

---0723 15：29
1. VACE 借鉴：VACE仓库：4090 /data/public/ripemangobox/Motion/VACE， paper：本机 /home/ripemangobox/Coding/Github/OpenSource/On_Process/BITE_Process/obsidian-vault/paperPDFs/ICCV_2025/VACE_All_in_One_Video_Creation_and_Editing.pdf。VACE 也是统一架构实现多任务训练。从他的mask，loss，数据组织，pipeline 等维度，详细分析他为什么能进行高质量的多任务学习，以及能够启发设计 storymotion stage2（不限于 stage1/2，课可以新增 stage 但强调每个 stage 目标和分工调整） 的哪些新的模式和设计？（架构/数据组织/训练阶段等任何维度都支持调整，但需要给出storymotion 目前的显著不合理或可疑点依据）
2. storymotion 问题总结：除了 ALL-JOINT arm 外，其余 arm 和 parent 都存在 joint 和 direct 的训练目标问题（从 clean 还是同 step noisy；是否看到另一 branch 的 text embedding 等的分歧）；
3. 可视化上，任何 arm 都在 799 step 存在 heading 不合理问题。基于 stage1 发现 heading 显著影响 重建的统计指标和物理质量，合理怀疑优于 H heading 预测偏差大，导致 H 整体和 C 伴随受到影响。
4. 清洗数据的质检，以及基于清洗后的多层次数据重新安排 storymotion 重训；
5. 数据增广的必要性；

12345 分别从不同维度尝试解决 storymotion 的三模式综合拟合和可视效果不佳的问题。让 agent 上述思考和问题的判定（小任务可在 4090 与 training 并行）

---0723 17：15
1. 目前 direct-h/joint-h 的human质量均不高，我觉得最核心的是要先解决human 质量问题（但我没有单独的 human 单任务训练过，不清楚是三模式混合还是 human 能力上限不足）。需要基于 mainline 的 stage1 先单独训练 human

完成：
1. obsidian-vault/ideas/StoryMotion/StoryMotion-iclr-reliability.md 的优化重构，目前太脏，表述繁琐且多语言混合，统一为核心内容和清晰中文
2. 如果 stage1 有证据证明明显构成 stage2 的瓶颈，需要聚焦根因，是数据表示，还是训练监督问题。为什么模型会对 heading 敏感？需要优化 latent space，简化 stage2 学习难度。 pulp official 的 stage1 将 camera 的 distance 建模为相对于 human root 的 realtive，storymotion 因为 stage2 的 direct-c 从 H0，而 joint—c 从 H_t 预测 C，因此主动更换为 global distane 来避免不同模式对 human 在 raw camera14 data 上的因果依赖，从而在 stage1 的指标远胜 pulp。但也因此 stage2 的 camera 相比 pulp 更容易拍不到人。目前还没有尝试过 camera14 基于 relative distance + C3-25 的 yaw + rootxy 的累计 loss 的版本。


---0725 11：09
1. E1 G-SYS-H generator已经完成完整的训练了吗？不要求超过所有指标，只是探测生成能力，且视觉效果优先；generator 是 base transformer+residual transformer 都完成了吗
2. E2 D-SYS-C 在多少训练量之后停止？做的具体是 human compleiton 还是 camera completion 还是双方？我更希望进行 joint 训练；
3. E3 C3-D-DC 和 E4 请给出具体的适配图+说明，绘制原有 pipeline 和适配后的对比，你分析评估。目前更怀疑是适配不合理导致结果不佳。另外，是否是三种模式需要不同的架构调整？如果是，从 joint 开始实验而不是 completion。

---0715 11:42
## 一、当前总状态

工作目录：

/home/ripemangobox/Coding/Github/OpenSource/On_Process/BITE_Process

当前 mainline 仍是：

- Stage1：v8.1C C3-25 seed17，non-causal，Human128 + Camera64。
- Stage2：对应 Unified-3 105K。
- E1/E2/E3 的 105K 训练均完成，TensorBoard 与 21K/42K/63K/84K/105K checkpoints 齐全。
- E4 只有实现骨架、preflight 和 smoke，没有 optimizer run。
- 三个 GPU 槽均已释放。
- v9 当前结论见 obsidian-vault/ideas/StoryMotion/current.md。
- 正式指标与 hashes 见 obsidian-vault/ideas/StoryMotion/StoryMotion-valid-metric-ledger.md:80。

———

## 二、问题 1：E1 generator 是否完整训练？

### 结论

E1 当前实现的 generator 训练到了总计 105K steps

已完成的是：

- 三个 part-wise RVQ-VAE：
    - lower
    - torso/head
    - arms/wrists

- 每个 RVQ endpoint 训练至 30K。
- 一个 PulpGestureShortcut generator：
    - 从旧 5K checkpoint 精确续训到总计 105K
    - batch 128
    - 总 Human exposure 13.44M
    - 31.65M 参数
    - 8-layer GestureLSM GestureDenoiser
    - latent velocity + shortcut consistency objective
    - Euler20 sampling

实现见 linkedCodebases/StoryMotion/experiments/stage2_backbone_upper_bound/e1_g_sys_h/model.py:46。

没有完成的是：

- 没有单独训练 base diffusion/flow Transformer。
- 没有 native GestureLSM 的完整 diffusion → reflow/shortcut distillation 链。
- 没有 MeanFlow arm。
- 当前 Stage2 直接预测连续的 [B,3,128,75] RVQ latent，stage2 是只 Shortcut denoiser。

### E1 实际生成能力

E1 不能简单写成“不会生成”。

Stage1 reconstruction：

- pure4,053 reconstruction floor 通过。
- global/RA-MPJPE：0.4832 / 0.0953 m。
- fixed reconstruction visual 可用。

Stage2 105K：

- FDTMR 819.12
- TMR 11.889
- HCov 0.2493
- global/RA-MPJPE 0.6810 / 0.2144 m
- root ADE/FDE 0.5936 / 0.9670 m

视觉上：

- 骨架拓扑基本稳定。
- 不是随机噪声或彻底 decode collapse。
- 但固定样本经常没有执行文本要求的动作/姿态。
- 长动作有僵硬、重复和低幅度问题。
- 匿名 blind 包已生成，但独立人工 blind verdict 尚未完成。

所以更准确的结论是：

> E1 已表现出非平凡的 Human motion generative capability，且几何比早期模型明显恢复；但文本动作控制与 coverage 仍弱。当前结果不是
> GestureLSM full generator 的能力上限，因为 base/reflow 路线没有完整实现。

### E1 当前适配的主要风险

当前把一个全局 Pulp text512 embedding 投影后，在全部 75 个 latent frames 上重复：

Human text512
  → MLP 768
  → 同一个向量重复 75 帧

GestureLSM 原本最擅长的是时间对齐的 speech/audio/onset/amplitude condition。把它改成常量序列，会削弱局部动作时序和语义覆盖，这与当
前“几何还行、动作不对”高度一致。

此外，native GestureLSM 有四个 observed seed frames；当前 Direct-H 将其全部置零。这也是显著的 distribution shift。

如果视觉优先，建议先完成：
- native-style base generator；
- 以文本动作命中、运动幅度、自然性、长程重复为主的 blind visual ranking；
- metrics 作为辅助，不要求每项超过 C3。

———

## 三、问题 2：E2 在多少训练量后停止？具体生成什么？

### 训练量

E2 有两代结果：

- 历史 original/bounded-FOV/no-framing screens：各自约 5K，当时停止。
- 最终 normalization-corrected MinMax r2：
    - fresh 0→105K
    - batch 32
    - Human/Camera exposure 各 3.36M
    - 53.18M 参数
    - 21K/42K/63K/84K/105K checkpoints 完整
    - 105K 后做 N=512 DDIM50 eval，再判定 stop

所以最终 E2 不是 5K 停止，而是完整训练 105K 后停止 promotion。

### E2 的任务边界

E2 做的是 Camera completion：

observed GT Human199 + Camera text
    → DC3D-style model
    → Camera14

它不是：

- Human completion
- Human generation
- joint Human-Camera generation
- 双方同时生成

Human 始终是 GT observed condition，没有 Human output branch。

### E2 的正确 normalization

最终版本完成了：

normalized Human199
  → inverse Pulp normalization 一次
  → raw joints/RIFKE pose66
  → train-only MinMax

camera14
  → train-only MinMax
  → diffusion loss
  → DDIM sample
  → inverse MinMax 一次
  → canonical camera14 evaluator

test statistics 没有进入 MinMax fit。

### E2 结果应如何解释

相对旧 5K：

- coverage、trajectory、rotation、framing 都显著改善。
- 因此正确 norm 和训练量确实解决了部分早期 collapse。
- 不应再写成“DC3D 完全无法 work”。

相对 C3 Direct-C：

- FDCLaTr：288.87 vs 25.09
- CLaTr：18.59 vs 59.54
- coverage：0.375 vs 0.750
- ADE/FDE：3.308/3.407 m vs 1.591/1.668 m
- rotation：71.07° vs 35.30°

因此仍不适合 promotion。

### 关于用户更希望 joint 训练

这是合理的，但需要重新命名：

> 直接同时输出 Human+Camera 的模型不是原生 DanceCamera3D，而应称为 DC3D-inspired joint architecture。

原生 DC3D 的关键前提就是 observed Human。要 joint generation，必须处理 Camera 分支在 sampling 时看到的是不断变化的 generated
Human，而不是 GT Human；这正是当前 StoryMotion joint blocker 的核心之一。

———

## 四、原 StoryMotion pipeline

flowchart LR
    A["Pulp Human199 + Camera14"] --> B["C3-25 non-causal joint Stage1"]
    B --> C["Human128 + Camera64"]
    C --> D["train-only full-cov normalization"]
    D --> E["192D TemporalObsUNet"]

    HT["Human text512"] --> E
    CT["Camera text512"] --> E
    TM["task id + observation mask"] --> E

    E --> F["predicted H128 + C64 START_X"]
    F --> G["inverse full-cov normalization"]
    G --> H["C3 owning joint decoder"]
    H --> I["Human199 + Camera14"]

    E -. "Direct-H" .-> DH["score Human"]
    E -. "Direct-C: observed H" .-> DC["score Camera"]
    E -. "joint parallel" .-> J["score Human + Camera"]

它用一个 homogeneous Temporal U-Net 同时服务三个不同问题：

- Direct-H：强语义与人体空间结构。
- Direct-C：observed Human 到 Camera 的几何/构图映射。
- Joint：两个 evolving states 的双向耦合。

这三个任务的最佳 inductive bias 很可能不同。

———

## 五、E3 当前适配图与评估

### E3 实际 pipeline

flowchart LR
    A["GT Human199 + Camera14"] --> B["frozen C3-25 Stage1/cache"]
    B --> C["observed normalized Human128"]
    B --> D["target normalized Camera64"]

    N["noise Camera64"] --> E["DC3D SepCFG Transformer"]
    C --> E
    CT["Camera text512"] --> E
    T["diffusion timestep"] --> E

    E --> F["predicted Camera64 START_X"]
    F --> G["concat with observed Human128"]
    G --> H["inverse C3 full-cov norm"]
    H --> I["C3 owning joint decoder"]
    I --> J["canonical Camera14 eval"]

代码见 linkedCodebases/StoryMotion/experiments/stage2_backbone_upper_bound/e3_c3_d_dc/model.py:44。

E3 固定了：

- C3 Stage1/checkpoint/cache/stats/decoder
- Camera64 START_X
- cosine schedule
- DDIM50
- sample exposure
- evaluator

只输出 Camera64，没有 Human output 或 joint mode。

### E3 结果

相对精确匹配的 Parent N512：

  Metric               E3     Parent
━━━━━━━━━━━━━━  ━━━━━━━━━  ━━━━━━━━━
  FDCLaTr ↓         94.43      34.08
──────────────  ─────────  ─────────
  CLaTr ↑           50.08      60.28
──────────────  ─────────  ─────────
  Coverage ↑        0.736      0.899
──────────────  ─────────  ─────────
  Center ADE ↓    1.399 m    1.592 m
──────────────  ─────────  ─────────
  Center FDE ↓    1.497 m    1.665 m
──────────────  ─────────  ─────────
  Rotation ↓       29.07°     32.64°

它是明确的：

> Camera dynamics/geometry 改善，但 Camera text semantics 和 coverage 退化。

### E3 适配可能不合理的地方

用户怀疑适配导致结果差，这个怀疑是有根据的。

1. DC3D 原生 condition 是 raw/time-aligned body geometry；E3 使用 75-frame dense Human128 latent。
2. DC3D 的 body attention/projective geometry 优势被削弱。E3 只把 Human128 与重复的 Camera text 拼接后送进 decoder。
3. 第一版有意移除了 DC3D velocity、acceleration、framing losses。因此它测试的是“DC3D Transformer shape”，不是 DC3D 完整 inductive
    bias。

4. Music branch 被 Camera text 替换，而 Camera text 是每帧重复的全局 embedding，缺少局部构图/镜头事件序列。
5. 只训练 Camera completion，没有 joint evolving-H exposure。它没有测试 Camera branch 如何适应 generated Human。

因此 E3 的几何改善说明 DC3D topology 有价值；语义下降更可能是 condition/interface 设计不足，不能直接解释为 backbone 不合适。

———

## 六、E4 当前适配图与评估

### E4 当前草稿

flowchart LR
    A["C3 normalized Human128 noise"] --> B["Linear 128→width"]
    HT["Human text512"] --> C["single global text token"]
    T["timestep"] --> C

    B --> D["3 cross-attention blocks"]
    C --> D
    D --> E["8 GestureLSM-style spatial-temporal blocks"]
    E --> F["Linear width→Human128"]
    F --> G["Human128 START_X"]

    G --> H["splice into full C3 latent"]
    GC["cached/GT Camera64 at decoder boundary"] --> H
    H --> I["C3 owning joint decoder"]
    I --> J["Human199 eval"]

代码见 linkedCodebases/StoryMotion/experiments/stage2_backbone_upper_bound/e4_c3_g_dh/model.py:159。

状态：

- import/forward/backward smoke 已具备。
- deterministic DDIM smoke 已具备。
- non-causal assertion 已具备。
- 没有 optimizer run。
- 没有 checkpoint。
- 没有 E4 generation evidence。

### E4 适配的主要问题

E4 当前设计很可能不能代表 GestureLSM 的核心 inductive bias。

最严重的是：

spatial_tokens = 1

因此 GestureLSM 的 spatial body-part attention 在 E4 中退化成单 token attention，几乎没有空间意义。

此外：

- Human128 channel 没有已知 anatomical partition。
- 没有 lower/torso/hands 三 part tokens。
- 没有 GestureLSM RVQ。
- 没有 native flow/shortcut/reflow。
- 没有 time-aligned acoustic/text condition。
- decode smoke 将 generated Human128 与缓存中的 Camera64 拼起来再走 joint decoder，带有隐藏的 GT Camera decoder-boundary 依赖。

因此即便 E4 训练失败，也只能否定这个 single-token adaptation，不能否定 GestureLSM topology。

———

## 七、三种模式是否需要不同架构？

我的判断是：需要不同的 branch-level inductive bias，但不一定需要三个完全独立 checkpoint。

  Mode        核心能力                                                    更合适的结构
━━━━━━━━━━  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Direct-H    text semantics、body parts、contact、heading、长程          GestureLSM-style part tokens + spatial-temporal Human
              motion prior                                                expert
──────────  ──────────────────────────────────────────────────────────  ──────────────────────────────────────────────────────────
  Direct-C    observed body geometry、framing、camera dynamics、          DC3D-style Camera expert + raw/projective geometry
              projection                                                  condition
──────────  ──────────────────────────────────────────────────────────  ──────────────────────────────────────────────────────────
  Joint       两个 evolving states 的互相约束、语义一致性、framing        Human/Camera 双流 + 双向 cross-attention + joint loss

一个 homogeneous U-Net 同时承担三项任务，很可能是当前问题之一。

更合理的是：

> 同一 checkpoint、共享 timestep/text infrastructure，但 Human 和 Camera 使用不同 experts，并在 joint mode 通过 cross-attention 耦
> 合。

———

## 八、建议改为 joint-first 的适配

用户希望从 joint 开始，我认为可以，但应命名为：

J-SYS-HC — exploratory multi-axis joint system probe

它不再是 pure-backbone ablation，而是验证“正确的 Human/Camera inductive bias组合是否能生成视觉可信的 joint sequence”。

flowchart LR
    NH["noise Human128"] --> HE["Human expert"]
    HT["Human text"] --> HE

    NC["noise Camera64"] --> CE["Camera expert"]
    CT["Camera text"] --> CE

    HE --> HC["bidirectional H↔C coupling blocks"]
    CE --> HC

    HP["3 learned/anatomical Human tokens"] --> HE
    GP["Human geometry proxy / evolving joints"] --> CE

    HC --> HO["Human128 head"]
    HC --> CO["Camera64 head"]

    HO --> Z["H128 + C64"]
    CO --> Z
    Z --> DN["inverse C3 norm + owning decoder"]
    DN --> OUT["joint Human199 + Camera14"]

建议结构：

- Human stream：
    - 将 H128 投影为 lower/torso/hands 三个 token；
    - GestureLSM-style temporal + spatial attention；
    - Human text condition。

- Camera stream：
    - DC3D SepCFG/temporal Transformer；
    - Camera text；
    - evolving Human tokens；
    - 可选 Human128→22-joint geometry proxy。

- Joint coupling：
    - 每若干层做 H→C 与 C→H cross-attention；
    - 不是简单 concat；
    - 同一 diffusion timestep 同时更新 H/C。

- Outputs：
    - 独立 H128、C64 heads；
    - branch-balanced START_X loss；
    - 之后再单独加入 Camera velocity/acceleration/framing 和 Human physical losses。

### 推荐实验顺序

1. J-SYS-HC-21K：joint-only visual viability screen。
2. 固定 16 prompts × 4 seeds，重点看：
    - 动作是否命中；
    - Human 是否自然；
    - Camera 是否跟随、构图是否合理；
    - Human/Camera 是否互相协调。

3. 如果视觉明确可用，继续到 42K/63K/105K。
4. 然后在同一架构中增加 mode masks：
    - Direct-C：clamp Human stream，只更新 Camera；
    - Direct-H：Human stream主导；
    - joint：双流共同更新。

5. 最终才用同一 checkpoint 报 Direct-H、Direct-C、joint parallel。

如果只训练 joint-only，它只能是 joint system probe，不能提前宣称三模式成立。

———

## 九、下一位 agent 的优先动作

3. 冻结 E2 completion 结果，不继续在当前 single-output Camera branch 上加训练量。
4. 把 E3 保留为“几何正信号、condition/semantics 适配失败”的诊断。
5. 不启动当前 single-token E4；其 spatial bias 已退化。
6. 先给出 joint-first dual-stream 的详细 contract、tensor shapes、loss、mode routing、参数量与流程图，经用户确认后实现。
7. 新 joint run 仍需 TensorBoard，并保存 20%/40%/60%/80%/100% checkpoints。
8. 不覆盖 E1/E2/E3 的旧 runs、decisions、failed eval roots 或 visual artifacts。

---

我弄混了，gesturelsm 没有 base/residual 之分；你直接接力解决上述任务，优先级 E1，E2，E3，E4，一个个部署实验。修正：
1. E1 补 vis；observed_seed 不是 随机种子，而是待生成序列的初始若干 frame/token，相当于提供开始状态；
2. gesturelsm 和 DC3D 相比 storymotion（abbr. STM） stage2，分别对 human 和 camera 有针对性适配。如 gesturelsm的人体分块（对human 保真很重要，但对于 human-camera 则要斟酌，防止 human 侧过分占用带宽），DC3D的 projective/geometry，用 human raw pos 而不是 latent（关联更易学习） 作 condition 等设计，同时两者原本都针对时序任务设计（speech/music input），这都是 STM 不具备的。修改 STM 来达到上述能力工程量大于替换为 gesturelsm/DC3D 后的适配的工程量。我希望能够解决三模式问题，同时保留双方的优势。
3. 删除 E1-E4无意义的短评测（5K 等），只基于合理训练量的结果评测；

后2. 我先看完可视化再决定是否继续：E1为了适应 text embedding condition，请将其架构适配从时序转为非时序导向（面向 text）是否可行？是否严重影响其 stage2 的 spatial-temporal 原设定；

---0726 10:56
完成可视化后，完成一下任务（需要确保长训正常部署，有 tensorboard记录重要指标，按照 storymotion 的 human 分支指标为准，有定期存 ckpt）：
1. 4090 添加把https://github.com/MotrixLab/ViMoGen的 stage2 替换 condmdi做 human only。ViMoGen基于MLD的 vae latent 训练，因此可以无缝替换。在
4090gpu1 先取 512 sample 过拟合测试，然后长训 105K。注意：完整 ViMoGen 以 1.3B Wan2.1 为初始化，使用 276D SMPL-X 表示，训练成本和 representation
mismatch 都很大，不适合作为第一版 StoryMotion 直接照搬。
更合适的是：
采用 ViMoGen-light 的 full-transformer、flow objective、multi-token text cross-attention；不采用完整 T2V branch。

2. 4090 gpu0 空出来后对 MARDM 适配的 stage2 进行相同的 512 train sample 过拟合测试。
3. 4090/5090 修改分多批同步，然后在 5090 使用 T5 替换 ViMoGen 的 storymotion stage2 适配，105K 长训。

--- 0726 15:58
1. MARDM的 storymotion stage2 eval/vis 在哪里？指标分析需写入文档
2. 目前5090没有UMT5 ViMoGen-light 105K，是否运行出错？
3. 两组过拟合是如何判断的？能够过拟合说明什么问题？


---0726 16:53
1. 5090 UMT5 ViMoGen-light eval+vis
2. 4090 的 ViMoGen-light clip 预计完成时间；
3. MARDM 的 storymotion stage2 的物理质量不足，怀疑有以下几点：（1）pulp 的 human data类型多，包含浮空/躺在地面/常规站立相关动作。root 和
heading 预测不准会严重影响整体质量；（2）pulp 本身huma 物理质量/语义对齐均不佳。导致 stage1 的流形学习和 stage2 的语义对齐有困难；
4. ViMoGen-light 的的 human 分支在 humanml3d 上训练，与 video 分支独立。但 storymotion stage1 使用联合的 human-camera（试过使用 separate，两个阶
段质量都严重下滑，很大原因是小规模非优质的 pulp data 很难让两个分支学习到高质量独立分布，联合分布反而降低建模难度）。如何让 storymotion 的
branch 单独增强 human 能力？能否也在 humanml3d 独立训练？stage1 是否需要调整？毕竟 stage1 和 stage2 的 human only 如果分布不同会带来额外的训练难
度。还是说 stage2 的 human branch 使用混合的 pulp 和 humanml3d？

---0726 17:54
# 回答与短测
1. ViMoGen-light CLIP eval+vis;
2. 是否有可靠的历史实验完成过 stage1 的Root/body 互换

对生成结果分别测试：

A
H=(generated body,GT root).
B
H=(GT body,generated root).

如果 A 视觉质量大幅恢复、B 明显崩溃，就可以确认 root/heading 是第一矛盾，而不是 MARDM 对 local motion 的建模能力。
测试理由：
（1） Root 和 heading 是误差放大器

Pulp 的 human representation 是：

Xh=(rz,r˙x,r˙y,α˙,Θ,J),

即：

pelvis 高度；
平面 root 速度；
root heading 角速度；
SMPL rotation；
local/global joint 信息。

也就是说，平面位置和朝向需要积分恢复：

ψt=ψ0+ τ=1∑tΔψ τ,pt=p0+τ=1∑tR(ψτ)vτ.

这意味着 heading 的一个小误差，不只是让人物“转错一点”，还会旋转后续所有 root velocity。时间越长：

root 路径越容易漂；
人物可能侧滑、绕弯或突然换向；
camera-human relative position 同时被破坏；
framing loss 又会驱动 camera 去追一个错误的人体轨迹。

Pulp 确实使用 root planar velocity 和 angular velocity；MARDM 的 essential representation 同样保留 root angular velocity、root planar velocity、root height 和 local joint positions。因此，MARDM 在 HumanML3D 上成功，并不能说明这种表示在噪声较大的视频估计数据上同样稳定。

此外，原始 MARDM 在 HumanML3D 上最长处理 196 帧，而 Pulp 的 Stage‑2 实验直接使用 300 帧样本。即使每帧 root/heading 误差不变，更长的积分区间也会放大漂移。

（2） Stage‑1 重建好，不能排除 root manifold 有问题

Stage‑1 reconstruction 测试的是：

D(E(H,C))≈(H,C).

但 Stage‑2 实际产生的是：

D(z^h​),z^h∼pθ​(z_h∣t).

即使 z^h 离真实 latent manifold 只偏一点，decoder 对 root 通道的敏感度也可能非常高：

||∂D_{root}/∂z_h|| ≫ ||∂D_{pose}/∂z_h||.

于是你会看到：
local pose 似乎还像个人；
但 root、heading、ground relationship 全崩；
最终视觉上整条 motion 都不可信。

Pulp 的 AE reconstruction 本身也显示 mixed subset 的 3D human reconstruction 比 pure subset 更差；而其 human 数据来自 TRAM 视频恢复，论文明确承认它低于 MoCap 数据质量，并用 HumanML3D-pretrained diffusion 去修复不可见身体区域。

3. 目前 stage1 是否只选取每个 sample 的前 64 frame？但在 stage2 最长需要生成 300 frame 序列，尤其电影镜头常常先有人物静止或建立镜头，真正动作在后面发生。这会引入系统性引偏置。

# 数据清洗与长训任务
1. stage1 架构更新&retrain：见 `obsidian-vault/BlackBoard/2026-07-26_stage1_redesign.md`，然后 retrain

---0726 19：08
2. 数据质量评估和清洗：pulp 不同regime data 分桶（按human text），分别评估：

upright/static；
locomotion；
sitting；
lying；
falling；
jumping/airborne。

记录：

root trajectory error；
heading drift；
lowest-joint height；
contact joint velocity；
body penetration；
TMR alignment；
human-camera framing。

很可能你会发现模型不是所有类型都差，而是某几个 regime 把整体视觉体验彻底拉垮。

2. 数据清洗后，storymotion stage2 ViMoGen-light retrain；

3. humanml3d 注入策略以这个版本为准：


---0727 13：23
1. stage1 旧版/redesign版 分别是否有 fixed first 64 frame 的严格裁切（不训练长 sample 的后续内容）？
2. resigned stage1 & HML+pulp：
（1）HML-root-local + Pulp-full 和 Pulp-only 都基于 redigned 的 stage1 吗？为什么不包含 pose6d（实际是 rot6d）？
（2）为什么 N=4053 和 N=1460 的 HML-root-local + Pulp-full 和 Pulp-only 两种 setting 优势完全反转？说明的是 eval 集特性，还是setting 问题？
（3）删除Pulp Camera r1、Pulp r2 与 HumanML r1等失败实验的所有实验数据和文件，以及文档描述，因为不再需要。
（4）metric table 添加 C3-25 的 stage1 的指标，以及新的 stage1 recon的 pulp vis：gt、C3-25（我忘了 stage1 编号）、redesign stage1 pulp，redesign stage1 HML+pulp；然后针对redesign stage1 HML+pulp给出 HML 的若干 vis。同一组的 vis 有统一播放按钮。
3. HML是如何与 pulp 数据联合训练的，为什么强调 HML的root-local？目前 HML 只使用了 root 和 local 数据吗，丢失了 rot6d 吗？motionstreamer272（4090的/data/public/ripemangobox/Motion/datasets/HumanML3D_272有数据，但需要检查完整性） 数据提供了 motion199 所需的所有数据。
4. 解决 4090/5090 dirty worktree 问题，必须两边都完成所有修改的保留判断，保留的修改分批次全部 commit + push，实现双边同步。
5. stage1 和 stage2 的backbone 替换实验的可视化确保放在一个 gradio 中，我在 mac 上通过 ssh -N -L 17867:127.0.0.1:7865 4090 访问。


实验整理：
1. MARDM storymotion stage2
2. ViMoGen-light storymotion clip，pulp only
3. ViMoGen-light storymotion T5，pulp only
4. stage1 redesign pulp only
5. stage1 HML-root-local + pulp

---0727 15；33
判断与结论：
1. 当前 HML 的 IK-derived rot6D 与 Pulp TRAM/SMPL 旋转不是同源观测，所以 4:136 被 Pulp mean 填充并排除出 HML supervision，这是禁止的伪造操作，训练获得的 ckpt 不能正式投入 stage2. 两个 dataset 的 rot6d 无法可靠转换吗？如果不行，根因是什么
2. md 中 setting 末尾的r2/r3/r4 指什么？
3. redesign stage1 的 HML+pulp 和 pulp只影响 human branch，几乎不影响 camera branch，是否侧面说明 stage1 redesign 的 H—C 解耦的有效性？
4. 可视化结论：
（1，核心）stage2 backbone：ViMoGen-light clip 显著胜出；
（2，核心）stage1：redesign stage1 pulp only 显著胜出，视觉质量相比 C3-25 · Stage1 没有恶化，且机制上增强了 H—C 独立可控。但 redesign stage1 和 C3-25 · Stage1 都在若干 sample 上最后一帧出现相机的明显跳动，导致 owing-camera projection 骤变。
（3，非核心，但验证 redesign stage1 的优越性，增强 OOD 能力）stage1· HML root/local，Redesign Stage1 · Pulp-only能够 zero-shot 胜任HML 上若干in-domain 动作（已经达到预期），Redesign Stage1 · HML+Pulp则做得更好。但两者都会随着时间呈现整个人的不合理的旋转（可能是由于部分 data 字段使用 pulp mean 导致）。
5. （重要，积累架构思考，写入obsidian-vault/ideas/StoryMotion/StoryMotion_Checkmate.md） 
（1）redesign stage1 的动机、依据、实现规划、结果，在遇到哪些类似问题需要留意表征设计的解耦和联合问题。
（2）为什么 ViMoGen 能够在 human motion gen 上显著胜出？其架构比其他 backbone 更适配胜任本任务的根因是什么？


---0727 17：28
检查：
1. 查看 ViMoGen CLIP context shape：
print(text_context.shape)  # [B, L, D]
若 L>1：ViMoGen 确实在做 token-level text-motion cross-attention，这很可能是显著增益来源；
若 L=1：当前增益就不能归因于细粒度词级对齐，而更可能来自 full transformer、逐层重复注入、flow objective 和调制机制。

2. ViMoGen 官方实现还有一个可选的 split_head：

先预测 local body motion；
将预测的 local motion 与 hidden feature 融合；
再预测 global motion。

其结构相当于：

x^{local}=H_{local}(h),
x^{global}=H_{global} ([h,x^{local}]).

官方代码中 local head 先输出关节旋转，再由 fusion layer 帮助 global head。

若你的 Pulp adaptation 开启了类似结构，那么它极可能是关键收益来源，因为 Pulp 中：

global root/heading 最难；
但它们可以借助已经预测出的 local pose 和动作 phase；
例如“身体已经进入迈步 phase”能帮助估计 root velocity；
“躯干正在旋转”能帮助估计 heading change。

部署实验：
2. 基于 redesign stage1 pulp only，4090 部署 ViMoGen-light clip stage2 human-only；
3. 先 git，再修改ViMoGen-light clip，适配storymotion stage2 的三模式（不影响 1 的实验）

---0728 20：16
`obsidian-vault/ideas/StoryMotion/2026-07-28_storymotion-v9-protected-h-three-stage-implementation-camera-diagnosis.md`
1. `1. 范围与术语` 的流程图是否有误：
我的理解是，stage1：
Z_H = F_H(human)
Z_C = F_C(camera)
Z_HC = F_HC(Z_H, Z_C)
我理解的 stage1 是否正确？这个设计与 pulp stage1 有差异吗？是否是这里图画错了？补充 stage1 的图。

2. 确认 140K 是健康 Direct-C endpoint，175K 出现 HC 改善／Direct-C 遗忘，189K 是两路折中点，是否保存了对应或附近的 ckpt？ 补测metric。
3. 梯度 cos 为正说明什么，是好是坏？

---0728 23：38
1. 目前 stage2 的 joint 是平行生成 H_t 和 C_t，还是 cascaded 先生成 H_0，再生成 C_0？

---0729 13:25
1. v9 stage1 的 phase B 和 phaes C的合理 loss 都应该放到 v10 的 phase B；
2. v10 的 stage2 的 human teacher 为什么需要训练？他与 v9 有什么区别？如果有区别，在 gradio 的 v10/GT/H recon/teacher页面补充v9

---0729 18：43
# 我没理解的点：
1. v9 版本的 stage1 设计会影响 stage2 直接适配 v10 版本的 camera 和 joint 吗？都使用 observed human 而不是在 joint 时候 parallel 去噪 z_h 和 z_c？如果可以，则基于 v9 的 stage2 human teacher 适配 v10 更正后的 stage2 后续阶段；

# 需要明确的点（基于 v9 stage1 和 stage2 的 human teacher）：
1. stage2的 camera/joint 训练，human 的 cfg 是否固定
2. camera48 还是 camera 64：v9 stage1 的 interaction16
3. 是否在 camera/joint training 使用 gt human 和 human teacher generated curriculum，以及是否使用置信度 condition；
4. 除了 latent loss，是否添加 human/camera 的 geo loss；
5. 四 route 训练是否需要按阶段训练。如果按阶段，需要合理添加保真 loss 来避免轮转遗忘；如果不分阶段，是否会由于前置能力不足而模型学不到东西。我更倾向于三阶段，先独立完成 direct-h 和 direct-c，然后在 joint 环节小 lr finetune learnable H 和C；

---0729 19：37
1. 为什么`formal joint 必须保留 joint-parallel`？这会直接导致 joint 崩溃甚至 stage2 崩溃；
2. latent velocity loss 和 geo loss，我打算开两个并行实验；
3. 不使用 DC3D 任何内容，除非你强烈建议则先与我敲定；
4. 其余按照建议

---0729 19：54
1. ### 1.2 Direct-C 与 joint 是否都能使用 observed Human 为什么回答 **不能。**，我看分析里写的是先 human teacher 生成 H，然后将 H 给到 direct—C，这不就是使用 observed H 吗？
2. cfg  `v_{11}` 由于流程上先 direct-h，再 direct-c，是否相当于先  `v_{10}` 再  `v_{01}`，本身没有意义（由于已经规定sequential h-c）；
3. `6.2 Stage C0-A：共享OBSERVED_H LR calibration` 是想要测试了两组 LR 的camera 收敛性吗？我建议默认直接使用 1e-4，这个实验低价值；`6.3 Stage C0-B` 和 `6.4 Stage C1` 实际组成一个 2*2 矩阵，注意选择合适lambda_geo（按照 stage1 的相对比例），5090 gpu2/3，4090 双卡 各自先训练 30K，注意 ckpt 保存；
4. `7. representation gate 与四项oracle` 我认为低价值，不必先行；

---0730 11:16
1. 既然目前 joint 采用 先 direct-h，再 diret-c，是否 stage2 就只有两个 phase了？如果是，请完成 joint 的 eval 并和 v9 对比，然后补充 human-camera-joint 的 vis（参考v9 human+camera 标签页的 Camera 210K · GT / Direct-C / joint-parallel，但每个 variant 的适配不 concat，保持一键播放）；
2. 目前最优 mainline 是 C0-LAT 吗，是否完成了 v11 的完整的 storymotion 的 stage1/2 的所有训练环节和评测？

---0730 18：46
1. v9 P3L exact Camera-phase30K 是什么 setting？
2. gradio 补充新的标签页：gt、C3-25，v9、四臂（camera 的 105K），2*3 呈现，每个视频使用类似于 `v9 Human+Camera`的GT / Direct-C / joint-parallel的 human+camera+joint的呈现，但每个视频只包含一个 variant。
3. 目前是否可说 mainline 替换为 v11的某版本？

---0721 00：51
git 同步 bite—process 和 4090/5090，将 v11 C0-LAT和 C0--geo 为共同的 mainline.
1. pulp 的视频相同尺寸，第三行其余空间可以空着；
2. 保留C0-LAT和 C0--geo 为共同的 mainline 选择，清理文档，构建新 mainline 的三模式与 baseline 的对比。
3. storymotion 核心目标：中稿 ICLR 2027。更新 `obsidian-vault/ideas/StoryMotion/StoryMotion-iclr-reliability.md`，分析为了中稿 iclr 还有哪些距离。

另外，目前剩下的实验整理（非必要，以中稿为目标）：
（1）目前 v11 的 stage1 偏复杂，如果说不出明确的设计依据，可能被审稿人 argue。之前 v10 设计了简化的 stage1 但 stage1/2 指标均退化且没找到明确的原因。
（2）还有 edit 能力没有探测与设计对应的训练阶段。

---0801 10:16
1. storymotion 在 v11 之后，计划补强的能力和重构的叙事是什么？落脚点不能在 human-camera 解耦，因为这是 ViGen 领域已经很成熟的工作，必须落到 ViGen 无法实现的更聚焦的point。data augmentation的目标是什么？storymotion 的数据处理，是否可以理解为构造合理但 unpair 的 H-C text data，从而让同一段 camera 能够处理不同的 human，以及同一段 human 能够被不同 camera 拍到？对于 storymotion 的预期和数据预期不能过于乐观，需要有降级备选。注意，由于终究是小数据小模型，因此过高的 claim+完美效果 是必然无法达成的，只要能在现有的 v11 上进一步提升 H，C，joint 质量，扩充多对多解耦控制与合理性，往 claim 靠拢（能验证方法有效性即可达到 ICLR 标准）。
1.1 目前 camera 的 human observation 是 full human motion（199），还是只有 root？两者各有利弊需注意（我更倾向于符合叙事的 human motion不一定 199 但不能只有 root）：full 能够随着 human motion 变化而不只是关注 root（否则人物朝向、动作等都被忽视是不合理的），但同时容易过拟合 ；关注 root 则丢失 human motion，称不上 director。如果是 full，在 data augment 和配对设计的新训练机制与框架上设计，希望 camera 在 multi human shot 上关注哪些 camera text 没有传达的信息（camera 可能需要同时获取 H和C的 text）
1.2 前者可以使用 humanml3d 扩充（之前已经有版本进行 pulp+hml，但后来聚焦 pulp only 最小变量先明确模型能力）；后者我不了解如何扩充。
1.3 上述扩充方案能否适配storymotion的 actor-director claim？通过data augment，有机会进一步解耦 H-C，这是目前的目的吗？数据扩充方法+扩充的数据集 自然能作为一个贡献，如果能有力支持 claim 则认可度更高。注意： pulp data 是对 movie 处理获得的，虽然不要求augment的 data 不完全按照真正导演级别的运镜设计，但要尽量贴近。
1.4 Rect-64，Rect-320，Rect-4096，A-series，B-series 分别指代什么？对于解耦控制的实验失败很正常，因为 pulp 的one-to-one 匹配限制能力上限。
1.5 数据扩充方面，我倾向于先自动化大批量构建，然后再自动化筛选，最后一步人工筛选。如果必须 manual 打标，则先提供 100 pair的 pulp 可视化 gradio（一个标签页完整呈现 25 行 4 列）供参考，包含 human motion，相机轨迹，camera projection 在同一个 video 中。
1.6 如果 pulp 的 同一个 sample（h 和c）text 各只有一个，则需要用 llm 先进行 text 同义写法扩充（如 humanml3d 多条 text 描述同一个 motion sample）。这算不上贡献，但对于提升泛化性有价值。
2. v10 stage1 简化（stage2 适配）的路线失败，v10 stage1 不如 v9 的复杂版本，根因是什么？
3. 放弃通过 MAE 的 edit 路线，这与 storymotion 的 stage2 训推架构不兼容，且 edit 特色不足；
4. 解释你在 goal 中完成的每个实验的目的和操作流程（如 N128 共享噪声）
4. gradio 标签页可视化v11 和 pulp 在修改 human/camera 后的效果（human，camera，projection），提供指标分别计算 human/camera 独立的与对应 gt的 metric（包含物理）；


2030. 有价值的下一篇想法（不保证可行性）：让 camera 能够自主判断需要聚焦 human/object/scene 的重要局部，得接 LLM，且目标更明确，因为很多时候不是局部or 全身的问题，而是自主运镜来提升叙事，可以做 ViGen。

---0801 12：35
1. stage1 与表征：
1.1 放弃 v10 的调整，之前 redesign stage1的 pulp+hml 是如何进行 hml 数据的混入的？对数据混合，独立一个md说明。
2. v9 stage1 尝试 raw human pose + camera latent variant（潜在好处是 camera 能够看到 pose root，因而提升 relatve distance 精度）：camera 从观察 human latent 变为 观察 human motion（需要评估使用 human199，还是纯 pose的 22*3=66，66 rep的root 外的 joint 是 global 还是 local rep）。但这条路线需要重新适配 stage1，如 camera concate human pose 而不是 human latent 进行 decode。这会造成 camera decode 时包含 human 的 raw 和 camera 的 latent，但我关注到 ARDY 提出了类似的 root raw + local latent 的hierarchical representation。6 组实验：
  - human199
  - human66，root + local motion
  - human66，global motion
  - Coarse-H：root、heading、height。
  - Coarse-H + oracle event time。
  - Full-H + predicted event time。
【去看 v11 的 pipeline】

2. human text 的 stage2 注入如何设计？考虑点是什么？

3. 三组实验变量：
（1）text 多样化（与 Rect 是一个含义吗）；
（2）human text 注入；
（3）stage1 human ovservation
如何在最小代价内合理找出组合最优？优先进行什么实验？避免进度回滚和返工。

4. 没理解`augmentation 不是简单扩充样本数，而是补足“Camera intent 所有权”和“Human-conditioned execution”监督`
  [
  C^*_{i,m}=\operatorname{SolveCamera}(H_i,P_m)
  ]

  即复用 Camera program (P_m)，而不是把同一条 world Camera trajectory 生硬配给不同 Human。原始 unpaired H_i + C_j 只能作为 negative/control 和人工兼
  容性诊断，不能直接成为 positive。

5. Rect 指的就是 text 丰富化吗？
6. 放在 gradio 哪个标签页？
7. 文档添加核心信息，清晰化表述但避免冗长，对缩写的实验添加说明

---0801 18：03
我来梳理目前我理解的内容：
任务优先级：
高优先：
1. 数据构造，包含RV-25（需要包含 pulp 源数据（h，c，proj），humanml3d，以及双方 text），Rect-N；（1）暂时不盲评，我先了解质量边界；（2）思考，stage1 是将 human motion 耦合到 camera的，扩充数据的目的是打破耦合，是否有冲突？（3）进行数据分组矩阵处理后，是否数据扩充不局限于 pulp 和 hml，也可以 pulp 内部组合扩充？（4）RV-25的构造原则是什么？如何筛选混合的数据以及通过筛选的标准是什么？pulp 内部组合以及 hml+pulp 跨组合标准有区别吗？
2. human text 注入 camera 分支，或许需要改为层次化、不同角色处理 camera text，human text 和 human observation（仍然使用v9 stage1 和 v11 stage2）；

低优先：
1. text 扩充；
2. stage1 pose 替换：HT0／HT1／HTS，O0–O3，N1–N3，J66-RL／J66-G，H68-HYB；

不理解内容：
1. MARDM／ViMoGen-light Human-only runs有局部改善，但三个external-style Human systems均未过strict physical gate，且没有Camera／composition输出，这是进行了额外的 train/eval 吗？
2. 实验缩写表格不完整，如 N128 缺少解释。
3. 文档优化重构，目前若干表述晦涩冗余且分布多处且缺乏符号解释（如`而不是默认每个cell都合法`的A()=1 和()=1，注意全文符号的统一避免歧义。将关闭和后置实验放到末尾，正文都是核心内容。

1. 4090 实验已完成，全量 metric eval（含物理），提供 gradio 可视化
2. RV 的具体筛选逻辑在哪里？ RV gradio 布局难以理解

---0802 17:38(待发)
1. 发现高优先级问题：pulp data对于 camera 方位描述不明确，原因是世界坐标系构建没固定。由于是从视频中处理 human 和 camera，将世界坐标系分别放到 human-camera 连线的左侧和右侧，则 camera的移动方位描述完全相反。这会导致camera的 text 与实际轨迹不匹配，导致生成和控制效果削弱。由于数据集有 16W 左右camera 数据，合理做法是根据相机具体参数的变化，将 camera text（新增，不删除原有 text）变成非歧义描述。但由于数据量大，无法通过可视化逐一判断，需设计质检手段。
2. 统计 camera 的元指令种类，


---0803 15：26
你给的解释很不清晰，不理解以下问题：
1. 我依然不不理解你说的 C0，human199 cascaded的含义，意思是从 mainline 的 human latent—>camera latent->camera trajectory 改 H128 → decode H199 → re-encode H128 → Camera ？这条路线的为什会影响 storymotion main claim？
2. 两篇 paper 的投稿 md 添加各自的 title

另外，目前剩余的核心任务应该是修正 pulp dataset 的 camera text


---0803 16：07
1. 标题采用：
paper A：StoryMotion: Preserving Human Motion Priors in Asymmetric Human–Camera Generation
paper B：DIRECT: Dual-Frame Cinematographic Intent Transfer across Articulated Human Motions

1. 目前聚焦 paper A，剩余的核心任务有 2个：pulp dataset 的 camera text 的处理，这也是 paper A 的一个贡献点。为了与 DIRECT 的贡献分离，storymotion 的数据处理只对 camera text 无歧义化，我忘了之前推荐过参考哪篇工作处理；（2）specialist 消融：独立 Human specialist 加独立 Camera specialist（stage1之前是否有在 16w 数据 train，pure 4053 eval 的可用公平可用的 stag？如果有，直接用于stage2 retrain；否则两个 stage 都 retrain）；Pulp-style symmetric joint generation；你的 protected-H + shared Camera（已完成，现有 mainline）。


---0803 18:57
specialist：
1. 后续实验没有说明，就默认 seed17；
2. `paperA_independent_conditional_camera64_stage1_210k_seed17_4090g1_20260803`是哪条 specialist？
3. 你停止的实验是否更接近 `fully separate`表述？`paperA_fully_separate_native_lat_h105k_c105k_seed17_4090g0_r2_20260803`是去掉 interaction16，因此 camera latent48 的 variant 吗？

pulp camera data：
1. trimotion 的阈值定义逻辑是什么？pulp 照搬阈值逻辑而非数值是否合理？目前临时 pulp 阈值是通过 trimotion 逻辑计算的吗？
2. trimotion 使用什么 llm 来把 camera 运动数值翻译为 short/long text？你（gpt）能否胜任？小批量和全量 16w 数据的处理？
3. 为了更好地质检和保质，下一步是先 llm 还是别的步骤？


---0804 15：59
1. NoInt-HREL 指标全线退化，且该坐标系有影响后续 camera text 的冲突风险，因此stage2 搁置；
2. C1REL 与 v9 难分上下，且坐标表示契合后续调整的 camera text，请在gpu0 部署：C1REL stage2 train，注意需要 retrain human teacher；
3. gpu1 部署 `C1REL-w/o-Interaction16` stage1.