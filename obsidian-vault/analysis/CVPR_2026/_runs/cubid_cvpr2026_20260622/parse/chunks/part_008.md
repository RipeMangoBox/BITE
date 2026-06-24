<!-- part 8/9 chars 39699-47475 -->

hieve state-of-the-art results even in the challenging regime of high-dimensional tokens,without requiring compression or reorganization of the original representation space.The preservation of native representation ability enables the same discrete tokens to serve both understanding and generation tasks,eliminating the need for separate tokenization schemes across tasks.We hope our work will inspire future research on unified multimodal architectures.

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