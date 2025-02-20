
lr=5e-5 # 5e-5
batch_size=8 # 8/16/32/64
beam_size=5
source_length=512
target_length=512
output_dir=/home/zhengjie/Desktop/ccf_competition/UniXcoder_repair/models
input_dir=/home/zhengjie/Desktop/ccf_competition/UniXcoder_repair/dataset
train_file=$input_dir/src-train.txt,$input_dir/tgt-train.txt
dev_file=$input_dir/src-val.txt,$input_dir/tgt-val.txt
log_file=train_set1.log
epochs=30  # 30
pretrained_model=microsoft/unixcoder-base

mkdir -p $output_dir

python run.py --do_train --do_eval --model_name_or_path $pretrained_model --train_filename $train_file --dev_filename $dev_file --output_dir $output_dir --max_source_length $source_length --max_target_length $target_length --beam_size $beam_size --train_batch_size $batch_size --eval_batch_size $batch_size --learning_rate $lr --num_train_epochs $epochs 2>&1| tee $output_dir/$log_file


	