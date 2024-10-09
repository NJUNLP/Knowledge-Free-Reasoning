#!/bin/bash
REQUIRED_GPUS=4 # number of GPU
batch_size=4
accumula=$((64/REQUIRED_GPUS/batch_size))

BASE_DIR="$PWD"
output_prefix="$BASE_DIR/model_outputs"

flash_attn=0

MASTER_PORT=$(python -c 'import socket; s = socket.socket(); s.bind(("", 0)); print(s.getsockname()[1]); s.close()')
# Automatically find free GPU
FREE_GPUS=$(python -c "
import subprocess
import re
import sys

def find_free_gpus():
    output = subprocess.check_output(['nvidia-smi', '--query-gpu=utilization.gpu,memory.free', '--format=csv,nounits,noheader'], universal_newlines=True)
    lines = output.strip().split('\\n')
    free_gpus = []
    for i, line in enumerate(lines):
        util, mem = map(int, re.split(',\\s*', line))
        if util < 10 and mem > 23000:
            free_gpus.append(str(i))

    if len(free_gpus) < $REQUIRED_GPUS:
        sys.stderr.write(f'Error: Not enough free GPUs. Required: $REQUIRED_GPUS, Available: {len(free_gpus)}\\n')
        sys.exit(1)

    print(','.join(free_gpus[:$REQUIRED_GPUS]))

find_free_gpus()
")
echo "Using GPUs: $FREE_GPUS"


function run_part {

model_name=${model##*/}
echo "model_name: $model_name"
template="$(python "$BASE_DIR/utils/model_registry.py" $model default_template)"
lora_target="all"
echo "lora_target: $lora_target"

dataset_dir="$BASE_DIR/prepared_data"

cd "$BASE_DIR" || exit
model_dir="$(realpath "$(python "$BASE_DIR/utils/model_registry.py" $model path)")"
cd "$BASE_DIR/LLaMA-Factory" || exit

lr=2e-4
dropout=0
lora_alpha=16
# ds_config="$PWD/examples/deepspeed/ds_z0_config.json"
ds_config="$PWD/examples/deepspeed/ds_z2_offload_config_mod.json"
suffix="lora-all"
adapter_args=""

for dataset in "${datasets[@]}"; do
    echo "$dataset"
    
    output_dir="${output_prefix}/${model_name}/${dataset}${lr}_${dropout}_${step}_${suffix}"
    
    deepspeed --include "localhost:$FREE_GPUS" --master_port="$MASTER_PORT" \
        "$PWD/src/train_bash.py" \
        --deepspeed "$ds_config" \
        --stage sft \
        --model_name_or_path "$model_dir" \
        $adapter_args \
        --do_train \
        --dataset_dir "$dataset_dir" \
        --dataset  "$dataset" \
        --template "$template" \
        --output_dir  "$output_dir" \
        --overwrite_cache \
        --per_device_train_batch_size $batch_size \
        --gradient_accumulation_steps $accumula \
        --lr_scheduler_type cosine \
        --logging_steps 1 \
        --learning_rate "$lr" \
        --num_train_epochs "$step" \
        --plot_loss \
        --save_strategy steps \
        --save_steps 5000 \
        --max_grad_norm 1.0 \
        --flash_attn $flash_attn \
        --gradient_checkpointing 1 \
        --finetuning_type lora \
        --lora_target $lora_target	 \
        --lora_rank 128 \
        --lora_alpha "$lora_alpha" \
        --lora_dropout "$dropout" \
    
done

}

function run_main {

mkdir -p "$BASE_DIR/model_outputs"

# StrategyQA

datasets=(
    "sqa_train"
    "sqa_facts_train"
)
step=4
model="mistral-7b-instruct-v0.1"
run_part
model="bloomz-7b1-mt"
run_part
model="qwen1.5-7b-chat"
run_part
model="llama-2-7b-chat"
run_part


datasets=(
    "sqa_one_fact_train"
    "sqa_two_fact_train"
)
step=4
model="llama-2-7b-chat"
run_part


# QASC

datasets=(
    "qasc_train"
    "qasc_two_facts_train"
)
step=1
model="mistral-7b-instruct-v0.1"
run_part
model="bloomz-7b1-mt"
run_part
model="qwen1.5-7b-chat"
run_part
model="llama-2-7b-chat"
run_part


datasets=(
    "qasc_one_facts_train"
)
step=1
model="llama-2-7b-chat"
run_part


# Main + SFT-CPT

datasets=(
    "kfrd_arithmetic_EN_train"
    "asdiv_a_train_EN"
)
step=4
model="mistral-7b-instruct-v0.1"
run_part
model="bloomz-7b1-mt"
run_part
model="qwen1.5-7b-chat"
run_part
model="llama-2-7b-chat"
run_part
model="sambalingo-arabic-base"
run_part
model="sambalingo-arabic-chat"
run_part
model="dictalm-2"
run_part
model="dictalm-2-instruct"
run_part
model="llama-2-7b-chat-arabic-lora"
run_part


datasets=(
    "kfrd_symbolic_EN_train"
    "kfrd_logical_EN_train"
    "coin_flip_train"
    "proofwriter_all_train_depth1_EN"
)
step=1
model="mistral-7b-instruct-v0.1"
run_part
model="bloomz-7b1-mt"
run_part
model="qwen1.5-7b-chat"
run_part
model="llama-2-7b-chat"
run_part
model="sambalingo-arabic-base"
run_part
model="sambalingo-arabic-chat"
run_part
model="dictalm-2"
run_part
model="dictalm-2-instruct"
run_part
model="llama-2-7b-chat-arabic-lora"
run_part


# Other Languages

datasets=(
    "kfrd_arithmetic_ZH_train"
    "kfrd_arithmetic_DE_train"
    "kfrd_arithmetic_HE_train"
    "kfrd_arithmetic_AR_train"
)
step=4
model="llama-2-7b-chat"
run_part


datasets=(
    "kfrd_symbolic_ZH_train"
    "kfrd_symbolic_DE_train"
    "kfrd_symbolic_HE_train"
    "kfrd_symbolic_AR_train"
    "kfrd_logical_ZH_train"
    "kfrd_logical_DE_train"
    "kfrd_logical_HE_train"
    "kfrd_logical_AR_train"
)
step=1
model="llama-2-7b-chat"
run_part


# Intepretability

datasets=("mkqa_v2_train_EN")
step=2
model="llama-2-7b-chat"
run_part


datasets=(
    "boolq_train_EN"
    "ambig_train_EN"
    "kfrd_symbolic_EN_train_10k"
    "kfrd_logical_EN_train_10k"
)
step=1
model="llama-2-7b-chat"
run_part


exit
}

run_main
