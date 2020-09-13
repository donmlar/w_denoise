

import rawpy
import numpy as np



def get_camera_wb(file_name , blue_gain=0 , green_gain=0):
    file = rawpy.imread(file_name)


    wb = file.camera_whitebalance

    black = file.black_level_per_channel

    raw_pattern = file.raw_pattern

    # print(wb)
    # print(black)

    # 映射到3x3对角矩阵
    nz3 = np.zeros((3,3) ,dtype=np.float32)
    nz3[0 , 0] = wb[0]/wb[1]
    nz3[1 , 1] = (wb[1]/wb[1])*(1+green_gain)
    nz3[2 , 2] = (wb[2]/wb[1])*(1+blue_gain)

    return nz3 , black,raw_pattern



