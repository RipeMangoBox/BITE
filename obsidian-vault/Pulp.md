## summary
1. 首个text conditioned joint generation of human motion and camera trajectory.
2. 借助 screen-space rep中间表示来串联human motion和camera trajectory


## method

explicit bridging human motion and camera trajectory by joint encoder and linear mapping（这有点像 StyleGAN 的多层linear，将latent space从W映射到Z）
![[Pasted image 20260605215603.png]]


## 数据集构建
1. human motion & camera trajectory，E.T方法
2. human motion caption，Qwen VL 2.5打标，TMR评估
3. motion data refine，相机reprojection确定拍到的区域，再使用motiongpt补全 没拍到的部分



## doubt
1. 对比实验的实现写得太笼统，没有实现细节，有些难以判定合理性
2. full、pure subset、mixed subset分别指什么


---

# Towards Storytelling Animations: Joint Synthesis of Human and Camera  Motions

## summary
learn to independently model the characters and camera, and explicitly learn character-character and camera-character interactions.

## data
professional motion data extracted from existing film clips, and high-quality motion data synthesized from a cinematography simulator

## method
\<character A, camera>,\<character B, camera>，\<character A, character B>，use the MDM backbone and interaction module like **InterGen**.

==Unconditional manner! Leaving the room for my unified conditional framework for \<human motion, camera trajectory> !==

## doubt


## insight
1. 相机的运动有一定的镜头语义，比如"push in"可以紧张气氛