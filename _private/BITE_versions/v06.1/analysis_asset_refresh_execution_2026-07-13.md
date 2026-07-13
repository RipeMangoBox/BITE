# BITE v06.1 分析资产刷新执行摘要

- date: 2026-07-13
- baseline: `_private/BITE_versions/v06/latest_analysis_chain_2026-07-03.md`
- scope: `obsidian-vault/analysis/*/*.md`
- source policy: 仅使用现有分析资产、v06 规则和本地元数据；未读取原 PDF

## 结果

| 项目 | 结果 |
|------|-----:|
| 全库 paper notes | 5,345 |
| 严格 v06 canonical | 5,341 |
| 启动前 dirty、未覆盖 | 5 |
| 图片人工复查 | 2,906 |
| 图片复查批次 | 59 |
| 最终图片总数 | 41,414 |
| 缺失且无法唯一修复的 PDF embed | 1 |
| `analysised → checked` | 4,232 |
| 保持 `analysised` | 82 |

结构、frontmatter、链接和 embed 先经过 20 篇校准，再以三个互斥 shard 执行。非标准结构随后以 54/57/53 三个批次逐篇处理。图片层使用 soft target：图数和“补充图表”标题仅作为召回信号，不机械截断；方法总览、主结果、关键消融、跨任务结果、效率、鲁棒性、失败案例和代表性定性证据均可构成超过 6 张的保留理由。

## 例外

1. 4 篇非 canonical note 属于运行启动前已有用户修改，未自动覆盖。
2. 1 篇 note 的 PDF embed 指向缺失文件，且本地没有唯一候选，因此未猜测替换。
3. 82 条状态未提升：72 条无法映射到唯一 note，6 条存在重复/冲突映射，4 条对应启动前 dirty note。

逐篇证据见 `_private/BITE_versions/v06.1/runs/2026-07-13/` 下的 manifest、59 份图片复查报告、三份轮转汇总及 `state_promotion_report.json`。
