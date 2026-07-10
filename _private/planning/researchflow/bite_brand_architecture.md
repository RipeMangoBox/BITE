---
created: 2026-05-22
updated: 2026-05-22
scope: private
status: accepted
---

# BITE Brand Architecture

## Accepted Naming

`BITE` = **Bibliographic Intelligence for Thought Emergence**

BITE 是 ResearchFlow / PaperBite 后续产品叙事的上层框架：它不只表示“把单篇论文压缩成 bite-sized note”，更强调基于可追溯文献证据，辅助科研想法从证据中生长出来。

## Product Layers

| Layer | Name | Role |
|---|---|---|
| Evidence layer | PaperBite | bite-sized paper evidence archive |
| Ideation agent layer | IdeaSpark | evidence-driven idea emergence |
| Knowledge map layer | Mosaic Atlas | multi-domain knowledge map |

## Current Positioning

当前的 `obsidian-vault/` 更接近 **PaperBite**，原因是知识体量、跨方向覆盖和关系图密度还没有达到完整 BITE 系统的规模。

因此当前阶段不应过度宣称已经完成 `IdeaSpark` 或 `Mosaic Atlas`。更准确的定位是：

- **PaperBite** 负责论文知识和证据沉淀。
- **PaperBite** 输出 bite-sized、结构化、可检索、可审计的论文笔记。
- **PaperBite** 保持 source anchors、frontmatter、PDF 引用和分析日志，确保下游 agent 可以追溯证据。
- **IdeaSpark** 是后续基于用户意图和 PaperBite 证据层运行的分析 / idea 构思 agent。
- **Mosaic Atlas** 是后续基于 PaperBite 证据层生成的知识地图、方向地图和领域视图，不是当前 vault 的基础职责。

## Boundary Decision

PaperBite 只管知识与证据沉淀，不把“智能涌现”硬塞进基础笔记层。

更合理的职责拆分是：

```text
PaperBite
  -> stores paper-level evidence
  -> normalizes notes, metadata, links, and source anchors
  -> keeps the knowledge base queryable and auditable

IdeaSpark
  -> reads PaperBite through user intent
  -> builds evidence-backed hypotheses, ideas, and research directions
  -> records why an idea is supported, weak, risky, or worth testing

Mosaic Atlas
  -> reads PaperBite and IdeaSpark outputs
  -> builds larger-scale topic maps, evidence maps, and direction maps
  -> helps users navigate many papers and many research questions
```

## Narrative Guardrails

- 对外讲 PaperBite 时，重点放在“单篇论文精华浓缩 + 可追溯证据沉淀”。
- 对外讲 BITE 时，重点放在“bibliographic intelligence” 和 “thought emergence”，即从文献证据到科研构思的完整链条。
- 不把当前 `obsidian-vault/` 说成已经具备完整 multi-domain knowledge map 能力。
- 不把 idea emergence 说成静态笔记自然产生的结果；它应由基于用户意图的 downstream agents 完成。
- 后续 agent 的质量依赖 PaperBite 的证据质量、覆盖规模、结构字段和 source anchors。

