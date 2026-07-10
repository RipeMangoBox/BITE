#!/usr/bin/env bash
set -euo pipefail

BASE=/data/public/ripemangobox/Motion/baselines
CONDA=/home/ripemangobox/miniconda3/bin/conda

mkdir -p "$BASE/logs" "$BASE/data"

"$CONDA" create -y -n molingo-pulp-cu128 python=3.10
source /home/ripemangobox/miniconda3/etc/profile.d/conda.sh
conda activate molingo-pulp-cu128
python -m pip install --upgrade pip
python -m pip install torch==2.8.0 torchvision==0.23.0 torchaudio==2.8.0 --index-url https://download.pytorch.org/whl/cu128
python -m pip install numpy==1.23.5 scipy tqdm einops transformers sentencepiece accelerate matplotlib rich wandb pyyaml moviepy imageio imageio-ffmpeg smplx chumpy

conda deactivate

"$CONDA" create -y -n director-pulp-cu128 python=3.10
conda activate director-pulp-cu128
python -m pip install --upgrade pip
python -m pip install torch==2.8.0 torchvision==0.23.0 torchaudio==2.8.0 --index-url https://download.pytorch.org/whl/cu128
python -m pip install -r "$BASE/DIRECTOR_storymotion_20260626/requirements.txt"
python -m pip install numpy==1.26.4

conda deactivate
