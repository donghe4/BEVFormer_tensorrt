import pycuda.autoinit
import unittest
import sys

sys.path.append(".")
import det2trt
from det2trt.models.utils.test_trt_ops.test_modulated_deformable_conv2d import *
from det2trt.models.utils.test_trt_ops.test_grid_sampler import *
from det2trt.models.utils.test_trt_ops import *

if __name__ == "__main__":
    unittest.main()
