你在审查一个本地代码仓库中的 TAMR / MotionPatches 改动。请重点审查“计划是否合理、代码是否真的落实了计划、之前指出的问题是否被正确修复、还有没有新的逻辑/实现风险”。不要把实验分数高低当成主结论，但可以用输出文件是否落盘来判断闭环是否接通。

工作目录：
/home/ripemangobox/Coding/Github/Motion/TMR

请优先阅读这些文件：
- /home/ripemangobox/Coding/Github/Motion/TMR/MotionPatches-main/structured_rerank.py
- /home/ripemangobox/Coding/Github/Motion/TMR/MotionPatches-main/scripts/test.py
- /home/ripemangobox/Coding/Github/Motion/TMR/MotionPatches-main/conf/config.yaml
- /home/ripemangobox/Coding/Github/Motion/TMR/MotionPatches-main/conf/test_config.yaml
- /home/ripemangobox/Coding/Github/Motion/TMR/MotionPatches-main/scripts/run_mp_s2e_v2_stage1_rerank_train.sh
- /home/ripemangobox/Coding/Github/Motion/TMR/MotionPatches-main/scripts/run_mp_s2e_v2_stage1_rerank_server_gpu1.sh
- /home/ripemangobox/Coding/Github/Motion/TMR/ResearchWY/paperIDEAs/TAMR/ROADMAP_naive_stage1.md

如果需要理解 motion/text 投影空间，也请参考：
- /home/ripemangobox/Coding/Github/Motion/TMR/MotionPatches-main/models/clip.py

这次改动的目标：
1. Stage 1 structured rerank 的样本分流规则：
   - K=1 -> global fallback
   - K>=2 默认 ordered monotonic
   - 只有显式 overlap cue（while/simultaneously/...）才走 unordered
2. 默认 DP 主线改为 strict，relaxed 只做对照
3. 修复之前最关键的问题：
   - 之前 top-K 内候选被替换为 zscore/rank 融合分数，top-K 外仍是原始 cosine，导致分数域不一致、全局 R@K 排名语义错误
   - 现在应该改成：只重排 top-K 内部顺序，并把最终顺序映射回原始 global score 域，不改变 top-K 集合本身
4. event encoding 增加 context 模式
5. test.py 中加入两个诊断：
   - top-K ceiling
   - reverse-order sanity
6. runtime eval.structured_rerank override 能正确 merge 到 saved_cfg
7. 对 context 文本截断风险进行了真实统计监测，并把监测指标接入 rerank eval 输出
8. 文档已同步更新 skip 语义与当前实现

你之前提出过这些核心意见，请你在本轮审查时明确检查它们是否已经被正确处理：
- 核心意见 A：top-K 内外分数域不一致是最需要优先修复的问题；如果没修好，会直接污染 rerank 指标语义
- 核心意见 B：skip 模式代码语义与 ROADMAP 文案可能不一致，需要文档或代码对齐
- 核心意见 C：context 截断风险需要真实统计，不应只靠猜测
- 核心意见 D：unordered matching 的 exact 版本当前可以接受，但如果实现复杂度与实际数据分布不匹配，需要指出
- 核心意见 E：server gpu1 脚本的 quoting / env / tmux 需要检查稳健性
- 核心意见 F：如果未来继续优化 temporal token 空间，比起直接用 pre-projection time tokens，更可能应该走“独立 temporal projection”路线；本轮只需检查当前代码是否把这个选择说清楚，不要求你推动实现

当前作者声称已经做了这些修正：
1. rerank 现在只重排 top-K 内部顺序，不再混用 fused score 和 outside global cosine 的不同分数域
2. skip 语义在文档里已明确为“最多跳过 2 个中间 segment”
3. context truncation 已做真实统计，当前 strict test 上：
   - truncated_count = 0
   - truncated_rate = 0
   - focus event fully_visible_rate = 1.0
4. truncation 监测指标已经自动写入 TMR-rerank.yaml
5. runtime eval.structured_rerank merge 已修复
6. 训练 recipe 仍保持与 S2E-v2 baseline 一致（epoch=50, batch_size=64）

请你完成以下审查任务：
1. 重建这次改动背后的设计意图，判断代码是否真的实现了这些意图
2. 逐条检查你之前的核心意见 A-F：
   - 哪些已经被正确修复
   - 哪些只是部分修复
   - 哪些还有残余风险
3. 特别检查这些点：
   - `structured_rerank.py` 里 top-K rerank 后的排名语义是否严格成立
   - top-K 外样本是否不可能因为分数域问题“反超”进来
   - `skip` 模式的实现和文档是否一致
   - context 编码是否真的按“完整 caption + event context + focus event”实现
   - truncation 统计逻辑本身是否正确，而不只是统计结果看起来正常
   - `test.py` 中 runtime config merge 是否已经彻底修复
   - server gpu1 脚本是否存在 quoting / tmux / path / env 风险
4. 你不需要重点讨论实验结果好坏；如果看到 rerank 分数下降，不要把这当成代码 bug，除非能证明是实现错误
5. 如果你认为当前版本在“计划-实现一致性”上基本成立，请明确说出来；如果你仍认为某个问题没真正修好，请指出具体文件和行号

输出格式要求：
1. 先给 Findings，按严重程度排序
2. 每条都带文件路径和行号
3. 明确区分：
   - 已修复的问题
   - 未修复/部分修复的问题
   - 新发现的问题
4. 再给 Open Questions / Residual Risks
5. 最后给一个很短的 Overall Assessment

如果你认为没有高置信 bug，也请明确写：
“未发现高置信实现错误，但存在以下 residual risks ...”
