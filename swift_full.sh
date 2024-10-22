# grounding task
USE_HF=1 CUDA_VISIBLE_DEVICES=0,1 NPROC_PER_NODE=2 WANDB_PROJECT="Florence-full" swift sft \
    --model_type florence-2-large-ft \
    --model_id_or_path /data1/home/ycx/ycxGit/Florence-2-large-ft \
    --dataset /data1/home/ycx/tools/FT-Florence2-swift/od_datasets/train_set.jsonl \
    --val_dataset /data1/home/ycx/tools/FT-Florence2-swift/od_datasets/val_set.jsonl#1000 \
    --freeze_vit true \
    --sft_type full \
    --learning_rate 1e-5 \
    --eval_steps 10 \
    --report_to wandb \
    --gradient_accumulation_steps 50 \
    --lazy_tokenize true \
    --preprocess_num_proc 8 \
    --check_model_is_latest false \
    --num_train_epochs 1 \
    --deepspeed config_zero3.json \
    --output_dir output_full \
    --save_strategy steps \
    --batch_size 4 \
    --save_total_limit -1 

