<!-- part 6/6 chars 36284-40133 -->

etching: when the sofa is lengthened, extra supporting legs appear, and the Arc de Triomphe likewise acquires a plausible shape. Moreover, as shown in Figure~\ref{fig:image-generation bbox compare}, the bounding box signal can inject an activation cue into the generation network when single-image conditioned generation fails, yielding a valid mesh.

{\bf Point cloud condition}.
As shown in Figure~\ref{fig:exp_point_control}, we present the generation results under two settings: image only and image with point cloud control. For the latter, we further consider three types of point cloud inputs: complete point clouds, point clouds from depth images, and point clouds from scans. For the first two cases in the figure, we observe that providing a complete point cloud as a control signal effectively resolves the ambiguity inherent in single-view inputs and allows the recovery of occluded internal structures. In the third and fifth cases, where surface point clouds are obtained via a depth map, the additional input similarly mitigates single-view ambiguity, ensuring that the generated geometry is well-aligned in scale with the ground truth. In the fourth case, given a noisy surface point cloud from a scan, the generated geometry is also better aligned with the original object compared with the image-only baseline, addressing the issue where the image encoder tends to ignore the true object pose. In summary, once point cloud input is provided, our Omni model can effectively align the generated geometry with real-world geometry. This further demonstrates that even partial point clouds serve as a strong cue for improving the quality of 3D geometry generation.

{\bf Voxel Condition}.
Similar to the point cloud condition, the voxel condition provides sparse geometric cues that help resolve the ambiguities inherent in a single image. As shown in Figure~\ref{fig:exp_voxel_control}, in the first and fifth cases, the additional voxel control condition ensures that the generated objects are properly aligned in scale with the ground truth geometry. Cases 2, 3, and 4 further illustrate how the voxel condition contributes to recovering fine geometric details. For instance, restoring the flat surface of the shield, capturing the shape of the bird's wing, and reproducing the low-poly style geometry of the cup. These examples clearly demonstrate that incorporating voxel conditions enables the model to faithfully recover both the proportions and the details of object geometry, thereby further improving generation quality.

\section{Conclusion}
In this paper, we propose a unified framework, called \shortname, for fine-grained and controllable 3D asset generation. We incorporate point cloud, voxel, bounding box, and skeleton to mitigate geometry distortion in image-only 3D generation and achieve style control. To unify these extra conditions in one diffusion model, we design a lightweight unified control encoder. Building on the powerful existing 3D generation model, such as Hunyuan3D 2.1, \shortname just introduces a lightweight encoder to achieve high-quality controllable generation. Experiments show that these additional controls improve generation accuracy, enable geometry-aware transformations, and increase robustness for production workflows.

\section{Contributors}
\large{Authors are listed \textbf{alphabetically by the first name}.}
\definecolor{tencentblue}{RGB}{38,54,221}

\large{
\color{tencentblue}
\begin{multicols}{2}
\raggedcolumns
Bowen Zhang\\
Chunchao Guo\\
Haolin Liu\\
Hongyu Yan\\
Huiwen Shi\\
Jingwei Huang\\
Junlin Yu\\
Kunhong Li\\
Linus\\
Penghao Wang\\
Qingxiang Lin\\
Sicong Liu\\
Xianghui Yang\\
Yixuan Tang\\
Yunfei Zhao\\
Zeqiang Lai\\
Zhihao Liang\\
Zibo Zhao
\end{multicols}}

\clearpage

\bibliography{colm2024_conference}
\bibliographystyle{colm2024_conference}


\end{document}