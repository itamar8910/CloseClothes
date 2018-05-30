# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import numpy as np
import scipy.io as sio
import os
import pickle
from argparse import ArgumentParser


def parse_args():
    argparse = ArgumentParser()
    argparse.add_argument('--matlab_model_path', type=str, help='Matlab pretrained model.',
                          default='/path/to/hr_res101.mat')
    argparse.add_argument('--weight_file_path', type=str, help='Weight file for Tensorflow.',
                          default='/path/to/mat2tf.pkl')

    args = argparse.parse_args()
    return args.matlab_model_path, args.pickle_model_path

# check arguments

def pickle_model(matlab_model_path):
    assert os.path.exists(matlab_model_path), \
        "Matlab pretrained model: " + matlab_model_path + " not found."

    mat_params_dict = {}
    mat_blocks_dict = {}

    f = sio.loadmat(matlab_model_path)
    net = f['net']
    clusters = np.copy(net['meta'][0][0][0][0][6])
    average_image = np.copy(net['meta'][0][0][0][0][2][0][0][2])[:, 0]
    mat_params_dict["clusters"] = clusters
    mat_params_dict["average_image"] = average_image

    layers = net['layers'][0][0][0]
    mat_params = net['params'][0][0][0]
    for p in mat_params:
        mat_params_dict[p[0][0]] = p[1]

    for k, layer in enumerate(layers):
        type_string = ''
        param_string = ''

        layer_name, layer_type = layer[0][0], layer[1][0]
        layer_inputs = []
        layer_outputs = []
        layer_params = []

        layer_inputs_count = layer[2][0].shape[0]
        for i in range(layer_inputs_count):
            layer_inputs.append(layer[2][0][i][0])

        layer_outputs_count = layer[3][0].shape[0]
        for i in range(layer_outputs_count):
            layer_outputs.append(layer[3][0][i][0])

        if layer[4].shape[0] > 0:
            layer_params_count = layer[4][0].shape[0]
            for i in range(layer_params_count):
                layer_params.append(layer[4][0][i][0])

        mat_blocks_dict[layer_name + '_type'] = layer_type
        mat_params_dict[layer_name + '_type'] = layer_type
        if layer_type == u'dagnn.Conv':
            nchw = layer[5][0][0][0][0]
            has_bias = layer[5][0][0][1][0][0]
            pad = layer[5][0][0][3][0]
            stride = layer[5][0][0][4][0]
            dilate = layer[5][0][0][5][0]
            mat_blocks_dict[layer_name + '_nchw'] = nchw
            mat_blocks_dict[layer_name + '_has_bias'] = has_bias
            mat_blocks_dict[layer_name + '_pad'] = pad
            mat_blocks_dict[layer_name + '_stride'] = stride
            mat_blocks_dict[layer_name + '_dilate'] = dilate
            if has_bias:
                bias = mat_params_dict[layer_name + '_bias'][0] # (1, N) -> (N,)
                mat_params_dict[layer_name + '_bias'] = bias
        elif layer_type == u'dagnn.BatchNorm':
            epsilon = layer[5][0][0][1][0][0]
            gamma = mat_params_dict[layer_name + '_mult'][:, 0] # (N, 1) -> (N,)
            beta = mat_params_dict[layer_name + '_bias'][:, 0] # (N, 1) -> (N,)
            moments = mat_params_dict[layer_name + '_moments'] # (N, 2) -> (N,), (N,)
            moving_mean = moments[:, 0]
            moving_var = moments[:, 1] * moments[:, 1] - epsilon

            mat_blocks_dict[layer_name + '_variance_epsilon'] = epsilon
            mat_params_dict[layer_name + '_scale'] = gamma
            mat_params_dict[layer_name + '_offset'] = beta
            mat_params_dict[layer_name + '_mean'] = moving_mean
            mat_params_dict[layer_name + '_variance'] = moving_var
        elif layer_type == u'dagnn.ConvTranspose':
            nchw = layer[5][0][0][0][0]
            has_bias = layer[5][0][0][1][0][0]
            upsample = layer[5][0][0][2][0]
            crop = layer[5][0][0][3][0]
            mat_blocks_dict[layer_name + '_nchw'] = nchw
            mat_blocks_dict[layer_name + '_has_bias'] = has_bias
            mat_blocks_dict[layer_name + '_upsample'] = upsample
            mat_blocks_dict[layer_name + '_crop'] = crop
            wmat = mat_params_dict[layer_name + 'f']
            mat_params_dict[layer_name + '_filter'] = wmat
        elif layer_type == u'dagnn.Pooling':
            method = layer[5][0][0][0][0]
            pool_size = layer[5][0][0][1][0]
            pad = layer[5][0][0][3][0]
            stride = layer[5][0][0][4][0]
            mat_blocks_dict[layer_name + '_method'] = method
            mat_blocks_dict[layer_name + '_pool_size'] = pool_size
            mat_blocks_dict[layer_name + '_pad'] = pad
            mat_blocks_dict[layer_name + '_stride'] = stride
        elif layer_type == u'dagnn.ReLU':
            pass
        elif layer_type == u'dagnn.Sum':
            pass
        else:
            pass
    return mat_blocks_dict, mat_params_dict


def save_pickle(pickle_path, pickle_model):
    try:
        os.makedirs(os.path.dirname(pickle_path))
    except:
        pass
    with open(pickle_path, 'wb') as f:
        pickle.dump(pickle_model, f, pickle.HIGHEST_PROTOCOL)
def convert_and_save_pickle_model(matlab_path,pickle_path):
    save_pickle(pickle_path, pickle_model(matlab_path))

if __name__ == '__main__':
    mat_path, pickle_path = parse_args()
    convert_and_save_pickle(pickle_path, mat_path)
