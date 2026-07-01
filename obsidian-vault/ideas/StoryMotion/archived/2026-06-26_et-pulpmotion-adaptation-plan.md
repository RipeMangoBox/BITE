---
title: "E.T. / DIRECTOR 适配 PulpMotion 数据处理方案"
created: 2026-06-26T21:15:00+08:00
updated: 2026-06-26T22:22:24+08:00
status: draft
tags:
  - StoryMotion
  - PulpMotion
  - camera_trajectory
  - baseline_adaptation
source_papers:
  - "[[analysis/ECCV_2024/E_T_the_Exceptional_Trajectories_Text_to_camera_trajectory_generation_with_character_awareness.md|E.T. / DIRECTOR]]"
  - "[[analysis/ICLR_2026/Pulp_Motion_Framing_aware_multimodal_camera_and_human_motion_generation.md|Pulp Motion]]"
hypothesis: |
  E.T. / DIRECTOR 可以收窄为 StoryMotion 的 camera completion baseline：输入 camera text、human motion 和可选 human text，输出 camera trajectory。适配目标是完成该 baseline 的必要数据契约，而不是复现或扩展 E.T. 的全部功能。
---

> [!abstract] 结论
> 当前任务不是找 E.T. checkpoint，也不是做完整 E.T. 功能复现，而是把 E.T. / DIRECTOR 作为 StoryMotion 的 camera completion baseline。允许输入 camera text、human motion 和 human text；唯一目标输出是 camera trajectory。现有 `director_pulp_mixed` 已满足 `traj`、`intrinsics`、`caption`、`caption_clip`、`cam_segments` 和 split 的基本读取；缺口集中在把 Pulp human motion 转为 `char` / `char_raw` 条件、重算 Pulp 专用标准化统计，以及完成 camera trajectory 输出与评估闭环。

## 目标边界

- 目标任务：StoryMotion camera completion baseline。
- 输入条件：
  - camera text：优先使用 `caption_cam`。
  - human motion：从 PulpMotion `smpl_raw["transl"]` 派生 E.T. loader 可读的角色中心轨迹。
  - human text：可选使用 `caption_char`，低风险方式是拼接到 camera text。
- 输出：camera trajectory only。
- 不做：
  - 不需要 E.T. official checkpoint。
  - 不需要生成 human motion。
  - 不需要 mesh / vertices / full SMPL 条件进入 E.T.。
  - 不需要扩展成完整 text-to-character-camera generation。

## 已核实事实

- E.T. / DIRECTOR 官方数据入口位于 5090 的 `/data/public/ripemangobox/Motion/baselines/DIRECTOR_storymotion_20260626`。
- 官方 loader 的核心文件契约：
  - `mixed_train_split.txt`、`mixed_val_split.txt`、`mixed_test_split.txt`：每行一个 sample id，不带后缀。
  - `traj/<id>.txt`：KITTI pose，每帧一行 3x4 pose；读入后转为 4x4 SE3，再转为 6D rotation + translation，共 9 维，pad 到 300 帧。
  - `intrinsics/<id>.npy`：当前 loader 原样返回；已有导出已修成 `(300, 4)` `float32`。
  - `caption/<id>.txt`、`caption_clip/seq/<id>.npy`、`caption_clip/token/<id>.npy`、`cam_segments/<id>.npy`：用于文本条件和 CLaTr 相关 raw 输出。
  - `char/<id>.npy`：`CharacterDataset` 期望 `(T, 3)` 角色中心轨迹，pad 到 300。
  - `char_raw/<id>.npy`：代码执行 `np.load(center_path)[0]`，因此应保存 `(T, 3)` 或至少 `(1, 3)`，不能保存 `(3,)`。
- 已有 `/data/public/ripemangobox/Motion/baselines/data/director_pulp_mixed`：
  - 已有 `traj`、`intrinsics`、`caption`、`caption_cam`、`caption_clip`、`caption_cam_clip`、`cam_segments`、mixed split。
  - 缺少 `char` 和 `char_raw`。
  - dataloader smoke 曾通过 `traj_feat (B, 9, 300)`、`intrinsics (B, 300, 4)`、`caption_feat (B, 512, 77)`。
- PulpMotion 原始字段：
  - `smpl_raw/<id>.npy` 是 object dict，包含 `body_pose (T, 23, 3, 3)`、`betas (T, 10)`、`transl (T, 3)`、`global_orient (T, 1, 3, 3)`。
  - `smpl_rifke/<id>.npy` 是 `(T, 199)`。
  - `caption_char/<id>.txt` 是人体动作文本。
  - `caption_cam/<id>.txt` 是相机运动文本。
  - `intrinsics/<id>.npy` 原始为 `(T, 4)`。

## 分类

| 内容                       | 分类     | 处理判断                                                                                                  |
| ------------------------ | ------ | ----------------------------------------------------------------------------------------------------- |
| mixed split 文件           | 直接满足   | 已由 StoryMotion cache 的 train / val sample id 写出。                                                      |
| `traj/<id>.txt`          | 直接满足   | 已能被 DIRECTOR `TrajectoryDataset` 读入并输出 `(9, 300)` 特征。                                                 |
| `intrinsics/<id>.npy`    | 直接满足   | 原始 `(T, 4)` 已补齐为 `(300, 4)` `float32`。                                                                |
| `caption_clip`           | 直接满足   | 已把 PulpMotion object/half-like CLIP 数组转成 `float32`，可被 loader 读取。                                      |
| `cam_segments`           | 直接满足   | PulpMotion 已提供；可作为 caption segment raw 数据。                                                            |
| `caption/<id>.txt`       | 适配后能解决 | camera completion 版本优先使用 `caption_cam`；若要利用 human text，再拼接 `caption_char`。                            |
| `char/<id>.npy`          | 适配后能解决 | 从 `smpl_raw["transl"]` 写出 `(T, 3)`，表示角色中心轨迹。                                                          |
| `char_raw/<id>.npy`      | 适配后能解决 | 同样写出 `transl (T, 3)`，保证 `np.load(...)[0]` 是第一帧三维中心。                                                   |
| Pulp 专用标准化统计             | 适配后能解决 | 必须重算 camera translation、camera velocity、char center、char velocity 的 mean/std，不能复用 E.T. 原 `0300.yaml`。 |
| E.T. 原始角色条件语义等价          | 无法直接解决 | 对 camera completion baseline 不需要追求完整等价；只需验证 `transl` 作为 human motion 条件能改善 camera trajectory。                 |
| 文本控制力                    | 无法直接解决 | 格式接通不证明模型使用了文本；必须通过 caption shuffle / caption swap / 固定角色换文本诊断。                                       |
| PulpMotion 与 E.T. 源域分布差异 | 无法直接解决 | 相机风格、尺度、帧率、场景来源和角色轨迹分布都可能偏移，只能实验验证。                                                                   |

## `char` / `char_raw` 方案

优先从 `smpl_raw["transl"]` 派生，而不是从 `smpl_rifke` 反拆 root。

理由：

- E.T. 的 `CharacterDataset` 实际使用的是 `(T, 3)` 角色中心轨迹，不需要完整 SMPL 姿态。
- `smpl_raw["transl"]` 是显式三维全局平移，语义上最接近角色中心或 root trajectory。
- `smpl_rifke` 是 199 维压缩运动表示，拆 root 需要依赖额外约定；在没有确认维度语义前不应使用。

导出规则：

```text
char/<id>.npy     = smpl_raw["transl"].astype(float32)      # shape: (T, 3)
char_raw/<id>.npy = smpl_raw["transl"].astype(float32)      # shape: (T, 3)
```

注意：`char_raw` 不能保存成 `(3,)`，因为当前代码取 `np.load(...)[0]`，`(3,)` 会得到标量。

## 文本条件选择

最小可运行版本使用 `caption_cam`：

- E.T. / DIRECTOR 的主任务是 text-to-camera trajectory。
- `caption_cam` 描述 camera movement，和目标输出 `traj` 对齐。
- 已有导出已经把 `caption_cam` 链接为 `caption`，工程风险最低。

利用 human text 的 camera completion 版本可以增加 `caption_char`：

- 低风险方案：拼接文本，例如 `camera: <caption_cam>. character: <caption_char>.`
- 高风险方案：双文本编码器或多条件融合，需要改模型；除非单文本拼接失败，否则不作为第一步。
- 不建议直接用 `caption_char` 替代 `caption_cam`，因为它改变了任务条件：人体动作文本不能直接监督相机运动文本控制。

## 执行路线

### Phase 0：保持现有最小读取

目标：确认当前 `traj+caption` 数据视图稳定。

- 使用 `configs/dataset/traj+caption.yaml` 或等价配置，避免 character 分支。
- 确认 batch shape：
  - `traj_feat`: `(B, 9, 300)`
  - `intrinsics`: `(B, 300, 4)`
  - `caption_feat`: `(B, 512, 77)` 或模型期望的转置形式
- 只声明“格式可读取”，不声明 E.T. 已完成适配。

### Phase 1：Pulp 专用标准化

目标：避免使用 E.T. 源域统计训练 Pulp 数据。

- 从 Pulp `traj` 读出 4x4 pose。
- 按 DIRECTOR `TrajectoryDataset.get_feature` 同样逻辑统计：
  - 第一帧 translation 的 `shift_mean` / `shift_std`
  - 后续 translation velocity 的 `norm_mean` / `norm_std`
- 从 `smpl_raw["transl"]` 统计：
  - 第一帧 char center 的均值/方差
  - 后续 char velocity 的均值/方差
- 写新的 standardization yaml，例如 `configs/dataset/standardization/pulp0300.yaml`。

### Phase 2：补齐 human-motion 条件数据视图

目标：把 Pulp human motion 以 E.T. loader 可读的角色中心轨迹形式接入 camera completion baseline。

- 生成：
  - `char/<id>.npy`
  - `char_raw/<id>.npy`
- 所有样本长度保持原始 `T`，由 loader pad 到 300。
- 对齐 sample id 和 split，不生成 split 外文件也可以，但全量生成便于复用。
- 运行 `traj+caption+char` dataloader smoke，确认：
  - `char_feat` shape 与模型配置一致。
  - `char_raw["char_centers"]` 不是全零或标量错误。
  - padding mask 与 `traj` 长度一致。

### Phase 3：camera completion 短训与诊断

目标：验证输出 camera trajectory 是否可训练，以及 camera text / human motion / human text 条件是否真的影响 camera completion。

- 先跑 1-2 epoch smoke，不做效果宣称。
- 最低诊断：
  - loss 不 NaN。
  - 训练 loss 有下降趋势。
  - 反标准化后的 camera translation 范围与 ground truth 同量级。
  - 生成轨迹不是静态塌缩。
- 文本控制诊断：
  - caption shuffle 后性能应下降。
  - 固定角色轨迹替换 camera caption，生成相机运动应有可测差异。
- character 条件诊断：
  - 固定 caption 替换 character trajectory，生成 camera 与角色的相对距离 / 视野内比例应变化。

## 验证指标

最小版本：

- ATE / 平移误差：生成 camera translation 与 GT 的绝对或对齐后误差。
- 旋转角误差：由生成 6D rotation 反解得到 rotation matrix 后统计角误差。
- 速度分布：translation velocity 的 JS divergence 或 Wasserstein distance。
- 静态基线对比：必须优于 zero-motion / mean-trajectory / random trajectory。

human-motion conditioned camera completion 版本：

- 角色入画率：用 generated camera + `smpl_raw["transl"]` / skeleton 投影，统计 root 或关键点是否在画面范围内。
- camera-character 距离分布：生成结果与 GT 的距离分布差异。
- 相对朝向：camera forward 与角色方向或角色中心向量的夹角分布。
- caption shuffle / char shuffle 消融：证明文本和角色条件确实被使用。

## 不能写成已解决的风险

- 不能写“E.T. 已适配完成”：在 `char` / `char_raw`、Pulp 标准化和短训诊断完成前，只能写“已完成部分数据视图”。
- 不能写“完整 E.T. character-aware 已成立”：本 baseline 只需要 human motion 条件辅助 camera completion，不需要证明与原始 E.T. 角色条件分布完全等价。
- 不能复用 E.T. `0300.yaml` 后声称公平：这是源域统计，Pulp 必须重算。
- 不能写“文本控制有效”：必须做 caption shuffle / swap 才能证明。
- 不能写“PulpMotion 的完整 SMPL 已被 E.T. 利用”：当前 baseline 只用 SMPL `transl` 作为 human motion 条件，不吃 `body_pose`、`betas` 或 `global_orient`。
- 不能把 `traj+caption` 最小版说成完整 camera completion baseline：它只用 camera text，没有用 human motion。
- 不能只凭 dataloader smoke 宣称 baseline 可比较：至少需要短训稳定性、反标准化 sanity 和基础定量指标。

## 下一步任务清单

1. 扩展 `_private/storymotion_baselines/prepare_director_pulp.py`，新增 `char` / `char_raw` 导出。
2. 新增 Pulp 专用 standardization 统计脚本，输出 `pulp0300.yaml`。
3. 分别跑 `traj+caption` 与 `traj+caption+char` dataloader smoke。
4. 跑 1-2 epoch 训练 smoke，记录 loss、反标准化轨迹范围和非塌缩检查。
5. 再决定是否进入完整训练，不提前使用“E.T. 已落实”表述。
