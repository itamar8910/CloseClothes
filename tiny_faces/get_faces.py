# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import tensorflow as tf
import Tiny_Faces_in_Tensorflow.tiny_face_model as tiny_face_model
import Tiny_Faces_in_Tensorflow.util as util
from argparse import ArgumentParser
import cv2
import scipy.io
import numpy as np
import matplotlib.pyplot as plt
import cv2
import pickle

import pylab as pl
import time
import os
import sys
from scipy.special import expit
import glob

MAX_INPUT_DIM = 5000.0
weight_file_path = 'Tiny_Faces_in_Tensorflow/models/hr_res101_pickle3.p'

print("loading tiny faces model")
# Create the tiny face model which weights are loaded from a pretrained model.
model = tiny_face_model.Model(weight_file_path)
print("finished loading tiny faces model")

# placeholder of input images. Currently batch size of one is supported.
x = tf.placeholder(tf.float32, [1, None, None, 3])  # n, h, w, c

score_final = model.tiny_face(x)

# Load an average image and clusters(reference boxes of templates).
with open(weight_file_path, "rb") as f:
    _, mat_params_dict = pickle.load(f)
average_image = model.get_data_by_key("average_image")
clusters = model.get_data_by_key("clusters")

def get_faces(img_path, prob_thresh=0.5, nms_thresh=0.1, lw=3, display=False):
    """
    Detect faces in images.
    """




    clusters_h = clusters[:, 3] - clusters[:, 1] + 1
    clusters_w = clusters[:, 2] - clusters[:, 0] + 1
    normal_idx = np.where(clusters[:, 4] == 1)

    # main
    with tf.Session() as sess:
        sess.run(tf.global_variables_initializer())

        fname = img_path.split(os.sep)[-1]
        raw_img = cv2.imread(img_path)
        raw_img = cv2.cvtColor(raw_img, cv2.COLOR_BGR2RGB)
        raw_img_f = raw_img.astype(np.float32)

        def _calc_scales():
            raw_h, raw_w = raw_img.shape[0], raw_img.shape[1]
            min_scale = min(np.floor(np.log2(np.max(clusters_w[normal_idx] / raw_w))),
                            np.floor(np.log2(np.max(clusters_h[normal_idx] / raw_h))))
            max_scale = min(1.0, -np.log2(max(raw_h, raw_w) / MAX_INPUT_DIM))
            scales_down = pl.frange(min_scale, 0, 1.)
            scales_up = pl.frange(0.5, max_scale, 0.5)
            scales_pow = np.hstack((scales_down, scales_up))
            scales = np.power(2.0, scales_pow)
            return scales

        # scales = _calc_scales()
        scales = np.array([2.0], dtype=np.float32)
        start = time.time()

        # initialize output
        bboxes = np.empty(shape=(0, 5))

        # process input at different scales
        for s in scales:
            print("Processing {} at scale {:.4f}".format(fname, s))
            img = cv2.resize(raw_img_f, (0, 0), fx=s, fy=s, interpolation=cv2.INTER_LINEAR)
            img = img - average_image
            img = img[np.newaxis, :]

            # we don't run every template on every scale ids of templates to ignore
            tids = list(range(4, 12)) + ([] if s <= 1.0 else list(range(18, 25)))
            ignoredTids = list(set(range(0, clusters.shape[0])) - set(tids))

            # run through the net
            score_final_tf = sess.run(score_final, feed_dict={x: img})

            # collect scores
            score_cls_tf, score_reg_tf = score_final_tf[:, :, :, :25], score_final_tf[:, :, :, 25:125]
            prob_cls_tf = expit(score_cls_tf)
            prob_cls_tf[0, :, :, ignoredTids] = 0.0

            def _calc_bounding_boxes():
                # threshold for detection
                _, fy, fx, fc = np.where(prob_cls_tf > prob_thresh)

                # interpret heatmap into bounding boxes
                cy = fy * 8 - 1
                cx = fx * 8 - 1
                ch = clusters[fc, 3] - clusters[fc, 1] + 1
                cw = clusters[fc, 2] - clusters[fc, 0] + 1

                # extract bounding box refinement
                Nt = clusters.shape[0]
                tx = score_reg_tf[0, :, :, 0:Nt]
                ty = score_reg_tf[0, :, :, Nt:2 * Nt]
                tw = score_reg_tf[0, :, :, 2 * Nt:3 * Nt]
                th = score_reg_tf[0, :, :, 3 * Nt:4 * Nt]

                # refine bounding boxes
                dcx = cw * tx[fy, fx, fc]
                dcy = ch * ty[fy, fx, fc]
                rcx = cx + dcx
                rcy = cy + dcy
                rcw = cw * np.exp(tw[fy, fx, fc])
                rch = ch * np.exp(th[fy, fx, fc])

                scores = score_cls_tf[0, fy, fx, fc]
                tmp_bboxes = np.vstack((rcx - rcw / 2, rcy - rch / 2, rcx + rcw / 2, rcy + rch / 2))
                tmp_bboxes = np.vstack((tmp_bboxes / s, scores))
                tmp_bboxes = tmp_bboxes.transpose()
                return tmp_bboxes

            tmp_bboxes = _calc_bounding_boxes()
            bboxes = np.vstack((bboxes, tmp_bboxes))  # <class 'tuple'>: (5265, 5)

        print("time {:.2f} secs for {}".format(time.time() - start, fname))

        # non maximum suppression
        # refind_idx = util.nms(bboxes, nms_thresh)
        refind_idx = tf.image.non_max_suppression(tf.convert_to_tensor(bboxes[:, :4], dtype=tf.float32),
                                                  tf.convert_to_tensor(bboxes[:, 4], dtype=tf.float32),
                                                  max_output_size=bboxes.shape[0], iou_threshold=nms_thresh)
        refind_idx = sess.run(refind_idx)
        refined_bboxes = bboxes[refind_idx]
        return refined_bboxes
        # overlay_bounding_boxes(raw_img, refined_bboxes, lw)
        #
        # if display:
        #     # plt.axis('off')
        #     plt.imshow(raw_img)
        #     plt.show()
        #
        # # save image with bounding boxes
        # raw_img = cv2.cvtColor(raw_img, cv2.COLOR_RGB2BGR)
        # cv2.imwrite(os.path.join(output_dir, fname), raw_img)

#
# def main():
#     argparse = ArgumentParser()
#     argparse.add_argument('--weight_file_path', type=str, help='Pretrained weight file.', default="/path/to/mat2tf.pkl")
#     argparse.add_argument('--data_dir', type=str, help='Image data directory.',
#                           default="/path/to/input_image_directory")
#     argparse.add_argument('--output_dir', type=str, help='Output directory for images with faces detected.',
#                           default="/path/to/output_directory")
#     argparse.add_argument('--prob_thresh', type=float, help='The threshold of detection confidence(default: 0.5).',
#                           default=0.5)
#     argparse.add_argument('--nms_thresh', type=float,
#                           help='The overlap threshold of non maximum suppression(default: 0.1).', default=0.1)
#     argparse.add_argument('--line_width', type=int, help='Line width of bounding boxes(0: auto).', default=3)
#     argparse.add_argument('--display', type=bool, help='Display each image on window.', default=False)
#
#     args = argparse.parse_args()
#
#     # check arguments
#     assert os.path.exists(args.weight_file_path), "weight file: " + args.weight_file_path + " not found."
#     assert os.path.exists(args.data_dir), "data directory: " + args.data_dir + " not found."
#     assert os.path.exists(args.output_dir), "output directory: " + args.output_dir + " not found."
#     assert args.line_width >= 0, "line_width should be >= 0."
#
#     with tf.Graph().as_default():
#         evaluate(
#             weight_file_path=args.weight_file_path, data_dir=args.data_dir, output_dir=args.output_dir,
#             prob_thresh=args.prob_thresh, nms_thresh=args.nms_thresh,
#             lw=args.line_width, display=args.display)
#
#
# if __name__ == '__main__':
#     main()
