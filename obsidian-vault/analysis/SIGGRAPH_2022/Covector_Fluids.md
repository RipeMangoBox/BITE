---
title: Covector Fluids
type: paper
paper_level: A
venue: SIGGRAPH
year: 2022
pdf_ref: paperPDFs/SIGGRAPH_2022/Covector_Fluids.pdf
project_link: "https://cseweb.ucsd.edu//~viscomp/projects/SIG22CovectorFluids/"
code_link: null
aliases:
- CFCCM
- CF
tags:
- SIGGRAPH_2022
- topic/other_unclear
core_operator: 将速度场视为余向量场，采用基于逆流映射转置雅可比矩阵的Lie平流，使平流与投影对易，从而在速度层级上隐式求解涡度方程。
primary_logic: 利用余向量Lie平流替代传统物质导数，确保沿流动曲线的环量守恒（Kelvin环流定理），在标准平流-投影框架内实现涡度保持，避免全局积分开销。
claims:
- 所提方法的核心修改是将速度平流更新从 u(x)←u(Ψ(x)) 改为 u(x)←(dΨ)⊺u(Ψ(x))
- 该修改等价于速度余向量场的Lie平流，可证明隐式求解了涡度方程
- 实验表明，相比其他方法，CF在多种场景下产生更多涡旋结构并更好地保持能量
- CF方法的临界CFL数达6.18，优于IVOCK(1.45)和SCPF(4.85)
---

# Covector Fluids

> [!tip] 核心洞察
> 利用余向量Lie平流替代传统物质导数，确保沿流动曲线的环量守恒（Kelvin环流定理），在标准平流-投影框架内实现涡度保持，避免全局积分开销。

| 字段 | 内容 |
|------|------|
| 中文题名 | 余向量流体 |
| 英文题名 | Covector Fluids |
| 会议/期刊 | SIGGRAPH 2022 |
| Links | [paper](https://cseweb.ucsd.edu//~viscomp/projects/SIG22CovectorFluids/) · [Project](https://cseweb.ucsd.edu//~viscomp/projects/SIG22CovectorFluids/") |
| Topic | #topic/other_unclear |
| Method | Covector Fluids (CF) / CF+MCM |
| Dataset | Leapfrogging test, Overall simulation workload |

> [!tip] 效果简介
> - Leapfrogging test (3D) 上，Critical CFL number 6.18 vs IVOCK: 1.45, SCPF: 4.85 (+327% vs IVOCK, +27% vs SCPF)。
> - Overall simulation workload 上，Time per step increase +15% vs Baseline advection-projection methods (15%)。

## 概要

传统流体模拟中，速度平流-投影方法因分裂误差将旋转分量转化为散度分量，造成严重的涡度耗散；而以涡度为中心的方法虽能保持涡度，却需昂贵的速度重建步骤。本文提出**余向量流体（Covector Fluids, CF）**方法，通过一项简洁的修改解决此困境：将速度平流更新从标准的分量式映射 $u(x) \leftarrow u(\Psi(x))$ 替换为余向量Lie平流 $u(x) \leftarrow (d\Psi(x))^\top u(\Psi(x))$，即使用逆流映射的转置雅可比矩阵。这一修改使平流与投影算子对易，在标准速度层级上隐式求解涡度方程，从而在保持涡度的同时避免全局积分开销，仅增加约15%的计算时间。实验表明，CF方法的临界CFL数达到6.18，显著优于IVOCK（1.45）和SCPF（4.85）；在多种场景下，CF能产生更丰富的涡旋结构，且能量保持能力与能量保持方法（如MC+R）相当。方法可轻松集成到主流半拉格朗日求解器及特征映射框架中。

## 核心方法与创新机理

### 问题瓶颈：分裂误差导致的涡度耗散

传统不可压缩欧拉方程求解器（如 **Stable Fluids**，Stam, SIGGRAPH 1999）采用算子分裂策略，将时间步分解为平流和投影两个独立步骤。在平流阶段，速度场按分量独立平流：

$$ \mathbf{u}(\mathbf{x}) \gets \mathbf{u}(\Psi(\mathbf{x})), \quad \mathbf{x} \in M $$

其中 $\Psi$ 是逆流映射。问题在于，这种分量式平流将速度视为标量场集合，破坏了速度场的几何结构——平流与投影不可对易，导致旋转分量被错误地转化为散度分量，在投影步骤中被当作无旋分量消除。这正是传统方法中数值涡度耗散的根本原因。

涡度方法（如 **SCPF**，Elcott et al., ACM Trans. Graph. 2007）通过直接求解涡度方程来规避此问题，但需要昂贵的速度重建步骤（求解泊松方程），且难以处理边界条件。**IVOCK**（Zhang et al., ACM Trans. Graph. 2015）试图在平流-投影框架内恢复缺失涡度，但本质上是对症状的补救而非对病因的根除。

### 核心洞察：余向量Lie平流与环量守恒

本文的核心洞察源于对Kelvin环流定理的重新审视：在无黏不可压缩流体中，沿任意随流体运动的闭合曲线的环量 $\oint_C \mathbf{u} \cdot d\mathbf{l}$ 守恒。分量式平流破坏环量守恒，因为它将速度视为向量场（contravariant object）而非余向量场（covariant object）。

将速度场 $\mathbf{u}$ 重新解释为余向量场 $\mathbf{u}^{\flat}$ 后，其正确的输运方程应由Lie材料导数描述：

$$ \left( \frac{\partial}{\partial t} + \mathcal{L}_{\mathbf{v}} \right) \xi_t = 0 \quad \Leftrightarrow \quad \xi_t = \Psi_t^* \xi_0 $$

其中 $\mathcal{L}_{\mathbf{v}}$ 是沿速度场 $\mathbf{v}$ 的Lie导数，$\Psi_t^*$ 是逆流映射的拉回（pullback）。余向量Lie导数的向量计算形式为：

$$ ( \mathcal{L}_{\mathbf{v}} \mathbf{a}^{\flat} )^{\sharp} = \mathbf{v} \cdot \nabla \mathbf{a} + (\nabla \mathbf{v}) \cdot \mathbf{a} $$

与传统物质导数 $\frac{D\mathbf{u}}{Dt} = \frac{\partial \mathbf{u}}{\partial t} + \mathbf{v} \cdot \nabla \mathbf{u}$ 相比，Lie导数多出了 $(\nabla \mathbf{v}) \cdot \mathbf{a}$ 项——这正是涡度拉伸项的来源。这一项确保平流过程自动保持环量守恒，从而隐式求解涡度方程。

### 唯一Changed Slot：平流更新规则

本文的方法修改极其精简——仅改变一个核心操作，即可将标准平流-投影求解器转化为余向量流体求解器：

| 组件 | 基线值 | 提出值 |
|------|--------|--------|
| 平流更新规则 | 分量式平流：$\mathbf{u}(\mathbf{x}) \gets \mathbf{u}(\Psi(\mathbf{x}))$ | 余向量Lie平流：$\mathbf{u}(\mathbf{x}) \gets (d\Psi(\mathbf{x}))^{\intercal} \mathbf{u}(\Psi(\mathbf{x}))$ |

其中 $d\Psi(\mathbf{x})$ 是逆流映射 $\Psi$ 在点 $\mathbf{x}$ 处的雅可比矩阵。这一修改的物理意义是：速度向量不仅跟随流线移动，还需根据流线的拉伸和旋转进行相应的变换。具体而言，转置雅可比 $(d\Psi)^{\intercal}$ 作用于速度向量，确保沿任意曲线的线积分在拉回下保持不变：

$$ \int_C (d\Psi(\mathbf{x}))^{\top} \mathbf{u}(\Psi(\mathbf{x})) \cdot d\mathbf{l} = \int_{\Psi(C)} \mathbf{u} \cdot d\mathbf{l} $$

该恒等式直接保证了环量守恒（Kelvin定理的离散对应），从而在速度层级上隐式求解了涡度方程：

$$ \frac{\partial}{\partial t} \mathbf{w} + \mathbf{v} \cdot \nabla \mathbf{w} - \mathbf{w} \cdot \nabla \mathbf{v} = \mathbf{0} $$

### 方法管线：模块顺序与因果链

CF方法的完整管线包含以下模块，按时间步顺序执行：

**步骤1：流动速度冻结（Flow Velocity Freezing）**
将当前速度场 $\mathbf{u}$ 复制为流动速度 $\mathbf{v} \gets \mathbf{u}$，用于构造逆流映射。此冻结假设在单时间步内成立，其截断误差可通过高阶时间积分（如中点法，2阶Runge–Kutta）降低。

**步骤2：余向量平流（Covector Advection）**
这是核心修改所在。对每个网格点 $\mathbf{x}$，沿冻结速度场 $\mathbf{v}$ 反向追踪至 $\Psi(\mathbf{x})$，计算该点的速度值 $\mathbf{u}(\Psi(\mathbf{x}))$，再乘以逆流映射的转置雅可比 $(d\Psi(\mathbf{x}))^{\intercal}$。雅可比矩阵通过追踪过程中相邻粒子的偏移量差分计算。

因果链：冻结速度场 $\mathbf{v}$ → 构造逆流映射 $\Psi$ → 计算转置雅可比 $d\Psi^{\intercal}$ → 变换速度向量 → 环量自动守恒 → 涡度方程隐式满足。

**步骤3：压力投影（Pressure Projection）**
施加不可压缩约束 $\nabla \cdot \mathbf{u} = 0$，与标准方法相同。关键优势在于：由于余向量平流已将旋转分量正确保持，投影步骤不再错误消除涡度。

**步骤4（可选）：BFECC无耗散Lie平流**
标准的半拉格朗日余向量平流存在显著的插值耗散。本文引入基于BFECC（Back-and-Forth Error Compensation and Correction）的二阶Lie平流方案（Algorithm 4）：通过正向-反向-补偿三轮追踪，抵消低阶截断误差的主导项，实现近似无耗散的余向量输运。实验表明，取消BFECC后能量损失显著增加（Fig. 8），证实了无耗散平流对能量保持的关键性。

**步骤5（可选）：特征映射方法CF+MCM**
为进一步减少插值带来的数值耗散，CF+MCM将余向量平流与**BiMocq**（Qu et al., ACM Trans. Graph. 2019）的双向特征映射方案结合（Algorithm 5）。通过拉格朗日标记的pullback操作，将速度场的拉回计算从欧拉网格插值转化为沿特征线的积分，保留了更多空间细节。此变体在定性比较中展现出更丰富的涡旋结构（Fig. 2, Fig. 11）。

![[assets/figures/papers/paper_list_l12_https_cseweb_ucsd_edu_viscomp_projects_SIG22CovectorFluids/figures/003_Figure_2.jpg]]
*Figure 2: A bunny meteor falling. Smoke is generated from the surface of a bunny obstacle against a laminar flow with no other external force. Our method is capable of shedding many more vortices from the surface of the obstacle. This results in a more detailed and heavier smoke cloud trailing the bunny*

### 与传统涡度方法的等价性与优势

从涡度方程角度看，余向量平流-投影与涡度方法具有等价性：两者都保证涡度方程的精确满足。但CF方法的关键优势在于**避免了速度-涡度变量转换**——所有计算均在速度变量上完成，无需全局积分（求解泊松方程）来从涡度重建速度。这使得CF的计算开销仅比标准平流-投影方法增加约15%（Table 2），远低于涡度方法的额外成本。

![[assets/figures/papers/paper_list_l12_https_cseweb_ucsd_edu_viscomp_projects_SIG22CovectorFluids/figures/013_Table_2.jpg]]
*Table 2: Performance and statistics*

图6形象地说明了这一关系：涡度方法以昂贵的速度重建为代价换取涡度保持，而CF方法以与传统平流方法相当的成本“模拟”了涡度方法的效果。

![[assets/figures/papers/paper_list_l12_https_cseweb_ucsd_edu_viscomp_projects_SIG22CovectorFluids/figures/008_Figure_5.jpg]]
*Figure 5: (a) This covector field, visualized as a level set, is initialized differently inside and outside of the Zalesak’s disk. (b) Component-wise advection of covector fields fails to correctly transport the field, resulting in a wrong orientation of the covector field. (c) The field is correctly transported using a covector advection scheme. Despite correct transportation of the covector field, the field is heavily dissipated due to sampling error. (d) Using BFECC, the field is accurately transported through time. This results in a field which matches the initial orientation while being rotated with the flow*

## 实验与关键发现

Covector Fluids（CF）的核心实验逻辑围绕一个因果链展开：将速度平流更新从标准分量式改为余向量Lie平流，等价于在速度层级上隐式求解涡度方程，从而在标准平流-投影框架内实现涡度保持。实验从涡旋结构生成、能量保持、稳定性边界和计算开销四个维度验证了这一主张。

### 涡旋生成与细节保持

**Von Kármán涡街**（Fig. 4）是贯穿全文的核心定性基准。在相同网格分辨率和时间步长下，CF方法在障碍物附近产生了明显更多的涡旋脱落，且这些涡旋在后续演化中持续形成更丰富的涡结构。相比之下，标准Semi-Lagrangian平流（SF）和BFECC等方法因分裂误差将旋转分量转化为散度分量，涡旋结构迅速耗散。

**Bunny陨石场景**（Fig. 2）进一步验证了这一优势：烟雾从障碍物表面生成并流经层流，CF方法从表面剥离出显著更多的涡旋，形成更厚重、细节更丰富的尾迹烟云。**墨滴下落**（Fig. 11, Fig. 12）和**烟羽上升**（Fig. 14）等场景中，CF方法始终产生更复杂的涡旋结构，且这些结构在长时间演化中得以保持。

**Delta翼**（Fig. 17）提供了与物理实验的定性对照：CF模拟结果与Henri Werlé在ONERA流体可视化实验室的物理实验结果在涡旋形态上高度一致，验证了方法的物理合理性。

### 能量保持能力

**Taylor涡旋演化**（Fig. 8）是能量保持的核心基准。CF方法的能量保持水平与专门的能量保持方法MC+R相当，而标准SF和BFECC方法则出现显著的动能衰减。消融实验表明，取消BFECC后能量损失显著增加，证实了无耗散Lie平流方案对能量保持的关键作用。

**三叶结涡旋**（Fig. 9）提供了更严格的验证：CF方法不仅捕获了物理实验中观察到的涡旋分离现象（Kleckner and Irvine, 2013），而且在涡旋强度保持上优于MC+R和BiMocq等近期方法，能量衰减曲线也更为平缓。

### 稳定性与临界CFL数

**Leapfrogging涡环**（3D）是量化稳定性的关键实验。CF方法的临界CFL数达到**6.18**，相比IVOCK的1.45提升**+327%**，相比SCPF的4.85提升**+27%**。这一差异源于CF方法在速度层级上隐式求解涡度方程，避免了涡度-速度转换引入的额外稳定性约束。2D leapfrogging实验（Fig. 7）进一步表明，采用中点法（2阶Runge–Kutta）降低冻结流动速度的截断误差后，CF方法能更好地捕捉涡环跃迁现象。

### 计算开销

Table 2显示，CF方法相比基线平流-投影方法仅增加约**15%**的每步计算时间。这一开销主要来自转置雅可比的计算和BFECC的额外子步，但考虑到涡度保持带来的质量提升，该开销是可接受的。CF+MCM变体通过拉格朗日标记的pullback减少插值，进一步提升了细节保持能力，但引入了额外的特征映射计算开销。

### 消融实验的关键发现

1. **余向量平流 vs 分量式平流**（Fig. 5）：在Zalesak圆盘旋转测试中，分量式平流导致余向量场朝向错误，而余向量Lie平流正确保持了场的朝向。但单纯的余向量平流存在显著的插值耗散，需要BFECC进行无耗散修正。

2. **BFECC的必要性**（Fig. 5d, Fig. 8）：BFECC将余向量平流提升为二阶无耗散方案，使旋转后的场既保持初始朝向又避免数值扩散。取消BFECC后，能量损失显著增加。

![[assets/figures/papers/paper_list_l12_https_cseweb_ucsd_edu_viscomp_projects_SIG22CovectorFluids/figures/014_Figure_8.jpg]]
*Figure 8: Evolution of Taylor vortices simulated with different methods. Using our method, energy is conserved as well as energy preserving methods such as MC+R. Note that error correction schemes, such as BFECC/MC, are crucial to energy preservation*

3. **中点法 vs 一阶冻结**（Fig. 7）：采用2阶Runge–Kutta中点法估计流动速度，可降低冻结速度引入的截断误差，对跃迁现象等瞬态过程的捕捉有显著改善。

![[assets/figures/papers/paper_list_l12_https_cseweb_ucsd_edu_viscomp_projects_SIG22CovectorFluids/figures/010_Figure_7.jpg]]
*Figure 7: 2D leapfrogging demonstrated with our method in its 1st and 2nd order variants. By lowering diffusion with the 2nd order covector advection scheme, the leapfrogging phenomenon is better captured*

4. **CF+MCM的附加收益**：通过拉格朗日标记的pullback，CF+MCM在墨滴下落（Fig. 11）等场景中保留了更多空间细节，验证了减少插值对细节保持的贡献。

### 适用边界与失败模式

**经验稳定性判据**：方法缺乏解析的稳定性准则，临界CFL数依赖于经验确定，不同场景可能需要手动调整。

**固流交互与边界层**：论文的固流耦合处理较为简单，未涉及精确的边界层建模。对于需要高精度壁面剪切应力预测的工程空气动力学应用，CF方法可能不足以替代专门的涡度-速度方法。

**高雷诺数定量预测**：虽然Fig. 15显示CF+MCM在von Kármán涡街中与MC+R的“ground truth”结果一致，但该验证仅覆盖了定性对称破缺现象，未涉及湍流统计量的定量比较。CF方法在高雷诺数湍流的定量预测能力仍待验证。

**数值耗散残余**：即使采用BFECC，CF方法仍存在一定程度的数值耗散（Fig. 5c vs Fig. 5d），在极长时间演化或极高涡度梯度场景中，涡旋强度仍会逐渐衰减。

![[assets/figures/papers/paper_list_l12_https_cseweb_ucsd_edu_viscomp_projects_SIG22CovectorFluids/figures/005_Figure_4.jpg]]
*Figure 4: Von Kármán vortex street simulated for different methods. Our method results in increasingly more vortex nucleation close to the obstacle compared to other methods (see Table 1 for method acronyms). The additional vortex nucleation allows our method to achieve more vortical structures throughout the simulation (see video 4:41)*

## 定位与知识库关联

**方法定位：在标准平流-投影框架内用“速度平流更新规则”一个 slot 的改变，隐式实现涡度方程求解。**

传统基于速度的流体模拟（如 **Stable Fluids** (Stam, SIGGRAPH 1999)）采用分量式平流更新 $\mathbf{u}(\mathbf{x}) \gets \mathbf{u}(\Psi(\mathbf{x}))$，其核心瓶颈在于：平流-投影算子分裂将速度的旋转分量部分错误地转化为散度分量，导致涡度数值耗散。涡度方法（如 **SCPF** (Elcott et al., ACM Trans. Graph. 2007)）通过直接求解涡度方程来保持涡度，但需要在每个时间步进行昂贵的速度重建（从涡度恢复速度场），计算开销显著。IVOCK (Zhang et al., ACM Trans. Graph. 2015) 试图在平流-投影框架内恢复缺失涡度，但采用经验性修正策略，缺乏严格的几何守恒保证。

Covector Fluids 的核心改变仅在于**平流更新规则这一个 slot**：将分量式平流替换为余向量 Lie 平流 $\mathbf{u}(\mathbf{x}) \gets (d\Psi(\mathbf{x}))^{\intercal} \mathbf{u}(\Psi(\mathbf{x}))$。这一修改的深层意义在于，它将速度场重新解释为余向量场（covector field），利用逆流映射的转置雅可比实现 Lie 拉回（pullback），从而保证沿任意随流闭合曲线的环量守恒（Kelvin 环流定理）。论文在 Section 4.4 中证明，该平流规则等价于隐式求解涡度方程 $\frac{\partial}{\partial t} \mathbf{w} + \mathbf{v} \cdot \nabla \mathbf{w} - \mathbf{w} \cdot \nabla \mathbf{v} = \mathbf{0}$ (Eq. 31)，从而在速度变量层级上直接获得涡度保持能力，无需显式转换到涡度变量。

**知识库挂载点：微分几何中的余向量输运与 Lie 导数理论。**

该方法的知识库根基在于微分几何中对张量场输运的区分：向量场与余向量场在流映射下的推前/拉回行为不同。论文将速度场 $\mathbf{u}$ 通过音乐同构 $\flat$ 映射为余向量场 $\mathbf{u}^{\flat}$，其 Lie 导数为 $(\mathcal{L}_{\mathbf{v}} \mathbf{a}^{\flat})^{\sharp} = \mathbf{v} \cdot \nabla \mathbf{a} + (\nabla \mathbf{v}) \cdot \mathbf{a}$ (Eq. 14)。这一形式与向量场的 Lie 导数 $[\mathbf{v}, \mathbf{a}]$ 不同，导致余向量场在流映射下的输运具有环量守恒性质。该理论连接将流体模拟的数值耗散问题归结为“平流更新规则未匹配速度场的正确几何身份”，为后续研究提供了明确的几何修正方向。

**适用边界与局限。**

CF 方法的稳定性依赖经验 CFL 数（临界 CFL 数约 6.18），缺乏解析稳定性判据，这限制了其在极端参数下的可靠性预测。论文未涉及高精度空气动力学模拟，对固流交互和边界层建模的处理较简单（如 bunny meteor 场景仅采用基本边界条件），可能不适用于需要精确壁面剪切应力预测的工程应用。此外，CF 方法在低分辨率或大时间步长下，余向量 Lie 平流的转置雅可比计算可能引入额外误差，需要 BFECC 或 MCM 等补偿方案来维持精度。

**对后续工作的启发。**

CF 方法证明了在标准平流-投影框架内，仅通过修改平流更新规则即可实现涡度保持，这为流体模拟的几何结构保持（structure-preserving）离散化提供了新范式。后续工作可沿以下方向展开：(1) 建立余向量流体的解析稳定性判据，将经验 CFL 条件理论化；(2) 将 CF 方法与高阶边界层模型结合，扩展至高雷诺数壁面湍流的定量预测；(3) 探索余向量 Lie 平流与其他几何守恒律（如能量、螺旋度）的联合离散化方案；(4) 将 CF 的几何视角推广至可压缩流或磁流体等更复杂的物理系统，利用微分几何的统一语言设计保持相应守恒律的数值格式。

## 原文 PDF

![[paperPDFs/SIGGRAPH_2022/Covector_Fluids.pdf]]