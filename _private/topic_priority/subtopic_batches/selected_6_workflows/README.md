# Selected 6 Workflows

- generated_at: `2026-05-12`
- policy: one existing `25`-paper batch selected for each requested subtopic
- source_root: `_private/topic_priority/subtopic_batches/batches`

## Selected Workflows

1. `vision_models_multimodal`
   manifest: `_private/topic_priority/subtopic_batches/batches/iclr26_vision_multimodal_applications__vision_models_multimodal__b001.jsonl`
   papers: `25`

2. `language_speech_and_dialog`
   manifest: `_private/topic_priority/subtopic_batches/batches/iclr26_vision_multimodal_applications__language_speech_and_dialog__b001.jsonl`
   papers: `25`

3. `generative_models_and_autoencoders`
   manifest: `_private/topic_priority/subtopic_batches/batches/iclr26_generative_models_diffusion__generative_models_and_autoencoders__b001.jsonl`
   papers: `25`

4. `image_and_video_generation`
   manifest: `_private/topic_priority/subtopic_batches/batches/iclr26_vision_multimodal_applications__image_and_video_generation__b001.jsonl`
   papers: `25`

5. `representation_learning`
   manifest: `_private/topic_priority/subtopic_batches/batches/iclr26_representation_self_supervised_transfer__representation_learning__b001.jsonl`
   papers: `25`

6. `deep_rl`
   manifest: `_private/topic_priority/subtopic_batches/batches/iclr26_reinforcement_learning_planning_agents__deep_rl__b001.jsonl`
   papers: `25`

## Run Template

```bash
cd /home/ripemangobox/Coding/Github/OpenSource/Open_Ready/ResearchFlow/researchflow-backend
PYTHONNOUSERSITE=1 ./.venv/bin/python scripts/run_local_iclr26_batch.py \
  --batch-manifest <manifest_path> \
  --limit 25 \
  --run-id <custom_run_id> \
  --provider deepseek \
  --api-key-env DEEPSEEK_API_KEY \
  --output-root ../_private/iclr26_batch/runs \
  --report-root ../_private/iclr26_batch/runs/batch_reports \
  --force
```
