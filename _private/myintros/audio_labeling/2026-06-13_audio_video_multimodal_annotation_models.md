# 面向 Motion 配对数据的音频清洗、处理与标注模型方案清单

生成日期：2026-06-13  
资料来源：官方文档 / [GitHub API](https://docs.github.com/en/rest)  
适用对象：舞蹈 / 说话视频中的音频清洗、切分、对齐、事件标注，以及 motion 训练数据配对

## 0. 结论先行

面向 motion 数据构建时，音频侧的核心目标不是覆盖所有音视频多模态标注任务，而是把原始视频中的音频处理成可与动作片段稳定配对的训练输入。常见输入包括舞蹈音乐、单人或多人说话、说话叠加背景音乐、环境声、掌声、脚步声、噪声和混响。

推荐把工作拆成五个主流程：

```text
音频标准化与质检
  -> 人声 / 音乐 / 背景声分离
  -> 降噪、去混响、响度归一化
  -> 语音 / 音乐 / 事件时间轴标注
  -> 与 motion 片段对齐并导出训练元数据
```

通用多模态大模型可用于摘要、规则检查和异常样本解释；帧级时间边界、说话人分离、音乐节拍、音频事件和音频清洗仍应使用专用模型或音频工具。

## 1. 维护时间口径

| 类型 | 维护时间写法 | 说明 |
|---|---|---|
| GitHub 开源项目 | `pushed_at` | 通过 GitHub API 核验的最近推送时间；不是 star 更新时间。 |
| 商用 API / 云服务 | 官方文档更新时间或本次访问核验日 | 厂商通常不公开模型仓库维护时间，因此用官方文档可用性和页面更新时间。 |
| 论文 / 基准 | 最近公开代码或项目更新时间 | 若代码归档、长期不维护或只适合作为基线，降级为观察项。 |

维护状态分级：

| 等级 | 含义 |
|---|---|
| 主推荐 | 可直接进入标注辅助管线，或作为稳定 API / 工程工具使用。 |
| 辅助 | 能提供特征、初稿、检索或质检，但不能单独完成最终标注。 |
| 观察 | 有研究价值或特定场景可用，但维护偏弱、适配成本高或任务边界较窄。 |
| 不优先 | 过旧、归档、无稳定工程入口，本文不放入主推荐。 |

## 2. 面向 motion 配对音频的主流程

| 主流程 | 处理目标 | 主推荐 | 主要输出 |
|---|---|---|---|
| 音频标准化与质检 | 统一采样率、声道、响度，发现静音、爆音、严重噪声、音画不同步 | ffmpeg、librosa、pyAudioAnalysis、AudioCraft/EnCodec | clean wav、quality flags、sample_rate、duration、loudness |
| 人声 / 音乐 / 背景声分离 | 从舞蹈或说话视频中分离 vocal、music、accompaniment、noise | UVR、Spleeter、Demucs、ClearerVoice-Studio | vocal.wav、music.wav、background.wav、separation_confidence |
| 语音清洗与说话时间轴 | 对说话音频做降噪、增强、ASR、词级时间戳、说话人分离 | DeepFilterNet、ClearerVoice-Studio、WhisperX、pyannote.audio、OpenAI / Deepgram / AssemblyAI | transcript、word timestamps、speaker_id、speech segments |
| 音乐结构与节拍特征 | 为舞蹈 motion 提取 beat、onset、tempo、energy、mel/chroma 等特征 | librosa、madmom、aubio、CLAP、BEATs | beat_times、tempo、onsets、music features |
| 背景音 / 事件标注 | 标出掌声、脚步声、口哨、环境声、噪声等会影响 motion 的事件 | BEATs、PANNs、CLAP、TimeChat / Gemini 辅助解释 | event timeline、audio_only / audio_visual、confidence |
| 音画 / motion 对齐质检 | 检查动作与音频是否同步，处理跳舞对拍、说话口型、剪辑错位 | SyncNet、Light-ASD、TalkNet-ASD、人工抽检 | offset、sync_score、bad_clip flag |

## 3. 推荐数据处理管线

### 3.1 舞蹈视频：音乐驱动 motion

1. 原始视频输入。
2. 使用 [ffmpeg](https://ffmpeg.org/) 抽取音频并统一采样率 / 声道 / 响度。
3. 使用 [UVR](https://github.com/Anjok07/ultimatevocalremovergui)、[Spleeter](https://github.com/deezer/spleeter) 或 [Demucs](https://github.com/facebookresearch/demucs) 分离 music 与 vocal。
4. 使用 [DeepFilterNet](https://github.com/Rikorose/DeepFilterNet) 或 [ClearerVoice-Studio](https://github.com/modelscope/ClearerVoice-Studio) 处理残留噪声。
5. 使用 [librosa](https://github.com/librosa/librosa)、[madmom](https://github.com/CPJKU/madmom) 或 [aubio](https://github.com/aubio/aubio) 提取 beat、onset、tempo、energy。
6. 使用 [BEATs](https://github.com/microsoft/unilm/tree/master/beats) 或 [PANNs](https://github.com/qiuqiangkong/audioset_tagging_cnn) 标注掌声、脚步声、口哨等事件。
7. 与 motion clip 按统一时间轴切片并导出 paired metadata。

建议保留的字段：

| 字段 | 说明 |
|---|---|
| `audio_path` | 清洗后的主音频路径，通常为 music 或 mixed_clean。 |
| `music_path` | 分离出的音乐 / 伴奏轨。 |
| `vocal_path` | 分离出的人声轨；纯舞蹈数据可为空。 |
| `start/end` | 与 motion clip 对齐的音频片段边界。 |
| `tempo` | 片段 tempo。 |
| `beat_times` | 相对片段起点的 beat 时间。 |
| `onset_times` | 强起音时间，可用于动作爆发点对齐。 |
| `energy_curve` | RMS / loudness 曲线或下采样后的能量特征。 |
| `event_tags` | 掌声、脚步声、口哨、噪声、环境声等。 |
| `quality_flags` | clipping、silence、low_snr、desync、separation_artifact 等。 |

### 3.2 说话视频：语音驱动 gesture / facial motion

1. 原始视频输入。
2. 使用 [ffmpeg](https://ffmpeg.org/) 抽取音频并统一格式。
3. 使用 [DeepFilterNet](https://github.com/Rikorose/DeepFilterNet) 或 [ClearerVoice-Studio](https://github.com/modelscope/ClearerVoice-Studio) 做语音增强。
4. 使用 [WhisperX](https://github.com/m-bain/whisperX)、[OpenAI Speech-to-Text](https://developers.openai.com/api/docs/guides/audio)、[Deepgram](https://developers.deepgram.com/docs/diarization) 或 [AssemblyAI](https://www.assemblyai.com/docs/pre-recorded-audio/label-speakers) 转写。
5. 使用 [pyannote.audio](https://github.com/pyannote/pyannote-audio) 做 speaker diarization。
6. 使用 [OpenFace](https://github.com/TadasBaltrusaitis/OpenFace)、[SyncNet](https://github.com/joonson/syncnet_python) 或 [Light-ASD](https://github.com/Junhua-Liao/Light-ASD) 做口型和说话人同步质检。
7. 按 utterance 或固定窗口切片并导出 paired metadata。

建议保留的字段：

| 字段 | 说明 |
|---|---|
| `audio_path` | 清洗后的语音音频。 |
| `speaker_id` | 说话人 ID，多人说话场景必需。 |
| `utterance` | 句级文本。 |
| `word_timestamps` | 词级时间戳，用于细粒度 gesture / face motion 对齐。 |
| `speech_segments` | 语音活动区间。 |
| `overlap_speech` | 是否有多人重叠说话。 |
| `emotion_features` | 可选，语速、音高、能量、OpenFace / Hume 情绪线索。 |
| `lip_sync_score` | 可选，口型同步评分。 |
| `quality_flags` | noise、music_overlap、reverb、desync、bad_diarization 等。 |

### 3.3 说话叠加背景音乐 / 背景音

1. 原始视频输入。
2. 使用 [UVR](https://github.com/Anjok07/ultimatevocalremovergui)、[Spleeter](https://github.com/deezer/spleeter) 或 [ClearerVoice-Studio](https://github.com/modelscope/ClearerVoice-Studio) 做源分离，得到 vocal / music / background。
3. vocal 分支使用 [DeepFilterNet](https://github.com/Rikorose/DeepFilterNet)、[WhisperX](https://github.com/m-bain/whisperX) 和 [pyannote.audio](https://github.com/pyannote/pyannote-audio) 处理语音增强、ASR、diarization。
4. music 分支使用 [librosa](https://github.com/librosa/librosa)、[madmom](https://github.com/CPJKU/madmom) 或 [aubio](https://github.com/aubio/aubio) 处理 beat / tempo / energy。
5. background 分支使用 [BEATs](https://github.com/microsoft/unilm/tree/master/beats) 或 [PANNs](https://github.com/qiuqiangkong/audioset_tagging_cnn) 做音频事件标注。
6. 三条时间轴合并到 motion clip metadata。

这类数据不要简单丢弃背景音。背景音乐、掌声、脚步声和环境声可能是 motion 的有效条件，但要明确记录其来源和置信度。

## 4. 音频清洗、分离与特征提取模型

| 名称 | 类型 | 维护时间 | 推荐等级 | 适合输出 | 链接 |
|---|---|---:|---|---|---|
| librosa | 开源音频分析库 | 2026-06-12 | 主推荐 | beat、onset、tempo、mel、chroma、RMS 等音乐 / 语音特征 | https://github.com/librosa/librosa |
| madmom | 开源音乐信号处理库 | 2026-03-20 | 主推荐 | beat tracking、downbeat、onset 检测 | https://github.com/CPJKU/madmom |
| aubio | 开源音频分析库 | 2026-04-10 | 主推荐 | onset、pitch、beat、tempo | https://github.com/aubio/aubio |
| pyAudioAnalysis | 开源音频分析库 | 2025-08-04 | 主推荐 | 音频切分、分类、特征提取、静音检测 | https://github.com/tyiannak/pyAudioAnalysis |
| DeepFilterNet | 开源语音降噪 | 2024-10-17 | 主推荐 | 语音增强、背景噪声抑制 | https://github.com/Rikorose/DeepFilterNet |
| ClearerVoice-Studio | 开源语音处理工具箱 | 2025-08-14 | 主推荐 | 语音增强、语音分离、目标说话人提取 | https://github.com/modelscope/ClearerVoice-Studio |
| Ultimate Vocal Remover | 开源源分离 GUI / 模型入口 | 2025-03-13 | 主推荐 | vocal / instrumental / noise 分离，适合人工批处理 | https://github.com/Anjok07/ultimatevocalremovergui |
| Spleeter | 开源源分离库 | 2025-04-02 | 主推荐 | vocal / accompaniment / stems 分离 | https://github.com/deezer/spleeter |
| Demucs | 开源音乐源分离 | 2024-04-24，仓库已归档 | 辅助 | 高质量音乐源分离基线；新项目需注意归档状态 | https://github.com/facebookresearch/demucs |
| AudioCraft / EnCodec | 开源音频建模库 | 2026-03-03 | 辅助 | 音频 tokenizer / codec 表征，适合模型侧特征实验 | https://github.com/facebookresearch/audiocraft |

注意：

- motion 训练数据通常更需要稳定、可复现的音频特征，而不是复杂的语义标签。
- 音乐源分离会引入 artifact，导出时建议保留原始混音、分离后 music、分离后 vocal 三份路径。
- 对舞蹈数据，beat / onset / energy 曲线往往比自然语言描述更直接。

## 5. 语音时间轴、说话人和唇同步

目标输出：

- 说话片段：`start/end`
- 当前说话人：`speaker_id`
- 视频位置：人脸或人体 `bbox`
- 唇音同步：一致 / 不一致 / offset / 分数

推荐组合：

推荐组合：使用 [WhisperX](https://github.com/m-bain/whisperX) 或 [pyannote.audio](https://github.com/pyannote/pyannote-audio) 做语音活动检测 / diarization，使用 [InsightFace](https://github.com/deepinsight/insightface) 或 [YOLO](https://github.com/ultralytics/ultralytics) 做人脸 / 人体检测，使用 [ByteTrack](https://github.com/ifzhang/ByteTrack) 或 [DeepSORT](https://github.com/nwojke/deep_sort) 做跨帧跟踪，使用 [TalkNet-ASD](https://github.com/TaoRuijie/TalkNet-ASD) 或 [Light-ASD](https://github.com/Junhua-Liao/Light-ASD) 识别哪张脸在说话，并使用 [SyncNet](https://github.com/joonson/syncnet_python) 做唇音同步评分。

| 名称 | 类型 | 维护时间 | 推荐等级 | 适合输出 | 链接 |
|---|---|---:|---|---|---|
| pyannote.audio | 开源 diarization 工具箱 | 2026-06-12 | 主推荐 | 语音活动、说话人分离、重叠语音检测 | https://github.com/pyannote/pyannote-audio |
| WhisperX | 开源 ASR + 对齐 + diarization | 2026-06-03 | 主推荐 | 字词级时间戳、说话人分离、字幕初稿 | https://github.com/m-bain/whisperX |
| InsightFace | 开源人脸分析 | 2026-05-23 | 主推荐 | 人脸检测、身份聚类、face bbox | https://github.com/deepinsight/insightface |
| Ultralytics YOLO | 开源检测框架 | 2026-06-13 | 主推荐 | 人体 / 物体 bbox，适合接跟踪 | https://github.com/ultralytics/ultralytics |
| TalkNet-ASD | 开源主动说话人检测 | 2023-10-23 | 主推荐但需环境复核 | 画面中哪张脸在说话 | https://github.com/TaoRuijie/TalkNet-ASD |
| Light-ASD | 开源主动说话人检测 | 2025-03-23 | 主推荐 | 轻量主动说话人检测 | https://github.com/Junhua-Liao/Light-ASD |
| SyncNet | 开源唇音同步检测 | 2026-04-17 | 主推荐 | lip-sync offset / 一致性评分 | https://github.com/joonson/syncnet_python |
| LoCoNet-ASD | 开源主动说话人检测 | 2023-05-01 | 观察 | ASD 研究参考 | https://github.com/SJTUwxz/LoCoNet_ASD |
| SPELL | 开源主动说话人检测 | 2023-10-29 | 观察 | 长时空图 ASD 参考 | https://github.com/SRA2/SPELL |

注意：

- [pyannote.audio](https://github.com/pyannote/pyannote-audio) 和 [WhisperX](https://github.com/m-bain/whisperX) 只能从音频侧识别“谁在何时说话”，不能直接给视频 bbox。
- [TalkNet-ASD](https://github.com/TaoRuijie/TalkNet-ASD) / [Light-ASD](https://github.com/Junhua-Liao/Light-ASD) 需要先有人脸检测和 tracking。
- [SyncNet](https://github.com/joonson/syncnet_python) 是唇音同步评分工具，不是完整说话人定位系统。

## 6. 扩展能力清单

以下能力不是 motion 配对音频的最小闭环，但在说话风格建模、背景事件建模、质检和数据筛选中有使用价值。

### 6.1 情感与说话风格特征

目标输出：

- 情感类别：高兴、愤怒、焦虑、悲伤、中性等
- 维度分数：valence / arousal / dominance
- 证据：面部 AU、头姿、视线、语速、音高、能量、停顿

推荐组合：

推荐组合：使用 [OpenFace](https://github.com/TadasBaltrusaitis/OpenFace) 提取面部 AU / 视线 / 头姿，使用 [openSMILE](https://github.com/audeering/opensmile) 提取语音韵律特征，再使用 [Hume AI Expression Measurement](https://dev.hume.ai/docs/expression-measurement/overview) 或自训分类器输出情感维度，并人工复核“视听冲突”样本。

| 名称 | 类型 | 维护时间 | 推荐等级 | 适合输出 | 链接 |
|---|---|---:|---|---|---|
| Hume AI Expression Measurement | 商用 API | 2026-06-13 核验官方入口 | 主推荐 | 面部 / 语音 / 文本表达维度，适合情绪预标注 | https://dev.hume.ai/docs/expression-measurement/overview |
| OpenFace | 开源面部行为分析 | 2024-06-01 | 主推荐 | AU、landmark、head pose、gaze | https://github.com/TadasBaltrusaitis/OpenFace |
| openSMILE | 开源音频特征提取 | 2026-01-26 | 主推荐 | 音频情感特征、韵律特征 | https://github.com/audeering/opensmile |
| MERBench / MER Challenge | 研究基准 | 按年度更新 | 辅助 | 模型评测、情感识别 baseline | https://github.com/zeroQiaoba/MERTools |

注意：

- “笑着哭”“勉强微笑”这类冲突样本应标注模态证据，而不是只给单一情感标签。
- 商用情感 API 的输出标签体系要和项目标注规范统一，否则跨批次会出现标签漂移。

### 6.2 音频事件与音视频一致性

目标输出：

- 事件名：如 `crack_egg`、`door_slam`、`applause`
- 视频时间段：`video_start/video_end`
- 音频时间段：`audio_start/audio_end`
- 一致性：`audio_visual_consistency`
- 类型：`audio_only`、`video_only`、`audio_visual`

推荐组合：

推荐组合：使用 [BEATs](https://github.com/microsoft/unilm/tree/master/beats) / [PANNs](https://github.com/qiuqiangkong/audioset_tagging_cnn) 做音频事件候选，使用 [CLAP](https://github.com/LAION-AI/CLAP) 做音频-文本相似度检索，使用 [Moment-DETR](https://github.com/jayleicn/moment_detr) / [TimeChat](https://github.com/RenShuhuai-Andy/TimeChat) 做视频片段定位，并人工确认 `audio_only` / `video_only` / `audio_visual`。

| 名称 | 类型 | 维护时间 | 推荐等级 | 适合输出 | 链接 |
|---|---|---:|---|---|---|
| BEATs | 开源音频预训练 / 分类 | 2026-01-23 | 主推荐 | 音频事件表示、AudioSet 类别识别 | https://github.com/microsoft/unilm/tree/master/beats |
| PANNs | 开源 AudioSet tagging | 2024-07-25 | 主推荐 | 音频事件类别和置信度 | https://github.com/qiuqiangkong/audioset_tagging_cnn |
| CLAP | 开源音频-文本对齐 | 2025-05-15 | 主推荐 | 用文本查询音频事件，做粗对齐 | https://github.com/LAION-AI/CLAP |
| Moment-DETR | 开源视频时刻检索 | 2026-03-09 | 主推荐 | 文本查询对应的视频时间段 | https://github.com/jayleicn/moment_detr |
| TimeChat | 开源时间敏感视频 LLM | 2025-05-08 | 主推荐 / 辅助 | 长视频问答、时间定位描述 | https://github.com/RenShuhuai-Andy/TimeChat |
| VTimeLLM | 开源视频时刻理解 | 2024-06-13 | 辅助 | 视频 moment 描述和定位 | https://github.com/huangb23/VTimeLLM |
| ImageBind | 开源多模态 embedding | 2025-11-21 | 辅助 | 多模态检索、粗粒度对齐 | https://github.com/facebookresearch/ImageBind |
| AV-HuBERT | 开源音视频语音表征 | 2023-12-07，已归档 | 不优先 | 语音相关研究基线 | https://github.com/facebookresearch/av_hubert |

注意：

- 音视频事件对齐通常是“管线任务”，不是单模型任务。
- [ImageBind](https://github.com/facebookresearch/ImageBind) 很适合检索和 embedding，但不直接给精确事件边界。
- [AV-HuBERT](https://github.com/facebookresearch/av_hubert) 已归档，不建议作为新工程主依赖。

### 6.3 声源定位与可见声源分割

目标输出：

- 声音类别：如 `barking`、`instrument_playing`
- 声源位置：bbox / heatmap / segmentation mask
- 时间段：`start/end`
- 声源可见性：visible / offscreen / ambiguous

推荐组合：

推荐组合：使用音频事件模型识别声音类别，使用 [AVSBench](https://github.com/OpenNLPLab/AVSBench) 生态模型输出发声物体 mask，使用 [YOLO](https://github.com/ultralytics/ultralytics) / [GroundingDINO](https://github.com/IDEA-Research/GroundingDINO) 输出 bbox 或开放词汇检测，并人工处理画外音、遮挡、多声源。

| 名称 | 类型 | 维护时间 | 推荐等级 | 适合输出 | 链接 |
|---|---|---:|---|---|---|
| AVSBench | 音视频分割基准与官方实现 | 2024-11-18 | 主推荐 | 发声物体 segmentation mask | https://github.com/OpenNLPLab/AVSBench |
| AVSegFormer | 开源 AVS 模型 | 2025-03-06 | 主推荐 | 音视频分割、声源 mask | https://github.com/vvvb-github/AVSegFormer |
| CAVP | 开源 AVS 方法 | 2025-10-31 | 主推荐 | AVS 基线 / 改进方法 | https://github.com/cyh-0/CAVP |
| UFE-AVS | 开源 AVS 方法 | 2024-07-07 | 主推荐 / 辅助 | 利用未标注帧的 AVS | https://github.com/jinxiang-liu/UFE-AVS |
| GroundingDINO | 开源开放词汇检测 | 2024-08-12 | 辅助 | 文本提示检测声源候选 bbox | https://github.com/IDEA-Research/GroundingDINO |
| EZ-VSL | 开源视觉声源定位 | 2022-10-02 | 观察 | 声源热图经典基线 | https://github.com/stoneMo/EZ-VSL |

注意：

- 声源定位和声源分割不同：前者可输出热图/bbox，后者输出像素级 mask。
- 多声源、画外音和反射声是主要误差来源，必须保留 `offscreen` 和 `ambiguous` 标签。

### 6.4 动作 / 行为语义标签

目标输出：

- 行为标签：如 `phone_call`、`applause`、`coughing`
- 时间段：`start/end`
- 模态证据：`visual_evidence`、`audio_evidence`
- 置信度和冲突说明

推荐组合：

推荐组合：使用 [MMAction2](https://github.com/open-mmlab/mmaction2) / [PySlowFast](https://github.com/facebookresearch/SlowFast) / [InternVideo](https://github.com/OpenGVLab/InternVideo) 做视频动作候选，使用 [BEATs](https://github.com/microsoft/unilm/tree/master/beats) / [PANNs](https://github.com/qiuqiangkong/audioset_tagging_cnn) 做声音事件候选，使用 [CLAP](https://github.com/LAION-AI/CLAP) 或规则层合并跨模态证据，并人工复核容易混淆的动作。

| 名称 | 类型 | 维护时间 | 推荐等级 | 适合输出 | 链接 |
|---|---|---:|---|---|---|
| MMAction2 | 开源视频理解工具箱 | 2026-03-18 | 主推荐 | 动作识别、时序动作检测、训练评测 | https://github.com/open-mmlab/mmaction2 |
| PySlowFast / AudioSlowFast | 开源视频理解代码库 | 2026-03-16 | 主推荐 | 视频 / 音视频行为识别基线 | https://github.com/facebookresearch/SlowFast |
| InternVideo | 开源视频基础模型 | 2026-06-11 | 主推荐 | 视频理解、检索、动作识别迁移 | https://github.com/OpenGVLab/InternVideo |
| VideoMAEv2 | 开源视频预训练模型 | 2024-10-08 | 辅助 | 视频 backbone，需接音频分支 | https://github.com/OpenGVLab/VideoMAEv2 |

注意：

- “打电话”“咳嗽”“鼓掌”这类行为需要写清楚视觉证据和音频证据。
- 只做视频动作识别会漏掉“声音决定语义”的行为，必须接音频事件分支。

### 6.5 语音转写与字幕服务选型

目标输出：

- 字幕文本
- 字 / 词 / 句级时间戳
- speaker_id
- 可选 bbox：说话人脸框 / 身体框
- 可选元数据：语种、置信度、情绪、噪声说明

推荐组合：

推荐组合：使用 [WhisperX](https://github.com/m-bain/whisperX) / [OpenAI Speech-to-Text](https://developers.openai.com/api/docs/guides/audio) / [Deepgram](https://developers.deepgram.com/docs/diarization) / [AssemblyAI](https://www.assemblyai.com/docs/pre-recorded-audio/label-speakers) 生成转写和时间戳，使用 [pyannote.audio](https://github.com/pyannote/pyannote-audio) 做 diarization 或校正 `speaker_id`，再使用 ASD 模型关联视频中说话人 bbox，并人工校对专名、断句、重叠语音。

| 名称 | 类型 | 维护时间 | 推荐等级 | 适合输出 | 链接 |
|---|---|---:|---|---|---|
| WhisperX | 开源 ASR + 对齐 + diarization | 2026-06-03 | 主推荐 | 字词级时间戳、说话人标签 | https://github.com/m-bain/whisperX |
| Whisper | 开源 ASR | 2026-04-15 | 主推荐 | 转写、翻译、字幕草稿 | https://github.com/openai/whisper |
| OpenAI Speech-to-Text | 商用 API | 2026-06-13 核验官方文档 | 主推荐 | 转写、翻译、流式语音处理 | https://developers.openai.com/api/docs/guides/audio |
| Deepgram | 商用 API | 2026-06-13 核验官方文档 | 主推荐 | 转写、diarization、实时语音 | https://developers.deepgram.com/docs/diarization |
| AssemblyAI | 商用 API | 2026-06-13 核验官方文档 | 主推荐 | 转写、speaker diarization、摘要等 | https://www.assemblyai.com/docs/pre-recorded-audio/label-speakers |
| Azure AI Video Indexer | 商用视频分析服务 | 文档更新时间 2025-12-18 | 主推荐 | 视频转写、说话人、OCR、人物、场景等 insights | https://learn.microsoft.com/en-us/azure/azure-video-indexer/video-indexer-overview |

注意：

- 字幕和“多模态字幕”不是一回事。字幕工具负责文本和时间戳；视频 bbox 需要接 ASD / face tracking。
- 对会议和访谈，speaker diarization 的错误会直接污染后续说话人情感、字幕归属和会议纪要。

### 6.6 异常与音画不一致质检

目标输出：

- 异常时间段
- 异常类型：`audio_visual_mismatch`、`danger_event`、`deepfake_suspected`、`offscreen_alarm`
- 描述：音频证据、视频证据、冲突点
- 风险等级和复核状态

推荐组合：

推荐组合：使用视频异常模型筛出异常时间段，使用音频事件模型检查危险声音 / 警报 / 破碎声，使用 [audio-visual-forensics](https://github.com/cfeng16/audio-visual-forensics) 检查音画一致性和深伪风险，再使用通用视频 LLM 生成解释，但不作为最终判定。

| 名称 | 类型 | 维护时间 | 推荐等级 | 适合输出 | 链接 |
|---|---|---:|---|---|---|
| RTFM | 开源弱监督视频异常检测 | 2025-10-29 | 主推荐 | 安防异常时间段候选 | https://github.com/tianyu0207/RTFM |
| VadCLIP | 开源 CLIP 式视频异常检测 | 2024-03-10 | 主推荐 / 辅助 | 异常片段检索和分类 | https://github.com/nwpu-zxr/VadCLIP |
| audio-visual-forensics | 开源音视频取证 | 2024-05-12 | 主推荐 / 特定场景 | 音画异常、深伪/篡改检测线索 | https://github.com/cfeng16/audio-visual-forensics |
| Reality Defender | 商用深伪检测 | 2026-06-13 核验官网 | 辅助 | 深伪检测 API / 平台 | https://www.realitydefender.com/ |

注意：

- [RTFM](https://github.com/tianyu0207/RTFM) / [VadCLIP](https://github.com/nwpu-zxr/VadCLIP) 主要是视频异常，不等于音视频不一致检测。
- 深伪检测、异常检测、内容安全审核是不同任务；不要混用标签体系。

### 6.7 通用多模态模型的辅助用途

目标输出：

- 用户意图：如 `zoom_in`、`select_object`、`turn_on`
- 指代目标：bbox / mask / object_id
- 融合依据：语音指令、手势、视线、上下文
- 置信度和歧义说明

推荐组合：

推荐组合：使用 ASR 提取语音指令，使用手势 / 视线 / 目标检测模型定位目标，再使用 [Gemini API video understanding](https://ai.google.dev/gemini-api/docs/video-understanding)、[OpenAI 多模态 API](https://developers.openai.com/api/docs/guides/audio) 或 [Qwen3-VL](https://github.com/QwenLM/Qwen3-VL) 解析意图和指代，并人工复核含糊指令和多目标场景。

| 名称 | 类型 | 维护时间 | 推荐等级 | 适合输出 | 链接 |
|---|---|---:|---|---|---|
| Gemini API video understanding | 商用多模态 API | 文档更新时间 2026-06-01 | 主推荐 / 预标注 | 视频问答、长视频理解、时间定位辅助 | https://ai.google.dev/gemini-api/docs/video-understanding |
| Gemini Live API | 商用实时多模态 API | 2026-06-13 核验官方文档 | 主推荐 / 预标注 | 实时音视频交互、语音对话 | https://ai.google.dev/gemini-api/docs/live-api |
| OpenAI 多模态 API | 商用 API | 2026-06-13 核验官方文档 | 主推荐 / 预标注 | 音频转写、图像/帧理解、规则质检 | https://developers.openai.com/api/docs/guides/audio |
| Qwen2.5-Omni | 开源端到端多模态模型 | 2025-06-12 | 主推荐 / 预标注 | 文本、音频、图像、视频理解与语音生成 | https://github.com/QwenLM/Qwen2.5-Omni |
| Qwen3-VL | 开源视觉语言模型 | 2026-01-30 | 主推荐 / 预标注 | 图像/视频理解、视觉问答、文档和 GUI 理解 | https://github.com/QwenLM/Qwen3-VL |
| LLaVA-NeXT | 开源视觉/视频 LMM | 2026-04-15 | 主推荐 / 预标注 | 视频描述、问答、全局语义初标 | https://github.com/LLaVA-VL/LLaVA-NeXT |
| VideoLLaMA2 | 开源视频音频语言模型 | 2025-01-23 | 辅助 | 视频问答、音频理解研究参考 | https://github.com/DAMO-NLP-SG/VideoLLaMA2 |

注意：

- 通用多模态大模型适合“理解”和“解释”，不适合作为最终时空标注器。
- 若需要 bbox / mask / 精确时间戳，应接专用检测、分割、跟踪、diarization 模型。

## 7. 推荐最小可用方案

### 7.1 舞蹈 motion 配对音频

主线工具：

主线工具：[ffmpeg](https://ffmpeg.org/) -> [UVR](https://github.com/Anjok07/ultimatevocalremovergui) / [Spleeter](https://github.com/deezer/spleeter) / [Demucs](https://github.com/facebookresearch/demucs) -> [librosa](https://github.com/librosa/librosa) / [madmom](https://github.com/CPJKU/madmom) / [aubio](https://github.com/aubio/aubio) -> [BEATs](https://github.com/microsoft/unilm/tree/master/beats) / [PANNs](https://github.com/qiuqiangkong/audioset_tagging_cnn) -> metadata 导出。

最小输出：

| 输出 | 用途 |
|---|---|
| `mixed_clean.wav` | 统一格式后的原始混音，保留完整条件信号。 |
| `music.wav` | 分离后的音乐轨，作为舞蹈 motion 的主条件。 |
| `vocal.wav` | 分离后的人声轨，用于判断是否有人声干扰或口播。 |
| `beat_times.json` | 节拍时间，用于动作节奏对齐。 |
| `audio_events.json` | 掌声、脚步、环境声、噪声等事件。 |
| `quality.json` | 音频质量、分离 artifact、静音、爆音、音画同步状态。 |

### 7.2 说话 / 多人说话 motion 配对音频

主线工具：

主线工具：[ffmpeg](https://ffmpeg.org/) -> [DeepFilterNet](https://github.com/Rikorose/DeepFilterNet) / [ClearerVoice-Studio](https://github.com/modelscope/ClearerVoice-Studio) -> [WhisperX](https://github.com/m-bain/whisperX) / [OpenAI Speech-to-Text](https://developers.openai.com/api/docs/guides/audio) / [Deepgram](https://developers.deepgram.com/docs/diarization) / [AssemblyAI](https://www.assemblyai.com/docs/pre-recorded-audio/label-speakers) -> [pyannote.audio](https://github.com/pyannote/pyannote-audio) -> [SyncNet](https://github.com/joonson/syncnet_python) / [Light-ASD](https://github.com/Junhua-Liao/Light-ASD) -> metadata 导出。

最小输出：

| 输出 | 用途 |
|---|---|
| `speech_clean.wav` | 清洗后的语音轨。 |
| `transcript.json` | 句级文本和时间戳。 |
| `words.json` | 词级时间戳，用于细粒度 gesture / face motion 对齐。 |
| `speakers.json` | speaker diarization 结果，多人说话必需。 |
| `sync.json` | 唇音同步或音画 offset 质检结果。 |
| `quality.json` | 噪声、混响、重叠说话、背景音乐干扰、低置信度片段。 |

### 7.3 统一 metadata schema

```json
{
  "clip_id": "sample_000001",
  "video_path": "video/sample_000001.mp4",
  "motion_path": "motion/sample_000001.npz",
  "audio": {
    "mixed_clean": "audio/sample_000001/mixed_clean.wav",
    "music": "audio/sample_000001/music.wav",
    "vocal": "audio/sample_000001/vocal.wav",
    "speech_clean": "audio/sample_000001/speech_clean.wav"
  },
  "time_range": {
    "start": 12.0,
    "end": 18.0
  },
  "music_features": {
    "tempo": 120.0,
    "beat_times": [0.12, 0.62, 1.12],
    "onset_times": [0.05, 0.31, 0.88]
  },
  "speech": {
    "speaker_id": "SPEAKER_00",
    "utterance": "example text",
    "word_timestamps": []
  },
  "events": [
    {
      "label": "applause",
      "start": 2.1,
      "end": 3.4,
      "confidence": 0.82
    }
  ],
  "quality_flags": ["music_overlap", "low_snr"]
}
```

## 8. 不建议作为主依赖的项目或用法

| 名称 | 原因 | 可保留用途 |
|---|---|---|
| Demucs | GitHub 仓库已归档，最近推送 2024-04-24 | 音乐源分离基线；生产中建议评估 UVR / Spleeter / 其他维护中实现 |
| AV-HuBERT | GitHub 仓库已归档，最近推送 2023-12-07 | 语音-视觉表征研究基线 |
| EZ-VSL | 最近推送 2022-10-02，维护偏旧 | 经典声源定位参考 |
| LoCoNet-ASD | 公开代码最近推送 2023-05-01 | ASD 论文复现参考 |
| SPELL | 最近推送 2023-10-29，社区较小 | ASD 长时空图方法参考 |
| 只用 Gemini / GPT / Qwen 做全部标注 | 不能稳定产出帧级 bbox、mask、字词级时间戳 | 预标注、摘要、规则检查、质检解释 |
| 只用 Whisper / ASR 做说话人定位 | ASR 不知道画面中人脸位置 | 字幕、转写、词级时间戳 |

## 9. 选型建议

1. 舞蹈 motion 数据优先建设 `music.wav + beat_times + onset_times + quality_flags`，再扩展人声和事件标签。
2. 说话 motion 数据优先建设 `speech_clean.wav + word_timestamps + speaker_id + sync_score`，再扩展情感和说话风格。
3. 混合音频不要只保留单一路径；建议同时保留 `mixed_clean`、`music`、`vocal`、`speech_clean`，便于后续训练和消融。
4. 通用多模态大模型适合做摘要、异常解释和人工复核辅助，不作为最终音频切分、节拍、diarization 或同步评分来源。
5. 每个 clip 都应带 `quality_flags`，低质样本可以进入弱监督或鲁棒性训练，但不能和高质量配对样本混用。

## 10. 参考链接

- librosa：https://github.com/librosa/librosa
- madmom：https://github.com/CPJKU/madmom
- aubio：https://github.com/aubio/aubio
- pyAudioAnalysis：https://github.com/tyiannak/pyAudioAnalysis
- DeepFilterNet：https://github.com/Rikorose/DeepFilterNet
- ClearerVoice-Studio：https://github.com/modelscope/ClearerVoice-Studio
- Ultimate Vocal Remover：https://github.com/Anjok07/ultimatevocalremovergui
- Spleeter：https://github.com/deezer/spleeter
- Demucs：https://github.com/facebookresearch/demucs
- AudioCraft：https://github.com/facebookresearch/audiocraft
- pyannote.audio：https://github.com/pyannote/pyannote-audio
- WhisperX：https://github.com/m-bain/whisperX
- Whisper：https://github.com/openai/whisper
- TalkNet-ASD：https://github.com/TaoRuijie/TalkNet-ASD
- Light-ASD：https://github.com/Junhua-Liao/Light-ASD
- SyncNet：https://github.com/joonson/syncnet_python
- OpenFace：https://github.com/TadasBaltrusaitis/OpenFace
- openSMILE：https://github.com/audeering/opensmile
- BEATs：https://github.com/microsoft/unilm/tree/master/beats
- PANNs：https://github.com/qiuqiangkong/audioset_tagging_cnn
- CLAP：https://github.com/LAION-AI/CLAP
- Moment-DETR：https://github.com/jayleicn/moment_detr
- TimeChat：https://github.com/RenShuhuai-Andy/TimeChat
- AVSBench：https://github.com/OpenNLPLab/AVSBench
- AVSegFormer：https://github.com/vvvb-github/AVSegFormer
- MMAction2：https://github.com/open-mmlab/mmaction2
- PySlowFast：https://github.com/facebookresearch/SlowFast
- InternVideo：https://github.com/OpenGVLab/InternVideo
- RTFM：https://github.com/tianyu0207/RTFM
- VadCLIP：https://github.com/nwpu-zxr/VadCLIP
- audio-visual-forensics：https://github.com/cfeng16/audio-visual-forensics
- Gemini video understanding：https://ai.google.dev/gemini-api/docs/video-understanding
- OpenAI audio docs：https://developers.openai.com/api/docs/guides/audio
- Azure AI Video Indexer：https://learn.microsoft.com/en-us/azure/azure-video-indexer/video-indexer-overview
- Hume AI Expression Measurement：https://dev.hume.ai/docs/expression-measurement/overview
- Deepgram diarization：https://developers.deepgram.com/docs/diarization
- AssemblyAI speaker diarization：https://www.assemblyai.com/docs/pre-recorded-audio/label-speakers
