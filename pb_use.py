import tensorflow as tf
from tensorflow.python.platform import gfile
import numpy as np
import rawpy
import glob
import scipy.io
import time
from PIL import Image
import white_balance

pb_path = './pb_model/frozen_model.pb'

raw_path = 'G:/dng/8/'
raw_path = './test/'

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


def restore_mode_pb(pb_file_path ,raw_path):


    sess = tf.Session()
    with gfile.FastGFile(pb_file_path, 'rb') as f:
        graph_def = tf.GraphDef()
        graph_def.ParseFromString(f.read())
        sess.graph.as_default()
        tf.import_graph_def(graph_def, name='')

        in_image = sess.graph.get_tensor_by_name('in_image:0')
        out_image = sess.graph.get_tensor_by_name('output:0')

        # in_image = tf.placeholder(tf.float32, [None, None, None, 4], name='in_image')
        # out_image = tf.placeholder(tf.float32, [None, None, None, 3])

        raw_list = glob.glob(raw_path + '*.rw2')

        for ind in raw_list:
            raw = rawpy.imread(ind)


            wb ,black ,raw_pattern = white_balance.get_camera_wb(ind)
            raw_pattern= str(raw_pattern).replace('\n', '').replace('\r', '')

            black = black[0]
            input_full = np.expand_dims(pack_raw(raw,raw_pattern ,black  ), axis=0)
            input_full = np.minimum(input_full, 1.0)

            output = sess.run(out_image, feed_dict={in_image: input_full})
            output = np.minimum(np.maximum(output, 0), 1)

            output = output[0, :, :, :]
            # 白平衡矫正
            b = output[:, :, np.newaxis, :]
            b = np.matmul(b, wb)
            c = np.squeeze(b)
            c = np.minimum(np.maximum(c, 0), 1)
            output = (c * 255).astype(np.uint8)
            # scipy.misc.toimage(output * 255, high=255, low=0, cmin=0, cmax=255).save(
            #       ind + '_429out.png')

            im = Image.fromarray(output,'RGB' )
            im.save("your_file.png")


# light  亮度放大
# rate   亮度前后级比例
# gamma  暗部放大

def restore_mode_pb_single(pb_file_path ,raw_file ,output_path ,light,rate,gamma):
#
    sess = tf.Session()
    with gfile.FastGFile(pb_file_path, 'rb') as f:
        graph_def = tf.GraphDef()
        graph_def.ParseFromString(f.read())
        sess.graph.as_default()
        tf.import_graph_def(graph_def, name='')

        in_image = sess.graph.get_tensor_by_name('in_image:0')
        out_image = sess.graph.get_tensor_by_name('output:0')

        name = raw_file.split('/')[-1].split('.')[0]


        print('开始降噪：' + name + "")
        # 计算放大
        # 按照10分 放大比例
        before_amp = 2** (light*(5-rate)/10)
        after_amp = 2** (light*(5+rate)/10)

        tick1 = time.time()
        raw = rawpy.imread(raw_file)

        wb, black, raw_pattern = white_balance.get_camera_wb(raw_file)
        raw_pattern = str(raw_pattern).replace('\n', '').replace('\r', '')

        black = black[0]
        input_full = np.expand_dims(pack_raw(raw, raw_pattern, black), axis=0)*before_amp
        input_full = np.minimum(input_full, 1.0)

        # 暗部处理
        input_full = np.power(input_full, 1 / (1+gamma))

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

        if output_path !='':

            im.save(output_path+'/'+name + "_denoise.png")
        else:
            im.save('./output/' + name + "_denoise.png")


        tick2 = time.time()

        print('用时：' + str(round(tick2 - tick1, 2)) + '秒')
        print('完成：'+name + "_denoise.png")


if __name__ == '__main__':

    restore_mode_pb(pb_path,raw_path)