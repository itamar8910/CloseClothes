# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import tensorflow as tf
import tiny_faces.tiny_face_model as tiny_face_model
import tiny_faces.util as util
from argparse import ArgumentParser
import cv2
import scipy.io
import numpy as np
import cv2
import pickle

import time
import os
import sys
from scipy.special import expit
import glob

MAX_INPUT_DIM = 5000.0
weight_file_path = 'tiny_faces/models/hr_res101_pickle3.p'

# print("loading tiny faces model")
# Create the tiny face model which weights are loaded from a pretrained model.
model = tiny_face_model.Model(weight_file_path)
# print("finished loading tiny faces model")

# placeholder of input images. Currently batch size of one is supported.
x = tf.placeholder(tf.float32, [1, None, None, 3])  # n, h, w, c

score_final = model.tiny_face(x)

# Load an average image and clusters(reference boxes of templates).
average_image = model.get_data_by_key("average_image")
clusters = model.get_data_by_key("clusters")

def standard_bboxes(bboxes):
    """return (x1,y1) (x2,y2) instead of (x1,y1,x2,y2,confidence)"""
    return [(bbox[:2], bbox[2:-1]) for bbox in bboxes]

def get_faces_from_file(img_path: str, prob_thresh=0.5, nms_thresh=0.1, lw=3, display=False):
    return get_faces(read_image(img_path), prob_thresh=0.5, nms_thresh=0.1, lw=3, display=False)

def get_faces(raw_img, prob_thresh=0.5, nms_thresh=0.1, lw=3, display=False):
    return standard_bboxes(_raw_get_faces(raw_img, prob_thresh, nms_thresh, lw, display))

def _raw_get_faces(raw_img, prob_thresh=0.5, nms_thresh=0.1, lw=3, display=False):
    """
    Detect faces in images.
    """




    clusters_h = clusters[:, 3] - clusters[:, 1] + 1
    clusters_w = clusters[:, 2] - clusters[:, 0] + 1
    normal_idx = np.where(clusters[:, 4] == 1)

    # main
    with tf.Session() as sess:
        sess.run(tf.global_variables_initializer())

        raw_img = cv2.cvtColor(raw_img, cv2.COLOR_BGR2RGB)
        raw_img_f = raw_img.astype(np.float32)

        scales = np.array([2.0], dtype=np.float32)
        start = time.time()

        # initialize output
        bboxes = np.empty(shape=(0, 5))

        # process input at different scales
        for s in scales:
            # print("Processing {} at scale {:.4f}".format(fname, s))
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

        # print("time {:.2f} secs for {}".format(time.time() - start, fname))

        # non maximum suppression
        # refind_idx = util.nms(bboxes, nms_thresh)
        refind_idx = tf.image.non_max_suppression(tf.convert_to_tensor(bboxes[:, :4], dtype=tf.float32),
                                                  tf.convert_to_tensor(bboxes[:, 4], dtype=tf.float32),
                                                  max_output_size=bboxes.shape[0], iou_threshold=nms_thresh)
        refind_idx = sess.run(refind_idx)
        refined_bboxes = bboxes[refind_idx]
        return refined_bboxes


def overlay_bounding_boxes(raw_img, refined_bboxes, lw):
    """Overlay bounding boxes of face on images.
    Args:
        raw_img:
        A target image.
        refined_bboxes:
        Bounding boxes of detected faces.
        lw: 
        Line width of bounding boxes. If zero specified,
        this is determined based on confidence of each detection.
    Returns:
        None.
    """

    # Overlay bounding boxes on an image with the color based on the confidence.
    for r in refined_bboxes:
        # print(r)
        # print(type(r))
        # print(type(r[0]))
        # exit()
        cv2.rectangle(raw_img, (int(r[0][0]), int(r[0][1])), (int(r[1][0]), int(r[1][1])), (255, 255, 255), 1)
    cv2.imshow('img', raw_img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

import imageio
def read_image(img_path):
    return imageio.imread(img_path)
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

def show_for_img(imgpath):
    img = read_image(imgpath)
    t1 = time.time()
    faces = get_faces(img)
    print('comp time:', time.time() - t1)
    print('faces:', faces)
    overlay_bounding_boxes(img, faces, 0)

if __name__ == "__main__":
    imgpath = 'tmp.png'
    img = read_image(imgpath)
    faces = get_faces(img)
    overlay_bounding_boxes(img, faces)