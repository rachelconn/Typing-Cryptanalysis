#!/bin/bash

# --dataset_config_names clean clean other \
# --dataset_split_names train.100 train.360 train.500 \

accelerate launch pretrain.py \
	--dataset_name="dataset/unlabeled" \
	--model_name_or_path="patrickvonplaten/wav2vec2-base-v2" \
	--output_dir="./wav2vec2-pretrained-demo" \
	--max_train_steps="90000" \
	--num_warmup_steps="15000" \
	--gradient_accumulation_steps="8" \
	--learning_rate="0.001" \
	--weight_decay="0.01" \
	--max_duration_in_seconds="20.0" \
	--min_duration_in_seconds="2.0" \
	--logging_steps="1" \
	--saving_steps="1000" \
	--per_device_train_batch_size="2" \
	--per_device_eval_batch_size="2" \
	--adam_beta1="0.9" \
	--adam_beta2="0.98" \
	--adam_epsilon="1e-06" \
	--gradient_checkpointing \
