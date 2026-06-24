<!-- part 5/9 chars 23857-28280 -->

LIP2 features.VQ:vector quantization,DQ:dimension-wise quantization．DQ maintains continuous-level performance while VQ shows significant degradation.
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