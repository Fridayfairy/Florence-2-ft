# grounding task
USE_HF=1 CUDA_VISIBLE_DEVICES=0,1 NPROC_PER_NODE=2 WANDB_PROJECT="Florence-lora" swift sft \
    --model_type florence-2-large-ft \
    --model_id_or_path /data1/home/ycx/ycxGit/Florence-2-large-ft \
    --dataset /data1/home/ycx/tools/FT-Florence2-swift/od_datasets/train_set.jsonl \
    --val_dataset /data1/home/ycx/tools/FT-Florence2-swift/od_datasets/val_set.jsonl#1000 \
    --lora_target_modules ALL \
    --report_to wandb \
    --gradient_accumulation_steps 50 \
    --lazy_tokenize true \
    --preprocess_num_proc 8 \
    --check_model_is_latest false \
    --num_train_epochs 1 \
    --deepspeed config_zero3.json \
    --output_dir output_lora \
    --save_strategy steps \
    --batch_size 4 \
    --sft_type lora \
    --lora_rank 32 \
    --lora_alpha 64 \
    --lora_dropout 0.1 \
    --save_total_limit -1 \
    --max_steps 1

