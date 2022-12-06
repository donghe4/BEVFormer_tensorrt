_base_ = ["bevformer_tiny_trt.py"]

model = dict(
    img_backbone=dict(type="ResNetQ", conv_cfg=dict(type="Conv2dQ")),
    img_neck=dict(conv_cfg=dict(type="Conv2dQ")),
    pts_bbox_head=dict(
        linear_cfg=dict(type="LinearQ"),
        transformer=dict(
            linear_cfg=dict(type="LinearQ"),
            encoder=dict(
                transformerlayers=dict(
                    ffn_cfgs=dict(linear_cfg=dict(type="LinearQ")),
                    attn_cfgs=[
                        dict(
                            type="TemporalSelfAttentionTRT",
                            embed_dims={{_base_._dim_}},
                            num_levels=1,
                            linear_cfg=dict(type="LinearQ"),
                        ),
                        dict(
                            type="SpatialCrossAttentionTRT",
                            pc_range={{_base_.point_cloud_range}},
                            deformable_attention=dict(
                                type="MSDeformableAttention3DTRT",
                                embed_dims={{_base_._dim_}},
                                num_points=8,
                                num_levels={{_base_._num_levels_}},
                                linear_cfg=dict(type="LinearQ"),
                            ),
                            embed_dims={{_base_._dim_}},
                            linear_cfg=dict(type="LinearQ"),
                        ),
                    ],
                )
            ),
            decoder=dict(
                transformerlayers=dict(
                    attn_cfgs=[
                        dict(
                            type="MultiheadAttention",
                            embed_dims={{_base_._dim_}},
                            num_heads=8,
                            dropout=0.1,
                        ),
                        dict(
                            type="CustomMSDeformableAttentionTRT",
                            embed_dims={{_base_._dim_}},
                            num_levels=1,
                            linear_cfg=dict(type="LinearQ"),
                        ),
                    ],
                    ffn_cfgs=dict(linear_cfg=dict(type="LinearQ")),
                )
            ),
        ),
    ),
)


data = dict(
    samples_per_gpu=1,
    quant=dict(
        type={{_base_.dataset_type}},
        data_root={{_base_.data_root}},
        ann_file={{_base_.data.train.ann_file}},
        pipeline={{_base_.test_pipeline}},
        bev_size={{_base_.data.train.bev_size}},
        classes={{_base_.class_names}},
        modality={{_base_.input_modality}},
        test_mode=True,
        box_type_3d="LiDAR",
    ),
)

# learning policy
lr_config = dict(_delete_=True, policy="step", step=[10])

total_epochs = 1
runner = dict(type="EpochBasedRunner", max_epochs=total_epochs)

optimizer = dict(
    type="SGD",
    lr=1e-6,
    momentum=0.9,
    weight_decay=5e-4,
    nesterov=True,
    paramwise_cfg=dict(norm_decay_mult=0.0, bias_decay_mult=0.0),
)
optimizer_config = dict(grad_clip=None)

load_from = "checkpoints/pytorch/bevformer_tiny_epoch_24.pth"
