---
title: "MoDebug P1 1-3 Event MVP Generation Protocol"
created: 2026-05-21T00:00:00+08:00
updated: 2026-05-21T00:00:00+08:00
type: experiment_protocol
tags:
  - MoDebug
  - P1
  - diagnostic
  - generation_mvp
---

# MoDebug P1 1-3 Event MVP Generation Protocol

## Scope

This MVP tests whether a minimal 1-3 event prompt set is useful for connecting:

- text-side full-vs-single event embedding;
- generator-side text condition propagation where available;
- generated motion visual inspection.

It does not establish final instruction-following strength or weakness.

## Inputs

- sample_count: `6`
- event_count: `12`
- generation_prompt_count: `18`
- length budget: `196` frames for cross-model alignment

## Required Metadata

Every result record must include:

- date
- artifact_path
- evaluator
- protocol
- motion_source
- condition_pair
- n/evaluable
- coverage
- role
- used_for
- limitations

## Interpretation Boundary

Generated motion and embedding evidence here can only support `diagnostic` or `cross_check` statements. It cannot be used as a held-out final evaluator, and it cannot by itself label a model or sample as high/weak instruction following.
