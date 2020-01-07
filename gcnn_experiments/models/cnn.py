import tensorflow as tf


VALID='VALID'


default_filter_size = 3
n_filters = 10
stride = 1
pool_stride = 2

def build_layer(filter_depth, layer_order, previous_layer, filter_size=default_filter_size,  weight_size=n_filters,  activation='relu'):
    weights = tf.get_variable('weights-conv'+str(layer_order), [filter_size,filter_size, filter_depth, weight_size])
    biases = tf.get_variable('biases-conv'+str(layer_order), [weight_size])
    output = tf.nn.conv2d(previous_layer, weights, strides=[1, 1, 1, 1], padding=VALID, use_cudnn_on_gpu=True, data_format='NHWC')
    output = tf.nn.bias_add(output, biases)
    if filter_size != 4:
        output = tf.layers.batch_normalization(output)
        output = tf.nn.relu(output)

    return output

def get_model(x,x_depth, y_size):
    l1 = build_layer(x_depth,1,x)
    l2 = build_layer(l1.shape[-1],2,l1)
    l2 = tf.nn.max_pool(l2, [1, pool_stride, pool_stride, 1],
                                [1, pool_stride, pool_stride, 1], padding='VALID')

    l3 = build_layer(l2.shape[-1],3,l2)
    l4 = build_layer(l3.shape[-1],4,l3)
    l5 = build_layer(l4.shape[-1],5,l4)
    l6 = build_layer(l5.shape[-1],6,l5)
    l7 = build_layer(l6.shape[-1], 7, l6, 4)
    images_flat = tf.contrib.layers.flatten(l7)
    l7 = tf.contrib.layers.fully_connected(images_flat, y_size, tf.nn.softmax)
    return l7


