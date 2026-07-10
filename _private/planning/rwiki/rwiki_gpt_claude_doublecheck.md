---
created: 2026-04-12
scope: private
purpose: GPT ↔ Claude 双模型互查协议
---

# ResearchWiki 双模型互查协议

> 两个模型各自处理一个 awesome 仓库的 collect + enrich，完成后交叉审查对方产出。
> 目标：通过互查发现 parse 遗漏、字段错误、补全失误，提升数据质量。

---

## 一、分工约定

| 角色 | 模型 | 运行环境 | 负责 source |
| --- | --- | --- | --- |
| Model A | Claude | Cursor 对话窗口 / Claude Code CLI | `awe_human_motion`（pilot） |
| Model B | GPT | Cursor Codex 插件 / Codex CLI | `awe_llm_reasoning`（规模小，验证流程） |

> 实际分配可灵活调整，上表仅为示例。

---

## 二、产出目录

各自只写自己的 `sources/<source_id>/`，不碰对方文件：

```text
ResearchWiki/sources/
├── awe_human_motion/          ← Model A 产出
│   ├── source_items.csv
│   ├── review_queue.csv
│   ├── meta.yaml
│   └── snapshots/
├── awe_llm_reasoning/         ← Model B 产出
│   ├── source_items.csv
│   ├── review_queue.csv
│   ├── meta.yaml
│   └── snapshots/
└── ...
```

---

## 三、互查 Prompt

一方完成 collect + enrich 后，将以下 prompt 交给另一方执行：

```
## 任务：审查另一个 agent 产出的 ResearchWiki source 数据

你是 <填入 Model A 或 Model B>，正在审查 <填入对方模型名> 的产出。

### 输入
- 审查目标：`ResearchWiki/sources/<source_id>/`
- 参考规范：`_private/planning/rwiki/rwiki_batch_task_spec.md`
- 原始 README 快照：`sources/<source_id>/snapshots/` 下最新的 .md 文件

### 审查清单

1. **字段合规**：`source_items.csv` 字段是否符合 spec（item_id, paper_title, venue, year, paper_link, code_link, project_link, source_section, has_code, parse_status, 补全_status）？有无缺列、多列、字段名拼写不一致？

2. **覆盖率**：对比 README 快照，是否有明显遗漏（README 中有但 csv 中没有的论文）？抽查至少 3 个 README section，统计覆盖率。

3. **paper_link 有效性**：随机抽查 20 条 `parse_status=ok` 的记录，验证 paper_link 是否可访问、是否指向正确论文（标题匹配）。

4. **enrich 质量**：对 `补全_status=done` 的条目，抽查 10 条，验证补全的 paper_link/venue/year 是否正确。

5. **状态标记一致性**：`parse_status` 和 `补全_status` 的取值是否符合 spec 定义？是否存在矛盾（如 parse_status=ok 但 paper_link 为空）？

6. **meta.yaml 完整性**：断点续跑信息是否完整？统计数字是否与 csv 行数一致？

### 输出
审查报告写入：`sources/<source_id>/review_report_by_<你的模型名>.md`

报告格式：
- 总体评价（一句话）
- 各项检查结果（pass / fail + 具体问题）
- 需要修复的条目列表（如有）
- 建议
```

---

## 四、互查流程

```text
Phase 1: 各自执行
  Model A: collect + enrich → awe_human_motion/
  Model B: collect + enrich → awe_llm_reasoning/

Phase 2: 交叉审查
  Model A 审查 → awe_llm_reasoning/review_report_by_claude.md
  Model B 审查 → awe_human_motion/review_report_by_gpt.md

Phase 3: 修复
  各自根据对方的 review_report 修复自己的产出
  修复后在 meta.yaml 中标记 reviewed: true
```

---

## 五、CLI 自动化方案

### 5.1 工具选择

| 工具 | 适用场景 | 无人值守能力 |
| --- | --- | --- |
| Claude Code CLI (`claude`) | 本地终端直接调用，支持 `--print` 非交互模式 | ✅ 可脚本化，支持 pipe 输入 |
| Codex CLI (`codex`) | OpenAI 的终端 agent，支持 `full-auto` 模式 | ✅ `--approval-mode full-auto` 可无人值守 |
| Cursor 对话窗口 | GUI 交互 | ❌ 需要手动开新会话 |
| Cursor Codex 插件 | GUI 内嵌 | ❌ 需要手动触发 |

**结论：要实现自动化，应该用 Claude Code CLI + Codex CLI，而不是 Cursor GUI。**

### 5.2 自动化脚本示例

```bash
#!/bin/bash
# rwiki_auto_collect.sh
# 用法: ./rwiki_auto_collect.sh <source_id> <model>
# 示例: ./rwiki_auto_collect.sh awe_human_motion claude
#       ./rwiki_auto_collect.sh awe_llm_reasoning codex

SOURCE_ID=$1
MODEL=$2
WORKSPACE="/home/ripemangobox/Coding/Github/OpenSource/Open_Ready/ResearchFlow"
SPEC="$WORKSPACE/_private/planning/rwiki/rwiki_batch_task_spec.md"
ARCH="$WORKSPACE/_private/rwiki_architecture.md"

PROMPT="你正在执行 ResearchWiki 的批量构建任务。

工作目录：$WORKSPACE/ResearchWiki/
任务 spec：_private/planning/rwiki/rwiki_batch_task_spec.md
架构参考：_private/rwiki_architecture.md

执行规则：
1. 读取 sources/$SOURCE_ID/meta.yaml，确定当前进度（如果不存在则从 Step 1 开始）
2. 从上次中断的 step 继续执行
3. 每完成一个 step 或处理 20 条记录，更新 meta.yaml 和 csv
4. enrich 步骤中，对 missing_paper_link 的条目用论文标题搜索 arxiv/semantic scholar 补全
5. 网络请求失败的条目标记 failed 跳过，不阻塞
6. 不要等我确认，自动持续执行直到该 source 的 collect + enrich 完成
7. 完成后输出状态摘要

当前任务：处理 source_id=$SOURCE_ID"

if [ "$MODEL" = "claude" ]; then
    # Claude Code CLI - 非交互模式
    echo "$PROMPT" | claude --print --dangerously-skip-permissions \
        --max-turns 50 \
        -p "$PROMPT"

elif [ "$MODEL" = "codex" ]; then
    # Codex CLI - full-auto 模式
    cd "$WORKSPACE"
    codex --approval-mode full-auto \
        --quiet \
        "$PROMPT"
fi
```

### 5.3 并行执行

```bash
# 终端 1: Claude 处理 pilot
./rwiki_auto_collect.sh awe_human_motion claude

# 终端 2: Codex 处理 batch 1 第一个
./rwiki_auto_collect.sh awe_llm_reasoning codex

# 两个终端并行，各自写各自的 sources/<source_id>/，不冲突
```

### 5.4 断点续跑（上下文耗尽后）

CLI 工具单次执行有 token 上限，耗尽后脚本退出。再次运行同一命令即可续跑：

```bash
# 第一次跑到一半，上下文满了，自动退出
./rwiki_auto_collect.sh awe_human_motion claude

# 直接再跑一次，agent 读 meta.yaml 从断点继续
./rwiki_auto_collect.sh awe_human_motion claude
```

meta.yaml 的 `last_step` + `last_step_status` 确保不会重复处理已完成的部分。

### 5.5 互查自动化

```bash
# Claude 审查 GPT 的产出
REVIEW_PROMPT="你正在审查 GPT 产出的 ResearchWiki source 数据。
审查目标：ResearchWiki/sources/awe_llm_reasoning/
参考规范：_private/planning/rwiki/rwiki_batch_task_spec.md
按 _private/planning/rwiki/rwiki_gpt_claude_doublecheck.md 中的审查清单执行。
输出：sources/awe_llm_reasoning/review_report_by_claude.md"

echo "$REVIEW_PROMPT" | claude --print --dangerously-skip-permissions -p "$REVIEW_PROMPT"

# GPT 审查 Claude 的产出
codex --approval-mode full-auto \
    "你正在审查 Claude 产出的 ResearchWiki source 数据。
审查目标：ResearchWiki/sources/awe_human_motion/
参考规范：_private/planning/rwiki/rwiki_batch_task_spec.md
按 _private/planning/rwiki/rwiki_gpt_claude_doublecheck.md 中的审查清单执行。
输出：sources/awe_human_motion/review_report_by_gpt.md"
```

---

## 六、注意事项

1. `_global/paper_registry.csv` 的写入需要在双方都完成 enrich 后统一合并，避免并发写冲突
2. Claude Code CLI 需要先 `claude login`；Codex CLI 需要先配置 API key
3. `--dangerously-skip-permissions` 允许 Claude 自动执行文件写入，生产环境慎用
4. 建议先在 pilot source 上手动跑一遍验证流程，再切换到 CLI 自动化
5. 两个 CLI 工具的 prompt 格式和能力略有差异，但只要 csv 输出格式一致，互查就不会有问题
