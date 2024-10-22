USE_HF=1 CUDA_VISIBLE_DEVICES=0 swift infer \
    --model_type florence-2-large-ft \
    --model_id_or_path /data1/home/ycx/ycxGit/Florence-2-large-ft \
    --max_new_tokens 1024 --stream false
