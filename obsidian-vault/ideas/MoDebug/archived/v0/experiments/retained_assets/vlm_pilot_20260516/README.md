---

## title: "MoDebug VLM切片标注实验总览"
created: 2026-05-16T17:37:56+08:00
updated: 2026-05-16T17:37:56+08:00
status: active
tags:
  - MoDebug
  - HumanML3D_E
  - VLM_caption
  - human_check
hypothesis: |
  VLM 切片标注和 PoseFix 几何侧证据可以作为 motion-side event boundary 的交叉检查，但必须按动作类型区分证据强度，不能直接升级为 formal evaluator。
source_papers:
  - "[[paperIDEAs/2026-05-12_fine-grained-text-motion-alignment-design|CPGA 时间戳设计]]"

# MoDebug VLM切片标注实验总览

## 当前结论

这一组实验只支持一个保守结论：VLM 切片标注可以做 `cross_check / diagnostic`，尤其适合可见姿态变化、显著肢体动作、转身和带轨迹叠加的往返位移；它还不能作为最终 evaluator，也不能独立判断精确步数、前进/后退、左右侧或回到起点。

## 样本索引

文件入口：

1. [[paperIDEAs/MoDebug/VLM/vlm-slice-caption-pilot-humanml3de_011798_trajectory_sanity]]
2. [[paperIDEAs/MoDebug/VLM/vlm-slice-caption-pilot-humanml3de_Q_009402]]
3. [[paperIDEAs/MoDebug/VLM/vlm-slice-caption-pilot-humanml3de_V_004012]]
4. [[paperIDEAs/MoDebug/VLM/vlm-slice-caption-pilot-humanml3de_T_004973]]
5. [[paperIDEAs/MoDebug/VLM/vlm-slice-caption-pilot-humanml3de_008354]]
6. [[paperIDEAs/MoDebug/VLM/vlm-slice-caption-pilot-humanml3de_009041]]


| 样本         | 实验定位              | 最可靠证据                                    | 主要限制            | 建议 human check                  |
| ---------- | ----------------- | ---------------------------------------- | --------------- | ------------------------------- |
| `V_004012` | 单腿上抬、踢出、收回的下肢动作正例 | `0.5s` 切片                                | 左/右脚和回到膝盖关系不稳   | 看 `1.0s-2.0s` 抬腿、`2.5s-3.5s` 踢出 |
| `T_004973` | 下蹲、双臂伸出、站起的姿态型正例  | `0.5s` 切片                                | 双臂是向前还是向外不稳     | 看 `2.0s-2.5s` 是否同时下蹲和伸臂         |
| `008354`   | 轻踢 + 小幅前后移动的中等正例  | `0.5s` 切片 + 轨迹图                          | 前进/后退幅度小，左脚身份不稳 | 看 `1.0s-1.5s` 是否为轻踢             |
| `009041`   | 投掷强、前走和后踢弱的失败边界样本 | 投掷窗口                                     | 位移和右腿后踢证据弱      | 不要把投掷强证据扩展到全部 event             |
| `Q_009402` | 短转身 + 回起点合理性检查样本  | `0.5s` 切片 + root trace                   | 回到起点不能只靠静态图     | 分开检查转身、停止、终点接近起点                |
| `011798`   | 长程往返轨迹最强合理性检查样本   | 全局 root trajectory + `0.5s` 切片 + PoseFix | 步数、jog、前进/后退不稳  | 主查外行、折返、返回、停止，不查精确计步            |


## 推荐检查顺序

1. 先看 `011798`：验证全局轨迹叠加是否确实让外行、折返、返回、停止可读。
2. 再看 `Q_009402`：验证短转身和回起点是否需要 root trace。
3. 再看 `V_004012` 和 `T_004973`：验证姿态/肢体动作是否适合 `0.5s` 切片。
4. 最后看 `009041`：确认当前 renderer 对弱 locomotion 和腿部后踢的失败模式。

## 统一证据角色

- `GT MP4`：人工主视觉证据，用于确认静态切片是否误导。
- `full_sequence_progression`：全局动作顺序粗查。
- `global_trajectory`：只用于位移、回到起点、外行/返回阶段。
- `1.0s` 切片：粗粒度合理性检查，不做精细边界。
- `0.5s` 切片：当前最适合 human check 的默认粒度。
- `0.2s` 切片：只做边界细化，不做独立 caption。
- `PoseFix`：只做静态几何和转向交叉检查，不判断速度、计步和相对身体朝向的语义。

## 不可写成结论的内容

1. 不写“VLM 可以做 HumanML3D-E 最终时间戳 evaluator”。
2. 不写“VLM 已经可靠判断精确步数”。
3. 不写“PoseFix 可以替代动态 motion evaluator”。
4. 不写“root 居中的静态 sheet 能单独判断回到起点”。
5. 不写“左右侧或前进/后退已经解决”，除非有明确视角或人工校准。

## 下一步最小动作

1. 对 `011798` 和 `Q_009402` 做人工复核表：每个 event 标 `visible / ambiguous / absent`。
2. 对 `V_004012`、`T_004973`、`008354` 做 `0.5s` event window 人工标注。
3. 对 `009041` 记录失败类型：renderer 不足、event 本身弱、还是 VLM caption 不稳。
4. 下一轮 prompt 不再自由 caption 全序列，而是输入已知 event，要求输出候选时间窗、证据来源和限制。

