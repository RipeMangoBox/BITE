<!-- part 11/13 chars 59628-66230 -->

Yuan, Hanfeng Lin, Shuyue Guo, Ge Zhang, Jiahao Pan, Yongyi Zang, Haohe Liu, Yiming Liang, Wenye Ma, Xingjian Du, et al. 2025. Yue: Scaling open foundation models for long-form music generation. arXiv preprint arXiv:2503.08638 (2025).

Ruibin Yuan, Hanfeng Lin, Yi Wang, Zeyue Tian, Shangda Wu, Tianhao Shen, Ge Zhang, Yuhang Wu, Cong Liu, Ziya Zhou, et al. 2024. Chatmusician: Understanding and generating music intrinsically with llm. arXiv preprint arXiv:2402.16153 (2024).

Jun Zhan, Junqi Dai, Jiasheng Ye, Yunhua Zhou, Dong Zhang, Zhigeng Liu, Xin Zhang, Ruibin Yuan, Ge Zhang, Linyang Li, et al. 2024. Anygpt: Unified multimodal llm with discrete sequence modeling. In Proceedings of the 62nd Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers). 9637–9662.

## 1 Appendix

Table A1. Ablation study on different encoders. We evaluate the impact of different encoders for text-to-audio (T2A) and video-to-audio (V2A) tasks.
<table><tr><td>Task</td><td>Encoder</td><td>KL↓</td><td>IS↑</td><td>FD↓</td><td>FAD↓</td></tr><tr><td rowspan="3">T2A</td><td>T5</td><td>1.51</td><td>11.27</td><td>15.78</td><td>2.75</td></tr><tr><td>CLAP</td><td>1.81</td><td>9.64</td><td>16.58</td><td>1.84</td></tr><tr><td>Qwen</td><td>1.25</td><td>11.65</td><td>12.21</td><td>2.14</td></tr><tr><td rowspan="3">V2A</td><td>CLIP</td><td>2.20</td><td>7.42</td><td>12.21</td><td>2.80</td></tr><tr><td>VideoMAE</td><td>2.29</td><td>6.58</td><td>14.72</td><td>3.06</td></tr><tr><td>Qwen</td><td>2.00</td><td>8.08</td><td>8.50</td><td>2.23</td></tr></table>

Table A2. Zero-shot cross-lingual text-to-audio generation results.
<table><tr><td>Method</td><td>Language</td><td>KL↓</td><td>IS↑</td><td>FD↓</td><td>FAD↓</td></tr><tr><td>Tango2 [Majumder et al. 2024]</td><td>EN</td><td>1.11</td><td>10.37</td><td>12.22</td><td>3.20</td></tr><tr><td>AudioX [Tian et al. 2025a]</td><td>EN</td><td>1.34</td><td>12.09</td><td>11.83</td><td>1.86</td></tr><tr><td>MMAudio Cheng et al. 2025]</td><td>EN</td><td>1.35</td><td>12.03</td><td>12.63</td><td>4.71</td></tr><tr><td>Stable-Audio-Open [Evans et al. 2024]</td><td>EN</td><td>2.01</td><td>10.37</td><td>29.01</td><td>3.15</td></tr><tr><td></td><td>EN</td><td>1.15</td><td>11.64</td><td>11.97</td><td>1.86</td></tr><tr><td></td><td>CN</td><td>1.65</td><td>11.10</td><td>15.05</td><td>2.26</td></tr><tr><td>Audio-Omni</td><td>ES</td><td>2.36</td><td>9.16</td><td>25.26</td><td>4.32</td></tr><tr><td></td><td>DE</td><td>2.39</td><td>9.13</td><td>23.51</td><td>2.92</td></tr><tr><td></td><td>FR</td><td>2.47</td><td>8.80</td><td>28.63</td><td>4.21</td></tr><tr><td></td><td>JP</td><td>2.27</td><td>8.67</td><td>19.82</td><td>3.13</td></tr></table>

This section includes dataset details, zero-shot cross-lingual textto-audio generation, and ablation studies.

## 1.1 Dataset Details

Our model is trained on a mixture of diverse datasets, as detailed in Table A4. The data composition for each task is as follows:

Text-to-Audio (T2A): Approximately 1.4k hours, sourced from AudioCaps [Kim et al. 2019], WavCaps [Mei et al. 2024], AudioSet-Caps [Bai et al. 2025], and AudioTime [Xie et al. 2025b].

Video-to-Audio (V2A): Approximately 700 hours, sourced from VGGSound [Chen et al. 2020] and the AudioSet Strong [Hershey et al. 2021] benchmark.

Text-to-Music (T2M): Approximately 17k hours, combining data from V2M [Tian et al. 2025c] and MUCaps [Liu et al. 2024a].

Video-to-Music (V2M): Approximately 16k hours, sourced entirely from the V2M [Tian et al. 2025c] dataset.

Speech: Approximately 6k hours, using the English subset of Audio-FLAN [Xue et al. 2025].

Audio Editing: Approximately 3k hours from our internally constructed AudioEdit dataset, with the methodology detailed in Section 3.

Style-Transfer Keyword Generation. For style-transfer data construction, we prompt Gemini 2.5 Pro with each audio’s original keyword to generate semantically related but stylistically different target keywords. The prompt template is: “Given audio with keyword ‘[original\_keyword]’, generate a related but different keyword for style transfer.” Generated candidates are filtered by CLAP before guiding ZETA for style transformation.

## 1.2 More Comparison Results

Detailed Results on Audio Editing Tasks. Table A3 presents detailed performance on the four primary audio editing tasks using FAD and LSD on our AudioEdit benchmark. Audio-Omni consistently achieves SOTA performance across all individual tasks.

Detailed Results on Generation Tasks. We provide a comprehensive breakdown of our model’s performance across all generation tasks with multiple evaluation metrics in Table A5. The table presents results on KL divergence, Inception Score (IS), Fréchet Distance (FD), and Fréchet Audio Distance (FAD) for Text-to-Audio (T2A), Text-to-Music (T2M), Video-to-Audio (V2A), Video-to-Music (V2M), and Text-to-Speech (TTS) tasks.

Zero-shot Cross-lingual Text-to-Audio Generation. A remarkable inherited capability of our framework is its zero-shot crosslingual generation, inherited directly from the frozen MLLM’s multilingual understanding. To evaluate this, we translated the AudioCaps test set into Chinese (CN), Spanish (ES), German (DE), French (FR), and Japanese (JP) using Gemini. As shown in Table A2, Audio-Omni maintains strong performance across all languages despite being trained almost exclusively on English. Notably, the quality of audio generated from non-English prompts (e.g., Chinese) is comparable to strong, English-only specialist models. This result validates that our decoupled architecture effectively transfers the MLLM’s linguistic capabilities to the synthesis task, bridging the language gap in generative audio.

## 1.3 More Ablation Studies

Effect of the Unified MLLM Encoder. To validate our choice of the understanding module, we compare our frozen Qwen-Omni-3B (Qwen) MLLM against specialized single-modality encoders. For T2A, evaluated on AudioCaps [Kim et al. 2019], we replace it with text encoders (T5 [Raffel et al. 2020], CLAP [Elizalde et al. 2023]). For V2A, evaluated on VGGSound [Chen et al. 2020], we compare against vision encoders (CLIP [Radford et al. 2021], VideoMAE [Tong et al. 2022]). As shown in Table A1, the results consistently demonstrate the superiority of using a unified MLLM, which achieves significantly better performance across all metrics in both tasks. We attribute this to the MLLM’s richer semantic understanding and, more importantly, its inherent ability to process multimodal contexts jointly, capturing cross-modal relationships that specialized encoders inherently miss.