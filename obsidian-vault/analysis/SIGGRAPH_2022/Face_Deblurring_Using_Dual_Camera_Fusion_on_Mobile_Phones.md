---
title: Face Deblurring Using Dual Camera Fusion on Mobile Phones
type: paper
paper_level: A
venue: SIGGRAPH
year: 2022
pdf_ref: paperPDFs/SIGGRAPH_2022/Face_Deblurring_Using_Dual_Camera_Fusion_on_Mobile_Phones.pdf
project_link: "https://www.wslai.net/publications/fusion_deblur/"
code_link: null
aliases:
- FDDCF
- FDUDCFMP
tags:
- SIGGRAPH_2022
- topic/vision_multimodal_applications
- topic/benchmarks_datasets_evaluation
core_operator: 同步启用超广角(UW)参考摄像头并设置N倍快速快门（如1/4或1/2曝光时间）获取清晰但噪声高的参考图像，将盲去模糊转化为显式参考引导的融合问题。
primary_logic: 利用现代手机普遍搭载的双摄系统（主摄+超广角），构建轻量级对齐（PWC-Net）与融合（FusionNet）流水线，仅在人脸区域工作，实现实时、高分辨率、高质量的人脸去模糊。
claims:
- 在Pixel 6上单次拍摄额外延迟仅463 ms，峰值内存增加264 MB，功耗468 mW，达到交互速率
- 在1783张包含多种运动、肤色、性别的真实场景图像上，NIMA无参考感知质量均优于MPRNet、MIMO-UNet、UMSN、BurstDeblurring、UHDVD、PVDNet及iPhone 13 Pro等商业产品
- 消融实验证明，移除参考图像、去除色彩一致性损失、或取消合成光斑数据增强均会导致去模糊质量显著下降
- In-house dataset (1783 real-world motion-blurred face images) 上 NIMA (no-reference perceptual quality) = highest median score
---

# Face Deblurring Using Dual Camera Fusion on Mobile Phones

> [!tip] 核心洞察
> 利用现代手机普遍搭载的双摄系统（主摄+超广角），构建轻量级对齐（PWC-Net）与融合（FusionNet）流水线，仅在人脸区域工作，实现实时、高分辨率、高质量的人脸去模糊。

| 字段 | 内容 |
|------|------|
| 中文题名 | 利用双摄融合的手机人脸去模糊 |
| 英文题名 | Face Deblurring Using Dual Camera Fusion on Mobile Phones |
| 会议/期刊 | SIGGRAPH 2022 |
| Links | [paper](https://www.wslai.net/publications/fusion_deblur/) · [Project](https://developer.android.com/guide/topics/media/camera) |
| Topic | #topic/vision_multimodal_applications #topic/benchmarks_datasets_evaluation |
| Method | Face Deblurring via Dual Camera Fusion |
| Dataset | In-house dataset, Runtime on Google Pixel 6, Desktop GPU latency |

> [!tip] 效果简介
> - In-house dataset (1783 real-world motion-blurred face images) 上，NIMA (no-reference perceptual quality) highest median score vs lower scores (MPRNet, MIMO-UNet, UMSN, etc.) (significant improvement)；ΔNIMA (NIMA difference before/after deblurring) consistently positive improvement vs some methods show score regression (ΔNIMA < 0) (robust improvement across conditions)。
> - Runtime on Google Pixel 6 上，Latency overhead per shot 463 ms vs baseline single-camera shot (463 ms extra)。
> - Desktop GPU latency (768×768, NVidia Quadro P5000) 上，Inference time 27 ms (FusionNet) vs MPRNet: 234 ms, MIMO-UNet: 52 ms (~1.9–8.7× faster)。

## 概要

针对手机拍摄运动人脸时，因传感器尺寸限制与交流照明闪烁，单摄像头无法使用高速快门导致的严重运动模糊问题，本文提出一种基于双摄融合的人脸去模糊系统。核心思路是将盲去模糊转化为显式参考引导的融合：同步启用超广角参考摄像头，以主摄快门速度的N倍（N=2或4）捕获清晰但高噪的参考图像，再通过轻量级光流对齐（PWC-Net）与融合网络（FusionNet）仅在人脸区域恢复清晰细节。该系统在Google Pixel 6上单次拍摄额外延迟仅463 ms，峰值内存增加264 MB，功耗468 mW，达到交互速率。在1783张涵盖多运动、肤色、性别及光照条件的真实场景图像上，NIMA无参考感知质量优于MPRNet、MIMO-UNet、UMSN等学术方法及iPhone 13 Pro等商业产品。该方法属于参考引导的图像融合范式，区别于传统单图/多帧盲去模糊路线，为移动端高质量计算摄影提供了实用的双摄协同方案。

## 核心方法与创新机理

### 问题瓶颈与核心机制

在移动端拍摄运动人脸时，由于传感器尺寸限制和AC照明闪烁（图2），主摄（Wide, W）无法在低光下使用高速快门，导致人脸区域出现严重的非刚体运动模糊。传统单图像去模糊方法（如MPRNet、MIMO-UNet）试图从单一模糊输入中盲恢复清晰图像，但面对大运动模糊时往往产生伪影或过度平滑；多帧方法（如BurstDeblurring）虽能利用时序信息，却无法处理人脸的非刚体形变。

本文的核心洞察在于：**利用现代手机普遍搭载的双摄系统（主摄W+超广角UW），将盲去模糊问题转化为显式参考引导的融合问题**。具体而言，系统在检测到运动模糊后，同步启用UW摄像头并以N倍快速快门（N=2或4，即曝光时间为W的1/2或1/4）捕获一帧清晰但噪声高、分辨率低的参考图像。该参考图像虽存在严重的传感器噪声和可能的闪烁条纹，却保留了人脸的关键高频细节。随后的核心任务变为：将W的低噪声模糊图像与UW的高噪声清晰参考进行对齐与融合，生成干净且清晰的人脸线性RAW。

### 关键Changed Slots

相较于现有方法，本工作在四个关键维度上做出了系统性改变：

1. **输入模态**：从单摄像头单帧/多帧输入，变为同步双摄（W+UW）RAW burst对。每个摄像头捕获7-9帧RAW，经鲁棒局部对齐（Hasinoff et al., 2016）合并为单张线性RAW后再送入后续管线。
2. **去模糊策略**：从盲去卷积或端到端单图CNN，变为基于显式清晰参考的对齐-融合范式。参考图像提供了真实的高频细节先验，使网络无需从模糊输入中“猜测”丢失的纹理。
3. **计算域**：从全图或全视频处理，变为仅在人脸ROI内操作。系统检测最大人脸框，扩展1.75倍以覆盖头发、耳朵和下巴，并向上取整至最大1536×1536像素进行推理，大幅降低计算量。
4. **快门控制**：UW快门锁定为W的1/N，曝光时间由W的自动曝光参数推导，确保参考图像在相同光照条件下捕获足够的运动冻结能力。

### 流水线模块与因果链路

系统整体流水线如图3和图4所示，包含以下顺序模块：

#### 1. 人脸检测与ROI提取（Section 3.1）

系统在W源图像上检测最大人脸框（红色框），扩展1.75倍得到覆盖全脸的蓝色框，再向上取整至1536×1536的绿色框作为融合ROI。随后使用基于UNet的主体分割网络（Wadhwa et al., 2018）在ROI内生成平滑的人脸掩模 $M_{\text{face}}$，用于后续融合时的区域引导和最终混合的羽化过渡。

#### 2. 色彩匹配（Section 3.1）

W和UW摄像头具有不同的色彩响应特性，直接融合会产生色彩不一致。系统通过两步进行色彩归一化：

**色彩空间转换**：利用预标定的色彩转换矩阵（CCM），将参考图像从UW色彩空间转换到W色彩空间：
$$I_{\mathrm{ref}}^{n} = CCM_{\mathrm{src}}^{-1} \cdot CCM_{\mathrm{ref}} \cdot I_{\mathrm{ref}} \tag{1}$$

**全局均值匹配**：为进一步对齐整体亮度，对归一化后的参考图像按RGB通道分别除以自身均值再乘以源图像对应通道均值：
$$\hat{I}_{\mathrm{ref}} = \frac{I_{\mathrm{ref}}^{n}}{\mu_{\mathrm{ref}}} \cdot \mu_{\mathrm{src}} \tag{2}$$

这两步确保了参考图像在色彩和亮度上与源图像大致一致，为后续光流估计和融合提供良好的输入条件。

#### 3. PWC-Net对齐（Section 3.2）

双摄之间存在基线视差，且人脸可能发生非刚体运动，需要密集的光流对齐。系统采用PWC-Net估计前向光流，但面临一个关键挑战：W和UW之间的位移量通常远超光流训练数据（如Sintel）中的运动幅度，直接在全分辨率上运行PWC-Net会导致严重的流估计错误和扭曲（图6(c)）。

**解决方案**：将源图像和色彩匹配后的参考图像进行4倍下采样后再送入PWC-Net，估计出的光流再上采样回原始分辨率：
$$F_{\mathrm{fwd}} = \mathrm{PWCNet}((I_{\mathrm{src}})_{\downarrow}, (\hat{I}_{\mathrm{ref}})_{\downarrow})_{\uparrow} \tag{3}$$

这一简单的尺度调整使光流估计的搜索范围有效扩大了4倍，显著提升了对齐质量（图6(d)）。随后使用前向光流对参考图像进行双线性扭曲：
$$I_{\mathrm{ref}}' = \mathbb{W}(\hat{I}_{\mathrm{ref}}; F_{\mathrm{fwd}}) \tag{4}$$

为满足移动端实时性要求，PWC-Net经过了针对性优化（减少特征金字塔层数、压缩通道数），将延迟从113 ms降至13 ms，内存占用从600 MB降至34 MB，模型大小从40 MB压缩至1.27 MB，代价是Sintel训练集上的平均端点误差（EPE）从2.91升至3.73。

#### 4. 遮挡掩模生成（Section 3.2）

光流扭曲在遮挡区域会产生严重的伪影。系统通过前向-后向流一致性检查生成遮挡掩模：对每个像素 $\mathbf{x}$，计算其经前向流扭曲后再经后向流扭曲后的位置与原始位置的距离，缩放后截断至 $[0,1]$：
$$M_{\mathrm{occ}}(\mathbf{x}) = \min(s \cdot || \mathbb{W}(\mathbb{W}(\mathbf{x}; F_{\mathrm{fwd}}); F_{\mathrm{bwd}}) - \mathbf{x} ||_2, 1.0) \tag{5}$$

其中 $s$ 为缩放因子。该掩模在融合时告知网络哪些区域的参考信息不可靠，应更多依赖源图像。

#### 5. FusionNet融合（Section 3.3）

FusionNet是整个流水线的核心学习模块，采用残差UNet变体架构（图7），具有7个尺度的编码器-解码器结构。其输入为四通道堆叠：源图像 $I_{\mathrm{src}}$、扭曲后的参考图像 $I_{\mathrm{ref}}'$、人脸掩模 $M_{\mathrm{face}}$ 和遮挡掩模 $M_{\mathrm{occ}}$。参考图像及相关掩模在输入时被下采样至源图像的一半尺寸，以降低计算量。

FusionNet学习预测残差图，叠加源图像得到融合结果：
$$I_{\mathrm{fused}} = \mathrm{FusionNet}(I_{\mathrm{src}}, I_{\mathrm{ref}}', M_{\mathrm{face}}, M_{\mathrm{occ}}) + I_{\mathrm{src}} \tag{6}$$

这一全局残差学习策略使得网络专注于恢复模糊丢失的高频细节，而将低频结构交由源图像保持，有效避免了色彩偏移和结构失真。

**训练数据合成**：由于难以获取真实场景下完美对齐的模糊-清晰-参考三元组，系统通过合成方式构建训练数据。以清晰的W图像作为真值 $I_{\mathrm{GT}}$，在其人脸区域施加随机采样的运动模糊核 $k$ 和鬼影效应，并在非人脸区域保留原始清晰像素：
$$I_{\mathrm{src}} = M_{\mathrm{blur}} \cdot (I_{\mathrm{GT}} \otimes k) + (1 - M_{\mathrm{blur}}) \cdot I_{\mathrm{GT}} + n \tag{7}$$

其中 $M_{\mathrm{blur}}$ 为模糊区域掩模，$n$ 为模拟噪声。参考图像则通过对 $I_{\mathrm{GT}}$ 添加符合UW特性的强噪声和可能的闪烁条纹来模拟。训练集包含约2594对W-UW图像。

**损失函数**：总损失由三项加权组成：
$$\mathcal{L} = w_{\mathrm{content}}\mathcal{L}_{\mathrm{content}} + w_{\mathrm{vgg}}\mathcal{L}_{\mathrm{vgg}} + w_{\mathrm{color}}\mathcal{L}_{\mathrm{color}} \tag{11}$$

- **内容损失** $\mathcal{L}_{\mathrm{content}} = ||I_{\mathrm{fused}} - I_{\mathrm{GT}}||_1$：像素级L1保真度。
- **感知损失** $\mathcal{L}_{\mathrm{vgg}} = \sum_j w_j ||VGG_j(I_{\mathrm{fused}}) - VGG_j(I_{\mathrm{GT}})||_1$：预训练VGG19多层特征的加权L1损失，促进纹理真实性。
- **色彩一致性损失** $\mathcal{L}_{\mathrm{color}} = ||\mathcal{G}_{\sigma}(I_{\mathrm{fused}}) - \mathcal{G}_{\sigma}(I_{\mathrm{src}})||_1$：对融合结果和源图像分别施加 $\sigma=20$ 的高斯模糊后计算L1损失，强制局部色彩与源图像一致，防止参考图像的色彩污染（如发丝上的绿色偏色）。

权重设置为 $w_{\mathrm{content}}=1, w_{\mathrm{vgg}}=2, w_{\mathrm{color}}=1$。

#### 6. 混合与后处理（Section 3.4, 3.5）

融合后的线性RAW人脸通过alpha混合无缝嵌入回全分辨率W图像，alpha值由人脸掩模的羽化边界决定。最后经全局色调映射和Polyblur锐化增强，输出最终的去模糊照片。

### 因果链路总结

整个系统的因果链路清晰且可解释：**运动检测触发UW同步捕获** → **快速快门冻结运动但引入噪声** → **色彩匹配消除摄像头间色彩差异** → **下采样光流解决大位移对齐** → **遮挡掩模抑制扭曲伪影** → **残差UNet融合噪声参考的高频细节与模糊源的低频结构** → **色彩一致性损失防止色彩污染** → **ROI限制计算开销**。每个模块针对前序模块的输出缺陷进行补偿，形成完整的因果闭环。

![[assets/figures/papers/paper_list_l41_https_www_wslai_net_publications_fusion_deblur/figures/001_Figure_1.jpg]]
*Figure 1: We present a robust and efficient system that leverages synchronized dual capture, which is commonly available on mobile phones, to deblur faces at an interactive rate on mobile devices. Input (a): In this setting where the subject performs ordinary exercise (jumping on a trampoline), the commercial-grade auto-exposure system equipped with high-sensitivity sensor from a modern premium phone still produces objectionable motion blur on the face region. Reference (b): Our system detects the subject motion and uses the ultrawide camera to capture a short-exposure shot as reference simultaneously. While the image appears noisy, has low-resolution, and has wrong color, it preserves the subject’s...*

![[assets/figures/papers/paper_list_l41_https_www_wslai_net_publications_fusion_deblur/figures/003_Figure_3.jpg]]
*Figure 3: System overview. Our system takes raw bursts from W and UW. We control the shutter speed of UW to be 4× faster than W. UW image is sharper but appears noisier and may contain flickering, i.e., the vertical bands in the image, due to rolling shutter under artificial lighting. We merge the burst raw into a linear RAW, and crop the face region for deblurring using ML-based alignment (Section 3.2) and fusion (Section 3.3). Detailed steps are described in Figure 4. We then blend the deblurred face back to W (Section 3.4), and outputs the final image through tone mapping and post-processing (Section 3.5). Note that the reference image size is 2× smaller than the source. We enlarge the reference i...*

![[assets/figures/papers/paper_list_l41_https_www_wslai_net_publications_fusion_deblur/figures/007_Figure_7.jpg]]
*Figure 7: FusionNet architecture. The model is a variant of residual UNet for multi-scale processing. The model takes inputs from the blurry source and stacked tensors consisting of the reference image, face mask, and occlusion mask at half the size of the source image*

![[assets/figures/papers/paper_list_l41_https_www_wslai_net_publications_fusion_deblur/figures/010_Figure_10.jpg]]
*Figure 10: Adaptive Streaming Design. The adaptive streaming system resides in the camera driver, passing camera metadata to the ML classifier to identify if the human face is suffering from motion blur, and turns on the UW camera dynamically*

## 实验与关键发现

### 评估体系与数据集

由于双摄人脸去模糊无法在现有公开基准上评测，作者构建了一个包含1783张真实场景运动模糊人脸图像的内部数据集，覆盖多种肤色、性别、年龄、面部姿态以及室内/室外/低光照明条件。评估采用无参考感知质量指标 **NIMA**（Talebi & Milanfar 2018），并引入 **ΔNIMA**（去模糊前后的NIMA差值）衡量各方法的改善幅度——ΔNIMA为正表示质量提升，为负则表示方法反而破坏了原图质量。

### 主结果：感知质量对比

在1783张真实图像上，本文方法在NIMA中位数上显著优于所有对比方法（Figure 13(a)）。更重要的是，从ΔNIMA分布来看（Figure 13(b)），本文方法始终给出正向改善，而若干基线方法出现NIMA评分倒退（ΔNIMA < 0），表明它们对部分输入不仅没有去模糊效果，反而引入了伪影或过度平滑。

![[assets/figures/papers/paper_list_l41_https_www_wslai_net_publications_fusion_deblur/figures/013_Figure_13.jpg]]
*Figure 13: Quantitative evaluation. (a) We calculate the no-reference image quality metric using NIMA [Talebi and Milanfar 2018]. Our method outperforms others and achieves the best perceptual quality. (b) We compute the ΔNIMA by subtracting the NIMA score before and after the deblurring. Some methods lead to NIMA score regression (ΔNIMA\< 0 within one standard deviation range), while our method robustly shows improvement*

对比对象涵盖：
- **单图像去模糊**：MPRNet（Zamir et al., CVPR 2021）、MIMO-UNet（Cho et al., ICCV 2021）
- **单图像人脸去模糊**：UMSN（Yasarla et al., IEEE TIP 2020）
- **多帧去模糊**：BurstDeblurring（Aittala & Durand, ECCV 2018）
- **视频去模糊**：UHDVD（Deng et al., CVPR 2021）、PVDNet（Son et al., ACM SIGGRAPH 2021）
- **商业产品**：iPhone 13 Pro、Adobe Photoshop Shake Reduction、Samsung Gallery Remaster

定性结果显示（Figure 12, Figure 14），MPRNet和MIMO-UNet等单图像方法在处理大幅度面部运动模糊时往往无法恢复清晰细节，产生模糊或伪影残留；视频去模糊方法UHDVD和PVDNet由于依赖多帧时序信息，在单次拍摄场景下效果有限；商业方案中，iPhone 13 Pro和Samsung Gallery Remaster对面部模糊的改善幅度明显不及本文方法，Adobe Photoshop Shake Reduction则容易引入振铃伪影。

### 运行效率

**桌面端延迟**（Table 1）：在768×768分辨率、NVIDIA Quadro P5000 GPU上，FusionNet单帧推理仅需 **27 ms**，相比之下MPRNet为234 ms（约8.7×），MIMO-UNet为52 ms（约1.9×）。PWC-Net光流估计在桌面端耗时为13 ms（优化后）。

**移动端延迟**（Table 2）：在Google Pixel 6上，整个系统相对于普通单摄拍摄的额外延迟仅 **463 ms**，峰值内存增加 **264 MB**，功耗 **468 mW**，达到交互速率。这一开销涵盖了人脸检测、PWC-Net对齐、FusionNet推理及后处理的完整流水线。

### 关键消融实验

消融实验系统性地验证了每个设计选择的因果贡献：

**1. 参考图像的必要性**（Figure 16）。移除参考图像后，模型退化为单图像去模糊方法，无法处理大幅度运动模糊，面部细节恢复失败，产生不自然的伪影。这直接证明了双摄参考引导是系统有效性的核心前提——盲去模糊在面对大运动时缺乏足够的先验信息。

**2. 色彩一致性损失**（Figure 15）。去除色彩一致性损失 $\mathcal{L}_{\text{color}}$ 后，参考图像的色彩偏差（如头发区域的绿色偏色）会传递到融合结果中。该损失通过对高斯模糊后的局部区域施加L1约束，有效抑制了跨摄像头色彩不一致。

**3. 合成光斑数据增强**（Figure 17）。训练时若不加入合成高光条纹，模型无法抑制眼球上的饱和光斑或反射区域，在饱和像素周围产生可见的振铃伪影。这一发现表明，真实运动模糊中伴随的镜面高光拖影是影响去模糊质量的关键退化模式，必须在训练数据中显式建模。

**4. 感知损失**（Figure 20）。去除VGG感知损失 $\mathcal{L}_{\text{vgg}}$ 后，FusionNet倾向于生成过度平滑的结果，尤其在眼镜框等高频结构区域出现振铃或模糊。L1内容损失单独不足以保持纹理真实性。

**5. 遮挡掩码**（Figure 25）。移除遮挡掩码后，参考图像在面部边界或背景区域的扭曲伪影会直接传递到融合输出。前后向光流一致性检查生成的遮挡掩码有效抑制了这类误差传播。

**6. 掩码边界平滑**（Figure 21）。面部掩码未经高斯平滑时，融合结果在面部与衣物交界处出现可见的硬边界，说明平滑过渡对自然融合至关重要。

**7. FusionNet输入完整性分析**（Figure 24）。将源图像、参考图像或面部掩码分别置零，FusionNet均无法生成合理结果——缺少源图像时输出无面部细节，缺少参考图像时无法恢复清晰度，缺少面部掩码时背景区域被不当处理。这验证了多模态输入的互补性。

### 失败模式与适用边界

尽管系统在大多数场景下表现优异，论文明确列出了以下限制：

- **多人脸场景**：受限于移动端算力预算，当前系统仅对画面中最大的单个人脸进行去模糊，无法同时处理多人脸。
- **极低光条件**：当环境光极暗时，UW参考图像因传感器噪声严重而丢失有效面部细节，融合输出会产生不可接受的伪影。
- **人脸过小**：在远距离合影等场景中，人脸区域过小导致UW摄像头无法捕获足够的面部细节，去模糊效果显著下降。
- **视差与遮挡**：系统假设W与UW摄像头可同步且视差可控；当双摄基线导致较大视差或面部被严重遮挡时，PWC-Net对齐精度下降，进而影响融合质量。

### 证据强度评估

整体实验设计较为扎实：真实场景数据集规模适中（1783张），覆盖人群多样性；NIMA作为无参考指标避免了合成数据上PSNR/SSIM的域偏差问题；消融实验覆盖了从输入模态、损失函数到数据增强的关键设计选择。但需注意，所有定量评估均基于内部数据集，缺乏公开基准的可复现性验证；与商业产品的对比仅在定性层面，未提供系统性的用户主观评分。

![[assets/figures/papers/paper_list_l41_https_www_wslai_net_publications_fusion_deblur/figures/002_Figure_2.jpg]]
*Figure 2: Flickering and banding. When a subject is illuminated by artificial lighting, e.g., 60Hz, increasing shutter speed faster than 1/120s (a) not only leads to excessive noise but also objectionable banding artifacts as shown in (b) due to the rolling shutter effects in CMOS sensors on mobile phones*

## 定位与知识库关联

本文的核心贡献在于将移动端人脸去模糊问题**从“盲去模糊”重新定义为“参考引导的融合”**，并据此改变了输入模态、计算域、快门控制策略和去模糊范式四个关键slot。

### 改变的Slot与本质差异

**1. 输入模态：从单摄到同步双摄RAW burst**

现有单图像去模糊方法（**MPRNet** (Zamir et al., CVPR 2021)、**MIMO-UNet** (Cho et al., ICCV 2021)）和视频去模糊方法（**UHDVD** (Deng et al., CVPR 2021)、**PVDNet** (Son et al., SIGGRAPH 2021)）均依赖单一摄像头捕获的模糊输入，其核心挑战是从模糊信号中盲恢复高频细节——这是一个病态逆问题。多帧方法如**BurstDeblurring** (Aittala and Durand, ECCV 2018)虽使用多帧，但帧间差异微小且均来自同一传感器，无法提供真正清晰的参考。

本文的slot改变在于：**同步启用超广角(UW)摄像头并以N倍快速快门捕获清晰但高噪声的参考图像**。这从根本上改变了问题的信息条件——系统拥有一个显式的、包含真实人脸细节的参考信号，将盲去模糊转化为有监督的对齐与融合任务。这一改变的关键因果机制是：现代手机普遍搭载双摄，UW传感器虽物理尺寸小、噪声高，但短曝光可冻结运动，恰好提供了W主摄长曝光所丢失的高频信息。

**2. 去模糊策略：从盲反卷积/端到端CNN到参考引导融合**

单图像方法（包括针对人脸的**UMSN** (Yasarla et al., IEEE TIP 2020)）试图从单张模糊图像中直接学习去模糊映射，其性能受限于模糊核估计的准确性和大运动下的信息丢失。本文的FusionNet不学习盲去模糊，而是学习**如何从噪声参考中提取并迁移清晰细节到模糊源图像**，通过PWC-Net光流对齐和UNet残差融合实现。

这一策略的本质优势在于：融合网络不需要“猜测”丢失的纹理，只需要“选择”和“迁移”参考中已有的信息。消融实验（Figure 16）提供了决定性证据——移除参考图像后，模型退化为单图像去模糊，无法恢复大运动模糊下的人脸细节，并产生不自然伪影。

**3. 计算域：从全图/视频到自适应人脸ROI**

现有方法在全图或视频帧上运算，计算量随分辨率线性增长。本文的slot改变是将处理限制在**最大人脸的自适应ROI（最大1536×1536）**内，通过人脸检测、1.75×扩展和取整实现。这利用了人脸去模糊的领域特性——用户关注的核心是面部区域，而非背景。结合优化的PWC-Net（延迟从113 ms降至13 ms，模型从40 MB压缩至1.27 MB），系统在Pixel 6上实现463 ms额外延迟，达到交互速率。

**4. 快门控制：从自动曝光到UW快门锁定N×加速**

传统单摄自动曝光系统在低光下会选择较长曝光时间以降低噪声，但牺牲了运动清晰度。本文的slot改变是：**W主摄维持自动曝光，UW快门的曝光时间固定为W的1/N（N=2或4）**。这一设计直接针对瓶颈——传感器尺寸限制和AC照明闪烁（Figure 2）——通过将“获取清晰细节”和“获取低噪声色彩”解耦到两个摄像头实现。

### 知识库挂载点

本文在知识库中的定位是**多摄计算摄影**与**人脸图像复原**的交叉节点。其方法链可挂载到以下知识路径：

- **上游依赖**：多帧RAW对齐与融合（Hasinoff et al., 2016的局部对齐方法）、光流估计（PWC-Net, Sun et al., CVPR 2018）、移动端人像分割（Wadhwa et al., 2018）。
- **并行关联**：与基于burst的去模糊（BurstDeblurring）共享多帧融合思想，但通过跨摄像头而非同摄像头burst获取信息增益；与双目/多摄超分（如Wronski et al., 2019的Handheld Multi-Frame Super-Resolution）共享利用视差和跨传感器信息的思想，但目标从超分辨率转向去模糊。
- **下游启发**：本文的“参考引导融合”范式可推广到其他双摄场景（如主摄+长焦去运动模糊、主摄+ToF深度辅助去模糊）。自适应ROI策略和轻量级PWC-Net优化为移动端实时计算摄影提供了可参考的工程路径。

### 适用边界与限制

本文方法存在明确的适用边界，需要在使用时注意：

1. **仅处理单人脸**：系统受限于设备算力预算，当前仅对最大人脸进行去模糊，无法处理多人合影场景。这是一个工程约束而非方法局限，但限制了实际应用范围。
2. **极低光下失效**：当环境光极低时，UW参考图像的信噪比严重下降，融合结果产生可感知的伪影。这是因为参考图像的高频细节被噪声淹没，FusionNet无法可靠区分信号与噪声。
3. **小人脸无效**：当被摄者面部过小（如远景合影），UW摄像头无法捕获足够的面部细节用于有效去模糊。这是UW传感器物理分辨率的硬约束。
4. **视差与遮挡敏感**：系统假设W和UW的视差可通过刚性光流对齐处理。在大视差或严重遮挡场景下，PWC-Net对齐可能失败，遮挡掩模（Equation 5）虽可缓解但不能完全消除伪影。
5. **AC照明闪烁**：尽管使用快速快门，CMOS卷帘快门效应仍可能在UW图像中引入条带伪影（Figure 2），系统通过RAW burst合并部分缓解，但未完全消除。

### 后续工作启发

本文留下的开放问题指向多个有价值的研究方向：**（1）多人脸扩展**——如何在当前功耗和算力预算内支持多张人脸的去模糊，可能需要更高效的共享特征提取或自适应ROI调度策略；**（2）端到端触发学习**——当前的模糊检测分类器（Figure 10）基于手工特征和元数据，替换为端到端学习触发器可能降低误触发率；**（3）语义先验融合**——当UW参考质量不足时，引入人脸语义先验（如3D可变形模型）补偿缺失细节；**（4）PWC-Net优化的定量影响**——论文仅报告了优化后PWC-Net的延迟和EPE变化，但未给出该优化对最终去模糊指标（PSNR/SSIM）的定量影响，这一空白值得填补。

## 原文 PDF

![[paperPDFs/SIGGRAPH_2022/Face_Deblurring_Using_Dual_Camera_Fusion_on_Mobile_Phones.pdf]]