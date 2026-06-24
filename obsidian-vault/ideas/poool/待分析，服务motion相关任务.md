
生成框架方面：semantic, fine details, data rep, generation framework；
+ 如果强调fine detail，未必死磕text-to-motion，可以关注 analysis库中其他motion任务和数据集支持；
+ 如果强调语义注入，同样可以用于text-to-motion以外的任务，竞争更小赛道更宽，比如用VLM提供简单的motion语义。另外，这里的语义未必是文本模态。

1. https://arxiv.org/pdf/2512.19693
2.  https://arxiv.org/pdf/2604.24763
3. https://arxiv.org/abs/2503.07076v5
4. https://arxiv.org/pdf/2509.05441
5. BLOCK DIFFUSION： https://arxiv.org/pdf/2503.09573
6. EQ-VAE： https://arxiv.org/pdf/2502.09509


noise study：
1. https://arxiv.org/pdf/2212.09541
2. https://arxiv.org/pdf/2511.07911


skeleton extraction
1. ![[BlumNet.pdf]]



layout概念是否能优化人物入镜率？低优先级，需要等4090完成camera projection containment实验再决定。
1. https://arxiv.org/pdf/2412.03859
2. https://www.semanticscholar.org/reader/478069d83c9d504c3fb70bb28c86b475257bb92a


motion本领域论文，强调了情景化的t2m，有意思，但数据和模型都不开源
1. https://openaccess.thecvf.com/content/ICCV2025/papers/Wang_You_Think_You_ACT_The_New_Task_of_Arbitrary_Text_ICCV_2025_paper.pdf

高精度motion 重建，或许能用于motion的生成、重建统一，或者单纯迁移高精度的设计到动作生成
1. https://arxiv.org/pdf/2604.21575