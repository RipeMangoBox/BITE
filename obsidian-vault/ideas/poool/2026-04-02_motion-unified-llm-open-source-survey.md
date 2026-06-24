---
created: 2026-04-02
updated: 2026-04-08T13:29
status: survey
source:
  - '[[paperAnalysis/Motion_Generation/NeurIPS_2023/2023_MotionGPT_Human_Motion_as_Foreign_Language|MotionGPT]]'
  - '[[paperAnalysis/Motion_Generation/CVPR_2024/2024_All_in_One_Framework_for_Motion_Understanding_Planning_Generation_and_Beyond|AvatarGPT]]'
  - '[[paperAnalysis/Motion_Generation/NeurIPS_2024/2024_An_Advanced_Multimodal_Multitask_Framework_for_Motion_Comprehension_and_Generation|M3GPT]]'
  - '[[paperAnalysis/Motion_Generation/ECCV_2024/2024_LMM_Large_Motion_Model_for_Unified_Multi_Modal_Motion_Generation|LMM]]'
  - '[[paperAnalysis/Motion_Generation/CVPR_2025/2025_MG_MotionLLM_A_Unified_Framework_for_Motion_Comprehension_and_Generation_across_Multiple_Granularities|MG-MotionLLM]]'
  - '[[paperAnalysis/Motion_Generation/CVPR_2025/2025_The_Languate_of_Motion_Unifying_Verbal_and_Non_verbal_Language_of_3D_Human_Motion|The Language of Motion]]'
  - '[[paperAnalysis/Motion_Generation/CVPR_2025/2025_AToM_Aligning_Text_to_Motion_Model_Event_Level_GPT4Vision_Reward|AToM]]'
  - '[[paperAnalysis/Motion_Generation/AAAI_2025/2025_RemoGPT_Part_Level_Retrieval_Augmented_Motion_Language_Models|ReMoGPT]]'
  - '[[paperAnalysis/Human_Interaction/CVPR_2025/2025_HSI_GPT_A_General_Purpose_Large_Scene_Motion_Language_Model_for_HumanScene_Interaction|HSI-GPT]]'
  - '[[paperAnalysis/Human_Interaction/ICCV_2025/2025_Being_M0_5_A_Real_Time_Controllable_Vision_Language_Motion_Model|Being-M0.5]]'
  - '[[paperAnalysis/Motion_Generation/Tencent_HY/2025_HY_Motion_1_0_Scaling_Flow_Matching_Text_to_Motion|HY-Motion 1.0]]'
  - '[[paperAnalysis/Motion_Generation/CVPR_2026/2026_MoLingo_Motion_Language_Alignment_for_Text_to_Motion_Generation|MoLingo]]'
tags:
  - survey
  - Motion_Generation
  - motion-understanding
  - motion-llm
  - large-motion-model
  - semantic-alignment
  - open-source
  - github
verified_on: 2026-04-02
---
# Motion 生成理解统一 / 动作生成大模型 / 动作-语义对齐论文开源调研

> 目标：从 ResearchWY 知识库中筛出三类论文：
>
> 1. **motion 生成-理解统一**
> 2. **动作生成大模型**
> 3. **动作-语义对齐**
>
> 并额外核查其 **GitHub 是否开源、是否像官方实现、社区热度（star）与开源可信度**。
>
> 说明：GitHub star 为 **2026-04-02** 联网核查时的近似值，后续会动态变化。
>
> 共享背景：统一表征、结构化对齐、多层控制之间的重合背景已抽到 [[2026-04-16_structured-alignment-multi-level-control-shared-frame|2026-04-16 结构化对齐与多层控制共享框架]]。本文保留“开源可复现性筛选”这一独立角度。

---
## 一、快速结论

### 1.1 最值得优先跟踪的开源项目

如果目标是 **“能直接看代码 / 复现价值高 / 社区热度高”**，优先级大致是：

1. [[paperAnalysis/Motion_Generation/Tencent_HY/2025_HY_Motion_1_0_Scaling_Flow_Matching_Text_to_Motion|HY-Motion 1.0]]
2. [[paperAnalysis/Motion_Generation/NeurIPS_2023/2023_MotionGPT_Human_Motion_as_Foreign_Language|MotionGPT]]
3. [[paperAnalysis/Motion_Generation/ECCV_2024/2024_LMM_Large_Motion_Model_for_Unified_Multi_Modal_Motion_Generation|LMM]]
4. [[paperAnalysis/Motion_Generation/CVPR_2025/2025_The_Languate_of_Motion_Unifying_Verbal_and_Non_verbal_Language_of_3D_Human_Motion|The Language of Motion]]
5. [[paperAnalysis/Motion_Generation/CVPR_2026/2026_MoLingo_Motion_Language_Alignment_for_Text_to_Motion_Generation|MoLingo]]

### 1.2 最适合看“统一生成+理解”的论文

- [[paperAnalysis/Motion_Generation/NeurIPS_2023/2023_MotionGPT_Human_Motion_as_Foreign_Language|MotionGPT]]
- [[paperAnalysis/Motion_Generation/CVPR_2024/2024_All_in_One_Framework_for_Motion_Understanding_Planning_Generation_and_Beyond|AvatarGPT]]
- [[paperAnalysis/Motion_Generation/NeurIPS_2024/2024_An_Advanced_Multimodal_Multitask_Framework_for_Motion_Comprehension_and_Generation|M3GPT]]
- [[paperAnalysis/Motion_Generation/CVPR_2025/2025_MG_MotionLLM_A_Unified_Framework_for_Motion_Comprehension_and_Generation_across_Multiple_Granularities|MG-MotionLLM]]

### 1.3 最适合看“动作生成大模型 / foundation model”的论文

- [[paperAnalysis/Motion_Generation/ECCV_2024/2024_LMM_Large_Motion_Model_for_Unified_Multi_Modal_Motion_Generation|LMM]]
- [[paperAnalysis/Motion_Generation/Tencent_HY/2025_HY_Motion_1_0_Scaling_Flow_Matching_Text_to_Motion|HY-Motion 1.0]]
- [[paperAnalysis/Human_Interaction/ICCV_2025/2025_Being_M0_5_A_Real_Time_Controllable_Vision_Language_Motion_Model|Being-M0.5]]
- [[paperAnalysis/Human_Interaction/CVPR_2025/2025_HSI_GPT_A_General_Purpose_Large_Scene_Motion_Language_Model_for_HumanScene_Interaction|HSI-GPT]]

### 1.4 最适合看“动作-语义对齐”的论文

- [[paperAnalysis/Motion_Generation/CVPR_2026/2026_MoLingo_Motion_Language_Alignment_for_Text_to_Motion_Generation|MoLingo]]
- [[paperAnalysis/Motion_Generation/CVPR_2025/2025_AToM_Aligning_Text_to_Motion_Model_Event_Level_GPT4Vision_Reward|AToM]]
- [[paperAnalysis/Motion_Generation/CVPR_2025/2025_The_Languate_of_Motion_Unifying_Verbal_and_Non_verbal_Language_of_3D_Human_Motion|The Language of Motion]]
- [[paperAnalysis/Motion_Generation/CVPR_2025/2025_MG_MotionLLM_A_Unified_Framework_for_Motion_Comprehension_and_Generation_across_Multiple_Granularities|MG-MotionLLM]]
- [[paperAnalysis/Motion_Generation/AAAI_2025/2025_RemoGPT_Part_Level_Retrieval_Augmented_Motion_Language_Models|ReMoGPT]]

---
## 二、开源可信度判定标准

这里的 **“开源可信度”** 是主观工程判断，不等于论文质量。

### 高

- 有明确 **官方仓库**（作者/实验室/组织名下）
- Repo 首页直接写明是该论文的 official implementation
- 能看到较完整工程形态（代码 / 环境 / checkpoint / demo / HuggingFace / issues）
- 社区热度明显（通常 star 较高）

### 中

- 能确认是官方或基本官方
- 但仓库热度一般，或工程完整度一般，或维护信号偏弱
- 适合参考，但不一定适合直接大规模复现

### 低

- 没找到官方代码，或只有 project page
- 或只找到组织相关仓库，但无法确认就是该论文的正式实现
- 或论文强，但开源证据不足

---
## 三、总表

| 主题      | 论文                                                                                                                                                      | Venue                    | 核心关键词        | GitHub 开源                                                     |            Stars | 开源可信度 | 备注  |                             |
| ------- | ------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------ | ------------ | ------------------------------------------------------------- | ---------------: | ----- | --- | --------------------------- |
| 统一生成+理解 | [[paperAnalysis/Motion_Generation/NeurIPS_2023/2023_MotionGPT_Human_Motion_as_Foreign_Language                                                          | MotionGPT]]              | NeurIPS 2023 | motion as language / unified tasks / instruction tuning       |             ✅ 官方 | 1896  | 高   | 统一 motion-text 经典基线，社区最成熟之一 |
| 统一生成+理解 | [[paperAnalysis/Motion_Generation/CVPR_2024/2024_All_in_One_Framework_for_Motion_Understanding_Planning_Generation_and_Beyond                           | AvatarGPT]]              | CVPR 2024    | understanding + planning + generation                         |             ✅ 官方 | 48    | 中   | 官方 repo 存在，但热度与传播不算高        |
| 统一生成+理解 | [[paperAnalysis/Motion_Generation/NeurIPS_2024/2024_An_Advanced_Multimodal_Multitask_Framework_for_Motion_Comprehension_and_Generation                  | M3GPT]]                  | NeurIPS 2024 | multimodal / multitask / text-as-bridge                       |             ✅ 官方 | 19    | 中-低 | 官方 repo 存在，但热度较低            |
| 统一生成+理解 | [[paperAnalysis/Motion_Generation/CVPR_2025/2025_MG_MotionLLM_A_Unified_Framework_for_Motion_Comprehension_and_Generation_across_Multiple_Granularities | MG-MotionLLM]]           | CVPR 2025    | multi-granularity / localization / fine-grained script        |             ✅ 官方 | 31    | 中   | 官方 repo 明确，但目前社区热度一般        |
| 动作大模型   | [[paperAnalysis/Motion_Generation/ECCV_2024/2024_LMM_Large_Motion_Model_for_Unified_Multi_Modal_Motion_Generation                                       | LMM]]                    | ECCV 2024    | MotionVerse / ArtAttention / generalist model                 |             ✅ 官方 | 307   | 高   | 大模型/大数据集路线较完整               |
| 动作大模型   | [[paperAnalysis/Motion_Generation/Tencent_HY/2025_HY_Motion_1_0_Scaling_Flow_Matching_Text_to_Motion                                                    | HY-Motion 1.0]]          | arXiv 2025   | 1B+ model / flow matching / RLHF                              |             ✅ 官方 | 2237  | 高   | 当前最强“工业级开源动作大模型”信号之一        |
| 动作大模型   | [[paperAnalysis/Human_Interaction/ICCV_2025/2025_Being_M0_5_A_Real_Time_Controllable_Vision_Language_Motion_Model                                       | Being-M0.5]]             | ICCV 2025    | VLMM / real-time / part-aware control                         | ⚠️ 未确认该论文官方 repo | —     | 低   | 只检到相关组织仓库，未核到论文级官方实现        |
| 动作大模型   | [[paperAnalysis/Human_Interaction/CVPR_2025/2025_HSI_GPT_A_General_Purpose_Large_Scene_Motion_Language_Model_for_HumanScene_Interaction                 | HSI-GPT]]                | CVPR 2025    | scene-motion-language model                                   |    ⚠️ 未检到官方 repo | —     | 低   | 论文强，但当前公开代码证据不足             |
| 语义对齐    | [[paperAnalysis/Motion_Generation/CVPR_2025/2025_The_Languate_of_Motion_Unifying_Verbal_and_Non_verbal_Language_of_3D_Human_Motion                      | The Language of Motion]] | CVPR 2025    | verbal/non-verbal alignment / compositional body tokenization |             ✅ 官方 | 90    | 高   | 官方 repo 明确，任务新且代码可信         |
| 语义对齐    | [[paperAnalysis/Motion_Generation/CVPR_2025/2025_AToM_Aligning_Text_to_Motion_Model_Event_Level_GPT4Vision_Reward                                       | AToM]]                   | CVPR 2025    | event-level alignment / preference tuning                     |             ✅ 官方 | 18    | 中   | 官方 repo 明确，但项目较新、热度较低       |
| 语义对齐    | [[paperAnalysis/Motion_Generation/CVPR_2026/2026_MoLingo_Motion_Language_Alignment_for_Text_to_Motion_Generation                                        | MoLingo]]                | CVPR 2026    | semantic latent space / contrastive alignment                 |             ✅ 官方 | 55    | 中-高 | 官方 repo 明确，方法聚焦且比较新         |
| 语义对齐    | [[paperAnalysis/Motion_Generation/AAAI_2025/2025_RemoGPT_Part_Level_Retrieval_Augmented_Motion_Language_Models                                          | ReMoGPT]]                | AAAI 2025    | retrieval-augmented / part-level alignment                    |    ⚠️ 未检到官方 repo | —     | 低   | 论文方向很有意思，但开源证据不足            |

---
## 四、分主题整理

## 4.1 Motion 生成-理解统一

### A. [[paperAnalysis/Motion_Generation/NeurIPS_2023/2023_MotionGPT_Human_Motion_as_Foreign_Language|MotionGPT]]

- **定位**：把 motion 当作外语，统一 text→motion / motion→text / prediction / completion
- **知识库关键词**：`motion token + T5 + instruction tuning + unified framework`
- **为什么重要**：这是后续 MotionLLM / Motion-language model 路线的核心祖先之一
- **开源情况**：✅ 官方仓库 `OpenMotionLab/MotionGPT`
- **Star**：约 **1896**
- **可信度**：**高**
- **判断原因**：OpenMotionLab 官方维护、社区热度高、是公认基线

### B. [[paperAnalysis/Motion_Generation/CVPR_2024/2024_All_in_One_Framework_for_Motion_Understanding_Planning_Generation_and_Beyond|AvatarGPT]]

- **定位**：统一 motion understanding / planning / generation / in-between 等 7 类任务
- **知识库关键词**：`all-in-one / planning / decomposition / generation`
- **为什么重要**：比 MotionGPT 更强调“高层规划→低层生成”的闭环
- **开源情况**：✅ 官方仓库 `zixiangzhou916/AvatarGPT`
- **Star**：约 **48**
- **可信度**：**中**
- **判断原因**：官方 repo 可定位，但社区传播与维护热度一般

### C. [[paperAnalysis/Motion_Generation/NeurIPS_2024/2024_An_Advanced_Multimodal_Multitask_Framework_for_Motion_Comprehension_and_Generation|M3GPT]]

- **定位**：把文本、运动、音乐统一起来，同时做 6 类任务
- **知识库关键词**：`multimodal / multitask / text-as-bridge`
- **为什么重要**：它比 MotionGPT/AvatarGPT 更强调“文本是跨模态桥梁”
- **开源情况**：✅ 官方仓库 `luomingshuang/m3gpt`
- **Star**：约 **19**
- **可信度**：**中-低**
- **判断原因**：官方仓库明确，但热度较低，后续维护信号偏弱

### D. [[paperAnalysis/Motion_Generation/CVPR_2025/2025_MG_MotionLLM_A_Unified_Framework_for_Motion_Comprehension_and_Generation_across_Multiple_Granularities|MG-MotionLLM]]

- **定位**：统一粗粒度 / 细粒度 motion comprehension and generation
- **知识库关键词**：`multi-granularity / motion script / localization`
- **为什么重要**：对“动作语义细粒度对齐”非常关键，尤其是 motion localization 和细粒度编辑
- **开源情况**：✅ 官方仓库 `CVI-SZU/MG-MotionLLM`
- **Star**：约 **31**
- **可信度**：**中**
- **判断原因**：官方 repo 明确，但还处在早期传播阶段

### 4.1 小结

这一组里，如果你关心 **统一生成+理解**，最值得优先读和跟的是：

1. MotionGPT
2. MG-MotionLLM
3. AvatarGPT
4. M3GPT

---
## 4.2 动作生成大模型 / foundation model

### A. [[paperAnalysis/Motion_Generation/ECCV_2024/2024_LMM_Large_Motion_Model_for_Unified_Multi_Modal_Motion_Generation|LMM]]

- **定位**：通用多模态动作大模型，统一 16 数据集、10 任务
- **知识库关键词**：`MotionVerse / ArtAttention / generalist diffusion-transformer`
- **为什么重要**：它代表“motion foundation model”思路，而不是单任务 text-to-motion
- **开源情况**：✅ 官方仓库 `mingyuan-zhang/LMM`
- **Star**：约 **307**
- **可信度**：**高**
- **判断原因**：官方 repo 明确，数据/模型/任务统一叙事完整，社区关注度不错

### B. [[paperAnalysis/Motion_Generation/Tencent_HY/2025_HY_Motion_1_0_Scaling_Flow_Matching_Text_to_Motion|HY-Motion 1.0]]

- **定位**：10 亿参数级 text-to-motion 大模型，三阶段训练（预训练→高质微调→RL 对齐）
- **知识库关键词**：`1B+ / flow matching / large-scale pretraining / RLHF`
- **为什么重要**：这是目前最接近“工业级 open-source 动作大模型”的路线
- **开源情况**：✅ 官方仓库 `Tencent-Hunyuan/HY-Motion-1.0`
- **Star**：约 **2237**
- **可信度**：**高**
- **判断原因**：腾讯组织官方、热度高、项目页和 HuggingFace 生态配套明显

### C. [[paperAnalysis/Human_Interaction/ICCV_2025/2025_Being_M0_5_A_Real_Time_Controllable_Vision_Language_Motion_Model|Being-M0.5]]

- **定位**：实时可控 VLMM，强调部位级控制和大规模数据 HuMo100M
- **知识库关键词**：`VLMM / real-time / part-aware tokenization`
- **为什么重要**：如果你关心“动作大模型 + 实时推理 + 局部控制”，它很有参考价值
- **开源情况**：⚠️ 目前**没有核到该论文对应的明确官方 repo**
- **Star**：—
- **可信度**：**低**
- **判断原因**：只找到组织相关仓库，无法确认就是论文的官方实现

### D. [[paperAnalysis/Human_Interaction/CVPR_2025/2025_HSI_GPT_A_General_Purpose_Large_Scene_Motion_Language_Model_for_HumanScene_Interaction|HSI-GPT]]

- **定位**：统一 scene-motion-language 的大模型，适合 human-scene interaction
- **知识库关键词**：`scene-motion-language / next-token prediction / HSI`
- **为什么重要**：如果你把“动作大模型”理解为更广义的 embodied motion model，它值得关注
- **开源情况**：⚠️ 未检到官方 repo
- **Star**：—
- **可信度**：**低**
- **判断原因**：公开论文明确，但代码证据不足

### 4.2 小结

如果你的目标是 **“可直接拿来跟进的动作大模型”**，当前最强候选是：

1. HY-Motion 1.0
2. LMM

如果是 **“概念上很强，但开源落地还不稳”**，则是：

- Being-M0.5
- HSI-GPT
---
## 4.3 动作-语义对齐

### A. [[paperAnalysis/Motion_Generation/CVPR_2026/2026_MoLingo_Motion_Language_Alignment_for_Text_to_Motion_Generation|MoLingo]]

- **定位**：在连续潜空间中显式做 motion-language semantic alignment
- **知识库关键词**：`semantic latent space / InfoNCE / text conditioning`
- **为什么重要**：它直接把“语义对齐”变成潜空间结构问题，而不是只改生成器
- **开源情况**：✅ 官方仓库 `hynann/MoLingo`
- **Star**：约 **55**
- **可信度**：**中-高**
- **判断原因**：官方 repo 明确，方法聚焦、开源清晰，但还比较新

### B. [[paperAnalysis/Motion_Generation/CVPR_2025/2025_AToM_Aligning_Text_to_Motion_Model_Event_Level_GPT4Vision_Reward|AToM]]

- **定位**：事件级 text-motion alignment，用 GPT-4V reward 做偏好学习
- **知识库关键词**：`event-level alignment / DPO / GPT4V reward`
- **为什么重要**：它把“动作-文本对齐”从句级提升到事件级（完整性 / 时序 / 频率）
- **开源情况**：✅ 官方仓库 `VincentHancoder/AToM`
- **Star**：约 **18**
- **可信度**：**中**
- **判断原因**：官方性明确，但项目较新，社区热度还没起来

### C. [[paperAnalysis/Motion_Generation/CVPR_2025/2025_The_Languate_of_Motion_Unifying_Verbal_and_Non_verbal_Language_of_3D_Human_Motion|The Language of Motion]]

- **定位**：统一 verbal（speech/text）与 non-verbal（gesture/expression）
- **知识库关键词**：`verbal/non-verbal / compositional body tokenization`
- **为什么重要**：它把语音、文本、身体动作三者放进统一语义空间，是“动作-语义对齐”很强的代表作
- **开源情况**：✅ 官方仓库 `Juzezhang/language_of_motion`
- **Star**：约 **90**
- **可信度**：**高**
- **判断原因**：官方 repo 清晰，定位明确，项目形态较完整

### D. MG-MotionLLM（细粒度对齐视角）

- 关联论文：[[paperAnalysis/Motion_Generation/CVPR_2025/2025_MG_MotionLLM_A_Unified_Framework_for_Motion_Comprehension_and_Generation_across_Multiple_Granularities|MG-MotionLLM]]
- **定位**：通过 motion script 和 localization 建立粗/细粒度语义对齐
- **知识库关键词**：`granularity-synergy / motion script / localization`
- **为什么重要**：它虽然不完全是“alignment paper”，但在细粒度动作-语言对齐上很强
- **开源情况**：✅ 官方仓库
- **Star**：约 **31**
- **可信度**：**中**

### E. [[paperAnalysis/Motion_Generation/AAAI_2025/2025_RemoGPT_Part_Level_Retrieval_Augmented_Motion_Language_Models|ReMoGPT]]

- **定位**：part-level retrieval-augmented motion-language alignment
- **知识库关键词**：`part-level retrieval / retrieval-augmented / body-part control`
- **为什么重要**：很适合借鉴到“细粒度动作-语义对齐 + 检索增强”研究里
- **开源情况**：⚠️ 未检到官方 repo
- **Star**：—
- **可信度**：**低**
- **判断原因**：论文思路强，但公开代码证据不足

### 4.3 小结

如果你研究的是 **“动作-语义对齐”**，优先级建议：

1. MoLingo
2. The Language of Motion
3. AToM
4. MG-MotionLLM
5. ReMoGPT（偏研究启发，不偏复现）

---
## 五、我建议的阅读 / 复现顺序

### 路线 A：如果你偏“统一 MotionLLM”

1. [[paperAnalysis/Motion_Generation/NeurIPS_2023/2023_MotionGPT_Human_Motion_as_Foreign_Language|MotionGPT]]
2. [[paperAnalysis/Motion_Generation/CVPR_2024/2024_All_in_One_Framework_for_Motion_Understanding_Planning_Generation_and_Beyond|AvatarGPT]]
3. [[paperAnalysis/Motion_Generation/NeurIPS_2024/2024_An_Advanced_Multimodal_Multitask_Framework_for_Motion_Comprehension_and_Generation|M3GPT]]
4. [[paperAnalysis/Motion_Generation/CVPR_2025/2025_MG_MotionLLM_A_Unified_Framework_for_Motion_Comprehension_and_Generation_across_Multiple_Granularities|MG-MotionLLM]]

### 路线 B：如果你偏“动作 foundation model / 大模型”

1. [[paperAnalysis/Motion_Generation/ECCV_2024/2024_LMM_Large_Motion_Model_for_Unified_Multi_Modal_Motion_Generation|LMM]]
2. [[paperAnalysis/Motion_Generation/Tencent_HY/2025_HY_Motion_1_0_Scaling_Flow_Matching_Text_to_Motion|HY-Motion 1.0]]
3. [[paperAnalysis/Human_Interaction/ICCV_2025/2025_Being_M0_5_A_Real_Time_Controllable_Vision_Language_Motion_Model|Being-M0.5]]（更偏概念参考）
4. [[paperAnalysis/Human_Interaction/CVPR_2025/2025_HSI_GPT_A_General_Purpose_Large_Scene_Motion_Language_Model_for_HumanScene_Interaction|HSI-GPT]]（更偏 embodied 扩展）

### 路线 C：如果你偏“动作-语义对齐 / 检索增强 / 对齐学习”

1. [[paperAnalysis/Motion_Generation/CVPR_2026/2026_MoLingo_Motion_Language_Alignment_for_Text_to_Motion_Generation|MoLingo]]
2. [[paperAnalysis/Motion_Generation/CVPR_2025/2025_The_Languate_of_Motion_Unifying_Verbal_and_Non_verbal_Language_of_3D_Human_Motion|The Language of Motion]]
3. [[paperAnalysis/Motion_Generation/CVPR_2025/2025_AToM_Aligning_Text_to_Motion_Model_Event_Level_GPT4Vision_Reward|AToM]]
4. [[paperAnalysis/Motion_Generation/AAAI_2025/2025_RemoGPT_Part_Level_Retrieval_Augmented_Motion_Language_Models|ReMoGPT]]

---
## 六、研究选题层面的启发

### 6.1 现在最稳的开源底座

- **MotionGPT**：最经典、最稳
- **HY-Motion 1.0**：最像工业级大模型底座
- **LMM**：最像 motion foundation model

### 6.2 现在最值得做增量创新的空白

- **统一生成+理解 + 细粒度对齐 + 强开源生态** 还没有完全统一
- 很多论文有很强的方法，但 **开源弱**：如 HSI-GPT、Being-M0.5、ReMoGPT
- 很多项目有代码，但 **社区热度不高**：如 M3GPT、MG-MotionLLM、AToM

### 6.3 如果要做你自己的研究路线

我会优先考虑下面几个组合：

1. **MotionGPT / HY-Motion 1.0 作为底座**
   - 往上加细粒度 semantic alignment
   - 或加 retrieval augmentation / event-level control

2. **MG-MotionLLM + MoLingo**
   - 一个偏细粒度统一理解生成
   - 一个偏潜空间语义对齐
   - 组合起来很适合做“可控 + 对齐”的新方向

3. **HY-Motion 1.0 + AToM**
   - 大模型底座 + 偏好对齐
   - 很适合做“动作生成 RLHF / RLAIF”路线

---
## 七、附：本次联网核查到的官方 / 候选仓库

- MotionGPT: [OpenMotionLab/MotionGPT](https://github.com/OpenMotionLab/MotionGPT)
- AvatarGPT: [zixiangzhou916/AvatarGPT](https://github.com/zixiangzhou916/AvatarGPT)
- M3GPT: [luomingshuang/m3gpt](https://github.com/luomingshuang/m3gpt)
- MG-MotionLLM: [CVI-SZU/MG-MotionLLM](https://github.com/CVI-SZU/MG-MotionLLM)
- LMM: [mingyuan-zhang/LMM](https://github.com/mingyuan-zhang/LMM)
- HY-Motion 1.0: [Tencent-Hunyuan/HY-Motion-1.0](https://github.com/Tencent-Hunyuan/HY-Motion-1.0)
- The Language of Motion: [Juzezhang/language_of_motion](https://github.com/Juzezhang/language_of_motion)
- AToM: [VincentHancoder/AToM](https://github.com/VincentHancoder/AToM)
- MoLingo: [hynann/MoLingo](https://github.com/hynann/MoLingo)

未稳定核到官方仓库：

- HSI-GPT
- Being-M0.5
- ReMoGPT