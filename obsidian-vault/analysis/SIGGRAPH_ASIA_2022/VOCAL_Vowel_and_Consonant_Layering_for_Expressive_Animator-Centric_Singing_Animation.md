---
title: "VOCAL: Vowel and Consonant Layering for Expressive Animator-Centric Singing Animation"
type: paper
paper_level: A
venue: SIGGRAPH ASIA
year: 2022
pdf_ref: paperPDFs/SIGGRAPH_ASIA_2022/VOCAL_Vowel_and_Consonant_Layering_for_Expressive_Animator_Centric_Singing_Animation.pdf
project_link: null
code_link: null
aliases:
- VOCAL
tags:
- SIGGRAPH_ASIA_2022
- topic/graphics_animation_interaction
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: Ma (Melodic‑accent) 和 Ps (Pitch‑sensitivity) 两个参数，分别控制元音拖长程度/辅音贡献与音高敏感度（颤音），与已有 Ja‑Li 共同构成 Ma‑Ps‑Ja‑Li 四维风格空间，直接决定元音与辅音动画曲线的时间行为。
primary_logic: 基于语音生理学中元音与辅音的不同功能，将两者解耦分层：元音先处理以承载旋律，辅音后叠加以强调节奏；通过 Ma‑Ps 参数抽象从说唱到美声的连续风格谱系。
claims:
- 31 人用户偏好研究中，VOCAL 在 6/10 片段获得超过 70% 的偏好（显著优于 JALI）
- 元音修正网络在合并易混淆元音后测试准确率达到 91%（原始 70%）
- 与真值比较，VOCAL 在顶点位置和速度上的累积误差均低于 JALI
- 语音模型 Faceformer 和 JALI 在歌唱元音上表现呆板，无法表达音高变化和颤音
---

# VOCAL: Vowel and Consonant Layering for Expressive Animator-Centric Singing Animation

> [!tip] 核心洞察
> 基于语音生理学中元音与辅音的不同功能，将两者解耦分层：元音先处理以承载旋律，辅音后叠加以强调节奏；通过 Ma‑Ps 参数抽象从说唱到美声的连续风格谱系。

| 字段 | 内容 |
|------|------|
| 中文题名 | VOCAL：面向动画师的表达性歌唱动画中的元音与辅音分层 |
| 英文题名 | VOCAL: Vowel and Consonant Layering for Expressive Animator-Centric Singing Animation |
| 会议/期刊 | SIGGRAPH ASIA 2022 |
| Links | [paper](https://www.dgp.toronto.edu/projects/vocal/) |
| Topic | #topic/graphics_animation_interaction #topic/vision_multimodal_applications/image_and_video_generation |
| Method | VOCAL |
| Dataset | VocalSet, 10 段歌唱片段 |

> [!tip] 效果简介
> - VocalSet (4 歌手测试集, 元音识别) 上，准确率 (Accuracy) 91% (合并易混淆元音后) vs 70% (未合并) (+21%)。
> - 10 段歌唱片段 (用户偏好) 上，偏好率 (Preference rate vs. JALI) 6/10 片段 >70% 偏好 vs JALI (50% 基线) (显著高于基线 (>70% in 60% clips))。
> - 真值捕捉 (Faceware) 上，顶点位置/速度累积误差 低于 JALI vs JALI (更低（未量化）)。

## 概要

传统语音动画系统将元音与辅音统一为 viseme 处理，无法体现歌唱中元音承载旋律、辅音强调节奏的生理差异，导致长元音表现呆板、缺乏颤音与音高变化，难以适配从说唱到美声的多样风格。VOCAL 提出元音与辅音分层框架：元音先处理以承载旋律，辅音后叠加以保证咬字清晰；引入 Melodic accent (Ma) 与 Pitch sensitivity (Ps) 两个参数，与已有 Jaw‑Lip 参数共同构成 Ma‑Ps‑Ja‑Li 四维风格空间，连续控制元音拖长程度、辅音贡献与颤音强度。系统包含音素对齐、基频分段线性拟合、元音修正 LSTM 网络及基于 Ma‑Ps 的四曲线混合动画生成。在 VocalSet 上，元音修正网络合并易混淆元音后准确率达 91%；31 人用户偏好测试中，VOCAL 在 6/10 片段获得超过 70% 的偏好，显著优于 JALI 基线；与真值捕捉相比，顶点位置与速度累积误差均低于 JALI。该方法定位于程序化歌唱动画，以语音生理学驱动风格化解耦，为动画师提供直观可控的歌唱面部动画工具。

## 核心方法与创新机理

### 问题瓶颈：语音动画系统为何在歌唱中失效

传统语音动画系统——无论是程序化方法（如 **JALI**，Edwards et al., 2016）还是数据驱动方法（如 **Faceformer**，Fan et al., 2022）——将音素统一处理为 viseme（口型配置），生成与语音节奏匹配的口型动画。然而，这一设计在歌唱场景中暴露出根本性缺陷：**元音与辅音在生理功能上存在本质差异，却被同等对待**。

从语音生理学角度看，元音是气流不受阻碍的持续发声，在歌唱中承载旋律线条、音高变化和颤音等表达性元素；辅音则是短暂的气流阻碍或摩擦，在歌唱中强调节奏分句和歌词清晰度。当系统将两者统一处理时，长元音（如拖长的 `/a/` 或 `/i/`）仅呈现为单调的静态口型，无法体现音高起伏和颤音振荡，导致歌唱动画"呆板、缺乏表现力"——这正是论文指出的核心瓶颈：*"Sustained vowels seem inexpressively monotonic, failing to show pitch change and vibrato."*

此外，歌唱中普遍存在**元音修正**（vowel modification）现象：歌手为适应音高和音色需求，实际唱出的元音往往偏离歌词标注（例如高音区将 `/a/` 唱成 `/ɔ/`）。传统系统直接使用歌词元音，无法检测和修正这种偏差。

### 核心创新：元音-辅音分层与 Ma-Ps 风格空间

VOCAL 的核心创新在于**基于生理功能差异的解耦分层架构**，并引入两个连续风格参数——**Melodic accent (Ma)** 和 **Pitch sensitivity (Ps)**——将歌唱风格抽象为从说唱到美声的连续谱系。

**元音与辅音的分层处理逻辑**：
- **元音先处理**：元音承载旋律，主导下巴运动（jaw opening），其动画曲线根据音高生成内部关键帧，并加入颤音振荡。
- **辅音后叠加**：辅音强调节奏，主要贡献唇形（lip shape）变化，其动画曲线在元音基础上分层叠加，通过协同发音（co-articulation）规则与元音曲线融合。

这一分层设计直接回应了瓶颈：元音获得独立的旋律表达通道，辅音保持节奏清晰度，两者不再相互干扰。

### 核心控制参数：Ma-Ps 风格空间

VOCAL 将 **JALI** 原有的 Jaw-Lip 二维风格空间扩展为 **Ma-Ps-Ja-Li 四维空间**。这是系统最关键的 changed slot：

| 参数 | 物理含义 | 动画效果 | 风格谱系位置 |
|------|----------|----------|-------------|
| **Ma** (Melodic accent) | 元音旋律化程度 | 高 Ma → 元音拖长、辅音减弱；低 Ma → 辅音突出、节奏感强 | 低 Ma 对应说唱/快节奏流行，高 Ma 对应美声/古典 |
| **Ps** (Pitch sensitivity) | 对音高变化的敏感度 | 高 Ps → 颤音振幅大、音高追踪紧密；低 Ps → 元音平滑稳定 | 低 Ps 对应口语化演唱，高 Ps 对应歌剧式颤音 |
| **Ja** (Jaw) | 下巴开合幅度 | 继承自 JALI | - |
| **Li** (Lip) | 唇形宽度 | 继承自 JALI | - |

**Ma 和 Ps 的自动计算**：系统从音频中提取启发式特征，无需手动标注。Ma 基于辅音的高频能量（`ε`）相对全曲范围自动推算：

$$Ma = \begin{cases} 0.2 & \text{if } \epsilon \leq \tau_{\text{low}} \\ 0.8 & \text{if } \epsilon \geq \tau_{\text{high}} \\ 0.5 & \text{otherwise} \end{cases}$$

Ps 基于元音时长（`ν`）与平均口语元音时长（约 0.2s）的差值计算：

$$Ps = \begin{cases} 0.1 & \text{if } \nu \leq \tau \\ \min(1, 0.1 + \nu - \tau) & \text{otherwise} \end{cases}$$

这种设计使 Ma 和 Ps 成为**可自动提取、可手动调节**的连续参数，动画师既可直接使用音频驱动的自动值，也可在四维空间中自由探索风格变化。

### 系统流水线与模块因果关系

VOCAL 的完整流水线分为两大阶段：**标记阶段**（Tagging）和**动画曲线生成阶段**（Animation Curve Generation）。各模块之间存在严格的数据依赖和因果链：

#### 阶段一：标记阶段（Tagging）

**模块 1：音素对齐（Phoneme Alignment）**
- **输入**：音频 + 歌词文本
- **处理**：使用强制对齐（forced alignment）将歌词转写为音素序列（CMU 记法），并与音频时间轴对齐，生成每个音素的起止时间。
- **输出**：时间对齐的音素序列
- **因果作用**：为后续所有模块提供时间基准。对齐错误将直接传播到动画曲线生成，是系统性能的下限。

**模块 2：音频标记（Audio Tagging）**
- **输入**：音频 + 音素时间对齐
- **处理**：
  - 提取基频（f₀）曲线，使用**分段线性拟合的动态规划算法**检测恒定音高段和颤音段。动态规划代价矩阵定义为：

    $$M(a,b) = \min_{a<x<b} \{ M(a,k) + M(k,b), E_{fit}(a,b) + E_{cost} \}$$

    其中拟合误差为基频值与线性段拟合值之差的绝对值之和：

    $$E_{fit}(a,b) = \sum_{t=a}^{b} | f_0(t) - (slope_t \times t + yint_t) |$$

  - 检测颤音区间（通过基频的周期性波动识别）
- **输出**：音符边界、恒定音高段、颤音段标记
- **因果作用**：音符边界决定元音动画曲线的内部关键帧位置；颤音标记触发 Ps 驱动的振荡。

**模块 3：Ma-Ps 参数计算**
- **输入**：音频频谱 + 音素时长
- **处理**：按上述启发式公式计算 Ma 和 Ps 值
- **输出**：标量 Ma、Ps 值
- **因果作用**：直接控制后续动画曲线生成中的四种极端曲线混合权重。

**模块 4：元音修正网络（Vowel Modification Detection Network）**
- **输入**：音频特征向量（MFCC 等）
- **架构**：受 VisemeNet（2018）启发的 LSTM 网络，包含三层 LSTM → ReLU 激活 → 全连接层 → Softmax，输出意大利五元音（`/a/, /e/, /i/, /o/, /u/`）加静音的概率分布。
- **训练**：在 VocalSet 数据集（20 位专业歌手）上训练，合并易混淆元音对（如 `/e/-/i/`、`/o/-/u/`）后测试准确率达 91%（原始 70%）。
- **输出**：每个时间戳的元音预测概率
- **因果作用**：当预测元音与歌词元音不一致时，触发唇形 AU（lipSpread/lipRound）修正曲线。修正曲线的峰值振幅为：

  $$\alpha = P(prediction) \cdot \alpha_{max}$$

  其中 `P(prediction)` 为网络预测概率，`α_max` 为对应 AU 的最大振幅。

#### 阶段二：动画曲线生成阶段

**模块 5：动画曲线生成（Animation Curve Generation）**

这是 VOCAL 最复杂的模块，采用**四曲线混合策略**，将 Ma-Ps 风格参数转化为具体的 viseme 动画曲线。生成过程分为三个子步骤：

**步骤 5a：四种极端曲线生成**

系统首先生成四条代表风格空间极点的曲线：
1. **Speech 曲线**：标准口语动画，元音与辅音统一处理，无旋律表达。
2. **Sing 曲线**：歌唱曲线，元音根据音高生成内部关键帧，加入颤音振荡。
3. **Ma-extreme 曲线**：Melodic accent 极端曲线，元音最大化拖长，辅音最小化。
4. **Ps-extreme 曲线**：Pitch sensitivity 极端曲线，颤音振幅最大化。

其中 Sing 曲线的生成是核心，涉及以下关键公式：

- **音符起始振幅**：根据音高线性映射到 `[0.6, 1.0]` 区间：

  $$\alpha_s = 0.4 \times (f_0(t_{start}) - f_{0,min}) / (f_{0,max} - f_{0,min}) + 0.6$$

- **音符结束振幅**：较起始振幅衰减 5%：

  $$\alpha_e = 0.95 \alpha_s$$

- **音符间过渡振幅**：取前后音振幅最小值的 90%：

  $$\alpha = 0.9 \times \min(\alpha_{end}^{prev}, \alpha_{start}^{next})$$

- **颤音振荡**：在 Ps 驱动下，对持续元音加入约 7 Hz 的正弦振荡，振幅与 Ps 值成正比。

**步骤 5b：协同发音处理（Co-articulation）**

相邻 viseme 之间产生重叠区域，系统在重叠区域生成过渡关键帧，确保口型平滑切换。当同一 viseme 在短时间内重复出现时（如连续两个 `/a/`），重叠可能导致冲突关键帧。

**步骤 5c：冲突解决（Conflict Resolution）**

对于重叠区域的冲突关键帧，系统合并 viseme 曲线：取同时激活的多个 viseme 的加权平均，权重由各 viseme 的目标振幅和时序位置决定。

**步骤 5d：Ma-Ps 混合（MaPs Field Blending）**

最终动画曲线由四条极端曲线在 Ma-Ps 空间中的双线性插值生成。给定当前片段的 `(Ma, Ps)` 坐标，系统计算其在 Speech-Sing-Ma-Ps 四极点构成的四边形中的归一化位置，混合权重由该位置决定。这使得动画师可以在四维风格空间中连续探索，从说唱（低 Ma，低 Ps）平滑过渡到歌剧（高 Ma，高 Ps）。

**模块 6：喉结运动（Larynx Movement）**
- **输入**：基频 f₀ 曲线
- **处理**：根据 f₀ 值驱动喉结骨骼的垂直位移。高音对应喉结上移，低音对应喉结下移。
- **因果作用**：补充下半脸之外的音色变化视觉线索，增强歌唱动画的生理真实感。

### 关键 Changed Slots 总结

| Changed Slot | 基线值 | VOCAL 值 | 因果机制 |
|-------------|--------|----------|----------|
| **风格参数空间** | Ja-Li (2D) | Ma-Ps-Ja-Li (4D) | Ma 控制元音拖长/辅音贡献比，Ps 控制颤音敏感度，两者通过四曲线混合直接决定动画曲线的时间行为 |
| **音素处理架构** | 统一 viseme 处理 | 元音先处理，辅音后分层叠加 | 元音承载旋律（下巴运动），辅音强调节奏（唇形），避免相互干扰 |
| **元音修正** | 无（直接使用歌词元音） | LSTM 网络检测实际唱出元音并修正 viseme | 修正曲线根据网络预测概率调制唇形 AU 振幅，纠正歌唱中的元音偏差 |
| **元音动画曲线** | 固定 ASR 包络 | 基于音高内部关键帧 + 颤音振荡 | 音符起止振幅与 f₀ 线性相关，Ps 驱动 7 Hz 颤音，消除长元音视觉冻结 |

### 推理路径与数据流

完整的推理路径为：
1. **音频 + 歌词** → 强制对齐 → **时间对齐音素序列**
2. **音频** → 基频提取 + 动态规划分段 → **音符边界与颤音标记**
3. **音频频谱 + 音素时长** → 启发式计算 → **Ma, Ps 标量值**
4. **音频特征** → LSTM 网络 → **元音修正概率** → 修正曲线
5. **音素序列 + 音符标记 + Ma-Ps 值** → 四曲线生成 → 协同发音 → 冲突解决 → Ma-Ps 混合 → **最终 viseme 动画曲线**
6. **基频 f₀** → 喉结位移映射 → **喉结动画**

整个流水线中，**Ma 和 Ps 是连接音频分析与动画生成的核心控制旋钮**：它们既是可自动提取的音频特征，又是动画师可手动调节的风格参数，实现了"自动驱动"与"艺术控制"的统一。

## 实验与关键发现

VOCAL 的实验评估围绕三个核心问题展开：元音修正网络的准确性、动画输出的用户偏好，以及与真值捕捉的定量对比。由于歌唱动画缺乏标准化的自动评测基准，作者采用了“网络准确率 + 用户偏好 + 真值误差”的多维度验证策略。

### 元音修正网络准确率

元音修正网络在 **VocalSet** 数据集上训练和测试，该数据集包含 20 位专业歌手的演唱录音。网络最初在六个类别（意大利五元音 + 静音）上测试，准确率为 **70%**。作者发现部分元音在歌唱中极易混淆（如 /e/ 与 /ɛ/），因此将易混淆元音合并后重新评估，测试准确率提升至 **91%**（Figure 5）。这一 +21% 的提升表明，歌唱中元音的声学边界比口语更模糊，合并策略是实用且有效的工程折中。需注意该网络仅在意大利五元音上训练，对英语歌曲中实际出现的更丰富元音集合的泛化能力未经独立验证，论文也未报告跨歌手或跨语言场景的准确率变化。

![[assets/figures/papers/paper_list_l99_https_www_dgp_toronto_edu_projects_vocal/figures/005_Figure_5.jpg]]
*Figure 5: Vowel modification predicts vowel probabilities from input audio*

### 用户偏好研究

这是论文最具说服力的实验。作者选取 **10 段**涵盖不同风格（说唱、流行、古典等）的歌唱片段，每段同时生成 VOCAL 和 JALI 两个版本的动画，邀请 **31 名**观看者进行盲测偏好投票。结果显示：**6/10 片段中 VOCAL 获得了超过 70% 的偏好票**（Figure 8），显著高于随机基线（50%）。在其余 4 个片段中，两者偏好接近或 JALI 略占优势，这些片段通常辅音密集、元音较短，VOCAL 的元音分层优势未能充分体现。

![[assets/figures/papers/paper_list_l99_https_www_dgp_toronto_edu_projects_vocal/figures/009_Figure_8.jpg]]
*Figure 8: Recorded user preference of 10 clips (Video 13:41-16:43)*

这一结果直接支撑了论文的核心主张：将元音与辅音解耦分层处理，在元音承载旋律的歌唱场景中具有明显视觉优势。但需注意，用户偏好受多种因素影响，包括动画风格、角色外观等，论文未控制这些变量，且样本量（31 人）在统计学上属于中等规模。

### 与真值捕捉的定量对比

作者使用 **Faceware** 头戴式摄像头捕捉了一位歌手演唱时的下半脸运动作为真值，然后分别用 JALI 和 VOCAL 从同一音频生成动画，计算顶点位置和速度的累积误差。论文报告 **VOCAL 在两个指标上的累积误差均低于 JALI**（Figure 7），但未提供具体数值。这一对比的置信度相对较低（0.8），因为真值仅来自单次捕捉，且误差计算的具体方法（如时间对齐策略、顶点权重等）未详细说明。建议将此结果视为定性佐证而非严格定量证据。

![[assets/figures/papers/paper_list_l99_https_www_dgp_toronto_edu_projects_vocal/figures/008_Figure_7.jpg]]
*Figure 7: Faceware captured ground truth compared to JALI a nd VOCAL*

### 关键消融与参数效果

**元音修正的消融**体现在准确率对比中：不合并易混淆元音时准确率 70%，合并后 91%，验证了合并策略的必要性。

**Ma 参数的风格控制效果**通过定性展示验证：增大 Ma 值使元音拖长、辅音贡献减弱，视觉风格从说唱（辅音清晰、节奏感强）连续过渡到古典美声（元音绵长、辅音弱化）。论文未对此进行定量用户研究，但 Figure 8 中不同风格片段的结果差异间接支持了 Ma 的有效性——在元音丰富的古典片段中 VOCAL 优势更明显。

**Ps 参数的颤音效果**获得了专业动画师的定性认可（“the vibrato is very effective to my eyes”），避免了长元音在视觉上的“冻结”感。7 Hz 的颤音振荡频率是基于声乐颤音的典型频率范围设定的，但论文未探索不同频率或波形的效果差异。

### 失败模式与适用边界

**音素对齐错误**：歌唱中的长乐句、音乐失真或非标准发音可能导致强制对齐失败，进而影响后续所有模块。论文在 Figure 6 中展示了部分失败案例，但未量化对齐错误率。

**元音修正的阈值依赖**：修正触发依赖于经验阈值 0.6（预测概率），可能导致部分应修正的元音被漏掉，或不应修正的被误改。论文未对该阈值进行敏感性分析。

**表达维度受限**：VOCAL 仅驱动下半脸（唇、下巴、喉结），无法表达歌唱中的呼吸感、颈筋紧张、皮肤紧绷等生理信号。上半脸、头部运动和视线仍需手工关键帧或表演捕捉补充。这限制了系统在需要全身表演的虚拟歌手场景中的直接应用。

**语言与风格泛化未验证**：所有实验均在英文歌曲上进行，元音修正网络基于意大利五元音体系。对于中文（含声调）、法语（鼻化元音）等语言，以及京剧、呼麦等非西方声乐传统，系统的适用性完全未知。

**数据驱动基线的局限**：与 Faceformer 和 Song2Face 的对比仅为定性展示（Figure 6），未进行定量或用户偏好比较。论文指出这些基线在歌唱元音上“呆板单调”，但未深入分析其原因（如训练数据以口语为主）。

![[assets/figures/papers/paper_list_l99_https_www_dgp_toronto_edu_projects_vocal/figures/007_Table.jpg]]

![[assets/figures/papers/paper_list_l99_https_www_dgp_toronto_edu_projects_vocal/figures/006_Figure_6.jpg]]
*Figure 6: Failure cases for song2face, FaceFormer, JALI and our system*

## 定位与知识库关联

VOCAL 在程序化语音动画谱系中占据一个独特位置：它并非替代通用语音动画系统，而是专门针对**歌唱场景**将元音与辅音的生理功能差异显式建模，从而填补了“语音动画系统无法表达歌唱旋律性”与“数据驱动歌唱动画系统缺乏风格可控性”之间的空白。

### 相对于基线的本质差异

传统程序化语音动画系统（以 **JALI** (Edwards et al., 2016) 为代表）将元音和辅音统一作为 viseme 处理，依赖 Ja（下颌）和 Li（唇）两个参数控制整体发音幅度。这一设计在说话场景中有效，但在歌唱中暴露出根本缺陷：元音承载旋律、辅音强调节奏的生理分工被抹平，导致长元音表现呆板、缺乏颤音与音高变化。VOCAL 改变的核心 slot 是**音素处理架构**——将元音与辅音解耦分层：元音先处理以承载旋律，辅音后叠加以强调节奏；同时将风格参数空间从 2D (Ja-Li) 扩展为 4D (Ma-Ps-Ja-Li)，使系统能够覆盖从说唱到美声的连续风格谱系。

与数据驱动语音动画基线 **Faceformer** (Fan et al., 2022) 相比，VOCAL 的差异在于**因果机制而非数据量**。Faceformer 从说话数据中学习音频到动画的映射，在辅音发音上表现良好，但在歌唱元音上“inexpressively monotonic, failing to show pitch change and vibrato”。这是因为其训练分布中不存在长时元音与音高变化的关联。VOCAL 通过显式的 Ma-Ps 参数和基于基频的动画曲线生成，将音高变化直接编码为视觉行为，绕过了数据驱动方法在歌唱场景中的分布外泛化问题。

与数据驱动歌唱动画基线 **Song2Face** (Iwase et al., 2020) 相比，VOCAL 的定位差异在于**可控性优先于真实感**。Song2Face 从表演捕捉数据中学习端到端映射，能产生较自然的动画，但缺乏对风格的显式控制，且如 Figure 6 所示存在失败案例。VOCAL 牺牲了一定的数据驱动真实感，换取了动画师可调节的四维风格空间，使其更适合需要精确艺术控制的生产环境。

### 知识库挂载点

VOCAL 可挂载到知识库的以下节点：

1. **程序化语音动画**（Procedural Speech Animation）：作为 JALI 在歌唱场景的扩展，新增 Ma-Ps 参数和元音/辅音分层架构。挂载关系为 `extends JALI with singing-specific vowel-consonant layering`。

2. **歌唱动画**（Singing Animation）：作为 Song2Face 的可控替代方案，提供显式风格参数而非黑箱映射。挂载关系为 `controllable alternative to data-driven singing animation`。

3. **语音生理学驱动的面部动画**（Physiology-driven Facial Animation）：基于元音与辅音的不同生理功能（元音主导下颌运动、辅音主要贡献唇形）设计分层架构，并引入喉结运动反映音高和音色变化。挂载关系为 `physiology-motivated decoupling of vowel and consonant contributions`。

4. **音频驱动的面部动画风格控制**（Audio-driven Facial Animation Style Control）：Ma-Ps-Ja-Li 四维风格空间为动画师提供了从说唱到古典的连续风格调节能力，可挂载到风格可控的面部动画方法谱系中。

### 适用边界与局限

VOCAL 的适用边界受以下因素制约：

- **语言与声乐传统**：元音修正网络在意大利五元音上训练，音素对齐依赖英文 CMU 词典。对非英语语言（尤其是元音系统差异较大的语言）和其他声乐传统（如京剧、呼麦）的扩展性未经验证。
- **歌唱风格覆盖**：VocalSet 训练数据含 20 位专业歌手，风格相对集中。普通用户哼唱或非西方声乐传统可能引入域外问题。
- **视觉表达范围**：系统仅驱动下半脸，无法表达歌唱中的用力和呼吸效果（如颈筋、皮肤紧绷），上半脸、头部和颈部的副语言运动仍需手工关键帧或表演捕捉辅助。
- **音素对齐鲁棒性**：歌唱中的长乐句或音乐失真片段可能导致对齐错误，需要人工修正。

### 后续启发与开放问题

VOCAL 的 Ma-Ps 风格空间抽象为后续工作提供了几个方向：

1. **从音频自动预测 Ma-Ps 轨迹**：当前 Ma-Ps 值通过启发式从音频计算，若能通过表演捕捉数据学习个性化 Ma-Ps 轨迹，可实现特定歌手风格自动适配。

2. **扩展到上半脸与头部运动**：如何从音频中预测歌唱时上半脸、头部和颈部的韵律同步运动，是构建完整歌唱动画系统的关键缺口。

3. **多语言与跨文化声乐传统**：将元音修正网络和音素对齐扩展到非英语语言，以及适应不同声乐传统（如京剧的拖腔、呼麦的双声部），需要重新审视元音/辅音分层的生理学假设是否仍然成立。

4. **呼吸与肌肉用力信号**：加入呼吸、肌肉用力等生理信号，可进一步增强歌唱动画的真实感，这需要新的音频特征提取和动画映射机制。

## 原文 PDF

![[paperPDFs/SIGGRAPH_ASIA_2022/VOCAL_Vowel_and_Consonant_Layering_for_Expressive_Animator_Centric_Singing_Animation.pdf]]