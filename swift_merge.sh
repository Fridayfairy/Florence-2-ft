USE_HF=1 CUDA_VISIBLE_DEVICES=0,1 NPROC_PER_NODE=2 swift export \
    --ckpt_dir "/data1/home/ycx/tools/FT-Florence2-swift/output_lora/florence-2-large-ft/v1-20240913-171907/checkpoint-186" \
    --merge_lora true