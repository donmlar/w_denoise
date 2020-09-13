import os

# import tensorflow as tf
from tensorflow import Session ,GraphDef , import_graph_def

from tensorflow.python.platform import gfile
import numpy as np
import rawpy
import glob
import scipy.io
import time
from PIL import Image
import white_balance
from numpy.lib.stride_tricks import as_strided
from pb_use_m import pack_raw
import tifffile as tiff
from threading import Thread

def pool2d(A, kernel_size, stride, padding, pool_mode='max'):
        '''
        2D Pooling

        Parameters:
            A: input 2D array
            kernel_size: int, the size of the window
            stride: int, the stride of the window
            padding: int, implicit zero paddings on both sides of the input
            pool_mode: string, 'max' or 'avg'
        '''
        # Padding
        A = np.pad(A, padding, mode='constant')

        # Window view of A
        output_shape = ((A.shape[0] - kernel_size) // stride + 1,
                        (A.shape[1] - kernel_size) // stride + 1)
        kernel_size = (kernel_size, kernel_size)
        A_w = as_strided(A, shape=output_shape + kernel_size,
                         strides=(stride * A.strides[0],
                                  stride * A.strides[1]) + A.strides)
        A_w = A_w.reshape(-1, *kernel_size)

        # Return the result of pooling
        if pool_mode == 'max':
            return A_w.max(axis=(1, 2)).reshape(output_shape)
        elif pool_mode == 'avg':
            return A_w.mean(axis=(1, 2)).reshape(output_shape)


def reduce(input_full):
    output = np.zeros(   (int(input_full.shape[0]/2),int(input_full.shape[1]/2)   ,4) ,dtype=np.float32)
    output[:,:,0]= pool2d(input_full[:,:,0], kernel_size=2, stride=2, padding=0, pool_mode='avg')
    output[:,:,1]= pool2d(input_full[:,:,1], kernel_size=2, stride=2, padding=0, pool_mode='avg')
    output[:,:,2]= pool2d(input_full[:,:,2], kernel_size=2, stride=2, padding=0, pool_mode='avg')
    output[:,:,3]= pool2d(input_full[:,:,3], kernel_size=2, stride=2, padding=0, pool_mode='avg')

    while output.shape[0]>600:
        output = reduce(output)
    return output


class ViewThread(Thread):

    def __init__(self,dict):
        Thread.__init__(self)


        self.pb_file_path =dict['pb_path']
        self.raw_file =dict['fileName']
        self.light =dict['light']
        self.rate = dict['rate']
        self.gamma =dict['gamma']
        self.blue_gain = dict['blue_gain']
        self.green_gain = dict['green_gain']

        self.purple_drift = dict['purple_drift']

        if dict['cpu_only']:
            os.environ["CUDA_VISIBLE_DEVICES"] = "-1"


    # 浏览图
    def run(self):
    #
        sess = Session()
        with gfile.FastGFile(self.pb_file_path, 'rb') as f:
            graph_def = GraphDef()
            graph_def.ParseFromString(f.read())
            sess.graph.as_default()
            import_graph_def(graph_def, name='')

            in_image = sess.graph.get_tensor_by_name('in_image:0')
            out_image = sess.graph.get_tensor_by_name('output:0')

            name = self.raw_file.split('/')[-1].split('.')[0]
            print('开始计算浏览图：' + name + "")
            # 计算放大
            # 按照10分 放大比例
            before_amp = 2** (self.light*(5-self.rate)/10)
            after_amp = 2** (self.light*(5+self.rate)/10)


            tick1 = time.time()
            raw = rawpy.imread(self.raw_file)

            wb, black, raw_pattern = white_balance.get_camera_wb(self.raw_file ,blue_gain=self.blue_gain ,green_gain = self.green_gain )
            raw_pattern = str(raw_pattern).replace('\n', '').replace('\r', '')

            black = black[0]
            input_full = pack_raw(raw, raw_pattern, black)*before_amp
            input_full = reduce(input_full)
            input_full = np.expand_dims(input_full, axis=0)
            # input_full = np.minimum(input_full, 1.0)

            # 暗部处理
            input_full = np.power(input_full, 1 / (1+self.gamma))

            # 暗部紫色偏移处理

            drift_value = self.purple_drift*0.0001
            input_full_tmp = input_full[:,:,:,2]
            input_full[:, :, :, 2] = input_full_tmp+drift_value

            input_full_tmp = input_full[:,:,:,0]
            input_full[:, :, :, 0] = input_full_tmp+drift_value

            output = sess.run(out_image, feed_dict={in_image: input_full})
            # output = np.minimum(np.maximum(output, 0), 1)

            output = output[0, :, :, :]
            # 白平衡矫正
            b = output[:, :, np.newaxis, :]
            b = np.matmul(b, wb)
            c = np.squeeze(b)*after_amp
            c = np.minimum(np.maximum(c, 0), 1)
            output = (c * 255).astype(np.uint8)

            im = Image.fromarray(output, 'RGB')


            im.save('./tmp/' + name + "_v.png")

            self.viewImg = output
            tick2 = time.time()
            print('用时：'+str(round(tick2 - tick1,2))+'秒')
            print('完成：'+name + " 浏览")

            print('浏览图仅用于参考曝光，不代表最终输出效果。')

    def getViewImg(self):
        return self.viewImg


