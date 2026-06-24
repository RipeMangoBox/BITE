# MoDebug GT-paired Human Annotations 20260510

Primary table: `human_annotations.csv`.

Compatibility files:
- `latest_annotations.json`: app-native latest state.
- `annotation_events.jsonl`: append-only save events.

Label definition:
- `OK`: motion is reasonable for the current prompt.
- `ERROR`: motion generated from the current prompt is unreasonable.

The `description` column records the concrete observed issue.
