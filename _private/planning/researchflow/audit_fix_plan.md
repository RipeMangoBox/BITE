# ResearchFlow Audit Fix Plan

> 基于 2026-05-07 架构评审的修改方案
> 评审原文见上文 conversation，Critical + Medium findings 共 10 条

---

## 总体策略

1. **当前实际**: 所有论文走全量分析（shallow → deep → report → materialize），不真实启用 gate 过滤
2. **修改原则**: 只修实现断裂，不改架构设计；不引入新抽象；每改一处有对应验证
3. **验证方式**: 对已有 L4_DEEP 论文重新分析（不参考已有结果），对比新旧报告质量

---

## Phase 1: 立即修复 (目标 1-2 天)

### Fix 1.1 — paper_report 在 verify 之前生成 (C1)

**文件**: `researchflow-backend/backend/services/ingest_workflow.py`

**当前问题**:
`deep_ingest()` 执行顺序: report (line 834) → materialize (line 849) → verify (line 860-870)
paper_report 收到的 `agent_results` 是未验证的原始 dict。

**改动**:
1. 将 paper_report 生成（lines 815-842）移到 materialize（line 849）和 verify（lines 860-870）之后
2. Report context 不再直接 dump `agent_results` dict，改为通过 `ContextPackBuilder.build("paper_report", ...)` 获取（它会使用 `ALL_VERIFIED` 配置只读取 `is_verified=True` 的 blackboard items）
3. 如果 materialize 失败，report 应跳过（记录 warning，不生成 orphan report）

**代码位置**:
```
ingest_workflow.py:
  - Lines 815-842: paper_report agent 调用 → 移到 line 870 之后
  - Line 829: f"{agent_results}" → 替换为 context pack builder 调用
  - Lines 883-908: _persist_paper_report → 保持在原地（materialize 之后）
```

**验证**:
- 在测试中 mock 全部 agents，验证 `AgentBlackboardItem.is_verified` 在 report 生成前已为 True
- 检查 paper_report 的 user_content 不包含失败 agent 的空 `{}`

---

### Fix 1.2 — Node/edge scoring signal 来源修正 (C3)

**文件**: `ingest_workflow.py` + `agent_runner.py`

**当前问题**:
`deep_ingest()` lines 763-790 从 graph_candidate 输出中读取 `evidence_count`、`connected_paper_quality` 等字段，但这些字段不存在于 graph_candidate agent 的 output schema (`agent_runner.py:219-253`)。

**改动方案 (选项 A — 确定性计算，推荐)**:

在 `ingest_workflow.py` deep_ingest() 中，用确定性计算替换 LLM 字段读取:

```python
for node_cand in node_candidates:
    evidence_refs = node_cand.get("evidence_refs", [])
    node_type = node_cand.get("node_type", "")
    node_name = node_cand.get("name", "")

    # 确定性 signal 计算
    evidence_count = min(100, len(evidence_refs) * 20)  # 每条 evidence 贡献 20
    avg_confidence = (
        sum(r.get("confidence", 0.5) for r in evidence_refs) / max(len(evidence_refs), 1)
        if evidence_refs else 0.3
    )
    connected_paper_quality = avg_confidence * 100
    source_diversity = min(100, len(set(
        r.get("section", "") for r in evidence_refs
    )) * 25 + 25)  # 不同 section 来源增加多样性
    structural_importance = {
        "method": 70, "mechanism": 60, "task": 50,
        "dataset": 40, "benchmark": 40, "lineage": 55, "lab": 20,
    }.get(node_type, 40)
    name_stability = min(100, 40 + len(node_name) * 2)  # 名字越长越稳定 (proxy)
    profile_completeness = 30  # 初始值，profile 后再更新

    node_signals = {
        "evidence_count": evidence_count,
        "connected_paper_quality": connected_paper_quality,
        "source_diversity": source_diversity,
        "structural_importance": structural_importance,
        "name_stability": name_stability,
        "profile_completeness": profile_completeness,
    }
```

对 edge 也做类似处理:
```python
for edge_cand in edge_candidates:
    evidence_refs = edge_cand.get("evidence_refs", [])
    relation_type = edge_cand.get("relation_type", "")

    evidence_directness = min(100, len(evidence_refs) * 25 + 25)
    relation_specificity = {
        "modifies_slot": 90, "proposes_method": 85, "extends_method": 80,
        "compares_against": 70, "evaluates_on": 65, "uses_dataset": 60,
        "cites_as_baseline": 55, "belongs_to_task": 50,
        "part_of_lineage": 50, "produced_by_lab": 30,
    }.get(relation_type, 40)
    extractor_agreement = 50  # 单 agent，无 agreement
    source_reliability = avg_confidence * 100
    graph_consistency = 40
    description_quality = min(100, max(20, len(edge_cand.get("one_liner", "")) * 1.5))
    ...
```

**代码位置**:
```
ingest_workflow.py:
  - Lines 763-772: node signal 计算 → 替换为确定性计算
  - Lines 777-790: edge signal 计算 → 替换为确定性计算
```

**验证**:
- 对已知 graph_candidate fixture（手动构造），预期得分可手工计算并断言
- 确保 `method` 类型节点得分 >= 50 基线

---

### Fix 1.3 — Structurality_score 连续化 (C4)

**文件**: `ingest_workflow.py`

**当前问题**:
Line 974: `"structurality_score": 0.7 if method_delta_lite.get("is_structural_change") else 0.3` — 二元硬编码。

**改动**:
替换为基于 deep_analyzer 输出的连续计算:

```python
# 从 deep_analyzer 输出计算结构度
method_full = deep.get("method", {})
method_delta_lite = shallow.get("method_delta", {})
pipeline_modules = method_full.get("pipeline_modules", [])
changed_slots = method_full.get("changed_slots", [])
new_components = method_full.get("new_components", [])

pipeline_total = max(len(pipeline_modules), 1)
new_module_ratio = sum(1 for m in pipeline_modules if m.get("is_new")) / pipeline_total
novel_slot_ratio = (
    sum(1 for s in changed_slots if s.get("is_novel"))
    / max(len(changed_slots), 1)
    if changed_slots else 0
)
is_structural_bool = method_delta_lite.get("is_structural_change", False)

structurality_score = 0.2 + (
    0.30 * new_module_ratio +
    0.25 * novel_slot_ratio +
    0.25 * float(is_structural_bool)
)
structurality_score = min(1.0, structurality_score)
```

**代码位置**:
```
ingest_workflow.py:
  - Line 974: 替换二元赋值
```

**验证**:
- Structural change 论文 → score >= 0.6
- Plugin patch 论文 → score < 0.5
- Pipeline 重写论文 (new_module_ratio > 0.5) → score >= 0.7

---

## Phase 2: 稳定化 (目标 1 周)

### Fix 2.1 — Deep evidence 进入 evidence_units (C2)

**文件**: `ingest_workflow.py` _materialize_to_graph()

**改动**:
在 `analysis_data["evidence_units"]` 构建时，增加来自 deep_analyzer 的 evidence:

```python
deep_evidence = []
# 从 experiment.main_results 提取
for mr in experiment.get("main_results", []):
    for ref in mr.get("evidence_refs", []):
        deep_evidence.append({
            "atom_type": "evidence",
            "claim": f"{mr.get('benchmark')}: {mr.get('proposed_score')} (improvement: {mr.get('improvement')})",
            "confidence": ref.get("confidence", 0.7),
            "basis": "experiment_backed",
            "source_section": ref.get("section", ""),
        })
# 从 ablations 提取
for ab in experiment.get("ablations", []):
    deep_evidence.append({
        "atom_type": "evidence",
        "claim": f"Ablation: remove {ab.get('component_removed')} → {ab.get('effect')} (Δ={ab.get('delta_value')})",
        "confidence": 0.85 if ab.get("supports_core_claim") else 0.6,
        "basis": "experiment_backed",
        "source_section": "experiments",
    })

# 合并 shallow + deep evidence
all_evidence = analysis_data["evidence_units"] + deep_evidence
analysis_data["evidence_units"] = all_evidence
```

---

### Fix 2.2 — deep_ingest 幂等性守卫 (M1)

**文件**: `ingest_workflow.py` deep_ingest()

**改动**:
在 `deep_ingest()` 开头增加:

```python
has_l4 = await self.session.execute(
    select(PaperAnalysis).where(
        PaperAnalysis.paper_id == paper_id,
        PaperAnalysis.level == AnalysisLevel.L4_DEEP,
        PaperAnalysis.is_current.is_(True),
    )
).scalar_one_or_none()

if has_l4:
    return {
        "paper_id": str(paper_id),
        "status": "skipped",
        "reason": "L4_DEEP analysis already exists",
    }
```

---

### Fix 2.3 — Report section 校验 (M2)

**文件**: `ingest_workflow.py` _persist_paper_report()

**改动**:
```python
REQUIRED_SECTIONS = {
    "metadata_overview", "background_motivation", "core_innovation",
    "framework_overview", "module_formulas", "experiment_analysis",
    "lineage_positioning",
}

got_sections = {s.get("section_type", "") for s in sections}
missing = REQUIRED_SECTIONS - got_sections
if missing:
    logger.warning("Paper %s report missing sections: %s", paper_id, missing)
    # 创建 review task 提示人工检查
```

---

### Fix 2.4 — Baseline 信息进 DeltaCard (M3)

**文件**: `ingest_workflow.py` _materialize_to_graph()

**改动**:
从 reference_role_map 提取 anchor_baselines 对应的 paper IDs，填充 DeltaCard 的 baseline_paper_ids。

---

## Phase 3: 架构增强 (后续)

### Fix 3.1 — full_report_md 版本化 (M5)
### Fix 3.2 — auto_publish gate 重校准 (M6)
### Fix 3.3 — 集成/回归测试
### Fix 3.4 — Layer D cross-paper abstraction 启停条件

---

## 实施顺序

```
Day 1: Fix 1.1 + Fix 1.2 + Fix 1.3 → 对已有论文重跑 → 对比旧报告 ✅
Day 2: 根据对比结果调整 → Fix 2.1 + Fix 2.2 + Fix 2.3 + Fix 2.4 ✅
Week 1: Fix 2.4 + 集成测试 + batch 验证
```

## 不做的事

- 不大重构 agent_runner.py（prompt 本身设计合理，问题在编排层）
- 不改 DeltaCard 不可变模型
- 不在 export 层引入新的知识推断逻辑（保持纯 materialization）
- 不引入新的 service 抽象层（当前 3 层够用）
- 不删除 quality_service.py（代码虽未被积极调用但结构正确，Phase 3 会启用）
