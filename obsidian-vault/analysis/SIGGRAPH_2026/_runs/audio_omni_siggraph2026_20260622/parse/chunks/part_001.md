<!-- part 1/13 chars 0-7686 -->

# Audio-Omni: Extending Multi-modal Understanding to Versatile Audio Generation and Editing

ZEYUE TIAN, Hong Kong University of Science and Technology, Hong Kong SAR, China

BINXIN YANG, WeChat Vision, Tencent Inc, China

ZHAOYANG LIU, Hong Kong University of Science and Technology, Hong Kong SAR, China

JIEXUAN ZHANG, Peking University, Beijing, China

RUIBIN YUAN, Hong Kong University of Science and Technology, Hong Kong SAR, China

HUBERY YIN, WeChat Vision, Tencent Inc, China

QIFENG CHEN, Hong Kong University of Science and Technology, Hong Kong SAR, China

CHEN LI∗, WeChat Vision, Tencent Inc, China

JING LYU, WeChat Vision, Tencent Inc, China

WEI XUE∗, Hong Kong University of Science and Technology, Hong Kong SAR, China

YIKE GUO, Hong Kong University of Science and Technology, Hong Kong SAR, China

![](images/da7a856def93e831ddbc3f9a1b328d6a5f5df29d255eccaa4ea109720a763f77.jpg)  
Fig. 1. An overview of the Audio-Omni framework and its capabilities. (Top) Our decoupled architecture connects a frozen MLLM for understanding with a trainable DiT for audio synthesis via a feature projector. (Middle) A showcase of the model’s unified capabilities across understanding, generation, and editing. (Bottom) A demonstration of remarkable emergent abilities inherited from the MLLM.

Recent progress in multimodal models has spurred rapid advances in audio understanding, generation, and editing. However, these capabilities are typically addressed by specialized models, leaving the development of a truly unified framework that can seamlessly integrate all three tasks underexplored. While some pioneering works have explored unifying audio understanding and generation, they often remain confined to specific domains. To address this, we introduce Audio-Omni, the first end-to-end framework to unify generation and editing across general sound, music, and speech domains, with integrated multi-modal understanding capabilities. Our architecture synergizes a frozen Multimodal Large Language Model for high-level reasoning with a trainable Diffusion Transformer for high-fidelity synthesis. To overcome the critical data scarcity in audio editing, we construct AudioEdit, a new large-scale dataset comprising over one million meticulously curated

editing pairs. Extensive experiments demonstrate that Audio-Omni achieves state-of-the-art performance across a suite of benchmarks, outperforming prior unified approaches while achieving performance on par with or superior to specialized expert models. Beyond its core capabilities, Audio-Omni exhibits remarkable inherited capabilities, including knowledge-augmented reasoning generation, in-context generation, and zero-shot cross-lingual control for audio generation, highlighting a promising direction toward universal generative audio intelligence. The code, model, and dataset will be publicly released on https://zeyuet.github.io/Audio-Omni.

CCS Concepts: • Computing methodologies → Artificial intelligence;   
Machine learning; Computer graphics.

Additional Key Words and Phrases: Audio generation, multimodal learning, diffusion models, unified models, audio editing

## 1 Introduction

Recent advances in multimodal learning have spurred a trend toward unified frameworks that integrate both understanding and generation within a single model, achieving significant progress in visual domains such as image [Chen et al. 2025b; Jiao et al. 2025; Ma et al. 2025; Pan et al. 2025] and video [Liu et al. 2025a; Wei et al. 2025] understanding and generation. However, the audio domain remains comparatively underexplored.

Unlike the visual modality, audio encompasses three distinct domains with significant distributional disparities: general sounds, music, and speech. While some efforts have been made to unify audio understanding and generation, they remain confined to specific domains, such as speech-centric models [AI et al. 2025; An et al. 2024] or those limited to general audio and music [Liu et al. 2024a; Tian et al. 2025b], failing to cover the full audio spectrum. Other systems rely on tool-based integration [Huang et al. 2024a], which lacks end-to-end optimization. Meanwhile, existing audio editing models [Manor and Michaeli 2024; Wang et al. 2023b] are designed exclusively for editing and cannot be extended to understanding or generation, leaving the unification of all three capabilities an open challenge.

To address these limitations, we introduce Audio-Omni, a framework that unifies audio understanding, generation, and editing across the full spectrum of audio domains. We adopt a decoupled design: a frozen Multimodal Large Language Model (MLLM) serves as the reasoning core, while a trainable Diffusion Transformer (DiT) handles generation and editing. Keeping the MLLM frozen preserves its rich multimodal knowledge, which in turn empowers the generative module with capabilities beyond its explicit training scope. To effectively bridge the two components, we design a hybrid conditioning mechanism that disentangles inputs into two complementary streams: a High-Level Semantic stream, combining MLLM features and text embeddings for speech synthesis, injected via cross-attention to provide instructional guidance; and a Low-Level Signal stream, fusing mel-spectrogram and video sync features, concatenated with the input noise for precise temporal control. This separation is key to mastering the diverse requirements of sound, music, and speech within a single framework.

Training a unified model of this scope demands a comprehensive and diverse dataset. A critical barrier to progress in instructionguided audio editing is the absence of any large-scale, publicly available dataset. To address this gap, we meticulously design a pipeline to construct AudioEdit, a large-scale, high-quality dataset for this task. Created through a systematic pipeline combining realworld data mining with scalable programmatic synthesis, AudioEdit contains over 1M rigorously curated samples covering editing tasks including addition, removal, extraction, and style transfer. Training on this dataset enables our model with its robust editing capabilities.

Extensive experiments validate the effectiveness of our unified design. Audio-Omni outperforms prior unified models across understanding, generation, and editing tasks, while matching or surpassing specialized expert models on several tasks. Beyond these core results, the generative module naturally inherits capabilities from the frozen MLLM, including world knowledge for reasoning-based generation, in-context learning for audio-conditioned synthesis, and multilingual understanding for cross-lingual control.

In summary, our main contributions are as follows:

• We propose Audio-Omni, the first unified framework for audio understanding, generation, and editing across general sound, music, and speech. At its core is a decoupled architecture that bridges a frozen MLLM with a trainable DiT, guided by a hybrid conditioning mechanism to disentangle semantic and signal-level control.

• We introduce AudioEdit, a large-scale, high-quality dataset with a meticulous pipeline for instruction-guided audio editing, encompassing a wide range of tasks to facilitate future research in this area.

• Extensive experiments demonstrate that Audio-Omni outperforms prior unified models and achieves competitive or superior results compared to specialized expert models across a broad range of tasks.

• Furthermore, Audio-Omni exhibits remarkable inherited capabilities for generation, such as knowledge-augmented generation and cross-lingual control, highlighting a path toward intelligent and versatile generative audio systems.