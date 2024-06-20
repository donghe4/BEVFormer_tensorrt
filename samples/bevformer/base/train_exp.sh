#!/bin/bash

# CUDA_VISIBLE_DEVICES='0,2' python -m torch.distributed.launch \
# --nproc_per_node=2 --master_port=28509 tools/bevformer/train.py configs/bevformer/bevformer_base.py --launcher pytorch


CUDA_VISIBLE_DEVICES='0,1,3' python -m torch.distributed.launch \
--nproc_per_node=3 --master_port=28509 tools/bevformer/train.py configs/bevformer/bevformer_small.py --launcher pytorch