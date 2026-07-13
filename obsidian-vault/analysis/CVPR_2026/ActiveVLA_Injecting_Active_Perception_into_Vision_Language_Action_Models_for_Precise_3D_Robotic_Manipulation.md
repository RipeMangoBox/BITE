---
title: "ActiveVLA: Injecting Active Perception into Vision-Language-Action Models for Precise 3D Robotic Manipulation"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/ActiveVLA_Injecting_Active_Perception_into_Vision_Language_Action_Models_for_Precise_3D_Robotic_Manipulation.pdf
project_link: "https://ZhenyangLiu.github.io/ActiveVLA"
code_link: null
aliases:
- ActiveVLA
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: 主动视角选择（Active View Selection）和主动3D缩放（Active 3D Zoom-in）机制，以及粗略到精细的感知策略。
primary_logic: 通过将3D点云投影为多视角2D表示，预测热图定位关键区域，并利用多目标优化选择最佳相机视角和放大关键区域，机器人能够自适应获取高质量视觉信息，实现精确的3D操作。
claims:
- 在RLBench基准上，ActiveVLA平均成功率达到91.8%，在所有18个任务中均优于现有最佳方法BridgeVLA（88.2%），尤其在精细操作任务中表现卓越。
- 在COLOSSEUM鲁棒性基准上，ActiveVLA平均成功率为65.9%，比最佳基线BridgeVLA（64.0%）高1.9个百分点，在多种扰动下保持领先。
- 消融实验表明，固定视角基线成功率为87.6%，加入主动视角选择提升至89.4%，进一步加入主动3D缩放提升至91.8%，验证了每个模块的有效性。
- 在真实世界遮挡严重任务中，ActiveVLA整体成功率达到96.3%，相比TriVLA提升显著（例如在‘红色到绿色方块’任务提升41%）。
---

# ActiveVLA: Injecting Active Perception into Vision-Language-Action Models for Precise 3D Robotic Manipulation

> [!tip] 核心洞察
> 通过将3D点云投影为多视角2D表示，预测热图定位关键区域，并利用多目标优化选择最佳相机视角和放大关键区域，机器人能够自适应获取高质量视觉信息，实现精确的3D操作。

| 字段 | 内容 |
|------|------|
| 中文题名 | ActiveVLA：将主动感知注入视觉-语言-动作模型以实现精确三维机器人操作 |
| 英文题名 | ActiveVLA: Injecting Active Perception into Vision-Language-Action Models for Precise 3D Robotic Manipulation |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2601.08325) · [Project](https://ZhenyangLiu.github.io/ActiveVLA) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | ActiveVLA |
| Dataset | RLBench, COLOSSEUM, GemBench |

> [!tip] 效果简介
> - RLBench 上，Avg. Success Rate (%) 91.8 vs 88.2 (BridgeVLA) (+3.6)。
> - COLOSSEUM 上，Avg. Success Rate (%) 65.9 vs 64.0 (BridgeVLA) (+1.9)。
> - GemBench 上，Avg. Success Rate (%) 51.3 vs 50.0 (Previous SOTA) (+1.3)。

## 概要

机器人操作任务日益要求长周期、精细化的三维空间推理，然而现有视觉-语言-动作（VLA）模型普遍依赖静态或手腕相机，无法根据任务需求动态调整视角与分辨率，导致在遮挡严重或需精细定位的场景中感知信息严重不足。**ActiveVLA** 针对这一瓶颈，提出将主动感知注入VLA框架：通过**主动视角选择**与**主动三维缩放**两个核心机制，使机器人能够自适应地获取高质量视觉信息，从而在复杂三维操作中实现精确、鲁棒的决策。

该方法采用**粗略到精细**的两阶段策略：粗阶段将三维点云投影为多视角正交图，预测热图以定位关键三维区域；细阶段则基于该区域，通过多目标优化从候选相机中选取最佳视角，并在该视角上缩小视场以放大局部细节，最终指导末端执行器的六自由度动作预测。这一设计将VLA模型的感知从“被动接收”升级为“主动探索”，直接打通了从任务语义到精细空间感知的因果链路。

在三个主流基准上的实验结果验证了上述设计的有效性。在 **RLBench** 的18项任务中，ActiveVLA平均成功率达到 **91.8%**，较此前最优方法BridgeVLA（88.2%）提升3.6个百分点，且在10项任务上取得第一。在鲁棒性基准 **COLOSSEUM** 上，ActiveVLA平均成功率为 **65.9%**，比BridgeVLA（64.0%）高出1.9个百分点，在多种视觉与空间扰动下保持领先。在 **GemBench** 上同样达到 **51.3%**，超越此前最优结果（50.0%）。消融实验进一步揭示：固定视角基线成功率为87.6%，单独加入主动视角选择后提升至89.4%，再叠加主动三维缩放后达到最终的91.8%，两个模块各自贡献明确。真实世界遮挡任务中，ActiveVLA整体成功率达 **96.3%**，在“红色到绿色方块”等精细任务上相比TriVLA提升高达41个百分点，展现出从仿真到真实场景的强泛化能力。

在方法谱系与知识库定位上，ActiveVLA属于**三维VLA + 主动感知**的交叉方向。其基线对比覆盖了从早期行为克隆方法（Image-BC、C2F-ARM-BC）、三维操作专用架构（PerAct、Act3D、RVT及其改进版RVT-2、3D Diffuser Actor），到最新的VLA模型（BridgeVLA），以及基于预训练视觉表征的策略（R3M-MLP、MVP-MLP）。ActiveVLA在所有这些基线之上取得了一致且显著的提升，表明主动感知并非对现有架构的简单修补，而是从根本上改变了视觉信息的获取方式，为VLA模型处理复杂三维操作提供了新的范式。

### 机器人操作中的感知瓶颈

机器人操作任务，尤其是长周期和精细操作，对感知系统提出了极高要求。机器人不仅需要理解三维场景的几何结构，还必须精准定位目标物体及其可操作部位，同时应对遮挡、杂乱背景和视角受限等挑战。然而，当前主流的视觉-语言-动作（VLA）模型在这一环节存在根本性局限：它们依赖**固定或手腕安装的相机**，无法根据任务需求动态调整视角或分辨率。

这种被动感知模式导致两个直接后果。其一，当关键操作区域被遮挡或超出相机视场时，模型缺乏主动绕开障碍、寻找更佳观测角度的能力。其二，固定分辨率意味着远处的精细部件（如开关、按钮、细小抓取点）在图像中仅占极少像素，模型难以提取足够的几何细节来支撑精确的六自由度动作预测。正如 Figure 1 所示，传统 VLA 系统在“将桌上苹果拿来”这类任务中频繁失败，正是因为固定相机遗漏了关键细节或被遮挡。

### 现有方法的缺口

已有的 3D 操作策略——包括基于点云的行为克隆方法（如 **PerAct**、**Act3D**、**RVT** 系列）和基于扩散的动作生成方法（如 **3D Diffuser Actor**）——在 RLBench 等基准上取得了显著进展，但它们共享一个隐含假设：观测视角在推理阶段是固定的。这些方法将 3D 场景投影为固定正交视图或直接处理点云，缺乏对**何处需要更精细观察**的显式建模。

近期出现的 VLA 模型（如 **BridgeVLA**）尝试将视觉-语言模型的语义理解能力引入机器人操作，但其感知管道仍然沿用静态投影策略。这种“一刀切”的感知方式在需要精细空间推理的任务中暴露出明显短板：模型无法将有限的感知资源聚焦于任务关键区域，导致在遮挡严重或目标细小的场景中性能急剧下降。

### 核心洞察：从被动到主动的感知范式

ActiveVLA 的核心洞察在于：**机器人应当像人类一样，根据任务上下文主动调整自己的观察方式**。人类在执行精细操作时会自然地移动头部以避开遮挡、靠近观察以获取细节——这种主动感知能力正是现有 VLA 模型所缺失的。

为实现这一目标，ActiveVLA 引入两个关键机制。**主动视角选择（Active View Selection）**使模型能够在 3D 空间中自由放置虚拟相机，从候选视角中通过可见性、距离和多样性多目标优化选择最佳观测角度。**主动 3D 缩放（Active 3D Zoom-in）**则在选定视角上缩小视场，等效放大关键区域，在不损失几何信息的前提下提升局部细节分辨率。两者结合形成“探索-利用”的分层感知策略：视角选择负责发现最佳观测位置（探索），3D 缩放负责在该位置提取精细特征（利用）。

这一范式的技术可行性建立在 3D 点云的可重渲染特性之上：只要场景被重建为点云，就可以从任意虚拟视角合成新的观测图像，无需物理移动相机。ActiveVLA 通过粗略到精细的两阶段流程实现这一过程——首先在粗阶段定位关键 3D 区域，随后在细阶段围绕该区域执行主动感知优化，最终输出精确的操作动作。

## 核心方法与创新机理

ActiveVLA 的核心创新在于将**主动感知（Active Perception）**引入视觉-语言-动作（VLA）模型，使机器人能够根据任务需求动态调整感知策略，而非被动接受固定相机提供的有限信息。这一创新围绕三个紧密耦合的 changed slots 展开。

### 从被动接收到主动视角选择

传统 VLA 方法（如 **BridgeVLA**、**RVT-2**）依赖固定安装或手腕上的相机，视角在任务执行过程中保持不变。当目标区域被遮挡或需要精细空间推理时，这种被动感知模式会丢失关键视觉细节（Figure 1）。ActiveVLA 的**主动视角选择（Active View Selection）**机制打破了这一限制：模型首先在粗阶段通过热图定位关键 3D 区域，随后在该区域周围生成候选相机位置，并通过一个多目标评分函数——综合考虑可见性、距离和视角多样性——选择最优视角进行场景重渲染。这一过程使机器人能够“主动寻找”信息最丰富的观察角度，而非被动接受可能被遮挡或缺乏细节的固定视角。

### 从固定分辨率到主动 3D 缩放

即使选择了最优视角，固定分辨率的渲染仍可能无法捕捉精细操作所需的局部细节。ActiveVLA 的**主动 3D 缩放（Active 3D Zoom-in）**机制在选定视角上缩小视场角，等效于对关键区域进行光学放大。缩放后的视场覆盖宽度由 $W(z) = 2d \tan\left(\frac{\alpha}{2z}\right)$ 决定，其中 $z$ 为缩放因子，$d$ 为相机距离，$\alpha$ 为原始视场角。这一操作利用 3D 点云进行尺度不变的视图合成，避免了传统图像缩放带来的几何损失。缩放后的局部渲染与全局上下文特征融合，使模型同时具备全局场景理解和局部精细空间精度。

### 从端到端直接预测到粗略到精细的感知粒度

ActiveVLA 将感知过程重构为**两阶段粗略到精细（Coarse-to-Fine）策略**，改变了 VLA 模型端到端直接预测的感知粒度。粗阶段将 3D 点云投影为三个正交视图（顶、前、右），通过 PaliGemma 骨干网络生成 2D 热图，再反向投影到 3D 空间定位关键区域。细阶段则基于该区域执行主动视角选择和 3D 缩放，生成高信息密度的局部观测用于最终动作预测。这种“探索（视角选择）与利用（缩放放大）”分离的层级化感知策略，使模型能够自适应地分配计算和感知资源到任务最相关的空间位置。

上述三个 changed slots 构成了 ActiveVLA 的因果调节旋钮：主动视角选择解决了“从哪看”的问题，主动 3D 缩放解决了“看多细”的问题，而粗略到精细的感知粒度则将两者组织为高效的层级化框架。消融实验（Table 4）证实了这一因果链：固定视角基线在 RLBench 上的成功率为 87.6%，仅添加主动视角选择提升至 89.4%，进一步添加主动 3D 缩放达到最终 91.8%，验证了每个模块的独立贡献。

ActiveVLA 是一个三维视觉-语言-动作（3D VLA）框架，其核心设计动机在于解决现有 VLA 方法因固定相机视角而导致感知信息不足的问题。传统 VLA 系统在长周期精细操作中，常因相机遮挡或分辨率固定而丢失关键视觉细节，ActiveVLA 通过引入**主动感知（Active Perception）** 机制，使机器人能够根据任务上下文自适应地调整观测视角与空间分辨率。

框架采用**两阶段、粗略到精细（Coarse-to-Fine）** 策略，将感知与决策过程解耦为关键区域定位与主动感知优化两个阶段，如 Figure 2 所示。

![[assets/figures/papers/paper_list_l2178_https_arxiv_org_abs_2601_08325/figures/002_Figure_2.jpg]]
*Figure 2: The pipeline of ActiveVLA. ActiveVLA is a 3D vision-language-action framework that adopts a two-stage, coarse-to-fine strategy. In the coarse stage, three orthographic projections of the 3D scene and a language instruction are processed by the PaliGemma backbone to generate 2D heatmaps, which are then back-projected to locate the most relevant 3D region. In the fine stage, an active perception module selects new views and performs a 3D zoom-in on this region. The refined PaliGemma then predicts heatmaps for key end-effector positions, while an action decoder outputs the final 3D action*

### 粗略阶段：关键区域定位

在粗略阶段，系统首先从标定相机的 RGB-D 图像重建场景的三维点云。随后，将该点云沿顶视（top）、前视（front）、右视（right）三个正交方向渲染为多视角二维投影图像，每个视图包含 RGB、深度和世界坐标通道。渲染过程遵循公式：

$$I^{(v)}(u_x, u_y) = \sum_{i=1}^{N} \mathbf{c}_i \cdot \delta\big((u_x, u_y) - \pi^{(v)}(\mathbf{p}_i)\big)$$

其中 $\pi^{(v)}(\mathbf{p}_i)$ 将三维点 $\mathbf{p}_i$ 投影到视图 $v$ 的像素坐标，通过最近深度点处理遮挡，$\mathbf{c}_i$ 为该点的颜色。这种正交投影表示将三维场景转化为与预训练视觉-语言模型骨干兼容的二维输入格式。

三视图投影与语言指令一同送入 **PaliGemma 骨干网络**，输出 patch tokens。热图预测模块将这些 tokens 重排为特征网格，并通过凸上采样（Convex Upsampling）生成与输入图像分辨率匹配的二维热图：

$$\mathbf{H} = \mathcal{U}\Big(\mathrm{Rearrange}\big(\{\mathbf{t}_i\}_{i=1}^{M}\big)\Big)$$

这些热图标识了与任务相关的关键区域。随后，系统将多视图热图反向投影到三维空间，累积各网格点的注意力得分，从而定位出最关键的 **3D 区域**，为精细阶段提供空间先验。

### 精细阶段：主动感知优化

精细阶段以粗略阶段定位的关键 3D 区域为中心，执行两项主动感知操作：

1. **主动视角选择（Active View Selection）**：在关键区域周围的球面上，通过递归细分正二十面体生成候选相机位置，其顶点数由 $V(k) = 12 + 30k + \frac{20}{3}(4^k - 1)$ 给出。每个候选视角通过多目标评分函数评估，综合考虑可见性（沿视线采样点与最近表面的距离）、距离（相机到关键区域中心的距离）和多样性（与其他候选视角的角度分离度），加权组合为统一评分：

$$s_i = w_{\mathrm{vis}} \cdot s_{\mathrm{vis}} + w_{\mathrm{dis}} \cdot s_{\mathrm{dis}} + w_{\mathrm{div}} \cdot s_{\mathrm{div}}$$

选择得分最高的视角作为最佳观测位置。

2. **主动 3D 缩放（Active 3D Zoom-in）**：在选定的最佳视角上，缩小视场角（FoV）重新渲染场景，等效于放大关键区域。缩放因子 $z$ 下的视场覆盖宽度为 $W(z) = 2d \tan\left(\frac{\alpha}{2z}\right)$，其中 $d$ 为相机到目标的距离，$\alpha$ 为原始视场角。该操作基于三维点云实现尺度不变的视图合成，避免了几何信息损失。

这种“探索（视角选择）—利用（缩放）”的分离形成了层次化感知策略：视角选择确保从最优角度观测目标，缩放则在该角度上进一步提升局部细节的分辨率。

### 动作预测

精细阶段获得的全局上下文（粗略阶段三视图特征）与局部上下文（缩放后的局部视图特征）通过 ROI-aware 采样器提取局部 tokens，进行全局-局部特征融合。融合后的 tokens 经过 MLP 动作解码器，预测末端执行器的平移、旋转、夹爪状态和碰撞标志。平移预测通过累积三视图热图得分得到三维得分体积：

$$S(\mathbf{g}) = \sum_{v=1}^{3} w_v h_v(\pi_v(\mathbf{g}))$$

其中 $h_v$ 为视图 $v$ 的热图值，$\pi_v(\mathbf{g})$ 将三维网格点 $\mathbf{g}$ 投影到该视图。

### 输入输出流总结

- **输入**：标定相机的 RGB-D 图像 + 语言指令
- **粗略阶段输出**：关键 3D 区域的空间定位
- **精细阶段输出**：最佳相机视角 + 缩放后的局部视图
- **最终输出**：7-DoF 末端执行器动作（平移、旋转、夹爪、碰撞标志）

整个管线的设计使 ActiveVLA 能够从固定被动的感知模式升级为任务驱动的主动感知，在遮挡严重或精细操作场景中获取更高质量的视觉信息，从而提升操作精度与鲁棒性。

### 补充图表

![[assets/figures/papers/paper_list_l2178_https_arxiv_org_abs_2601_08325/figures/001_Figure_1.jpg]]
*Figure 1: Comparison between previous VLA methods and ActiveVLA. Traditional VLA systems often fail in tasks like “bring the apples on the table” because their fixed cameras miss critical details or become occluded. In contrast, ActiveVLA leverages 3D scene understanding to freely place virtual cameras and synthesize optimal viewpoints, enabling robots to adjust their view for clearer, more informative observations and thus achieve more reliable manipulation performance even under occlusion*

### 3.1 问题形式化

ActiveVLA 将视觉‑语言‑动作策略建模为映射 $\pi : (\mathbf{o}, l) \mapsto \mathbf{a}$，其中 $\mathbf{o}$ 为多模态观测，$l$ 为语言指令，$\mathbf{a}$ 为末端执行器动作。与传统 VLA 方法不同，ActiveVLA 在策略执行过程中引入主动感知机制，使观测 $\mathbf{o}$ 本身成为可优化变量——系统根据任务上下文动态选择相机视角与缩放因子，从而获取信息量更高的视觉输入。

### 3.2 多视角正交投影渲染

给定从校准 RGB‑D 相机重建的 3D 点云，ActiveVLA 首先将其渲染为三个正交投影视图（俯视、正视、右视）。对于视角 $v$，渲染图像 $I^{(v)}$ 在像素 $(u_x, u_y)$ 处的颜色由最近深度点决定：

$$I^{(v)}(u_x, u_y) = \sum_{i=1}^{N} \mathbf{c}_i \cdot \delta\big((u_x, u_y) - \pi^{(v)}(\mathbf{p}_i)\big)$$

其中 $\mathbf{c}_i$ 为点 $\mathbf{p}_i$ 的颜色，$\pi^{(v)}$ 为到视角 $v$ 的正交投影，$\delta$ 函数通过深度比较实现遮挡剔除。每个渲染视图包含 RGB、深度和世界坐标三个通道，为后续 VLM 骨干提供结构化的 3D 场景表示。

### 3.3 热图预测与关键区域定位

粗糙阶段的核心是定位任务相关的关键 3D 区域。三张正交投影图像与语言指令拼接后送入 PaliGemma 骨干，其输出的 patch tokens $\{\mathbf{t}_i\}_{i=1}^{M}$ 经重排与凸上采样生成 2D 热图：

$$\mathbf{H} = \mathcal{U}\Big(\mathrm{Rearrange}\big(\{\mathbf{t}_i\}_{i=1}^{M}\big)\Big)$$

其中 $\mathcal{U}$ 为凸上采样块，将低分辨率 token 网格映射至与输入图像分辨率匹配的热图。多视图热图随后反向投影到 3D 空间，累积各网格点的注意力得分，形成得分体积：

$$S(\mathbf{g}) = \sum_{v=1}^{3} w_v h_v(\pi_v(\mathbf{g}))$$

其中 $\mathbf{g}$ 为 3D 网格点，$h_v$ 为视角 $v$ 的热图，$w_v$ 为视角权重。得分最高的区域被确定为核心操作区，引导后续精细阶段的主动感知。

### 3.4 主动视角选择

精细阶段的核心创新在于主动视角选择（Active View Selection）。系统围绕关键区域生成候选相机位置：在关键区域中心放置递归细分的正二十面体，其第 $k$ 级细分的顶点数为：

$$V(k) = 12 + 30k + \frac{20}{3}(4^k - 1)$$

每个候选视角 $c_i$ 通过多目标评分函数评估：

$$s_i = w_{\mathrm{vis}} \cdot s_{\mathrm{vis}} + w_{\mathrm{dis}} \cdot s_{\mathrm{dis}} + w_{\mathrm{div}} \cdot s_{\mathrm{div}}$$

其中三个分项分别衡量：

- **可见性得分** $s_{\mathrm{vis}}$：沿视线方向采样点，计算与最近表面的距离 $d_k = \min_{s \in \mathcal{S}} \|q_k - s\|$，判断关键区域是否被遮挡；
- **距离得分** $s_{\mathrm{dis}}$：鼓励相机靠近关键区域以捕获细节；
- **多样性得分** $s_{\mathrm{div}}$：计算候选视角与其他已选视角的角度分离度 $S_{\mathrm{div}}(c_i) = \sum_{j \neq i} \operatorname{arccos}(\mathbf{v}_i \cdot \mathbf{v}_j)$，避免冗余视角。

评分最高的 $K$ 个视角被选中，系统从这些视角重新渲染场景。

### 3.5 主动 3D 缩放

选定最佳视角后，ActiveVLA 执行主动 3D 缩放（Active 3D Zoom‑in）：保持相机位姿不变，缩小视场角进行重新渲染。缩放因子 $z$ 下的视场覆盖宽度为：

$$W(z) = 2d \tan\left(\frac{\alpha}{2z}\right)$$

其中 $d$ 为相机到关键区域中心的距离，$\alpha$ 为原始视场角。该操作等效于在不损失几何信息的前提下放大关键区域，使局部细节在固定分辨率图像中占据更多像素，显著提升精细操作所需的感知精度。

### 3.6 全局‑局部融合与动作解码

精细阶段生成的局部上下文 tokens 与粗糙阶段的全局 tokens 拼接后，通过 MLP 头预测末端执行器的平移、旋转、夹爪状态和碰撞标志。这种全局‑局部融合设计使模型同时保持场景级理解与毫米级空间精度，是实现安全、精确 3D 操作的关键架构选择。

### 补充图表

![[assets/figures/papers/paper_list_l2178_https_arxiv_org_abs_2601_08325/figures/005_Figure_3.jpg]]
*Figure 3: Qualitative results of fine-grained manipulation tasks. Left of the dotted line (coarse stage): (a) project 3D modalities onto orthographic images, then (b) predict heatmaps to mark critical regions. Right of the dotted line (fine stage): using these regions, perform (c) active view selection and (d) active 3D zoom-in for fine-grained manipulation in complex scenes*

## 实验与关键发现

### 核心实验设置

ActiveVLA在三个主流机器人操作基准上进行了系统评估：**RLBench**（18项任务，涵盖抓取、工具使用和复杂空间交互）、**COLOSSEUM**（14种泛化扰动场景，测试鲁棒性）和**GemBench**（泛化能力评估）。主要对比基线包括传统行为克隆方法（Image-BC、C2F-ARM-BC）、3D感知方法（PerAct、Act3D、RVT、3D Diffuser Actor、RVT-2）以及VLA方法（BridgeVLA）。所有实验均以平均成功率为核心指标，其中RLBench和COLOSSEUM还报告了跨任务平均排名。

### 主结果分析

**RLBench基准（Table 1）**：ActiveVLA以**91.8%的平均成功率**在所有18项任务中达到最优，较最强基线BridgeVLA（88.2%）提升3.6个百分点。在18项任务中，ActiveVLA在10项任务上排名第一，平均排名仅1.22，显著优于BridgeVLA的2.28。这一优势在精细操作任务中尤为突出——这类任务要求精确的6D姿态推理和局部细节感知，正是主动视角选择和3D缩放机制的发力点。

**COLOSSEUM鲁棒性基准（Table 2）**：在14种视觉和空间扰动场景下，ActiveVLA平均成功率达到**65.9%**，比最佳基线BridgeVLA（64.0%）高出1.9个百分点。Table 6进一步展示了各扰动任务的具体表现，ActiveVLA在多种扰动下保持一致性高性能，验证了主动感知策略对环境变化（如光照、遮挡、相机位置偏移）的鲁棒性优势。

**GemBench泛化基准（Table 3）**：ActiveVLA取得**51.3%的平均成功率**，较此前最优方法（50.0%）提升1.3个百分点。该基准测试模型在未见场景中的泛化能力，结果表明主动感知机制有助于模型适应新环境。

**真实世界实验（Table 5）**：在四个遮挡严重的真实操作任务中，ActiveVLA整体成功率达到**96.3%**。相比TriVLA基线，在“红色到绿色方块”任务上提升高达41个百分点，充分证明了主动视角选择和3D缩放在处理真实遮挡场景时的实用价值。

### 消融实验

Table 4的消融实验揭示了各模块的贡献和代价：

- **固定视角基线**：成功率为87.6%，推理时间0.39秒。
- **+主动视角选择（A-VS）**：成功率提升至89.4%（+1.8个百分点），推理时间仅增至0.45秒。这表明动态选择最优视角能以极小的计算代价换取显著的感知质量提升。
- **+主动3D缩放（A-3Z）**：成功率进一步提升至91.8%（+2.4个百分点），推理时间增至0.56秒。缩放机制引入了额外的重渲染开销，但仍在实时性可接受范围内。

两个模块的叠加增益是累进的，且各自独立有效，不存在冗余。

### 超参数敏感性

Figure 5展示了两个关键超参数的影响：

- **主动视角数量**：从1个视角增加到3个视角时，成功率从82.2%单调提升至91.8%。视角数量的增加为模型提供了多角度的互补信息，有效缓解了单视角遮挡问题。
- **缩放因子**：从1倍增加到4倍时，性能稳步提升。更大的缩放因子等效于更高的局部分辨率，有助于精细操作中的精确位姿估计。

值得注意的是，两个参数均在当前最大值处达到最优，暗示进一步增加视角数量或缩放因子可能仍有收益，但需权衡推理时间成本。

### 失败模式与局限性

尽管ActiveVLA在各项基准上表现优异，分析仍揭示了若干潜在局限：

1. **虚拟相机与物理实现的鸿沟**：主动视角选择目前完全在3D点云的虚拟渲染空间中操作，尚未在物理机器人上实现真实相机移动。这引出一个开放问题：虚拟渲染的视角在多大程度上能代表真实相机采集的图像？当场景包含镜面反射、透明物体或复杂光照时，基于点云渲染的视角可能与真实观测存在分布差异。

2. **动态环境适应性未验证**：现有实验均在静态场景中进行，主动感知策略在移动障碍物或动态物体场景中的有效性尚待检验。在动态环境中，粗阶段定位的关键区域可能在细阶段感知时已发生变化。

3. **超参数需人工设定**：视角数量和缩放因子目前依赖人工调参，缺乏任务自适应机制。不同任务的感知需求差异显著，固定超参数可能限制模型在极端任务上的表现。

4. **未见物体类别的泛化能力**：尽管GemBench测试了场景级泛化，但模型在全新物体类别上的表现仍需进一步验证。热图预测模块依赖VLM的语义理解能力，其对训练时未见物体的关键区域定位准确性可能下降。

### 补充图表

![[assets/figures/papers/paper_list_l2178_https_arxiv_org_abs_2601_08325/figures/003_Table_1.jpg]]
*Table 1: Results on RLBench. “Avg. Rank” denotes the average rank across all 18 tasks, where a lower value signifies better overall performance. ActiveVLA attains first place in 10 tasks, highlighting its dominance in the benchmark*

![[assets/figures/papers/paper_list_l2178_https_arxiv_org_abs_2601_08325/figures/004_Table_2.jpg]]
*Table 2: Results on the COLOSSEUM Benchmark. The table presents performance across 14 generalization scenarios. ”Avg. Rank” indicates the mean ranking of each method over all perturbations, with lower values reflecting stronger overall performance. ActiveVLA surpasses the current best method by 1.9 percentage points in average success rate, demonstrating improved robustness and generalization*

![[assets/figures/papers/paper_list_l2178_https_arxiv_org_abs_2601_08325/figures/008_Table_4.jpg]]
*Table 4: Ablation study on key components. We report the success rate (%) and inference time (s) over 100 trials. A-VS (Active View Selection) dynamically acquires informative views, while A-3Z (Active 3D Zoom-in) refines local focus*

![[assets/figures/papers/paper_list_l2178_https_arxiv_org_abs_2601_08325/figures/009_Figure_5.jpg]]
*Figure 5: Success rates of ActiveVLA under different hyperparameters: (a) Number of selected views; (b) Active 3D zoom-in factor. Experiments are evaluated on the RLBench benchmark*

![[assets/figures/papers/paper_list_l2178_https_arxiv_org_abs_2601_08325/figures/010_Table_5.jpg]]
*Table 5: Success rates (%) on the Real-World Experiment. We compare our ActiveVLA with more baselines on real-world tasks. The tasks involve complex spatial occlusion and manipulation*

![[assets/figures/papers/paper_list_l2178_https_arxiv_org_abs_2601_08325/figures/011_Table_6.jpg]]
*Table 6: Success rates (%) of ActiveVLA under different perturbations in COLOSSEUM. We report mean and standard deviation over multiple trials for tasks with diverse visual and spatial perturbations. ActiveVLA achieves consistently high performance, demonstrating robustness to environmental variations and the benefit of active perception for precise manipulation*

![[assets/figures/papers/paper_list_l2178_https_arxiv_org_abs_2601_08325/figures/006_Table.jpg]]

![[assets/figures/papers/paper_list_l2178_https_arxiv_org_abs_2601_08325/figures/007_Figure.jpg]]

## 定位与知识库关联

### 1. 核心问题与因果杠杆

现有VLA模型依赖静态或手腕相机，无法根据任务动态调整相机视角或分辨率，导致在长周期和精细操作任务中感知信息不足。ActiveVLA的因果杠杆在于**主动视角选择**（Active View Selection）和**主动3D缩放**（Active 3D Zoom-in）机制，配合粗略到精细的感知策略：模型先在粗阶段定位关键3D区域，再在细阶段自适应获取高质量视觉信息，从而实现精确的3D操作。

### 2. 方法谱系与基线定位

ActiveVLA的工作建立在两条研究脉络的交汇处：**3D操作策略学习**与**视觉-语言-动作模型**。

#### 2.1 3D操作策略学习谱系

在RLBench基准上，过去数年涌现了一系列基于3D表示的端到端操作策略。早期方法如**Image-BC (CNN)** 和**Image-BC (ViT)** 直接将2D图像映射到动作，缺乏3D几何理解。**C2F-ARM-BC**引入了粗略到精细的动作预测，但感知端仍被动接收固定视角。**PerAct**通过3D体素网格和语言条件化实现了感知-动作的联合学习，**Act3D**进一步用3D特征场提升了空间精度。**RVT**和**RVT-2**将3D点云重投影为多视图2D表示，利用Transformer的高效注意力实现了当时最优的性能。**3D Diffuser Actor**则将扩散模型引入3D动作生成。

ActiveVLA在RVT/RVT-2的多视图投影范式基础上，将**被动感知升级为主动感知**：它不满足于固定正交投影，而是根据任务需求自主选择最佳虚拟相机视角，并对关键区域进行3D缩放。这一改动在RLBench上带来了91.8%的平均成功率，比当前最佳基线**BridgeVLA**（88.2%）高出3.6个百分点（Table 1），并在18个任务中的10个取得第一。

#### 2.2 VLA模型谱系

在视觉-语言-动作模型方向，**BridgeVLA**代表了将大规模VLM（如PaliGemma）作为骨干、直接预测动作的范式。ActiveVLA沿用了PaliGemma骨干，但关键区别在于：BridgeVLA等基线依赖固定相机视角或手腕相机，感知是被动的；ActiveVLA在VLM推理前插入了主动感知模块，使模型能够“主动看”。这一设计使ActiveVLA在COLOSSEUM鲁棒性基准上以65.9%的成功率超越BridgeVLA（64.0%，Table 2），在GemBench上以51.3%超越此前最优方法（50.0%，Table 3）。

#### 2.3 真实世界基线

在真实世界遮挡严重任务中，ActiveVLA与**TriVLA**等基线进行了比较，整体成功率达96.3%，在“红色到绿色方块”任务上提升41个百分点（Table 5 / part_011）。此外，**R3M-MLP**和**MVP-MLP**等基于预训练视觉表示的MLP策略也被用作基线。

### 3. 模块消融与机制验证

消融实验（Table 4）清晰验证了各模块的独立贡献：
- 固定视角基线（仅使用正交投影，无主动感知）在RLBench上成功率为87.6%
- 仅添加**主动视角选择**（A-VS）后提升至89.4%，推理时间从0.39s增至0.45s
- 进一步添加**主动3D缩放**（A-3Z）后达到91.8%，推理时间增至0.56s，仍满足实时性要求

超参数敏感性分析（Figure 5）表明：主动视角数从1增加到3时，成功率从82.2%提升至91.8%；缩放因子从1增加到4时性能稳步提升。这些结果共同证实了主动感知机制的有效性。

### 4. 适用边界与局限

尽管ActiveVLA在多个基准上表现卓越，其适用边界仍需审慎界定：

- **虚拟相机假设**：主动视角选择和3D缩放均依赖3D点云重建和虚拟渲染，当前实现未在物理机器人上验证真实相机移动的可行性。在真实世界中，相机移动可能引入运动模糊、标定误差和机械延迟。
- **静态场景假设**：方法假设场景在感知-动作循环内保持静态。在动态变化环境（移动障碍物、移动物体）中的有效性尚未验证。
- **超参数依赖**：最佳视角数量和缩放因子目前需人工设定，缺乏自动适应不同任务的机制。
- **未见泛化**：在全新物体类别和场景中的泛化能力需要进一步评估，当前实验主要覆盖RLBench和COLOSSEUM的已知任务分布。

### 5. 开放问题

1. 主动视角选择策略能否从虚拟渲染迁移到物理相机的实际移动？涉及实时3D重建、相机路径规划和伺服控制等工程挑战。
2. 如何自动确定最佳视角数量和缩放因子，使模型能够根据任务复杂度自适应调整感知资源？
3. 在动态环境中（如移动障碍物或人机协作场景），主动感知策略需要何种扩展以保持鲁棒性？
4. 主动感知带来的额外推理成本（0.56s vs 0.39s）在需要更高频率控制的接触式操作任务中是否可接受？

## 原文 PDF

![[paperPDFs/CVPR_2026/ActiveVLA_Injecting_Active_Perception_into_Vision_Language_Action_Models_for_Precise_3D_Robotic_Manipulation.pdf]]
