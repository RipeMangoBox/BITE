---
title: Deep Hybrid Camera Deblurring for Smartphone Cameras
type: paper
paper_level: A
venue: SIGGRAPH
year: 2024
pdf_ref: paperPDFs/SIGGRAPH_2024/Deep_Hybrid_Camera_Deblurring_for_Smartphone_Cameras.pdf
project_link: null
code_link: null
aliases:
- DHCDSC
tags:
- SIGGRAPH_2024
- topic/vision_multimodal_applications
core_operator: 利用超广角摄像头同步捕获的突发短曝光图像，提供精确的像素级运动轨迹与高频细节，用于估计模糊核和细化去模糊结果。
primary_logic: 通过混合相机系统同步捕捉不同焦距和帧率的图像，可以从辅助摄像头提取运动轨迹构建准确的模糊核，并在初步去模糊后利用光流精细对齐突发图像进行进一步增强，从而突破单图像和传统参考基方法的瓶颈。
claims:
- HCDeblur 在 HCBlur-Syn 数据集上达到 26.76 PSNR 和 0.7373 SSIM，在 HCBlur-Real 数据集上达到 3.95 NIQE，显著优于所有单图像、参考基和核基去模糊方法。
- 完整 HCDeblur 模型（HC-DNet + FOV + RAFT + HC-FNet + TSA）在 HCBlur-Syn 上获得 26.76/0.7373，移除 HC-DNet 后 PSNR 降至 23.22，替换为 NAFNet-32 仅获 24.05，证明 HC-DNet 和细化模块的关键作用。
- KDB 在不同模糊核利用方案中取得最高 PSNR/SSIM（26.13/0.7251），优于简单拼接、KGC、KAM 和固定偏移量等方法，验证了其学习自适应偏移量的有效性。
- HCBlur-Syn 上 PSNR / SSIM = 26.76 / 0.7373
---

# Deep Hybrid Camera Deblurring for Smartphone Cameras

> [!tip] 核心洞察
> 通过混合相机系统同步捕捉不同焦距和帧率的图像，可以从辅助摄像头提取运动轨迹构建准确的模糊核，并在初步去模糊后利用光流精细对齐突发图像进行进一步增强，从而突破单图像和传统参考基方法的瓶颈。

| 字段 | 内容 |
|------|------|
| 中文题名 | 面向智能手机相机的深度混合相机去模糊 |
| 英文题名 | Deep Hybrid Camera Deblurring for Smartphone Cameras |
| 会议/期刊 | SIGGRAPH 2024 |
| Links | [paper](https://cg.postech.ac.kr/research/HCDeblur/) |
| Topic | #topic/vision_multimodal_applications |
| Method | HCDeblur |
| Dataset | HCBlur-Syn, HCBlur-Real |

> [!tip] 效果简介
> - HCBlur-Syn 上，PSNR / SSIM 26.76 / 0.7373 vs 优于所有对比方法 (显著提升)。
> - HCBlur-Real 上，NIQE 3.95 vs 优于所有对比方法 (显著降低)。

## 概要

智能手机因小传感器需长曝光而常产生严重运动模糊，传统单图像去模糊能力有限，而现有参考基方法受限于对齐误差和低分辨率参考信息。本文提出 **HCDeblur**，一种面向智能手机的深度混合相机去模糊框架，同步捕获宽幅长曝光图像与超广角突发短曝光图像序列，利用突发图像提取像素级运动轨迹构建精确模糊核，并分两阶段进行去模糊与细化。核心网络 **HC-DNet** 基于 U-Net 架构，通过核可变形模块（KDB）自适应利用模糊核进行核基去模糊；**HC-FNet** 则利用光流精细对齐突发图像，通过时空注意力（TSA）融合多帧细节进一步增强结果。在合成数据集 HCBlur-Syn 上，HCDeblur 达到 26.76 PSNR / 0.7373 SSIM；在真实数据集 HCBlur-Real 上，NIQE 降至 3.95，显著优于单图像、参考基及核基去模糊方法。该方法属于**混合相机去模糊**与**核基图像复原**的交叉方向，通过引入同步突发图像作为精确运动信息源，突破了传统方法的瓶颈。

## 核心方法与创新机理

### 问题瓶颈与核心思路

智能手机相机因小尺寸传感器需要较长曝光时间来收集足够光子，导致手持拍摄时极易产生严重的运动模糊。传统单图像去模糊方法（如 NAFNet-64）仅从单张模糊图像出发盲估计模糊核，信息高度不足。参考基方法（如 NAFNet-Ref、LSFNet、D2HNet）虽引入额外短曝光图像作为参考，但在模糊图像与参考图像之间进行直接对齐时面临两难：模糊图像因模糊而缺失高频细节，导致对齐误差大；而参考图像通常分辨率较低，提供的补充信息有限。

HCDeblur 的核心洞察在于：利用现代智能手机普遍配备的多摄像头系统，同步捕获**宽幅长曝光图像**（主摄）和**超广角突发短曝光图像序列**（辅助摄像头）。超广角摄像头因其短曝光特性，帧间冻结了清晰的运动瞬间，可以从突发序列中提取像素级的精确运动轨迹，进而构建高质量的模糊核。这一策略将“从模糊图像盲估计模糊核”的困难问题转化为“从清晰突发序列中测量运动”，从根本上突破了信息瓶颈。

### 框架总览与模块因果链

HCDeblur 框架包含五个顺序级联的处理阶段，如 Figure 2 所示，输入为宽幅长曝光图像 $W$ 和 $N$ 张超广角突发图像序列 $\mathbf{U} = \{U_1, \cdots, U_N\}$：

![[assets/figures/papers/paper_list_l15_https_cg_postech_ac_kr_research_HCDeblur/figures/002_Figure_2.jpg]]
*Figure 2: Overview of HCDeblur. Our framework takes a long-exposure wide image ?? and a burst of short-exposure ultra-wide images U as inputs. We estimate a homography matrix ??ˆ for aligning U in the FOV alignment (Sec. 3.2) and compute pixel-wise motion trajectories P (Sec. 3.2). HC-DNet performs kernel-based deblurring by exploiting blur kernels K constructed from P (Sec. 3.3). After deblurring, an additional alignment step is adopted to align the burst images to the deblurred wide image*

1. **混合相机同步捕获**：利用智能手机的双摄像头同时采集 $W$ 和 $\mathbf{U}$，两者具有不同的视场角（FOV）和曝光时间。
2. **视场对齐与运动估计**：通过平面扫描法估计单应性矩阵，将超广角突发序列对齐到宽幅图像的视场；同时利用 RAFT 光流网络估计突发帧间的像素级运动轨迹。
3. **模糊核构建**：根据运动轨迹和相对时间戳，通过重采样生成与宽幅图像曝光时间对应的固定长度模糊核。
4. **HC-DNet 核基去模糊**：以 $W$ 和模糊核为输入，通过 U-Net 架构配合 NAFBlock 和核心创新模块 KDB（Kernel Deformable Block），利用模糊核引导空间可变的反卷积过程，生成初步去模糊结果 $W_D$。
5. **HC-FNet 突发增强细化**：将超广角突发图像通过光流精细对齐到 $W_D$，利用 TSA（Temporal and Spatial Attention）融合多帧特征，恢复高频细节，输出最终结果。

模块间的因果关系清晰：阶段 2 为阶段 3 提供运动轨迹，阶段 3 为阶段 4 提供模糊核，阶段 4 输出 $W_D$ 后，阶段 5 利用 $W_D$ 作为对齐目标，反过来将突发图像的清晰细节注入最终结果。$W_D$ 的去模糊质量直接影响阶段 5 的对齐精度，进而影响细节增强效果。

### 关键 Changed Slot 1：输入模态与运动信息获取

**Baseline 输入**：单张模糊图像（单图像方法）或模糊图像加一张短曝光参考图像（参考基方法）。

**HCDeblur 输入**：同步捕获的宽幅长曝光图像 $W$ 与超广角突发短曝光序列 $\mathbf{U}$。这一改变的深层价值在于：突发序列帧间的时间间隔极短，每帧几乎无运动模糊，因此帧间光流可以精确刻画手抖和场景运动的轨迹。相比从单张模糊图像中盲估计模糊核，从清晰帧序列中“测量”运动轨迹的难度大幅降低，精度显著提升。

### 关键 Changed Slot 2：对齐策略的分阶段设计

传统参考基方法直接在模糊图像与参考图像之间进行对齐，因模糊图像缺乏高频纹理而鲁棒性差。HCDeblur 将对齐问题分解为两个阶段：

**FOV 对齐（粗对齐）**：针对超广角与宽幅间的视场差异，采用平面扫描法寻找最优深度 $\hat{d}$，通过最小化 MSE 确定单应性矩阵：

$$\hat{d} = \underset{d \in D}{\operatorname{argmin}}\ MSE(W, \mathbb{W}(U_{\mathrm{avg}}, H_d))$$

其中 $H_d = K_u E d K_w^{-1}$ 为逆扭曲单应性，$K_u$、$K_w$ 为内外参矩阵，$E$ 为相对外参。该单应性用于将超广角图像对齐到宽幅视场，对微小不对齐具有天然鲁棒性——因为后续模糊核构建和去模糊过程对亚像素偏移不敏感。

**去模糊后光流对齐（精对齐）**：在 HC-DNet 生成初步去模糊结果 $W_D$ 后，$W_D$ 已恢复大量高频纹理，此时再估计超广角突发图像到 $W_D$ 的光流，可以做到像素级精确对齐，为 HC-FNet 的多帧融合奠定基础。

这一“先粗后精”的对齐策略是 HCDeblur 成功的关键设计：在模糊核阶段避免了对模糊图像做精确对齐的困难，而在需要精细融合的阶段则利用已去模糊的图像作为对齐锚点。

### 关键 Changed Slot 3：模糊核的利用方式——KDB 模块

获得模糊核后，如何将其有效注入去模糊网络是另一核心问题。HCDeblur 设计了 **KDB（Kernel Deformable Block）**，区别于简单的拼接、核全局编码（KGC）或核注意力模块（KAM）。

KDB 的核心机制是**学习自适应偏移量**：对于特征图上的每个空间位置，KDB 利用对应位置的模糊核预测可变形卷积的采样偏移量，使得卷积核能够沿着运动轨迹方向自适应地聚合信息。这相当于让网络在模糊核指示的运动方向上执行“非盲反卷积”，而非仅将模糊核作为全局条件信号。消融实验（Table 3）证实，KDB 在 PSNR/SSIM 上（26.13/0.7251）显著优于 KGC、KAM、MAB 等替代方案，验证了空间自适应偏移量学习在核利用中的有效性。

### 模糊核构建的数学细节

从运动轨迹到模糊核的构建过程如下：

**相对时间戳计算**：对于第 $i$ 张超广角图像，其相对于宽幅图像曝光的相对时间戳为：

$$r_i = \frac{(t_{i,s} + t_{i,e}) / 2 - t_s^W}{t_s^W - t_e^W}$$

其中 $t_{i,s}$、$t_{i,e}$ 为超广角图像的曝光起止时间，$t_s^W$、$t_e^W$ 为宽幅图像的曝光起止时间。

**模糊核插值**：对于宽幅曝光区间内的任意时间戳 $t$，通过线性插值生成对应模糊核：

$$K_t = (t - r_i) \cdot \frac{\hat{P}_{i+1} - \hat{P}_i}{r_{i+1} - r_i} + \hat{P}_i$$

其中 $\hat{P}_i$ 为第 $i$ 帧处的累积运动轨迹。最终通过重采样获得固定长度的模糊核序列，覆盖宽幅图像的整个曝光周期。

### 网络架构细节

**HC-DNet**（Figure 4）：采用 U-Net 架构，编码器和解码器的每个层级由 NAFBlock 组成。KDB 模块嵌入在编码器-解码器之间的跳跃连接处，利用模糊核调制特征。NAFBlock 提供高效的非线性变换能力，而 KDB 负责将模糊核的空间信息注入特征图。

**HC-FNet**（Figure 5）：将超广角突发图像通过光流扭曲对齐到 $W_D$ 后，逐帧经过 NAFBlock 提取特征，随后通过 TSA 模块进行时空注意力融合。TSA 同时建模时间维度（跨帧）和空间维度（跨像素）的依赖关系，使网络能够自适应地选择最清晰的帧区域来增强 $W_D$ 的细节。消融实验（Table 2）表明，TSA 优于简单的平均融合和转置注意力，验证了时空联合建模对突发图像融合的必要性。

### 训练与推理路径

**训练策略**：HC-DNet 和 HC-FNet 分阶段训练。HC-DNet 先以 $W$ 和模糊核为输入、清晰图像为监督信号训练 300,000 次迭代（batch size 32，patch size 384）。HC-FNet 在 HC-DNet 固定后训练 150,000 次迭代（batch size 8），输入为 $W_D$ 和对齐后的突发图像特征。分阶段训练保证了各模块的稳定收敛。

**推理路径**：输入 $W$ 和 $\mathbf{U}$ → RAFT 估计突发帧间光流 → 构建运动轨迹和模糊核 → FOV 对齐 → HC-DNet 生成 $W_D$ → 光流对齐突发图像到 $W_D$ → HC-FNet 融合输出最终结果。主要计算瓶颈在 RAFT 光流估计，当突发大小为 8 时，单次推理约需 4 秒，主要限制了实时应用。

### 局限性锚点

该方法的核心假设是超广角突发图像能够提供可靠的帧间光流。在极暗环境或纹理缺失区域，光流估计可能失败，导致运动轨迹和模糊核质量下降，进而影响整体去模糊性能。此外，RAFT 的计算开销是当前框架的主要效率瓶颈。

![[assets/figures/papers/paper_list_l15_https_cg_postech_ac_kr_research_HCDeblur/figures/001_Figure_1.jpg]]
*Figure 1: Our hybrid camera system and deblurred results. We simultaneously capture a long-exposure wide image ?? and short-exposure burst ultra-wide images U from a smartphone, and utilize the burst images to deblur ?? . Our method produces significantly sharper results compared to NAFNet-64 [Chen et al. 2022], a state-of-the-art single-image deblurring method*

![[assets/figures/papers/paper_list_l15_https_cg_postech_ac_kr_research_HCDeblur/figures/005_Figure_4.jpg]]
*Figure 4: Architecture of HC-DNet*

## 实验与关键发现

### 核心定量结果

HCDeblur 在两个专门构建的混合相机去模糊基准上均取得最优性能。在合成数据集 HCBlur-Syn 上，完整模型达到 **26.76 PSNR** 和 **0.7373 SSIM**（Table 1），显著超越所有对比方法。在真实数据集 HCBlur-Real 上，由于缺乏真值参考，采用无参考指标评估：HCDeblur 获得 **3.95 NIQE**，同样大幅领先其他方法（Table 1）。

![[assets/figures/papers/paper_list_l15_https_cg_postech_ac_kr_research_HCDeblur/figures/006_Table_1.jpg]]
*Table 1: Quantitative comparisons on the HCBlur-Syn and HCBlur-Real datasets. For the HCBlur-Real dataset, we use noreference metrics (i.e., NIQE [Mittal et al. 2012b], BRISQUE [Mittal et al. 2012a], and TOPIQ [Chen et al. 2024] trained on SPAQ [Fang et al. 2020]) for evaluation. The number of parameters, MACs, and inference times of the kernel-based deblurring methods and HCDeblur include those for the optical flow estimation when the burst size of U is eight. HCDeblursmall indicates a lightweight version of HCDeblur, which uses a smaller version of RAFT [Teed and Deng 2020]*

对比基线涵盖三类代表性方法：
- **单图像去模糊**：NAFNet-64 仅能利用长曝光宽幅图像自身信息，缺乏运动先验，性能受限。
- **参考基去模糊**：NAFNet-Ref（NAFNet 扩展）、LSFNet、D2HNet 等方法虽引入了短曝光参考图像，但受限于对齐误差和低分辨率参考信息，无法充分利用突发序列中的运动线索。
- **核基去模糊**：MotionETR、UFPNet 依赖从单张模糊图像盲估计模糊核，在复杂运动场景下核估计精度不足。

值得注意的是，即使仅使用 HC-DNet（不含 HC-FNet 细化模块），模型在 HCBlur-Syn 上仍能超越所有竞争对手，表明从超广角突发序列构建的精确模糊核本身已提供强判别性运动信息。

### 消融实验与因果链路

**HC-DNet 的核心作用**（Table 2）：完整 HCDeblur 在 HCBlur-Syn 上取得 26.76/0.7373。移除 HC-DNet 后，PSNR 骤降至 **23.22**（降幅 3.54 dB），SSIM 降至 0.6671。若将 HC-DNet 替换为单图像去模糊网络 NAFNet-32，仅获得 **24.05 PSNR**，仍远低于完整模型。这验证了两个关键因果链路：① 从突发序列提取的运动轨迹构建的模糊核提供了单图像方法无法获取的精确退化信息；② HC-DNet 中的核可变形模块（KDB）能有效利用该模糊核进行自适应去模糊。

**模糊核利用策略对比**（Table 3）：系统对比了五种核利用方案，KDB 取得最高 **26.13 PSNR / 0.7251 SSIM**。简单拼接核与图像特征效果最差；核全局上下文（KGC）、核注意力机制（KAM）、多尺度自适应块（MAB）等方案虽有所改善，但 KDB 通过学习自适应偏移量，使卷积核形状随模糊核变化，实现了更精确的像素级去模糊。

**对齐策略的递进验证**（Table 2）：仅使用 FOV 对齐（通过平面扫描估计单应性矩阵）时性能有限；引入 RAFT 光流估计进行运动轨迹计算后，性能显著提升，优于使用 BIPNet 光流网络的变体。这证明精确的像素级运动估计对模糊核质量至关重要——FOV 对齐解决了宽幅与超广角间的视场差异，而 RAFT 光流提供了突发帧间的精细运动信息。

**HC-FNet 融合策略**（Table 2）：时间空间注意力（TSA）融合优于简单平均融合和转置注意力，验证了在突发序列帧间进行自适应时空特征聚合对细节增强的有效性。TSA 机制使网络能选择性关注不同帧中恢复良好的区域，抑制对齐残留误差的影响。

### 失败模式与适用边界

**计算开销瓶颈**：框架依赖大型光流网络 RAFT 在突发图像间计算密集光流场，单次推理约需 4 秒，难以满足设备端实时应用需求。论文提出了轻量版 HCDeblur-small（使用小型 RAFT），但性能与效率的权衡仍需进一步探索。

**极端场景退化风险**：在极暗环境或纹理稀少区域，光流估计可能失效，导致运动轨迹不准确，进而影响模糊核质量和最终去模糊效果。这是基于光流的运动估计方法的固有限制，论文未提供针对此类场景的鲁棒性实验或应对策略。

**硬件依赖**：方法假设智能手机具备同步捕获宽幅长曝光与超广角突发短曝光的能力，这对相机硬件和 ISP 管道提出特定要求，限制了方法在普通单摄设备上的适用性。

### 实验公平性保障

所有对比方法均在 HCBlur-Syn 数据集上重新训练以确保公平比较。对于参考基方法，使用超广角图像的中心帧经上采样和 FOV 对齐后作为参考输入，适配其单帧参考的设计要求。对于核基方法，使用从超广角突发序列估计的模糊核替换其原有单图像盲核估计模块后重新训练，确保比较的是核利用方式而非核估计能力差异。

![[assets/figures/papers/paper_list_l15_https_cg_postech_ac_kr_research_HCDeblur/figures/007_Table_2.jpg]]
*Table 2: Ablation study for variants of HCDeblur. We compare its performance without HC-DNet and with NAFNet-32 [Chen et al. 2022], evaluate different alignment modules (RAFT [Teed and Deng 2020] vs BIPNet [Dudhane et al. 2022]) after the FOV alignment, and examine burst features fusion strategies like averaging (Avg.), transposed attention (Trans Att.) [Mehta et al. 2023], and temporal and spatial attention (TSA) [Wang et al. 2019]*

![[assets/figures/papers/paper_list_l15_https_cg_postech_ac_kr_research_HCDeblur/figures/008_Table_3.jpg]]
*Table 3: Comparison of different schemes for exploiting blur kernels*

## 定位与知识库关联

HCDeblur 的核心定位是：**在智能手机混合相机系统的硬件条件下，将单图像去模糊问题转化为“核估计+多帧参考增强”的双阶段问题**。其相对已有方法的本质差异在于同时改变了四个关键 slot：

1. **输入模态 slot**：从单张长曝光图像或“模糊+单张短曝光参考”对，变为同步捕获的宽幅长曝光图像与超广角突发短曝光序列 $\mathbf{U} = \{U_1, \cdots, U_N\}$。这一变化直接打破了单图像去模糊的欠定性和传统参考基方法中参考信息时空分辨率不足的瓶颈。

2. **运动/模糊核估计 slot**：从盲估计或无核先验，变为利用超广角突发图像间的光流场构建像素级运动轨迹，再通过时间戳重采样生成固定长度模糊核。这提供了物理上更精确的退化模型先验，而非依赖网络隐式学习。

3. **对齐策略 slot**：传统参考基方法（如 **NAFNet-Ref**、**LSFNet**、**D2HNet**）直接对模糊图像与参考图像进行单应性或光流对齐，在严重模糊下误差较大。HCDeblur 采用两阶段对齐——对模糊核使用 FOV 对齐（通过平面扫描法寻找最优深度 $\hat{d}$ 下的单应性 $H_d = K_u E d K_w^{-1}$，对微小不对齐鲁棒），对去模糊后图像再使用 RAFT 进行光流精细对齐——将困难的对齐问题分解到合适的处理阶段。

4. **细化过程 slot**：从无额外细化或简单单帧融合，变为利用全部突发参考图像通过 HC-FNet 进行多帧特征融合与细节增强，采用 TSA 注意力机制聚合时序和空间信息。

### 知识库挂载点

HCDeblur 可挂载到以下知识库节点：

- **多帧/突发图像去模糊**：与传统的突发去模糊方法（利用多帧短曝光融合去噪/去模糊）不同，HCDeblur 的突发图像来自不同焦距的辅助摄像头，且主要用于核估计和后期细化，而非直接融合。这扩展了“突发处理”的应用范式。

- **参考基图像恢复**：相比于 **D2HNet** 等需要精确对齐的参考基方法，HCDeblur 通过 FOV 对齐和两阶段策略降低了对齐精度要求。其核心启示是：**当参考图像与目标图像存在视场差异时，在核空间而非图像空间进行初始对齐可能更鲁棒**。

- **核基去模糊**：不同于 **MotionETR**、**UFPNet** 等从单张模糊图像盲估计核的方法，HCDeblur 从辅助摄像头直接观测运动轨迹，核的物理精度更高。HC-DNet 中的 KDB 模块提供了将物理核注入深度网络的范例——通过学习自适应偏移量而非固定核卷积，平衡了核先验的利用与网络的学习自由度。

- **混合相机系统**：HCDeblur 属于利用多摄像头异构性进行计算摄影的范式，与超分辨率中的混合变焦融合、深度估计中的立体匹配等方法共享“多摄协同”的思想，但具体实现路径（同步捕获、不同帧率、核估计+细化）是新的。

### 适用边界与局限

HCDeblur 的适用边界受以下因素制约：

1. **硬件依赖**：要求智能手机具备可同步捕获的超广角和宽幅摄像头，且超广角摄像头需支持突发短曝光模式。这并非所有设备都具备。

2. **计算开销**：框架依赖大型光流网络 RAFT 在突发图像间计算光流，单次推理约需 4 秒，难以在设备端实时应用。这是限制其实际部署的主要瓶颈。

3. **场景鲁棒性**：在极暗或纹理稀少场景下，光流估计可能失败，进而影响模糊核质量和去模糊性能。这意味着方法在低光条件下的可靠性需要进一步验证。

4. **数据集泛化**：实验在自建的 HCBlur-Syn 和 HCBlur-Real 数据集上进行，虽然覆盖了多种场景，但其泛化到不同手机型号、不同摄像头配置的能力尚未验证。

### 后续启发与可迁移价值

1. **轻量化方向**：用更高效的轻量级网络替代 RAFT 以降低推理延时，是该工作最直接的改进方向。消融实验已表明 FOV + RAFT 优于 FOV + BIPNet，但仍有探索更高效光流估计的空间。

2. **核注入机制的泛化**：KDB 模块中“学习自适应偏移量”的思想可迁移到其他需要利用物理先验的图像恢复任务，如去雾（利用大气散射模型）、去反射（利用反射层估计）等。

3. **两阶段对齐策略的启示**：在核空间进行粗对齐、在图像空间进行细对齐的策略，可推广到其他涉及多源图像融合的任务，特别是当输入图像之间存在视场差异和严重退化时。

4. **鲁棒性增强**：针对低纹理/低光照场景的光流估计失败问题，可探索引入惯性传感器（IMU）数据作为运动估计的补充线索，或设计对光流误差具有鲁棒性的核构建和去模糊模块。

## 原文 PDF

![[paperPDFs/SIGGRAPH_2024/Deep_Hybrid_Camera_Deblurring_for_Smartphone_Cameras.pdf]]