# Cubic Discrete Difusion: Discrete Visual Generation on High-Dimensional Representation Tokens

Yuqing Wang1 Chuofan Ma1 Zhijie Lin2† Yao Teng1 Lijun Yu3 Shuai Wang4 Jiaming Han5 Jiashi Feng2 Yi Jiang2 Xihui Liul \* lUniversity of Hong Kong ²ByteDance Seed3Carnegie Mellon University 4Nanjing University 5The Chinese University of Hong Kong

## Abstract

Visual generation with discrete tokens has gained significant attention as it enables a unified token prediction paradigm shared with language models,promising seamless multimodal architectures. However, current discrete generation methods remain limited to low-dimensional latent tokens (typically 8-32 dims)，sacrificing the semantic richness essential for understanding.While highdimensional pretrained representations (768-1024 dims) could bridge this gap,their discrete generation poses fundamental challenges.In thispaper,we present Cubic Discrete Diffusion (CubiD),the first discrete generation model forhigh-dimensional representations.CubiD performs fine-grained masking throughout the high-dimensional discrete representation—any dimension at any position can bemasked and predicted from partial observations.This enables themodel to learn rich correlations both within andacrossspatial positions,with the numberofgeneration stepsfixedatT regardlessoffeaturedimensionality,where T<hwd.On ImageNet-256,CubiD achieves state-of-theart discrete generation with strong scaling behavior from 900Mto 3.7B parameters.Crucially,wevalidate that these discretized tokens preserve original representation capabilities,demonstrating that the same discrete tokens can effectively serve both understanding and generation tasks. We hope thisworkwill inspire future research toward unified multimodal architectures. Code is available at: ht tps : //github.com/YuqingWangl029/CubiD.

## 1. Introduction

The pursuit of unified multimodal modeling [6,38,46] requires both language and vision to operate on semantically meaningful tokens. While language models have long benefited from semantic tokens that naturally support both understanding and generation,visual models remain fragmented—using high-dimensional semantic features for understanding but low-dimensional compressed tokens [10,16,41,47,54] for generation．Recent advances [5,37,53] have shown that high-dimensional representation features (768-1O24 dimensions） can achieve high-quality reconstruction,offering a path forward.For discrete generative models [2,36,39],which share the token-based paradigm with language models,adopting such high-dimensional representation tokens is particularly compelling,as it would allow visual generation to leverage the same semantic richness that has proven essential for understanding,potentially enabling more coherent unified architectures.

![](auto/images/rf_full_regions/page_001_Figure_1_c1621dbf36eb.jpg)  
(b) High-dim Token Generation

Figure 1.Comparison of discrete visual generation approaches.(a) Low-dimensional token generation:Both methods operate at the spatial level—autoregressive requires h × w sequential steps,while discrete diffusion achieves parallel generation in T<h ×w iterations.(b)High-dimensional token generation:Autoregressive becomes intractable (h X w X d steps),and standard discrete diffusion cannot model intra-position dependencies. Our Cubic Discrete Diffusion performs fine-grained masking across the entire 3D tensor—any dimension at any position can be masked and predicted independently-enabling effcient generation in T< h ×w ×d iterations while capturing both spatial and dimensional correlations.

![](images/b6415517082ec51d32360678bde13fe75befb4f79bb1cb2919b75efbe675fa9c.jpg)  
Figur2.Generatedsamples fromCubiD.Clas-conditioal generatioresultsonImageNet256×256usinghigh-dimensionalrepresentation tokens from DINOv2-B encoder,demonstrating fine details and textures across diverse categories.

However,high-dimensional representations pose significant challenges for discrete generative modeling.The first is how to discretize these features while maintaining their representation quality. Traditional Vector Quantization [41] methods that work well in low dimensions （8- 32) fail at 768-1O24 dimensions due to the curse of dimensionality—data points become sparsely distributed, making clustering ineffective,and the codebook size required for adequate coverage grows exponentially. The quantized features inevitably drift from the original representations,corrupting the semantic information essential for understanding.Dimension-wise quantization [43] offers a promising solution.By treating each dimension independently rather than quantizing entire vectors jointly,it sidesteps the clustering problems in high-dimensional spaces.As a trainingfree method, it can be directly applied to frozen pretrained features,making discretization tractable at 768+ dimensions.We validate this approach on multimodal understanding tasks:dimension-wise quantized features achieve nearly identical performance to continuous features,while VQ suffers substantial degradation (Table 3). This result confirms that properly discretized high-dimensional tokens preserve semantic quality for understanding tasks,establishing them as viable unified representations.

The more fundamental challenge lies in modeling such high-dimensional discrete tokens.While dimension-wise quantization successfully preserves semantic quality, the resulting representation contains h × w × d discrete tokens (196.608 for a typical 16 ×16× 768 configuration). As illustrated in Figure 1(b),direct sequential generation requires O(hwd) steps,which is intractable,while standard discrete diffusion methods cannot capture the dependencies across dimensions within each spatial position.To make this problem tractable,we need a method that avoids sequential bottlenecks while preserving the rich dependency structure across both spatial and dimensional axes.We observe that the h×w ×d tensor has inherent multi-dimensional structure that can be exploited—rather than treating spatial positions as atomic units or requiring sequential generation of all dimensions,we can break these rigid boundaries and operate flexibly across the entire tensor.

We propose Cubic Discrete Diffusion (CubiD)，a masked diffusion method [1,3,26] for high-dimensional discrete generation. Our key insight is to perform finegrained masking across the three-dimensional h × w × d tensor.Unlike existing methods [3] that mask entire spatial positions,our approach treats this tensor as a unified cubic space where any subset of dimensions at any position can be masked and predicted from partial observations.This allows the model to learn complex dependencies both within and across spatial locations.As shown in Figure 1(b),during generation,CubiD starts froma fully masked tensor and iteratively refines it through progressive unmasking,randomly selecting tokens across the entire tensor to unmask at each step until reaching the complete representation.

This approach offers two main advantages.First,it effectively models complex dependencies in high-dimensional tensors—learning both intra-position correlations (how dimensions relate within a spatial location) and inter-position patterns (how features propagate spatially)—through bidirectional attention over partially observed values.Second,it decouples generation complexity from dimensionality:unlike autoregressive methods that scale with O(hwd), our iterative refinement requires a fixed number of steps Tregardless of feature dimensionality,benefiting from the semantic redundancy inherent in high-dimensional representations.By transforming an intractable sequential process into hundreds of parallel iterations,CubiD makes high-dimensional discrete generation computationally feasible while maintaining the modeling capacity necessary for

high-quality synthesis.

Extensive experiments validate our approach．We first verify that dimension-wise quantization preserves both understanding and reconstruction capabilities of the original continuous representations.In ablation studies,we compare our fine-grained cubic masking against alternative strategies: treating spatial positions or dimensions as groups significantly degrades performance,confirming the necessity of element-wise masking across the 3D tensor. The method also exhibits strong scaling behavior from 90oM to 3.7B parameters and generalizes well across different representation encoders (DINOv2 [3O] and SigLIP2 [4O]). On ImageNet 256x256 [8],CubiD achieves a competitive 1.88 FID score with 768-dimensional discrete tokens,establishing that high-dimensional discrete generation is both feasible and effective.

Our contributions are summarized as follows:

·We demonstrate that proper discretization of highdimensional representation tokens can preserve their original semantic capabilities,establishing the viability of unified discrete representations for both understanding and generation.

·We propose Cubic Discrete Diffusion,a novel method that addresses the fundamental modeling challenge of high-dimensional discrete generation by treating the h × w × d tensor as a unified space with fine-grained masking,making discrete generative models tractable at high dimensionality.

· We achieve state-of-the-art discrete generation results on ImageNet 256x256,with strong scaling behavior from 900M to 3B parameters and generalization across different representation encoders,demonstrating the effectiveness of discrete diffusion for high-dimensional visual generation.

## 2.Related Work

Visual TokenizationVisual tokenization is commonly used to convert images into latent representations that support image reconstruction and generation.In the traditional VAE tokenizers [7,16],an encoder first compresses an image into a low-dimensional continuous latent map (typically with 4-32 dimensions) and then a decoder reconstructs the corresponding image with the latent as input. The encoder and decoder of these tokenizers are jointly trained for the reconstruction task.Building on this framework,discrete tokenizers further quantize each vector from the latent maps into one or several tokens [10,13,28,43,49,51],enabling discrete image generation．More recently,representationbased tokenizers [34,52,53] have emerged.Most of these methods use a frozen pretrained vision foundation model [3O,4O] as the encoder and further train additional adapters to project its outputs into low-dimensional latents. In contrast,RAE [53] directly uses high-dimensional DI-

NOv2 [30] or SigLIP [4O] features as latents (768+ dimensions)without any adaptation,and a specially designed training schedule is applied to these high-dimensional latents to adapt the continuous diffusion models for generation.In this paper,we first transform high-dimensional features from vision foundation models into discrete tokens and then train generative models on those tokens.

Discrete Visual Generation Discrete visual generation performs image generation based on sequences of discrete tokens. Autoregressive models [17,24,31,36, 42, 44, 48] generate tokens sequentially via the next-token prediction paradigm.Although these models can generate high-quality images,they require O(N） generation steps for N tokens, making this paradigm computationally expensive for highresolution images.To improve sampling efficiency,discrete diffusion models [3] have been introduced.Instead of generating tokens sequentially, they generate multiple tokens in parallel, thereby achieving higher efficiency. Like continuous diffusion models,discrete diffusion models also learn to restore corrupted tokens, with corruption defined by absorbing-state [3,26,29,45],uniform[1],or Gaussianlike transitions [1,26].Among these,the absorbing-state transition is the predominant choice due to its strong empirical performance [29]. It corrupts tokens into a special [MASK] state,aligning with representative masked generative models such as BERT[9] and MaskGIT[3]. Existing autoregressive and discrete diffusion models perform well when each image is represented by a small number of discrete tokens derived from low-dimensional latents.However,when representation-based tokenizers produce more tokens per latent,the total token count grows dramatically and existing models become impractical. Therefore,in this work,we extend discrete diffusion models to more efficiently handle tokens derived from high-dimensional latents.

## 3.Method

Our goal is to enable discrete generative modeling of highdimensional representation tokens from frozen pretrained encoders.This requires two steps:discretizing the continuous high-dimensional features,and modeling the resulting discrete token distribution.We frst review the necessary preliminaries:high-dimensional features from pretrained encoders and dimension-wise quantization that enables tractable discretization (Sec.3.1). The core challenge—and our main contribution—lies in modeling the joint distribution of the resulting h × w × d discrete tokens,an exponentially large space where traditional methods fail.We propose Cubic Discrete Diffusion (CubiD), which performs masked prediction across both spatial and dimensional axes simultaneously. By masking and predicting at the dimension level, CubiD captures complex interdimensional dependencies while enabling efcient parallel generation,transforming intractable sequential modeling into practical iterative refinement (Sec. 3.2).

![](images/1eafac52892166386681d533f32eeef3d31b9776144cf80cb53cbe840b7de4d0.jpg)  
Figur 3.OverviewofCubicDiscreteDiffusion.(a)HighdimensionalTokenDiscretizationGivenaninputimage,afrozenrepresentationecoderextractscontiuoustokens,whicaretendiscretizedthroughdimension-wisequantizationintoh××ddiscretetoks. (b)TrainngviaDimension-wiseMaskModeling.Duringtraining,werandomlymasktokensacrosbothspatialanddimensioalaxes ofthe ensor(white:maskedtokens,pnk:visiblegroundtruthtokensothercolors:predictedtokens).Theransformerleastopredict these masked tokens fromthe unmaskedcontext,capturing thecomplexdependencies acrossboth spatialand dimensionalaxes.

## 3.1. Preliminaries

High-dimensional Representation Tokens.Our method operates on features from frozen pretrained vision encoders. Given an input image $\mathbf { x } ~ \in ~ \mathbb { R } ^ { \mathbf { \hat { H } } \times W \times 3 }$ ，apretrained encoder E (e.g.,DINOv2 [30], SigLIP2 [40]) with patch size p produces a feature map $\textbf { z } = \boldsymbol { E } ( \mathbf { x } ) \in \mathbb { R } ^ { h \times w \times d }$ ，where $h \ = \ H / p , \ w \ = \ W / p ,$ and d is the feature dimension (typically 768-1024).These encoders produce semantically rich,high-dimensional features that capture both local details and global semantic structures,in contrast to the low-dimensional compressed spaces (8-32 dims) commonly used in generative modeling.

Dimension-wise Quantization.To discretize these highdimensional features,we adopt dimension-wise quantization [43],which operates directly on frozen encoder features without any retraining.As shown in Figure 3(a),it independently quantizes each continuous value into L discrete levels:

$$
q _ { x , y , i } = \mathrm { Q u a n t i z e } ( z _ { x , y , i } ; L ) ,\tag{1}
$$

where $z _ { x , y , i } \in$ z denotes the i-th dimension at spatial position $( x , y )$ ,and Quantize(-;L) maps continuous values to discrete indices in $\{ 0 , . . . , L - 1 \}$ .Unlike vector quantization which struggles to cover high-dimensional spaces with fixed-size codebooks,this method treats each dimension independently,making it tractable even for 768-dimensional features. The resulting $h \times w \times d$ discrete tokens maintain their tensor structure.More details can be found in [43]. Through experiments on understanding tasks,we verify that this discretization preserves the semantic quality of the original representations (Table 3).

## 3.2. Cubic Discrete Diffusion

The discretization process,although preserving continuouslevel quality,yields h ×w ×d discrete tokens.For example, it takes 196,608 tokens for a typical 16x16x768 configuration.The real challenge lies in how to model this massive token space: direct autoregressive generation would require O(hwd) steps,while naive parallel methods fail to capture the complex dependencies within this structured tensor.

Masking Across Spatial and Dimensional Axes.In this paper, we propose Cubic Discrete Diffusion (CubiD),which follows the discrete diffusion paradigm by treating generation as iterative denoising of masked tokens.Unlike traditional discrete diffusion methods like MaskGIT [3] that mask entire spatial positions,CubiD performs fine-grained masking at the dimension level—treating the $h \times w \times d$ tensor as a unified modeling space where any subset of dimensions can be masked and predicted from the remaining visible context.This enables the model to capture rich dependencies both within and across spatial locations.

Given discrete tokens $\mathbf { q } \in \{ 0 , . . . , L - 1 \} ^ { h \times w \times d }$ from dimension-wise quantization, CubiD learns to predict randomly masked tokens from visible ones．As illustrated in Figure 3(b),during training,we apply a binary mask $\mathbf { M } \in \{ 0 , 1 \} ^ { h \times w \times d }$ where each element is independently and randomly masked.We first sample a masking ratio r from a truncated Gaussian distribution:

$$
r \sim \mathrm { T r u n c N o r m } ( \mu = 1 . 0 , \sigma , [ 0 , 1 . 0 ] )\tag{2}
$$

where $\mu = 1 . 0$ is the mean and o is the standard deviation, with the distribution truncated to the range [O,1]. Then, we randomlyselect $\lfloor r \times h \times w \times d \rfloor$ positions to mask across the entire tensor. This distribution covers the fullrange [O,1] to ensure consistency with inference,which progresses from fully masked to fully unmasked.With $\mu = 1 . 0$ ,itbiases toward aggressive masking,encouraging the model to learn robust predictions from minimal context.Masked positions are replaced with a learnable [MASK] token,and the model is trained to predict the original discrete token categories at these positions through cross-entropy loss:

![](images/81cc91a110464149186ceac2ffd68c0691231fc6e3f1adeee405b9e1f4af80d9.jpg)  
Figure4.InferenceprocessofCubiD.Toprowshowsthelatenttokenstate(white:masked,pink:unmasked),botomrowshows correspondingdecodedimages.uringgeneration,CubiDstartsfromafullyasedtensor(O%)andprogressvelyunmasktkensuntil reachingacompleteimage(O0%).Atachiteration,themodelpredictsallmaskedtokensinparalelandrandomlyunmasksasubset. The percentagesshowtheprogessthroughgenerationsteps.Generationtakeshundredsofterationsregardlessoffeaturedimensioality makingigh-dmensioaletegneratiomputatioallfeasibl.Thsualizatidemostratesacoarse-tfnegeeratiooces, where early iterations establish overall structure and later iterations refine details.

$$
\mathcal { L } = - \mathbb { E } _ { \mathbf { q } , \mathbf { M } } \left[ \sum _ { i \in \mathbf { M } } \log p ( q _ { i } | \mathbf { q } _ { \bar { \mathbf { M } } } ) \right]\tag{3}
$$

where $\mathbf { q } _ { \mathrm { M } }$ denotes the visible tokens that provide context for prediction.

This fine-grained masking allows the model to observe partial dimensions at each location,learning how different dimensions jointly encode information and constrain each other's values.Through bidirectional attention over the partially masked tensor, the model discovers complex dependency patterns both within and across spatial positions without being constrained to predefined factorization orders.

Inference.During inference,CubiD generates images through iterative refinement starting from a fully masked tensor.As illustrated in Figure 4,the model begins with all tokens masked (O%）and progressively unmasks them until reaching a complete image (loo%).At each iteration t, the model predicts all masked tokens simultaneously and unmasks a subset randomly. Motivated by MaskGIT [3], the number of tokens to unmask follows a cosine schedule.The schedule ensures a coarse-to-fine generation process where early iterations establish overall structure and later iterations refine details. Crucially, the parallel nature of our approach means generation requires only O(T) iterations—typically hundreds of steps-regardless of the tensor dimensionality d,making high-dimensional discrete generation computationally feasible.

Model Architecture.CubiD employs a standard Transformer architecture with bidirectional attention.As shown in Figure 3(b),each spatial position,comprising d tokens,is treated as a single token for the transformer model, thereby preserving the spatial structure while enabling fine-grained predictions. Specifically, for each spatial position,we dequantize its d discrete tokens back to continuous scalars (with ［MASK] tokens mapped to a learnable value） and concatenate them into a d-dimensional feature vector. This results in a sequence of h × w tokens,each with dimensionality d. The Transformer processes this sequence through bidirectional attention,with the sequence length remaining fixed at h × w regardless of feature dimensionality. Each output token from the Transformer is passed through an MLP-based prediction head that produces d × L logits,enabling simultaneous prediction of all d dimensions at that spatial position. This design decouples computational complexity from feature dimensionality—the Transformer's sequence length depends only on spatial resolution, not on d.

Table 1.Model sizes and architecture configurations of CubiD.
<table><tr><td>Model</td><td>Hidden Dim</td><td>Blocks</td><td>Parameters</td></tr><tr><td>CubiD-L</td><td>1536</td><td>32</td><td>946M</td></tr><tr><td>CubiD-XL</td><td>1920</td><td>32</td><td>1.4B</td></tr><tr><td>CubiD-XXL</td><td>3072</td><td>32</td><td>3.7B</td></tr></table>

## 4. Experiments

## 4.1.Implementation Details

Representation Encoders.We use frozen DINOv2-B [30] and SigLIP2-B [4O] as representation encoders,both producing 16x16x768 feature maps. DINOv2-B processes 224×224 images while SigLIP2-B takes 256x256 inputs. For reconstruction,we adopt decoders from [53] that decode 256x256 images.Unless otherwise specified,we use DINOv2-B as our default encoder.

Model Configurations.We evaluate three model sizes as shown in Table 1.All models use 16 attention heads with MLP ratio of 4. Unless otherwise specified,we report results using CubiD-L.

Training and Inference. Models are trained on ImageNet [8] at 256x256 resolution. We use AdamW optimizer with learning rate $5 \times 1 0 ^ { - 5 }$ ,cosine schedule,and 0.05 weight decay.Gradient clipping is applied at norm 3.0.Ablation studies use 15O epochs while final results are reported at 8OO epochs. Generation employs iterative unmasking with cosine scheduling for mask ratios,using T = 256 steps for ablation studies.

![](auto/images/rf_full_regions/page_006_Table_2_18451403a218.jpg)
Table 2. Effect of quantization levels on reconstruction quality. Both encoders achieve continuous-level performance with appropriate quantization levels (L=8 for DINOv2,L=16 for SigLIP2).
<table><tr><td colspan="3">DINOv2 [30] L rFID↓ IS↑</td></tr><tr><td>Continuous</td><td></td><td>-0.57 226.9</td></tr><tr><td>Discrete</td><td></td><td>21.38 206.1 40.70 221.1</td></tr><tr><td></td><td>8 0.57 226.8</td><td></td></tr><tr><td></td><td></td><td></td></tr><tr><td></td><td></td><td>16 0.57 226.9</td></tr></table>

<table><tr><td colspan="2">SigLIP2 [40] L rFID↓IS↑</td></tr><tr><td>Continuous</td><td>-0.69 217.5</td></tr><tr><td>Discrete</td><td>41.54 193.8 8 0.92 210.7</td></tr><tr><td></td><td>16 0.69 216.2</td></tr><tr><td></td><td>32 0.69 217.5</td></tr><tr><td></td><td></td></tr></table>

Table 3.Understanding performance onLLaVA benchmarks with different quantization methods.Evaluation using SigLIP2 features.VQ:vector quantization,DQ:dimension-wise quantization．DQ maintains continuous-level performance while VQ shows significant degradation.
<table><tr><td>Tokenizer</td><td>Type</td><td>GQA</td><td>TextVQA</td><td>POPE</td><td>MME</td></tr><tr><td>SigLIP2</td><td>Continuous</td><td>63.2</td><td>59.6</td><td>85.4</td><td>1484</td></tr><tr><td>SigLIP2-VQ</td><td>Discrete</td><td>54.9</td><td>45.6</td><td>81.2</td><td>1189</td></tr><tr><td>SigLIP2-DQ</td><td>Discrete</td><td>63.1</td><td>59.8</td><td>85.0</td><td>1480</td></tr></table>

Evaluation Metrics. We evaluate generation quality using Fréchet Inception Distance (FID) [14] and Inception Score (IS)[33] on ImageNet 256x256.Precision and Recall metrics [18] are reported as additional references for sample quality and diversity.

## 4.2. Studies of Discretization

In this section,we study the effects of dimension-wise quantization on high-dimensional features through reconstruction and understanding experiments.

Reconstruction Quality.We evaluate dimension-wise quantization on two representation encoders,DINOv2- B [30] and SigLIP2-B [4O],using their continuous reconstruction results as baselines.As shown in Table 2,discretized tokens can preserve the original continuous performance with appropriate quantization levels. Specifically, DINOv2-B achieves baseline rFID(0.57) at L = 8,while SigLIP2-B reaches its baseline (rFID=O.69)at L= 16.We adopt these settings for all subsequent experiments.The different optimal quantization levels likely reflect distinct feature distributions between encoders.

Understanding Quality. To validate whether discrete tokens maintain the understanding capabilities of continuous representations,we evaluate the discrete token features on multimodal understanding tasks. We adopt the classic LLaVA [25] framework and select SigLIP2[40] as the vision encoder for its strong cross-modal alignment. In our setup,we only replace the vision encoder features while keeping all other components unchanged.We compare three variants:(1） original continuous SigLIP2 features,(2) vector quantization [41] (SigLIP2-VQ),and (3) dimension-wise quantization (SigLIP2-DQ).For the discrete variants,we use their dequantized features as input to LLaVA.We follow the LLaVA training protocol and evaluate on four standard benchmarks:GQA [15], TextVQA [35],POPE [23],and MME [11]．As shown in Table 3,SigLIP2-DQ achieves nearly identical performance to continuous features (63.1 vs 63.2 on GQA,59.8 vs 59.6 on TextVQA),while SigLIP2-VQ shows significant degradation across all metrics.These results confirm that dimension-wise quantization preserves the semantic understanding capabilities essential for multimodal tasks.

Table 4.Ablation studies on CubiD design choices.Gray rows indicate best results.
<table><tr><td>9 gFID↓</td></tr><tr><td>0.05 7.65</td></tr><tr><td>0.10 5.33</td></tr><tr><td>0.15 5.81</td></tr></table>

<table><tr><td>Masking Strategy</td><td>gFID↓</td></tr><tr><td>Per-dim</td><td>120.03</td></tr><tr><td>Per-spatial</td><td>22.22</td></tr><tr><td>Per-element (Ours)</td><td>5.33</td></tr></table>

(a)Mask ratio distribution. Effect of standard deviation σ in sampling mask ratios. Smaller σ biases toward aggressive masking,larger σ provides uniform coverage.  
(b)Masking granularity.Perdim: mask all spatial positions per dimension. Per-spatial: mask all dimensions per position. Perelement:mask independently across all axes.

<table><tr><td>Mask Value</td><td>gFID↓</td></tr><tr><td>Fixed</td><td>5.56</td></tr><tr><td>Random</td><td>56.38</td></tr><tr><td>Learned</td><td>5.33</td></tr></table>

![](auto/images/rf_full_regions/page_006_Table_00e81ee9c115.jpg)
(c)Mask value.Fixed,random, or learned mask token.

<table><tr><td>Steps</td><td>gFID↓</td></tr><tr><td>64</td><td>9.14</td></tr><tr><td>256</td><td>5.33</td></tr><tr><td>512</td><td>5.25</td></tr><tr><td>1024</td><td>5.25</td></tr></table>

![](auto/images/rf_full_regions/page_006_Table_1a71602ebb4c.jpg)
(d) Inference steps.Effect of inference steps T.

<table><tr><td>Params</td><td>gFID↓</td></tr><tr><td>946M</td><td>5.25</td></tr><tr><td>1.4B</td><td>4.91</td></tr><tr><td>3.7B</td><td>4.68</td></tr></table>

(e）Model scaling.Effect of model size.

<table><tr><td>Encoder</td><td>gFID↓</td></tr><tr><td>DINOv2</td><td>5.25</td></tr><tr><td>SigLIP2</td><td>5.87</td></tr></table>

(f) Representation encoder. DI-NOv2 vs. SigLIP2.

## 4.3. Studies of CubiD

Mask Ratio Distribution.Masking is the core operation of our discrete diffusion approach,and the distribution of masking ratios critically affects what patterns the model learns.We sample the masking ratio r from a truncated Gaussian distribution (Eq.2) with μ = 1.O and varying standard deviation o．The parameter o controls the diversity of masking scenarios: small o concentrates sampling around high masking ratios,forcing the model to learn from minimal context,while larger δ provides more uniform coverage across the [O,1] range.Table 4a shows that 9= 0.10 achieves optimal performance (gFID=5.33). Too small values (o = O.O5) degrade generation quality—the model overfits to heavily masked patterns without learning the full distribution.This optimal setting suggests that highdimensional features benefit from aggressive masking during training,likely due to their inherent redundancy.

Masking Strategy.We investigate different masking strategies for the h × w × d representation tensor. Table 4b and Figure 5 compare three approaches:(1) Per-dim masking, where all spatial positions for each dimension are masked together;(2)Per-spatial masking,where all dimensions at each spatial position are masked together；and (3)Perelement masking,our approach that independently masks individual elements across the tensor. The results show obvious performance differences: per-dim masking completely fails (gFID=120.03） with severe texture artifacts, while per-spatial masking produces blurry,locally inconsistent images (gFID=22.22). In contrast,our per-element masking achieves strong performance (gFID=5.33).This is because elements within the same spatial location or dimension exhibit strong dependencies and cannot be treated as independent units for parallel sampling.The 768 dimensions at each spatial position jointly encode semantic information—masking them together (per-spatial) prevents the model from leveraging these within-position correlations. Per-dim masking performs even worse as it requires all spatial positions to be generated in parallel,destroying spatial coherence entirely.Our per-element masking enables the model to observe partial information along both axes during training and generation,utilizing bidirectional attention to capture dependencies across the tensor. This validates the necessity of fine-grained masking for modeling highdimensional discrete tokens,where neither spatial positions nor dimensions can be fully decoupled.

Mask Token Design.We investigate different strategies for the mask token value used during training and inference.Table 4c compares three approaches:(1) Fixed:using a constant value (zero in our experiments),(2) Random:sampling from the discrete codebook at each masking operation,and (3) Learned: treating the mask token as a learnable parameter. The learned mask token achieves the best performance (gFID=5.33),while random sampling performs poorly (gFID=56.38). The failure of random sampling likely stems from the model's inability to distinguish between actual content tokens and randomly sampled mask tokens,as both come from the same codebook distribution. In contrast,a learned mask token can evolve during training to be maximally distinguishable from content tokens,facilitating more effective learning.

Number of Iterations.Table 4d illustrates the effect of inference steps on generation quality. In this experiment with DINOv2,our model needs to generate h × w × d = 16 × 16 × 768 = 196,608 discrete tokens for each image. Despite this massive token count,our method requires only hundreds of iterations to achieve high-quality generation. Performance improves from 64 to 256 steps and saturates around 512 iterations (gFID=5.25).This is remarkably efficient compared to autoregressive methods that would require all 196,608 sequential steps.

![](images/256b80b327cb9f2125c251a19b11d58fdd665d7bfbc6da1d27984bb0afbe3cfe.jpg)  
Figure 5.Qualitative comparison of different masking strategies.Top row:Per-dim masking completely fails,producing severe texture-like artifacts.Middle row:Per-spatial masking generates images with significant local inconsistencies and blurry details.Bottom row: Our per-element masking produces clear, coherent images with fine details.The dramatic quality difference validates that high-dimensional tokens require fine-grained masking across both spatial and dimensional axes.

Model Scaling. Table 4e shows results for models ranging from 946M to 3.7B parameters.We observe consistent improvement in generation quality as model size increases, with gFID decreasing from 5.25 for the 946M model to 4.68 for the 3.7B model．This scaling behavior demonstrates that our cubic discrete formulation effectively leverages increased model capacity,exhibiting strong scaling properties similar to other discrete generative models like autoregressive models. The steady improvement across model sizes suggests that our method can benefit from further scaling,making it a promising direction for high-quality representation-based image generation atlarger scales.

Representation Encoder. We evaluate CubiD with different representation encoders to assess generalization.Table 4f compares DINOv2 [30] and SigLIP2 [40] encoders, both producing 16x16x768 feature maps.Both encoders work well with our generation model,achieving gFID scores of 5.25 and 5.87 respectively with limited epochs. DINOv2 achieves slightly better generation quality, likely due to its ImageNet pretraining being better aligned with ImageNet-based evaluation metrics.The consistent performance across both encoders,despite their different training objectives,demonstrates the robustness of our approach.

<table><tr><td rowspan="2">Method</td><td rowspan="2">Latent Dim</td><td rowspan="2">#Params</td><td colspan="4">Generation @256 w/o guidance</td><td colspan="4">Generation@256 w/cfg or re</td></tr><tr><td>gFID↓</td><td>IS↑</td><td>Prec.↑</td><td>Rec.个</td><td>gFID↓</td><td>IS↑</td><td>Prec.↑</td><td>Rec.↑</td></tr><tr><td colspan="10">Discrete Diffusion Models with Low-dimensional Tokens</td></tr><tr><td>MaskGIT[3]</td><td>16</td><td>227M</td><td>6.18</td><td>182.1</td><td>0.80</td><td>0.51</td><td>4.02re</td><td>355.6re</td><td></td><td></td></tr><tr><td>VQ-Diffusion [12]</td><td>16</td><td>370M</td><td>11.89</td><td>-</td><td>-</td><td>1</td><td>1</td><td>1</td><td></td><td></td></tr><tr><td>Token-Critic [20]</td><td>16</td><td>368M</td><td>4.69</td><td>174.5</td><td>0.76</td><td>0.51</td><td>-</td><td>=</td><td></td><td></td></tr><tr><td>DPC [21]</td><td>16</td><td>454M</td><td>4.45</td><td>244.8</td><td>-</td><td>1</td><td>-</td><td>-</td><td></td><td></td></tr><tr><td>TiTok-S-128 [50]</td><td>16</td><td>287M</td><td>1</td><td>-</td><td>-</td><td>1</td><td>1.97</td><td>281.8</td><td></td><td></td></tr><tr><td colspan="10">Discrete Autoregressive Models with Low-dimensional Tokens</td></tr><tr><td>VQVAE2 [32]</td><td>64</td><td>13.5B</td><td>31.11</td><td>45</td><td>0.36</td><td>0.57</td><td>-</td><td>=</td><td></td><td></td></tr><tr><td>VQGAN [10]</td><td>128</td><td>1.4B</td><td>15.78</td><td>74.3</td><td>-</td><td>1</td><td>5.20re</td><td>280.3re</td><td></td><td></td></tr><tr><td>ViT-VQGAN [47]</td><td>32</td><td>1.7B</td><td>4.17</td><td>175.1</td><td>-</td><td>-</td><td>3.04re</td><td>227.4re</td><td>=</td><td></td></tr><tr><td>RQTran. [19]</td><td>16</td><td>3.8B</td><td>7.55</td><td>134.0</td><td>1</td><td>1</td><td>3.80re</td><td>323.7re</td><td>-</td><td>-</td></tr><tr><td>LlamaGen-XXL [36]</td><td>8</td><td>1.4B</td><td>14.6</td><td>86.3</td><td>0.63</td><td>0.68</td><td>2.34</td><td>253.9</td><td>0.81</td><td>0.60</td></tr><tr><td>VAR [39]</td><td>32</td><td>2.0B</td><td>2.16</td><td>288.7</td><td>0.81</td><td>0.61</td><td>1.97</td><td>334.7</td><td>0.81</td><td>0.61</td></tr><tr><td>VFMTok-XXL [52]</td><td>12</td><td>1.4B</td><td>1.95</td><td>259.3</td><td>0.82</td><td>0.62</td><td>2.19</td><td>278.0</td><td>0.83</td><td>0.60</td></tr><tr><td>VFMTok-3B [52]</td><td>12</td><td>3.1B</td><td>2.04</td><td>267.6</td><td>0.82</td><td>0.61</td><td>2.07</td><td>280.4</td><td>0.81</td><td>0.62</td></tr><tr><td colspan="10">Discrete Models with High-dimensional Tokens</td></tr><tr><td>CubiD-L</td><td>768</td><td>946M</td><td>2.38</td><td>213.1</td><td>0.84</td><td>0.57</td><td>2.37</td><td>213.4</td><td>0.84</td><td>0.57</td></tr><tr><td>CubiD-XL</td><td>768</td><td>1.4B</td><td>2.06</td><td>216.4</td><td>0.83</td><td>0.58</td><td>2.04</td><td>217.0</td><td>0.83</td><td>0.59</td></tr><tr><td>CubiD-XXL</td><td>768</td><td>3.7B</td><td>2.02</td><td>214.8</td><td>0.81</td><td>0.61</td><td>1.88</td><td>247.0</td><td>0.83</td><td>0.58</td></tr></table>

Table 5.Discrete generationmethodsonImageNet[8256x256.LatentDimdenotes theoriginaldimensionalityofthelatentspace (featureseforevectorquantizationforlow-dimensionalmethods,beforeandafterdimension-wiseuantizationforCubiD).Resultsith superscript"redenoterejectionsampling.CubiDisthefirstandonlydiscretemethodtodirectlygeneratewithnativehigh-dimensional representation tokens (768d),while allother methods use compressed or low-dimensional tokens (mostly below 32).

## 4.4. Main Results

Table 5 presents our main results on ImageNet 256×256 class-conditional generation, comparing CubiD with existing discrete generation methods.We organize methods into three categories: discrete diffusion with low-dimensional tokens,discrete autoregressive with low-dimensional tokens,and discrete models with high-dimensional tokens. CubiD is the only method that directly generates with native high-dimensional representation tokens.All existing methods operate in latent spaces ranging from 8 to 128 dimensions,with most below 32.Despite the increased complexity of modeling high-dimensional tokens,CubiD-XXL achieves state-of-the-art discrete generation with a gFID of 1.88.Notably,representation tokens show reduced dependency on classifier-free guidance—even without guidance, CubiD-XXL achieves 2.02 gFID,outperforming most VAEbased methods without guidance (e.g.,MaskGIT at 6.18 and LlamaGen-XXL at 14.6). While VFMTok also leveragesrepresentation features,it introduces deformable attention and region-adaptive mechanisms to reorganize the original features into 12-dimensional VQ tokens. This reorganization enables tractable autoregressive generation but fundamentally alters the token space,potentially limiting their use for understanding tasks.Moreover, VFM-Tok shows limited scaling benefits—performance slightly degrades from VFMTok-XXL(1.95 gFID) to VFMTok-3B(2.04 gFID).In contrast, CubiD demonstrates consistent improvement with scale,from 2.37 (L) to 2.04 (XL) to 1.88(XXL） with cfg,while generating directly in the original high-dimensional representation space without any reorganization or compression.These results illustrate the effectiveness of our discrete diffusion approach for highdimensional token generation.

## 5. Conclusion

In this work,we introduce CubiD,a novel discrete generative model that directly models native high-dimensional representation tokens for the first time.We achieve this through fine-grained masking across the entire spatialdimensional tensor, transforming the intractable problem of generating hundreds of thousands of sequential tokens into manageable parallel iterations. Our work demonstrates that discrete generation with standard cross-entropy loss can achieve state-of-the-art results even in the challenging regime of high-dimensional tokens,without requiring compression or reorganization of the original representation space.The preservation of native representation ability enables the same discrete tokens to serve both understanding and generation tasks,eliminating the need for separate tokenization schemes across tasks.We hope our work will inspire future research on unified multimodal architectures.

## Acknowledgment

This work is supported in part by the Research Grant Council of Hong Kong through the NSFC-RGC Joint Research Scheme under grant N\_HKU769/25.The authors are grateful to Boyang Zheng for helpful discussions on RAE and to Difan Zou,Yi Zhang,Yujin Han and Yuanzhi Zhu for valuable feedback on the early version of this work.

## References

[1] Jacob Austin,Daniel D Johnson,Jonathan Ho,Daniel Tarlow,and Rianne Van Den Berg. Structured denoising diffusion models in discrete state-spaces.In NeurIPS,2O21．2, 3

[2] Tom Brown,Benjamin Mann,Nick Ryder,Melanie Subbiah,Jared D Kaplan,Prafulla Dhariwal,Arvind Neelakantan,Pranav Shyam, Sastry,et al. Language models are fewshot learners.In NeurIPS,2020.1

[3] Huiwen Chang，Han Zhang,Lu Jiang，Ce Liu,and William T.Freeman.Maskgit: Masked generative image transformer.In CVPR,2022.2,3,4,5,8

[4] Junyu Chen,Han Cai,Junsong Chen,Enze Xie,Shang Yang, Haotian Tang,Muyang Li, Yao Lu,and Song Han.Deep compression autoencoder for efficient high-resolution diffusion models.arXiv preprint arXiv:2410.10733,2024.1

[5] Jiuhai Chen,Zhiyang Xu, Xichen Pan, Yushi Hu, Can Qin, Tom Goldstein,Lifu Huang,Tianyi Zhou, Saining Xie, Silvio Savarese,et al.Blip3-o:A family of fully open unifed multimodal models-architecture,training and dataset.arXiv preprint arXiv:2505.09568,2025.1

[6] Yufeng Cui,Honghao Chen,Haoge Deng, Xu Huang, Xinghang Li, Jirong Liu, Yang Liu, Zhuoyan Luo,Jinsheng Wang，Wenxuan Wang,etal.Emu3.5:Native multimodal models are world learners.arXiv preprint arXiv:2510.26583, 2025.1

[7] Bin Dai and David Wipf.Diagnosing and enhancing Vae models.arXiv preprint arXiv:1903.05789,2019.3

[8] Jia Deng,Wei Dong,Richard Socher,Li-Jia Li,Kai Li, and Li Fei-Fei. Imagenet: A large-scale hierarchical image database.In CVPR,2009.3,6,8,1

[9]Jacob Devlin,Ming-Wei Chang,Kenton Lee,and Kristina Toutanova. Bert: Pre-training of deep bidirectional transformers for language understanding.In NAACL,2019.3

[10] Patrick Esser,Robin Rombach,and Bjorn Ommer. Taming transformers for high-resolution image synthesis. In CVPR, 2021. 1, 3,8

[11] Chaoyou Fu,Peixian Chen，Yunhang Shen,Yulei Qin, Mengdan Zhang,Xu Lin, Jinrui Yang,Xiawu Zheng,Ke Li, Xing Sun,et al. Mme:A comprehensive evaluation benchmark for multimodal large language models.arXiv preprint arXiv:2306.13394,2023.6,1

[12] Shuyang Gu,Dong Chen,Jianmin Bao,Fang Wen,Bo Zhang,Dongdong Chen,Lu Yuan,and Baining Guo．Vector quantized diffusion model for text-to-image synthesis.In CVPR,2022.8

[13]Jian Han,Jinlai Liu,Yi Jiang,Bin Yan, Yuqi Zhang,Zehuan Yuan,Bingyue Peng,and Xiaobing Liu.Infinity: Scaling bitwise autoregressive modeling for high-resolution image synthesis.arXiv preprint arXiv:2412.04431,2024.3

[14] Martin Heusel,Hubert Ramsauer,Thomas Unterthiner, Bernhard Nesser,and Sepp Hochreiter. Gans trained by a two time-scale update rule converge to a local nash equilibrium.NeurIPS,30,2017.6

[15] Drew A Hudson and Christopher D Manning.Gqa:A new dataset for real-world visual reasoning and compositional question answering.In CVPR,2019.6,1

[16]Diederik P Kingma and Max Welling.Auto-encoding variational bayes.arXiv preprint arXiv:1312.6114,2013.1,3

[17] Dan Kondratyuk,Lijun Yu,Xiuye Gu,José Lezama, Jonathan Huang,Rachel Hornung,Hartwig Adam,Hassan Akbari,Yair Alon,Vighnesh Birodkar,et al.Videopoet:A large language model for zero-shot video generation.arXiv preprint arXiv:2312.14125,2023.3

[18] Tuomas Kynkäänniemi,Tero Karras,Samuli Laine,Jaakko Lehtinen,and Timo Aila.Improved precision and recall metric for assessing generative models.NeurIPS,32,2019.6

[19] Doyup Lee,Chiheon Kim, Saehoon Kim,Minsu Cho,and Wook-Shin Han.Autoregressive image generation using residual quantization.In CVPR,2022.8

[20] José Lezama,Huiwen Chang,Lu Jiang,and Irfan Essa. Improved masked image generation with token-critic.In ECCV, 2022. 8

[21] Jose Lezama,Tim Salimans,Lu Jiang,Huiwen Chang, Jonathan Ho,and Irfan Essa．Discrete predictor-corrector diffusion models for image synthesis. In ICLR,2022.8

[22] Junnan Li,Dongxu Li,Caiming Xiong,and Steven Hoi. Blip: Bootstrapping language-image pre-training for unified vision-language understanding and generation. In ICML, 2022.1

[23] Yifan Li, Yifan Du,Kun Zhou,Jinpeng Wang,Wayne Xin Zhao,and Ji rong Wen．Evaluating object hallucination in large vision-language models. 2023. 6,1

[24] Dongyang Liu,Shitian Zhao,Le Zhuo,Weifeng Lin, Yu Qiao,Hongsheng Li,and Peng Gao．Lumina-mgpt: Illuminate flexible photorealistic text-to-image generation with multimodal generative pretraining.arXiv preprint arXiv:2408.02657,2024.3

[25] Haotian Liu,Chunyuan Li,Yuheng LiBo Li,Yuanhan Zhang,Sheng Shen,and Yong Jae Lee.Llava-next:Improved reasoning,ocr,and world knowledge,2024.6,1

[26] Aaron Lou,Chenlin Meng,and Stefano Ermon．Discrete diffusion modeling by estimating the ratios of the data distribution. arXiv preprint arXiv:2310.16834,2023.2,3

[27] Nanye Ma,Mark Goldstein，Michael S.Albergo, Nicholas M.Bof，Eric Vanden-Eijnden，and Saining Xie.Sit: Exploring flow and diffusion-based generative models with scalable interpolant transformers.arXiv preprint arXiv:2401.08740,2024.1

[28] Fabian Mentzer,David Minnen,Eirikur Agustsson,and Michael Tschannen.Finite scalar quantization: Vq-vae made simple.arXiv preprint arXiv:2309.15505,2023.3

[29] Shen Nie,Fengqi Zhu, Zebin You, Xiaolu Zhang,Jingyang Ou,Jun Hu,Jun Zhou,Yankai Lin,Ji-Rong Wen,and Chongxuan Li.Large language diffusion models.arXiv preprint arXiv:2502.09992,2025.3

[30] Maxime Oquab,Timothée Darcet,Theo Moutakanni,Huy Vo,Marc Szafraniec,Vasil Khalidov,Pierre Fernandez, Daniel Haziza,Francisco Massa,Alaaeldin El-Nouby,et al. Dinov2:Learning robust visual features without supervision. arXiv preprint arXiv:2304.07193,2023.3,4,5,6,7

[31] Aditya Ramesh,Mikhail Pavlov,Gabriel Goh, Scott Gray, Chelsea Voss,Alec Radford,Mark Chen,and Ilya Sutskever. Zero-shot text-to-image generation.In ICML, pages 8821- 8831,2021. 3

[32] Ali Razavi,Aäron van den Oord,and Oriol Vinyals.Generating diverse high-fidelity images with vq-vae-2.In NeurIPS, 2019.8

[33] Tim Salimans,Ian Goodfellow,Wojciech Zaremba,Vicki Cheung,Alec Radford,and Xi Chen.Improved techniques for training gans.NeurIPS,29,2016.6

[34] Minglei Shi,Haolin Wang,Wenzhao Zheng,Ziyang Yuan, Xiaoshi Wu,Xintao Wang,Pengfei Wan,Jie Zhou,and Jiwen Lu.Latent diffusion model without variational autoencoder. arXiv preprint arXiv:2510.15301,2025.3

[35] Amanpreet Singh,Vivek Natarajan,Meet Shah,Yu Jiang, Xinlei Chen，Dhruv Batra,Devi Parikh,and Marcus Rohrbach．Towards vqa models that can read．In CVPR, 2019. 6,1

[36] Peize Sun,Yi Jiang,Shoufa Chen,Shilong Zhang,Bingyue Peng,Ping Luo,and Zehuan Yuan．Autoregressive model beats diffusion: Llama for scalable image generation.arXiv preprint arXiv:2406.06525,2024.1,3,8

[37] Quan Sun, Yufeng Cui, Xiaosong Zhang,Fan Zhang, Qiying Yu, Zhengxiong Luo,Yueze Wang,Yongming Rao,Jingjing Liu,Tiejun Huang,and Xinlong Wang. Generative multimodal models are in-context learners.2023.1

[38] Chameleon Team． Chameleon:Mixed-modal early-fusion foundation models.arXiv preprint arXiv:2405.09818,2024.

[39] Keyu Tian,Yi Jiang,Zehuan Yuan,Bingyue Peng,and Liwei Wang.Visual autoregressive modeling: Scalable image generation via next-scale prediction.arXiv preprint arXiv:2404.02905,2024. 1,8

[40] Michael Tschannen,Alexey Gritsenko,Xiao Wang,Muhammad Ferjad Naeem,Ibrahim Alabdulmohsin，Nikhil Parthasarathy,Talfan Evans,Lucas Beyer,Ye Xia,Basil Mustafa,et al. Siglip 2:Multilingual vision-language encoders with improved semantic understanding,localization, and dense features.arXiv preprint arXiv:2502.14786,2025. 3,4,5,6,7

[41] Aaron van den Oord, Oriol Vinyals,and koray kavukcuoglu. Neural discrete representation learning．In NeurIPS,2017. 1,2, 6

[42] Yuqing Wang,Tianwei Xiong,Daquan Zhou, Zhijie Lin, Yang Zhao, Bingyi Kang,JiashiFeng,and Xihui Liu.Loong: Generating minute-level long videos with autoregressive language models.arXiv preprint arXiv:2410.02757,2024.3

[43] Yuqing Wang,Zhijie Lin,Yao Teng,Yuanzhi Zhu,Shuhuai Ren,Jiashi Feng,and Xihui Liu.Bridging continuous and

discrete tokens for autoregressive visual generation．2025. 2,3,4

[44] Yuqing Wang,Shuhuai Ren,Zhijie Lin, Yujin Han,Haoyuan Guo,Zhenheng Yang,Difan Zou,Jiashi Feng,and Xihui Liu.Parallelized autoregressive visual generation.In CVPR, 2025.3

[45] Mark Weber,Lijun Yu,Qihang Yu,Xueqing Deng,Xiaohui Shen,Daniel Cremers,and Liang-Chieh Chen.Maskbit: Embedding-free image generation via bit tokens.Transactions onMachineLearning Research,2024.3

[46] Jinheng Xie,Weijia Mao,Zechen Bai,David Junhao Zhang, Weihao Wang，Kevin Qinghong Lin,Yuchao Gu,Zhijie Chen,Zhenheng Yang,and Mike Zheng Shou． Show-o: One single transformer to unify multimodal understanding and generation. ArXiv,2024.1

[47] Jiahui Yu, Xin Li,Jing Yu Koh, Han Zhang,Ruoming Pang, James Qin,Alexander Ku, Yuanzhong Xu,Jason Baldridge, and Yonghui Wu.Vector-quantized image modeling with improved vqgan.arXiv preprint arXiv:2110.04627,2021.1, 8

[48] Jiahui Yu, Yuanzhong Xu, Jing Yu Koh,Thang Luong,Gunjan Baid, Zirui Wang,Vijay Vasudevan,Alexander Ku,Yinfei Yang,Burcu Karagol Ayan,et al.Scaling autoregressive models for content-rich text-to-image generation. arXiv preprint arXiv:2206.10789,2022.3

[49] Lijun Yu,José Lezama,Nitesh B Gundavarapu,Luca Versari,Kihyuk Sohn,David Minnen，Yong Cheng，Agrim Gupta, Xiuye Gu, Alexander G Hauptmann, et al. Language model beats diffusion-tokenizer is key to visual generation. In ICLR,2024.3

[50] Qihang Yu,Mark Weber, Xueqing Deng,Xiaohui Shen, Daniel Cremers,and Liang-Chieh Chen.An image is worth 32 tokens for reconstruction and generation．arxiv: 2406.07550,2024. 8

[51] Yue Zhao,Yuanjun Xiong,and Philipp Krähenbuhl. Image and video tokenization with binary spherical quantization. arXiv preprint arXiv:2406.07548,2024.3

[52] Anlin Zheng,Xin Wen,Xuanyang Zhang,Chuofan Ma, Tiancai Wang,Gang Yu,Xiangyu Zhang,and Xiaojuan Qi. Vision foundation models as effective visual tokenizers for autoregressive image generation.arXiv preprint arXiv:2507.08441,2025. 3,8

[53] Boyang Zheng,Nanye Ma, Shengbang Tong,and Saining Xie.Diffusion transformers with representation autoencoders．arXiv preprint arXiv:2510.11690,2025．1,3,5, 2

[54] Chuanxia Zheng and Andrea Vedaldi. Online clustered codebook.In ICCV,2023.1

[55] Lianmin Zheng，Wei-Lin Chiang，Ying Sheng，Siyuan Zhuang,Zhanghao Wu,Yonghao Zhuang,Zi Lin, Zhuohan Li,Dacheng Li, Eric.P Xing,Hao Zhang,Joseph E.Gonzalez,and Ion Stoica. Judging llm-as-a-judge with mt-bench and chatbot arena.arXiv preprint arXiv:2306.05685,2023. 1