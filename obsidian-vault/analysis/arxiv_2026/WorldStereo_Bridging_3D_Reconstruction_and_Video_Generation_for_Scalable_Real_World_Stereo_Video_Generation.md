---
title: "WorldStereo: Bridging 3D Reconstruction and Video Generation for Scalable Real-World Stereo Video Generation"
type: paper
paper_level: A
venue: arXiv
year: 2026
pdf_ref: paperPDFs/arxiv_2026/WorldStereo_Bridging_3D_Reconstruction_and_Video_Generation_for_Scalable_Real_World_Stereo_Video_Generation.pdf
project_link: null
code_link: https://github.com/FuchengSu/WorldStereo
aliases:
- WorldStereo
tags:
- arxiv_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
core_operator: 全局几何记忆（GGM）通过增量更新的点云提供粗粒度结构先验，空间立体记忆（SSM）利用三维对应约束注意力实现细粒度纹理一致性。
primary_logic: 基于预训练视频扩散模型的泛化能力，通过即插即用的几何记忆模块和分布匹配蒸馏（DMD）实现高效、高质量的多视角一致视频生成与三维重建，无需联合训练即可加速。
claims:
- WorldStereo通过两个专用的几何记忆模块桥接摄像机引导的视频生成与三维重建。
- 全局几何记忆增量更新点云条件，为多视频生成提供全局三维先验。
- 空间立体记忆通过检索参考视图并限制注意力于3D对应区域，恢复细粒度细节。
- OOD Camera Control (WorldScore) 上 RotErr = 0.132 (WorldStereo*)
---

# WorldStereo: Bridging 3D Reconstruction and Video Generation for Scalable Real-World Stereo Video Generation

> [!tip] 核心洞察
> 基于预训练视频扩散模型的泛化能力，通过即插即用的几何记忆模块和分布匹配蒸馏（DMD）实现高效、高质量的多视角一致视频生成与三维重建，无需联合训练即可加速。

| 字段 | 内容 |
|------|------|
| 中文题名 | WorldStereo：连接三维重建与视频生成实现可扩展的真实世界立体视频生成 |
| 英文题名 | WorldStereo: Bridging 3D Reconstruction and Video Generation for Scalable Real-World Stereo Video Generation |
| 会议/期刊 | arXiv 2026 |
| Links | [paper](https://arxiv.org/abs/2603.02049) · [Code](https://github.com/FuchengSu/WorldStereo) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion |
| Method | WorldStereo |
| Dataset | OOD Camera Control, 3D Reconstruction, Inference Efficiency |

> [!tip] 效果简介
> - OOD Camera Control (WorldScore) 上，RotErr 0.132 (WorldStereo*) vs 0.155 (Uni3C) (-0.023 (↓14.8%))。
> - 3D Reconstruction (Tanks-and-Temples) 上，F1-Score 0.578 (WorldStereo-Full) vs 0.424 (Uni3C) (+0.154 (↑36.3%))。
> - Inference Efficiency 上，Time (sec) 9 (WorldStereo-DMD) vs 162 (WorldStereo*) (-153s (↓94.4%))。

## 概要

### 1. 问题背景与瓶颈

从稀疏图像输入重建高质量三维场景是计算机视觉的核心挑战。现有摄像机引导的视频扩散模型（VDM）虽能生成符合指定轨迹的动态内容，但将其直接用于三维重建时面临根本性瓶颈：**多视角生成缺乏几何一致性**。由于模型缺乏对场景全局几何结构的记忆能力，不同轨迹生成的视频在重叠区域往往出现纹理错位、结构漂移，导致后续重建结果模糊、细节丢失。这一瓶颈的深层原因在于，纯摄像机条件仅提供逐帧的局部视角约束，无法传递跨轨迹的全局三维先验。

### 2. 核心方法思想

**WorldStereo** 提出了一种即插即用的几何记忆增强框架，在不修改预训练VDM主干的前提下，通过两个互补的记忆模块桥接视频生成与三维重建：

- **全局几何记忆（Global-Geometric Memory, GGM）**：将生成视频的帧通过深度估计反投影为点云，增量更新为全局点云条件 $X_{pcd}^g = [X_{pcd}, \hat{X}_{pcd}]$，为多轨迹生成注入粗粒度的三维结构先验，确保场景布局的全局一致性。

- **空间立体记忆（Spatial-Stereo Memory, SSM）**：从记忆库中检索空间相似的参考视图，将目标帧与参考帧水平拼接并融入点图（pointmap）编码的三维对应信息，通过重构注意力张量限制每个目标-参考对仅关注自身特征，从而恢复细粒度纹理一致性。

两个模块协同工作：GGM提供“骨架”，SSM填充“血肉”。此外，WorldStereo利用像素对齐的ControlNet注入特性，通过分布匹配蒸馏（DMD）将40步去噪生成器蒸馏为4步DiT，实现约**20倍推理加速**，且无需对记忆模块进行联合训练。

### 3. 方法定位

WorldStereo在视频生成范式谱系中属于**多轨迹记忆增强型（Multi-Bi-Mem）**方案（见表1）。与单次生成长轨迹的VDM（Long-Bi VDM）和自回归逐帧生成（AR模型）不同，WorldStereo基于强大的开源预训练VDM，通过互补视角的多轨迹生成与记忆机制实现集成式三维重建，兼具泛化能力与生成效率。

在知识库定位上，WorldStereo处于**摄像机引导视频生成**与**三维重建**的交叉地带。其基线方法**Uni3C**提供摄像机ControlNet分支的基础架构；与端到端三维生成方法（如**Voyager**、**Lyra**）和摄像机引导生成方法（如**SEVA**、**Gen3C**）相比，WorldStereo的独特贡献在于通过几何记忆模块将视频扩散模型的泛化能力迁移到三维一致性问题，而非重新训练专用三维生成模型。

### 4. 关键结果预览

- **摄像机控制精度**：在OOD WorldScore基准上，WorldStereo-full的旋转误差（RotErr）为0.132，较基线Uni3C（0.155）降低14.8%；DMD蒸馏版本在保持控制精度的同时将推理时间从162秒压缩至9秒。

- **三维重建质量**：在Tanks-and-Temples数据集上，WorldStereo-full的F1-Score达到0.578，较Uni3C（0.424）提升36.3%，重建点云显著更完整、噪声更少。

- **记忆模块消融**：GGM将PSNR从14.64提升至17.45，SSM进一步推至18.40；LPIPS从0.412降至0.283。定性结果显示GGM捕捉粗粒度结构但丢失细节，SSM配合点图能显著恢复与参考帧一致的纹理。

### 5. 局限与开放问题

当前WorldStereo仅评估静态场景，未讨论对动态物体或非刚性运动的处理能力。DMD训练需过滤困难轨迹以保证稳定性，可能限制生成多样性。轨迹顺序和角度依赖手动预设，缺乏自动化规划。开放问题包括：如何处理包含移动物体的动态输入？当记忆库中参考帧极度无序时SSM的鲁棒性如何？能否自动规划最优轨迹以最大化重建质量？模型能否扩展至更长序列或更多样化场景而无性能衰减？



### 三维重建与视频生成的割裂

从二维图像恢复三维场景是计算机视觉的核心目标之一。传统三维重建管线依赖多视角图像的特征匹配与几何优化，但在稀疏视角或弱纹理区域往往产生不完整或模糊的结果。近年来，视频扩散模型（VDM）展现出强大的视觉内容生成能力，为三维重建提供了新的可能——通过生成覆盖目标场景的多视角视频，再利用重建算法恢复场景结构。然而，**现有摄像机引导的视频扩散模型难以生成多视角一致的视频**：它们缺乏对场景几何的显式记忆，导致不同视频片段间的内容不一致，最终重建出的三维模型出现严重模糊。

### 现有生成范式的局限

当前用于三维重建的视频生成方案可归为三类（Table 1）：**长序列双向VDM**在单次推理中生成覆盖多视角的长轨迹，但受限于模型容量，难以保证大范围视角变化下的结构一致性；**自回归模型**逐帧生成长视频，但误差累积问题突出；**多段双向VDM**虽能利用强大的预训练模型生成互补视角，却缺乏跨视频的记忆机制，无法维持全局几何一致性。这些方法的共同瓶颈在于**缺乏几何记忆**——生成过程仅依赖当前帧的摄像机参数与图像条件，无法感知已生成内容的三维结构，导致不同视频之间产生内容漂移。

### 动机：以几何记忆桥接生成与重建

本文的核心动机在于，**通过即插即用的几何记忆模块，将摄像机引导的视频生成与三维重建深度耦合**，使生成过程能够感知并利用累积的三维先验。具体而言，WorldStereo 引入两类互补的记忆机制：

- **全局几何记忆（GGM）**：通过增量更新的点云条件，为多段视频生成提供粗粒度的三维结构先验，确保不同视频在全局几何层面保持一致。
- **空间立体记忆（SSM）**：检索已生成视图中的参考帧，利用三维对应关系约束注意力感受野，恢复细粒度的纹理与细节一致性。

这种设计使 WorldStereo 能够基于预训练视频扩散模型的强大泛化能力，在不进行联合训练的前提下，实现高效、高质量的多视角一致视频生成，并直接服务于下游三维重建。此外，通过分布匹配蒸馏（DMD）将生成器蒸馏为4步DiT，可将推理速度提升约20倍，进一步增强了方法的实用性。



## 核心方法与创新机理

WorldStereo 的核心创新在于通过两个即插即用的几何记忆模块，将摄像机引导的视频扩散模型（VDM）与三维重建桥接起来，解决了现有方法在多视角一致视频生成中的几何记忆缺失与内容不一致问题。其关键设计可归纳为三个 **changed slots**，相对于基线方法 **Uni3C**（摄像机控制基线 VDM）实现了根本性突破。

---

### 1. 全局几何记忆（GGM）：从单帧点云到增量式全局结构先验

**基线方法**仅使用参考帧的反投影点云 $X_{pcd}$ 作为几何条件，缺乏对场景全局结构的感知。**WorldStereo** 将点云条件扩展为全局点云 $X_{pcd}^g = [X_{pcd}, \hat{X}_{pcd}]$，其中 $\hat{X}_{pcd}$ 来自先前生成视图的累积重建点云（Eq.2）。这一扩展通过 **3D Cache** 实现：每次生成视频后，利用 WorldMirror 进行增量三维重建，并通过 Umeyama 变换对齐到统一坐标系，逐步更新全局点云条件。

为增强对不完整点云的鲁棒性，GGM 引入了**点云遮蔽策略**——在训练时随机丢弃部分点，并采用连续遮蔽增强。这使得模型学会从稀疏、噪声的全局点云中推断粗粒度三维结构，为多轨迹视频生成提供一致的几何先验。消融实验（Figure 5）表明，仅添加 GGM 即可将 PSNR 从 14.64 提升至 17.45（Table 5），但粗粒度结构仍会丢失细粒度纹理细节。

---

### 2. 空间立体记忆（SSM）：基于 3D 对应的细粒度注意力约束

**基线方法**无额外记忆分支，仅依赖摄像机 ControlNet。**WorldStereo** 新增 SSM 分支，通过检索参考帧并注入三维对应信息，实现细粒度纹理一致性。其核心机制包括：

- **参考帧检索与拼接**：从 Memory Bank 中检索与目标视图空间相似的参考帧，将目标帧与参考帧水平拼接为“目标-参考对”。
- **点图注入**：利用 3D Cache 为每对拼接帧生成点图（pointmap），编码三维对应关系，作为额外的条件信号注入 SSM ControlNet。
- **受限注意力**：将拼接后的特征张量重构为 $[BF, H \times 2W, C]$ 的形状，迫使每个目标帧的注意力仅集中于其专属的参考帧区域，而非全局扩散。这使得模型能够从检索到的参考帧中精确恢复细粒度细节。

消融实验（Figure 5(c)(d)）证实，三维对应信息对 SSM 的性能至关重要。定量消融（Table 5）显示，在 GGM 基础上加入 SSM 后，PSNR 进一步提升至 18.40，LPIPS 从 0.412 降至 0.283。

---

### 3. 分布匹配蒸馏（DMD）：无联合训练的 20 倍推理加速

**基线方法**使用 40 步去噪推理，耗时 162 秒。**WorldStereo** 通过修改的分布匹配蒸馏（DMD）将生成器蒸馏为 4 步 DiT，推理时间降至 9 秒，实现约 20 倍加速（Table 2）。其关键优势在于：

- **无需联合训练记忆分支**：DMD 训练仅基于纯摄像机引导的视频生成，不涉及 GGM 或 SSM 的记忆训练。这得益于 WorldStereo 中 ControlNet 注入的像素级对齐特性，使得蒸馏后的生成器可直接继承完整模型的记忆能力。
- **CFG-free 生成器**：训练时对真实分数函数使用 CFG scale 5.0，蒸馏后生成器无需 CFG 即可生成高质量视频，进一步降低推理开销。
- **数据过滤策略**：DMD 训练时过滤困难轨迹以保证稳定性，实验验证（Table 2）表明该策略不会损害摄像机控制精度。

DMD 更新梯度基于真实分数函数 $s_{\mathrm{real}}$ 与伪造分数函数 $s_{\mathrm{fake}}$ 之差：

$$
\nabla \mathcal{L}_{\mathrm{DMD}} = - \frac{\mathbb{E}}{t} \left( \int \left( s_{\mathrm{real}}(x_t, t) - s_{\mathrm{fake}}(x_t, t) \right) \frac{d x_t}{d \theta} d z \right)
$$

---

### 创新本质：几何记忆作为桥接机制

WorldStereo 的核心洞察在于：**预训练视频扩散模型的泛化能力可作为多视角一致视频生成的基础，而几何记忆模块则充当摄像机引导生成与三维重建之间的桥接器**。GGM 提供粗粒度结构先验，SSM 恢复细粒度纹理，二者协同工作，使模型无需端到端联合训练即可生成多轨迹一致的视频，进而支撑高质量三维重建。在 Tanks-and-Temples 基准上，WorldStereo-Full 的 F1-Score 达到 0.578，较基线 Uni3C 的 0.424 提升 36.3%（Table 3），充分验证了该创新范式的有效性。



WorldStereo 的整体 pipeline 围绕“摄像机引导的视频生成”与“三维重建”之间的桥梁构建。其核心思路是：在预训练视频扩散模型（VDM）的基础上，通过两个即插即用的几何记忆模块，将多视角一致的视频生成与增量式三维重建耦合为一个闭环系统，从而在无需联合训练的情况下实现高质量的真实世界立体视频生成。

### 输入与输出流

系统的输入可以是一张单视图图像或一张全景图。输出为多段具有精确摄像机控制且多视角一致的视频，这些视频可直接馈入现有的三维重建流程（如 WorldMirror）以生成稠密点云。Figure 2 展示了完整的生成管线。

![[assets/figures/papers/paper_list_l11_https_arxiv_org_abs_2603_02049/figures/003_Figure_2.jpg]]
*Figure 2: Overview of WorldStereo. WorldStereo comprises two ControlNet branches. The camera branch ensures precise camera control and Global-Geometric Memory (GGM), depending on global point clouds; the Spatial-Stereo Memory (SSM) branch leverages retrieved reference frames and pointmap (3D correspondence) guidance obtained from the 3D cache to further preserve fine-grained consistency. We omit the diffusion noise part for simplicity*

### 双分支 ControlNet 架构

WorldStereo 在预训练 VDM 之上构建了两个并行的 ControlNet 分支，分别负责粗粒度几何先验注入与细粒度纹理一致性保持：

1. **摄像机分支（Camera Branch）与全局几何记忆（GGM）**  
   该分支接收摄像机射线（camera rays）和增量更新的全局点云条件 $X_{pcd}^g$。全局点云由参考帧点云 $X_{pcd}$ 与其他视图重建的点云 $\hat{X}_{pcd}$ 拼接而成：$X_{pcd}^g = [X_{pcd}, \hat{X}_{pcd}]$。GGM 通过迭代更新这一全局点云条件，为多段视频的生成提供一致的粗粒度三维结构先验，同时确保精确的摄像机控制。训练时引入随机点云遮蔽（randomly dropping a subset of points）和连续遮蔽策略以增强鲁棒性。

2. **空间立体记忆分支（SSM Branch）**  
   该分支从记忆库（Memory Bank）中检索与当前目标视角空间相似的参考帧，将目标帧与参考帧水平拼接，并融入从三维缓存（3D Cache）导出的点图（pointmap）作为三维对应信息。随后，通过重构特征张量形状为 `[B×F, H×2W, C]`，将注意力感受野限制在每一对目标-参考帧内部，使目标帧特征仅关注其专属的检索参考帧，从而恢复细粒度纹理细节。

### 记忆与缓存系统

两个记忆组件支撑着上述分支的运作：

- **记忆库（Memory Bank）**：存储已生成视频的时间降采样帧，为 SSM 提供检索源。
- **三维缓存（3D Cache）**：累积通过 WorldMirror 从记忆库图像增量重建的全局点云集合 $X_{cache}$，并通过 Umeyama 变换进行对齐。该缓存同时为 GGM 提供扩展点云条件，为 SSM 提供点图对应信息。

### 推理加速：DMD 蒸馏

WorldStereo 利用其像素级对齐的 ControlNet 注入特性，通过分布匹配蒸馏（Distribution Matching Distillation, DMD）将生成器蒸馏为仅需 4 步去噪的 DiT，实现约 20 倍推理加速（从 162 秒降至 9 秒）。DMD 训练基于纯摄像机引导的视频生成，无需联合训练记忆分支，从而保持了模型的泛化能力。DMD 的生成器更新梯度为：

$$\nabla \mathcal{L}_{\mathrm{DMD}} = - \frac{\mathbb{E}}{t} \left( \int \left( s_{\mathrm{real}}(x_t, t) - s_{\mathrm{fake}}(x_t, t) \right) \frac{d x_t}{d \theta} d z \right)$$

### 闭环生成流程

整个 pipeline 以闭环方式运行：VDM 生成视频帧 → 帧存入记忆库 → WorldMirror 增量重建点云并更新 3D Cache → 更新后的全局点云反馈给 GGM 作为下一轮生成的条件，同时点图信息注入 SSM 以约束注意力。这种“生成-重建-记忆”的循环机制使得 WorldStereo 能够生成互补视角的多段一致视频，为集成式三维重建提供高质量输入。

### 补充图表

![[assets/figures/papers/paper_list_l11_https_arxiv_org_abs_2603_02049/figures/014_Figure_8.jpg]]
*Figure 8: Illustration of the trajectory*



### 3.1 基础摄像机引导的视频扩散模型

WorldStereo 构建于预训练视频扩散模型（VDM）之上，采用 **Uni3C** 作为摄像机引导的基线生成器。该基线通过一个轻量级 ControlNet 分支注入摄像机射线和点云条件，实现对生成视角的精确控制。

对于参考图像中的像素 $x$，其三维修正点云通过反投影获得：

$$X_{pcd}(x) \simeq R_{cw} D(x) K^{-1} \hat{x}$$

其中 $R_{cw}$ 为摄像机到世界坐标系的旋转矩阵，$D(x)$ 为深度估计值，$K^{-1}$ 为相机内参矩阵的逆。该点云条件作为强几何引导信号输入 ControlNet 分支（第3.1节）。

### 3.2 全局几何记忆（GGM）

**核心瓶颈**：基础 VDM 在生成多段视频时缺乏跨轨迹的几何一致性，导致后续三维重建模糊。

**GGM 设计**：通过增量更新的全局点云提供粗粒度结构先验。具体而言，将参考帧点云 $X_{pcd}$ 与其他已生成视图的点云 $\hat{X}_{pcd}$ 拼接，形成扩展的全局点云条件：

$$X_{pcd}^g = [X_{pcd}, \hat{X}_{pcd}]$$

训练时引入随机遮蔽策略——随机丢弃部分点云以增强鲁棒性，并采用连续遮蔽机制模拟生成过程中的信息不完整性。GGM 通过摄像机 ControlNet 分支注入，确保多段视频共享一致的全局三维结构，但定性消融（图5）表明其仅能捕捉粗粒度结构，细粒度纹理细节仍需后续模块补充。

### 3.3 空间立体记忆（SSM）

**核心瓶颈**：GGM 提供了全局结构先验，但无法恢复细粒度纹理一致性。

**SSM 设计**：通过检索参考帧并利用三维对应关系约束注意力，实现像素级纹理对齐。具体流程如下（图3）：

1. **检索与拼接**：从记忆库中检索空间相似的参考视图，将目标帧与参考帧水平拼接为目标-参考对。
2. **点图注入**：基于三维缓存为每个拼接对生成点图，编码三维对应信息。
3. **注意力约束**：将拼接特征张量重构为 $[BF, H \times 2W, C]$ 形状，使每个目标-参考对仅关注自身特征，强制模型在三维对应区域进行细粒度匹配。

消融实验（图5c/d）证实，三维对应信息对 SSM 性能至关重要——移除点图引导将显著降低与检索参考帧的一致性。

### 3.4 分布匹配蒸馏（DMD）加速

**核心瓶颈**：基础 VDM 需 40 步去噪推理，耗时约 162 秒，难以实际部署。

**DMD 设计**：WorldStereo 利用 ControlNet 分支的像素级对齐注入特性，将生成器蒸馏为 4 步 DiT，无需联合训练记忆分支。DMD 生成器的更新梯度基于真实分数函数 $s_{\mathrm{real}}$ 与伪造分数函数 $s_{\mathrm{fake}}$ 之差：

$$\nabla \mathcal{L}_{\mathrm{DMD}} = - \frac{\mathbb{E}}{t} \left( \int \left( s_{\mathrm{real}}(x_t, t) - s_{\mathrm{fake}}(x_t, t) \right) \frac{d x_t}{d \theta} d z \right)```

蒸馏后的 WorldStereo-DMD 将推理时间从 162 秒压缩至 9 秒，实现约 20 倍加速（表2），同时保持摄像机控制精度和视觉质量。DMD 训练中采用数据过滤策略保留高质量轨迹，表2验证该策略未损害摄像机可控性。

### 补充图表

![[assets/figures/papers/paper_list_l11_https_arxiv_org_abs_2603_02049/figures/009_Figure_5.jpg]]
*Figure 5: Ablation studies of memory components. Please see the red-framed regions to check the consistency compared to retrieved references. Baseline results are generated without any memory. GGM can capture coarse structures, but loses fine-grained details. Moreover, the incorporation of pointmap significantly enhances the consistency gained via the reference frames retrieved from the memory bank*

![[assets/figures/papers/paper_list_l11_https_arxiv_org_abs_2603_02049/figures/004_Figure_3.jpg]]
*Figure 3: Spatial-Stereo Memory (SSM). Reference views are retrieved from the memory bank, while pointmaps for both target and reference views are constructed based on the 3D cache. In SSM attention, we horizontally stitch each target-reference pair and rearrange the tensor shape to make each target frame’s features focus on the specifically retrieved reference. B, F, H, W, C indicate dimensions of batch, frame, height, width, and channels*



## 实验与关键发现

### 核心实验结果

WorldStereo 在跨分布（OOD）摄像机控制、三维重建质量和推理效率三个维度上均展现出显著优势。表2（Table 2）汇总了基于 WorldScore 图像的 OOD 摄像机控制与视觉质量评估：基础版本 WorldStereo∗（无任何记忆机制）的旋转误差 RotErr 为 0.155，已优于 Uni3C 等对比方法；引入全局几何记忆（GGM）和空间立体记忆（SSM）后的完整版 WorldStereo-Full 将 RotErr 进一步降至 0.132（↓14.8%），同时平移误差 TransErr 和绝对轨迹误差 ATE 也保持领先。在三维重建基准 Tanks-and-Temples 上（Table 3），WorldStereo-Full 的 F1-Score 达到 0.578，相较 Uni3C 基线（0.424）提升 36.3%，较端到端方法 Voyager（0.363）提升 59.2%。在 MipNeRF360 数据集上，WorldStereo-Full 同样取得最优 PSNR（18.40）和 SSIM（0.675），LPIPS 降至 0.283。

![[assets/figures/papers/paper_list_l11_https_arxiv_org_abs_2603_02049/figures/005_Table_2.jpg]]
*Table 2: Quantitative results of OOD benchmark with WorldScore [21] images. ∗ indicates the baseline version of our method without any memory mechanism, while the ‘full’ version denotes adding both GGM and SSM. The ‘DMD’ version is based on ‘WorldStereo-full’. Inference times are all tested with 8 H20 GPUs. **

![[assets/figures/papers/paper_list_l11_https_arxiv_org_abs_2603_02049/figures/006_Table_3.jpg]]
*Table 3: Quantitative results of 3D reconstruction based on Tanks-and-Temples [45] and MipNeRF360 [4]. ∗ indicates the baseline version of our method without any memory mechanism*

定性结果（Figure 4）进一步验证了上述定量趋势：Uni3C 生成的点云存在明显噪声和空洞，Voyager 重建结果模糊且缺失细节，而 WorldStereo 重建的点云结构完整、纹理清晰，生成的新视角图像与真值高度一致。

![[assets/figures/papers/paper_list_l11_https_arxiv_org_abs_2603_02049/figures/008_Figure_4.jpg]]
*Figure 4: Results of 3D reconstruction benchmark. The column (a) shows input views and ground-truth point clouds with pre-defined four trajectories (up, left, right rotations, and orbit). We compare the qualitative results of reconstructed point clouds (left) and generated novel views (right) for each method*

推理效率方面（Table 2），完整版 WorldStereo-Full 在 8 张 H20 GPU 上推理耗时 162 秒；经分布匹配蒸馏（DMD）压缩为 4 步 DiT 后，WorldStereo-DMD 仅需 9 秒即可完成生成，加速约 18 倍，同时摄像机控制精度（RotErr 0.129）与完整模型相当，验证了 DMD 训练中数据过滤策略的有效性。

### 消融实验

**记忆组件的贡献**。消融实验从定性和定量两个层面揭示了 GGM 与 SSM 的互补作用。定性消融（Figure 5）显示：基线版本（无记忆）生成结果与检索参考帧存在明显不一致，尤其在红色框标注区域；单独引入 GGM 后，模型能捕捉粗粒度三维结构（如物体轮廓和空间布局），但细粒度纹理（如表面图案、边缘细节）仍然丢失；进一步加入 SSM 并配合点图（pointmap）提供的三维对应信息后，生成结果与检索参考帧的一致性显著增强，纹理细节得到有效恢复。

定量消融（Table 5）佐证了这一结论：基线 PSNR 为 14.64、LPIPS 为 0.412；添加 GGM 后 PSNR 提升至 17.45（+2.81 dB），LPIPS 降至 0.325；加入 SSM 后 PSNR 进一步提升至 18.40（+0.95 dB），LPIPS 降至 0.283。值得注意的是，SSM 在摄像机控制指标上略有退化（RotErr 从 0.132 升至 0.135），但换来了细粒度一致性的显著改善，体现了设计上的权衡。

![[assets/figures/papers/paper_list_l11_https_arxiv_org_abs_2603_02049/figures/010_Table_5.jpg]]
*Table 5: Quantitative ablation for memory components. ∗ indicates our baseline without any memory mechanism, while the ‘full’ version denotes adding both GGM and SSM. The ‘DMD’ version is based on ‘WorldStereo-full’*

**点图的关键作用**。Figure 5(c)(d) 的消融证实，若移除 SSM 中的点图输入（即仅依赖检索帧的水平拼接），模型无法有效利用三维对应信息，生成结果与检索参考帧的一致性大幅下降。这表明点图提供的显式三维对应约束是 SSM 发挥作用的必要条件。

**DMD 蒸馏的影响**。Table 2 和 Table 5 的 DMD 版本数据显示，蒸馏后的 4 步生成器在摄像机控制精度（RotErr 0.129）和重建质量（F1-Score 0.558）上仅略低于完整模型，但推理速度提升约 18–20 倍。这一结果验证了基于像素对齐 ControlNet 注入的 DMD 训练策略能够在不牺牲泛化能力的前提下实现高效推理。

### 摄像机控制能力评估

Table 6 单独评估了各方法的摄像机控制能力。WorldStereo∗ 在旋转误差和平移误差上均优于 Uni3C、Gen3C 和 SEVA 等基线，表明基于全局点云条件的 ControlNet 分支本身已具备较强的摄像机控制能力。引入记忆模块后，摄像机控制精度保持稳定，未出现退化。

![[assets/figures/papers/paper_list_l11_https_arxiv_org_abs_2603_02049/figures/012_Table_6.jpg]]
*Table 6: Quantitative results for camera control*

### 全景生成中的轨迹顺序消融

Table 7 展示了全景三维生成中不同轨迹顺序对记忆检索质量的影响。当记忆库仅包含全景分割的 24 个视图时，重叠视场（FoV）得分较低；随着生成轨迹的增量更新，检索到的相关帧比例上升，FoV 得分提高。实验表明，合理的轨迹顺序能够提升记忆库中参考帧的覆盖度，进而增强生成一致性。

![[assets/figures/papers/paper_list_l11_https_arxiv_org_abs_2603_02049/figures/015_Table_7.jpg]]
*Table 7: Overlapping FoV scores of 3D panorama generation (trajectory order ablation). Memory bank settings: ‘only panorama’ uses 24 views split from the panorama; others are incrementally updated with generations from different trajectory orders. Higher scores mean that more relevant frames are retrieved. ‘reference prop.’ indicates the proportion of retrieved frames belonging to panoramic (pano.) or generated (gen.) frames*

### 失败模式与局限性

尽管 WorldStereo 在静态场景重建上表现优异，论文未评估其对动态场景或非刚性运动的处理能力——所有重建基准仅覆盖静态区域。DMD 训练中采用的困难轨迹过滤策略（保留“高质量且相对容易”的轨迹）虽然保证了蒸馏稳定性，但可能限制生成内容的多样性，在极端视角或复杂几何场景下存在性能下降风险。此外，当前方法依赖手动预设的轨迹顺序和角度，缺乏自动化规划机制，在实际部署中需要人工介入。当检索的参考帧极度无序或视场重叠不足时，SSM 的细粒度一致性增强效果可能减弱，该场景下的鲁棒性尚需进一步验证。

### 补充图表

![[assets/figures/papers/paper_list_l11_https_arxiv_org_abs_2603_02049/figures/002_Table_1.jpg]]
*Table 1: Different video generation schemes for 3D reconstruction. Long-Bi VDMs produce long trajectories in a single pass to cover diverse viewpoints. AR models sequentially generate long videos in an autoregressive manner. Multi-Bi-Mem (ours) achieves multiple consistent generations based on a powerful open-released VDM [78] with complementary viewpoints and memory mechanisms for integrated reconstruction*

![[assets/figures/papers/paper_list_l11_https_arxiv_org_abs_2603_02049/figures/001_Figure_1.jpg]]
*Figure 1: WorldStereo enables high-quality 3D scene generation based on single-view or panoramic inputs. The input reference views are framed in green. We present point clouds reconstructed from videos generated by WorldStereo: the top two perspective scenes use WorldMirror [58], while the bottom two panoramic scenes are aligned via monocular depth maps [84]*



## 定位与知识库关联

### 任务定位与范式对比

WorldStereo 定位于**摄像机引导的真实世界立体视频生成**，并将其直接服务于下游三维重建。Table 1 将现有视频生成范式归纳为三类：长双向视频扩散模型（Long-Bi VDMs）在单次生成中覆盖多视角但受限于序列长度；自回归模型（AR models）顺序生成长视频但累积漂移；WorldStereo 提出的**多双向记忆增强范式（Multi-Bi-Mem）** 则基于预训练视频扩散模型的泛化能力，通过互补轨迹生成与几何记忆机制实现多段一致性视频的集成重建。

### 与基线方法的关系

**摄像机控制基线。** WorldStereo 的基础版本（WorldStereo*）直接继承自 **Uni3C**，后者在 Wan-I2V 预训练主干上集成轻量级 ControlNet 分支，以摄像机射线和参考帧点云作为条件。WorldStereo 在此之上扩展了条件空间：将单帧点云 $X_{pcd}$ 扩展为全局点云 $X_{pcd}^g = [X_{pcd}, \hat{X}_{pcd}]$，并引入点云遮蔽策略增强鲁棒性。Table 2 显示，仅基础版本已在 OOD 摄像机控制指标 RotErr 上达到 0.155，优于同期方法。

**端到端三维生成方法。** 与 **Voyager**、**Lyra** 等直接生成三维表征的方法不同，WorldStereo 采用“生成视频—重建三维”的两阶段路线。这种解耦设计使其能充分利用预训练视频扩散模型的海量数据先验，同时通过几何记忆模块弥补视频生成与三维重建之间的多视角一致性鸿沟。Table 3 的 Tanks-and-Temples 重建基准上，WorldStereo-Full 的 F1-Score 达到 0.578，显著高于 Uni3C 的 0.424（↑36.3%）。

**内存增强视频生成。** **VMem** 等内存增强方法通常服务于长视频生成的时序一致性，而 WorldStereo 的记忆机制专门针对**空间多视角一致性**设计：全局几何记忆（GGM）提供粗粒度三维结构先验，空间立体记忆（SSM）通过检索参考帧并约束注意力到三维对应区域来恢复细粒度纹理。Figure 5 的消融实验揭示了二者的互补关系——GGM 可捕捉粗粒度结构但丢失细粒度细节，SSM 配合点图能显著恢复纹理一致性。

**摄像机引导生成方法。** 与 **SEVA**（稳定虚拟摄像机）和 **Gen3C**（摄像机引导生成）相比，WorldStereo 的独特之处在于将摄像机控制与几何记忆深度融合。Table 2 的定量对比表明，WorldStereo* 在 RotErr 和 TransErr 上均优于这些方法，而加入记忆模块后的完整版本在保持摄像机控制精度的同时大幅提升了视觉质量。

### 适用边界与局限

**静态场景假设。** 论文的所有实验和重建基准均针对静态区域，未讨论对动态场景或非刚性运动的处理能力。当输入包含移动物体时，基于点云反投影的几何记忆机制可能失效。

**轨迹预设依赖。** 当前方法需要手动预设生成轨迹的顺序和角度（Figure 8），缺乏自动化的最优轨迹规划。Table 7 的全景生成消融表明，不同轨迹顺序会影响记忆库中相关帧的检索比例，进而影响重建质量。

**DMD 训练的数据过滤。** 分布匹配蒸馏训练需要过滤困难轨迹以保证稳定性（Section 3.4），这一策略可能限制生成内容的多样性，尽管 Table 2 验证了过滤后的模型仍保持了摄像机控制精度。

**检索鲁棒性未充分验证。** SSM 在训练中通过随机打乱和遮蔽参考帧来模拟检索噪声，但当记忆库中参考帧极度无序或差异性大时，其鲁棒性仍需进一步验证。

### 开放问题

1. **动态场景扩展**：如何处理包含移动物体的动态场景？是否需要引入运动分割或动态点云建模？
2. **检索鲁棒性边界**：当记忆库覆盖不足或检索到的参考帧与目标视角差异极大时，SSM 的注意力约束机制是否会失效？
3. **轨迹自动规划**：能否根据输入视图自动规划最优生成轨迹，以最大化三维重建的覆盖度和质量？
4. **长序列扩展**：模型能否扩展到更长的生成序列或更多样化的场景类型，而不会出现几何记忆累积误差导致的性能下降？
5. **真实世界部署**：当前实验均在受控基准上进行，在完全开放的真实世界场景（如无约束拍摄、大范围场景）中的泛化能力尚未验证。



## 原文 PDF

![[paperPDFs/arxiv_2026/WorldStereo_Bridging_3D_Reconstruction_and_Video_Generation_for_Scalable_Real_World_Stereo_Video_Generation.pdf]]
