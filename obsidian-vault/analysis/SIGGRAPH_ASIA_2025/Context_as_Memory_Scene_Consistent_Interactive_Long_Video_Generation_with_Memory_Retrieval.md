---
title: "Context as Memory: Scene-Consistent Interactive Long Video Generation with Memory Retrieval"
type: paper
paper_level: A
venue: "SIGGRAPH Asia"
year: 2025
pdf_ref: paperPDFs/SIGGRAPH_ASIA_2025/Context_as_Memory_Scene_Consistent_Interactive_Long_Video_Generation_with_Memory_Retrieval.pdf
code_link: null
project_link: https://context-as-memory.github.io/
aliases:
- CAM
- CAMSCILVGMR
tags:
- SIGGRAPH_ASIA_2025
- topic/generative_models_diffusion
- topic/generative_models_diffusion/diffusion_image_video
core_operator: "通过相机轨迹的视场（FOV）重叠检测，从所有历史帧中检索与当前待生成帧具有共视关系的相关帧作为上下文条件，直接将历史帧作为记忆，并与预测帧沿帧维度拼接输入，无需额外控制模块。"
primary_logic: "所有历史生成帧都可以直接作为记忆存储（无后处理），通过基于相机轨迹的FOV重叠的规则化记忆检索，高效滤除冗余和无关帧，仅将真正相关的历史帧作为条件注入生成过程，实现了长视频的场景一致性。"
claims:
- "直接存储上下文帧为记忆，无需特征嵌入或3D重建等后处理。"
- "通过帧维度拼接将上下文注入输入，无需外部适配器或交叉注意力。"
- "记忆检索通过相机轨迹的FOV重叠选择相关上下文帧。"
- "在定量评估中显著优于SOTA，最相关的ground truth比较中PSNR达20.22，LPIPS 0.3003，FID 107.18，FVD 821.37。"
---

# Context as Memory: Scene-Consistent Interactive Long Video Generation with Memory Retrieval

> [!tip] 核心洞察
> 所有历史生成帧都可以直接作为记忆存储（无后处理），通过基于相机轨迹的FOV重叠的规则化记忆检索，高效滤除冗余和无关帧，仅将真正相关的历史帧作为条件注入生成过程，实现了长视频的场景一致性。

| 字段 | 内容 |
|------|------|
| 中文题名 | 上下文即记忆：基于记忆检索的场景一致性交互式长视频生成 |
| 英文题名 | Context as Memory: Scene-Consistent Interactive Long Video Generation with Memory Retrieval |
| 会议/期刊 | SIGGRAPH Asia 2025 |
| Links | [paper](https://arxiv.org/abs/2506.03141) · [Project](https://context-as-memory.github.io/) |
| Topic | #topic/generative_models_diffusion #topic/generative_models_diffusion/diffusion_image_video |
| Method | Context-as-Memory |
| Dataset | 自采集UE5渲染数据集（含精确相机位姿）, 同上 |

> [!tip] 效果简介
> - 自采集UE5渲染数据集（含精确相机位姿） 上，PSNR↑ (Ground Truth / History Context) 为 20.22 / 18.11，对比 DFoT: 15.28 / 14.00; FramePack: 15.60 / 14.19; Random: 17.91 / 16.17; Neighbor: 15.75 / 14.47，变化 GT较最佳基线 +2.31。
> - 同上 上，LPIPS↓ (GT / HC) 为 0.3003 / 0.3414，对比 DFoT: 0.4018 / 0.4380; FramePack: 0.3935 / 0.4196; Random: 0.3302 / 0.3677; Neighbor: 0.3932 / 0.4187，变化 GT较最佳基线 -0.0299。
> - 同上 上，FID↓ 为 107.18，对比 Random: 148.25; Neighbor: 171.47; DFoT: 185.93; FramePack: 175.51，变化 优于最佳基线 -41.07。

## 概要

**瓶颈**：交互式长视频生成的核心挑战在于，现有方法（如**DFoT**，Song et al., 2025；**FramePack**，Zhang and Agrawala, 2025）在逐帧生成时只能依赖固定窗口或最近几帧的有限上下文，缺乏对长期历史信息的有效利用。当相机轨迹回到先前位置时，场景往往已发生不可逆的改变，暴露出严重的长程场景不一致问题——本质上是缺乏长期记忆能力。

**核心洞察**：该工作提出 **Context-as-Memory**，将“上下文即记忆”作为核心理念：所有已生成的历史帧直接作为记忆存储，无需任何特征嵌入或3D重建等后处理；在生成新帧时，通过基于相机轨迹的**视场（FOV）重叠检测**，从全部历史帧中高效检索出与当前帧具有共视关系的相关帧，作为上下文条件注入生成过程。

**方法定位**：与现有方法在三个关键维度上形成根本差异——（1）上下文来源从“固定窗口/最近帧”变为“基于FOV重叠从全部历史帧中动态检索”；（2）上下文注入方式从通道拼接、交叉注意力或外部适配器变为“沿帧维度直接拼接干净上下文latent与带噪预测latent，共同参与DiT的3D自注意力计算”；（3）上下文选择策略从最近帧、随机选择或分层压缩变为“FOV重叠规则检索 + 非相邻帧去冗余 + 可选远帧采样”的结构化检索流程。该方法无需额外控制模块，架构简洁。

**主要结果**：在自采集的UE5渲染数据集上，Context-as-Memory在场景记忆能力上显著优于所有基线。以ground truth帧为上下文的协议下，PSNR达20.22（较最佳基线**Random Selection**提升+2.31），LPIPS降至0.3003（改善-0.0299），FID降至107.18（改善-41.07），FVD降至821.37（改善-132.43）。消融实验证实，上下文尺寸K=20在性能与推理速度（0.97 fps）间取得较优平衡；FOV检索与非相邻帧过滤是记忆性能提升的关键驱动因素。



### 交互式长视频生成的核心挑战

交互式长视频生成要求模型根据用户实时输入（如相机轨迹）持续生成新的视频帧。其本质可形式化为流式视频生成问题：每一帧的生成以所有前序帧为条件：

$$p(x^0,x^1,...,x^n) = \prod_{i=0}^{n} p(x^i | x^0,x^1,...,x^{i-1})$$

当引入控制信号 $c$（如相机姿态）后，问题进一步扩展为可控视频生成 $p(\mathbf{x}|c)$。

然而，现有方法在实际应用中面临一个关键瓶颈：**缺乏长期记忆能力**。当相机在长轨迹中移动并返回先前位置时，生成的新帧往往与历史帧产生严重的场景不一致——原本存在的物体消失、场景布局改变。这一问题的根源在于，现有方法在生成新帧时只能依赖有限的前序帧上下文，无法有效利用长期历史信息。

### 现有方案的上下文利用策略及其局限

当前主流的交互式长视频生成方法在上下文利用上存在明显不足：

- **固定窗口/最近帧策略**：如 **DFoT**（Song et al., 2025）仅使用最近的24帧作为上下文条件。当相机轨迹较长且需要回溯时，与当前帧真正相关的历史帧早已滑出窗口范围，导致场景记忆丢失。

- **分层压缩策略**：如 **FramePack**（Zhang and Agrawala, 2025）将历史上下文帧压缩至2-3帧。虽然计算效率高，但压缩过程不可避免地丢失了大量场景细节信息，无法为场景一致性提供足够的视觉参考。

- **随机选择策略**：随机从历史帧中选取上下文帧，虽然平均意义上能获得比仅用最近帧更多的信息（Table 1中Random的PSNR为17.91，优于DFoT的15.28和FramePack的15.60），但无法保证所选帧与当前帧具有真正的视觉关联。

这些方法的共同缺陷在于：**上下文来源受限**，未能从全部历史帧中智能筛选真正相关的信息。当相机轨迹包含大幅度的空间移动和视角变化时，这一缺陷尤为致命。

### 本文动机：将历史帧直接作为记忆

本文的核心洞察是：**所有历史生成帧都可以直接作为记忆存储，无需任何后处理**。与需要特征嵌入提取或3D重建的方法不同，原始帧本身包含了最完整的场景信息。关键问题不在于存储格式，而在于如何高效地从庞大的历史帧集合中检索出与当前生成真正相关的帧。

为此，本文提出 **Context-as-Memory** 方法，核心思路是：利用相机轨迹的视场（FOV）重叠检测，从所有历史帧中检索与当前待生成帧具有共视关系的相关帧作为上下文条件。这一规则化检索策略能够高效滤除冗余和无关帧，仅将真正相关的历史帧注入生成过程，从而在长视频生成中实现场景一致性。



## 核心方法与创新机理

Context-as-Memory 的核心创新在于将交互式长视频生成重新定义为**以历史帧为显式记忆的条件生成问题**，并通过三个关键设计（changed slots）突破了现有方法依赖有限前序上下文的瓶颈。

### 1. 上下文来源：从固定窗口到全历史动态检索

现有方法普遍受限于有限的上下文窗口：**DFoT**（Song et al., 2025）仅使用最近24帧作为条件，**FramePack**（Zhang and Agrawala, 2025）将历史帧分层压缩至2-3帧。这种“近视”策略导致相机回到先前位置时，模型已“遗忘”原有场景，产生严重的场景不一致。

Context-as-Memory 将**所有历史生成帧直接存储为记忆**，无需任何后处理（如特征嵌入提取或3D重建）。在生成第 $i$ 帧时，通过记忆检索模块从全部 $i-1$ 帧历史中动态选取最相关的 $K=20$ 帧作为上下文条件。这一设计使模型能够跨越数百帧间隔，精准调用与当前视点共视的历史信息。

### 2. 上下文注入：从外部控制模块到原生帧维度拼接

现有方法通常依赖额外的控制模块注入上下文，如外部适配器或交叉注意力机制，增加了架构复杂度。Context-as-Memory 采用**沿帧维度直接拼接**的极简策略：将检索到的干净上下文 latent $\mathbf{z}^c$ 与带噪预测 latent $\mathbf{z}_t$ 在帧维度拼接后共同输入 DiT，仅通过扩散损失更新预测部分，上下文 latent 保持不变。由于基模型使用 RoPE 位置编码，可灵活适配变长序列条件，无需任何额外模块。

### 3. 上下文选择：从盲目采样到基于相机轨迹的规则化检索

上下文的质量而非数量决定了记忆效果。随机选择历史帧虽能平均获得更多信息（Table 1 中 Random 基线优于 DFoT 和 FramePack），但无法保证相关性。Context-as-Memory 提出**基于相机轨迹的 FOV 重叠检索**：

- **FOV 过滤**：通过检测两帧相机视场（四条射线）的交点判断共视关系，仅保留与当前帧存在场景重叠的历史帧；
- **非相邻帧去重**（Non-adj）：从连续帧序列中仅选取一帧作为候选，消除冗余信息；
- **远帧采样**（Far-space-time）：在候选帧中额外采样空间或时间最远的帧，补充长程信息。

消融实验（Table 3）表明，FOV 检索 + 非相邻过滤的组合带来了最显著的记忆性能提升，而远帧采样仅带来轻微增益。该检索策略无需训练，完全基于相机位姿的几何规则，高效且可解释。

### 创新本质：将“记忆”从隐式状态变为显式条件

上述三个 changed slots 共同指向一个核心洞察：**长视频的场景一致性本质上是一个记忆检索问题**。Context-as-Memory 将记忆从模型内部的隐式状态外化为可直接索引的历史帧集合，并通过几何感知的检索策略在生成时精准注入相关信息，从而在无需增大模型规模或复杂记忆模块的前提下，显著提升了长视频的场景一致性。



Context-as-Memory 的整体流水线围绕一个核心洞察构建：**所有历史生成帧都可以直接作为记忆存储，无需任何后处理**。方法将交互式长视频生成重新表述为一个记忆检索增强的流式预测问题——每一帧的生成不仅依赖最近的前序帧，而是通过基于相机轨迹的视场（FOV）重叠检测，从全部历史帧中动态检索真正相关的上下文帧，将其作为条件注入生成过程，从而在相机回到先前位置时保持场景一致性。

### 流水线总览

整个系统由四个核心模块串联构成，数据流从相机轨迹出发，经记忆检索筛选上下文，再通过帧维度拼接注入扩散 Transformer，最终输出当前帧：

1. **预训练全序列文本到视频扩散 Transformer 基模型**
   提供生成能力和图像先验。该基模型采用 3D VAE 将视频帧压缩到 latent 空间，并在 DiT（Diffusion Transformer）架构中引入 3D 自注意力机制，支持对全帧序列的联合建模。基模型使用标准扩散损失训练：
   $$\mathcal{L}(\phi) = \mathbb{E}[||\epsilon_{\phi}(\mathbf{z}_t, \mathbf{p}, t) - \epsilon||]$$
   其中 $\mathbf{z}_t$ 为加噪 latent，$\mathbf{p}$ 为文本提示条件，$\epsilon$ 为真实噪声（Eq. 1）。

2. **相机条件注入模块**
   为实现相机可控生成，方法将每帧对应的相机姿态 $\mathbf{cam}$ 通过一个轻量 MLP 编码器 $\mathcal{E}_c$ 映射为特征向量，直接加到空间注意力输出上：
   $$\mathbf{F}_i = \mathbf{F}_o + \mathcal{E}_c(\mathbf{cam})$$
   该操作在 3D 注意力之前完成，使模型学会根据相机位姿调整生成内容（Eq. 2）。带相机条件的训练损失为：
   $$\mathcal{L}_{\mathbf{cam}}(\phi, \phi_{MLP}) = \mathbb{E}[||\epsilon_{\phi, \phi_{MLP}}(\mathbf{z}_t, \mathbf{p}, \mathbf{cam}, t) - \epsilon||]$$
   （Eq. 3）。

3. **记忆检索模块（Memory Retrieval）**
   这是方法的核心创新。给定当前待生成帧的相机位姿和所有历史帧的相机位姿，记忆检索通过检测 FOV 重叠来判断哪些历史帧与当前帧具有共视关系，从而筛选出真正相关的上下文帧。检索流程包含三步过滤（详见 Fig. 3b）：
   - **FOV 重叠检测**：简化相机视场为从相机原点出发的四条射线，通过判断左右射线对的相交情况来确定两个相机视场是否重叠（Fig. 4）。该规则覆盖大多数情况，但无法处理遮挡场景。
   - **非相邻帧去重（Non-adj）**：从连续帧序列中仅选取一帧作为候选，滤除时间上高度冗余的相邻帧。
   - **可选远帧采样（Far-space-time）**：在满足 FOV 重叠的候选帧中，额外优先选择空间或时间上最远的帧，以增加上下文多样性。

   最终从筛选后的候选帧中选取最多 $K$ 帧作为上下文条件（$K=20$ 为默认设置）。该模块本质上是一个**基于规则的确定性检索算法**，无需学习参数，高效且可解释。

4. **上下文帧拼接与扩散去噪**
   检索到的上下文帧 latent $\mathbf{z}^c$（干净，无噪声）与当前待预测帧的加噪 latent $\mathbf{z}_t$ 沿**帧维度**直接拼接（Fig. 2），共同输入 DiT 进行注意力计算。在输出端，仅从预测噪声中更新 $\mathbf{z}_t$ 部分，上下文 latent $\mathbf{z}^c$ 保持不变。这种注入方式无需外部适配器、交叉注意力或特征嵌入，实现极简的条件机制。

![[assets/figures/papers/paper_list_l1497_https_arxiv_org_abs_2506_03141/figures/002_Figure_2.jpg]]
*Figure 2: Model Architecture. We concatenate the context to be conditioned and the predicted frames along the frame dimension. This method of injecting context is simple and effective, requiring no additional modules*

   为处理可变长度的上下文，方法利用基模型中的 RoPE（旋转位置编码）——预测帧保持原始位置编码，上下文帧则被赋予新的位置编码，使模型能灵活适应不同数量的上下文帧。

### 训练与推理流程

- **训练阶段**：从完整渲染序列中采样一帧作为预测目标，其余帧作为候选记忆池。通过记忆检索从候选池中选取上下文帧，与预测帧 latent 拼接后计算扩散损失，端到端训练。
- **推理阶段**：采用流式生成范式，逐帧自回归生成。每生成一帧后，将其加入记忆池。生成下一帧时，从当前记忆池中检索上下文帧，重复拼接-去噪过程。这一流程严格遵循流式视频生成的分解形式：
  $$p(x^0,x^1,...,x^n) = \prod_{i=0}^{n} p(x^i | x^0,x^1,...,x^{i-1})$$
  其中每一帧的条件集通过记忆检索从全部前序帧中动态选取，而非简单使用所有前序帧。

### 模块间关系

记忆检索模块是连接“记忆存储”和“条件注入”的关键桥梁：它将无结构的全量历史帧转化为精炼的、与当前视角相关的上下文帧集合，使得简单的帧维度拼接条件注入能够发挥最大效用。相机条件注入模块则为记忆检索提供了精确的 FOV 判断依据，两者协同实现了“相机轨迹驱动记忆检索”的闭环。

### 补充图表

![[assets/figures/papers/paper_list_l1497_https_arxiv_org_abs_2506_03141/figures/010_Figure_7.jpg]]
*Figure 7: Overview of the base text-to-video generation model. Fig. 8. Open-Domain Results*



### 3.1 基模型与扩散训练

Context-as-Memory 构建于一个预训练的全序列文生视频扩散Transformer（DiT）基模型之上。该基模型采用3D VAE将视频压缩至潜在空间，并通过3D自注意力机制建模时空依赖。其扩散训练损失为标准噪声预测损失：

$$\mathcal{L}(\phi) = \mathbb{E}\left[\left\|\epsilon_{\phi}(\mathbf{z}_t, \mathbf{p}, t) - \epsilon\right\|\right] \quad \text{(Eq. 1)}$$

其中 $\mathbf{z}_t$ 为加噪后的潜在表示，$\mathbf{p}$ 为文本提示条件，$t$ 为扩散时间步，$\epsilon$ 为真实噪声，$\epsilon_{\phi}$ 为模型预测噪声。

### 3.2 相机条件注入模块

为实现相机可控的视频生成，该方法在空间注意力输出与3D注意力输入之间插入相机条件。相机姿态 $\mathbf{cam}$ 通过一个MLP编码器 $\mathcal{E}_c$ 编码后，以残差形式加到空间注意力输出 $\mathbf{F}_o$ 上：

$$\mathbf{F}_i = \mathbf{F}_o + \mathcal{E}_c(\mathbf{cam}) \quad \text{(Eq. 2)}$$

带相机条件的扩散训练损失为：

$$\mathcal{L}_{\mathbf{cam}}(\phi, \phi_{MLP}) = \mathbb{E}\left[\left\|\epsilon_{\phi, \phi_{MLP}}(\mathbf{z}_t, \mathbf{p}, \mathbf{cam}, t) - \epsilon\right\|\right] \quad \text{(Eq. 3)}$$

### 3.3 上下文帧拼接注入

这是 Context-as-Memory 的核心条件注入方式。与现有方法使用交叉注意力或外部适配器不同，该方法将检索到的上下文帧潜在表示 $\mathbf{z}^c$ 与当前待预测帧的加噪潜在表示 $\mathbf{z}_t$ 沿**帧维度**直接拼接，共同输入DiT进行3D自注意力计算。输出时，仅更新预测部分的噪声估计，保持上下文潜在表示 $\mathbf{z}^c$ 不变。

该设计的关键支撑在于基模型使用 **RoPE**（旋转位置编码），可灵活适配变长序列的位置编码。具体而言，预测帧潜在表示 $\mathbf{z}_t$ 保留预训练阶段的原始位置编码，而新加入的上下文帧潜在表示 $\mathbf{z}^c$ 被赋予新的位置编码。

### 3.4 记忆检索模块

记忆检索是决定上下文帧选择质量的核心模块，其输入为所有已生成的历史帧及对应的相机轨迹，输出为最多 $K$ 帧（默认 $K=20$）的相关上下文帧。检索流程包含三个关键步骤：

1. **FOV重叠检测**：基于相机轨迹，通过检测两帧相机视场（Field of View）的四条边界射线是否相交来判断共视关系。实际规则要求左、右两对射线均相交，且交点不过近或过远（Fig. 4）。该规则覆盖大多数情况，偶发的遗漏或误判对整体性能影响不大。

2. **非相邻帧去重（Non-adj）**：连续相邻帧的FOV高度重叠，信息冗余严重。该过滤策略从连续帧序列中仅选取一帧作为候选，有效减少冗余。

3. **远帧采样（Far-space-time）**：在满足FOV重叠的候选帧中，额外优先选择空间或时间上最远的帧，以增加上下文多样性。消融实验（Table 3）表明，该步骤带来的增益小于FOV和Non-adj过滤。



## 实验与关键发现

### 评估协议设计

为评估长视频生成的场景记忆能力，作者提出两种互补的评估协议：

1. **Ground Truth Comparison（GT比较）**：以真实帧作为上下文条件，评估预测帧与真实帧的匹配程度。该协议直接衡量模型在理想上下文下的重建能力。
2. **History Context Comparison（HC比较）**：以模型自身生成的历史帧作为上下文，评估新生成帧与先前生成帧的场景一致性。该协议更贴近实际流式生成场景，反映误差累积下的记忆保持能力。

测试轨迹设计为“旋转n度再返回”的简单相机运动，使对应帧易于识别并进行PSNR/LPIPS计算。

### 主实验结果

在自采集的UE5渲染数据集上，Context-as-Memory在所有指标上均显著优于对比方法。

**Table 1 定量对比核心结果**：

| 方法 | PSNR↑ (GT/HC) | LPIPS↓ (GT/HC) | FID↓ | FVD↓ |
|------|---------------|----------------|------|------|
| DFoT | 15.28 / 14.00 | 0.4018 / 0.4380 | 185.93 | 1126.82 |
| FramePack | 15.60 / 14.19 | 0.3935 / 0.4196 | 175.51 | 1063.88 |
| Random | 17.91 / 16.17 | 0.3302 / 0.3677 | 148.25 | 953.80 |
| Neighbor | 15.75 / 14.47 | 0.3932 / 0.4187 | 171.47 | 1087.66 |
| **Ours** | **20.22 / 18.11** | **0.3003 / 0.3414** | **107.18** | **821.37** |

GT比较下，PSNR较最佳基线（Random）提升2.31 dB，LPIPS降低0.0299，FID降低41.07，FVD降低132.43。HC比较下趋势一致，验证了方法在真实流式生成中的鲁棒性。

**关键发现**：DFoT和FramePack仅能利用最近帧上下文，其性能甚至逊于随机选择历史帧的方法。原因在于：尽管随机选择无法保证选取有用信息，但平均而言能获取比仅学习最近上下文更多的信息量。这一结果直接验证了论文的核心瓶颈判断——长期记忆的缺失是场景一致性的关键制约。

Fig. 5的定性对比进一步印证：Context-as-Memory在相机回到先前位置时能准确还原场景细节，而其他方法均出现不同程度的场景漂移或遗忘。

### 消融研究

#### 上下文尺寸K的影响（Table 2）

![[assets/figures/papers/paper_list_l1497_https_arxiv_org_abs_2506_03141/figures/008_Table_2.jpg]]
*Table 2: Ablation of Context Size. Larger context sizes contain more useful information and lead to better memory capability, but also incur higher computational overhead, necessitating an optimal trade-off choice*

增大上下文尺寸K可持续提升记忆指标，但推理速度线性下降：

- K=1时GT PSNR仅17.36，LPIPS 0.3768；
- K=20时GT PSNR达20.22，LPIPS降至0.3003，推理速度0.97 fps；
- K=40时指标继续改善但幅度收窄，速度降至0.49 fps。

作者选择K=20作为质量与效率的平衡点。

#### 记忆检索策略消融（Table 3）

![[assets/figures/papers/paper_list_l1497_https_arxiv_org_abs_2506_03141/figures/009_Table_3.jpg]]
*Table 3: Ablation of Memory Retrieval Strategy. The filtering methods of "FOV" and "Non-adj" (where only one frame from continuous frame sequences is selected as a candidate) effectively filter out useless and redundant information, leading to significant improvements in memory capability*

消融实验逐步叠加检索策略，揭示各组件的贡献：

- **Random（无检索）**：基线，随机选取历史帧；
- **+ FOV**：仅基于FOV重叠筛选相关帧，性能大幅提升，验证了共视关系对记忆的关键作用；
- **+ Non-adj过滤**：在FOV基础上，从连续相邻帧中仅保留一帧以去除冗余，带来显著额外增益，表明冗余帧不仅浪费上下文预算，还可能稀释有效信息；
- **+ Far-space-time**：额外采样空间或时间最远的帧，带来轻微增益，但幅度明显小于FOV和Non-adj过滤。

结论：FOV检索和去冗余是记忆检索的核心有效组件，远帧采样为锦上添花。

### 开域泛化

在从互联网采集的开域图像上进行“旋转离开再返回”轨迹的生成测试（Fig. 6），方法展现出良好的记忆能力，即使生成新内容时也能在相机返回时保持场景一致性。但作者明确指出，当前方法尚不支持复杂、多样、动态的长期场景探索，无法从任意图像出发实现自由扩展导航。

### 失败模式与局限性

1. **基模型容量瓶颈**：基模型仅1B参数，在复杂轨迹上生成质量下降，长视频误差累积严重。更大规模基模型的验证仍是开放问题。
2. **遮挡处理失败**：FOV重叠检测无法处理遮挡情况，会导致部分相关帧遗漏。作者指出偶发的遗漏或误选对总体性能影响不大，但在密集遮挡场景下可能成为问题。
3. **轨迹限制**：当前方法仅针对静态相机轨迹（相机仅可在XY平面移动），未扩展到动态场景和物体变化。
4. **开域扩展受限**：在开域场景下尚不支持复杂、多样、动态的长期探索。

### 补充图表

![[assets/figures/papers/paper_list_l1497_https_arxiv_org_abs_2506_03141/figures/005_Figure.jpg]]
*Figure: Frame 5 Frame 25 Frame 45 Frame 65*

![[assets/figures/papers/paper_list_l1497_https_arxiv_org_abs_2506_03141/figures/006_Figure_5.jpg]]
*Figure 5: Qualitative Comparison Results. Among them, Context-as-Memory demonstrated the best memory capabilities and the highest visual quality, indicating the effectiveness of sufficient context information conditioning. Other methods exhibit scene inconsistency issues due to limited context utilization. Table 1. Quantitative Comparison results. Due to learning abundant context, Context-as-Memory demonstrates the best memory capabilities and highest quality of generated videos. In contrast, DFoT [Song et al. 2025] and FramePack [Zhang and Agrawala 2025], which can only utilize the most recent contexts, show relatively inferior performance, even worse than random context selection. This is because a...*



## 定位与知识库关联

### 问题定位与核心瓶颈

交互式长视频生成面临一个根本性矛盾：模型在逐帧生成新内容时，只能依赖极其有限的历史上下文。现有方法或仅使用固定窗口内的最近几帧（如 **DFoT** (Song et al., 2025) 使用24帧上下文），或将历史帧分层压缩至2-3个表征（如 **FramePack** (Zhang and Agrawala, 2025)），本质上丢弃了绝大部分长期信息。这导致场景一致性严重退化——当相机经过长轨迹回到先前位置时，场景已经面目全非。问题的本质是**缺乏长期记忆能力**，而非生成质量本身的不足。

### 因果机制：从"遗忘"到"记忆"

本文提出的 **Context-as-Memory** 方法通过一个简洁的因果链路解决了上述瓶颈：

1. **存储格式零后处理**：所有历史生成帧直接以原始帧格式存储为记忆，无需特征嵌入提取或3D重建等后处理步骤。这保留了完整的视觉信息，避免了压缩导致的信息损失。

2. **基于相机轨迹的规则化检索**：通过检测相机视场（FOV）重叠来判断帧间共视关系，从全部历史帧中筛选出与当前待生成帧真正相关的上下文帧。这一规则化方法高效滤除了冗余和无关帧，仅将有效记忆注入生成过程。

3. **帧维度拼接注入**：将检索到的干净上下文latent与带噪预测latent沿帧维度直接拼接，共同输入DiT的自注意力计算，仅更新预测部分。无需外部适配器或交叉注意力等额外控制模块。

这一设计使得模型能够"回忆"起任意久远的历史场景，从根本上解决了长视频生成中的场景遗忘问题。

### 在方法谱系中的位置

Context-as-Memory 位于**基于扩散的视频生成**与**流式自回归生成**的交叉地带，其方法定位可从以下几个维度理解：

**与流式视频生成方法的关系**：流式生成将视频分解为条件概率链 $p(x^0,x^1,...,x^n) = \prod_{i=0}^{n} p(x^i | x^0,x^1,...,x^{i-1})$，理论上每一帧以所有前序帧为条件。DFoT 和 FramePack 均属此类，但受限于上下文窗口或压缩瓶颈。Context-as-Memory 在保持流式生成框架的前提下，通过记忆检索突破了上下文数量的限制。

**与可控视频生成的关系**：该方法同时属于可控生成范畴 $p(\mathbf{x}|c)$，其中控制信号 $c$ 包含相机姿态。相机条件通过 $\mathbf{F}_i = \mathbf{F}_o + \mathcal{E}_c(\mathbf{cam})$ 注入空间注意力输出，实现了对相机轨迹的精确控制，这是记忆检索得以实施的前提。

**与基于记忆的生成方法的关系**：不同于将记忆存储为压缩特征向量的方法，Context-as-Memory 将记忆定义为原始帧本身，检索机制也非基于学习的相似度度量，而是基于几何规则的FOV重叠检测。这种设计牺牲了一定的灵活性，但换来了可解释性和零额外训练成本。

### 适用边界与关键局限

**适用前提**：
- 需要精确的相机位姿信息，当前仅在UE5渲染数据集上验证，该数据集提供逐帧的真实相机参数。
- 基模型需具备3D自注意力机制和RoPE位置编码，以支持变长帧序列的拼接。
- 记忆检索的有效性依赖于FOV重叠检测的正确性，对遮挡场景存在理论缺陷。

**已确认的局限**：
- **基模型规模限制**：当前基模型仅1B参数，在复杂轨迹上生成质量下降明显，长视频的误差累积问题严重。更大规模基模型的验证尚未进行。
- **场景动态性限制**：方法仅针对静态相机轨迹（相机仅可在XY平面移动），未扩展到包含物体运动和场景变化的动态场景。
- **FOV检索的遮挡盲区**：基于FOV重叠的记忆检索无法处理遮挡情况，会导致相关帧遗漏。论文指出偶发的遗漏或错误对总体性能影响不大，但在密集遮挡场景中可能成为瓶颈。
- **开域泛化不足**：在开域场景下，方法还不能支持复杂、多样、动态的长期场景探索，无法从任意图像出发实现自由扩展导航并保持内存一致性。

### 关键开放问题

1. **真实世界数据适配**：如何将该方法扩展到无真实相机姿态的真实世界数据集？是否需要引入视觉里程计或学习式位姿估计作为替代？

2. **上下文压缩的引入**：当前最佳上下文尺寸K=20在记忆性能与推理速度（0.97 fps）之间取得平衡。能否使用上下文压缩技术进一步降低K值，提升推理效率？

3. **动态场景扩展**：如何将记忆检索扩展到包含物体运动和场景变化的动态场景？如何处理严重遮挡导致FOV重叠失败的情况？

4. **误差累积缓解**：长视频生成中的固有误差累积如何减轻？是否可以通过记忆检索的回环修正机制来抑制漂移？

5. **规模化验证**：该方法在更大规模基模型（如10B+参数）上的表现如何？对复杂轨迹和开域设置的泛化能力是否随模型规模提升而显著改善？

### 证据强度评估

本文的核心主张均有较强证据支撑：定量实验中，Context-as-Memory 在Ground Truth比较协议下PSNR达20.22（较最佳基线Random Selection的17.91提升2.31），LPIPS降至0.3003（较最佳基线降低0.0299），FID和FVD分别较最佳基线降低41.07和132.43。消融实验系统验证了FOV检索和非相邻帧过滤的独立贡献。然而，所有实验均在自采集的UE5渲染数据集上进行，开域结果仅以定性示例呈现，方法的真实世界泛化性仍需独立验证。



## 原文 PDF

![[paperPDFs/SIGGRAPH_ASIA_2025/Context_as_Memory_Scene_Consistent_Interactive_Long_Video_Generation_with_Memory_Retrieval.pdf]]
