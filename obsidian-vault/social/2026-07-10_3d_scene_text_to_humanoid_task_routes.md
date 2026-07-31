---
title: "从文本到 3D 场景人形搬运：2024–2026 路线图与关键工作"
type: research-synthesis
status: complete
created: 2026-07-10T12:15:00+08:00
updated: 2026-07-10T12:28:00+08:00
tags:
  - humanoid_robotics
  - text_to_motion
  - vision_language_action
  - sim_to_real
  - loco_manipulation
  - 3d_gaussian_splatting
source_papers:
  - "[[analysis/ICLR_2024/UniHSI_Unified_Human_Scene_Interaction_via_Prompted_Chain_of_Contacts|UniHSI]]"
  - "[[analysis/NEURIPS_2024/HumanVLA_Towards_Vision_Language_Directed_Object_Rearrangement_by_Physical_Humanoid|HumanVLA]]"
  - "[[analysis/SIGGRAPH_2024/SuperPADL_Scaling_Language_Directed_Physics_Based_Control_with_Progressive_Supervised_Distillation|SuperPADL]]"
  - "[[analysis/SIGGRAPH_ASIA_2024/LINGO_Autonomous_Character_Scene_Interaction_Synthesis_from_Text_Instruction|LINGO]]"
  - "[[analysis/arxiv_2025/BeyondMimic_From_Motion_Tracking_to_Versatile_Humanoid_Control_via_Guided_Diffusion|BeyondMimic]]"
  - "[[analysis/arxiv_2025/GaussGym_An_Open-Source_Real-to-Sim_Framework_for_Learning_Locomotion_from_Pixels|GaussGym]]"
  - "[[analysis/arxiv_2026/PhyGile_Physics_Prefix_Guided_Motion_Generation_for_Agile_General_Humanoid_Motion_Tracking|PhyGile]]"
  - "[[analysis/arxiv_2026/VLK_Learning_Humanoid_Loco-Manipulation_from_Synthetic_Interactions_in_Reconstructed_Scenes|VLK]]"
  - "[[analysis/CVPR_2026/Scalable_Trajectory_Generation_for_Whole_Body_Mobile_Manipulation|AutoMoMa]]"
---

# 从文本到 3D 场景人形搬运：2024–2026 路线图与关键工作

> [!abstract] 核心判断
> “根据文本在真实室内场景搬东西”不是 text-to-motion 的直接放大，而是一个**视觉语言条件的全身移动操作**问题。近三年的共识路线是：用语言规定任务和接触意图，用视觉定位当前场景，用合成或特权数据教会策略从视觉恢复行动线索，再由高频物理控制器将短时全身轨迹安全执行。[[analysis/arxiv_2026/VLK_Learning_Humanoid_Loco-Manipulation_from_Synthetic_Interactions_in_Reconstructed_Scenes|VLK]] 最接近这条完整闭环；它把前人分别解决的“任务表示、特权教师、场景数据、物理执行”首次紧密地连到真机搬运。

## 一、从 text-to-motion 到 text-to-task：中间缺了什么

text-to-motion 通常回答“这句话对应怎样一段骨架动作”，例如挥手或转身；而“把桌上的箱子搬到门边”还必须同时回答四个问题：

- **看什么**：从机器人第一视角找出箱子、桌面、障碍物和可走区域；
- **先做什么**：把长指令拆为走近、对准、抓取、搬运、放置等阶段；
- **怎样接触**：在何时让哪只手接触物体、双脚怎样保持支撑；
- **怎样真的做出来**：将参考姿态变成考虑关节限位、力矩、质量、摩擦和扰动的关节动作。

因而，当前最稳妥的系统接口是：`第一视角图像 + 当前文本子指令 + 本体状态 + 接触状态 → 下一秒全身参考轨迹 → 全身 tracker → 关节动作`。模型每次只预测短轨迹；机器人执行后重新观察，再预测下一段。这样视觉误差、物体移动和抓取失败不会在一次很长的生成里无限累积。

### 物理与 RL 的最小解释

**运动学轨迹**规定“身体想摆成什么样”，并不保证不会摔倒；**tracker** 是高速稳定器，持续把真实身体拉回参考轨迹，并在脚或手接触时调整动作。强化学习（RL）通常用于训练这个 tracker 或仿真中的特权教师：完成目标、保持平衡、避免碰撞会得到更高奖励。它不是让机器人从零靠奖惩理解一句自然语言，而是解决“在物理世界中如何可靠执行已有目标”的层。

## 二、路线如何形成：从场景动作合成到真机视觉语言操作

### 2024：先把长任务拆成场景、接触和可执行技能

2024 年的关键进展是认识到长时人—场景交互不能靠一段无结构的动作完成。[[analysis/SIGGRAPH_ASIA_2024/LINGO_Autonomous_Character_Scene_Interaction_Synthesis_from_Text_Instruction|LINGO]] 用双体素场景表示、文本条件的自回归扩散和自主调度器，把行走、避障、伸手等片段衔接为角色—场景交互。它说明了文本、场景和阶段转换应共同决定下一段运动；但它的输出仍是角色运动，未解决真实机器人的动力学执行。

另一条更接近物理控制的思路来自 [[analysis/ICLR_2024/UniHSI_Unified_Human_Scene_Interaction_via_Prompted_Chain_of_Contacts|UniHSI]]。它把“拿起”“坐下”等任务表示为**接触链**：一串“哪个关节在何时接触哪个物体部件、接触方向如何”的约束。LLM 把语言转成接触链，统一控制器将其转为观测和奖励。这给今天的搬运系统留下一个重要接口：语言不应只给一个模糊动作 token，还应提供可验证的接触阶段。

同年，[[analysis/NEURIPS_2024/HumanVLA_Towards_Vision_Language_Directed_Object_Rearrangement_by_Physical_Humanoid|HumanVLA]] 已经把任务推进到“视觉语言引导的人形物体重排”。它先用物体精确状态训练目标条件 RL 教师，再以 DAgger 将其蒸馏为只看自我中心视觉和语言的学生，并加入搬运课程、路径规划和主动渲染。它是 VLK 之前最直接的系统祖先：**出数据和训练教师时可以看特权状态，部署学生时只能看视觉与语言**。

### 2025：把两个瓶颈推到可扩展——视觉仿真与物理动作先验

[[analysis/arxiv_2025/GaussGym_An_Open-Source_Real-to-Sim_Framework_for_Learning_Locomotion_from_Pixels|GaussGym]] 把 3D Gaussian Splatting（3DGS）作为矢量化物理引擎的渲染后端，自动对齐视觉重建与碰撞网格，并在单张 RTX 4090、4096 并行环境、640×480 条件下报告超过 10 万步/秒。它的价值不在语言或抓取本身，而在于让机器人能从 RGB 大规模训练：视觉能带来深度图没有的语义线索，而仿真仍足够快供 RL 试错。

执行端则出现了更强的“动作先验 + 物理控制”组合。[[analysis/SIGGRAPH_2024/SuperPADL_Scaling_Language_Directed_Physics_Based_Control_with_Progressive_Supervised_Distillation|SuperPADL]] 先在小规模上用 RL 学高质量动作专家，再渐进蒸馏到能覆盖数千动作的通用语言条件控制器，说明 RL 的质量和监督学习的规模可以分工。[[analysis/arxiv_2025/BeyondMimic_From_Motion_Tracking_to_Versatile_Humanoid_Control_via_Guided_Diffusion|BeyondMimic]] 则用统一 RL 跟踪器建立稳定的真实人形动作，再用潜状态—动作扩散在测试时以可微目标引导，完成航点、避障和动作补全等新目标。

这两类工作共同改变了对 RL 的理解：RL 不必承担语言、视觉、规划和动作生成的全部负担，它更适合做可靠的物理技能库或 tracker；上层可以通过蒸馏、扩散引导或视觉策略调用这些技能。

### 2026：数据工厂与短时闭环，开始把移动操作接到真实场景

2026 年的突出趋势是承认数据规模和数据接口才是端到端移动操作的刚性约束。[[analysis/CVPR_2026/Scalable_Trajectory_Generation_for_Whole_Body_Mobile_Manipulation|AutoMoMa]] 将移动底座、机械臂与物体统一为增强运动学链，在 GPU 上批量轨迹优化和碰撞检测，生成 50 万以上物理有效全身轨迹；这说明高质量演示不必都靠人工遥操作。

[[analysis/arxiv_2026/VLK_Learning_Humanoid_Loco-Manipulation_from_Synthetic_Interactions_in_Reconstructed_Scenes|VLK]] 把该思想推进到人形真实室内环境：它从 iPhone 重建米制 3DGS 房间，借助特权场景几何合成走向、抓取、放置轨迹，然后从机器人眼睛重新渲染图像，得到严格配对的图像—语言—运动学监督。每个场景可自动得到 48,000 条轨迹；策略预测一秒、30 Hz 的全身运动学轨迹，接触感知 tracker 以 50 Hz 执行到 Unitree G1。它用纯合成训练在真机进行导航和单物体搬运，长任务由流式子指令串接。

## 三、当前主流的四层系统，以及每层该借谁的思想

### 1. 任务与接触层：把语言变成可检查的阶段约束

高层不应直接将整句文本映射为数分钟关节轨迹。更好的形式是持续输出“当前目标物、目标位置、阶段、接触意图”。UniHSI 的接触链说明接触是语言与物理控制之间的紧凑桥梁；LINGO 的阶段调度说明走路、避障和交互需要显式切换。对于“搬箱子”，可从 `walk-to(box) → wrist-contact(box) → carry(box) → place(box, table)` 这样的原子阶段开始。

### 2. 场景与数据层：利用特权状态造题，而不是部署时作弊

重建出的 3DGS 场景能提供与真实房间外观一致的相机图像；碰撞网格、物体姿态和可行走区域则只在生成数据时使用。GaussGym 说明这种视觉—几何对齐可以高吞吐量地服务 RL；AutoMoMa 说明全身操作轨迹可以 GPU 批量合成；VLK 则将二者变成第一视角图像、文本和机器人轨迹的监督三元组。

关键边界是：视觉真实不等于物理真实。3DGS 主要保证渲染，碰撞、摩擦、质量、可抓取性仍需单独建模、随机化和真机验证。因而“真实到仿真”是获得廉价训练世界，而不是取消物理建模。

### 3. 感知—运动层：只预测短时、机器人原生的全身参考

HumanVLA 的教师—学生蒸馏和 VLK 的图像—语言—运动学监督都遵循同一原则：训练可使用精确状态来获得强教师或可靠标签，部署的学生只使用第一视角视觉、语言和自身传感器。VLK 的短时轨迹预测尤其适合真机，因为每秒都可重新观察、纠正目标位置与物体状态。

[[analysis/arxiv_2026/PhyGile_Physics_Prefix_Guided_Motion_Generation_for_Agile_General_Humanoid_Motion_Tracking|PhyGile]] 对这一层补上“轨迹必须适合机器人”。它不处理场景视觉和搬运任务，但直接在机器人原生 262 维表示中生成，并以已被 tracker 验证的物理前缀约束后续扩散生成，避免人类动捕重定向后看似合理却不可执行的问题。它可作为 VLK 式系统的运动先验或增强 tracker，而不能替代视觉语言策略。

### 4. 物理执行层：让接触标签与 tracker 留在闭环中

低层 tracker 必须以远高于视觉模型的频率运行，接收短时参考、当前本体状态和接触状态，输出关节控制。SuperPADL、BeyondMimic、PhyGile 分别提供了三种可扩展的技能/跟踪思路；VLK 的真机结果则直接证明接触状态不是附属信息：去掉腕部接触标签后，其地面抓取真机试验为 0/5。

因此，在当前任务中，RL 最自然的职责是训练稳定控制器和特权教师，或为合成轨迹作物理筛选；语言模型负责阶段与对象语义，视觉模型负责从当前画面恢复任务相关状态。把这三者强行压成一个直接输出力矩的大模型，现阶段通常更难训练、也更难排查失败。

## 四、这三篇新论文究竟新增了什么，而非重复前人

PhyGile、GaussGym、VLK 并不是三个竞争的完整 text-to-task 系统，而是分别把已有路线的薄弱接口推进了一步：

- **PhyGile**：将“文本动作生成”改为“机器人原生、物理前缀约束的生成—跟踪闭环”。相对 SuperPADL/BeyondMimic 的核心新增是生成器与可执行 tracker 的更紧密共享接口；但仍主要验证平地敏捷运动，不等于已具备场景搬运能力。
- **GaussGym**：将 3DGS 从高保真但慢的重建表示，变为能与大规模并行物理仿真共同训练的 RGB 渲染后端。相对 HumanVLA 的主动渲染，它更强调场景来源与吞吐；但主要验证 locomotion/导航，尚未给出语言抓取闭环。
- **VLK**：将 HumanVLA 的特权教师—视觉学生逻辑、GaussGym 式真实场景重建、短时参考—tracker 执行组合为一条数据工厂。它的关键不是提出一个孤立的新网络，而是生成完整且同步的 VLK 三元组，并把它们部署到真机移动搬运。

从系统覆盖看，VLK 是当前最直接的主框架；GaussGym 为它的场景训练规模提供支撑；PhyGile 为它的敏捷与物理可执行动作提供可嫁接的改进。UniHSI 的接触链则是值得加入 VLK 数据和高层规划的缺失结构：目前 VLK 已使用接触标签，但还没有把接触序列提升为通用语言规划接口。

## 五、面向当前目标的最小可行研究路线

不要从“开放词汇、任意物体、任意房间”起步。建议以一间静态房间、单一可抓取箱子、两类表面和四个原子技能为第一闭环：

1. 重建房间，建立视觉渲染与碰撞几何的共同坐标系；
2. 用特权场景状态自动产生 `walk-to / pick / carry / place` 轨迹，并保留腕部和脚部接触标签；
3. 以第一视角图像、模板化短指令和本体状态训练一秒全身轨迹预测器；
4. 使用已验证的全身 tracker 执行，部署时滚动重预测；
5. 分别测量感知定位、接触成功、轨迹跟踪与完整任务成功，避免只报告一个终局成功率；
6. 基础闭环稳定后，再引入 PhyGile 式物理前缀或 BeyondMimic 式可微目标引导，提高动作覆盖与恢复能力。

> [!warning] 最重要的风险
> 长任务失败常来自接口不同步，而不是某一层模型不够大：图像时间戳、语言阶段、物体状态、接触标签和参考轨迹若未严格对齐，tracker 再强也会执行错误目标。VLK 的价值正是把这些接口作为数据产品共同生成；后续研究应优先验证这些接口的可观测性和可纠错性。

## 关联笔记

- [[analysis/ICLR_2024/UniHSI_Unified_Human_Scene_Interaction_via_Prompted_Chain_of_Contacts|UniHSI：语言到接触链]]
- [[analysis/NEURIPS_2024/HumanVLA_Towards_Vision_Language_Directed_Object_Rearrangement_by_Physical_Humanoid|HumanVLA：特权教师到视觉语言学生]]
- [[analysis/SIGGRAPH_2024/SuperPADL_Scaling_Language_Directed_Physics_Based_Control_with_Progressive_Supervised_Distillation|SuperPADL：可扩展物理技能蒸馏]]
- [[analysis/SIGGRAPH_ASIA_2024/LINGO_Autonomous_Character_Scene_Interaction_Synthesis_from_Text_Instruction|LINGO：文本驱动阶段化场景交互]]
- [[analysis/arxiv_2025/BeyondMimic_From_Motion_Tracking_to_Versatile_Humanoid_Control_via_Guided_Diffusion|BeyondMimic：可引导的通用人形控制]]
- [[analysis/arxiv_2025/GaussGym_An_Open-Source_Real-to-Sim_Framework_for_Learning_Locomotion_from_Pixels|GaussGym：高吞吐量视觉仿真]]
- [[analysis/arxiv_2026/PhyGile_Physics_Prefix_Guided_Motion_Generation_for_Agile_General_Humanoid_Motion_Tracking|PhyGile：物理前缀生成—执行闭环]]
- [[analysis/arxiv_2026/VLK_Learning_Humanoid_Loco-Manipulation_from_Synthetic_Interactions_in_Reconstructed_Scenes|VLK：重建场景的合成 VLK 监督]]
- [[analysis/CVPR_2026/Scalable_Trajectory_Generation_for_Whole_Body_Mobile_Manipulation|AutoMoMa：规模化全身移动操作轨迹]]
