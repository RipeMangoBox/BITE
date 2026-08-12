---
title: "StoryMotion Experiment SHA Registry"
status: active
hypothesis: |
  Immutable experiment identities are centralized here so the metric ledger
  remains a numeric evidence owner rather than mixing results with hashes.
tags:
  - StoryMotion
  - experiment
  - provenance
  - status/active
aliases:
  - StoryMotion-Exp-SHA
source_notes:
  - "[[StoryMotion/current]]"
  - "[[StoryMotion-valid-metric-ledger]]"
  - "[[version_family]]"
  - "[[2026-07-29_storymotion-v10-human-relative-camera-training-contract]]"
  - "[[2026-07-29_storymotion-v11-v9-owner-stage2-three-mode-rescue-contract]]"
created: 2026-07-28T12:03:02+08:00
updated: 2026-08-13T02:03:00+08:00
---

# StoryMotion Experiment SHA Registry

> [!abstract] Identity owner
> 本页集中拥有 StoryMotion checkpoint、owning decoder、cache、ordered-ID、contract、result、records、visual 与 implementation SHA256。数值结论只见 [[StoryMotion-valid-metric-ledger]]；当前裁决只见 [[StoryMotion/current]]。本页不重新解释指标，也不以 hash 存在替代 formal audit。

## 1. v9 redesign protected-H ViMoGen Unified-3

Run：v9_hanchor_protected_vimogen_u3_diag_seed17_4090g1_20260727。

### 1.1 Stage1 owner, Stage2 training, and cache

| stage / run | immutable role | SHA256 |
| --- | --- | --- |
| Stage1 redesign Pulp-only / stage1_hanchor_pulp_only_matched_r3_636k_seed17_4090g0_20260726 | step636K checkpoint and owning decoder | 51233f6a032c779e66b6eed4bb22b7f61c41d9b4a5a0a1ffc7dade7d3d86d4df |
| Stage2 redesign protected-H / full run | experiment contract / trained manifest | 54cdb96c3a89422cc250bfc05974f0d7823e572c437842831802a1ebc6d7c32b / 2084e5808843a3c74bd999967f689c776d49463318d88c2d5ed6cb80a5c8fc50 |
| Stage2 redesign protected-H / Human boundary | teacher checkpoint / transition payload | 3efd59481f8052b401889fce6559e31f96cb88f51dfb6c466464cf05ec6c2c50 / 03c8b636920ad748330b57d5ebb84657a40832a01a10dbde3739b28e2942414f |
| Stage2 redesign protected-H / global210K | step210K checkpoint / last.pt | 07652423f954549219bce797920e50636f4943215b4d856fd6e7864da9a04cb9 / 87314a4e362b9c259b49113842aa6cd162b86499595209ead4f4aa6ece105aec |
| Stage2 redesign protected-H / cache | train / eval / train-only full-cov stats / cache manifest | 04add8e553af334e4724f08c7076a0be24f171470b938920120ef64fc7b01576 / cd10a02a09bbb716dcdd1796bc0b11cac4451ff3f18496535c68464e0d88a603 / 117d51a1d2ed1ae57541723b85c732118172634c57b2665f00b246c36e218558 / 4c1c54159ca3b0027da82234540c411101bceee3e01ecd0740e52b9b239c225e |
| Stage2 redesign protected-H / first512 | ordered sample IDs | 6b9c92a533d2d0aff76cce6c7ad23361733fb38d3157128bf7eee56cdc33d8df |

### 1.2 Human teacher endpoint N=512

| stage / run | immutable role | SHA256 |
| --- | --- | --- |
| Human teacher105K Direct-H / human_teacher_105k_direct_h_n512_20260728 | eval contract / manifest / result / records / fixed samples | 25f2b40c55bfa2cc4233678774a82a1e753bf6165cb3c66f02cbd1095faf39f0 / 002db30b56fa302654af12b64ec17704c7921a1b1ae594e231358d04917a1d0a / 1db8f3ad226df27def2015f4ef047de64bcdd0fe231e62a9e3aace957556d2a7 / 46da26c3d1419240536ad3fd7921066e8930b07a486e8ed927db03232d96ebcd / 6310a1b32396247e79175aac67ea0155438f0ba88010c005545029e35eb3fc16 |
| Human teacher105K Direct-H / fixed8 | visual manifest | f8885a5bd262e52bd2611a5ac9d199098b4072dbde77c9a6fb8fc95de835f28a |

### 1.3 Unified global210K N=512

| stage / run | immutable role | SHA256 |
| --- | --- | --- |
| Unified210K Direct-H / unified_210k_direct_h_n512_r2_20260728 | eval contract / manifest / result / records / fixed samples | 59fd2e28a8ef2a5233b7059509dca9ad3e6513d65c35b05e890fc7aedebc0f40 / 94b7f2508dcaeb240559e418503d5b18e2c715b94c3fad4c5d997fd444f2bd72 / 9dae46d216b91d4744b722591748b05917d9bba06432a3751f20669cda2abd73 / 6decee38543a73eb9b53dfcd37d4dfcac7075d57c4a62be6f347dd9756471dc0 / f5222297b42fa7057b6f777c70e283c5379f2a27b251fe8824a886f235885732 |
| Unified210K Direct-C / unified_210k_direct_c_n512_20260728 | eval contract / manifest / result / records / fixed samples | 355c5a204208bdb4e0cde8b86370983e2049f2a2be59fc92fb59b77856f32a8c / 5febbf1470b9a7c0411afa7017dcce0616b083bae9db01fe9895b7026ef964a7 / fac9c33295ba7273537834f6c0c13451c150d5c76a0d33bc043532ebccc780fa / f8a25164478a3be1b6cf23c17b7baca63ae72e807b6217906a89d8f19357c1bf / 044d2bae9647417c6e651ac9cd9d8f83b54bb18f37e6d56d8507dee7388839b1 |
| Unified210K joint parallel / unified_210k_joint_parallel_n512_r2_20260728 | eval contract / manifest / result / records / fixed samples | 596a4a2819d93f03a03e014a6ff928be4aaae7dded9ea89bcdd7f7974516bd75 / 5e88814e60b09bf4b29d7dbcd06fc3bd4bf8a91ecd1bcf61bd038f3157e58bce / 1c6bda40946f92585a032653fb3f694630ddccd607ae9aaa6b7849ba676f8c7d / d119374c2c66030391892b37630b6c9bea20d3c24c8406b227dc1a706b26ea4d / 4400a5c3f170fa8ae28098059e77833ab3f64feef3de5cb9757be5e094a23354 |
| Unified210K Camera + joint / fixed8 | visual manifest | 39cfb7e970a70d067eb855d6328d1e5d52c09d35ac84650f12cc44edbdb7c15f |

> [!warning] Eligibility boundary
> 上述 redesign run 的 contract 明确 diagnostic_only=true、promotion_eligible=false。集中登记 SHA 不改变该边界。

### 1.4 P0 intermediate snapshot formal eval

| stage / run | immutable role | SHA256 |
| --- | --- | --- |
| Unified global140K | Camera EMA snapshot | be96e3ec73b20e76af7b767b012dd4dd03a45aadb5a0cc23ba753ff21e3040a7 |
| Unified global175K | Camera EMA snapshot | 421b3f06d69c797fe9c44af0f89702c999c5709539ac83b603742b63bd006256 |
| Unified global189K | Camera EMA snapshot | 158663c5d756ffecf52d799c4b9c4ae34774762f236227d206b408bc3a97277c |

以下字段顺序均为 eval contract / manifest / result / records / fixed samples。

| stage / run | SHA256 |
| --- | --- |
| `unified_140k_direct_c_n512_r2_20260728` | 52adae02fdd6f4801a7df93946c54671605bc34a009e5172bd59ce122dc355e5 / 5bf2cfc1daf8e2b53735cb29b23eb597506a92b02d7853209a52034d8179dfe1 / 94be540ff0fae4c5f837001c2ecca3f62959aaccf28718b4eb9d0aab6bca7646 / d9eb70dba91b36c03252e79aabe479edb615ea98b93bd11d6626c86749d68e07 / 799b3bc20149e5eb23c4b177d98423cd566733d75a8a30a411c1e91ab587587a |
| `unified_140k_joint_parallel_n512_r2_20260728` | be65468be31971e5ca7dd86f8969fd6b76d23e26b261431d55d96fb7f5166143 / 3ca26eebd65c85d309fbc49ce61fe84474cfc012be14a7b688a03521af32f50f / 9c6744118c87eadd266dcff5cac202bf5ef30a45da3af3f47bda3b3a1c3b7b7c / 4d4cb73266626ed95f3682da240b4952a0a6dd2529071981df393203a4ad02f6 / 4ef1f377d780e35ea234cfcecdf015f4389cc6539d6b05edfcf47466c6c2176c |
| `unified_175k_direct_c_n512_r2_20260728` | 66a1762e1bdf2cee5e7032b107203c4a039b7c8950facfa760df6863e475dcdb / 93cd53ddc3df4c2775cfd2bd496d1f2eef1a748f5048eb63e0af2bc7b5a75311 / 348ecca2b2077b506c39712e7b0dd857f0b3319a28b6707800b8af440c223109 / 999cda2045337b859945aa3e38b24de6f277acdac613e0b8236e35a1574d0ba4 / 14d2dbf9e834bd3e1f54d05baf7e2e1daf808f361d8b54bf61d0c9ff28e8a121 |
| `unified_175k_joint_parallel_n512_r2_20260728` | 0f88ff4721036f99f8d143418f07e2b07dae306f7aae433c07765608964aa7f3 / a84c6debbd2fa5b9e5534dedc6045b5ef58ba0a4a2d2861226ceb96a80946779 / 49f01308ce4a9b8546dbc1feb9c755bf67c59706cb35519c4dfb94931f5a3061 / 8f136ae1ae6b32123e67312cfc4f2de58ba2fd8e771e6e251d3b118756c6e354 / 79408d5cffcab41034fc22531e6d62b7308b585b8aa4982a278ba61e0cce6ed9 |
| `unified_189k_direct_c_n512_r2_20260728` | 9431545f22efc1767f162fab340f45d4872f3e3b09c36d8763eba48ded514026 / ba1be881657e29fcae046591c8edc94291bcf267b0d64094b721685efb44643b / 9515609229e94f5946e8158a2bea4798420e118cf5ffa67a7ef123ede6be3b71 / 6e01f52969db4a9fd3acdee4297c44dca6466c2ca6c2cbcba2a6e59fb916a5e4 / 9436eb9597537dc681990c8d02f4463699f30af9f87513647cddaa731d1bc65b |
| `unified_189k_joint_parallel_n512_r2_20260728` | 910b59ec316d80d1ac639e82d1dd22c3f10ed04352f1b70f0b58ce3100841f2c / 3bfc38d266c3b6d5770164118f7cf34db48380f648941b456c57d25c58ba8beb / 9867be98fea3d0141d933b2bd708a44c7c01ae7cc7651f121ef18af7fba91887 / 452a0851ba696c744d539f1183c5d8726e9ab87a6d6e8aaea5a0d48bd062a25b / cf72a77c846944cd16feeacfe7f417ab56ae28996061de11c2e843b80b8a5e37 |

### 1.5 P1 CFG／trust read-only screens

以下 first-128 与 confirmation 字段顺序均为 eval contract / manifest / result / records / fixed samples。两次无结果的初始 joint contract保留在原目录，但不登记为 evidence；有效 joint rows均为 matched-reference `r2`。

| stage / run | SHA256 |
| --- | --- |
| `p1_189k_direct_c_cfg111_n128_20260728` | 7cae02eb1990ffd8f5f694d007d90d86e8dabfd17f2373acf41990363cb4fe63 / 9054bf75f2979dc97903c65d3c49859e385ec9e1fb5a0ef387c659a5111756e4 / 64a8b07b6f7bbdc101874d286766389f66537eb2af7d3d6e4d3326b2335c36c6 / 14abfcbde41b8585b3f480505d34c0791c8ce79c4cdc15082d16b684a995279c / 2856f58dc756acfa41d74db8a7d95a8319b59ac28b86c8a43f38fc56053f150b |
| `p1_189k_direct_c_cfg311_n128_20260728` | d84c6e2c3bcde3252647ef92cfe13533e59c66830e4ac7f046b2c8da4873ca88 / 05db9a59a4f7395901f61a30141d61ccf07b91b8b1ffaf750e98f05973360b3f / 9523e52fc6992d5e209f9d04dd3972b31f17440f70ce0592301ddc0cbf9bb5dd / 2fad91208144ef65533cf43391166d74790c72d45864524be844568f53a5565e / a109f79eb1c7e3a354c447a1593c257d01836f6a9cd999f51a5a9e7cbf724da8 |
| `p1_189k_direct_c_cfg313_n128_20260728` | e2f37e11846f7efa211aacbfcf35980a0506d02d103b6bda5f320757c4ee4395 / d57f8a06227071bbf9621575dcd30bbb22b2689e3c74a7ad654301843f19922d / f365f7277e82d7c5c3a723c20e2fc8753b13ac6c8f82d0e019914ff0dfe8490b / 74c6be2218d60f24f0c88d9aea8913a9cd4e4cf948eb27371501a101af004bbb / 09739d13a57e451c5ed7a060d887555ed3df370f9b4b8c79cedc2898e8b9c9c3 |
| `p1_189k_direct_c_cfg313_trustg05_n128_20260728` | 1abf63fded676ca089ddb422bf759412c06a7bb1a429702eaa0b59abba5c1e1b / 35c83c5bd31ba81e94806a5e43efff22d57d4cff183aa350f9275aef4a59cddb / 021f1144f5986091fd28cffd6e71a9be7ee0fb31a08c4cfa9e3df364a13bb92a / 95513123da797fedf4d3574825e75136f59e1055dd6e2583bb5dea5ee94d0cbb / 80710551951f1be96ec9d379a0f29a40cec67201c71ca8fae8890f2d06e7bd6a |
| `p1_189k_direct_c_cfg313_trustg1_n128_20260728` | 0c75742d54a38c088ae8b534f55e9a8d7103fc829dac1afaba5c8aa46a5af73d / 4a7493067a62cf1a4ee20c57b013100bedda066126b6760ad10f781d9b8e4a32 / 00f895fb2897ba6d03a6c2fcc964f8cc5e04e7f818ab8b790a04e89a5d2d5fb0 / 120f1649d64bdf101640a72eebdad6baebf2512ef8a654c7ab422e934971705e / 500c98b7b2944f4823eca77551bbc5265e11365c175a1d1868a4d86da07ebf40 |
| `p1_189k_direct_c_cfg313_trustg2_n128_20260728` | 6ea5df4a30cf23b5823f3e5b9128527a331e2703e005c6222477e395ad114063 / 8308962e6f6f9374c165334aebc6469217421fc09c23ceb27782d62243afe621 / c3d5b5dcbe160ecb7807d20b7613b4a6b9b5474b9a2df6ec8d743442c4bc9f49 / 096a14ccd31bf4bc420a69c1d6af5cb50f687dbc25615d22ad0583efc7615a94 / 53ecb5b6139f431624501d200dd3c67f610d0131c14a1262d2aebfe26f462362 |
| `p1_189k_joint_cfg311_hcfg1_n128_r2_20260728` | 0368194677efb5f6d15a72972504ff4b6d5e422f79e1eb6354828a6611037741 / b567f195263e06d1f6e7bff927fffceb96c698d1aa1d267eb18d81255a75f3f2 / a95cb82dc69aa5f6bda9e5e3e5fb3d665df7684c09695920cba75cb88c946ab0 / 3f23c910dba520cc837b78a7dcd925f073c207cd222a0d5179c2d1039249867e / 94be75f12ce5e091b657ca1aeb6d16ab2ca97f064b3d4571002ffda20113ac4d |
| `p1_189k_joint_cfg311_hcfg3_n128_r2_20260728` | f5508aa5bc8543caa691bed6165b81c1dfbd40cff9f6f79af827c964c8f61645 / 4b92c20f310cd94f2da3d9fce8ed66f5660553e9f4ab32ba5901f114cb8cfa80 / 89ab4d22c7bf2496ead72bb70003f3ebe34f932b7e49d677e927a95f7a1de0f2 / eb5fcd75102a54468b2c1289b9f67e21ffe874b15f18afe5ab57214fbb957c21 / f315807f3047f3516a0a8b7e84e4dc49e3a06034a02ed6bf1732e0f70d57616c |
| `p1_189k_direct_c_cfg313_n512_confirm_20260728` | de7e48d58c55788b48dbe72087e44f0120ea330521d4a379355a5bd4341b107b / 5a542276f63d9701d4c48e526ad2e8a8afc73d8d33c9c0367fe747253529c7da / d43192711dc5a46530563739449be1cef22085bf3d4675322d257dbafeb2f47c / 3c1e19aad57f3d8b3974aaac95b351e7fa9a773a8e0ddebd04349cf211dd8532 / a4b87bef3b7559383a388c3ec7fe27b497ffec7fd6c7fe73d83ce24e31698737 |
| `p1_189k_joint_cfg311_hcfg1_n512_confirm_20260728` | b54b177e81efeea027fecb364a83d97ba98a9c01c5eced22dbc0a0936caaac14 / 4a3a08ef0456a7236e1bc0564c8a32a9df2d11bd65b5ea79fd281d9fcc9b2fd2 / aea64479c970c88d319dadc4518822d8897bd844c3c9a37b9a6e6e30c7daa472 / 5c05ff2c4e31dc04a54661e57379f5b6d5697beb2a032d92888f7c0485648311 / 87aa55460db48deca67fa6b6eba33464c7fc0675edb59b5d87b43796b9786340 |

### 1.6 P2 matched failure replay

以下字段顺序为 experiment contract / manifest / diagnostic summary / gradient diagnostics / replay inputs / train log / last checkpoint。

| stage / run | SHA256 |
| --- | --- |
| `v9_p2_replay175_original_moments_10k_seed17_4090g0_20260728` | 876e7a9898b1d00ecb658c913c0c62ae36bd76d8d7fa9fd769a04d20f46f4e7a / 43e508b0ca822a752f1f7d0c3c0a3e86915d029e64e1be304f3b1e789885cefb / 4d52128f76c7b8d504ebbad19411f0b1fdc930f3a289eaa720fbd46aa4e94fca / dcc7fe5b8edcd43229931d89f8c4472ee141040365d5f324bb01672aefcd98f0 / 2d4b35435440653d89d9eae2e680f2ddce883aea8e47ff61ed5c886a4f41fd22 / 73dc1baa4bd5edcb0a345277984d223f2299feb49673ce71ea5fd3dd295e656d / dd4fc3ddc0c64bd01d2066373915e67404b20a623d49f4ad87abe7de869869eb |
| `v9_p2_replay175_fresh_moments_10k_seed17_4090g1_20260728` | d30f6dead7f9cb5ec2e0b49974b6f73e8ef83b6f141d43ef81e46a23df234a87 / b45e781e50a57cdd2607a27eb8e31d0f50a0e44649e21d09f933981fb959517e / 76b1c190dba9966e2e1f2ea421b010686affaa3e096aff17af6868f842043ebc / 6b2a166a6d19e1c4a9fe40f7f6f758e91f75e97bebf777c0e59fa14630fc0798 / bbcdd1f1a66b7ed486280a77f6595563d2c28a47255c0e41139eadbdb9692da6 / 2196e12513582d423f7f7ca6ac56cf16d121b0d2182acd811d59babd45c24f19 / 7969766008a4a019ed905ec3aaf1d01a7c43fe579c68d94f388797fef197a7c3 |

### 1.7 P3 same-step balanced screens

训练字段顺序为 experiment contract / manifest / diagnostic summary / gradient diagnostics / replay inputs / train log / last checkpoint / selected global115K snapshot。

| stage / run | SHA256 |
| --- | --- |
| `v9_p3_balanced64x2_lr5e5_10k_seed17_4090g0_20260728` | 1b5b033da5fcbe6ea81c5bf1094df17ab7845ea6b8297f3852dae4f99a3a38c4 / 92b25b2f3e393b70f74bca3a60162d013e7b4675075a00a1e7a2b3b971510729 / 9bf03774ec31aedd3cb17ac654582704c6b77a7a7799ebddab69b901b5092932 / 5e1e09d9d6ed68d845ada162337e0a430fe16739209a8dcf81175d93268d5529 / 26e604cf16f0d7550e773c5379ed70fef833d40e6eb072840358871e43ecd84c / 29d02abe28e1baa02daf2aeb4c4a986d3c9f88db7131f7e9baad21492f3ee6f9 / f5ac9907b89226cabc81cef73b805ad7dba094e028916f8a0e3107bda6ef5ae3 / 311e2a66cc769a60725aafc55daf9e5c233a4e15db87b7b3b825e03dfed2babf |
| `v9_p3_balanced64x2_lr1e4_10k_seed17_4090g1_20260728` | 7dd31c70abf9c04310e20b36301c5663f72cb3c47cfd2c5e46ad326ef6a98240 / d43d054e0a25820a86face04d845517c124a882a3183cef1e1ce3a80cbee9455 / 000821f4ab88d9c1756a9f6dd89e4ffb125b459ea3825fb97787f2662f6f559d / f21f5352764e4e4c41f8d132b62a671f972ffd599b64b00ad081c2cae9e1cb75 / 26e604cf16f0d7550e773c5379ed70fef833d40e6eb072840358871e43ecd84c / 204ad9be6672eccf5889929059e62d1ce44f5e597c5fc1bdbfcd33a8fe521c82 / 680c4aed687eb1668f1c14aa789a45ab2fe1da9d18b2aa4630f3f96f88fc69ec / 6f465ff593e112eb4d1f64a404641a80394a24ecc2b1130cb5e63cd8e1544043 |

decoded screen字段顺序为 eval contract / manifest / result / records / fixed samples。

| stage / run | SHA256 |
| --- | --- |
| `p3_lr1e4_global115k_direct_c_n512_20260728` | 7b607bcab85444faea935ea6c6b40e694d4b798a5f02dc515dde4a11347a44d4 / f661205aaa5833b06d7494edcb9426fa649580b526b2fe0361a42c1318cba19e / b195f9fe373b9bf58cf1a79b1b02d27fe75f2b8d4500f06c16a10172712b7b9d / 4f1c9339e9c544294fee9756a2e2aaf88f2119bfa56309a0b7bfce8d13b1caba / c03c0dd5a472c39a43d82ee4a2c0bbeea69ff0a451cd13c5d63600075884af84 |
| `p3_lr1e4_global115k_joint_parallel_n512_r2_20260728` | 74a8a5749520d313affb615ed1c725e66e70b031636b6b83847284bbc09c169c / 1b3865731a15ff1ebfdbd2dda63feedcd658858b3d7edd197e827f6a51a83f08 / 07974ed469bb31dec7a479411cb7737bf442a6ee34ea00cc20d412a88a19f320 / 8dce923961d21ddfcba7f1b0add9f65a02fffd21ffe269f9bd02c5ef1e87cec5 / 15c24ad9153585145e040b26f8a568f74fe4b9ff22f5fa736a998c86c4a31d1a |

初始 `p3_lr1e4_global115k_joint_parallel_n512_20260728` 在结果写入前被 Human functional-reference guard拒绝；原 contract SHA为 `19322d793674b33ff637d1c5d4816a8d38e0967a015d456de2aa370a86f372ad`，仅保 failed provenance，不登记为 evidence。

### 1.8 P4 native component-oracle screen

以下字段顺序为 eval contract / manifest / result / records。两路均固定 global189K、P1 已选 sampler与相同 first-128；这是 mechanism screen，不是 formal metric-ledger evidence。

| stage / run | SHA256 |
| --- | --- |
| `p4_189k_direct_c_component_oracle_n128_5090g2_20260728` | 43b24aa9d43f494c81cec1a0a83336532bb53ecbfd6cc28cce9b12c1af10cded / 398acb79c7728d284e041bdb2af21a3f541225d769ae36a2a6a9737f6542758f / 26621223ed987ea676ee861df02bbb48bf54d16553ad286b7bfbe8c42cc9b8c1 / fd09f4d4b477ee44265be1a2f6ff39d95b0fcfcecb3bcb681dd982962d01dd0f |
| `p4_189k_joint_component_oracle_n128_5090g3_r2_20260728` | 23a7c4e72569285035c0d76c600ba98191e7430c99ca2f12490e55fa0e65f177 / b82e5837fdd3d1ea75177360d4979d3a72d74dcc35986ea63a5b112cf9337c2d / aa980df29b99bed5899443470ddf5a6fd6c6dd4ef82a61e1a8ba2818ee2658c8 / ca73fa974e40f5fbe4e147466006c1e4e2e77302e327fde5e6aad4e740739f3e |

初始 `p4_189k_joint_component_oracle_n128_5090g3_20260728` 在任何样本写入前被错误的单分支 Human-reference guard拒绝；failed contract / driver log / empty records SHA依次为 `8a3d02d106f7103421289b7d44ca30f2f26c2a017a24d3292f1d31f1dbe8e5ba / 05cfe70879de6ad32fda8473fa2e9da0cc63704121943fe65477801ad64126df / e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`。有效 joint row使用 P1 已验证的 matched two-branch Human reference，失败现场不登记为结果 evidence。

### 1.9 P0–P4 isolated implementation

以下 driver／generator在本地与4090远端逐文件 SHA exact一致；原 base evaluator／contract bytes未回写。

| implementation | SHA256 |
| --- | --- |
| `make_snapshot_eval_contract.py` | 1feaf7b2b88ec7671c0624c8688b4f988718dbb80716fcc5d0cbd8de390f7e0e |
| `snapshot_evaluate.py` | d418e1b7cbce2cc154844603be22b92a11a9b0707b57a908c5a4297e3bc72f9d |
| `make_cfg_screen_contract.py` | c11e9a00c101835efe95f30ac3d0960c54ee56ada95cec245e0bc48b32b7b53d |
| `cfg_screen_evaluate.py` | b8114a4f24095b5decfd92368c6e24fcc14ed139827c12fc23c55e01a72b4be8 |
| `make_joint_hcfg_screen_contract.py` | 49f862862e0fddbea671f2e534b0a7c8deaebf6d70628ce0d3aa799b19abb511 |
| `joint_hcfg_screen_evaluate.py` | 2eb22612e254f1c34fa782aa38b0b13bb34cf11c8c36e5d64f0940657ebdf956 |
| `make_joint_hcfg_confirmation_contract.py` | da1e1dbfd101fbc1779957938b74fde2ad559ad5da3cb957d16d3d28fa2a18f5 |
| `make_camera_fix_contract.py` | cd8f4b175713e57759750e7c8496c58d0300095ca8278ea8fcf9ab076791688c |
| `camera_fix_train.py` | dea0054c78060c9218d1d2e9e8617ff2bf308290310056f864b26c7c7de4a4d6 |
| `test_make_camera_fix_contract.py` | 9cc12130a11f22950126bfcba0ce880aee899c1ec0fdf317ed9723c5935a59fd |
| `make_camera_fix_eval_contract.py` | a539c2f668760ec647c049750f160d86c3d25422a528f88d1e3bbb2b63edadf0 |
| `camera_fix_evaluate.py` | d0d1e7cc1054cdffcce13ce857c869ea25301e991dda47e6c348b73003a1dd05 |
| `make_camera_fix_joint_eval_contract.py` | 6734aa5a93cc2dbf680b81e4afb69ea6c7788610ede12bf2f5664ade21b7b86f |
| `camera_fix_joint_evaluate.py` | 4a20afda59e477327db08c5e8b206682ac95a091f842e13cf6070afed46be44c |
| `make_component_oracle_contract.py` | 187f74852dbc5ee7d2c50485fe4ecd46f31f5eef7abd2047eb72f445f9f53f41 |
| `component_oracle_evaluate.py` | c55583403c78838ddc7d8933ecc1ab89bde033509a605891fe3bdf436293a853 |
| `component_oracle_joint_evaluate.py` | dd2bc317fe980c2938283383277a1318552e1dbc760492ede084fae3e02adf49 |
| `make_component_oracle_joint_r2_contract.py` | 3b8222d567a20994bec0aaeb356cf86107a5992bba6fc501cc0d42fcb3ddbea5 |
| `test_component_oracle_evaluate.py` | e1ef93c367f00e4791f082019493b0f76b82dd4e2aaca98d9db0bc4e14b73361 |

## 2. Naming map for former shorthand

| former shorthand | descriptive experiment name |
| --- | --- |
| E1 Stage1 | GestureLSM part-wise RVQ Stage1 |
| E1 Stage2 | GestureLSM zero-start generator Stage2 |
| E1-R | GestureLSM observed-start continuation Stage2 |
| E2 | DC3D MinMax observed-H Camera completion |
| E3 | fixed-C3 DC3D-light observed-H Camera completion |
| E5 | C3-MARDM-H105K |
| E6 CLIP | C3-ViMoGen-CLIP-H105K |
| E6 UMT5 | C3-ViMoGen-UMT5-H105K |

## 3. Historical organized registry

### 3.1 Stage1 core artifacts

| version / run | Stage / status | checkpoint / owning-decoder SHA256 | geometry SHA256 | contract / audit SHA256 |
| --- | --- | --- | --- | --- |
| v7.14 / joint AE official r2 | Stage1 former mainline | 91248bf440a4a5493a0f8b4994d6d36479fcaa221d331f6995a91ed1af8e7ce1 | abac845f8eac2b3c6da9beeabc02d26058e17b2007fa93d60dda54e7c3ee5248 | evaluator a52aba4d6260aeefac4e5891fbe510322bf6eaf12ce98e3d0bda16ffbc8ddf5e |
| v8.1A / yaw001-root003 seed17 | Stage1 full | ac47c2191c44d6368a5468510975cefcf0efd1338b03ace50266830c344151f1 | same-script evaluator above | owning checkpoint verified |
| v8.1C C2 / center100 seed17 | Stage1 full no-promotion | f16fb879eb7feebbebba10d24c6039cfec4fbc7812492fadedd9cb5c9c73530e | 0f4cddf17fd15a4b73afeff17c2b489702f237928b099d9d699340eba2f31d96 | contract 904ae14866b0a62fed37cc0b09de5f6bf9d177f81cfcfea760fb96247bdcdac8 |
| v8.1C C3-25 / seed17 selected | Stage1 full；exact Stage2 diagnostic parent | d0abb3268b14c19aada48fd2b9242fbbb03e9d808959539cac47f33448e4788a | 8b0ab3ba82f85192adeb066d99ce6a07f0fe645b2e916300c96e16b4aad43f4d | contract 80fbf5743aab7517acbfe9bcff6cde4311ce9257cd477e7af5baa658c2de6e73；audit 75d2daf8cd39d91affae8181cfb1365efb3a52bfbc85f50a1cdc6b7d90cf9b15 |
| v8.1C C3-25 / seed23 robustness | Stage1 full no-Stage2 | c73027b8f4c114c1c2ba54994c576592cb3f223dd7117fac7188dba9a7b0d3ad | 8e5a44cb586eeba1cbaeca82ee2b731badfa4dab4f15c40f11ccb7140f3a1b34 | contract 32ce7f8d1a91c75afe821659a2235d3ed05f8878380b79a7c7dd44a4e20bb4c1 |
| v8.1C C3-50 / seed17 exploratory | Stage1 full no-Stage2 | 4c9b51778104aef3e85f2664086a22802988a9a23833181026c6facdab608d98 | c0bb55bb244011ebffad5911d9ba43a7b4ba1b28bcc031a6df58e0f2158f89fc | contract 98a5aa0c00c14b30bb23c6a4ac1fe80a4397216f408f3ef3d48196c92edca8c3 |
| v8.1C C5-B / fresh calibration seed17/23 | Stage1 read-only；doses frozen | no checkpoint | seed17 c5755cf277da27fb62bba9518239af2a55eb9156acd994b196d1e665860832d5；seed23 561b1c4f43f59a06012b1585c49a58729d02d0a3382db5fc86e6d434137cf0c7；frozen doses 9042aa679a97c41b75fd9b2eb8b7854f141bc55c5df8a5bc4d0a153f3d6ab720 | contract c735a9c4aa7c7bcc8a56924bf2266d93333244d5f1f232b8114930e18b3b32c0 |
| v8.1C C5-B / seed17 control | Stage1 `10,176` matched comparator | 49b4e71ea0225ad299dbfd2b9c8590c372deaab1b8ae03044a0c5d7138f825fa | c74393c248b016237ba183ff904e83a23ef962191b4b7dfa90e47f643200d043 | contract 523f187c3baa687b93c5292e86bb043ce2194225f5a4a3595853aac351e3051b；shared gate 0260192649bd0eaaa179fb5d39fa8d62a42f4db7744e2d28bd9974aed7b6b766 |
| v8.1C C5-B / seed17 dose0.5 | Stage1 `10,176` target fail | eba485badc38c762bb55bb639dc1e83b675daa3d3b1f4483ad573c55832298f3 | b8291f8675c13972cfd859cd7f5eb5b186bb9acbb20ff8a739d4b483a7567a54 | contract 0e6cf69d6be78e47c86abd229b9bc8a7ac5272c48b5a4dddf3733923066623b1；shared gate 0260192649bd0eaaa179fb5d39fa8d62a42f4db7744e2d28bd9974aed7b6b766 |
| v8.1C C5-B / seed17 dose1.0 | Stage1 `10,176` selected for confirmation | ad6e32dbf4865db68b205c0aadcf3e640641d063e37d2b8a77a93405d825a05b | e765454a74c4c25d867cef602fab42a8f20b3b01a2f161a51fdf6ab300471edc | contract e9a430428c22efd804e41691454f8a7df7123529d1d18c3421272f462ed8092a；shared gate 0260192649bd0eaaa179fb5d39fa8d62a42f4db7744e2d28bd9974aed7b6b766 |
| v8.1C C5-B / seed23 control | Stage1 `10,176` matched comparator | f15ada53e469f43ad209531edde505083b7b3881538f2aee2cb16ccf5fa5a984 | 00a7eb840b42dee68caf16b81c3af881c766a6f7f4a4e3a155dcaca8f225535f | contract 32a5c5fa5d1d0eccdcb5ccc7e87448491afd9f904721ff26c1b44244114a2d23；shared gate 6bed0bc8957c691f7f448165d30fe5703ebf35ee7bb515eec90b7e818a43ce88 |
| v8.1C C5-B / seed23 dose1.0 | Stage1 `10,176` confirmation fail | e1cb80a10420ad0ffd703da1060a93630bd7afb9252c18c72783da27cdef36d6 | 189996bfcf5d3fa85a4d13b4c2586546baa2a0b9005939b86075565dae091c42 | contract d1731adeeae99dbf1edb56628067f83f845d5689869be556d3011ef0f023ec21；shared gate 6bed0bc8957c691f7f448165d30fe5703ebf35ee7bb515eec90b7e818a43ce88 |

Stage1 train/eval ordered-ID SHA256：a0981b6c6223409d656ad8c43cfcf95cae6ec9a28640143b87b6322292c51dc9 / a0d7627ee827e36a229d33f9975f8417ae78b504cd5a6db1edf62cb1a9266b93。

### 3.2 Stage2 core artifacts

| version / run | Stage / status | checkpoint SHA256 | owning decoder / cache boundary | contract / audit |
| --- | --- | --- | --- | --- |
| v7.38 L0 / clean | Stage2 105K former mainline | ab474d353a29a4ee707c8ed4e37599fcc47ea79c124452ebdd366d5bdafdaf35 | v7.14 owning decoder | 20/20 family artifacts audited |
| v7.47 / official-AE Unified | Stage2 105K S-control | b8c06913a5efdbaa0c178e452998352033174614aa0a60ad96920fe14a8acbb2 | decoder e0ff0a66129d77eb27a18d0034b23f692aaec3ef53afd540097d8d9544a73e52；train/eval cache 1924c632…d1e8 / c642f7c7…d1d3 | contract 37d61e28076735979731e47712500cee016365a4e9e2eb7753d93a10416dee51 |
| v7.36 A30 / matched control | Stage2 30K | 7dcf3b1911af144ea9ef2b30017dd07472d62f655fd04c1dc9263581e3382c0b | v7.14 decoder 91248bf4…7ce1；cache f7a00a48…a5983 / 6f13816c…9b25 | matched comparator |
| v8.1A G3 / diagnostic Unified | Stage2 30K stopped | becc2c11051bfd7857acb0602f61c755cd664969f34acef1f0232711feee5bb8 | v8.1A decoder ac47c219…151f；cache 3b55223d…bd22 / 1050748f…541d | contract c841fda54b8611d27b59aeaa3ca3c74c26865eee100428828df8c1e73ca5ab59 |
| v8.1C C3-25 / former-mainline baseline；historical diagnostic contract | Stage2 `0→105K` completed；30K/105K formal passed | 3533a4216b441b8fba0d6a791408d60a8708dc9a44e47b93d3187217ee83e226 | C3-25 decoder d0abb326…4788a；train/eval cache bc8c847e…3fa9 / 39485590…f5d6；full-cov stats 0c97d247…3400 | step contract 963327e766cf5acb168dc668616f7098df94c4df50b2a160299bcfcd2d2fe066；contract audit 6182d01d6f3ff4179b8c4f7b8d543d78f3fa4cce60b3db296f10e461e2daf597；H/C/J results c35566ed…b84b4 / accaa2c5…c5ea / 1606e328…9e5b；records 9e34e94d…d07c / e8ae3261…9dfb / 375e9ec5…b772；audits 11afdefc…7df6 / d7733761…8b90 / b6b747ec…925a；historical flags retained |
| MoMask-Pulp / native seed17 | Stage2 native formal Direct-H | VQ e21d42684e4441b67782b8951e1a5e6c9e5c25bbd1bc460aa7fda138ea348664；Mask 037871329eaf980e320961445f5492c7a79ad85d60e9e2b79640678dfabeff3c；Residual 89faab30ffb62d185a789a814ae7c061ed5f5375f9ce5128dc4764756c43e0b1 | native non-causal RVQ + MaskTransformer + ResidualTransformer + owning VQ decoder | eval contract 94a217f900e26212e523dd1f0444fbbba5e6392a7c424e0441bab19c02238901；result 3a133b834bfac8203a9bfb92cea55e0127f50369bc51c68a53bb3b0d877baf70；records 6545ab1a4e17bc13b73663aafd983b439ccae664b016251640dcc22a0e067ed8；formal audit 71bd4b1d31409a8e70e991715ee7a09ee1706384df39831ea575e9f4a2ff3232；byte-exact replay audit 0d7d549e64ff863da2f4815245c18ecb03d997ecc1cef3f423ae817c90f28c2e |
| v7.45 / MoLingo human | Stage2 240K formal Direct-H | 4669a56fb6c9a4adafc2cfedef39b27c060cd00949a7407c86c68cc9fa30200d | corrected v7.14 latent + owning decoder；offline bidirectional masked RF | contract 34544e1588a5af63614a1b04c50e2481c6f73ed97e21cfc3ab93ba657a2d163a；result 445695958ba86c11831cbc8f931939c71f72135453b21ca6b6d5e2f170b6f685；records 6edb7d5f9e54a61540b175028cad6911d5b573d4290e7dc95edc7e6fce122a9c |
| MotionLab-MFT / v7.14 latent | Stage2 30K formal Direct-H | 45477134830f25c58b6db2ea54cfdce4cadd8f0e84c0e9312f1ead73bce468dd | corrected v7.14 latent + owning decoder | contract a2f4d063bad486075084d9a66d06084a430f012d28356f42a4b161f8eaef8002；result f1a45654d740d8937152c96b75f88a53a765bc37977719d6628ccef6c36d79ba；records 2b6d42544e75ad330e01091e4a3a294a67e02f2fe0db17ba14fc12e5afdca765 |
| Director-C / native | Stage2 native formal Direct-C | ad27564052465ff11f5264c5606473f2daacaaf74abbf45adc7b563328b5e823 | native direct 9D C2W；GT pelvis trajectory；no StoryMotion tokenizer | contract 3a3635be17fa1c6cc155fa8e5ad7339d46e446c55195ec9ca1b350390addcaa1；result f9693592d62780dd2a4ed330dc2b102b88b775a839e459c6adefc6eb2bd97b15；records e0734d76e316dc5f66149214e2daf7cbdd42adaeec17c796a1897e88dfaf2e4a |
| CCD-Pulp / v7.14 latent | Stage2 60K formal Direct-C | 8014b120c218a7ce8bd7d6f6c3e381cc009939950926da847c4dc2597f6603da | v7.14 cache + owning decoder；GT-H latent | contract bb1818fb9703035d34bc691bdbffe82a3c9447c9c68a3b6010cd3387e5b93039；result f016ba46250c1bb4895aed14b447088852658c9ca025f2118244b0ff9a144e5b；records 19354e7949d004af4057269f432b47b6f33392a8ceb1da376b1e2a05c64ba9c0 |
| PulpMotion / official DiT-xy step92950 | Stage2 native formal joint | 7c11cb59d5f51b9090abc1448e76329d157459fc30485031f5a79a7a119660d9 | released Pulp AE + native sampler；same 4,053 IDs in native order | no-Aux result 499db08e4f957f178cebc9b8c5f07dbe53ed680bf1bce657c2b5438e1ebdbbf9；Aux result 5be1e1e30213e6415c0a057eca2a444af31c30614fea1517cbd2f2f3b637961d；no per-sample records artifact |

v7.47 official pure4053 ordered records SHA256：a0d7627ee827e36a229d33f9975f8417ae78b504cd5a6db1edf62cb1a9266b93。v7.47 training script 与 L0 historical training script SHA256 分别为 71a9a2a3b700d4f0a699fda5f28bf8da72f563c20871e1c1cfb5d4d4cae0ac08 / f207c840fa363afc13e308047ddbe3900683f048366c10e9c135b49a2da886c8，因此 strict representation isolation 未建立。

### 3.3 Diagnostic artifacts

| version / run | diagnostic | artifact / comparison SHA256 |
| --- | --- | --- |
| v8.1C C3-25 D1 / continuous diagnostic | full train estimate + frozen eval cache geometry | artifact 2f5a64315d8cca23d3d432bb872bec55ba72fdb775ace37b26019c78c05002b1；script 98121fae2392aa0909b5847ac46c917d4f91751bc325cc42c3ffcfe51f593d50 |
| v8.1A D4 vs v7.36 D4 | raw residual propagation | candidate 142614050c5d94ae8e0e680327129a7893d64afcd0cc3ff0070aaf3b1a02274f；baseline d22a13b9c0974c7610f7142c3b73ac6876ed5fb368ca0cb8ee8808550519469a；comparison 13f9715b446a33d32181a231b2a4eb7bd17eddcb2044b8c2228cda8cd4e20727 |
| v8.1A D4.2 vs v7.36 D4.2 | Camera-text reliance | candidate 134195504286677d0a77c0da6ee7e8a897008525337a908b91506a301dedc795；baseline e8064825521865a74081c79f40b8d5481c72df1969521fd762eb27177ddf4148；comparison 8d98765900ee9f9683e84b3e2de309b66ae92733de41ce49490d9b149f5baed9 |
| v8.1A D4.3 r3 vs v7.36 r3 | decoder direction sensitivity | candidate 58b6f62c6004e2ef24f94bd831790058e0e799e29650f1622a0a44e9eee19d7f；baseline 370e30d190deb63e66e675defc26265c103fe1c62a860a982e577597ad8e5c07；comparison ff0df9c541f351827ae234700b25cf5f9f355ec369b0c9f7c8525de0ab7ef7ae |
| v8.1C C3-25 D4.3 vs v7.36 r3 | step30000 decoder direction sensitivity | contract 2c8294f034d1911900f308a11e183122900878b979964fa438b0ce5c163f1fa9；raw residual b82e1f6abc805237d7d702fb18ccb42f65142470eb7bce989ea973a0768689b2；candidate 88188b5459ed4835dea1d3c38039b6b3e5ca336aff9cbac218ec381855c8eaf6；comparison ff15128b9d36d79e718ef4556c26c157d1404e3932be165546b31005d32b7393 |

### 3.4 Relocated legacy identity blocks

这些值原先混在旧 metric ledger 的机制诊断与 matched comparison 段落；本节只迁移身份，不恢复已退役的数值表。

| version / run | artifact role | SHA256 |
| --- | --- | --- |
| PulpMotion official DiT-xy | native-order 4,053 ordered IDs | 16d73df1916048dc44d407191bea9d3589113b55e22281b1acd574b16b9a8196 |
| C3-25 joint condition replay | source contract | 7af1bf9a49a92609dcab1a1d176fee622b9ac844fc2add053982ed036e667851 |
| C3-25 joint condition replay / GT-H | result / records / audit | 6eceb3430eede08eb5ac5a49015932e03131bc762ef89ee98e494c6eae711c9a / f80f54f8092f1a3521eeaf1f846cd41f30f9a64dd19ecec2fe79ffb084c3d16b / 19da362eba46c020ebb890a3285f28a934952aae5a31e0045e465a3b40546f04 |
| C3-25 joint condition replay / generated-H | result / records / audit | 9d92edd0900eb694e55a0a82bd895142dcf50933b780fee167246ad0b9896a7e / 3c6cc3ae8c395c31f7e2569060e30c49366b8498a7aa416c892e82973f284d95 / efeb2c49200d9c76ecec1421462c44558d708272b46005314775824e53a411d4 |
| C3-25 joint condition replay / shuffled generated-H | result / records / audit | 2e6805faa59b4c291a7407734cd2ed5a5070f2f7aff36f6acda24be5ba65ad49 / 456a60f3a846337478d5941d41e2b56232b765444bf8b9a8363dd94d17f69f8c / 79214c0065cd2d4e1804b92f8eb013d8d4ef5bd14170a020330f540b3f88ac20 |
| v8.1A 30K corrected single-step | source checkpoint / ordered 30-artifact set | 82078ab184084db3e7714f67e8b876cd8cc4c0e9109225affd095fac7642c61f / 6c85631adaaaf93271632cf8aaf18ce6c3a853e69e5506d362663cd3791ff487 |
| C3-25 30K corrected single-step | source contract / corrected diagnostic contract | 7af1bf9a49a92609dcab1a1d176fee622b9ac844fc2add053982ed036e667851 / 24a7752efae53e5a6e022feedb39e2a614dda2faa1b61015514afb9e8fe8c9f5 |
| C3-25 30K corrected single-step | audit / ordered 30-artifact set / final manifest | 11d59f9f898177b84525c09d95c0ceb5b727ca0aaeccd0006f6a8a5e94444806 / f0f859f023eaf5158720780f43bb776d0962f77821fcff38b1b0b7c3274716ba / e9b49bf6f61c8da8f45401381ab22fc4d90c29e14fdcf82339a3c6250bc4e1f2 |
| v8.1A Unified-3 105K | checkpoint / experiment contract | dad04dac44fc778f02566d4221377e02aded322fe7e72bdccc01869245438b73 / a36dfd3664b23404959a4b246eb9d3108367f5e8500f9a4440835fe5bd12cd47 |
| v8.1A Unified-3 105K / Human | result / records / audit | 4558dad025adc01c8ac4a55211e23a1ce5c2d18737a34f4d457d510bf36f4901 / b92e22a2bef69ae31a973606299a7a60d049fbc74f19970905996bad505e8352 / 95dba60f9d0bd2a6062eb972a3e87836912d580b85439ea30edc576c98ed07c3 |
| v8.1A Unified-3 105K / Camera | result / records / audit | 2c1eadf434465bca3c705b351beb706128178bbd10e507b88841b3bbad4d60b1 / cf9c090c193527fa988defc900712f317bc46ce763725798ebcd31f867c4c330 / 7c14ee14b3a279901e86911d7d96c973b17a377ca6d5974dfd22d973b9e99f0f |
| v8.1A Unified-3 105K / joint | result / records / audit | e9da34e44d0103b717248071e6ce4688fd073d478eb7affb5912935aea10c5e2 / fbbf5d16667600009b27240bead6765e5dfae368c1762c807770924d713c0fbd / 8637306a7712dc8eba06fecf666ba562740fbab5e391ef47c62075c5a87e2fa6 |

> [!warning] Incomplete historical token
> 旧 ledger 把 v8.1A Unified-3 105K final manifest 写成 `42a0effef73909adf7eee39cad5f9dfa4a0ec4da6f0057dcf57bba411fd9`，只有 `60` 个十六进制字符，不能当作有效 SHA256。本页原样保留这个 provenance token，但在重新取得 immutable manifest 前不补猜缺失字符。

### 3.5 Evidence roots

    runs/eval/stage1/v7_14_official_contract_20260710/joint_ae_v8_schema_reaudit_20260718/
    runs/stage1/v8_1a_joint_ae_yaw001_root003_seed17_4090g0_20260717/
    runs/stage1/v8_1c_center25pct_full636k_seed17_4090g0_20260719/
    runs/stage1/v8_1c_center25pct_full636k_seed23_5090g0_20260719/
    runs/stage1/v8_1c_center50pct_full636k_seed17_4090g1_exploratory_20260719/
    runs/stage2/v7_38_l0_clean_lr3em5_105k_purefull_seed17_4090g0_20260715/
    runs/train/stage2/v8_1c_c3_25_diag_unified3_105k_seed17_4090g0_20260719/
    runs/eval/stage2/v8_1c_c3_25_diag_unified3_105k_seed17_4090g0_20260719/
    runs/eval/stage2/v8_1c_c3_25_d43_decoder_sensitivity_n64_seed17_5090g0_20260719/
    runs/stage2/v7_47_official_ae_unified_matched_seed17_5090g0_20260717/eval/official_pure4053/
    runs/legacy/eval/stage2/v7_36_p0a_asym_unified3_joint30k_seed17_4090g0_20260714/
    runs/legacy/eval/stage2/v8_1a_diag_unified3_30k_seed17_4090g0_20260718/
    runs/legacy/eval/stage2/v7_45_molingo_offline_masked_ar_human240k_seed17_4090g0_20260717/
    runs/legacy/eval/stage2/baseline_motionlab_mft_v714_human_seed17_4090g0_20260716/
    baselines/runs/momask_pulp_human_native_seed17_5090g3_stage1matched_20260716/
    baselines/runs/director_c_pure_matched_seed17_5090g3_20260716/
    baselines/runs/ccd_pulp_camera_completion_v714_seed17_4090g1_20260716/
    runs/eval/stage2/pulpmotion_official_matrix_20260616/full/

旧 v7.17–v7.35 collapse/condition diagnostics、v7.39–v7.45 operator screens 与 invalidation provenance 仍由原 run artifacts 保存；它们不再复制成第二套 current ranking。版本族中的已闭合 milestone 与 bug 入口见 [[version_family]]。



## 4. v10 Phase-A Human 与 Human-relative Camera 前置实验

本节只登记两条4090并行前置实验的 immutable identity。Stage1 run与Human teacher run没有共享optimizer或Camera参数；二者只共享同一个Pulp-only Phase A `step_210000.pt` Human owner。

### 4.1 Stage1 Human-relative Camera old-3-loss Phase B

Run：`v10_hrelcam_stage1_phasea210k_phaseb_camera48_210k_seed17_4090g0_20260729`。

本run的immutable数字与文件保留，但objective没有framing反传；因此全部endpoint／selection identity只属于historical diagnostic，不再拥有resume或cache资格。

| stage / run | immutable role | SHA256 |
| --- | --- | --- |
| Phase-A parent / `step_210000.pt` | owning checkpoint / frozen Human parameter state | aade19d4948e51ae635fb2dec712d1e4e63cef6cd4386f4c1c5b49b55e2493c3 / 1c9b82f35b16da8351ac35e2c41478b6a9b59bca23d2c2a8ed0dfea214478d44 |
| v10 old-3-loss Phase B / full run | experiment contract / pre-correction selected manifest / current audited manifest | 108ca7fce71326b3f9c21ed6f53cda23253ff9937159fe1e71bf88ff463d1669 / c1e305c8fd2ec5ca9619f9bea918c2fb163245b765b6b846ba3eab9584dd7cc3 / 2b45cedac35c635f1c037b4bcf704970dcf8dce566a056ed166bddc1055dd914 |
| v10 old-3-loss Phase B / normalization and endpoint | relative-Camera train-only stats / historical final `step_210000.pt` | 9d58b99a2edc701a5dc4cfdbb67cae38676453566b4e3f15b7447ef95052cbfc / 60f7ca14cd9e80f062b67d2eeae340c8f28ff9ed76b613f1529dbdbd57a969fb |
| v10 Stage1 Phase B / formal selection | selection contract / legacy mean-aggregation selection result / min-max policy-correction audit / pure4,053 ordered IDs | a529ac8445c5aec986eba6cd172134411e8cb76914ac12782617308fdcdca63f / 8cc5a8745a837d21db03161da2ed7ba78719186710efdd60886628b140fef897 / 2847ba3c23525fe91a52c550def282f7b67b47058d727702d5aa3dadd525c79d / a0d7627ee827e36a229d33f9975f8417ae78b504cd5a6db1edf62cb1a9266b93 |

四个formal候选的字段顺序为 checkpoint / eval contract / result / records / fixed samples。

| role / step | SHA256 |
| --- | --- |
| framing anchor / `110K` | 8937af522ce33cbd826b56f459a4d7bcad871ce255509674354f1e357a61cb0c / 13ab9e500b37a00972591e08e69a6653adb8d238821234260b1607c9e50ba917 / 316a7c4df5415a1bc04607c24265006f454ed62ab9baafde9c25a2b4af4ade33 / 4c03d60f89f538088b7b30e421659d9c5feb779132d8a6e48b826c174be7bdb7 / 0daca9c4cbb92ea7cb23184a551cd91a3498d725d69f1c4b0a14942ff43b6e25 |
| field-balanced knee / `184K` | 2f0fb7a22de1b6a458c3c60b77b6bcbfef2e851c63ea6c9a53559ffd32a59739 / 1cdfbeae8173ef4ad177512cbbb64906e050d2935db4f215494cc99d7f931a8c / e65f014cc5932e374665a7d6f9ee50ad2484b6eab71340cbbeb00acda2917ded / b3db050f43478550afa924d6bee8a5af54f0dfb89dc214251e99e953594350e3 / 405595ba11860f8e2581fc40caa4dec969a70cd8e6a922f394a8a8ccb31fe4bb |
| axis-balanced knee / `207K` selected | b39793182f805cb08240dff9dbc2f13bbd0f33f2700907f58a02ed6ea003626d / 80d72deec8be8105f40bc10451c83ff207d64bf9f6dd3cd9be17aa58fe8ca0ed / 1832598a3193e68feaf9b2bdf8dbf13c86197ad664ab144fbff6fc165dc0f4a4 / 408919045e61dc69a18a749b5af0a95fa665eaea9b92cde13c928ac836be150d / 7af85a81d1587713e73df3501ea5d8ad528696b49f49e88a83fa0031616afa14 |
| world-geometry anchor / `209K` | a37a3e3c46d79028c5847108a2f05820a8d7b6a63784917486b8b9f8547cab02 / d9e435d5e5d11df90b156cd0fcbf85ceba01a2905e6624c65ce4d8bd306f9ed0 / 0dc484dd415646177c9917f5d4a71143e7a564bdd0024fb0ba8a7b7825dad50f / 129161af9b10416579b148858cb5818612b7c2a155a17b755d38f2fbeb8c5adc / f1c5e400743b53dc8fe111ebe864a999827e5a71db6c7e3616f1ec39dcdb7a75 |

| stage / run | immutable role | SHA256 |
| --- | --- | --- |
| v10 Stage1 selected207K / fixed8 | visual manifest / contact sheet | 2160e555f19ded87972d2a5fffbecf9511e3f7a32da7e3beba2e97afd7695480 / 4c555b7cbaf59885d0b344d3e38889e16e75f963099a8cdac1d088fac56daf31 |

### 4.1.1 Corrected-framing Phase B

Run：`v10_hrelcam_stage1_phasea210k_phaseb_framing_r2_seed17_4090g0_20260729`。本run从同一exact Phase-A父权重fresh初始化Camera branch，不复用上节checkpoint或optimizer。以下登记immutable preregistration／preflight identity与已闭合的`30K` screen边界；mutable manifest与普通per-step checkpoint不在本页追写。

| stage / run | immutable role | SHA256 |
| --- | --- | --- |
| v10 corrected-framing Phase B / preregistration | experiment contract / relative-Camera train-only stats / preflight result | edeb42d7b7cc7702a39627f5095cf84e47a7931106513ad1c3217aafd3825a19 / 29ee9555ff1a83cbc955378ae3359ec2a7b82b3127286060ae3315bd036c976f / 22752babff8cf9aa52a784b7773ac2f368e3f4501a0e4284e97b425d9ca1a521 |
| v10 corrected-framing implementation | model / metrics / trainer / config | 1643ea4efe5e6f0aabdee177c66be3456732a6e8b0b96cf87131bb749ed63ec8 / a280bc05e73d7b7b172097e426d5298ee2ae7333511faa63c305c3b41fa5269c / 3e504d29a870639a8873bdd230cf3b1f51a4ed3e2ab495de35ab7860214a807c / 50c3b3fad70f1a222d8a8214e3dced28455ea60f50da07c1377fc495c4f94606 |
| v10 corrected-framing evaluators | endpoint evaluator / formal evaluator | 59ad18b34eab902e16c15c841d65c91039bd3bd1fa9db9122b8ef4e39292309d / 4b016bfcc23f3aa10b55ba38436cfe68f0a140222e13c40374473e74097bf468 |
| v10 corrected-framing gradient regression | `test_model.py` | 330cd75c07d29a2e2e9428e96b59d98cd9f851effebdd5725c651382e544dbcf |
| v10 corrected-framing `30K` smoke boundary | checkpoint / fixed record / fixed first32 / smoke gate | 9a14f1753ea7cde623cd03cd4fb215897096c07f3d01d84e9af4127182f784e0 / 4045fc96eb5831a85a28c8f8580d2d283120b7a1355c69f49d1b07c415cc7b67 / 55977bfc5711cc185dec4cf02353594a8d3a47b027b1429ab29219c8f8bf7c6b / 8fb67fa2d8602c7cbbb3885620feb45eac51a5e1314921a271238eb43ffce591 |
| v10 corrected-framing smoke gate implementation | `smoke_gate.py` | 69160acd3c8948c133532a196e9dd2e0ab50e00dd676591c9a3dc70003c0c8e4 |

### 4.2 Stage2 Phase-A Human teacher prerequisite

Run：`v10_hrelcam_phasea210k_human_teacher105k_seed17_4090g1_20260729`。

| stage / run | immutable role | SHA256 |
| --- | --- | --- |
| v10 Human teacher / full run | experiment contract / completed manifest | 8dbace244600d777f8c7d631d30302fd2f62eaef82796f02c33e9f68cb2176d7 / 9fec940b97b222eb0791283306cad3f3ab6efa53d4b1d1a4db0465ed36269b1d |
| v10 Human teacher / EMA boundary | `teacher.pt` file / Human teacher parameter state | 5bd3b06c2078a96d45f7915a3f1bd35cc6ddbc8926d661b9bdc99c56126e3bc4 / 10ceba15f4eb20c035e1697f53c129a5d29d3d7cd11467399cb82e015000f25f |
| v10 Human teacher / cache boundary | train cache / eval cache / Human train-only stats | fff5f4bf31c6d4d6ed79a82983d405aa4b25b8cf49a87949353d091eb9773240 / 5d3a9b25e66e2d9a86725467ab448cb68711b9975ac1b06f9524c116c07f82ca / 630bae776ffd2c565329b55e12b1acb9ec99188b73c585078494937e9c9e7e3a |
| v10 Human teacher / Direct-H N512 | eval contract / result / records / fixed samples / ordered IDs | 01923360abb956b9feffc53edfb04aac96e3699e36ab3767e7b20f35325e9884 / a9d4d8fda8e0f8e7071efbf5a56dbe211120e2fe75fc5c56d87c007d86734582 / 3c3fb8c8b750c858361d4cf1f9893c9cf43da3a9d6586d5f4a4c0a1b965ce937 / 145018b6155f8fc8a70748fe1c9f6b05e6ef376efc5c58e4d69a3a93bbe308b5 / 6b9c92a533d2d0aff76cce6c7ad23361733fb38d3157128bf7eee56cdc33d8df |
| v10 Human teacher / Direct-H CFG3 N512 | eval contract / eval manifest / result / records / fixed samples / ordered IDs | 8fc0b7989515c78804cac2929a8b7200cf735da1251df0fa74ddb6581a13e807 / a84e9862149d7208b3581ad583b1d87827f92da2149fae8241637b0a5e957c35 / 31bacab0bc8c9f6c34a2dc4b8c3fae66d8c0ea4f242b83b5ad1fa0d8dce3f0c6 / 27787737a59fc3741b8834265d10e7a3ab3b9198d678fd887e34bdfeaf1a3d48 / cb5534b6ff19b12e4969ff0c850db86ac2af4bea3d5ae64342c9609df7a687c4 / 6b9c92a533d2d0aff76cce6c7ad23361733fb38d3157128bf7eee56cdc33d8df |
| v9 Human teacher / Direct-H CFG1 N512 matched source | eval contract / manifest / result / records / fixed samples / ordered IDs | 0f8fb21b3c095eb5fb1d69c008e8b32328c1a64ba039ce00f63018ab50acc081 / f82f40a7b1d86bca772c9a29ea953f40e5c88fb77454361a27d4bdca63a66f77 / 9d0a5b9ba5b9220e926db750713c0439ca8a49e6b823a77d1d693b2a3182de31 / 1042499837340b7afc59be3997439411450e2623776b2fcdbedfbacf990bd51e / 89e64290cc9bd3988104eef0ff7965fa77ef343c8c514b149b0f1d4baeef9daa / 6b9c92a533d2d0aff76cce6c7ad23361733fb38d3157128bf7eee56cdc33d8df |
| v10 Human teacher / fixed8 | visual manifest | 2b1150494985aebc02f9504d83e336ed3188b1d1226ceb9b46ed7e4fee871088 |
| Phase-A vs Phase-C Human owner audit | audit JSON / v10 fixed source / v9 fixed source | 356cedb539755e3a56ebe3209baa71dad9221d8960cd94f7b8bd4e81184bf66a / 145018b6155f8fc8a70748fe1c9f6b05e6ef376efc5c58e4d69a3a93bbe308b5 / 6310a1b32396247e79175aac67ea0155438f0ba88010c005545029e35eb3fc16 |

### 4.3 Formal evaluator and renderer implementations

本地与4090远端逐文件SHA exact；Stage1在fixed-framing gradient regression加入后为`10/10`通过，Stage2为`8/8`通过。

| implementation | SHA256 |
| --- | --- |
| `stage1_human_relative_camera_v10/evaluate_formal.py` / candidate eval and legacy finalize bound by selection contract | d68f384cd3e2c3a54b408ac643ed8ff4f7cd64ee0de84c6ff99b9883668a808d |
| `stage1_human_relative_camera_v10/evaluate_formal.py` / corrected min-max finalize and audit | 87cdff609ac0ce3a2bb866cd26f9d20bc6cc9c7b4086444e4ccf66c77b130e54 |
| `stage1_human_relative_camera_v10/test_evaluate_formal.py` | 1052c6fefdf3851f7df5920c1a9a94c3228436831f13ddab26fc19c599f6773d |
| `stage1_human_relative_camera_v10/render_fixed.py` | 92ebe47a7126dae78f56192d01caadee5bb6b186e08161e198ae9296c912a6cb |
| `stage2_human_relative_camera_v10/evaluate_human_teacher.py` / original fixed-CFG evaluator | 9dbc3870931d21cadf8293e206c56c33f2bad07b5ba75f16fad87eb477540685 |
| `stage2_human_relative_camera_v10/evaluate_human_teacher.py` / explicit audited CFG override | 1cd7cd6f966d66d5a0c99baf8a4ff11eff269fccb94af3050f7dcef1dd5b43fb |
| `stage2_protected_h_vimogen/human_teacher_diagnostic.py` / explicit audited CFG override | d7017a2d09f07f378fa16c72f5f9e4893329321c0476c420740c7fe13f9379cf |
| `stage2_human_relative_camera_v10/render_human_teacher.py` | df7709e1a249e7e7e31c5568e84f3edb79e8512b5b154a1c3cb04eadf8305fa2 |

### 4.4 Historical final `210K` endpoint audit与Gradio六路visual

endpoint audit是post-training、non-overwriting evaluator；没有构造optimizer，也没有改写训练run或旧selection artifacts。它现在只属于old-3-loss diagnostic。当前visual将同一fixed8的GT、Phase-A Human reconstruction、v10 CFG1/3 teacher与v9 CFG1/3 teacher分别渲染为standalone MP4；旧三路／四路bundle继续保留provenance。

| stage / run | immutable role | SHA256 |
| --- | --- | --- |
| v10 Stage1 final210K / canonical true4053 endpoint | evaluation contract / result / records / fixed samples / eval manifest | 148d74d675daf02f5e6feedc4f4806cfd25f077824114d354a5bd0bb3b45998d / dc3af92f961b5ad3bb0ee734f1a21b95b46201261633fe1cf5c73bec4b6908a8 / 1122fa0afdc23eeb7bf41539bcb2aedbbf3d10e83083fe4c4a3623199970c7bd / 8d5390ae6f53255b6440468a783164e497ed6ce9986a88ce1e8d131f25767908 / 959d097ea4188dc7db4ac692fb7d745416d35d8e0c0932b71c047033143273a9 |
| v10 GT / H recon / Human teacher fixed8 old three-column | visual manifest | 1ecb8c9dda4087e90be4272d203dcb7ffc625a4ae81b0d94d675fb29328d9436 |
| v10 GT / H recon / v10-v9 teacher fixed8 four-column | visual manifest | 2176701952e30ba64e448f1158324baa02dd873dc87f662076aad8a503f6a52e |
| v10 GT / H recon / v10-v9 CFG1/3 teacher fixed8 six-way | visual manifest | 2be929db619d9f945fb18af8992e2fbc381ad45d682f79bd58377f4d62790eeb |
| v10 old endpoint audit / old three-column renderer | `evaluate_endpoint.py` / `render_human_comparison.py` | ce1147c101093a62c66310d400da73fbf8a3c21976b47a5fa30e8ab12e8b3857 / 4779bf5050fe00ceae998fa2f7fabe8b520303b659a766b8ba37765ca84b2c16 |
| v10 four-column visual renderer | `render_human_comparison.py` | 12ad167d68c95fe95b2c6694098d4a64cbfcd414cc29a8f2f8a3f741487b61e5 |
| v10-v9 CFG1/3 six-way visual renderer | `render_human_comparison.py` | 8756baab608cc73e3474218a90284065a9fdb2193d3a4e9a0f067f48de8503fe |
| Gradio previous integration / browser smoke | `v736_p0_matched_gradio.py` / `v10_human_compare_gradio_smoke.py` | 9c78bde500a804422e99ec1365429e5fba5e1246845cf7cb3d5fce0e10bc2c92 / 23af321fd34c085dd08b13e3ed114c600a99ace40edd9071bfc5d12de70b98b7 |
| Gradio four-column integration / browser smoke | `v736_p0_matched_gradio.py` / `v10_human_compare_gradio_smoke.py` | 7355a109a56ee4caf80c1aca6d9b7c8abee32e107d2210cbda13a45fbac34f3d / 90e85d8b57724af07b9a5815e8c042c5a21ef676b79db06548c9c4acf2b64225 |
| Gradio six-way CFG1/3 integration / browser smoke | `v736_p0_matched_gradio.py` / `v10_human_compare_gradio_smoke.py` | a96380d4669a77f92438aaf4fca44f98eca76c4e473d6a0df16faac4ec769c1a / 2b532430d227020475b698c5a082197c9d24d59187e239e50ae2823b238f657c |

> [!warning] Eligibility boundary
> old-3-loss final `210K`只拥有historical diagnostic资格，不再是endpoint／cache候选；Human teacher结果明确为diagnostic-only、promotion_eligible=false。corrected-framing run尚无formal endpoint，也没有任何v10 Camera flow、Direct-C、sequential joint、synchronous joint或Unified-3 artifact可登记。

> [!bug] Stage1 selection policy correction
> 原 `selection_result.json` 的四份formal metric和Pareto集合有效，但legacy finalize把三个axis score取均值，与contract中的min-max文字不一致。后续又确认该selection framing axis把native raw joint-out occupancy误作lower-is-better error。原结果、policy-correction、selected-207K visual与final-210K canonical audit均保留provenance；loss-contract更正后，它们不再拥有当前endpoint或cache决策权。

## 5. v11 four-arm `105K` confirmation and visual

四臂formal数值与checkpoint／result／records／audit SHA由[[StoryMotion-valid-metric-ledger#3.10 v11 four-arm 105K first-512 audited confirmation]]拥有。本节只登记其余eval fixed source、visual与实现identity；四个visual均为相同first-8 ordered sample IDs的GT／Direct-C／formal sequential三联，`joint_parallel=false`。2026-08-04 C0-LAT被指定为后续唯一operational mainline；C0-GEO与C1两臂保留不可改写的审计／visual identity，但不作为默认后续训练parent。

| version / run | fixed samples SHA256 | visual manifest SHA256 |
| --- | --- | --- |
| v11 / `v11_c0_lat_fixedh_35to105k_seed17_5090g2_r2_20260730` | e671177cb81769a4f4c225cb0651bc695fd91f17939b8772b957812950ccecab | 55a6deebb4a4dcc6d275a54d9d97b9eca3ed491fbbbc63d5b6c13a327af2742d |
| v11 / `v11_c0_geo_fixedh_35to105k_seed17_5090g3_r2_20260730` | d2c765e819c21e3f9416add6d2b6f943835c34de25ffa4699a713bf055ffc954 | d32ea8e23389a275d17ba43d2a43d43bb93cc463ced29f9b0e07d8e656d09a1f |
| v11 / `v11_c1_lat_fixedh_gt64_tf64_35to105k_seed17_4090g0_r2_20260730` | 792def84bd6f3dc050ae6500c65dc854cf3bcb36dc5b8973d67b3c926151a29c | 0d56a222d05f8d2722090750e29d7b3c7e3ce1978b25ff4b87c1716c2b84b545 |
| v11 / `v11_c1_geo_fixedh_gt64_tf64_35to105k_seed17_4090g1_r2_20260730` | 7a24295534f22f1ba29be049d2a545a314fe3691443de8f2df557f00f0202520 | 0948a95713ec409c7c754abc840373d0a585be5481ec6ba9978b9386ee700b10 |

| implementation | SHA256 |
| --- | --- |
| `stage2_v11_fixed_h_camera/evaluate_confirmation.py` | ac2f4e89d701faede7172785a764bb853a5110d4d94850958375a09eb36e36cc |
| `stage2_v11_fixed_h_camera/audit_confirmation.py` | a1ea4e3086dafeec6366cd0cbd39e8cd31981cd15cb34d12d504c518f677ad07 |
| `stage2_v11_fixed_h_camera/render_confirmation.py` | b52cc9c051eba975fa8216ef3ae2ed17246389f410259eec064fe3d4a9619072 |

visual roots统一为`/data/public/ripemangobox/Motion/StoryMotion/runs/vis/stage2/<run_id>/confirmation_105000_fixed8/`；每个manifest均逐项绑定embedded fixed source、8个MP4、8个midpoint PNG与contact sheet SHA。C0 visual在4090的受控ffmpeg节点渲染后回写5090同名canonical root，源fixed-sample与目标embedded source SHA逐字节一致。

### 5.1 Camera `105K` + Pulp seven-system Gradio

新增页的前六格保持原`2 × 3` StoryMotion布局：C3-25、v9、C0-LAT、C0-GEO、C1-LAT、C1-GEO；第三行只在第一列放置PulpMotion official，播放器宽度与前六格相同，其余两列留空。每个播放器只属于一个系统或variant，内部均为上排world skeleton、下排owning-camera projection。StoryMotion六路的三列依次为GT／Direct-C／formal joint；C3-25与v9的formal joint为joint-parallel，v11四臂只展示sequential Human→Camera，`joint_parallel=false`。Pulp native checkpoint为pure step `92,950`，只拥有native joint generation，因此其三列明确为GT／no-aux joint／aux joint，不伪标Direct-C。七路共享ordered fixed-8 ID SHA-256 `6b9c92a533d2d0aff76cce6c7ad23361733fb38d3157128bf7eee56cdc33d8df`；该页是matched-ID视觉审查，不把不同representation／decoder／sampler／formal mode冒充单变量ablation。

同页metric table共`14`行，逐系统列出页面所展示的两种可用Camera模式。C3、v11与Pulp读取pure-test `N=4,053` formal artifact；v9仅有matched `N=512`，在表中逐行明示。Pulp没有Direct-C或当前StoryMotion decoded-geometry，因此相应字段为`N/A`。该表只索引[[StoryMotion-valid-metric-ledger]]及其源artifact已经拥有的数值，不创建第二套metric owner。

| artifact | SHA256 |
| --- | --- |
| C3-25 `105K` fixed-8 Camera／joint source render summary | 61b294ff36abe0c977a7a34898c900a392abdc637834948033664c475c874ba8 |
| C3-25 GT／Direct-C／joint-parallel composite visual manifest | dad1aca6c3a44e1e035f814d0cca82d012a654e79837890f7f67b5022cbef646 |
| Pulp official native Stage2 checkpoint `dit-xy-ddpm-p2ee3dj7` | 7c11cb59d5f51b9090abc1448e76329d157459fc30485031f5a79a7a119660d9 |
| Pulp official current-fixed-8 source render summary | 44dfa0a9a18fdc6eed492dc220cfae9606bc9f31832462699c3453ccb7e3bc57 |
| Pulp official 12 FPS composite visual manifest（superseded playback only） | d1ab43bd564f1a9c909b8826c5fee7ab7eeac11bf6e5bb1c823fc160d0745cfb |
| Pulp official GT／no-aux joint／aux joint 30 FPS active visual manifest | 03808277bf274789574a074878dc9e301dba8e5e464929986cc267e9d00b4fe3 |
| Camera `105K` + Pulp metric-table Gradio integration（Pulp same-width + co-mainline labels） | 000da4dd7f920b8540a8f116eadfede3b09270ac43f8a56f5cec94d5c705361f |
| Matched six-panel／FPS-normalization composer | 3dc1405e7761f52fc8ab0fd61c1a71ba67ac0b416bf5ab0518ddc89e2742859e |
| Browser smoke（duration + equal-width assertion） | 10c0391bad3ca1ca109cb5868d6e26f68905ddff8a1165666c49cce83a16a053 |

最初Pulp composite沿用旧native renderer的`12 FPS`，而StoryMotion六路均为`30 FPS`；相同`valid_frames`因此被错误播放得更长。active manifest保持每条容器帧数等于`valid_frames`，仅以time scale `12 / 30 = 0.4`归一到`30 FPS`，不改变模型样本或裁剪帧。Gradio全量validation读取`1510`个required files，missing为`0`；browser smoke通过用户路径`17868 → 4090:7865`确认新tab、8个sample options、14行metric、七个唯一video、样本切换、媒体HTTP响应与同步播放。选中76帧样本的七路container duration均为`2.533333 s`，page／console errors均为空。服务部署于4090的`127.0.0.1:17865`与`0.0.0.0:7865`。

### 5.2 C0-LAT no-source fixed-8 visual supplement

两套补片均取相同pure4,053 ordered fixed-8 IDs，以同一renderer生成GT／Direct-C／formal
sequential三列，`30 FPS`、`is_causal=false`、`joint_parallel=false`。每套均含8个可解码MP4、
8张midpoint PNG、contact sheet与逐文件SHA manifest；本节只登记visual identity，不新增metric或
system-selection结论。

| version / run | immutable role | SHA256 |
| --- | --- | --- |
| v11 / sm_c0_lat_nosource_c105k_seed17_4090g0_20260812 | embedded fixed source / visual manifest / contact sheet | 5ae6a2b5afa5f4464692a95cf82fc5e97e6839122ead3cd64102953265ad0f51 / ea8ce2fefb640ad05b126c91b97944a55e522446794625272358eccf09a6936a / 9f7e783b1454c6a60131f3dac9a84474f6ac7570ce42c0f242a0aab86374b1dc |
| v11 / v11_c0_lat_fixedh_35to105k_seed17_5090g2_r2_20260730 | embedded fixed source / visual manifest / contact sheet | d1bec3b1782e0d4d67c09eeb5608ddf61bfc8e5c083f62df94561a3b36c52aa2 / ed36775980ff125582d83afb55a0466b0bfe2711bd2922dd95331e8db71a8f9e / 7e6f91af5a9d52e0224b1d2688071c7de3759e20d0761922c6b31bd7552ce51a |

共同ordered IDs SHA为`a0d7627ee827e36a229d33f9975f8417ae78b504cd5a6db1edf62cb1a9266b93`；
owning decoder SHA为`51233f6a032c779e66b6eed4bb22b7f61c41d9b4a5a0a1ffc7dade7d3d86d4df`；
renderer SHA为`b52cc9c051eba975fa8216ef3ae2ed17246389f410259eec064fe3d4a9619072`。

## 6. Migration completeness index

本页上方按角色组织的表与下列去重索引合并覆盖本轮重构前 metric ledger 出现的全部完整 64 位 SHA256、HEAD 历史 organized registry，以及本次v9 redesign、v10前置实验和v11四臂新产物。它们共同构成防丢失校验；角色语义优先以上述按 run/stage 组织的表。若某个历史值只在索引出现，其详细角色仍由对应 immutable run root 或只读 archive 拥有，不能由本页猜测补写。

- 002db30b56fa302654af12b64ec17704c7921a1b1ae594e231358d04917a1d0a
- 00866077d7eef9e7d12812db34f256561d0c0f407cfca28cf321fc6ecb577ef0
- 00a7eb840b42dee68caf16b81c3af881c766a6f7f4a4e3a155dcaca8f225535f
- 00b6989a956347d279eeee02b5855bd60ff24f708ce0fcd0cfef329917797d9f
- 00c8ce7bc2307c66f69981f28b0e1bebd3e9ee9da3c0506d93a9f3b7f7bdc000
- 00d71010cf036b20f45d5e251434c4cce93e6ddaf5495657b3dcb62bcfb6545d
- 00da5137e8323d757d8c3bfad1acc6ad1ff399772107a83e479611e80265584f
- 01513ea8da4bc12e06f72d07db5bd0d44b33fd404c7efcefa2080e85a7486c00
- 017a6412ed30095130a09b7e35385bb4bc77129ab32cdd953355e133eb7814bd
- 0201dbc9a5199902091ea226b3979859332eede593f4e8b3a410c8516e3c0b74
- 0214c2d6a9201697542e79e6e762bb0acefd6780a730b8cce4c777a1656ba44a
- 023ccf8eec7b0d3c42b24ade3030c9e8943465062c760d7db2a8e4b376e24dbd
- 025d14515b04cced90949787ee5e783c65728076a28f3885e9ed5a04d0c6e77a
- 0260192649bd0eaaa179fb5d39fa8d62a42f4db7744e2d28bd9974aed7b6b766
- 037871329eaf980e320961445f5492c7a79ad85d60e9e2b79640678dfabeff3c
- 03c8b636920ad748330b57d5ebb84657a40832a01a10dbde3739b28e2942414f
- 044d2bae9647417c6e651ac9cd9d8f83b54bb18f37e6d56d8507dee7388839b1
- 04add8e553af334e4724f08c7076a0be24f171470b938920120ef64fc7b01576
- 056f7513bab5e99036649cfd3298c405e6640b68d49fe888e1373e5ef75ec288
- 05b11d23edf2f73665c94e604c868ce8c54406622f125f31cc80b2a453f469c1
- 064e2eb0b6823e39836647178df534b564cb3d984f04b6075baf1f3820c28c5e
- 07652423f954549219bce797920e50636f4943215b4d856fd6e7864da9a04cb9
- 0776a69c18df6362450c152b632c66b6a20970697da9d04875af3cbc09bed6bc
- 07f907cc12cfdb6ace6a397ad93d56a324d95a337e71e7b662ac9895a1ba6ff7
- 080c04fa0bde88f6f56842b376f6a1ed61a6f383c992ce5acfb4a03bd9b9b819
- 0871bbf932fa6bbaf407a4e597182abe5664f64f06fc269cdbf7d18f5e977694
- 08881b7e6bf5423c8bc170b41216fc2d00d46229f66057ef26db43c635719d0a
- 0945e527e81789b243a79dcdc0f380defad57e9bbcd7125633f91259bc50dac4
- 0a0a47aa5621910c7f411e74880daffca3c792275457f48c27d0bc46c3b98f39
- 0a3ee046c5c76c3991064b913019cfbd38b9eba24214d144a0dc792a3bd204f3
- 0abdd8333bc44569c1e4e4a5fb55d9fca74263a5e4208811965167f10e581276
- 0af52d7e108bbe74256233bcf083eab483e661683c1bcb7300ee1973916d32d1
- 0b05cff3c20372ee5c0701df5f4451a06fb62b2f805c47cff15d9acddc46e444
- 0b752c42d45889a61ecbe1ec27437487929ec993d171518240a8d844d1e72c63
- 0ce39698e21b558faf47bc0da3f89d7cac42d15b78da8011fcf17d5bf35123ca
- 0d7d549e64ff863da2f4815245c18ecb03d997ecc1cef3f423ae817c90f28c2e
- 0d7dfbcb9a32cbc6e03f0df0ac3a5911d1cbe6ce83e4b551f8808bb0c2f5e33f
- 0e11862869ef4c16ab94cb8c30b414ce05d5b7e7074dc0fbdf85a6d9483797ab
- 0e13ae9a9850574f6066cb2938cb6fa6b0ac9bbbfffa0b6c571e6897abdfb704
- 0e6cf69d6be78e47c86abd229b9bc8a7ac5272c48b5a4dddf3733923066623b1
- 0e845d2925fd2331e12ef43e3f5392b9a0ab7a45b36ad4d74c505bc9c8fb29c1
- 0e862248d006d80f63f3e220e3e5d0f370dbe0d7bed1fb9bd91de54bcbb267d2
- 0f2365be063b4512dae64faf867889568f9b2e4a776aa51aa572e87fe4c82eaf
- 0f3569026b0aeed6f1d54336853da62a0f735801ade3e086042b33b7471eebeb
- 0f4cddf17fd15a4b73afeff17c2b489702f237928b099d9d699340eba2f31d96
- 0f5a917290dabd54dab99ab3d7b853c02987e7aaf2ccc10f688148c3235e44e0
- 0f6d7ffb730dee181b22ef03ef895f81d4e50e10bc4a474400895a5be19a9dee
- 117d51a1d2ed1ae57541723b85c732118172634c57b2665f00b246c36e218558
- 11bc6f6728859f19cfb6184d14547f1060e32e65196b8eb328123c03d952c173
- 1242ffca84d5542a582441c8c8b4181feefe0d36f679de84ac0031d5d34cc17b
- 134195504286677d0a77c0da6ee7e8a897008525337a908b91506a301dedc795
- 138b364513fe76b1d47a3a2b5ae0d67f9bc11735417d8ce675e9dce921f17451
- 13f9715b446a33d32181a231b2a4eb7bd17eddcb2044b8c2228cda8cd4e20727
- 142614050c5d94ae8e0e680327129a7893d64afcd0cc3ff0070aaf3b1a02274f
- 142df6bf6fd5cbfb90263167e1741ae880afbd55254a0507f9fe4ab956034f4e
- 15bf39fd02f07482767649448ab894ae2f45e95e8fcabf5beaebdc03421fd051
- 189996bfcf5d3fa85a4d13b4c2586546baa2a0b9005939b86075565dae091c42
- 18b00e90fb59f3d26c9b41ff877957af36408f7b33f1f819bd8d582fa1a50476
- 18b3cb388f93bb447062a468ac5894ff2e0bd6c9ecf91b14f00e74d0fc1e17ef
- 19354e7949d004af4057269f432b47b6f33392a8ceb1da376b1e2a05c64ba9c0
- 1977aef6a6557c9321b1ef117aadbeb0fe20a00cb99a42564644bf461aaa7a84
- 19b4898674c02267b2678f5eea4d7d6f7c61067c454a798f16a99ca54c647c99
- 1a3dbd02f38ca8e68d37261f138e59936e0e0e885d006ceafb1b4015a4b5958b
- 1c6bda40946f92585a032653fb3f694630ddccd607ae9aaa6b7849ba676f8c7d
- 1ce48a1673b9a22ff8a55790db163a7de27f685acb596eb4cf4a6f7b622fb719
- 1d0d859ffdad1e69955c950e2a3562b9c2b41963d73881c550a3cf631a0f0e4e
- 1db8f3ad226df27def2015f4ef047de64bcdd0fe231e62a9e3aace957556d2a7
- 1ee7fc533c1f8a6468967218a61137ee5997377ab98719510e8f21a9b21afd86
- 1f83de6b3abebd7d0e9f5b2fe2bf46d23189156557d4a29e016ce717cad8a0d2
- 2084e5808843a3c74bd999967f689c776d49463318d88c2d5ed6cb80a5c8fc50
- 22b34b5b76f7215f089a6b1dc6034774870b80dfb9ec6b6866b0ef36a0d9d8b1
- 2326767456188e2c756718fb023e1f3a2b780fecad4cd49e546f48dcda915865
- 25d50be2354ea8c73986f51c55da1e6c1544aba31a117b16eaa29168ef197846
- 25dbcfe0e490b925555ac2665196d9648cfb39b9c42a7634f47f253b0e016bdf
- 25ef53b93e8473b26ed4543ea75895cc3cc49f49d7d8fdc3da6cc6b962dccc92
- 25f2b40c55bfa2cc4233678774a82a1e753bf6165cb3c66f02cbd1095faf39f0
- 2644a137df83ff121e53f275db57740ac0468ca7f682997cea53544ffb5c581e
- 266ea63f00b545a6194b656a59f0a94bfcf7ef5199022e7cd09f76defdcd3208
- 27d9c3a619b92fc835fec24169a2424c05eed34994ca8d8f9cc600569c851bc8
- 27eedeeca48a207fca03359c969505b82b777584154ad5646a79dfc0f56a1e36
- 292da2869e0bce6cd3135c1d194182800ddd58e49054396dc5aa37fb61b59324
- 2b1cbf3a25f92bb70972b880b764d41ae12711aaeef3d0c0314b9792784979d4
- 2b6d42544e75ad330e01091e4a3a294a67e02f2fe0db17ba14fc12e5afdca765
- 2ba85cbfc292b9393279825eb49434af03a4fe710e08acebe3344feb56dcbf91
- 2c1eadf434465bca3c705b351beb706128178bbd10e507b88841b3bbad4d60b1
- 2c8294f034d1911900f308a11e183122900878b979964fa438b0ce5c163f1fa9
- 2dda4bf879bba6a32681d749a1e47193f1fc75a5ffd8bfa7e0ab3e75d5bfec92
- 2e0cceba7beec0c3e565dde98a2925a4ac9c692fe152339a757fa140574a2099
- 2f5a64315d8cca23d3d432bb872bec55ba72fdb775ace37b26019c78c05002b1
- 2f9946a411fe33091e52962bea689aa0bbc35601edd8e879b35c20581d92fe5f
- 2fcf8daa6514a0808e9a811830b2ebfd416d8455dce8600b76cc58a113eae8f1
- 2fd54592d9d63fd55f894a47756ef39236f7fe7e2b0eeb1321bbfdad0cf0c14e
- 32a5c5fa5d1d0eccdcb5ccc7e87448491afd9f904721ff26c1b44244114a2d23
- 32ce7f8d1a91c75afe821659a2235d3ed05f8878380b79a7c7dd44a4e20bb4c1
- 33d171c03417a490942063405e4c90aed5a4e2a4cf2c626ec8636418b45ee5cd
- 34544e1588a5af63614a1b04c50e2481c6f73ed97e21cfc3ab93ba657a2d163a
- 3533a4216b441b8fba0d6a791408d60a8708dc9a44e47b93d3187217ee83e226
- 355c5a204208bdb4e0cde8b86370983e2049f2a2be59fc92fb59b77856f32a8c
- 36226884d17a318100bbe6bf466b7bcb8b8fbae913ff6ed6be8d0e531f85ef09
- 36350e2b440f052ce890ee8824183bc686ec6cb0fc4e36ee7ecee573eacf11f3
- 36d866fe2f3882e8a01a320ef9b8311702b944413d327a125fc2152ebd5db0eb
- 370e30d190deb63e66e675defc26265c103fe1c62a860a982e577597ad8e5c07
- 37d61e28076735979731e47712500cee016365a4e9e2eb7753d93a10416dee51
- 387ba81dd5999fb67b7fae9b00388e6b79b583ff5bcfe278bcafa89ad8250a4a
- 39485590b363a5ad5fa0bb69d99699bb588bf83c6799ba4c1e63965812b4f5d6
- 39cfb7e970a70d067eb855d6328d1e5d52c09d35ac84650f12cc44edbdb7c15f
- 39f649a2d074f1bffab607d70fbaf54d087263164498e898cadcfb7f7b7404fe
- 3a133b834bfac8203a9bfb92cea55e0127f50369bc51c68a53bb3b0d877baf70
- 3a3635be17fa1c6cc155fa8e5ad7339d46e446c55195ec9ca1b350390addcaa1
- 3a39cbadde535073a3889042c370826ea51dffd62b57700eb97d39dbdde57e87
- 3b5b4363e49938b188f9059c6c6f76775c6dba2cf4ff73c62b98cef022913420
- 3b9158edffd44e72937942eef1c820ffe1822409e1c8c89926ecb24286622615
- 3ba1e81aa0b80a604584c888a4367898c375d9f189df6ae2f5cb8ed22c757a8a
- 3bed536d9a475085b440c5fd644c652aca7f2107326df26444fb62b5a29be2ac
- 3ccf6e2347f884e35ffd55077bd2647c0c1a88b7748bbf962dd71293727a4783
- 3efd59481f8052b401889fce6559e31f96cb88f51dfb6c466464cf05ec6c2c50
- 3fddbb68282a97c01dbe08f6ee2d3c27f12298ff47292ca045e98024b592c01e
- 42f0c971b6ae232eaa74140e0ffd5953e3dac0e0d2f06092c5d455818e080002
- 4313a7dd328bf93b59445faf752d90a82283cef87ecb7abc68ce6c1f46bd1391
- 43898e866c5c63745c399325d3298f035a3face13a51506f1b324776a9a67485
- 43f79dcfab79434726d9b68bb69ccc0ee4ef2f31c84f1c0076315ba8bfece167
- 4400a5c3f170fa8ae28098059e77833ab3f64feef3de5cb9757be5e094a23354
- 445695958ba86c11831cbc8f931939c71f72135453b21ca6b6d5e2f170b6f685
- 45477134830f25c58b6db2ea54cfdce4cadd8f0e84c0e9312f1ead73bce468dd
- 4558dad025adc01c8ac4a55211e23a1ce5c2d18737a34f4d457d510bf36f4901
- 45f7f0594b0105ca6811f08a0e99b87ed6071950cdf39f1e7e5db5055a0e76f8
- 4669a56fb6c9a4adafc2cfedef39b27c060cd00949a7407c86c68cc9fa30200d
- 46da26c3d1419240536ad3fd7921066e8930b07a486e8ed927db03232d96ebcd
- 48850abae1b4d9d364c612105b748e5db6fbe8634f04969f6ccb495cb9bf00d6
- 48da45ad23c51131d9d51faf9e0b346a0b6c145843cee55bb7a6a17e54ef0c2d
- 499db08e4f957f178cebc9b8c5f07dbe53ed680bf1bce657c2b5438e1ebdbbf9
- 49b4e71ea0225ad299dbfd2b9c8590c372deaab1b8ae03044a0c5d7138f825fa
- 49d0842b03e1483f9d549c1133d8848f5f6b381d57e61fcc01e4aa9664db067d
- 4a4136b85c106218f285fcccff0892a4dcd57efef65e1054c3996852876f0720
- 4aa209b5015231fc3a86b4edc76137ccaad2078abda2ef146ec28d4cba1dd48e
- 4b3370da1a923145a43ae0929b745b6c6115435aa83be45a1bf5ec95076a66aa
- 4bdb881a6cf486d76d3a3c7cd72939217f52e1e03047fe64e34359a1868dd7dd
- 4c1c54159ca3b0027da82234540c411101bceee3e01ecd0740e52b9b239c225e
- 4c2cc227a712e0df5faec0d809d15a5be708eaf9a2ffbed693f6866b6fd89760
- 4c9b51778104aef3e85f2664086a22802988a9a23833181026c6facdab608d98
- 4db5f2dbf50b38b00a100b32e3a28ccc92f212c212e169dcbbd438c83a1765cc
- 4eda0ab973a7238394e72aceda6f07cd0ee83c7587fbc8a7feb6256ef5322cd3
- 4f20358b7401edf86aff84054a90111d1fe0d87b04c40934f49ec8496fd29e7f
- 51233f6a032c779e66b6eed4bb22b7f61c41d9b4a5a0a1ffc7dade7d3d86d4df
- 516a9fdf175f03c0a5bba638e2c0f48767f3daaf61ba29098aaae5320eee7922
- 523f187c3baa687b93c5292e86bb043ce2194225f5a4a3595853aac351e3051b
- 5424aa275ac454ad24725a6579b7b559e329ee312ba49d0f60211f840ef58c46
- 54cdb96c3a89422cc250bfc05974f0d7823e572c437842831802a1ebc6d7c32b
- 55019105e181ad2afbd49cdc27cebd3c631b78af8df9783d5ac9969e3fbaab48
- 5593209de89f3f0cbde72be4e8bf869f3aa71e37458b070018096503c9680e32
- 561b1c4f43f59a06012b1585c49a58729d02d0a3382db5fc86e6d434137cf0c7
- 561fe3735cd2d9bdc32fb7e867a9229467df290cca036177ed5ac6c17f51e288
- 56f955491cf92fd0e2e86942c24420747fb06db35bf1cc1cfe93d1de885e0fd6
- 582145d253e77ef1a67009a5b4bd08c6682e37a3a260b0f3efc23dd4c4ff42c1
- 58b6f62c6004e2ef24f94bd831790058e0e799e29650f1622a0a44e9eee19d7f
- 58cc7015d316e43b6b290799dd6a86711e99c3bd5abd5a7f4d70bc996f34deef
- 596a4a2819d93f03a03e014a6ff928be4aaae7dded9ea89bcdd7f7974516bd75
- 59f20c3fd76a17cf5bec37e951309ce0f777fb6d9ddb839e11f752e1f4d45133
- 59fd2e28a8ef2a5233b7059509dca9ad3e6513d65c35b05e890fc7aedebc0f40
- 5be1e1e30213e6415c0a057eca2a444af31c30614fea1517cbd2f2f3b637961d
- 5bf76c2c4d7591f56abb70f7fd25b69f37d31bd1e837962206dcef5fc02b6c74
- 5c2a59f3e8f5863e09f3c076bdc0f80ad6296f6c62a2ceeee113c77f09c6db8c
- 5c81808ddbc4fe12a0b08ba1869e2dc602b87bba0d59bd0fc6986a83fbfec579
- 5da21f1f7bd4d12e5cccfb464c63b12718388b6a8140d6a68d7e508079e5e5ac
- 5ded52a0d6d7e51a756e16b600da0c38bb0c3b85b14a9c79d42fe0818b741b08
- 5e88814e60b09bf4b29d7dbcd06fc3bd4bf8a91ecd1bcf61bd038f3157e58bce
- 5ed0778004fa4972a23ad26cf395f31b3dc06272531a30dad19b58a8c60a3895
- 5fbeac52b9594bbbe488d87cbd6859e73c1e80645a2bc3e61f31f3f9a09aa1c9
- 5febbf1470b9a7c0411afa7017dcce0616b083bae9db01fe9895b7026ef964a7
- 6018e593253969abbd5a07e1861a401b10330460702d4186484bf40f5fee7cc0
- 6030fec7834e719f4b436bb2bbafe75c5a0b7465379c5a149893843b5e78cb42
- 606667828dd43c012776168a881f502ccf4df8c4fd4fae103a13e9d939049595
- 6182d01d6f3ff4179b8c4f7b8d543d78f3fa4cce60b3db296f10e461e2daf597
- 61b294ff36abe0c977a7a34898c900a392abdc637834948033664c475c874ba8
- 6310a1b32396247e79175aac67ea0155438f0ba88010c005545029e35eb3fc16
- 63695bc184accd77258f8751829133b5fa5c22953040bc8738f4d48f3713b2f3
- 63f908546921d8888b706eda57ced6fe64cf7d20d011828af8d82ed78777896d
- 64822aa8064eebba16f5c05986781f191ce8945e30fe0a96aaade4e585520646
- 6545ab1a4e17bc13b73663aafd983b439ccae664b016251640dcc22a0e067ed8
- 65bd2dc96028f06057e44020172a2a41a48901e5f0bc0ea981e81f4a7343aa4e
- 66cfdb383804620bdaeed07a513256122e8317ef6a9fd9f980c8686ca264e9ee
- 66f64cc8add76ea941a972d8a197cab380a85dadd1913fcedb0e0da312458b3a
- 6719c9d90c41a967d0c0988b3c58dba183d91c9588d5dbea023fd3dba9272875
- 68120768402b0560332cfa320c8d5f3f11067c125eb2d0ac9b8c04ddddab0611
- 689201d2bc0ba215648a7272c932806f78fe7d4f450f2bd85534b27e8479ca27
- 68bbcca0747f83cdd52900b7f2ba7d6efb5226dae864ac67e211827df3693cca
- 6a566d6529e90d5048ea1fd8c171e18f1a8c7eb0c7eb15a8aa3a07a179847ff6
- 6b9c92a533d2d0aff76cce6c7ad23361733fb38d3157128bf7eee56cdc33d8df
- 6bb2965b54975ad0987efb3bd2e609f28691f112419c62df2d9e0da85828a32f
- 6bed0bc8957c691f7f448165d30fe5703ebf35ee7bb515eec90b7e818a43ce88
- 6c32d3002ecd111f177dcb6f93b0fcc063bfe79578204087b590d60bff0d5bf7
- 6decee38543a73eb9b53dfcd37d4dfcac7075d57c4a62be6f347dd9756471dc0
- 6e26707058cd3d90907375f42bcd1446bee0dceabcf84b6f1e9b84def32c5199
- 6e9ecf26e7ff284089fce7538b72eee875ceff8e466c7f2e04c06f772d85c2ab
- 6edb7d5f9e54a61540b175028cad6911d5b573d4290e7dc95edc7e6fce122a9c
- 6f82b94c0a2f3acbc8e4a09ea2caff454efe44f30596c7e8a32bb5f391fce8a3
- 700a1a113cc7d2ea1b2566ca4b896edb92521f22ac253de46df8714e05440300
- 704180110482a4db774e2d5deeb015873024f7ca54951af9c5e4f1c9f081216e
- 708c5b2594bbb06deb535110d4a134215d3c6d21f52d5ee0c6f0f0fb77f361cf
- 70dd4df1d635b7db20c0c5735b8aa182f04d73604851e162ae27a70cb1f268b3
- 712020076d9eecfcb76d5ebc853b0d86f824d87c5349302864c4563f247d7a99
- 717e322fb77313a8c3c3899464d8c9c78a7cdc6dff0b53be2154e416ea9a671f
- 71a9a2a3b700d4f0a699fda5f28bf8da72f563c20871e1c1cfb5d4d4cae0ac08
- 71bd4b1d31409a8e70e991715ee7a09ee1706384df39831ea575e9f4a2ff3232
- 71d82756d5cb30da6c5ed895c8ba6fbead2fc81f936e3ebbf0f0f6858aa4479d
- 72170f39349f32649014725b0332fa8a2f88042eb7ffd8f5af7a3cea2a4c43fe
- 7221ab294ab41e9029052612fbe6fa913104723186c0340d4b96d5f1db3de97c
- 72c604d24d60274b27b749d3bf6ecd4bfa5c0b1c03ccf70c8ff011106d9bb744
- 736b546ad2cbd99587fb62fc1f378a48132c499cbbac6bb8fcc867356fe6ac39
- 7472486f9b839ff07d378a2ea76c398f446da15bd8cbece12ee5adca56b6cd8c
- 74ba112886bc84bc6edeca9804b9e597b94bf0601c897041e778ff849fca32ec
- 75124010e6c65c216cd1b6fa82ad6ac05d417bd5211d86168dade0cf5973e7e0
- 756d41d1790c3fef34c5366366a7d6289dee49cf63208e6b2c6880db4910758a
- 75d2daf8cd39d91affae8181cfb1365efb3a52bfbc85f50a1cdc6b7d90cf9b15
- 78d01ded78e2f608dc966dc0dc83f9d7344471a831c4105e7dde9aa297bfad9e
- 79589f51b81b70a9ce5a3f8f80ec2608f41aa2c206b83d749690017a6aae261d
- 797d611815abb020780c28d00c53a183597a6d336c0adcec89df22951c9b2cf5
- 79e0d2b3689915075e0ba01c412208135452087e11ebef0bd2c0e856514725ad
- 7ae3de5da6ad538b6362f45dd9f5556c105f878319745b7bfb6c0330de2d2531
- 7b8c3524f59672f25cc3541b23b7658863965a1229e3881841976e44a26e4715
- 7bd4389bdb5f5b3dddb5b95366aa794f7c80f6c95046b5d98a9cf81b41286617
- 7c11cb59d5f51b9090abc1448e76329d157459fc30485031f5a79a7a119660d9
- 7dcf3b1911af144ea9ef2b30017dd07472d62f655fd04c1dc9263581e3382c0b
- 7decc3dd213d5af79176eeb3d95d1ba2561994bce0cf04fffa7cbd40b38742af
- 7e356764c9bab74a7ae6afc51f65dc91e868536861dcd67a8c7a9c4fd4a18026
- 7eee57505c973e332697ba6ddfeeea388343fcc580061cb83b84cf1f4e530fed
- 7f38f04e6f8a7eff5a44ae16a67dbd8d51476f6874bbb4f7f9bb15bdc2bba15a
- 7fabd979fb4ecba3774b212f18d68e580b420613296a92e5cfc6674000df3619
- 7fb0af21592a422df28e15b07b09eaa0189dad984e8631b73a8f3722e8ace13d
- 8014b120c218a7ce8bd7d6f6c3e381cc009939950926da847c4dc2597f6603da
- 80652903af9b7b7e90912a619856b951ad2e106eeb2a7b4051af30122c2c2a4c
- 808d4799a2c064f0e10888abb87564f63b008023d793fddc3f6aa87bcf9f1355
- 80fbf5743aab7517acbfe9bcff6cde4311ce9257cd477e7af5baa658c2de6e73
- 8172bfbcd76714344159f512d99a5e5f9bdea8a0c861160d218c954d67d3305b
- 819048a0ed51d493912cab8198ca3d7ebe5b4e63dff8f7d67109303d9c74522e
- 81945ad3cbe533ac7fdf6893b1b3c33352466f15f744f5df1a36998d659cd725
- 81a32456f4c7911f3309224c62b83589830d86da9447c090ee8251bf63075995
- 81b07878fc4dd9801f3621a984b155d584b09a69a0599e27674f23586b20ac7f
- 81ccc70234210168c3b7a12d5a5825475467cc8667f3fdd57ccdf5c22fc95485
- 830ad4ce50589c49f4454b0084f8e84e4baa52e8029770ec1c031b9398fb1f0c
- 8326f4fa91b925d446a731668d30ee3c1f4c28f54043959a15ff032fdf93ddae
- 84949319ca605c6847ebbbcd71e9e38dc3e2bc8c46dc521e6d11037d9cc679b5
- 86894b7871c23235b45674fb5ddc368f228c59740393bfa8f2bace4c5a39ba2d
- 86e3f11ed382aa4d0934a8ae99057ad7a23fdf26ece45d1007f1c6a8e2a404d1
- 87314a4e362b9c259b49113842aa6cd162b86499595209ead4f4aa6ece105aec
- 88188b5459ed4835dea1d3c38039b6b3e5ca336aff9cbac218ec381855c8eaf6
- 892d61b9d426d170379c618b27f1f73a97007f214f3ec3375c7f3daa4de8da91
- 895a9fc6e69ac5547082435c8c084375bf42d044b1b45ed1f06c7fb479d66361
- 89ae1e1fde0f508a3c69d265a49f8e98674167be899082cadf69d0a9fdbc3728
- 89c7223e31020d6ef0daaf777387b80b4a628d3eb8b62452e3290e304d3aaf01
- 89faab30ffb62d185a789a814ae7c061ed5f5375f9ce5128dc4764756c43e0b1
- 8a83ecf9f1f3567adafcc7b485c42316d139bec0f65221c3836879cc827de24d
- 8abd4512ec02ede51aed4eb39127614f63d3389722f1057658edec8a9a331fd3
- 8b0ab3ba82f85192adeb066d99ce6a07f0fe645b2e916300c96e16b4aad43f4d
- 8b4f38e990084dfed58c1c2d2b487463a4bef8a3c83436f89324bb518a8ab0ee
- 8d8f6d2bed58eaeaeeef0106a1cb694aa08890d8c9a71d323dac5bd83a12ee09
- 8d98765900ee9f9683e84b3e2de309b66ae92733de41ce49490d9b149f5baed9
- 8e5a44cb586eeba1cbaeca82ee2b731badfa4dab4f15c40f11ccb7140f3a1b34
- 8f178f124b120b4fa6f62d736ec01d2046ccd3711ec1850e79d9e97cf82829b5
- 9042aa679a97c41b75fd9b2eb8b7854f141bc55c5df8a5bc4d0a153f3d6ab720
- 904ae14866b0a62fed37cc0b09de5f6bf9d177f81cfcfea760fb96247bdcdac8
- 91248bf440a4a5493a0f8b4994d6d36479fcaa221d331f6995a91ed1af8e7ce1
- 91a81209ad5165c01f35d6c3ce6cdca703f0d3cb2c812a5d39319376032cbb3b
- 92e28c02cbf1e35fa632e726fad41d2b4628149db666ea66c785dbd2ba5b099c
- 94a217f900e26212e523dd1f0444fbbba5e6392a7c424e0441bab19c02238901
- 94b7f2508dcaeb240559e418503d5b18e2c715b94c3fad4c5d997fd444f2bd72
- 9559fe496639cf6663bee6283a4ffc17de0782e3c88dea99a74c3ad3c5ea11f1
- 963327e766cf5acb168dc668616f7098df94c4df50b2a160299bcfcd2d2fe066
- 96552a68699bb6c9dd694a19e8a4147d6ddf2f2c997c53aed93532e461f6cc28
- 97313a98ca7ee486bfacd6a6e3be29fe352509361e28f8f018f168ca8f674d32
- 98121fae2392aa0909b5847ac46c917d4f91751bc325cc42c3ffcfe51f593d50
- 981aa4732617f140df8f4a24a596ca3cb892026c5ea7b4f126154d757ca13287
- 986982f835bca22c46c286cefdd4ac325ace1758ef10982497d317435079358a
- 9879f71cebed55a94bf725b63bd1558dee2f3a04cb054fc9ffdb5aecb0b8f5b1
- 98a5aa0c00c14b30bb23c6a4ac1fe80a4397216f408f3ef3d48196c92edca8c3
- 9945895b7b22ae33554cc1ec7d35b1a8b48ce0de8b0231db6f6f0c25c990e81f
- 9994c8d97c625b9b2cee6167a6f8f74418e5816bbc812b245680dcff7d5583c1
- 9a8a7dbc6dce3a6d8d26c5414fc1a7240cdafd349092737c484dd9393673471a
- 9ceaadd284345a569a0c2e71c0c7d2bbbc2cd750cf8b2f046d9df172e795479c
- 9d5fccde0e22020c8b5f2b337b6e26df36d6f2806b3e9c62fc9ef109331d086d
- 9d8749c180131ddc69c2f48de6d5768ce6a944c75644b7ae33f6093fa76ddf95
- 9dae46d216b91d4744b722591748b05917d9bba06432a3751f20669cda2abd73
- a0981b6c6223409d656ad8c43cfcf95cae6ec9a28640143b87b6322292c51dc9
- a0d7627ee827e36a229d33f9975f8417ae78b504cd5a6db1edf62cb1a9266b93
- a16d95a10e04173f7fd1d86ed324ee4a796bdd5c6ebdc6d9944260c46c020fb5
- a197b4c174499d9c0cc0160544b4ab2c627a122645ec7174b46ff145be504358
- a21d46925b2649139204f1a4b7a7ab880221d15bebd3b248c932de9e1b122588
- a259cc1a043bf9ba4a9e6866156f91cc71805d6daba4bc0db2de55c8a69fb6af
- a2f4d063bad486075084d9a66d06084a430f012d28356f42a4b161f8eaef8002
- a36dfd3664b23404959a4b246eb9d3108367f5e8500f9a4440835fe5bd12cd47
- a45edafec83ef539d28f54cd6bf863970a45559251e7f688fb43c6c9bc091922
- a52aba4d6260aeefac4e5891fbe510322bf6eaf12ce98e3d0bda16ffbc8ddf5e
- a55df270cbf7766a44078d11f906e9729d771c6a949b9e23d67e6c9406887664
- a6206cf7184ec768ab3eccb0251ad69772e54c4a324094e4128dcfede7ac403d
- a7c8f48fc2706a2d71d961d13bc09b5c89abe743d6aa2bd4854fc5cb89e5940a
- a907b2fb6976be10e42b5bb1037c299c6f44d8e875da9eb23d46aaf68c2f2782
- ab474d353a29a4ee707c8ed4e37599fcc47ea79c124452ebdd366d5bdafdaf35
- abac845f8eac2b3c6da9beeabc02d26058e17b2007fa93d60dda54e7c3ee5248
- ac47c2191c44d6368a5468510975cefcf0efd1338b03ace50266830c344151f1
- ac79b06e4536e61230cd629ef3f59ef1c783d9fef476cc60f08c9f54dbaf1696
- ad24c5a2959808800610c05c12f9287520fd25b50a0eca3ea841cbb31c67b28f
- ad27564052465ff11f5264c5606473f2daacaaf74abbf45adc7b563328b5e823
- ad455ffe35f16ff382c146a3da205d83a15066fece0c97beb958e8fbf36d62a8
- ad6e32dbf4865db68b205c0aadcf3e640641d063e37d2b8a77a93405d825a05b
- ad7f275348397b80dd44bb327681ca55329a01c2f529820eb4e4ef7761a6a50c
- ae1993b459858ff4cd580a00fc16256dd35644b0d12e15f53c5b46fa35285218
- af121aa334bc9039179fa3b5bb37fd5cb01bc2db01770dc55790d0bd2827c07d
- af2a97f12ee1f7227719af2162efe79fac354baf4c2f5df229ac4a0c2f0e8546
- af3dd12413995f70356d7fbfc7a50bd7ca3e0715909ebbf34397c8b539ceeac4
- af8154b48fb5d2dd9237d16f62b01ebbd0ab0450ea99031190589083a420e47a
- b0d8f936aca06d89caf980f0ae482ef177ea571086f9d6791d89ef935cbbf2eb
- b2205b551d7338808b4d3608288e9a891d5b82af24d53be601098d3f740b8cbe
- b33089bf7dfb5f4625145d2e3049b3baf508d987110945d57c0cba59ee7a2189
- b3372376ec180a4105a3b2f88f8c95e7ee143207439fa949d5c0d1d74e756e69
- b36b1ad7c6a93b2bcf523c58dda946d8bb86566a9f758a609b2015bc4d1faed2
- b5aaef9e37a0a4a6e3fe98084de65495e9f5697bc72163c94ca81bf784fa9921
- b63554a45c05b2f52fef5215dc4de36bbfa7ac8e8490a29ba6730fe98f3f615f
- b7fefa26ade60e5fa0304974dd2a3c6cf54b6e0410ea8b847cc007083a13955d
- b8291f8675c13972cfd859cd7f5eb5b186bb9acbb20ff8a739d4b483a7567a54
- b82e1f6abc805237d7d702fb18ccb42f65142470eb7bce989ea973a0768689b2
- b8c06913a5efdbaa0c178e452998352033174614aa0a60ad96920fe14a8acbb2
- b8dbb899ab44511785d00150a512973181d613b19bb7f4546e4900c6f61c0785
- b9dadbc14221f259867138b4325d459587e01baee6a5de6d3e06453564f748f1
- bb1818fb9703035d34bc691bdbffe82a3c9447c9c68a3b6010cd3387e5b93039
- bc38dbf6f8cba040c608b2ccd726221426243a43960cf1b06ebf494a4afaa8d7
- bc8c847e414635aec022e0892201cba0e3f56fb54fa9056accc458be9bb03fa9
- bcd0d77e7333579b3df8f4b6f34757f2a5592571044bdba1700087c7aacae3d7
- bd33049469c6b50789cfc78497fc035eac11dea3ea9e1c452537bfe12e3d3a1b
- be43f0a9643fe044ca268b061afefe8a99c1bc81a4eceb7f17bf39c0229961a8
- becc2c11051bfd7857acb0602f61c755cd664969f34acef1f0232711feee5bb8
- c029cd016e3dba6d84f0bca5081417e44a61ca3c94cc9f351c1958afc9513dff
- c0393a076fe20e3e667443e17f1dfb3ddf7bd97ca78f807ab95c3a0471b9fbee
- c0bb55bb244011ebffad5911d9ba43a7b4ba1b28bcc031a6df58e0f2158f89fc
- c1a9ad4c9e67f340d108f260bad97a90d5281932cfed11255cc2a52ae2869ac8
- c1eda30d2ad97e3c7ac3484a2089ed61e438f6386d1d4d1e2c16854d4e13de97
- c26f06d7b9b2881f06520202b7ce7953b01d3e59b472f80fdc6cfc37fcb10774
- c2ef272e053d539b9e20c7500e7aad2c053574a06184cfd95174038db0d3f0a7
- c41e320b692389576f0eb7ec695a22884b7a0c9623ed0d9b35a4605098019aba
- c4a2ff328d0028807766bdfa160d3d173a6de9ae2a94a83bc226190be142df2f
- c503914f28eb7b84d3a782816e9d3a24be76ec8948744f1bf95ff3a7f99d0e4e
- c55257f52320822aab757ba22033919cc52b54e48cf2003dfab0dd81cd84ce47
- c5755cf277da27fb62bba9518239af2a55eb9156acd994b196d1e665860832d5
- c575ca29f696fb00aebd55aed4e46466ad18d46f956d41f78272590078e9e9d7
- c5e2064860d31cb618aed3db2423965576b4fcf73e86e7d2e1fc73df875ff678
- c636e888d37abc4d3ffb09db83f161677b906322e89b5ffebd786da46a087209
- c6451652466f7e3d7d0c1e29beecf58284687ebaeee6ef2c384a138be99262db
- c6c17b7b88c357bc2a290ffb4fd481dd567a6b00c57990dbef71d7d7c30f5223
- c6edde9ea6582b828a5b71747a78be95388ae85d6cf43cf718452e7c21f7bae4
- c7294037d58fd396d75e46fad0c35326e6e2c98ef9ae4dc8d59c90854bfa945a
- c73027b8f4c114c1c2ba54994c576592cb3f223dd7117fac7188dba9a7b0d3ad
- c735a9c4aa7c7bcc8a56924bf2266d93333244d5f1f232b8114930e18b3b32c0
- c74393c248b016237ba183ff904e83a23ef962191b4b7dfa90e47f643200d043
- c807d6d0dccde7afc87244864650449403523787d5a801e976a2d1f93aa920de
- c841fda54b8611d27b59aeaa3ca3c74c26865eee100428828df8c1e73ca5ab59
- c8823daab8a56d2e1c776c0ed422d6d166e66176f2f77c3bba112109ea822df2
- cacecc17fab6e7f7bfedc2f8431b870da1ed20cf273bc32bd943969ee1279442
- cae55ded17a5b44bcfe84f1793b80fd79de95b2fb94d7ef6427a397e1dd7b30f
- cba4b7b2251344d277ce61d49ad67a10de2f4d723db55f166e8fa26673818384
- cc0dc001f595426e39ec13d8c06df67bd73953842f3460b5e86e86168c452044
- cc773c3322458c6d32c1eef0573f24b0e6be92a06fc54a04bad36a7d372a7844
- cd10a02a09bbb716dcdd1796bc0b11cac4451ff3f18496535c68464e0d88a603
- cdbb90d6270f7c130228a5cee48c7d35a29f9971f9c437d8a20ac05520faa5b0
- ce92ada041eb88cffe403bb136433ff722b54d0a268cda4cff1873ddb21fc11a
- d0abb3268b14c19aada48fd2b9242fbbb03e9d808959539cac47f33448e4788a
- d0bd9e6766b19c029779ac6ae902bf6bb6b3395521c9993a9fab43ec3940d437
- d0f44d8db88952a9d3b7c72710da4c903e001ff095d2fbb65e468f057304d657
- d119374c2c66030391892b37630b6c9bea20d3c24c8406b227dc1a706b26ea4d
- d1731adeeae99dbf1edb56628067f83f845d5689869be556d3011ef0f023ec21
- d1aaab86fa02d87997171aeb3220b40f5e28046ec4d1674848f9ec5f589f297c
- d1b310600902fc975eefdf989c416b1eff5b588fdd2438fe5d4e2544428bdcdd
- d22a13b9c0974c7610f7142c3b73ac6876ed5fb368ca0cb8ee8808550519469a
- d32a27b4f527dcbca68d307dac8cd0c59aa927b7ed34275015336ece11cb558c
- d3bc19caf52c1e1020da75c39fce890a8ad80392a299ad7d702bbfd870e4fe12
- d4f85dca76b4a052f2882aa4e4c2cfdbe58cd1fe4883dbd93c7d5c7570cc9c56
- d5a2bcd7cd429b4984ef236e24390c1072db8f77a4d58fc3be9567d6b0946e90
- d6646215be839522bade80c7415d0d92b80a9dbe38d34ee1a037e82ae0ea3e01
- d70ca3f9e244eac72e583330d6f826a953da3c3a699ba36d476b33fec9be6b24
- d73ebfe3f923c4e624a87693389a7fe3a7ca6e220c3db34ec8e8ad1c205b4737
- d996e04c5f5eed45fa65d35ced2e2261dd416e85e5f4005579ef0c6c629146c0
- da5cbb3e52d0b6947b8061d8c5278467ee8a2749878ac6a63ca078d350d073d8
- dac53025524bb74aed0d1668e215fd82519aa622112b6642f9cf3b0cf4e3f28b
- dad04dac44fc778f02566d4221377e02aded322fe7e72bdccc01869245438b73
- dad1aca6c3a44e1e035f814d0cca82d012a654e79837890f7f67b5022cbef646
- dbc65d9cadd96a1b7635ec875323835192b788aabc0339a51a085d44c3ec4a09
- dcf21ad953b0abfe309d7207d0dfdb5b4b8ad95a21490fc33b9eb9560a7c2593
- e0734d76e316dc5f66149214e2daf7cbdd42adaeec17c796a1897e88dfaf2e4a
- e075bb2c1d8b21a9a45655ed475e7c99a5aab9e05e96131ad0594f6f0f57c358
- e0ff0a66129d77eb27a18d0034b23f692aaec3ef53afd540097d8d9544a73e52
- e1737608ebe980b3352b9ecf45f0568fb71078b4b07aa3e8959a12c1a1825cb5
- e1838d4f1374e52a1b03e406e65fc1929af724d4e97f9f8d9a499a5839ae1611
- e19bbcd13b45f08f2a9672a754a83bc8694fc426baca63f9534b49e124791cb4
- e1aca7ddb397dfca534235d5c7f3322c18213a03465d4ad7e8da4de8460f931c
- e1cb80a10420ad0ffd703da1060a93630bd7afb9252c18c72783da27cdef36d6
- e21d42684e4441b67782b8951e1a5e6c9e5c25bbd1bc460aa7fda138ea348664
- e2284ab0156c5ec39683e5daf5373ab9d026ac426b6657cad44a4bc0ee22b482
- e23f4d307f1fe13f6706f82e83be6432adfaaca1f9160717b2a4c714a9cf7a9b
- e28cbe04c2ab8238fb07400978914e636a768766c1c8bfe470c4cf5df809e53a
- e36ad23ecec7a67ce67508ce92759ef8e0139360d6ae1497383d8316eb52caa5
- e44f0a97c502090de1156b41a412e84f6eae882a7ff2e71d0e4471ab3b5b2625
- e765454a74c4c25d867cef602fab42a8f20b3b01a2f161a51fdf6ab300471edc
- e7cefcd9037a1ca49504750e29c194a9b1416a73678fda3552e86c59512844e8
- e8064825521865a74081c79f40b8d5481c72df1969521fd762eb27177ddf4148
- e8d7e1b9b30fac9de689f400cd32a1c75ff92ba5d2e50d227be3da921ccf3f17
- e9a430428c22efd804e41691454f8a7df7123529d1d18c3421272f462ed8092a
- e9da34e44d0103b717248071e6ce4688fd073d478eb7affb5912935aea10c5e2
- ea1ae9b7c52b3ddc042c4266cfbc981cef8169e085d67c3bfc70925bf4a50fe0
- eb61219cb4bae318ed3caf9fa707f16555e9031c46d2231bd2eecd7102eaa81c
- eba485badc38c762bb55bb639dc1e83b675daa3d3b1f4483ad573c55832298f3
- ec83b104ed7ca856612e649bdeaf790de006be5ccea6c5d224fa80b1cb92787c
- ee67ee18dbdbb44e265d344da750d3bae0c47984a6539272573fd7921b54452e
- ef2eb86614adfe76aceb13374d280be328b844e6b2a3d24fa718e838cee3f664
- f016ba46250c1bb4895aed14b447088852658c9ca025f2118244b0ff9a144e5b
- f04fa565cf9c69b9f0a6407a2016f66e13a2a8ea675b58ae42f6774917f09ba7
- f0ca5b3da20bccd8d437a889fd693ba4c686d1bb7bc6fe03be5e0a3579b19840
- f11995336b25e6e345b8dfa40158808272f3407bdadea67eed73ce72d4c7ae1d
- f13d0aa7440fe282e41230e3fcb3616955ce049f557b31d78eeac7796e15629c
- f15ada53e469f43ad209531edde505083b7b3881538f2aee2cb16ccf5fa5a984
- f16fb879eb7feebbebba10d24c6039cfec4fbc7812492fadedd9cb5c9c73530e
- f1a45654d740d8937152c96b75f88a53a765bc37977719d6628ccef6c36d79ba
- f1db6dc6c0ee2e8b8919d754cfc64657bf5ef5a46d48263c005302a8b93a60f3
- f207c840fa363afc13e308047ddbe3900683f048366c10e9c135b49a2da886c8
- f22509fa8fa95e8a2c40c44ded7af6b303aae4f50a91832548fe4f335a500c3e
- f3f14dd72b865c952b77cefe7a0389b18a9b684755f06ed7558358f088ab05a0
- f49d19e57f9fa7eb7eb29fc9f24beda5af6ccf27910a7b82fc6d664612698c8d
- f5222297b42fa7057b6f777c70e283c5379f2a27b251fe8824a886f235885732
- f5bd48561c7a03547ef81eda1194387efdfae446c2c0781ecd5566af2005c811
- f658d57eac15c3154b8e32b065f6a3ce42fb9a632f54b52ebe51144b832fd917
- f6cc85dad9e27af744df617aa441ae47816be7150538df14a4e49cdee749be99
- f713043df6f43cd4474b78968b4ce9a6ea1455b50b93d1ffbf0766bea075cc05
- f86c5580856ba80e67098204224526be867c2605ec2b2ce579956aa4093579e9
- f87eeeb50d254807161037c66c9ca94951e770551fb94b6e7c84b6a501236607
- f8885a5bd262e52bd2611a5ac9d199098b4072dbde77c9a6fb8fc95de835f28a
- f8a25164478a3be1b6cf23c17b7baca63ae72e807b6217906a89d8f19357c1bf
- f92133ac2a29624c43f822e055ad891c32e1153dc1d8b063006d99b035067d75
- f9693592d62780dd2a4ed330dc2b102b88b775a839e459c6adefc6eb2bd97b15
- f99824fc5b631944cfe79d602a133c8df60d8c87d237f1f8b93d4cd9800dd086
- f9b0b812ca67adce1f08aa7eff1766d23f70d4c0557fdb6b163a1bf85d39906a
- fac9c33295ba7273537834f6c0c13451c150d5c76a0d33bc043532ebccc780fa
- fb37855300496dfcef5337cf1f59432a448307e18de0c295118c8a9907f2d1e3
- fd90e80286511580bc44eb5ce6c7240228732120bd70a46a8d80441fd0e23deb
- ff0df9c541f351827ae234700b25cf5f9f355ec369b0c9f7c8525de0ab7ef7ae
- ff15128b9d36d79e718ef4556c26c157d1404e3932be165546b31005d32b7393
- ff3ad49bc8390e46428994ac298ff2404921263802a4eee3a5a9d1e0f79db3be
