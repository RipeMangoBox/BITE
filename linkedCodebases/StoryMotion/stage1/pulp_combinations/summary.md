# Stage1 Pulp Combination Eval

- samples: 64
- pulp stage1 checkpoint: `/data/public/ripemangobox/Motion/PulpMotion_official_eval/pulpmotion-models/autoencoder/aemmardm-xgmj0yjj-325.ckpt`

| combo | mpjpe_mean | camera_translation_l2_mean | camera_rotation_deg_mean | projection_xy_l2_visible_mean_px |
|---|---:|---:|---:|---:|
| gt_camera+gt_motion | 0 | 0 | 0.00739128 | 0 |
| vae_camera+gt_motion | 0 | 0.0310732 | 2.83731 | 43.8546 |
| gt_camera+vae_motion | 0.659485 | 0 | 0.00739128 | 529.514 |
| vae_camera+vae_motion | 0.659485 | 0.0310732 | 2.83731 | 617.418 |
| pulp_camera+gt_motion | 0 | 0.112428 | 1.63751 | 53.1719 |
| gt_camera+pulp_motion | 0.170226 | 0 | 0.00739128 | 45.0881 |
| pulp_camera+pulp_motion | 0.170226 | 0.112428 | 1.63751 | 58.4547 |
