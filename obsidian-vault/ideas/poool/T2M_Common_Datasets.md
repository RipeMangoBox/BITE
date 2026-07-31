# T2M Common Datasets

Shared reference for datasets frequently cited in Text-to-Motion (T2M) research. Analysis notes should link to this document rather than re-describing dataset statistics inline.

## Quick Reference

| Dataset | Sequences | Text Annotations | Frame Rate | Joints | Representation | Source |
|---|---|---|---|---|---|---|
| HumanML3D | 14,616 | 44,970 | 20 fps | 22 (SMPL) | 263-dim or 272-dim | Guo et al., CVPR 2022 |
| KIT-ML | 3,911 | ~6,278 | 12.5 fps | -- | similar to HumanML3D | Plappert et al., 2016 |
| BABEL | 10,881 (from AMASS) | ~65,926 labels | -- | -- | frame/seq annotations | Punnakkal et al., CVPR 2021 |
| AMASS | 40+ hours | none | -- | SMPL/SMPL-H/SMPL-X | mocap surfaces | Mahmood et al., ICCV 2019 |
| Motion-X | ~80K | text annotations | -- | SMPL-X | 3D motion + text | Lin et al., NeurIPS 2024 |
| MotionHub | ~350K | -- | -- | SMPL-H | multi-source mocap | -- |
| SAMP | ~100K frames | -- | -- | SMPL-X | scene-aware (3D-FRONT) | Hassan et al., ICCV 2021 |
| GRAB | 1.6M frames | -- | -- | SMPL-X | grasping, 51 objects | Taheri et al., ECCV 2020 |
| BEHAVE | ~15K frames | -- | -- | SMPL | HOI, 20 objects | Bhatnagar et al., CVPR 2022 |
| 3D-FRONT | 18K rooms | -- | -- | -- | 3D indoor scenes | Fu et al., CVPR 2021 |
| FineMotion | -- | fine-grained text | -- | SMPL | spatial+textual annotation | -- |
| Human3.6M | 3.6M frames | 17 action classes | 50 fps | 32 (custom) | 3D poses, 11 subjects | Ionescu et al., TPAMI 2014 |

## HumanML3D

- **Full name**: Human Motion Language 3D
- **Size**: 14,616 motion sequences, 44,970 text descriptions
- **Representation**: 263-dim feature vector (root velocity, joint rotations, foot contact), or 272-dim SMPL 6D rotation variant
- **Frame rate**: 20 fps
- **Joints**: 22 joints (SMPL skeleton)
- **Source paper**: Guo et al., "Generating Diverse and Natural 3D Human Motions from Text", CVPR 2022
- **Standard splits**: train/test as defined by Guo et al.
- **Common use in T2M papers**: Primary benchmark for text-to-motion generation. Standard evaluation metrics (FID, R-Precision, MM-Dist, Diversity, MModality) are computed using the feature extractor from Guo et al.

## KIT Motion-Language (KIT-ML)

- **Size**: 3,911 motion sequences, ~6,278 text descriptions
- **Representation**: similar to HumanML3D
- **Frame rate**: 12.5 fps
- **Source**: Plappert et al., "The KIT Motion-Language Dataset", 2016
- **Common use in T2M papers**: Secondary benchmark, typically used alongside HumanML3D to validate generalization to a smaller dataset with different motion characteristics.

## BABEL

- **Size**: 10,881 motion sequences from AMASS, ~65,926 text labels
- **Action types**: ~40
- **Annotations**: Frame-level and sequence-level text labels
- **Source**: Punnakkal et al., "BABEL: Bodies, Action and Behavior with English Labels", CVPR 2021
- **Common use in T2M papers**: Motion generation with dense frame-level text annotations or transition-focused tasks.

## AMASS

- **Full name**: Archive of Motion Capture as Surface Shapes
- **Size**: 40+ hours of mocap from multiple datasets (CMU, MPI, BMLrub, EyesJapan, etc.)
- **Text annotations**: None (BABEL provides text labels on top of AMASS)
- **Body models**: SMPL, SMPL-H, SMPL-X
- **Source**: Mahmood et al., "AMASS: Archive of Motion Capture as Surface Shapes", ICCV 2019
- **Common use in T2M papers**: Used for unconditional motion generation, motion prediction/interpolation pretraining, and as the raw mocap source for BABEL.

## Motion-X

- **Size**: ~80K sequences with text annotations
- **Representation**: SMPL-X parameters, whole-body motion (body + hands + face)
- **Common use**: Large-scale whole-body motion generation, multi-modal conditioning.

## MotionHub

- **Size**: ~350K SMPL-H sequences aggregated from multiple public datasets
- **Common use**: Large-scale pretraining for motion generation models.

## SAMP

- **Size**: ~100K mocap frames with scene annotations from 3D-FRONT
- **Representation**: SMPL-X
- **Source**: Hassan et al., "Stochastic Scene-Aware Motion Prediction", ICCV 2021
- **Common use**: Scene-aware motion generation, human-scene interaction.

## GRAB

- **Size**: 1.6M grasping frames, 51 objects
- **Representation**: SMPL-X with hand poses
- **Source**: Taheri et al., "GRAB: A Dataset of Whole-Body Human Grasping of Objects", ECCV 2020
- **Common use**: Human-object interaction, grasping motion generation.

## BEHAVE

- **Size**: ~15K frames, 20 objects
- **Representation**: SMPL with object meshes
- **Source**: Bhatnagar et al., "BEHAVE: Dataset and Method for Tracking Human Object Interactions", CVPR 2022
- **Common use**: Human-object interaction generation and tracking.

## 3D-FRONT

- **Size**: 18K rooms (3D indoor scenes with furniture layouts)
- **Source**: Fu et al., "3D-FRONT: 3D Furnished Rooms with layOuts and semaNTics", CVPR 2021
- **Common use**: Provides scene context for scene-aware motion generation (e.g., SAMP).

## FineMotion

- **Size and format**: Fine-grained spatial and textual annotations for motion
- **Common use**: Motion generation requiring detailed spatial grounding of text descriptions.

## Human3.6M

- **Size**: 3.6M frames, 11 subjects, 17 action classes
- **Frame rate**: 50 fps
- **Joints**: 32 joints (custom skeleton)
- **Source**: Ionescu et al., "Human3.6M: Large Scale Datasets and Predictive Methods for 3D Human Sensing in Natural Environments", TPAMI 2014
- **Common use**: Classic benchmark for human pose estimation and motion prediction. Occasionally used as auxiliary data in T2M work.

---

> **Note for analysis notes**: When describing experimental setups, link to this document rather than re-stating dataset sizes, dimensions, and formats inline. For example: `Trained on HumanML3D（详见[[../../references/T2M_Common_Datasets#HumanML3D|HumanML3D]]）and KIT-ML.` Reserve inline text for how the specific paper uses the dataset (training protocol, metrics, splits, preprocessing choices).
