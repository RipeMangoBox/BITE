---
title: Multi-material Mesh-based Surface Tracking With Implicit Topology Changes
type: paper
paper_level: A
venue: SIGGRAPH
year: 2024
pdf_ref: paperPDFs/SIGGRAPH_2024/Multi_material_Mesh_based_Surface_Tracking_With_Implicit_Topology_Changes.pdf
project_link: null
code_link: null
aliases:
- MMMBSTITCOA
- MMMBSTITC
tags:
- SIGGRAPH_2024
- topic/graphics_geometry_processing
- topic/graphics_rendering_materials
- topic/graphics_physical_simulation
core_operator: 引入材料向量（material vector）在多材料网格中检测缺陷区域，仅对缺陷区域应用基于稀疏背景网格的隐式拓扑变化（检测、切割、替换），其余部分保留显式网格，从而在鲁棒处理拓扑变化的同时保留表面特征。
primary_logic: 将材料向量推广到多材料非流形表面，结合稀疏背景网格进行射线投射以确定空间材料归属，识别出非物理材料向量的区域，并在该区域局部执行基于网格的隐式拓扑重建，实现了显式网格特征保持与隐式方法鲁棒性、效率的统一。
claims:
- 在100个球体的正常流测试中，我们的方法成功率100%（100/100），平均运行时间6.1分钟；Los Topos成功率85%，平均84.5分钟。
- 在1000个球体的正常流测试中，我们的方法成功率100%（50/50），平均44.6分钟；Los Topos成功率26%（13/50）。
- 在1000个气泡的肥皂膜模拟中，我们的方法平均每时间步36.5秒，相比Los Topos总体快7.5倍，并允许10倍大的时间步长。
- Dr. Krabunkle布尔并集测试中，算法在8分钟内于570^3网格上解析了530万个三角形和72种材料的重叠。
---

# Multi-material Mesh-based Surface Tracking With Implicit Topology Changes

> [!tip] 核心洞察
> 将材料向量推广到多材料非流形表面，结合稀疏背景网格进行射线投射以确定空间材料归属，识别出非物理材料向量的区域，并在该区域局部执行基于网格的隐式拓扑重建，实现了显式网格特征保持与隐式方法鲁棒性、效率的统一。

| 字段 | 内容 |
|------|------|
| 中文题名 | 基于隐式拓扑变化的多材料网格表面跟踪方法 |
| 英文题名 | Multi-material Mesh-based Surface Tracking With Implicit Topology Changes |
| 会议/期刊 | SIGGRAPH 2024 |
| Links | [paper](https://visualcomputing.ist.ac.at/publications/2024/SDTF/) |
| Topic | #topic/graphics_geometry_processing #topic/graphics_rendering_materials #topic/graphics_physical_simulation |
| Method | Multi-material mesh-based surface tracking with implicit topology changes (our algorithm) |
| Dataset | 100-sphere normal flow robustness test, 1000-sphere normal flow robustness test, 1000-bubble soap film simulation, Dr. Krabunkle multi-material boolean union |

> [!tip] 效果简介
> - 100-sphere normal flow robustness test 上，success rate 100% (6.1 min avg) vs 85% (84.5 min avg, Los Topos) (+15% success rate, 13.8x faster)。
> - 1000-sphere normal flow robustness test 上，success rate 100% (50/50) vs 26% (13/50, Los Topos) (+74% success rate)。
> - 1000-bubble soap film simulation 上，speedup over Los Topos 7.5x faster overall vs 1x (Los Topos) (6.5x speedup)。

## 概要

本文针对多材料非流形表面跟踪中拓扑变化处理的鲁棒性与效率难题，提出一种基于显式网格的局部隐式拓扑变化方法。核心思路是引入**材料向量**在多材料网格中检测缺陷区域，仅对缺陷区域应用基于稀疏背景网格的隐式拓扑重建（检测、切割、替换），其余部分保留显式网格，从而在鲁棒处理拓扑变化的同时保持表面特征。

实验表明，该方法在100个球体正常流测试中成功率达100%（Los Topos为85%），平均运行时间6.1分钟（Los Topos为84.5分钟）；在1000个球体测试中成功率100%（Los Topos仅26%）；在1000个气泡的肥皂膜模拟中整体快7.5倍，并允许10倍大的时间步长。方法定位为**Wojtan et al. (2009)** 流形表面跟踪器向多材料非流形设置的泛化，填补了显式网格方法在多材料拓扑变化处理上的空白。

## 核心方法与创新机理

### 问题背景与核心瓶颈

在计算机图形学与物理仿真中，基于网格的表面跟踪方法能精确保持几何特征，但在处理拓扑变化（如自交、合并、分裂）时极易崩溃。现有方法如 **Los Topos**（Da et al., 2014）虽能处理多材料非流形网格，但其基于局部网格操作的策略在面对大规模拓扑事件时鲁棒性差、效率低，且常因退化几何配置而失败。本文识别出的关键瓶颈在于：**局部网格改进步骤占据总运行时间的约80%**，这意味着任何试图全局重采样的方案都将因计算成本过高而不可行。

### 核心创新：材料向量驱动的局部隐式拓扑变化

本文的核心洞察是将显式网格的特征保持能力与隐式方法的拓扑鲁棒性统一在一个局部化框架中。具体而言，方法引入**材料向量（material vector）**作为连接显式网格与隐式背景网格的桥梁，仅在检测到拓扑缺陷的局部区域执行基于稀疏背景网格的隐式重建，其余区域保留原始网格不变。这一“检测-切割-替换”的局部策略实现了三个关键突破：

1. **多材料非流形扩展**：将Wojtan et al.（2009）的流形两材料表面跟踪框架推广到任意多材料非流形表面。
2. **隐式拓扑变化的局部化**：避免全局重采样对表面细节的侵蚀，同时获得隐式方法处理复杂拓扑的鲁棒性。
3. **退化配置的一致性处理**：通过符号扰动（Simulation of Simplicity）确保射线投射在退化定向测试中的确定性。

### 方法框架与模块顺序

算法输入为一个无边界非流形三角网格，每个三角形存储两个材料标签（法向方向和反法向方向各一），输出为拓扑清洁的多材料非流形网格。处理流程由五个顺序模块构成：

#### 模块1：材料分配（Material Assignment）

在稀疏背景网格的每个顶点上，沿三个坐标轴方向进行射线投射。当射线穿过三角形时，根据三角形的材料标签和射线相对法向的朝向更新材料向量：

$$v \leftarrow v - e_a + e_b$$

其中 $v$ 是材料向量（长度等于总材料数），$e_a$ 和 $e_b$ 分别是离开材料 $a$ 和进入材料 $b$ 的单位向量。正确嵌入的区域应具有独热编码的材料向量；若某顶点的三个轴向射线投射结果不一致，或向量包含负分量，则表明该位置存在拓扑缺陷。

#### 模块2：拓扑缺陷检测（Topological Flaw Detection）

基于材料向量和网格-网格相交检测，识别三类复杂基元（complex primitives）：
- **复杂边**：网格边与三角形发生几何相交的网格边。
- **复杂面**：三角形与网格面的交点数量偏离2的网格面（图8）。
- **复杂体**：包含非物理材料向量的网格单元。

缺陷区域通过迭代扩张确定：从包含非物理材料向量的单元出发，不断将相邻单元加入缺陷区域，直到缺陷边界上不再存在复杂边或复杂面。这一扩张过程确保切割边界位于几何和拓扑上“干净”的位置。

#### 模块3：网格切割（Mesh Cutting）

沿缺陷区域边界裁剪原始网格三角形。关键创新在于采用受Pavić et al.（2010）启发的**约束Delaunay三角剖分**，而非Wojtan et al.（2009）的普通三角剖分。后者会在切割边界产生T-接合和零面积三角形（图11），而约束Delaunay三角剖分通过强制边界边存在于剖分中，避免了这些退化元素，保证了后续网格改进的稳定性。

#### 模块4：网格替换（Mesh Replacement）

在缺陷区域内，首先修正非物理材料向量：对每个非物理网格顶点，使用快速行进法找到最近的“断裂点”（breaking point，即物理材料向量与缺陷区域边界上的采样点），将其材料向量覆盖为断裂点的独热编码。随后，基于修正后的材料向量在缺陷区域内生成新三角形，规则是每个新三角形恰有一条边完全位于单个网格面内（图12）。新三角形的材料标签从网格顶点标签或裁剪三角形标签推断。

#### 模块5：网格改进（Mesh Improvement）

通过顶点分离、边分割、边翻转、边折叠和顶点平滑等操作优化局部三角形质量。该模块是当前的计算瓶颈，占据约80%的总运行时间。

### 三个关键Changed Slots

#### Slot 1：表面类型 — 从两材料流形到多材料非流形

**基线**（Wojtan et al., 2009）：仅支持两材料流形表面，通过射线投射判断内部/外部。
**本文**：引入材料向量，将“内部/外部”二元判断推广为多材料空间归属的向量表示。每个三角形存储两个材料标签，支持非流形连接处的多材料交界。

#### Slot 2：拓扑缺陷检测 — 从单材料内外测试到多材料向量一致性检验

**基线**：基于射线投射的单材料内部/外部测试，检测网格与隐式表面不一致的“深单元”。
**本文**：通过比较三个轴向射线投射的材料向量一致性来检测缺陷顶点；通过网格-网格几何相交检测复杂边和复杂面。缺陷区域的扩张策略保证了切割边界的光滑性。

#### Slot 3：网格替换中的三角剖分 — 从普通剖分到约束Delaunay剖分

**基线**：Wojtan et al.的普通三角剖分可能产生T-接合和零面积三角形。
**本文**：采用约束Delaunay三角剖分，强制切割边界边存在于剖分中，避免退化元素，提升后续网格改进的起点质量。

### 鲁棒性保障机制

为处理退化几何配置（如射线恰好穿过顶点或边），方法采用**符号扰动**（Edelsbrunner and Mücke, 1990），通过对顶点坐标施加无穷小扰动来一致地解决退化定向测试，确保射线投射的确定性。这一机制是方法在1000球体正常流测试中达到100%成功率的关键因素之一。

### 模块间因果关系

材料分配模块产生的材料向量是缺陷检测的输入；缺陷检测确定的缺陷区域决定了切割模块的作用范围；切割模块的三角剖分质量直接影响替换模块的边界连接性；替换模块生成的新网格质量则决定了网格改进模块的工作量——这正是瓶颈所在。五个模块形成严格的因果链，任何一环的失败都会导致最终输出的拓扑错误。

![[assets/figures/papers/paper_list_l23_https_visualcomputing_ist_ac_at_publications_2024_SDTF/figures/003_Figure_2.jpg]]
*Figure 2: Our algorithm takes an input mesh with topological flaws (e.g. self-intersections, overlaps, and inside-out regions) and outputs a new mesh that is topologically clean based on its sampling on a background grid*

## 实验与关键发现

### 鲁棒性压力测试：大规模拓扑事件下的成功率与效率

本方法的核心实验证据来自一系列极端拓扑变化场景下的鲁棒性对比。在**100个球体的法向流测试**中，所有球体以恒定速度沿法向膨胀、碰撞并合并，产生密集的拓扑事件。本文方法在100次测试中**成功率达100%（100/100）**，平均运行时间仅6.1分钟；而当前最先进的多材料网格表面跟踪方法**Los Topos**（Da et al., 2014）成功率为85%（85/100），平均运行时间高达84.5分钟。这意味着本文方法在成功率上提升15个百分点的同时，速度提升了约**13.8倍**。

当测试规模进一步扩大到**1000个球体**时，差距更加显著：本文方法在50次测试中**全部成功（50/50，100%）**，而Los Topos仅成功13次（26%）。这一结果直接验证了核心主张——隐式拓扑变化机制在多材料、大变形场景下具有根本性的鲁棒性优势。Los Topos的失败主要源于其显式拓扑操作在面对大量自交和重叠时无法可靠地解析所有退化配置。

### 肥皂膜模拟：时间步长与整体效率的突破

在**1000个气泡的肥皂膜模拟**中，本文方法展现出对物理仿真流程的适配优势。平均每时间步运行时间为36.5秒，相比Los Topos**整体快7.5倍**。更关键的是，本文方法允许**10倍大的时间步长**——这是因为隐式拓扑变化机制不要求网格在每步保持无自交状态，从而解除了对时间步长的严格约束。Los Topos需要较小步长来限制单步变形量，避免拓扑操作失败。这一特性使得本文方法能够处理此前无法企及的仿真规模（图21）。

### 极端布尔并集：多材料重叠的解析能力

**Dr. Krabunkle测试**（图16）将一只细节丰富的螃蟹网格克隆并绕质心旋转5次，生成包含530万个三角形和72种材料的极端重叠场景。本文算法在分辨率为570³的背景网格上，**8分钟内**解析了所有重叠，生成包含360万个三角形的正确多材料非流形表面。这一测试证明了方法处理高材料数、高三角形数、高重叠度复合场景的能力，且输出网格内部材料边界正确分离（图16右剖视图）。

### 消融实验：局部策略与全局重采样的对比

为验证“仅对缺陷区域进行局部重网格”这一设计选择的有效性，本文构造了一个**全局重采样变体（GR）**——将所有网格顶点都替换为基于背景网格重建的顶点。在“滚动石头”测试（图17）中，两个带有表面装饰的球体相互滚入、合并后分离。本文的局部方法**完美保留了原始表面的装饰细节**，而GR变体则明显侵蚀了这些特征（图17a vs 图17b）。这一消融直接证明了局部策略在保持表面特征方面的决定性作用，同时解释了为何全局方法在相同网格分辨率下效果不佳。

### 网格质量消融：约束Delaunay三角剖分

在网格切割步骤中，若采用Wojtan et al.（2009）的普通三角剖分策略，会在裁剪边界产生**T-接合和零面积三角形**等退化元素。本文采用受Pavić et al.（2010）启发的约束Delaunay三角剖分（图11），从机制上避免了这些退化，确保了后续网格改进步骤的输入质量。这一消融虽未单独量化运行时间影响，但在方法链条中是保证输出网格拓扑正确性和几何质量的关键环节。

### 符号扰动消融：退化配置下的射线投射一致性

射线投射在确定网格顶点材料向量时，会频繁遇到射线恰好穿过三角形边或顶点的退化定向测试。本文采用**Simulation of Simplicity**（Edelsbrunner and Mücke, 1990）进行符号扰动，确保这类退化测试的一致性判定。消融证据表明，不采用符号扰动时，同一顶点沿不同坐标轴的射线投射可能得到不同材料向量，导致缺陷区域误判和扩大。这一机制虽不直接体现在整体指标中，但构成了鲁棒性保证的基础。

### 计算瓶颈识别

性能分析揭示了明确的瓶颈：**局部网格改进步骤占据约80%的总运行时间**。该步骤包括顶点分离、边分割、边翻转、边折叠和顶点平滑等操作，旨在优化局部三角形质量。这一发现为后续优化指明了方向——任何针对网格改进的效率提升都将直接转化为整体加速。当前实现中，该步骤的耗时占比限制了方法在低分辨率网格或简单场景下对Los Topos的相对优势。

### 适用边界与失败模式

1. **拓扑保证的分辨率依赖**：输出网格的拓扑正确性依赖于背景网格分辨率L。方法仅保证修复尺寸大于L的自交和拓扑缺陷，无法提供全尺度无自交硬保证。Los Topos则保证最终网格绝对无自交，这是本文方法的一个理论让步。

2. **简单场景下的相对效率**：在变形简单、拓扑事件稀少的场景中，Los Topos可能更快。本文方法的优势在极端拓扑变化下才充分体现，两者适用场景存在互补性。

3. **体积保持**：局部重网格策略引起的体积变化与L及合并/分裂表面积成正比，方法不能精确保持体积。这在需要严格体积守恒的应用中构成限制。

4. **高频细节检测的敏感性**：若不加小心，表面高频细节可能被误检为复杂边并被重采样（图9），导致细节丢失。方法通过特定启发式缓解此问题，但未提供硬性保证。

5. **大规模重叠下的光滑表面生成**：处理极端重叠时，生成光滑非流形表面的启发式方法尚不够直接，需进一步形式化（论文自身指出的开放问题）。

6. **薄片与GPU加速的缺失**：方法尚未扩展到薄片、无网格三角剖分和GPU加速等在流形情况中已证明有效的技术，这些功能的缺失限制了其在特定应用场景中的适用性。

### 公平性说明

论文坦承比较存在若干局限：鲁棒性基准测试可能未均匀采样所有网格配置，参数未针对双方分别优化；Los Topos和本文方法均为研究原型实现，可能存在各自的效率和错误问题；全局重采样和粒子基方法的比较仅作参考，并非公平优化对比。因此，上述数值差异应理解为方法特性的体现，而非绝对性能排名。

![[assets/figures/papers/paper_list_l23_https_visualcomputing_ist_ac_at_publications_2024_SDTF/figures/013_Figure_11.jpg]]
*Figure 11: Comparison of subdivision strategies on the complex boundary. [Wojtan et al. 2009] produces a T-junction with a 0-area triangle; constrained triangulation [Pavić et al. 2010] avoids these degeneracies*

![[assets/figures/papers/paper_list_l23_https_visualcomputing_ist_ac_at_publications_2024_SDTF/figures/025_Figure_22.jpg]]
*Figure 22: Running time for 1000 soap bubbles test. A comparison of per-frame running times for two different surface trackers on the same 1000- soap-bubble animation. Timings exclude the cost of physics calculations (i.e., surface tracker only). × indicates failure of the surface tracker*

![[assets/figures/papers/paper_list_l23_https_visualcomputing_ist_ac_at_publications_2024_SDTF/figures/020_Figure_17.jpg]]
*Figure 17: Rolling stones. Two decorated spheres roll into each other, merge and roll away, tracked by (a) our algorithm, (b) a modified algorithm with global resampling (GR), and (c)–(d) particle-based methods (PR). (a)–(c) use the same grid resolution, while (d) requires a 73 × denser voxel grid*

## 定位与知识库关联

本文的核心贡献在于将显式网格表面跟踪的**拓扑变化处理机制**从两材料流形域推广到多材料非流形域，改变的关键槽位（slot）是**拓扑缺陷检测与修复的作用域**：基线方法 **Wojtan et al.**（2009, SIGGRAPH）仅能处理两材料流形表面，其缺陷检测依赖简单的内部/外部射线投射测试；而本文通过引入**材料向量（material vector）**，将检测逻辑推广为在背景网格顶点上执行多材料射线投射，识别出非物理材料向量（如负分量）的区域，从而将拓扑修复的作用域从二元分类扩展到任意数量材料的非流形配置。

相对于当前最先进的多材料网格表面跟踪器 **Los Topos**（Da et al., 2014, SIGGRAPH），本文改变的第二个关键槽位是**拓扑处理的策略模式**：Los Topos 采用全局碰撞检测和局部拓扑操作（边翻转、面分割等）来逐步修复自交，其成功率和效率在大量拓扑事件下急剧退化（1000球体测试中成功率仅26%）；本文则转而采用**基于稀疏背景网格的局部隐式重采样**策略——仅在检测到的缺陷区域内执行网格切割与替换，其余区域保留原始显式网格。这一策略切换使得拓扑修复的鲁棒性从概率性保证提升为确定性保证（相对于网格分辨率L），同时将运行时间降低了一个数量级（肥皂泡模拟中总体快7.5倍）。

在知识库中的挂载点，本文可定位于**显式网格表面跟踪**与**隐式表面重建**的交叉地带。具体而言：
- **上游挂载**：继承自 Wojtan et al. 的“深度单元”检测思想，以及 **Pavić et al.**（2010）的约束Delaunay三角剖分策略，用于避免网格替换边界处的T-接合和零面积三角形退化。
- **并行参照**：与基于粒子的表面跟踪方法（如VDB重建管线）形成对比——后者在相同网格分辨率下会侵蚀表面细节，需要73倍密度的体素网格才能达到可比质量（Fig. 17），而本文的局部方法完美保留未修复区域的原始表面特征。
- **下游启发**：局部隐式重采样策略为其他需要兼顾特征保持与拓扑鲁棒性的几何处理任务（如布尔运算、流体表面重建）提供了可复用的范式，即“仅在缺陷区域切换表示形式”。Dr. Krabunkle 测试（570³网格上8分钟解析530万三角形、72种材料的重叠）验证了这一范式在极端布尔并集场景下的可扩展性。

**适用边界**需谨慎理解：
1. 输出网格的拓扑正确性**依赖于背景网格分辨率L**：仅保证大于L的自交和缺陷被修复，无法提供全尺度无自交的硬保证（与Los Topos的绝对无自交保证形成权衡）。
2. 局部网格改进步骤占据约80%的总运行时间，构成当前计算瓶颈，限制了实时交互场景的适用性。
3. 局部重网格策略引起的体积变化与L及合并/分裂表面积成正比，不能精确保持体积，在需要严格体积守恒的应用中需额外补偿机制。
4. 方法尚未扩展到薄片（thin sheets）、无网格三角剖分和GPU加速等在两材料流形场景中已验证有效的技术，这些扩展是明确的后续方向。

**后续工作启发**包括：将符号扰动（Simulation of Simplicity）的鲁棒性保证与GPU并行化结合，以消除局部网格改进瓶颈；探索基于材料向量的亚网格缺陷检测，以突破分辨率L的限制；以及将多材料非流形处理能力引入物理模拟管线（如肥皂膜力学），使大规模拓扑变化模拟成为标准工具而非特例。

## 原文 PDF

![[paperPDFs/SIGGRAPH_2024/Multi_material_Mesh_based_Surface_Tracking_With_Implicit_Topology_Changes.pdf]]