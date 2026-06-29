---
title: Towards Motion Metamers for Foveated Rendering
type: paper
paper_level: A
venue: SIGGRAPH
year: 2024
pdf_ref: paperPDFs/SIGGRAPH_2024/Towards_Motion_Metamers_for_Foveated_Rendering.pdf
project_link: null
code_link: null
aliases:
- MMSG
- TMMFR
tags:
- SIGGRAPH_2024
- topic/graphics_rendering_materials
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: 通过在注视渲染视频上叠加与局部运动方向对齐的可控时空运动能量（Gabor噪声相位漂移），补偿被削弱的运动线索。
primary_logic: 受“双重漂移错觉”启发，相干相位调制可引入全局运动感知；通过程序化Gabor噪声合成高频空间纹理，并控制其相位变化速率以匹配局部运动流，可以在不引入可察觉伪影的前提下恢复周边视觉的运动速度感知。
claims:
- 注视渲染场景感知速度显著慢于全分辨率场景
- 所提方法在中、高注视程度下显著减轻了速度感知损失（p<0.05）
- 多数被试在质量判断中偏好所提方法，未报告引入明显伪影
- Velocity matching experiment (Vegetation and City scenes) 上 Percentage difference in velocity perception relative to fu... = Our method significantly reduced velocity underestimation (...
---

# Towards Motion Metamers for Foveated Rendering

> [!tip] 核心洞察
> 受“双重漂移错觉”启发，相干相位调制可引入全局运动感知；通过程序化Gabor噪声合成高频空间纹理，并控制其相位变化速率以匹配局部运动流，可以在不引入可察觉伪影的前提下恢复周边视觉的运动速度感知。

| 字段 | 内容 |
|------|------|
| 中文题名 | 迈向注视渲染的运动元映射 |
| 英文题名 | Towards Motion Metamers for Foveated Rendering |
| 会议/期刊 | SIGGRAPH 2024 |
| Links | [paper](https://www.pdf.inf.usi.ch/projects/MotionMetamers/index.html) |
| Topic | #topic/graphics_rendering_materials #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | Motion Metamer Synthesis (基于程序化Gabor噪声的时空运动能量合成) |
| Dataset | Velocity matching experiment, 2AFC quality preference experiment |

> [!tip] 效果简介
> - Velocity matching experiment (Vegetation and City scenes) 上，Percentage difference in velocity perception relative to full-quality reference Our method significantly reduced velocity underestimation (p<0.05 for Mid and H... vs Standard foveated rendering (consistent velocity underestimation, e.g., -X%) (Significant reduction in loss; for High foveation, perceived velocity improved...)。
> - 2AFC quality preference experiment 上，Percentage of judgments favoring the proposed technique over foveated (in terms... Majority of judgments favored the proposed technique (preference >50%) vs Standard foveated rendering (Clear preference for the proposed method across conditions)。

## 概要

注视渲染通过降低周边视觉区域的空间细节来节省算力，但本文发现这一做法会抑制人类周边视觉的运动感知，导致用户系统性地低估场景运动速度。为解决该问题，作者提出**运动元映射**概念——即生成与参考视频结构不同但诱发相同速度感知的图像序列。具体而言，该方法在注视渲染帧上叠加程序化Gabor噪声，并通过与局部运动流对齐的相干相位调制来合成可控的时空运动能量，从而补偿被削弱的运动线索。用户实验表明：在中、高注视程度下，所提方法显著减轻了速度感知损失（p<0.05），且多数被试在质量判断中偏好该方法，未报告明显伪影。该方法属于注视渲染与感知驱动的程序化纹理合成的交叉，为实时图形系统中运动感知保真度的维持提供了新思路。

## 核心方法与创新机理

### 问题瓶颈与核心洞察

注视渲染通过随离心率增大而降低周边区域空间细节（通常采用高斯模糊）来节省计算资源，但这项工作揭示了一个此前被忽视的关键副作用：**空间细节的丢失会抑制人类周边视觉的运动感知，导致用户系统性低估场景运动速度**。作者通过速度匹配实验验证了这一现象：被试需要将注视渲染场景的速度调至显著高于全分辨率参考场景，才能获得相同的速度感知（Figure 2），说明注视渲染场景被感知为“更慢”。

![[assets/figures/papers/paper_list_l41_https_www_pdf_inf_usi_ch_projects_MotionMetamers_index_html/figures/002_Figure_2.jpg]]
*Figure 2: Foveated Motion Perception: In a full reference task to match the velocity of foveated/full-resolution scenes a reference moving at a fixed velocity (dotted blue line). People tend to assign the foveated scene a significantly higher velocity compared to the full-resolution scene for equivalence (foveated was percieved slower). This serves as evidence for potential loss in motion perception/cues due to peripheral blur. The reported p-value is for a t-test between the two groups (full-resolution and foveated). The error bars represent Standard Error (SE)*

这一瓶颈的因果机制在于：周边视觉的运动感知依赖于时空频率信息的联合编码，而注视渲染仅降低了空间频率成分，未补偿由此造成的运动能量损失。作者从“双重漂移错觉”（double-drift illusion）获得启发——在周边视觉中，Gabor斑点的物理位移与其内部相位漂移会被视觉系统整合，产生与实际运动不同的感知运动方向。这意味着：**通过程序化控制Gabor噪声的相位变化速率，可以在不引入可察觉空间伪影的前提下，向周边区域注入可控的时空运动能量，从而补偿注视渲染造成的运动感知损失**。

### 核心概念：运动元映射

作者提出了“运动元映射”（motion metamer）的概念框架：两个视频序列在结构上不同（如空间频率分布差异显著），但引发的空间感知和运动感知等价。本文作为迈向运动元映射的第一步，目标是合成一种“运动补偿纹理”，使其叠加到注视渲染视频后，恢复与全分辨率参考相同的速度感知，同时保持不可见性（即不引入可分辨的空间伪影）。

### 方法框架与模块顺序

整体方法流程（Figure 4）包含五个核心模块，按推理路径串联：

![[assets/figures/papers/paper_list_l41_https_www_pdf_inf_usi_ch_projects_MotionMetamers_index_html/figures/004_Figure_4.jpg]]
*Figure 4: Method Overview: Our method takes a foveated rendering frame as input. We first do a multi-scale decomposition of the input frame (Gaussian and Laplacian pyramid), and estimate motion flow. The obtained pyramids and motion flow are thereafter processed by our technique, which is centered around on the spatio-temporal frequency perception characteristics of the human visual system. Thereafter, we synthesize perceptually controlled directional motion energy using procedural Gabor noise, and super-impose it over the foveated frame*

1. **多尺度分解**：对输入的注视渲染帧构建高斯金字塔和拉普拉斯金字塔，用于后续的对比度掩蔽估计和空间频率分析。
2. **运动流估计**：计算逐像素的运动向量场 $v(\mathbf{x})$，作为运动能量合成的方向与速率依据。
3. **感知模型参数估计**：基于时空可分辨性边界和对比度掩蔽模型，为每个Gabor斑点计算其空间频率、时间频率、朝向和振幅，确保合成内容处于可见性边界之下。
4. **Gabor噪声合成**：在随机采样位置生成程序化Gabor斑点，并通过相位调制引入与局部运动方向对齐的时空运动能量。
5. **叠加输出**：将合成的运动能量叠加到注视渲染帧上，得到最终输出。

### 关键Changed Slots

相较于标准注视渲染，该方法在三个关键环节进行了替换：

| 环节 | 标准注视渲染 | 本文方法 | 因果作用 |
|------|-------------|---------|---------|
| 周边空间细节处理 | 离心率依赖的高斯模糊，直接丢弃高频信息 | 合成高频Gabor噪声叠加，补偿丢失的空间纹理 | 恢复运动感知所需的空间载波信号 |
| 运动能量合成 | 无显式运动能量合成 | 通过相位调制产生与局部运动流对齐的时空运动能量 | 直接补偿运动感知损失的核心机制 |
| 时间频率控制 | 无 | 相位变化速率与局部速度成正比（α因子控制） | 使合成运动能量的感知强度与场景运动匹配 |

### 核心机制：Gabor噪声与相位调制

方法的基础构建块是**程序化Gabor噪声**。每个Gabor斑点定义为正弦载波与高斯包络的乘积：

$$g_i(x, y) = K_i e^{-\pi a_i^2 (x^2 + y^2)} \cos(2\pi f_s^i (x \cos\theta_i + y \sin\theta_i) + \phi_i)$$

其中 $K_i$ 为振幅，$a_i$ 控制高斯包络宽度，$f_s^i$ 为空间频率，$\theta_i$ 为朝向，$\phi_i$ 为相位。某点的噪声值为周围Gabor斑点的加权叠加：

$$N(x, y) = \sum_{i \in I} w_i \cdot g_i(x - x_i, y - y_i)$$

权重 $w_i$ 随机取二值，使合成噪声期望均值为零，避免引入直流分量。

**引入运动能量的关键操作是相位调制**。受双重漂移错觉启发，作者使每个Gabor斑点的相位随时间连续变化，变化速率与局部运动流对齐：

$$\phi_v(i) = 2\pi f_t(i)$$

其中时间频率 $f_t(i)$ 定义为：

$$f_t(i) = \alpha \cdot f_s(i) \cdot v(\mathbf{x_i})$$

即空间频率与局部运动速度的乘积，$\alpha$ 为额外的全局缩放因子（实验中设为1.0）。每帧的相位更新为：

$$\phi_i^{k+1} = \phi_i^k + \frac{\phi_v(i)}{R}$$

其中 $R$ 为显示器刷新率。这种相位漂移在周边视觉中会产生连贯的全局运动感知，其方向与局部运动流一致，强度由 $\alpha$ 和 $v(\mathbf{x_i})$ 共同控制。

### 感知模型：可见性边界控制

为确保合成内容不可见（即不引入可分辨的空间伪影），方法将Gabor斑点的参数严格约束在人类视觉系统的时空可分辨性边界之内。具体而言，利用对比度敏感度函数 $S_{csf}$ 定义每个斑点的可分辨性：

$$S(i) = S_{csf}(f_s(i), f_t(i), e(\mathbf{x_i}))$$

$S(i) < 1$ 表示该斑点不可分辨。方法使用 stelaCSF 模型，该模型给出了 $S_{csf} = 1$ 的等敏感度曲面（Figure 5a）。作者观察到，等离心率截面的 $f_s$-$f_t$ 关系近似线性（Figure 5b），据此推导出空间频率的闭式解：

$$f_s(i) = \frac{T_s(e(\mathbf{x_i}))}{1 + \frac{T_s(e(\mathbf{x_i}))}{T_t(e(\mathbf{x_i}))} \cdot \alpha \cdot v(\mathbf{x_i})}$$

其中 $T_s(e)$ 和 $T_t(e)$ 分别为离心率 $e$ 处的空间和时间截止频率。该公式保证了合成斑点的 $(f_s, f_t)$ 恰好落在可见性边界上，在不可见的前提下最大化运动能量注入。

### 振幅估计与对比度掩蔽

振幅 $K_i$ 的估计考虑了背景内容的对比度掩蔽效应。利用拉普拉斯金字塔和对应高斯金字塔层级的比值估计局部 Michelson 对比度：

$$C(\mathbf{x_i}, f_L(i)) = \frac{\mathcal{P}_{lap}^{(\mathbf{x_i}, L(i))}}{\mathcal{P}_{gauss}^{(\mathbf{x_i}, L(i)+1)}}$$

进而通过 CSF 归一化得到感知掩蔽对比度：

$$C_n(\mathbf{x_i}, f_L(i)) = S_{csf}(f_L(i), f_t(i)) \cdot C(\mathbf{x_i}, f_L(i))$$

最终振幅由归一化掩蔽对比度经幂函数变换（指数 $\gamma$）后缩放（系数 $\beta$）得到。$\beta$ 和 $\gamma$ 为可调参数，实验中分别设为 0.3 和 0.5。

### 抗混叠与孔径约束

方法还考虑了两个实际约束（Figure 6）：(1) **Nyquist 率约束**：空间频率不得超过显示器 Nyquist 频率的一半，避免运动混叠；(2) **孔径问题约束**：高斯包络的宽度必须足够大，使得窗口内至少包含一个完整的正弦周期，避免因孔径过小导致运动方向不可分辨。

![[assets/figures/papers/paper_list_l41_https_www_pdf_inf_usi_ch_projects_MotionMetamers_index_html/figures/006_Figure_6.jpg]]
*Figure 6: Motion Considerations (a): The Nyquist-Rate must be respected so that motion aliasing is avoided. (b): The aperture (Gaussian window) size must be adjusted such that the aperture problem is avoided*

### 推理路径总结

完整的推理路径为：输入注视渲染帧 → 金字塔分解 + 运动流估计 → 对每个随机采样的Gabor斑点位置，根据离心率和局部速度计算空间频率 $f_s(i)$（约束在可见性边界上）→ 根据 $f_s(i)$ 和 $v(\mathbf{x_i})$ 计算时间频率 $f_t(i)$ → 根据局部对比度掩蔽计算振幅 $K_i$ → 每帧按 $\phi_v(i)/R$ 更新相位 → 加权叠加所有Gabor斑点 → 叠加到注视渲染帧输出。整个过程无需训练，所有参数通过感知模型解析计算，支持实时推理。

![[assets/figures/papers/paper_list_l41_https_www_pdf_inf_usi_ch_projects_MotionMetamers_index_html/figures/003_Figure_3.jpg]]
*Figure 3: Double-Drift Illusion: In peripheral vision, the visual system integrates the actual motion and the internal drift due to phase change; resulting in a perceived motion that is different from the actual motion of the Gabor stimulus*

## 实验与关键发现

### 核心问题验证：注视渲染导致周边速度感知损失

论文首先通过一个速度匹配实验确认了待解决问题的存在（Figure 2）。被试需要调整测试场景的速度，使其感知速度与一个以固定速度运动的全分辨率参考场景相匹配。测试场景分为全分辨率与注视渲染两种条件。结果显示，当注视渲染场景与全分辨率参考场景在物理上以相同速度运动时，被试系统性地将注视渲染场景感知为更慢——他们需要将注视渲染场景的物理速度调得显著更高才能达到感知等效。这一结果为“注视渲染降低周边空间细节会抑制运动感知”提供了直接的行为学证据（p值来自两组间的t检验）。

### 主实验：速度感知恢复效果

核心用户研究采用速度匹配范式，在Vegetation和City两个场景上评估所提方法（Figure 7a）。场景以三种全局平移速度（低速、中速、高速）运动，注视程度分为Mid和High两档（注视阈值基于场景和速度单独测量，Figure 7b）。14名被试（9男5女，19-25岁，视力正常或矫正至正常）分3个session完成实验以减轻疲劳，被试对实验目的不知情，眼动仪确保中央凹注视，试次随机化。

主要结果以感知速度相对于全质量参考的百分比差异呈现（Figure 8）。0%表示与参考无差异，负值表示感知更慢，正值表示感知更快：

![[assets/figures/papers/paper_list_l41_https_www_pdf_inf_usi_ch_projects_MotionMetamers_index_html/figures/009_Figure_8.jpg]]
*Figure 8: Velocity User-Study Results: Percentage difference in velocity perception with respect to the full-quality reference for foveated and our technique. 0% means no difference with the reference velocity. \<0% means perceived slower compared to the reference. >0% means perceived faster than the reference. The p-values for pairwise t-test’s between the foveated and ours are reported. The error bars represent standard error (SE)*

- **标准注视渲染**：在所有条件下均一致地低估速度，High注视程度下感知速度损失约达-15%。
- **所提方法**：在中、高注视程度下均显著减轻了速度感知损失（配对t检验p<0.05）。High注视程度下，感知速度从约-15%改善至接近参考水平（接近0%）。但在高速条件下出现了轻微的感知速度过冲（perceived faster than reference），提示当前参数校准尚未完全适应所有速度范围。

### 质量感知实验：无引入可察觉伪影

为验证合成运动能量是否引入了可见伪影，进行了全参考2AFC质量偏好实验（Figure 9）。7名被试在Mid和High注视程度、三种速度条件下，判断所提方法与标准注视渲染哪个更接近全分辨率参考的质量/分辨率。结果显示，多数判断偏好所提方法（偏好率>50%），被试未报告引入明显伪影。这表明程序化Gabor噪声合成在周边视觉中成功保持了元映射的不可见性——合成内容落在时空分辨率的不可见边界上（由stelaCSF模型约束），同时有效补偿了运动感知线索。

### 方法有效性的因果机制

所提方法有效性的因果链条可归纳为：

1. **空间频率补偿**：注视渲染通过偏心度依赖的高斯模糊削弱了周边高频空间细节。方法在周边叠加程序化Gabor噪声，合成高频空间纹理（Eq. 1, Eq. 2），其空间频率$f_s(i)$由等敏感度边界$S_{csf}=1$解析求解（Eq. 7），确保合成内容在周边视觉中不可见。
2. **运动能量注入**：每个Gabor斑点的相位以速率$\phi_v(i) = 2\pi f_t(i)$逐帧更新（Eq. 8, Eq. 9），其中时间频率$f_t(i) = \alpha f_s(i) \cdot v(\mathbf{x_i})$与局部运动流速度成正比（Eq. 4）。这种相干相位调制在周边视觉中引入全局运动感知，受“双重漂移错觉”启发（Figure 3）。
3. **感知约束**：合成幅度受背景对比度掩蔽约束（Section 4.4），利用拉普拉斯/高斯金字塔估计局部Michelson对比度，经CSF归一化后控制Gabor斑点的振幅，避免合成内容在已有纹理区域变得可见。

### 局限性与适用边界

论文明确指出的局限性构成方法当前的适用边界：

- **参数校准初步**：$\alpha$（时间频率缩放）、$\beta$（空间频率缩放）、$\gamma$（振幅缩放）的取值基于初步校准，最优值可能随场景内容和运动速度变化。高速条件下的感知过冲现象直接反映了这一局限。
- **仅验证全局平移运动**：实验仅使用全局匀速平移（相机运动），未对加速运动、局部运动、旋转等复杂运动模式进行验证。方法依赖运动流估计，其在复杂运动场景下的鲁棒性未知。
- **仅考察周边视觉**：实验通过遮挡中央凹确保被试仅使用周边视觉，未研究中央凹与周边视觉如何协同形成连贯运动感知。实际注视渲染应用中，用户可在中央凹与周边之间自由切换注视点。
- **合成伪影未完全消除**：边缘存在微弱的条带不连续性（Gabor斑块边界），虽在周边不可见，但未进行平滑处理。在低注视程度或用户注视点快速移动时可能变得可察觉。
- **元映射等价性未充分验证**：当前工作仅验证了速度感知的恢复，未系统研究空间元映射等价是否必然意味着运动感知等价。加速度感知、运动方向辨别等更丰富的运动感知维度尚未测试。

### 实验证据强度评估

| 证据 | 强度 | 说明 |
|------|------|------|
| 注视渲染导致速度感知损失 | 高（p<0.05，Figure 2） | 行为学证据直接，但样本量中等（14人） |
| 所提方法显著恢复速度感知 | 高（p<0.05，Figure 8） | Mid和High注视程度下均显著，但高速条件存在过冲 |
| 合成内容不可见 | 中等（Figure 9偏好率>50%） | 2AFC实验仅7人，需更大样本确认 |
| 参数泛化性 | 低 | 仅两个场景、三种速度，未验证内容和运动多样性 |

需要注意的是，实验中的注视阈值（Figure 7b）是基于每个场景和速度单独测量的，这意味着不同条件下的注视程度并非统一标准，而是相对于各自的可感知阈值定义。这一设计增强了实验的生态效度，但也使得跨条件的直接数值比较需要谨慎解读。

## 定位与知识库关联

本文的核心贡献在于**首次将周边视觉的运动感知损失识别为注视渲染的一个关键瓶颈**，并提出了一种基于程序化Gabor噪声的时空运动能量合成方法来补偿这一损失。相对于已有工作，本文改变的核心 slot 是：**在注视渲染的周边区域，不仅降低空间细节，还主动合成与局部运动流对齐的可控运动能量**。

### 1. 与标准注视渲染的本质差异

标准注视渲染（eccentricity-dependent Gaussian blur）的设计逻辑是“空间保真度随离心率衰减”——它仅控制空间频率的可见性，完全忽略了周边视觉中运动线索的损失。本文的动机实验（Figure 2）直接证明了这一盲区：注视渲染场景的感知速度显著慢于全分辨率参考（p < 0.05），用户需要将注视场景的物理速度调高才能匹配全参考的感知速度。

本文的方法改变了这一局面：**在注视渲染的降质周边区域上叠加程序化Gabor噪声，并通过相位调制引入与局部运动流方向一致的时空运动能量**。这一叠加内容本身被约束在人类视觉系统的时空可分辨边界以下（由 stelaCSF 模型定义，Mantiuk et al. 2022），因此在空间感知上不可见，不引入可察觉伪影，却能恢复被削弱的运动感知线索。

### 2. 知识库挂载点

本文的方法建立在以下知识库节点之上：

- **程序化Gabor噪声合成框架**：直接继承自 Tariq et al. (2022) 的注视渲染空间元映射工作。该工作证明了在周边区域叠加高频Gabor噪声可以实现空间感知的元映射等价（即“看起来一样”）。本文将其扩展到时域：通过控制Gabor斑点的相位变化速率（Eq. 8: $\phi_v(i) = 2\pi f_t(i)$），赋予合成噪声以方向性的运动能量，从而实现“运动感知的元映射等价”。

- **双重漂移错觉（double-drift illusion）**：本文的核心洞察来源于这一经典视觉错觉——在周边视觉中，Gabor刺激的物理位移与内部相位漂移被视觉系统整合，产生不同于实际运动的感知运动（Figure 3）。本文反向利用这一机制：在注视渲染的周边区域，通过相干相位调制“植入”运动能量，补偿因空间细节丢失而削弱的运动线索。

- **时空对比度敏感度模型（stelaCSF）**：Mantiuk et al. (2022) 的 stelaCSF 模型提供了离心率、空间频率、时间频率三者之间的可见性边界。本文利用该模型的等敏感度面（$S_{csf}=1$）推导出空间频率的闭式解（Eq. 7），确保合成内容在任意离心率和运动速度下均处于不可见边界，这是实现“无伪影”补偿的感知基础。

- **对比度掩蔽模型**：基于 Legge & Foley (1980) 的对比度掩蔽理论，本文通过拉普拉斯/高斯金字塔估计背景的 Michelson 对比度（Mantiuk et al. 2021），并据此调制 Gabor 斑点的振幅，防止合成能量在已有高对比度纹理区域产生可见伪影。

### 3. 适用边界与限制

本文的方法和结论受以下边界条件约束：

- **运动类型**：当前验证仅限于全局匀速相机运动（平移）。对于加速运动、局部物体运动、旋转运动等复杂运动模式，方法是否有效尚待验证。这是本文明确指出的开放问题之一。

- **参数校准**：时间频率缩放因子 $\alpha$、以及振幅调制中的 $\beta$、$\gamma$ 等参数的校准基于初步实验，最优值可能随场景内容和运动速度变化。当前方法尚未实现内容自适应的参数调节。

- **中央凹-周边协同**：实验设计通过眼动仪确保被试中央凹注视屏幕中心，周边视觉的刺激完全来自注视渲染的降质区域。这排除了中央凹与周边视觉协同形成运动感知的复杂情况，而实际应用中用户的注视点会自由移动。

- **感知等价性**：本文证明了所提方法能显著减轻速度感知损失，但并未完全消除（部分条件下出现速度感知的轻微过冲，Figure 8）。完全的“运动元映射等价”——即感知速度与全参考无统计显著差异——仍是未达成的目标。

- **下游任务影响**：本文仅验证了低层级的感知指标（速度匹配、质量偏好），运动线索损失对高层级任务表现（如导航决策、交互精度）的影响未被考察。

### 4. 后续启发

本文开辟了“运动元映射”（motion metamers）这一新概念，其核心问题是：**空间感知的元映射等价是否必然蕴含运动感知的元映射等价？** 本文的动机实验给出了否定答案——注视渲染在空间上是可接受的（用户察觉不到周边模糊），但运动感知却显著受损。这提示未来的注视渲染系统需要将运动感知作为一个独立的优化维度。

具体而言，后续工作可以从以下方向展开：
- **内容自适应参数调节**：利用场景的局部运动统计（如运动对比度、加速度）动态调整 $\alpha$ 等参数，以逼近全参考的运动感知。
- **加速度线索的合成**：当前方法仅补偿速度感知，而加速度感知可能依赖于不同离心率区域运动线索的差异，这需要更复杂的时空能量分布设计。
- **与注视预测的集成**：在实际注视渲染系统中，注视点实时变化，中央凹与周边的边界动态移动，如何无缝切换运动能量合成的区域和强度是一个工程挑战。
- **跨模态影响**：运动感知线索的损失是否会影响用户的晕动症（cybersickness）或临场感（presence），是VR/AR应用中值得关注的问题。

## 原文 PDF

![[paperPDFs/SIGGRAPH_2024/Towards_Motion_Metamers_for_Foveated_Rendering.pdf]]