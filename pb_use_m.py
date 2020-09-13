# import tensorflow as tf

from tensorflow import Session ,GraphDef , import_graph_def

from tensorflow.python.platform import gfile
import numpy as np
import rawpy
import math
import time
from PIL import Image
import white_balance
import tifffile as tiff
from threading import Thread

import os



pb_path_normal = './pb_model/n3/frozen_model.pb'


# pb_path_normal = './pb_model/highlight2/frozen_model.pb'


pb_path_soft = './pb_model/highlight2/frozen_model.pb'


pb_path_soft = './pb_model/soft4/frozen_model.pb'

pb_path_sharp = './pb_model/sharp2/frozen_model.pb'

pb_path_mix =  './pb_model/mix/frozen_model.pb'




def pack_raw(raw ,raw_pattern ,black ):
    # pack Bayer image to 4 channels
    im = raw.raw_image_visible.astype(np.float32)
    # im = np.maximum(im - 512, 0) / (16383 - 512)  # subtract the black level

    max_value = im.max()
    white = 1023
    if max_value>1024:
        white = 4096
    if max_value>4096:
        white = 16383

    im = np.maximum(im-black , 0) / (white)
    im = np.expand_dims(im, axis=2)
    img_shape = im.shape


    # vivo
    if raw_pattern == '[[2 3] [1 0]]':
        H = img_shape[0]
        W = img_shape[1]

        out = np.concatenate((im[0:H:2, 0:W:2, :],
                              im[0:H:2, 1:W:2, :],
                              im[1:H:2, 1:W:2, :],
                              im[1:H:2, 0:W:2, :]), axis=2)
    # s6
    elif  raw_pattern == '[[1 0] [2 3]]':
        H = img_shape[0] - 4
        W = img_shape[1]

        imt = im[3:img_shape[0] - 1, 0:img_shape[1], :]
        out = np.concatenate((imt[0:H:2, 0:W:2, :],  # 绿1
                              imt[0:H:2, 1:W:2, :],  # 红
                              imt[1:H:2, 1:W:2, :],  # 绿2
                              imt[1:H:2, 0:W:2, :]), axis=2)  # 蓝
    # zz6
    elif  raw_pattern == '[[0 1] [3 2]]':
        H = img_shape[0] - 4
        W = img_shape[1] - 4
        imt = im[3:H - 1, 3:W - 1, :]
        out = np.concatenate((imt[0:H:2, 0:W:2, :],  # 绿1
                              imt[0:H:2, 1:W:2, :],  # 红
                              imt[1:H:2, 1:W:2, :],  # 绿2
                              imt[1:H:2, 0:W:2, :]), axis=2)  # 蓝

    #
    elif  raw_pattern == '[[3 2] [0 1]]':
        H = img_shape[0]
        W = img_shape[1] - 4
        imt = im[0:H, 3:W - 1, :]
        out = np.concatenate((imt[0:H:2, 0:W:2, :],  # 绿1
                              imt[0:H:2, 1:W:2, :],  # 红
                              imt[1:H:2, 1:W:2, :],  # 绿2
                              imt[1:H:2, 0:W:2, :]), axis=2)  # 蓝


    return out




# light  亮度放大
# rate   亮度前后级比例
# gamma  暗部放大

class restore_mode_pb_single(Thread):

    def __init__(self,dict):
        Thread.__init__(self)
        self.pb_file_path =dict['pb_path']
        self.raw_file =dict['fileName']
        self.light =dict['light']
        self.rate = dict['rate']
        self.gamma =dict['gamma']
        self.blue_gain = dict['blue_gain']
        self.green_gain = dict['green_gain']

        self.output_path = dict['output_path']

        self.purple_drift = dict['purple_drift']

        if dict['cpu_only']:
            os.environ["CUDA_VISIBLE_DEVICES"] = "-1"




    def run(self):

        sess = Session()
        with gfile.FastGFile(self.pb_file_path , 'rb') as f:
            graph_def = GraphDef()
            graph_def.ParseFromString(f.read())

            sess.graph.as_default()

            import_graph_def(graph_def, name='')


            in_image = sess.graph.get_tensor_by_name('in_image:0')
            out_image = sess.graph.get_tensor_by_name('output:0')

            name = self.raw_file.split('/')[-1].split('.')[0]

            print('开始降噪：' + name + "")
            # 计算放大
            # 按照10分 放大比例
            before_amp = 2** (self.light*(5-self.rate)/10)
            after_amp = 2** (self.light*(5+self.rate)/10)


            raw = rawpy.imread(self.raw_file)

            wb, black, raw_pattern = white_balance.get_camera_wb(self.raw_file , blue_gain=self.blue_gain,green_gain=self.green_gain)
            raw_pattern = str(raw_pattern).replace('\n', '').replace('\r', '')

            black = black[0]
            input_full = np.expand_dims(pack_raw(raw, raw_pattern, black), axis=0)*before_amp
            # input_full = np.minimum(input_full, 1.0)
            # 暗部处理
            input_full = np.power(input_full, 1 / (1+self.gamma))


            # 暗部紫色偏移处理

            drift_value = self.purple_drift*0.0001
            input_full_tmp = input_full[:,:,:,2]
            input_full[:, :, :, 2] = input_full_tmp+drift_value

            input_full_tmp = input_full[:,:,:,0]
            input_full[:, :, :, 0] = input_full_tmp+drift_value
            # 图像通道对应
            # 0 b
            # 1 g
            # 2 r
            # 3 g


            output = sess.run(out_image, feed_dict={in_image: input_full})


            output = np.minimum(np.maximum(output, 0), 1)*after_amp

        # output = output[0, :, :, :]
        # # 白平衡矫正
        # b = output[:, :, np.newaxis, :]
        # b = np.matmul(b, wb)
        # c = np.squeeze(b)*after_amp
        # self.output = np.minimum(np.maximum(c, 0), 1)

        output = output[0, :, :, :]
        # 白平衡矫正
        b = output[:, :, np.newaxis, :]
        b = np.matmul(b, wb)
        c = np.squeeze(b)
        self.output = np.minimum(np.maximum(c, 0), 1)


    def get_result(self):
        Thread.join(self)  # 等待线程执行完毕
        try:
            return self.output
        except Exception:
            return None




class mix(Thread):

    def __init__(self,dict):
        Thread.__init__(self)
        self.pb_file_path =dict['pb_path']
        self.normal =dict['normal']
        self.soft =dict['soft']

    def run(self):

        cut_size = 512

        sess = Session()
        with gfile.FastGFile(self.pb_file_path , 'rb') as f:
            graph_def = GraphDef()
            graph_def.ParseFromString(f.read())

            sess.graph.as_default()

            import_graph_def(graph_def, name='')


            in_image = sess.graph.get_tensor_by_name('in_image:0')
            out_image = sess.graph.get_tensor_by_name('output:0')



            print('开始混合'  "")


            origin_x = self.normal.shape[0]
            origin_y = self.normal.shape[1]
            img = np.zeros(dtype=np.float32, shape=[origin_x, origin_y, 6])
            img[..., 0:3] = self.normal
            img[..., 3:6] = self.soft
            input_full = img

            num_x = math.ceil(img.shape[0] / cut_size)
            num_y = math.ceil(img.shape[1] / cut_size)

            input_cut = np.zeros(dtype=np.float32, shape=[1, cut_size, cut_size, 6])

            output = np.zeros(dtype=np.float32, shape=[1, num_x * cut_size, num_y * cut_size, 3])

            imgtmp = np.zeros(dtype=np.float32, shape=[num_x * cut_size, num_y * cut_size, 6])
            imgtmp[0:img.shape[0], 0:img.shape[1], :] = input_full

            for i in range(num_x):
                for j in range(num_y):
                    input_cut[0, ...] = imgtmp[i * cut_size:(i + 1) * cut_size, j * cut_size:(j + 1) * cut_size, :]

                    output[0, i * cut_size:(i + 1) * cut_size, j * cut_size:(j + 1) * cut_size, :] = sess.run(out_image, feed_dict={in_image: input_cut})

            # output = sess.run(out_image, feed_dict={in_image: input_full})
            # output = np.minimum(np.maximum(output, 0), 1)

        output = output[0, 0:img.shape[0], 0:img.shape[1], :]

        # toc = time.perf_counter()
        # print('Finish, time: {:.2f}'.format(toc - tic))

        self.output =   np.minimum(np.maximum(output, 0), 1)

    def get_result(self):
        Thread.join(self)  # 等待线程执行完毕
        try:
            return self.output
        except Exception:
            return None



class restore_mult_model(Thread):

    def __init__(self,dict):
        Thread.__init__(self)
        self.dict = dict
        self.raw_file =dict['fileName']
        self.light =dict['light']
        self.rate = dict['rate']
        self.gamma =dict['gamma']
        self.blue_gain = dict['blue_gain']
        self.green_gain = dict['green_gain']

        self.output_path = dict['output_path']

        self.type = dict['type']




    def run(self):

        tick1 = time.time()

        name = self.raw_file.split('/')[-1].split('.')[0]


        self.dict['pb_path'] = pb_path_normal
        th1 = restore_mode_pb_single(self.dict)
        th1.start()
        th1.join()
        output_normal = th1.get_result()
        th1.join()
        output_normal_uint8 = (output_normal * 255).astype(np.uint8)
        im = Image.fromarray(output_normal_uint8, 'RGB')
        if self.output_path !='':
            im.save(self.output_path+'/'+name +"_denoise.png")
        else:
            im.save('./output/' + name  + "_denoise.png")


        if self.type>1:
            self.dict['pb_path'] = pb_path_soft
            th2 = restore_mode_pb_single(self.dict)
            th2.start()
            th2.join()
            output_soft = th2.get_result()
            th2.join()
            output_soft_uint8 = (output_soft * 255).astype(np.uint8)
            im = Image.fromarray(output_soft_uint8, 'RGB')
            if self.output_path !='':
                im.save(self.output_path+'/'+name +"_highlight.png")
            else:
                im.save('./output/' + name  + "_highlight.png")

        if self.type > 2:
            self.dict['pb_path'] = pb_path_mix
            self.dict['normal'] = output_normal
            self.dict['soft'] = output_soft
            th2 = mix(self.dict)
            th2.start()
            th2.join()
            output_soft = th2.get_result()
            th2.join()
            output_soft = (output_soft * 255).astype(np.uint8)
            im = Image.fromarray(output_soft, 'RGB')
            if self.output_path !='':
                im.save(self.output_path+'/'+name +"_mix.png")
            else:
                im.save('./output/' + name  + "_mix.png")

        # name = self.raw_file.split('/')[-1].split('.')[0]
        #
        # output = (self.soft/100)*output_soft + (1- (self.soft+self.sharp)/100)*output_normal +(self.sharp/100)*output_sharp
        # output = (output * 255).astype(np.uint8)
        #
        # im = Image.fromarray(output, 'RGB')
        # imtiff = (output*65535).astype(np.uint16)
        # # im.save('./tmp/' + name + "_v.tif")
        # if self.output_path !='':
        #     im.save(self.output_path+'/'+name + '_'+str(self.soft)+"_denoise.png")
        #     # tiff.imsave('./tmp/' + name + "_denoise.tif", imtiff)
        # else:
        #     im.save('./output/' + name  + '_'+str(self.soft)+"_denoise.png")
        #     # tiff.imsave('./tmp/' + name + "_denoise.tif", imtiff)
        tick2 = time.time()
        print('用时：' + str(round(tick2 - tick1, 2)) + '秒')
        print('完成：'+name + "_denoise.png")