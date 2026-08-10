# StoryMotion Contributions Review

我的总体判断是：第 1、2 条方向正确，但当前表述仍过于接近 PulpMotion；第 3 条可以成为独立贡献，
但必须经过严格的“数据质量—模型控制能力”双重验证；第 4 条只能作为结果性贡献，且在本地可用数据
范围与官方训练范围不完全一致时，不能现在就冻结成无条件的 `consistent SOTA`。

1）PulpMotion 已经提出 text-conditioned human–camera joint generation，其第一条贡献本身就是
“a unified framework that jointly generates human motion and camera trajectories”；方法上又采用
joint/shared latent space，并通过 on-screen framing 辅助模态增强联合一致性。因此，StoryMotion
如果继续使用泛化的 “unified framework + joint representation + joint generation” 三个词组，
容易被审稿人理解成“换了一套架构重新做 PulpMotion 的问题”，而不是解决了一个新的核心矛盾。
[Pulp Motion][1]

StoryMotion 更强、也更独特的主线应当是：**在保持强 Human marginal 的前提下，实现有向的
Human→Camera coupling，并在同一 checkpoint 中覆盖三个条件接口。** 这直接回应了 PulpMotion
自己暴露出的局限：其附录观察到，dual-modality generation 往往提高跨模态一致性，但会牺牲
modality-wise performance。StoryMotion 的目标不是再次证明“联合比独立更一致”，而是解决
“如何在耦合 Camera 的同时，不损伤 Human generation”这一 quality–coherence trade-off。
[Pulp Motion][1]

True-P2 matched symmetric formal使这个动机需要更精确：不能再写成“Camera supervision经验上必然
损害Human指标”。允许Camera loss更新Human后，P2的Direct-H与sequential Human geometry反而改善，
但Direct-C以及sequential Camera semantic／framing显著回退。因而StoryMotion更可信的价值是提供
**可验证的Human ownership不变量，并保持一个可用的observed-H／generated-H Camera接口**；不是声称
所有symmetric joint optimization都会让Human数值变差。P1 HREL只是同evaluator secondary control，
严格factorization因果结论仍需与P2 exact初始化匹配的C0-LAT同协议reference。

对于第三个接口，审稿人说“joint generation 只是前两者的组合”并不完全错，但这不构成致命问题。
你应当主动承认其有向因子分解，而不是试图把第三个模式包装成完全独立的生成原语。当前三个接口
可以严格写成：

$$
\text{Direct-H:}\qquad
\hat H\sim p_\theta(H\mid T_H),
$$

$$
\text{Observed-H Camera:}\qquad
\hat C\sim p_\theta(C\mid H_{\mathrm{obs}},T_C),
$$

$$
\text{Sequential H--C Generation:}\qquad
\hat H\sim p_\theta(H\mid T_H),\qquad
\hat C\sim p_\theta(C\mid \hat H,T_C).
$$

因此第三种模式对应的联合分布是：

$$
p_\theta(H,C\mid T_H,T_C)
=p_\theta(H\mid T_H)\,p_\theta(C\mid H,T_C).
$$

这在概率意义上当然属于 joint generation，只是它是**有向、非对称、顺序因子化的 joint generation**，而不是 PulpMotion 那种同时建模并共同采样 (H,C) 的对称联合生成。你目前冻结的是先完整生成 Human，再将最终 Human 固定为 Camera 条件的 two-pass inference，因此正文中不要写 “simultaneously generates” 或 “joint sampling”。最准确的术语是：

* `sequential human–camera pair generation`
* `asymmetric human–camera co-generation`
* `generated-motion-conditioned camera generation`

其中我最建议贡献点使用 `sequential human–camera pair generation`，实验表格中为了和现有工作对齐，可以写成 `Joint / Generated-H→C`。

这里还需要澄清一个概念：Camera generator 本身不是只能“吃 GT Human”。它接受的是任意 Human trajectory；只是在 Direct-C 协议下输入来源是 observed/GT Human，而在 Sequential 协议下输入来源是模型生成的 Human。两者的区别不是 Camera branch 的函数形式，而是条件变量的来源：

$$
H_{\mathrm{obs}}\sim p_{\mathrm{data}}(H)
\quad \text{versus}\quad
\hat H\sim p_\theta(H\mid T_H).
$$

后者包含 Human generation error、分布偏移和样本不确定性，因此必须单独评估。也就是说，三种模式是三个必要的**任务与评测接口**，但不应被描述成三个彼此独立的算法模块。更准确的叙述是：StoryMotion 包含两个可复用生成算子 $G_H$ 和 $G_C$，通过不同组合暴露三个接口。

第一条贡献可以改成：

> **We present StoryMotion, a single-checkpoint asymmetric framework that supports three complementary human–camera generation interfaces: text-to-human motion generation, camera trajectory generation conditioned on observed human motion, and sequential human–camera pair generation from separate human and camera descriptions. In the last setting, the camera is conditioned on model-generated rather than ground-truth human motion.**

这里的 `single-checkpoint asymmetric framework` 比单纯的 `unified framework` 更有辨识度。要让这条贡献成立，实验上至少需要证明四件事：三个接口确实来自同一 checkpoint；Camera 训练前后 Direct-H 输出逐元素不变或指标不退化；Generated-H→C 与 GT-H→C 分开报告；加入“两个独立模型串联”的 pipeline baseline，以证明 StoryMotion 不只是把一个 Human model 和一个 Camera model放在同一个代码仓库里。

2）关于第二条贡献，`human-dependent camera learning` 并没有价值观上的负面含义，但技术表达不够好。`dependent` 容易让人理解为 Camera 缺少自身可控自由度，也没有说明依赖是条件建模、几何依赖还是统计相关。更标准的表达是：

* `human-conditioned camera generation`
* `human-aware camera modeling`
* `directed Human→Camera coupling`

其中方法贡献中最好使用 `directed Human→Camera coupling`，任务名称中使用 `human-motion-conditioned camera generation`。

我也不建议继续叫 `human-camera joint representation`。PulpMotion 本身已经使用 shared multimodal latent space 和 joint autoencoder；你再强调 “joint representation”，反而模糊了两者最重要的差异。PulpMotion 的核心倾向是通过共享和辅助 framing 加强联合一致性，而 StoryMotion 的核心倾向是通过**显式所有权分解**实现“需要耦合的部分耦合，不应受 Camera 影响的 Human 部分完全隔离”。[Pulp Motion][1] Stage 1 的实际结构更适合称为：

* `human-anchored factorized representation`
* `human-anchor interaction representation`
* `factorized human–camera latent representation`

其中第一种最完整。你的表征实际上包含 Human-only latent (z_h)、Human–Camera interaction residual (z_{hc}) 和 Camera-specific component (z_c)。Human decoder 只读取 (z_h)，Camera/framing decoder读取 ([z_h,z_{hc},z_c])；Stage 2 又延续了同样的非对称所有权：Human route 图隔离，Camera route读取 observed 或 generated Human。因而真正的贡献不是“一个 joint latent”，而是：

$$
\underbrace{z_h}_{\text{Human owner}}
\quad+\quad
\underbrace{z_{hc}}_{\text{interaction}}
\quad+\quad
\underbrace{z_c}_{\text{Camera-specific}}.
$$

并满足：

$$
\hat H=D_h(z_h),
\qquad
(\hat C,\hat F)=D_c(z_h,z_{hc},z_c),
$$

从架构上实现 $C\nrightarrow H$ 和 $H\rightarrow C$。

第二条可以改成：

> **We introduce a human-anchored factorized representation together with a protected dual-stream generator. The representation separates a human-only latent, a compact human–camera interaction residual, and a camera-specific latent; correspondingly, the human route is isolated from camera inputs and supervision, while the camera route conditions on human motion and interaction features. This design enables directed Human→Camera coupling while preserving the human-motion marginal.**

这里建议使用 `preserving the human-motion marginal`，而不是泛泛的 `preserving a strong human prior`。前者对应可验证的数学与工程性质：Camera branch 的训练不改变 (p_\theta(H\mid T_H))。在摘要或更易读的地方，可以写成 `without degrading human-only generation quality`。

还要严格区分两种“解耦”：

第一种是**结构解耦或 latent ownership**：Human latent 不受 Camera 影响，Camera-specific latent 与 interaction latent 被单独表示。这是 Stage 1 和 Stage 2 架构赋予的。

第二种是**语义可控性解耦**：在固定 Human 时，仅修改 Camera text，Camera 能按照 trucking、dolly、orbit、方向、速度、时间段等要求变化，同时 framing 仍合理。这主要依赖 Camera text supervision 和 Stage 2 的 text-to-latent mapping，不能仅由 Stage 1 representation 自动保证。

尤其 Stage 1 本身不使用 Camera text，因此 Pulp++ 不会“改善 Stage 1 representation”；它能做的是让 Stage 2 更准确地把 Camera text 映射到 (z_{hc},z_c) 中可供控制的自由度。更严谨的因果表述应是：**Stage 1 提供结构上可分离的控制载体，Pulp++ 提供能够识别这些自由度的语义监督。**

另外，若要在贡献中使用 `factorized` 或 `disentangled`，最好补充 latent intervention 证据。仅有重建指标还不足以证明 (z_{hc}) 和 (z_c) 真正承担不同语义。至少应展示固定 (z_h) 后交换或改变 (z_c)、(z_{hc}) 的结果，以及各 latent 被移除后的 Camera、framing 和 Human 重建变化。在证据不足前，使用 `factorized` 是安全的，使用 `disentangled` 风险更大。

3）Pulp++ 如果效果成立，完全可以成为第三条贡献，但它必须被定义成**一个几何约束明确、可审计的 Camera annotation correction and enrichment**，而不是“我们用 LLM 把 caption 写得更丰富”。原始 PulpMotion 的 Camera caption 本来就是先进行 motion tagging，再输入 LLM 生成自然语言，因此单纯换模型、扩写句子或增加描述长度不会形成明显新意。[Pulp Motion][1] 至少要体现以下方法差异：明确 Camera direction 所属坐标系，消除 world-left/right、camera-local left/right 和 human-relative left/right 的混用；将长序列分解成有时间边界的 Camera primitive；区分 static、follow、truck、dolly、orbit、crane 等运动；对方向、强度、速度和时间顺序提供几何可验证标签；对无法确定的样本保留 unknown/quarantine，而不是让 LLM 猜测。LLM 最多负责把已经由几何程序确定的结构化标签 verbalize 成自然语言。

如果最终只修改 Camera text，而不改变 Human motion、Camera trajectory 或样本内容，我不建议正式名称继续使用宽泛的 `Pulp++`。更准确的名称可以是 `PulpMotion-CamText` 或 `PulpMotion-CT`。这样不会让人误以为你重建了整个 PulpMotion 数据集，也更容易说明贡献边界。

Pulp++ 是否能进入 contribution，应设置以下五个门槛：第一，人工分层审计证明新文本在方向、primitive、时间顺序和轨迹一致性上显著优于原文本；第二，在完全相同的 sample IDs 和 trajectories 上，固定模型后仅替换 Camera text，Camera control 指标稳定提升；第三，framing、out-of-screen、Camera realism 和 Human metrics不发生有意义退化；第四，收益至少能在 StoryMotion 和一个重训的 PulpMotion baseline 上出现，避免被认为是为自家模型定制的数据；第五，至少能公开 annotation、sample manifest 和构造代码，即使不能重新分发原始资产。

最可信的实验不是简单比较 “Original PulpMotion published result” 与 “StoryMotion trained on Pulp++”，而是做一个严格的 $2\times2$ 设计：

|                      | Original camera text | Pulp++ camera text |
| -------------------- | -------------------: | -----------------: |
| Retrained PulpMotion |             (M_0D_0) |           (M_0D_1) |
| StoryMotion          |             (M_1D_0) |           (M_1D_1) |

其中 (M_1D_0-M_0D_0) 是模型设计带来的收益；(M_0D_1-M_0D_0) 和 (M_1D_1-M_1D_0) 是数据监督带来的收益；还可以通过

$$
\Delta_{\mathrm{interaction}}
= (M_1D_1-M_1D_0) - (M_0D_1-M_0D_0).
$$

判断 StoryMotion 的 factorized representation 是否比基线更善于利用高质量 Camera text。这样，你就可以非常清楚地写：Human–Camera coherence 主要来自表示与架构，Camera-text controllability 主要来自 Pulp++，两者是否存在协同作用则由 interaction term 决定。

Pulp++ 的可信度不能只依赖 CLaTr-Score。原始 evaluator 可能无法识别更细粒度的新描述；重新训练一个 evaluator 又可能造成“用自己的标注训练自己的评估器”的循环论证。建议保留官方 evaluator 用于 original benchmark comparability，同时在 Pulp++ test 上增加几何可计算的 primitive、direction、temporal-order、speed-bin accuracy，以及一个人工核验的 sealed subset。Pulp++ 的核心结果应是“控制指令是否被执行”，而不是仅仅“新 caption 与新 evaluator 的 embedding 更接近”。

4）本地可用训练集为 162,760 条，而 PulpMotion 论文报告整个数据集约 193K samples，因此“数据范围减少”和“Camera text 修正”必须在实验中被拆成两个正交变量。[Pulp Motion][1] 审稿人不会仅仅因为你没有拿到全部数据而抵触；真正的问题是无法判断提升究竟来自模型、筛选后的较容易样本，还是修改后的标签。

建议把原论文公开结果作为单独的 `Published, full-data setting` 行，并用符号注明其训练数据不同，不参与严格显著性比较；然后在 162,760 条 matched available-data cohort 上同时重训 PulpMotion 和 StoryMotion，作为受控 architecture comparison。这里的 162,760 是原始 `ae_train_split.txt` 173,912 条中能够物化全部必要文件的完整交集，也是 StoryMotion 当前 Stage2 的完整训练集，不是 StoryMotion 的更小子集；PulpMotion 与 StoryMotion 的 train/eval ID 集已审计为 exact `162,760/4,053`、集合差异为 0。Pulp++ 实验继续固定这 162,760 个 sample IDs，只替换 Camera captions。还应发布具体 ID manifest，并报告该 cohort 与论文公开训练范围在 sequence length、Camera primitive、Human action 和 caption length 上的分布差异。不要在论文中使用“redefine PulpMotion”或含糊的 `common-subset`，使用 `controlled matched available-data protocol` 更准确。

因此，审稿可信度可以分成三层：

* 官方测试集、官方文本、官方评估代码：用于与既有工作比较。
* 相同 162,760 条 matched available-data 训练数据上的重训结果：用于受控比较 StoryMotion 与 PulpMotion；representation、decoder 与 generation mode 仍不相同，因此不能仅凭同 cohort 声称单变量架构优越。
* 相同 IDs、不同 Camera captions 的 Pulp++ 结果：用于证明数据修正带来的控制能力提升。

只要三层不混在同一张无说明的表里，数据双重变化不会成为硬伤；相反，$2\times2$ 因果拆分会让实验设计显得很严谨。

自由编辑不建议加入正式contribution列表。最稳妥的定位是一个optimizer-free compositional utility
stress test：参考[[analysis/CVPR_2025/Dynamic_Motion_Blending_for_Versatile_Motion_Editing|MotionCutMix]]，
在raw motion中用hard replacement＋边界SLERP构造上／下半身组合，
只保留经kinematic和view-space framing检查后仍与原Camera有效配对的样本，再重算pair-dependent
Interaction16。它回答“Camera branch能否处理受控composite Human”，而不是宣称任意Human text与
Camera text都可自由替换。若该screen失败，再单独授权冻结Human的Camera-branch augmentation；在此之前
把editing写成主贡献会稀释human-preserving sequential generation的核心定位。

5）第四条 `StoryMotion achieves consistent SOTA on PulpMotion benchmark for ...` 目前也需要降一档表述。PulpMotion 原论文主要把任务定义为 $p(H,C\mid c)$ 的联合生成，并把 human-conditioned camera generation 作为比较基线之一，而不是正式宣布 Human-only、Observed-H Camera、Joint 三个官方 benchmark tracks。[Pulp Motion][1] 因此应写：

> `across three evaluation protocols on PulpMotion`

而不是：

> `across three PulpMotion benchmark tracks`

此外，`consistent SOTA` 通常暗示主要指标几乎全面领先，而且训练数据、评估代码和随机采样预算可比。考虑到 Human quality、Camera text alignment、Camera trajectory fidelity、framing coherence 和 diversity 往往存在冲突，更贴合 StoryMotion 核心主张的结果表述是：

> **StoryMotion establishes a stronger quality–coherence Pareto frontier across three evaluation protocols on PulpMotion, preserving human-only generation quality while improving observed-motion-conditioned camera generation and sequential human–camera pair generation.**

最终如果主要指标确实全面超过现有结果，再升级为：

> **StoryMotion achieves state-of-the-art overall performance across three controlled evaluation protocols on PulpMotion.**

若你使用 162,760 条 matched available-data cohort 却超过了 PulpMotion 使用更完整数据得到的公开数字，可以写：

> `outperforms the published results despite using a reduced training subset`

但严格统计显著性仍应建立在 matched available-data cohort 的重训结果上，而不是跨不同训练数据直接计算；若 representation、decoder 或 mode 不同，还必须把结论限制为 system comparison。

综合下来，在 Pulp++ 尚未确认前，我建议先冻结下面三条：

> **1. We present StoryMotion, a single-checkpoint asymmetric framework that supports three complementary human–camera generation interfaces: text-to-human motion generation, camera trajectory generation conditioned on observed human motion, and sequential human–camera pair generation from separate human and camera descriptions. In the last setting, the camera is conditioned on model-generated rather than ground-truth human motion.**
>
> **2. We introduce a human-anchored factorized representation together with a protected dual-stream generator. The representation separates a human-only latent, a compact human–camera interaction residual, and a camera-specific latent; correspondingly, the human route is isolated from camera inputs and supervision, while the camera route conditions on human motion and interaction features. This design enables directed Human→Camera coupling while preserving the human-motion marginal.**
>
> **3. Across three controlled evaluation protocols on PulpMotion, StoryMotion establishes a stronger quality–coherence Pareto frontier for human generation, observed-motion-conditioned camera generation, and sequential human–camera pair generation.**

如果 Pulp++ 达到上述门槛，则变成四条：

> **1. We present StoryMotion, a single-checkpoint asymmetric framework that supports text-to-human motion generation, observed-motion-conditioned camera generation, and sequential human–camera pair generation from separate human and camera descriptions.**
>
> **2. We introduce a human-anchored factorized representation and a protected dual-stream generator that enable directed Human→Camera coupling while preserving the human-motion marginal.**
>
> **3. We introduce PulpMotion-CamText, a geometry-grounded correction and enrichment of PulpMotion camera descriptions, with explicit coordinate-frame semantics and temporally localized camera attributes, while leaving the underlying human motions and camera trajectories unchanged.**
>
> **4. Controlled experiments on both the original and revised annotations disentangle architecture and supervision effects: StoryMotion improves human–camera coherence under fixed data, while the revised camera supervision improves camera-text controllability without degrading human generation or framing quality.**

这套表述与 PulpMotion 的差异会非常明确：PulpMotion 的主语是**通过 shared latent 和 auxiliary framing 提高 simultaneous joint generation coherence**；StoryMotion 的主语则是**通过 human-anchored factorization 和 protected asymmetric routing，在不损伤 Human marginal 的条件下覆盖 observed-H 与 generated-H 两种 Camera generation 场景**。Pulp++ 若成功，则补上“结构可分离”到“文本可控制”之间缺失的监督环节，而不是被混在 representation 的功劳里。

[1]: https://arxiv.org/html/2510.05097v2 "Pulp Motion: Framing-aware multimodal camera and human motion generation"
