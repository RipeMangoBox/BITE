---
title: "MoDebug P0 Baseline Repo Registry v1"
created: 2026-04-23T01:35
updated: 2026-04-26T02:31
status: archived
tags:
  - Motion_Generation
  - MoDebug
  - p0
  - registry
related_exec:
  - '[[paperIDEAs/MoDebug/2026-04-22_modebug-exec-plan-alignment-first|MoDebug Exec]]'
---

# MoDebug P0 Baseline Repo Registry v1

## 目标

把当前机器上已经存在的 motion baseline 仓库，收口成 `linkedCodebases` 下的 canonical registry。

## 本轮已完成

- 已新增 `[[linkedCodebases/ActionPlan-Code]]`
  - real path: `/home/ripemangobox/Coding/Github/Motion/ActionPlan-Code`
  - git commit: `03efc15`
- 已新增 `[[linkedCodebases/ReAlign]]`
  - real path: `/home/ripemangobox/Coding/Github/Motion/ReAlign`
  - git commit: `2b93b3f`
- 已新增 `[[linkedCodebases/FineXtrol]]`
  - real path: `/home/ripemangobox/Coding/Github/Motion/FineXtrol`
  - git commit: `de84bca`
- 已新增 `[[linkedCodebases/FineMotion]]`
  - real path: `/home/ripemangobox/Coding/Github/Motion/FineMotion`
  - git commit: `cc42cab`
- 已新增 `[[linkedCodebases/FineMotion_release]]`
  - real path: `/home/ripemangobox/Coding/Github/Motion/FineMotion_release`
  - git commit: `4464eda`
  - note: 这是 FineMotion 文本标注 release repo，不是 benchmark method repo
- 已新增 `[[linkedCodebases/teach]]`
  - real path: `/home/ripemangobox/Coding/Github/Motion/teach`
  - git commit: `0ba5348`

## 当前 registry 内的主相关仓库

- `[[linkedCodebases/EventT2M-codes-main]]`
  - git commit: `85bb3de`
- `[[linkedCodebases/ActionPlan-Code]]`
  - git commit: `03efc15`
- `[[linkedCodebases/ReAlign]]`
  - git commit: `2b93b3f`
- `[[linkedCodebases/teach]]`
  - git commit: `0ba5348`
- `MLD` host-level baseline
  - host path: `[[linkedCodebases/ReAlign/mld]]`
  - real path: `/home/ripemangobox/Coding/Github/Motion/ReAlign/mld`
  - host repo: `[[linkedCodebases/ReAlign]]`
  - git commit: `2b93b3f`
  - note: 当前只存在 host-level 子树记录，不是独立 standalone canonical repo
- `[[linkedCodebases/motionfix]]`
  - git commit: `62844ff`
- `[[linkedCodebases/motionReFit]]`
  - git commit: `ffe6988`

## 当前 registry 内的辅助 repo

- `[[linkedCodebases/FineMotion]]`
  - benchmark / paper repo
  - git commit: `cc42cab`
- `[[linkedCodebases/FineMotion_release]]`
  - FineMotion 文本标注 release repo
  - git commit: `4464eda`
- `[[linkedCodebases/FineXtrol]]`
  - paper-only related work repo
  - git commit: `de84bca`

## 仍缺失的 canonical repo

- `MLD`
  - standalone canonical repo 仍未发现。
  - 备注：已补 `[[linkedCodebases/ReAlign/mld]]` 的 host-level baseline 记录，但它仍是 `ReAlign` 内部子树。

## 下一步

- 若后续发现独立 `MLD` clone，可把当前 host-level 记录提升为 standalone canonical repo。
- `FineXtrol` repo 保留在 registry 中，但仅作 paper-only 追踪，不再视为项目依赖。
