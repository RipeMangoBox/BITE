## MoDebug
MoDebug核心思想： 显式或隐式或混合式识别motion生成结果或过程的不足,然后自适应地评估与优化（训练或training-free均可）,获得更加指令跟随的动作输出。

思考：
1. backbone应该选event-t2m这样带event level的，然后引入artifacts的localization和编辑机制来纠正artifact；还是在edit backbone上引入event机制？

code：
1. 已有
	1. TMR
2. 新增
	1. SimMotionEdit，相似度监督
	2. SALAD，attention层面的manipulation，提供一个embedding分析和操作的抓手，跳出input-output聚集局限；
	3. MotionLab，motion  edit的强基线，unified control framework，使用rf和一维ROPE（不清楚具体实现）

论文重点分析：
1. MotionCLR 如何建立attention的操作和可视化结果的关联，如何强调和去强调。指出text-motion的cross attention的高similarity区域是被关注的对齐区域，因此可以设法提高跨模态overlap区域的占比来提高alignment；
2. PartMotionEdit：body分5part+配套part similarity监督（这块的设计不make sense）+text-motion双向交互注意力
3. 

![[cb4a8359848cc78629a6e293ec17f896.jpg]]


当前任务：

P0
1. 设计并验证VLM+posefix是否能做到motion sequence与text event边界对齐；
2. 寻找text-event embedding在网络传递过程中的信号变化。
	1. 视角
		1. SALAD & MotionCLR的 attention manipulation + SimMotionEdit 的 similarity视角，分别观察text encoder和text embedding在motion generator中的传输变化（如通过similarity等方式查看语义的稀释和关注）
		2. 暂时没想到第二个，可以参考[[2026-05-08_motionfix_related_work_dataset_audit]]
	2. case
		1. 对于omission，是否某些text embedding传着传着就diminish了
		2. 对于replace，是否传着就混淆了（相似text的embedding难区分->text space的去稠密化）
		3. 对于数量错误（如steps），如何将数量添加到action unit的语义上，并明确区分？->造不同step的数据
		4. shuffle和repeat直觉上不太容易发生，暂不考虑
	3. process
		1. MVP：单event到5event都有，每个event setting各给5个sample的可视化，然后再挑选聚焦的event上限

新的similarity计算想法：
1. 想法一：对humanml3d-e进行text-motion的event对齐划分后，用TMR在每个event（所有sample的单个event 切分，以及多event组合（指full events的子集而不是自由组合）上仿照kimodo的多元automatic训练。
2. 想法二：实现motion-text的隐空间共享，将raw motion space对齐到text空间。text embedding对于不同长度的text应该是等长的（CLIP、T5、DistillBert等，但不知道Qwen或者qwen VL是不是），而motion天然是变长的，所以需要一种合理的时序表征和压缩方式来解决变长问题。比如deepphase（但我试过它不能很好地重建非周期性的text to motion的数据，还没挖掘出深层原因。）然后，将motion feature映射到text embedding（或许这里还需要对text embedding space重构或者处理）。最终我希望text embedding和motion embedding都是以event为切割单位的，对齐后，他们就能用同一个embedding对应到text和motion，也就天然能实现生成理解统一（或许使用多模态模型优于纯文本模型）。

P1
1. 数据清洗

2026-05-16 SEED/KIMODO data-first P1 shortcut：
1. 目标：先跳过 HumanML3D P0 数据质量争议，用更高质量的 SEED/KIMODO 光学动捕+人工 temporal event 标注测试 P1 的 event trace / data selection 方案。
2. 下载策略：不下载 110G 全量。先只下载 `metadata/seed_metadata_v004.parquet`、`metadata/seed_metadata_v002_temporal_labels.jsonl` 和 `soma_shapes/**`，用 metadata + temporal labels 筛选接近 HumanML3D 体量、排除 emotion-only 或非关注任务的 motion 子集。
3. Motion 表示选择：
	1. 若目标是 text-to-motion / event trace 与 HumanML3D 风格对齐，优先只下载 `soma_uniform.tar.gz`（约45GB），因为统一 skeleton 更适合跨样本训练和 baseline 对齐。
	2. 若目标转向机器人 / MuJoCo 控制，再下载 `g1.tar.gz`（约23.5GB）。
	3. 只有需要 actor body proportion 作为研究变量时才下载 `soma_proportional.tar.gz`（约45GB）；三种格式都需要时才下载约114GB全量。
4. 风险：motion 文件是 monolithic tar.gz，metadata 可以筛选 motion/category/path，但不能从 HF 按单条 motion 直接下载。筛选只能避免下载不需要的表示格式，不能避免下载所选 tar 包本身。
5. 产物：
	1. `seed_metadata_probe.json`：记录 metadata 字段、可筛选条件、许可/下载状态。
	2. `seed_event_subset_manifest.tsv`：记录选中的 `motion_id`、duration、category、event_count、temporal label coverage、chosen_representation、role。
	3. `seed_split_manifest.tsv`：按 actor / motion family / category 做 train / inference / validation 划分，避免同 actor 或近重复 motion 泄漏。

2026-05-16 MotionGPT P1 baseline：
1. 角色更新：MotionGPT 没有 event-level training，但它的 text encoder / LM 路线与 MoMask、MoGenTS 的冻结 CLIP 路线不同，因此不再作为第一组公平比较对象。它保留为 `heterogeneous_control`，用于观察 T5/LM 生成范式下 text event signal 如何保留、稀释或混淆；所有 attention / hidden state / logits 先只记为 `diagnostic`。
2. 输入条件：从 SEED/KIMODO temporal labels 构造 `full_text`、`drop_event_text`、`replace_event_text`、`count_or_duration_altered_text`。每条记录必须写明 `condition_pair`、`motion_source=seed_kimodo_metadata_selected`、`role=diagnostic`。
3. 观察层：
	1. tokenizer / prompt：event phrase 是否被截断或拆分异常。
	2. T5 encoder embedding 和 hidden states：event verb / direction / count / duration 的 norm、event-event cosine separation、full-vs-drop / replace 的分离度。
	3. decoder cross-attention：生成 `<motion_id_*>` 时每个 event phrase 的 attention mass 是否对应到 motion token 时间段。
	4. motion-token logits：full / drop / replace / count-altered 条件下 motion token 分布是否有局部响应。
4. 最小实验：先选 5 个单 event、5 个双 event、5 个三到五 event 样本；每个样本跑 4 个条件和固定 seed，输出 `trace_manifest.jsonl` 与 case card。成功口径不是 attention 好看，而是 event unit 的 text-side trace 与 motion-side temporal label 能互相支持。
5. 失败收缩：如果 MotionGPT trace 对 full/drop/replace 几乎不变，说明普通 LM baseline 对 event 不敏感，后续优先换 event-aware generator 或引入 event-conditioned adapter；不要直接做 intervention。

2026-05-16 comparable-work update：
1. Drift note：`MotionGPT-first baseline -> CLIP-family-first comparison -> heterogeneous controls`。原因是 MotionGPT 使用微调后的 T5 / LM 生成路线，而 MoMask、MoGenTS 使用冻结 CLIP 文本编码和 VQ token 生成路线；把它们直接并列解释会混淆 text encoder 差异、motion generator 差异和 event completion 差异。
2. 第一比较组：`MoMask` 与 `MoGenTS`。
	1. 共同点：两者 artifacts 已有 90 prompt 的结果与 trace 目录；text 侧同为 CLIP `ViT-B/32`，并且已有 `network_activation_rerun_20260509` 与 `network_activation_gt_paired_20260510` 的 embedding snapshots。
	2. 差异点：MoMask 是 masked motion token generator，MoGenTS 增加 spatial-temporal joint modeling。这个差异适合问“同一冻结 CLIP 条件下，生成器结构是否共同丢失 late event / count / direction 信息”。
	3. 成功口径：只在这组内比较 shared failure family，例如 `omission`、`replace`、`count/duration`、late-event weakening；不把 MotionGPT 的 T5 trace 混入主结论。
3. 第二比较组：`EventT2M` 作为 event-aware probe，而不是同构 baseline。
	1. 角色：回答 event-level conditioning 是否改善局部 event 对齐，以及是否仍存在 event completion gap。
	2. 证据限制：当前 EventT2M artifacts 多为 native output audit，`internal_attention_available=false`、`internal_activation_available=false`、`internal_logits_available=false`，所以它不能承担 model-internal trace 对比；只能承担 motion-side event completion / metrics mismatch probe。
4. 异构对照组：`MotionGPT` 与 `MoLiNGO`。
	1. 角色：验证问题是否跨越 T5/LM 风格 generator，但只作为 `heterogeneous_control`，不用于第一主张的公平机制比较。
	2. 使用方式：同一 event unit、同一 corruption 条件下记录 text-side / generation-side diagnostic；若结果相同，只能说 failure 跨范式出现，不能说机制相同。
5. 方法参照组：`SALAD`、`MotionLab`、`SimMotionEdit`。
	1. `SALAD`：作为 attention / latent manipulation 的可操作参照；当前已有 runtime readiness，不是质量结果。
	2. `MotionLab`：作为 unified generation/editing 与 flow matching 参照；当前是 asset gate / runtime 诊断，不是主比较模型。
	3. `SimMotionEdit`：作为 text-motion similarity / where-to-edit 参照，服务 event unit similarity 设计，不直接进入同构生成器比较。
6. 新执行顺序：
	1. 先用 MoMask + MoGenTS 的 CLIP-family 组，在同一批 event unit 上跑 `full_text`、`drop_event_text`、`replace_event_text`、`count_or_duration_altered_text`，输出 `clip_family_trace_manifest.jsonl` 和 case cards。
	2. 再接 EventT2M，确认 event-aware conditioning 是否缓解局部 event 对齐但仍留下 completion gap；输出 `eventt2m_completion_probe_manifest.tsv`。
	3. 最后接 MotionGPT / MoLiNGO 作为异构 sanity，检查 failure 是否跨 T5/LM 路线复现；输出 `heterogeneous_control_trace_manifest.jsonl`。
7. 关键约束：第一篇/第一阶段的 claim 只写“同一冻结 CLIP text encoder 下，多个 VQ-style generator 共享的 event completion / corruption sensitivity 问题”。EventT2M 和 MotionGPT 只能作为 probe / control，不能和 MoMask、MoGenTS 混成同一公平排序表。


补全评估：
1. 当前更新的方向是合理的：先验证“motion侧event边界是否可观测”，再追踪“text-event信号在生成过程里如何被保留、稀释或混淆”。这比直接做correction更稳，因为它先回答失败到底发生在文本解析、条件传递、motion realization，还是评估盲区。
2. 但P0的两个问题不能混成一个实验。VLM+PoseFix只能给motion-side boundary / geometry cross-check；text-event embedding追踪是model-internal diagnostic。前者证明“动作片段在哪里”，后者证明“语义信号有没有传到对应片段”，两者需要用同一批event unit对齐，但证据角色不同。
3. VLM+PoseFix目前只能作为`cross_check`，不能写成final evaluator。PoseFix对局部姿态和转向有用，但对动态速度、前后方向、exact step count不可靠；VLM对全局事件描述有用，但边界和计数需要轨迹、foot contact或人工校准支撑。已有011798 pilot可以作为当前证据入口：[[paperIDEAs/MoDebug/VLM/vlm-slice-caption-pilot-humanml3de_011798_trajectory_sanity]]。
4. SALAD / MotionCLR / SimMotionEdit的角色需要分开：SALAD更适合做traceable generator probe，因为skeleton-time latent和cross-attention可导出；MotionCLR更适合提供attention manipulation的可解释性范式；SimMotionEdit更适合作为“where to edit / similarity supervision”的设计参照，而不是直接替代event-level mechanism。
5. 现在最缺的是可复查的event unit schema、边界标注协议、trace指标定义和失败后路线收缩规则；否则后面容易把attention heatmap、VLM caption或similarity curve误写成因果证据。

缺失定义补全：
1. `event unit`：caption中一个可独立观察的动作语义单元，至少包含`event_id`、`text_span`、`action_verb`、`body_part`、`direction_or_path`、`count_or_duration`、`expected_motion_cue`。没有可观察cue的event不进入P0。
2. `event boundary`：motion中该event的可观察起止区间。边界可以先用粗粒度`start / middle / end`或秒级窗口表示，不必一开始追求frame-exact timestamp。
3. `event completion`：event不只是出现一次局部cue，而是完成text要求的动作范围，例如路径方向、turn、return、stop、count或duration中的关键约束。当前主线应优先看completion，而不是只看presence。
4. `omission`：对应event的motion-side cue缺失，或text-side event signal在生成过程中显著低于其他events。
5. `replace / wrong event`：motion-side cue存在但语义类别错，或text-side event token与相似action token的representation / attention变得不可区分。
6. `count / duration error`：动作类别正确，但repeat count、step count、hold duration或持续帧数不满足文本。这个分支需要专门构造count-controlled prompts，不应和自然caption混在一起判断。

最小验证口径：
1. Boundary口径：每个样本先给text-side event decomposition，再生成固定窗口的render / trajectory / PoseFix pair evidence。输出不是一个caption，而是`event_id -> candidate_time_window -> evidence_type -> confidence -> limitation`。
2. Trace口径：对同一批event unit导出token-level或phrase-level信号，包括text encoder embedding、cross-attention mass、time/joint-local attention、denoising sensitivity、event token与motion latent的similarity。每个信号都要能回到`event_id`。
3. Case口径：先保留`omission`、`replace`、`count/duration`三类；`shuffle`和`repeat`暂时只当sanity / stress test，不进入P0主判断。
4. 对照口径：每个case至少有`full_text`与一个corruption条件，例如`drop_text`、`replace_text`或count-altered text。不要裸写`drop=`或`full>drop`，必须写清evaluator / scorer、motion source、condition pair、n和role。
5. 成功口径：不是“attention图看起来对了”，而是motion-side boundary与trace-side event signal在同一个event unit上相互支持，并能解释至少一个可见failure family。
6. 失败口径：如果VLM+PoseFix不能稳定给boundary，就先收缩到人工边界+trace；如果trace信号不能区分success/failure，就不要做intervention，先换backbone或换可观测信号。

建议产物格式：
1. `event_units.jsonl`：每行一个event unit，记录`sample_id`、`event_id`、`text_span`、`expected_motion_cue`、`condition_pair`。
2. `boundary_manifest.tsv`：记录每个event的candidate window、motion evidence、VLM/PoseFix/trajectory/human来源、confidence和limitation。
3. `trace_manifest.jsonl`：记录每个event token / phrase在各层、各timestep、各motion window的signal。
4. `case_cards/`：每个failure case一张短卡，只写observation、evidence、limitation、next_action，不直接升级成claim。

证据角色约束：
1. VLM、PoseFix、attention map、similarity curve都只能先写成`cross_check`或`diagnostic`。
2. 只有经过独立人工校准或held-out protocol的scorer才能写成final evaluator。
3. 只有做过intervention或controlled ablation后，attention / similarity才能从相关性证据升级为机制证据。
4. SALAD denoiser runtime smoke已证明环境可跑，但只是runtime readiness，不是MoDebug方法结果：[[paperIDEAs/MoDebug/2026-05-15_salad_denoiser_runtime_smoke]]。
5. MotionLab official train/test 当前只跑到runtime / asset gate：`event-t2m`加临时overlay后能进入dataset构造，但卡在`datasets/all/new_joint_vecs/004822.npy`缺失；demo卡在`h5py`可视化依赖。这只是readiness诊断，不是MotionLab质量或MoDebug方法结果：[[paperIDEAs/MoDebug/2026-05-15_motionlab_runtime_gate_smoke]]。

下一步收缩判断：
1. 若P0-1通过，进入同一批样本的trace alignment；若不通过，先改render / trajectory / human boundary，不急着做embedding分析。
2. 若P0-2通过，才考虑training-free reweighting、attention manipulation或lightweight adapter；若不通过，MoDebug暂时定位为diagnosis / evaluator-gap paper，而不是correction paper。
3. P1数据清洗的最小范围应服务P0：只清理能支持event decomposition、boundary evidence和trace alignment的样本，不做泛化数据工程。

## IDEA2（暂时忽略）
motion-text的细粒度对齐
	细粒度特点：
		1. 【待评估，基于VLM和posefix（没时间戳）两种途径】双模态的event对齐划分；
		2. 【待观察】双模态各自的去稠密化；
		3. 【待定】对齐架构与loss设计
