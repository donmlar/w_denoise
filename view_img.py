import tensorflow as tf
from tensorflow.python.platform import gfile
import numpy as np
import rawpy
import glob
import scipy.io
import time
from PIL import Image
import white_balance
from numpy.lib.stride_tricks import as_strided
from pb_use import pack_raw

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

    while output.shape[0]>120:
        output = reduce(output)
    return output


class ViewThread(Thread):

    def __init__(self,pb_file_path ,raw_file  ,light,rate,gamma):
        Thread.__init__(self)
        self.pb_file_path =pb_file_path
        self.raw_file =raw_file
        self.light =light
        self.rate = rate
        self.gamma =gamma


    # 浏览图
    def run(self):
    #
        sess = tf.Session()
        with gfile.FastGFile(self.pb_file_path, 'rb') as f:
            graph_def = tf.GraphDef()
            graph_def.ParseFromString(f.read())
            sess.graph.as_default()
            tf.import_graph_def(graph_def, name='')

            in_image = sess.graph.get_tensor_by_name('in_image:0')
            out_image = sess.graph.get_tensor_by_name('output:0')

            name = self.raw_file.split('/')[-1].split('.')[0]

            # 计算放大
            # 按照10分 放大比例
            before_amp = 2** (self.light*(5-self.rate)/10)
            after_amp = 2** (self.light*(5+self.rate)/10)

            print('before_amp:'+str(before_amp))
            print('after_amp:'+str(after_amp))

            tick1 = time.time()
            raw = rawpy.imread(self.raw_file)

            wb, black, raw_pattern = white_balance.get_camera_wb(self.raw_file)
            raw_pattern = str(raw_pattern).replace('\n', '').replace('\r', '')

            black = black[0]
            input_full = pack_raw(raw, raw_pattern, black)*before_amp
            input_full = reduce(input_full)
            input_full = np.expand_dims(input_full, axis=0)
            input_full = np.minimum(input_full, 1.0)

            # 暗部处理
            input_full = np.power(input_full, 1 / (1+self.gamma))

            output = sess.run(out_image, feed_dict={in_image: input_full})
            output = np.minimum(np.maximum(output, 0), 1)

            output = output[0, :, :, :]
            # 白平衡矫正
            b = output[:, :, np.newaxis, :]
            b = np.matmul(b, wb)
            c = np.squeeze(b)*after_amp
            c = np.minimum(np.maximum(c, 0), 1)
            output = (c * 255).astype(np.uint8)

            im = Image.fromarray(output, 'RGB')


            im.save('./output/' + name + "_v.png")




            self.viewImg = output
            tick2 = time.time()
            print(tick2 - tick1)
            print('完成：'+name + " view")

    def getViewImg(self):
        return self.viewImg


