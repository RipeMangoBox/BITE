---

## title: "小课题组科研方向与技术分享路线图"
created: 2026-07-03T00:00:00+08:00
updated: 2026-07-03T00:00:00+08:00
type: social
tags:
  - group_strategy
  - research_roadmap
  - post_training
  - motion_generation
  - scene_graph
  - gaussian_splatting
  - vr_affective_computing

# 小课题组科研方向与技术分享路线图

> [!abstract] 核心结论
> 对当前组内资源条件，最理性的路线不是去卷大模型预训练、通用视频生成、纯指标型 4DGS 或纯封闭集场景图，而是围绕 **真实项目入口 + 小算力后训练 + 结构化评测 + 可交互系统 demo** 建立组内共同技术底座。  
> 优先级建议：**动作生成/虚拟人后训练与评测**、**场景图/知识图谱/Agent 规划**、**4DGS 交互编辑与空间计算**、**VR 情感闭环应用**。高能物理与光方向建议定位为 **科学仪器/数据智能体/可视分析/交互系统**，不要贸然做核心物理发现模型。

## 0. 判断前提

### 组内客观约束

- 人力：约 4 个博士、10 个硕士，属于能做 2-4 条主线、若干工程/数据子题的规模。
- 算力：4 卡 RTX 5090、2 卡 L40、2 卡 RTX 4090。适合中小模型后训练、扩散/3DGS 单场景优化、VLM/LLM LoRA、奖励模型、数据构建、评测系统；不适合从零预训练大模型或大规模视频生成基础模型。
- 已有方向：人体动作生成、高能物理与光研究、4DGS 生成/重建/编辑、场景图、VR 情感计算。
- 导师公开主页显示的研究与项目入口包括：多模态场景智能理解、交互可视分析与混合现实、知识驱动场景仿真与数字孪生、可控情感数字人、工业和科学计算大模型；近年项目包含焊接知识图谱、同步辐射实验统一用户交互界面、HEPS 数据获取 GUI、数据智能体、多模态开集场景图、城市三维空间建模渲染等。外部来源见[导师主页](https://faculty.ecnu.edu.cn/_s16/hgq2/main.psp)。

### 我的基本立场

不要把“热门方向”本身当创新点。后训练、Agent、RAG、VLA、3DGS、场景图都只是工具层，论文贡献必须落到一个具体任务瓶颈：数据不可靠、评测不可信、物理不可执行、交互不可实时、场景理解不能闭环、工业流程不能落地。

对小课题组，最有性价比的贡献类型是：

- **后训练**：在已有开源模型上做奖励、偏好、SFT/DPO/GRPO/RFT、测试时适配、数据过滤，而不是训练基础模型。
- **评测与验证**：把“看起来合理”变成可测的语义一致性、物理可行性、任务成功率、用户偏好、延迟、显存、鲁棒性。
- **结构化中间表示**：场景图、知识图谱、运动 token、物理状态、用户状态，把 VLM/LLM 的黑箱输出变成可检查、可修正、可部署的系统。
- **系统型 demo**：VR/数字孪生/科学仪器/工业知识库这些方向，论文和就业价值都依赖可展示的端到端系统。

## 1. 优先方向总览


| 优先级 | 方向                      | 为什么适合小课题组                    | 最可能产出                            | 主要风险                    |
| --- | ----------------------- | ---------------------------- | -------------------------------- | ----------------------- |
| P0  | 动作生成与虚拟人的后训练、奖励、评测      | 组内已有动作生成基础；后训练比预训练省算力；工业应用明确 | CCF A/B 论文、开源 benchmark、数字人 demo | 奖励模型不可信、只刷 HumanML3D 指标 |
| P0  | 场景图/知识图谱 + VLM/Agent 规划 | 与导师项目和工业 KG 强相关；结构化中间表示有真实需求 | 场景理解、机器人/运维/工业 Agent 系统          | 只做封闭集 SGG 指标会红海且应用弱     |
| P1  | 4DGS 交互编辑/动态重建/VR 空间计算  | 与图形学和数字孪生契合；可做系统型工作          | SIGGRAPH/ACM MM/VR 方向 demo       | 纯 PSNR/LPIPS 动态重建很卷     |
| P1  | VR 情感计算与可控情感数字人         | 结合组内 VR 与数字人资产；可做用户闭环        | CHI/VR/PG/多媒体交叉                  | 小样本问卷不足以支撑强论文           |
| P2  | AI4Science/高能物理与光的数据智能体 | 有项目入口；更适合做科学工作流工具            | 科学仪器交互、数据可视分析、实验 copilot         | 不要做无物理团队背书的核心物理模型       |


## 2. P0：动作生成要转向“后训练 + 评测 + 可执行”

### 2.1 方向判断

文本到动作、共语音手势、舞蹈生成、人-物交互这些方向已经过了“换一个扩散 backbone 刷指标”的阶段。更有价值的问题是：

- 生成动作是否真的符合文本、音乐、情绪、角色个性？
- 是否物理可执行，能不能被机器人/虚拟人控制器稳定跟踪？
- 是否支持用户偏好、导演意图、教育/康复/VR 任务目标？
- 评测是否可信，是否存在数据泄漏和指标错配？

本地 KB 中几个代表性证据：

- [[analysis/arxiv_2026/MotionRFT_Unified_Reinforcement_Fine-Tuning_for_Text-to-Motion_Generation|MotionRFT]]：用 MotionReward + EasyTune 做文本到动作强化微调，核心是统一异构运动表示奖励模型，并把去噪链反传的显存复杂度从随步数增长降到逐步独立优化；HumanML3D 上 FID 和 R-Precision 有明显提升。
- [[analysis/arxiv_2026/PhysMoDPO_Physically-Plausible_Humanoid_Motion_with_Preference_Optimization|PhysMoDPO]]：把预训练全身控制器作为黑盒物理验证器，用 DPO 让运动生成在物理跟踪后仍保持任务一致和可执行，说明“物理验证反馈”比手工脚滑惩罚更接近真实部署。
- [[analysis/arxiv_2026/MotionVLA_Vision-Language-Action_Model_for_Humanoid_Motion|MotionVLA]]：从频域发现位置/旋转偏低频、速度偏高频，用双流 tokenizer 解耦语义和物理动态；这说明运动表示本身是论文贡献点。
- [[analysis/arxiv_2026/OpenT2M_No_frill_Motion_Generation_with_Open_source_Large_scale_High_quality_Data|OpenT2M]]：指出 HumanML3D/Motion-X 存在验证文本与训练文本重叠，强调大规模高质量数据和数据泄漏清理对泛化评估的重要性。
- [[analysis/PG_2025/EmoDiffGes_Emotion_Aware_Co_Speech_Holistic_Gesture_Generation_with_Progressive_Synergistic_Diffusion|EmoDiffGes]]：情感不应是单个静态标签，而应是动态情感轨迹；身体区域也不应整体压缩或完全独立，而应区域化协同。

外部增强证据：

- [MotionRFT arXiv](https://arxiv.org/abs/2603.27185) 与[项目页](https://xiaofeng-tan.github.io/projects/MotionRFT/)显示动作生成已经开始系统引入强化微调、奖励模型和自精炼偏好学习。
- [MotionRL OpenReview](https://openreview.net/forum?id=v1OQ0kNq0w)说明文本到动作的人类偏好对齐仍是活跃问题。
- [What Can RL Bring to VLA Generalization?](https://arxiv.org/html/2505.19789v4)指出 VLA 仅靠 SFT 在分布转移下容易出现 compounding error，RL 可直接优化任务目标；这对动作生成、机器人和数字人都有共性启发。

### 2.2 建议组内主线

**主线 A：面向虚拟人动作生成的轻量后训练框架**

目标不是提出一个“又一个 T2M 模型”，而是做一个可以迁移到多个动作生成器的后训练层。

可做题目：

- 情绪一致性奖励：面向 co-speech gesture / 数字人，建立“语音情绪、文本情绪、面部/手势/姿态动态”的多维奖励。
- 物理可执行奖励：用现有运动控制器、运动学约束、脚滑/接触/jerk/平衡指标作为偏好构造器，做 DPO/RFT。
- 导演意图奖励：把“更有表现力、更克制、更专业、更像老师/销售/主持人”等风格偏好做成小规模 pairwise preference 数据。
- 长序列一致性后训练：重点解决动作漂移、重复、段落切换突兀，而不是单帧质量。

推荐技术栈：

- 先做 SFT/LoRA 和离线 reward reranking，再做 DPO/GRPO/RFT。
- 先用 7B 以内 LLM/VLM 或轻量 motion encoder 做奖励模型，不要上来训练大模型。
- 每个实验必须有三类指标：传统动作指标、任务指标、人工/偏好指标。

**主线 B：动作生成评测与数据卫生**

OpenT2M 的启发很直接：如果 benchmark 污染，模型排名没有意义。组内可以建立“动作生成可靠评测包”。

可做题目：

- 检测 HumanML3D、BEAT、AIST、Motion-X、组内数据的文本/动作泄漏。
- 建立面向长动作、复杂文本、情感变化、多人交互、场景约束的 stress test。
- 训练一个 motion judge，但必须加入反例与校准，不要只让 LLM/VLM 打分。

这个方向对硕士非常适合：工作量可控，工程价值高，容易和后训练主线互相喂数据。

### 2.3 不建议做的动作题

- 只换 backbone 刷 HumanML3D FID。
- 没有真实偏好数据却声称“人类偏好对齐”。
- 只有定性视频、没有任务成功率或失败分析。
- 把 LLM 加进 prompt decomposition 后就称为智能体。

## 3. P0：场景图要从“分类指标”转向“可验证中间表示”

### 3.1 方向判断

场景图是组内最应该继续投入的方向之一，因为它天然连接导师项目中的多模态场景理解、焊接知识图谱、数字孪生、开集场景图、工业数据智能体。问题是：不要困在 Visual Genome 上做封闭集谓词分类。

更有价值的路线是：

- 开放词汇与长尾关系；
- 图作为 VLM/Agent 的中间表示；
- 图生成后的验证、修正、任务规划；
- 实时全景场景图服务工业/VR/机器人系统；
- 工业知识图谱与视觉场景图融合。

本地 KB 代表证据：

- [[analysis/CVPR_2026/Mixture_of_Experts_based_Feature_Decoupling_for_Open_Vocabulary_Scene_Graph_Generation|MoE-FD]]：开放词汇 SGG 的瓶颈不是简单 VLM 对齐，而是缺少判别性属性解耦和物体-关系双向语义交互。
- [[analysis/CVPR_2026/Can_We_Build_Scene_Graphs_Not_Classify_Them_FlowSG_Progressive_Image_Conditioned_Scene_Graph_Generation_with_Flow_Matching|FlowSG]]：把场景图从“一次分类”改成混合离散-连续空间中的渐进生成过程，强调全局一致性和迭代修正。
- [[analysis/CVPR_2026/DSFlash_Comprehensive_Panoptic_Scene_Graph_Generation_in_Realtime|DSFlash]]：实时全景场景图的关键在共享骨干、双向单次关系预测、动态 token 剪枝；这类效率优化对工业部署比单纯指标更有价值。
- [[analysis/ICLR_2026/MomaGraph_State_Aware_Unified_Scene_Graphs_with_Vision_Language_Models_for_Embodied_Task_Planning|MomaGraph]]：Graph-then-Plan 明显优于直接规划，统一空间-功能图和零件级节点能提升具身任务规划。

外部增强证据：

- [MomaGraph arXiv](https://arxiv.org/html/2512.16909v2)明确把场景图定位为具身 Agent 的任务相关结构化表示，而不是普通关系检测输出。
- [Awesome Scene Graph Generation](https://github.com/ChocoWu/Awesome-Scene-Graph-Generation)列出的近年工作显示 SGG 正在向 VLM、动态环境、具身导航、3D 场景推理迁移。
- [VeriGraph](https://verigraph-agent.github.io/)强调用场景图和迭代验证提升机器人任务规划可靠性。

### 3.2 建议组内主线

**主线 C：工业场景图 + 知识图谱 + Agent 验证**

利用导师已有焊接知识图谱、工业运维、数字孪生项目，把场景图变成 Agent 的工作记忆和验证对象。

可做题目：

- 面向焊接/工厂/运维的开放词汇场景图：节点不仅是物体，还包括设备状态、工艺阶段、风险事件。
- 多模态知识图谱驱动的视觉问答与巡检：让 VLM 输出结构化图，再由规则/图数据库/LLM 共同验证。
- Verification Scene Graph：专门诊断 VLM 视觉逻辑断裂，做“先构图、再验证、再回答”。
- 实时 PSGG for digital twin：参考 DSFlash，把场景图生成做成低延迟服务，接入三维可视化或 VR。

**主线 D：Graph-then-Agent 组内公共平台**

搭一个轻量平台，让场景图成为所有方向可共用的中间层：

- 输入：图片/视频/3DGS/VR 场景/工业传感器日志。
- 输出：对象、关系、状态、时间变化、可执行动作、风险点。
- 工具：VLM 解析、规则校验、KG 查询、LLM 规划、日志回放。
- 评测：图准确率、任务成功率、幻觉率、延迟、人工修正成本。

这个平台能服务场景图、4DGS、VR、AI4Science 数据智能体多个方向。

### 3.3 不建议做的场景图题

- 只在封闭集 Visual Genome 上做一点 mR 提升。
- 只把 CLIP/VLM 特征拼进去，没有解释具体解决了什么关系错误。
- 没有下游任务，只输出一堆三元组。
- 没有错误分析，不区分感知错误、关系错误、知识错误、规划错误。

## 4. P1：4DGS 要做“交互/编辑/系统”，不要只做重建指标

### 4.1 方向判断

4DGS/3DGS 仍然热，但纯动态重建指标赛道非常拥挤。小组更适合做：

- 语义可编辑；
- 物理可交互；
- VR/数字孪生应用；
- 动态场景的低成本重建；
- 与场景图、Agent、用户交互结合。

本地 KB 代表证据：

- [[analysis/NEURIPS_2024/L4GM_Large_4D_Gaussian_Reconstruction_Model|L4GM]]：把静态 3D 高斯预训练迁移到 4D，通过时间自注意力传播首帧几何先验，说明“预训练 3D 先验 + 时间建模”比逐场景优化更适合交互式生产。
- [[analysis/NEURIPS_2024/MotionGS_Exploring_Explicit_Motion_Guidance_for_Deformable_3D_Gaussian_Splatting|MotionGS]]：动态 3DGS 不能直接用混合光流监督，必须剥离相机运动得到纯净对象运动流；这提示我们做动态重建要抓住因果运动信号。
- [[analysis/SIGGRAPH_2024/VR-GS_A_Physical_Dynamics-aware_Interactive_Gaussian_Splatting_System_in_Virtual_Reality|VR-GS]]：把 3DGS 与 XPBD 物理仿真接上，核心贡献是两级嵌入，让高斯能平滑响应物理交互。
- [[analysis/SIGGRAPH_2025/DreamCraft_Interactive_3D_Scene_Creation_From_Editable_Panorama_in_Virtual_Reality|DreamCraft]]：真正有应用价值的是“生成式 AI + VR 原生交互 + 3D 重建”的系统闭环，而不只是单个重建模块。

外部增强证据：

- [Instruct-4DGS](https://hanbyelcho.info/instruct-4dgs/)显示 4DGS 编辑已经成为 CVPR 2025 级别主题，重点是动态场景编辑效率和质量。
- [L4DGS OpenReview](https://openreview.net/forum?id=YgOY1QTEZj)显示语言引导 4DGS 正在和实时动态场景渲染结合。
- [Sparse4DGS AAAI 2026 PDF](https://ojs.aaai.org/index.php/AAAI/article/view/37848/41810)说明 sparse-frame dynamic scene reconstruction 仍有现实输入稀缺问题。

### 4.2 建议组内主线

**主线 E：场景图约束的 4DGS 编辑**

把场景图作为 4DGS 编辑的语义控制层：

- 用户说“把机器臂旁边的工具箱移开，并保持地面阴影合理”；
- 系统先生成对象-关系-约束图；
- 再执行高斯选择、分割、补全、编辑；
- 最后用图一致性、几何一致性、视频一致性验证。

可能贡献：

- 语义对象级高斯选择；
- 编辑前后关系保持；
- 动态对象运动一致性；
- VLM/scene graph 驱动的编辑验证。

**主线 F：VR/数字孪生中的交互式 Gaussian 系统**

不要只做重建。要做能给企业、导师项目、招聘面试看的系统：

- 城市三维空间/工厂数字孪生的 3DGS 浏览、标注、编辑；
- VR 中抓取、移动、检查 3DGS 对象；
- 物理/碰撞/状态变化接入；
- 与场景图/知识图谱/Agent 查询联动。

可分配给硕士的子题：

- 高斯对象分割与选取工具；
- 低延迟渲染和 LOD；
- 语义标签到高斯资产管理；
- VR 交互设计与用户研究；
- 编辑后多视角一致性评测。

### 4.3 不建议做的 4DGS 题

- 只提升某个动态场景 PSNR 0.2 dB。
- 没有交互、编辑、语义或系统价值的“又一个 4DGS”。
- 需要大量多视角设备或大规模数据采集，超出组内条件。
- Demo 只在作者挑选视频上好看，没有失败案例。

## 5. P1：VR 情感计算要做闭环，不要只做问卷

### 5.1 方向判断

VR 情感计算和可控情感数字人很符合导师公开方向，但论文风险在于：如果只做小样本用户问卷和普通情感分类，很容易弱。应该把它做成闭环：

感知用户状态 → 生成/调整虚拟人或环境 → 采集行为/生理/任务反馈 → 再适应。

本地 KB 代表证据：

- [[analysis/PG_2025/EmoDiffGes_Emotion_Aware_Co_Speech_Holistic_Gesture_Generation_with_Progressive_Synergistic_Diffusion|EmoDiffGes]]说明动态情感轨迹和身体区域协同对数字人表达很重要。
- [[analysis/arxiv_2023/Explainable_Multimodal_Emotion_Recognition|Explainable Multimodal Emotion Recognition]]把情感识别从封闭标签转为开放词汇解释，这对心理/教育/VR 场景更适合。
- [[analysis/SIGGRAPH_ASIA_2022/Transcendental_Avatar_Experiencing_Bioresponsive_Avatar_of_the_Self_for_Improved_Cognition|Transcendental Avatar]]用 HRV/EDA 驱动自我化身抽象度，体现了生理信号-虚拟化身闭环。
- [[analysis/SIGGRAPH_2025/DreamCraft_Interactive_3D_Scene_Creation_From_Editable_Panorama_in_Virtual_Reality|DreamCraft]]展示了 VR 原生交互和生成式 AI 结合的系统价值。

### 5.2 建议组内主线

**主线 G：情感可控数字人用于教育/心理/训练场景**

可做题目：

- 面向教师/讲解员/心理陪伴的动态情感手势生成；
- 用户压力/注意力驱动的虚拟人反馈策略；
- VR 公共安全/消防/工业培训中的情绪调节；
- 用可解释情感标签替代封闭分类标签。

最低可行评测：

- 行为指标：任务完成时间、错误率、回看次数、交互中断。
- 生理指标：HRV、EDA、眼动、头动稳定性，可选。
- 主观指标：presence、负荷、情绪、信任，但不能只靠问卷。
- 生成指标：动作自然度、情绪一致性、语义一致性、时序稳定。

### 5.3 不建议做的 VR 情感题

- 20 人以内小样本问卷就声称心理疗效。
- 没有对照组、没有任务指标、没有长期效果。
- 只做普通 FER/微表情分类，和 VR/交互/数字人无关。

## 6. P2：高能物理与光方向的现实定位

### 6.1 判断

如果组内没有稳定的物理专家、实验数据权限、长期项目绑定，不建议直接做“AI 发现新物理”“大模型理解高能物理”这类题。更现实、更可能产出的是：

- 科学仪器与实验工作流 Agent；
- 同步辐射/衍射/散射实验的用户交互与可视分析；
- 高维科学数据的检索、标注、异常检测、可视化；
- 论文/实验记录/脚本/参数/数据的知识库与助手；
- 数据采集 GUI 和插件系统的智能化。

这个定位与导师公开项目中的“同步辐射实验统一用户交互界面”“动态原位衍射散射实验智能反馈系统”“HEPS 数据获取 GUI”“数据智能体感知系统”更匹配。

### 6.2 建议组内主线

**主线 H：科学实验工作流 Copilot**

任务不是让 LLM 直接给科学结论，而是让它帮助科学家完成：

- 实验方案检索；
- 参数推荐与风险检查；
- 数据质量监控；
- 图表与报告自动生成；
- 历史实验记录问答；
- 插件调用和脚本生成。

研究贡献可以来自：

- 面向科学仪器的工具调用 Agent；
- 实验状态图/知识图谱；
- 可靠性评测与防幻觉机制；
- 人机协同可视分析。

### 6.3 Kill criteria

如果拿不到真实实验流程、真实数据样例、物理专家反馈，那么这个方向只适合做平台原型，不适合作为核心论文方向。

## 7. 组内应该共同掌握的科研技术

### 7.1 后训练技术栈

后训练不是论文创新本身，但会成为很多方向的基础能力。

建议分享顺序：

1. SFT/LoRA/QLoRA：会训，会排查数据格式和过拟合。
2. Preference data：pairwise、listwise、AI feedback、human feedback、hard negative。
3. DPO/IPO/KTO：先做离线偏好优化，风险低。
4. GRPO/RFT：用于需要采样、奖励函数、任务成功率优化的场景。
5. Reward model：奖励必须可校准、可解释、有反例集。
6. Evaluation harness：每次训练后自动输出指标、样例、失败分类。
7. Safety and robustness：不要让模型只学会 reward hacking。

外部学习材料：

- [DeepLearning.AI GRPO 课程](https://www.deeplearning.ai/courses/reinforcement-fine-tuning-llms-grpo)可作为入门技术材料。
- [Awesome VLA Post-Training](https://github.com/AoqunJin/Awesome-VLA-Post-Training)可跟踪 VLA 后训练论文。

### 7.2 Agent/RAG 工程技术栈

组内不要把 Agent 理解成“LLM + prompt”。必须掌握：

- 工具调用：文件、数据库、图数据库、可视化、仿真器、训练脚本。
- 记忆：短期任务状态、长期知识库、实验日志。
- 规划：任务分解、依赖检查、失败回滚。
- 验证：规则检查、图一致性检查、执行反馈。
- 观测：日志、trace、错误分类、人工修正。

适合落地到：

- 科研论文分析 Agent；
- 运动生成评测 Agent；
- 场景图验证 Agent；
- 工业知识图谱问答 Agent；
- 科学实验 GUI Copilot。

### 7.3 数据与评测技术栈

这是小组最应该补的基本功。

- 数据泄漏检测：文本相似度、embedding 聚类、near duplicate、视频/动作重复。
- 数据质量过滤：物理可行性、标注一致性、异常帧、传感器噪声。
- 统一评测：传统指标 + 任务指标 + 人类偏好 + 延迟/显存。
- 失败 taxonomy：把失败分成语义错、物理错、时序错、交互错、规划错、渲染错。
- 可复现实验：固定 seed、配置管理、结果表自动生成、样例 dashboard。

### 7.4 3D/4D/VR 工程技术栈

- 3DGS 基础训练、渲染、压缩、分割、编辑。
- SAM/Grounded-SAM/Track Anything 等对象分割跟踪工具。
- COLMAP/MASt3R/DUSt3R 类位姿与几何工具。
- Unity/Unreal/WebXR 至少一种交互展示栈。
- Gaussian asset 管理：对象级元数据、状态、版本、编辑历史。

## 8. 博士与硕士题目分配建议

### 博士题目


| 编号    | 题目                          | 目标贡献                        | 依赖         |
| ----- | --------------------------- | --------------------------- | ---------- |
| PhD-A | 面向数字人动作生成的奖励建模与后训练          | motion reward、DPO/RFT、长序列评测 | 动作生成、偏好数据  |
| PhD-B | Graph-then-Agent 的工业场景理解与验证 | 场景图 + KG + Agent 验证闭环       | 场景图、工业项目   |
| PhD-C | 语义约束的 4DGS 动态编辑系统           | 对象级高斯编辑、关系保持、多视角一致性         | 4DGS、场景图   |
| PhD-D | VR 情感数字人的闭环适应               | 用户状态感知、情感生成、任务反馈            | VR、动作/表情生成 |


### 硕士题目


| 编号    | 题目                                 | 可交付物                                        |
| ----- | ---------------------------------- | ------------------------------------------- |
| MS-1  | HumanML3D/Motion-X/BEAT 数据泄漏和压力测试包 | benchmark report + eval toolkit             |
| MS-2  | 动作生成 pairwise preference 标注与奖励模型   | preference dataset + reward model           |
| MS-3  | 物理可行性 motion checker               | foot sliding/contact/jerk/balance dashboard |
| MS-4  | 实时 PSGG 轻量服务                       | DSFlash-like inference service              |
| MS-5  | 工业场景图标注工具                          | image/video to graph annotation UI          |
| MS-6  | 3DGS 对象分割与高斯选择工具                   | interactive Gaussian selection plugin       |
| MS-7  | 4DGS 编辑一致性评测                       | multi-view/time consistency metrics         |
| MS-8  | VR 数字人用户研究平台                       | logging + questionnaire + behavior metrics  |
| MS-9  | 科学实验文档/数据 RAG                      | domain KB + tool calling demo               |
| MS-10 | 组内统一实验管理与论文复现模板                    | config + report + artifact registry         |


## 9. 六个月执行计划

### 第 0-1 月：统一底座

目标：不要急着开新题，先把技术债补上。

- 每人复现一个代表性开源项目或本地 KB 论文。
- 建立统一实验模板：数据路径、配置、日志、可视化、结果表。
- 建立组内 paper reading 规范：每篇必须讲清楚问题、因果瓶颈、changed slot、验证证据、可复用点。
- 确定 2 条 P0 主线和 2 条 P1 主线，每条主线有负责人。

验收：

- 每条主线至少有一个可运行 baseline。
- 每个 baseline 有失败样例和可视化。
- 明确 6 个月内能投什么 venue 或做什么 demo。

### 第 1-2 月：数据与评测先行

- 动作组：构建 stress test 与偏好标注协议。
- 场景图组：选定工业/室内/VR 场景数据，定义节点和关系 schema。
- 4DGS 组：实现对象级选择、编辑和一致性评测初版。
- VR 组：完成用户实验协议和日志系统。
- AI4Science 组：拿到真实流程样例，否则只做平台原型。

验收：

- 每条主线有一份问题诊断报告。
- 至少发现一个 baseline 明确失败模式。
- 失败模式能被指标捕捉，而不是只靠肉眼。

### 第 2-4 月：提出最小创新模块

每个方向只允许做一个核心 changed slot。

- 动作：一个奖励模型或一个 DPO/RFT 策略。
- 场景图：一个图验证或图更新机制。
- 4DGS：一个语义/关系约束编辑模块。
- VR：一个情感状态闭环策略。
- AI4Science：一个工具调用/实验状态图机制。

验收：

- 核心模块对至少两个 baseline 有稳定增益。
- 有消融：去掉模块会明显退化。
- 有失败分析：说明什么时候无效。

### 第 4-6 月：论文化或系统化

- 论文线：补齐 ablation、对比、泛化、用户研究或真实案例。
- 系统线：做端到端 demo、录屏、部署文档、用户流程。
- 工业线：争取真实场景反馈，哪怕是少量专家评价。

验收：

- 每条主线形成一个 paper draft 或 demo report。
- 所有实验可复现。
- 每篇草稿必须有“为什么不是工程堆叠”的论证。

## 10. 组会分享安排

### 10.1 第一轮：共同技术底座

1. 后训练总览：SFT、DPO、GRPO/RFT、Reward Model、Eval。
2. 场景图到 Agent：Graph-then-Plan、Graph Verification、工业 KG。
3. 3DGS/4DGS 系统：重建、编辑、交互、VR。
4. 数据与评测：泄漏检测、stress test、失败 taxonomy。

### 10.2 第二轮：方向专题

1. 动作生成后训练：MotionRFT、PhysMoDPO、MotionVLA、OpenT2M。
2. 开放词汇/实时/生成式场景图：MoE-FD、FlowSG、DSFlash、MomaGraph。
3. 4DGS 交互系统：L4GM、MotionGS、VR-GS、DreamCraft、Instruct-4DGS。
4. VR 情感数字人：EmoDiffGes、Transcendental Avatar、Explainable MER。
5. 科学工作流 Agent：实验 GUI、数据智能体、科学 RAG、可视分析。

## 11. 决策规则

### 11.1 选题必须回答的 8 个问题

1. 真实用户是谁？
2. 真实数据来自哪里？
3. baseline 为什么失败？
4. 失败能否被指标捕捉？
5. 核心 changed slot 是什么？
6. 为什么这个 changed slot 比堆模型更合理？
7. 6 个月内最低可发表/可展示结果是什么？
8. 如果失败，最迟什么时候停止？

### 11.2 Kill criteria

满足任一条件就应该调整或停止：

- 两个月内无法获得真实数据或可信替代数据。
- baseline 失败模式不稳定，无法复现。
- 提出的模块只在一个 cherry-picked 样例有效。
- 评测指标与肉眼/用户/任务结果明显不一致，且无法解释。
- 需要的算力超过组内资源，必须长期排队或租大量云卡。
- 论文贡献只能描述为“我们把 A 和 B 结合起来”。

## 12. 最后的建议

组内真正的优势不在算力，而在几个方向可以互相连接：

- 动作生成可以给 VR/数字人提供内容；
- VR/数字人可以提供偏好数据和用户反馈；
- 场景图可以给 4DGS 和 Agent 提供结构化中间表示；
- 4DGS 可以给数字孪生和 VR 提供真实空间载体；
- AI4Science/工业项目可以提供真实场景、数据和部署需求；
- 后训练和评测可以成为所有方向的共同方法底座。

如果能把这些连接做实，组内不需要追最贵的红海大模型，也能做出有就业竞争力、有论文价值、有真实应用感的研究。

## 参考源

### 本地 KB 重点论文

- [[analysis/arxiv_2026/MotionRFT_Unified_Reinforcement_Fine-Tuning_for_Text-to-Motion_Generation|MotionRFT]]
- [[analysis/arxiv_2026/PhysMoDPO_Physically-Plausible_Humanoid_Motion_with_Preference_Optimization|PhysMoDPO]]
- [[analysis/arxiv_2026/MotionVLA_Vision-Language-Action_Model_for_Humanoid_Motion|MotionVLA]]
- [[analysis/arxiv_2026/OpenT2M_No_frill_Motion_Generation_with_Open_source_Large_scale_High_quality_Data|OpenT2M]]
- [[analysis/PG_2025/EmoDiffGes_Emotion_Aware_Co_Speech_Holistic_Gesture_Generation_with_Progressive_Synergistic_Diffusion|EmoDiffGes]]
- [[analysis/CVPR_2026/Mixture_of_Experts_based_Feature_Decoupling_for_Open_Vocabulary_Scene_Graph_Generation|MoE-FD]]
- [[analysis/CVPR_2026/Can_We_Build_Scene_Graphs_Not_Classify_Them_FlowSG_Progressive_Image_Conditioned_Scene_Graph_Generation_with_Flow_Matching|FlowSG]]
- [[analysis/CVPR_2026/DSFlash_Comprehensive_Panoptic_Scene_Graph_Generation_in_Realtime|DSFlash]]
- [[analysis/ICLR_2026/MomaGraph_State_Aware_Unified_Scene_Graphs_with_Vision_Language_Models_for_Embodied_Task_Planning|MomaGraph]]
- [[analysis/NEURIPS_2024/L4GM_Large_4D_Gaussian_Reconstruction_Model|L4GM]]
- [[analysis/NEURIPS_2024/MotionGS_Exploring_Explicit_Motion_Guidance_for_Deformable_3D_Gaussian_Splatting|MotionGS]]
- [[analysis/SIGGRAPH_2024/VR-GS_A_Physical_Dynamics-aware_Interactive_Gaussian_Splatting_System_in_Virtual_Reality|VR-GS]]
- [[analysis/SIGGRAPH_2025/DreamCraft_Interactive_3D_Scene_Creation_From_Editable_Panorama_in_Virtual_Reality|DreamCraft]]



NoWay2030System

### Web 增强来源

- [何高奇教授主页](https://faculty.ecnu.edu.cn/_s16/hgq2/main.psp)
- [MotionRFT arXiv](https://arxiv.org/abs/2603.27185)
- [MotionRFT project](https://xiaofeng-tan.github.io/projects/MotionRFT/)
- [MotionRL OpenReview](https://openreview.net/forum?id=v1OQ0kNq0w)
- [What Can RL Bring to VLA Generalization?](https://arxiv.org/html/2505.19789v4)
- [MomaGraph arXiv](https://arxiv.org/html/2512.16909v2)
- [Awesome Scene Graph Generation](https://github.com/ChocoWu/Awesome-Scene-Graph-Generation)
- [VeriGraph project](https://verigraph-agent.github.io/)
- [Instruct-4DGS project](https://hanbyelcho.info/instruct-4dgs/)
- [Sparse4DGS AAAI 2026 PDF](https://ojs.aaai.org/index.php/AAAI/article/view/37848/41810)
- [L4DGS OpenReview](https://openreview.net/forum?id=YgOY1QTEZj)
- [Awesome VLA Post-Training](https://github.com/AoqunJin/Awesome-VLA-Post-Training)
- [DeepLearning.AI GRPO course](https://www.deeplearning.ai/courses/reinforcement-fine-tuning-llms-grpo)

