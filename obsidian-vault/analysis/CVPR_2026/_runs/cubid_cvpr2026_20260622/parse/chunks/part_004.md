<!-- part 4/9 chars 19626-24657 -->

rence,CubiD generates images through iterative refinement starting from a fully masked tensor.As illustrated in Figure 4,the model begins with all tokens masked (O%）and progressively unmasks them until reaching a complete image (loo%).At each iteration t, the model predicts all masked tokens simultaneously and unmasks a subset randomly. Motivated by MaskGIT [3], the number of tokens to unmask follows a cosine schedule.The schedule ensures a coarse-to-fine generation process where early iterations establish overall structure and later iterations refine details. Crucially, the parallel nature of our approach means generation requires only O(T) iterations—typically hundreds of steps-regardless of the tensor dimensionality d,making high-dimensional discrete generation computationally feasible.

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