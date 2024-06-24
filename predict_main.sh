#!/bin/bash

alias mktemp=tempfile

PYTHON=python

function run_part {
    echo "$adapter_name"
    test_data=""
    for lang in $langs; do
        test_data="${test_data} ${test_data_template//%/$lang}"
    done
    export ADAPTER_BASE="model_outputs/$MODEL"
    DATA_NAME=$test_data ADAPTER=$adapter_name $PYTHON predict.py | grep -E "accuracy =|output_name ="
    echo
}

function run_part_temp_file {
tmp_file=$(mktemp)
tmp_file_list="${tmp_file_list} ${tmp_file}"
echo $MODEL > "$tmp_file"
run_part >> "$tmp_file"
}

function run_main_models {
tmp_file_list="/dev/null"

export MODEL="llama-2-7b-chat"
run_part_temp_file &
export MODEL="qwen1.5-7b-chat"
run_part_temp_file &
export MODEL="bloomz-7b1-mt"
run_part_temp_file &
export MODEL="mistral-7b-instruct-v0.1"
run_part_temp_file &

wait
cat ${tmp_file_list}
}

function run_aux_models {
tmp_file_list="/dev/null"

langs="EN AR"
export MODEL="llama-2-7b-chat-arabic-lora"
run_part_temp_file &
export MODEL="sambalingo-arabic-base"
run_part_temp_file &
export MODEL="sambalingo-arabic-chat"
run_part_temp_file &

langs="EN HE"
export MODEL="dictalm-2"
run_part_temp_file &
export MODEL="dictalm-2-instruct"
run_part_temp_file &

wait
cat ${tmp_file_list}
}

function run_main {

langs="EN DE AR HE FR IT RU PL ZH JA"

export DATA_INFO_PATH="$PWD/prepared_data/dataset_info.json"

# StrategyQA

export ALLOW_TOK='["Yes", "No"]'
test_data_template="sqa_facts_dev_%"
adapter_name="sqa_facts_train2e-4_0_4_lora-all"
run_main_models
test_data_template="sqa_dev_%"
adapter_name="sqa_train2e-4_0_4_lora-all"
run_main_models
test_data_template="sqa_facts_dev_% sqa_dev_%"
adapter_name="none"
run_main_models

export MODEL="llama-2-7b-chat"
test_data_template="sqa_one_fact_dev_%"
adapter_name="sqa_one_fact_train2e-4_0_4_lora-all"
run_part
test_data_template="sqa_two_fact_dev_%"
adapter_name="sqa_two_fact_train2e-4_0_4_lora-all"
run_part
test_data_template="sqa_one_fact_dev_% sqa_two_fact_dev_%"
adapter_name="none"
run_part

# Main + SFT-CPT

export ALLOW_TOK='["A", "B", "C", "D"]'
test_data_template="kfrd_arithmetic_%_test"
adapter_name="kfrd_arithmetic_EN_train2e-4_0_4_lora-all"
run_main_models
test_data_template="kfrd_symbolic_%_test"
adapter_name="kfrd_symbolic_EN_train2e-4_0_1_lora-all"
run_main_models
test_data_template="kfrd_logical_%_test"
adapter_name="kfrd_logical_EN_train2e-4_0_1_lora-all"
run_main_models
test_data_template="kfrd_arithmetic_%_test kfrd_symbolic_%_test kfrd_logical_%_test"
adapter_name="none"
run_main_models

# Other Languages

export MODEL="llama-2-7b-chat"
test_data_template="kfrd_arithmetic_%_test"
adapter_name="kfrd_arithmetic_ZH_train2e-4_0_4_lora-all" run_part
adapter_name="kfrd_arithmetic_DE_train2e-4_0_4_lora-all" run_part
adapter_name="kfrd_arithmetic_HE_train2e-4_0_4_lora-all" run_part
adapter_name="kfrd_arithmetic_AR_train2e-4_0_4_lora-all" run_part

test_data_template="kfrd_symbolic_%_test"
adapter_name="kfrd_symbolic_ZH_train2e-4_0_1_lora-all" run_part
adapter_name="kfrd_symbolic_DE_train2e-4_0_1_lora-all" run_part
adapter_name="kfrd_symbolic_HE_train2e-4_0_1_lora-all" run_part
adapter_name="kfrd_symbolic_AR_train2e-4_0_1_lora-all" run_part

test_data_template="kfrd_logical_%_test"
adapter_name="kfrd_logical_ZH_train2e-4_0_1_lora-all" run_part
adapter_name="kfrd_logical_DE_train2e-4_0_1_lora-all" run_part
adapter_name="kfrd_logical_HE_train2e-4_0_1_lora-all" run_part
adapter_name="kfrd_logical_AR_train2e-4_0_1_lora-all" run_part

# SFT-CPT

test_data_template="kfrd_arithmetic_%_test"
adapter_name="kfrd_arithmetic_EN_train2e-4_0_4_lora-all"
run_aux_models
test_data_template="kfrd_symbolic_%_test"
adapter_name="kfrd_symbolic_EN_train2e-4_0_1_lora-all"
run_aux_models
test_data_template="kfrd_logical_%_test"
adapter_name="kfrd_logical_EN_train2e-4_0_1_lora-all"
run_aux_models

exit
}

run_main
