# 小红书 Human Motion 研究方向博主图谱

扫描日期: 2026-05-10 | 方法: MediaCrawler 关键词搜索 × 2轮 (QR码+CDP) + 博主交叉分析 | 覆盖帖子: 167条科研向 (去噪后) | 博主总数: 104

---

## 1. 核心博主画像

### 1.1 郭川不上班 (Eric Guo) — Humanoid Motion Generation 核心研究者

**身份**: SnapMoGen / LIGHT 作者，IJCV 综述一作
**小红书 ID**: `6297bf9e0000000021020351`
**GitHub**: Ericguo5513, snap-research

**代表性工作 (在小红书分享的)**:

| 工作 | 发表 | 核心贡献 |
|------|------|----------|
| SnapMoGen | ICLR | 高质量文本驱动 Text2Motion 数据集，44h MoCap，122K 细粒度标注（单条48词，HumanML3D的4倍） |
| LIGHT | ICLR 2026 | HOI + Diffusion Forcing，pace-induced guidance 替代 classifier guidance/contact prior |
| 3D人体交互综述 | IJCV | 生成式人体交互领域系统梳理，覆盖人-人/物/环境交互，含 benchmark 和 GitHub awesome list |

**学术观点 (从帖子提炼)**:
- Text2Motion 的核心瓶颈不是模型架构，而是**文本标注的粒度和质量**——类比图像生成中的 LLM prompt rewrite
- HOI 生成不需要额外的 classifier guidance/物理仿真，**模型可以通过 diffusion forcing 的多模态异步去噪学会自我引导**
- 人体-世界交互是"重要的未来研究方向"，目前还比较早期

**可追踪的合作者 (也在小红书)**:
- Sirui (UIUC) — LIGHT 主要作者
- wzy / Ziyin — LIGHT 主要作者

---

### 1.2 每日ComputerScience — 顶会论文速递

**小红书 ID**: `677419a40000000015005599`
**定位**: 论文解读 + 速递，覆盖 motion / 视频生成 / 物理仿真

**代表性分享**:
- 上交 & 港大 PALUM：骨架无关全骨架动作重定向
- 斯坦福：动作→物理→生成的 4D 世界模型
- UCSD & Google DiT-Mem：10K 数据让视频 AI 遵守物理定律
- 北大 & 阿里：统一攻克长视频生成（自回归+扩散+KV Cache）

---

### 1.3 AI椰青 — Motion Retargeting + World Models

**小红书 ID**: `645271980000000014011ef5`
**关注方向**: 人形机器人运动重定向、物理合理性、Latent World Models

---

### 1.4 Ailing Zeng — CVPR 人物运动/重建

**小红书 ID**: `5558254467bc657e50f3d19e`
**分享内容**: CVPR 人物运动重建 (544/444 评分)、LPM 角色一致性

---

### 1.5 清水湾穆勒 — Motion-Agent

**小红书 ID**: `62f36485000000001f007cb5`
**代表性工作**: ICLR 2025 Motion-Agent（LLM驱动的动作生成Agent）

---

### 1.6 卢宗青 — 具身智能 + Motion

**小红书 ID**: `63042525000000000f005664`
**代表性工作**: JALA (CVPR 2026, Joint-Aligned Latent Action) — 用 joint alignment 替代视觉重建做具身预训练

---

### 1.7 AI朋友圈 — Motion Retargeting + Humanoid 高频分享者

**小红书 ID**: `5d8655b3000000000101bda0`
**定位**: 持续分享人形机器人运动重定向、NMR、全身控制等前沿论文
**发帖频率**: 5帖/批 (科研分最高 132, 平均 26.4)

**代表性分享**:
- NMR (CVPR 2026 Highlight?) "零抖动重定向" ×2 帖 — 高度关注该方法
- 人形机器人全身控制相关
- 多个机器人/运动方向帖子

**价值**: 高频、高质量、聚焦 motion retargeting，是追踪该子方向的最佳信号源之一

---

### 1.8 Exoskeleton — 系统化论文搬运

**小红书 ID**: `644b9c0b000000001f030f0c`
**定位**: 系统化搬运顶会人体运动/交互论文，标注 "[文献搬运]"
**发帖频率**: 4帖/批 (科研分 74, 平均 18.5)

**代表性分享**:
- HALO 【文献搬运】— 人-物-场景交互生成
- HuMam 【文献搬运】— 人体动作生成
- 涵盖 HOI、motion generation、interaction 等子方向

**价值**: 论文筛选品味好，覆盖方向与 Modebug 高度重合

---

## 2. 周边值得关注的博主

### 2.1 Motion / Humanoid 方向

| 博主 | 定位 | 代表性内容 |
|------|------|-----------|
| 具身智识局 | 具身智能论文解读 | 西北工大 PhyGile 物理前缀运动跟踪 |
| 正合时宜 | Humanoid 研究者 | 2025 Humanoid 回顾、SONIC 通用人形控制 |
| BeingBeyond | 物理反馈动作生成 | RLPF：物理反馈的人形机器人动作生成框架 |
| 云旗子 | 开源 Motion | "言出法随" 文本驱动机器人动作生成，全套开源 |
| RoboX | NVIDIA Motion | MotionBricks (NVIDIA 2026)、SMASH |
| Guanya | Retargeting | OmniRetarget: 人形机器人重定向新方法 |
| RoboMiner | Retargeting | GMR 一般运动重定向 |
| 低空前沿 | 实时 Text-Driven | 实时交互式文本驱动的人形机器人运动生成 |
| Axellwppr | Motion Tracking 工具 | 基于 mjlab 的通用全身运动追踪框架 |
| 刘东瑞 上海 AI Lab | Motion + World Model | 统一动作生成框架交互式世界模型基准 |
| 包不住的橙子 | PhyGile 分享 | PhyGile 物理先验引导的通用人形动作生成 |

### 2.2 Paper 速递 / 综述

| 博主 | 定位 | 代表性内容 |
|------|------|-----------|
| Exoskeleton | 系统化论文搬运 | HALO、HuMam 等顶会工作 [文献搬运] 系列 |
| 论文速读 | 顶会论文解读 | 斯坦福 GMR 通用运动重定向 |
| 科研残疾人 | ICCV Motion | ICCV2025 文本生成高保真人体动作 |
| PaperReader | 物理引导生成 | 物理引导视频生成新突破 |
| AI智沿前线 | 论文速递 | RealDPO 用真实视频教会AI生成自然动作 |
| Heisenberg | 个人科研分享 | ICRA 录用论文分享 |
| 哈酒烧不开 | 每日论文 | "今天看什么" 系列 |
| L.Transition | CVPR 论文 | CVPR 2025 人物运动/重建方向 |
| 多多的贾维斯 | 扩散动作生成 | arXiv 扩散动作生成解读 |

### 2.3 人形机器人/Embodied

| 博主 | 定位 | 代表性内容 |
|------|------|-----------|
| 机器人解剖师 | 人形控制 | WBC 规划控制学习方法 |
| AYa | 人形部署 | ASAP、PBHC 复现，G1 舞蹈部署框架 |
| 深蓝AI | 全身控制 | 人形机器人全身控制误差降低 15% |
| ♥VLA和RL的具身未来😴 | 具身前沿 | Figure 抛弃 MPC，统一运动操作 |
| 具身智能情报站 | 具身论文速递 | OmniTrack 物理一致重构 |
| 刘缘-HKUST | 3D 人体+视频 | CoMoVi - 图像+文本生成视频与 3D 人体运动 |

### 2.4 视频生成 / 数字人 / 跨域

| 博主 | 定位 | 代表性内容 |
|------|------|-----------|
| AI-Dreamer | 视频生成 | 复杂人物动作视频生成新突破 |
| 智能CV | 数字人 | Meta 首个实时空间感知数字人系统 |
| 朗读并背诵全文 | 世界模型 | MultiWorld 多智能体多视角视频世界模型 |
| AI陆陆 | 运动+AI 跨域 | 运动生物力学+人工智能是被低估的科研方向 |
| Elysia | MoCap | MoCapAnything V2 |
| Python 智能研习社 | 具身智能 | X-Humanoid 具身智能生成式视频编辑 |
| 叫我Alonzo就好了 | 视频生成前沿 | CVPR & ICCV 25 T2V 方向分析 |
| 一只哔mer | 具身智能论文 | EMMA 第一人称移动操作 |
| karminski | 大模型+Motion | 混元-Motion-1.0 |
| 生成纪元 GenEra | 视频生成 | 3D 动态世界、流式交互视频生成 |
| Jaydenrau | Reviewer 视角 | CVPR 2026 Reviewer 吐槽 |

---

## 3. 如何发现更多同类博主

### 3.1 从现有博主的关系网找

郭川在 LIGHT 帖子中 @ 了合作者：
- **Sirui** (UIUC) — 搜索关键词: "LIGHT HOI UIUC"
- **wzy / Ziyin** — 搜索关键词: "Diffusion Forcing LIGHT"

### 3.2 从论文作者追踪

上述帖子的高频作者/机构，可去小红书搜索其姓名：
- SnapMoGen/LIGHT 团队 (Snap Research / UIUC)
- PALUM 团队 (上交 & 港大)
- PhyGile 团队 (西北工大)
- OmniTrack 团队 (华科 & 北通院)
- JALA 团队 (卢宗青组)
- NMR 团队 — AI朋友圈高频分享，retargeting SOTA
- MotionBricks/SMASH 团队 (NVIDIA)
- CoMoVi 团队 (HKUST 刘缘)
- OmniRetarget 团队 (Guanya)

### 3.3 推荐搜索的关键词

```
"CVPR motion generation" "ICLR motion" "动作生成" 
"humanoid 论文" "运动重定向 科研" "text2motion"
"具身智能 动作" "motion capture 科研"
"retargeting 论文" "physics motion" "物理 动作"
"文献搬运"  ← 高信号标签，Exoskeleton 系列
```

### 3.4 从标签反查

高信号标签（出现在科研帖中）:
`ICLR2026` `CVPR26` `动作生成` `MotionGeneration` `EmbodiedAI`
`具身智能` `Humanoid` `DiffusionModel` `3D视觉` `文献搬运`

### 3.5 从社区互动发现

- Exoskeleton 的"文献搬运"系列帖下可能有其他 researcher 互动
- zed (uid: `5b58247711be100c074e376f`) 在小红书提问 motion retargeting 技术细节 — 关注评论区可发现同行
- AI朋友圈的 NMR 帖下推测有 retargeting 方向讨论
- 搜索互动信号: 在科研帖下 comment 的博主大概率也是同行

---

## 4. 与 Modebug 项目的交叉价值

| 博主 | 可追踪内容 | 对 Modebug 的价值 |
|------|-----------|-------------------|
| 郭川不上班 | SnapMoGen 新的 benchmark 结果、HOI failure case | 高质量数据集的 failure mode 分析 |
| 每日CS | 持续的最新顶会论文 | 跟进 SOTA，发现新的比较基线 |
| 清水湾穆勒 | Motion-Agent 后续 LLM+Motion | LLM-based agent 做 motion 的新 failure |
| 卢宗青 | JALA latent action 分析 | latent space failure 对比 |
| AI椰青 | retargeting + physics + humanoid | 物理一致性 failure 维度 |
| AI朋友圈 | NMR + retargeting SOTA | retargeting 精度退化/failure case 追踪 |
| Exoskeleton | HALO, HuMam 等 HOI 论文 | 人-物交互生成的 failure 分析 |
| RoboX | MotionBricks, SMASH | NVIDIA SOTA 方法的 failure profiling |
| BeingBeyond | RLPF 物理反馈 | 物理约束失效模式分析 |
| 包不住的橙子 | PhyGile 物理先验 | 物理引导失败案例 |
| 刘东瑞 上海 AI Lab | 统一动作生成框架 + 世界模型 | 交互式动作生成 failure |
| 低空前沿 | 实时文本驱动 humanoid | 实时场景的 latency/accuracy tradeoff |
| Guanya | OmniRetarget | 跨形态重定向退化分析 |

---

## 5. 爬取技术说明

本次扫描分两轮：

| 轮次 | 方式 | 搜索词 | 结果 |
|------|------|--------|------|
| 第1轮 | QR码登录 | `郭川,humanoid motion,动作生成 科研,运动重定向 论文` | 80条, 55条科研向 |
| 第2轮 | CDP (Chrome DevTools Protocol) | `"humanoid motion" "动作生成 论文" "运动生成 科研"` | 140条 → 去重去噪后 98条科研向 |

**CDP 模式要点** (推荐后续使用):
- 需要 Chrome 保持运行（`--remote-debugging-port=9222`）
- MediaCrawler 配置: `ENABLE_CDP_MODE=True`, `CDP_CONNECT_EXISTING=True`
- 使用真实浏览器指纹，反爬效果好于 cookie/qrcode 模式
- 每次搜索间隔 1-2 分钟，避免触发风控

**后续追踪策略**:
- 每月运行一次 /xhs-search 扫描新帖
- 关注核心博主的最新帖子（手动浏览小批量）
- 出现新的"文献搬运"或高频论文帖时，顺藤摸瓜发现新博主
