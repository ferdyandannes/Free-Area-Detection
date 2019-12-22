import sys
ros_path = '/opt/ros/kinetic/lib/python2.7/dist-packages'
if ros_path in sys.path:
    sys.path.remove(ros_path)
import cv2

import h5py
import numpy as np
import os
import copy
import operator

from collections import defaultdict
from statistics import mean

def get_transform_matrix(src, dst):
    # Get the transform matrix by OpenCV function. 
    # src : Coordinates of quadrangle vertices in the source image.
    # dst : Coordinates of the corresponding quadrangle vertices in the destination image.
    # return : Transform matrix
    M = cv2.getPerspectiveTransform(src, dst)
    return M

def read(filename):
    f = h5py.File(filename, 'r')
    object_id = f['object_id'].value
    #ego_motion = f['ego_motion'].value
    x=[]
    y=[]
    for i in object_id:
        x.append(f[str(i)].value[0])
        y.append(f[str(i)].value[1])
    return object_id, x,y

def check_dir(dir_list):
    for d in dir_list:
        if not os.path.isdir(d):
            print('Create directory :\n' + d)
            os.makedirs(d)

def remove_values_from_list(the_list, val):
   return [value for value in the_list if value != val]

def check_posisi(cX, cY, check_pos, batas):
    we, ha = check_pos.shape

    if ha == 4:
        if 0 < cX < batas[0] and 0 < cY < 100:
            check_pos[0, 0] = 1
        elif batas[0] < cX < batas[1] and 0 < cY < 100:
            check_pos[0, 1] = 1
        elif batas[1] < cX < batas[2] and 0 < cY < 100:
            check_pos[0, 2] = 1
        elif batas[2] < cX < 175 and 0 < cY < 100:
            check_pos[0, 3] = 1

        if 0 < cX < batas[0] and 100 < cY < 200:
            check_pos[1, 0] = 1
        elif batas[0] < cX < batas[1] and 100 < cY < 200:
            check_pos[1, 1] = 1
        elif batas[1] < cX < batas[2] and 100 < cY < 200:
            check_pos[1, 2] = 1
        elif batas[2] < cX < 175 and 100 < cY < 200:
            check_pos[1, 3] = 1

        if 0 < cX < batas[0] and 200 < cY < 300:
            check_pos[2, 0] = 1
        elif batas[0] < cX < batas[1] and 200 < cY < 300:
            check_pos[2, 1] = 1
        elif batas[1] < cX < batas[2] and 200 < cY < 300:
            check_pos[2, 2] = 1
        elif batas[2] < cX < 175 and 200 < cY < 300:
            check_pos[2, 3] = 1

        if 0 < cX < batas[0] and 300 < cY < 400:
            check_pos[3, 0] = 1
        elif batas[0] < cX < batas[1] and 300 < cY < 400:
            check_pos[3, 1] = 1
        elif batas[1] < cX < batas[2] and 300 < cY < 400:
            check_pos[3, 2] = 1
        elif batas[2] < cX < 175 and 300 < cY < 400:
            check_pos[3, 3] = 1

        if 0 < cX < batas[0] and 400 < cY < 500:
            check_pos[4, 0] = 1
        elif batas[0] < cX < batas[1] and 400 < cY < 500:
            check_pos[4, 1] = 1
        elif batas[1] < cX < batas[2] and 400 < cY < 500:
            check_pos[4, 2] = 1
        elif batas[2] < cX < 175 and 400 < cY < 500:
            check_pos[4, 3] = 1

        if 0 < cX < batas[0] and 500 < cY < 600:
            check_pos[5, 0] = 1
        elif batas[0] < cX < batas[1] and 500 < cY < 600:
            check_pos[5, 1] = 1
        elif batas[1] < cX < batas[2] and 500 < cY < 600:
            check_pos[5, 2] = 1
        elif batas[2] < cX < 175 and 500 < cY < 600:
            check_pos[5, 3] = 1
    elif ha == 5:
        if 0 < cX < batas[0] and 0 < cY < 100:
            check_pos[0, 0] = 1
        elif batas[0] < cX < batas[1] and 0 < cY < 100:
            check_pos[0, 1] = 1
        elif batas[1] < cX < batas[2] and 0 < cY < 100:
            check_pos[0, 2] = 1
        elif batas[2] < cX < batas[3] and 0 < cY < 100:
            check_pos[0, 3] = 1
        elif batas[3] < cX < 175 and 0 < cY < 100:
            check_pos[0, 4] = 1

        if 0 < cX < batas[0] and 100 < cY < 200:
            check_pos[1, 0] = 1
        elif batas[0] < cX < batas[1] and 100 < cY < 200:
            check_pos[1, 1] = 1
        elif batas[1] < cX < batas[2] and 100 < cY < 200:
            check_pos[1, 2] = 1
        elif batas[2] < cX < batas[3] and 100 < cY < 200:
            check_pos[1, 3] = 1
        elif batas[3] < cX < 175 and 100 < cY < 200:
            check_pos[1, 4] = 1

        if 0 < cX < batas[0] and 200 < cY < 300:
            check_pos[2, 0] = 1
        elif batas[0] < cX < batas[1] and 200 < cY < 300:
            check_pos[2, 1] = 1
        elif batas[1] < cX < batas[2] and 200 < cY < 300:
            check_pos[2, 2] = 1
        elif batas[2] < cX < batas[3] and 200 < cY < 300:
            check_pos[2, 3] = 1
        elif batas[3] < cX < 175 and 200 < cY < 300:
            check_pos[2, 4] = 1

        if 0 < cX < batas[0] and 300 < cY < 400:
            check_pos[3, 0] = 1
        elif batas[0] < cX < batas[1] and 300 < cY < 400:
            check_pos[3, 1] = 1
        elif batas[1] < cX < batas[2] and 300 < cY < 400:
            check_pos[3, 2] = 1
        elif batas[2] < cX < batas[3] and 300 < cY < 400:
            check_pos[3, 3] = 1
        elif batas[3] < cX < 175 and 300 < cY < 400:
            check_pos[3, 4] = 1

        if 0 < cX < batas[0] and 400 < cY < 500:
            check_pos[4, 0] = 1
        elif batas[0] < cX < batas[1] and 400 < cY < 500:
            check_pos[4, 1] = 1
        elif batas[1] < cX < batas[2] and 400 < cY < 500:
            check_pos[4, 2] = 1
        elif batas[2] < cX < batas[3] and 400 < cY < 500:
            check_pos[4, 3] = 1
        elif batas[3] < cX < 175 and 400 < cY < 500:
            check_pos[4, 4] = 1

        if 0 < cX < batas[0] and 500 < cY < 600:
            check_pos[5, 0] = 1
        elif batas[0] < cX < batas[1] and 500 < cY < 600:
            check_pos[5, 1] = 1
        elif batas[1] < cX < batas[2] and 500 < cY < 600:
            check_pos[5, 2] = 1
        elif batas[2] < cX < batas[3] and 500 < cY < 600:
            check_pos[5, 3] = 1
        elif batas[3] < cX < 175 and 500 < cY < 600:
            check_pos[5, 4] = 1
    elif ha == 6:
        if 0 < cX < batas[0] and 0 < cY < 100:
            check_pos[0, 0] = 1
        elif batas[0] < cX < batas[1] and 0 < cY < 100:
            check_pos[0, 1] = 1
        elif batas[1] < cX < batas[2] and 0 < cY < 100:
            check_pos[0, 2] = 1
        elif batas[2] < cX < batas[3] and 0 < cY < 100:
            check_pos[0, 3] = 1
        elif batas[3] < cX < batas[4] and 0 < cY < 100:
            check_pos[0, 4] = 1
        elif batas[4] < cX < 175 and 0 < cY < 100:
            check_pos[0, 5] = 1

        if 0 < cX < batas[0] and 100 < cY < 200:
            check_pos[1, 0] = 1
        elif batas[0] < cX < batas[1] and 100 < cY < 200:
            check_pos[1, 1] = 1
        elif batas[1] < cX < batas[2] and 100 < cY < 200:
            check_pos[1, 2] = 1
        elif batas[2] < cX < batas[3] and 100 < cY < 200:
            check_pos[1, 3] = 1
        elif batas[3] < cX < batas[4] and 100 < cY < 200:
            check_pos[1, 4] = 1
        elif batas[4] < cX < 175 and 100 < cY < 200:
            check_pos[1, 5] = 1

        if 0 < cX < batas[0] and 200 < cY < 300:
            check_pos[2, 0] = 1
        elif batas[0] < cX < batas[1] and 200 < cY < 300:
            check_pos[2, 1] = 1
        elif batas[1] < cX < batas[2] and 200 < cY < 300:
            check_pos[2, 2] = 1
        elif batas[2] < cX < batas[3] and 200 < cY < 300:
            check_pos[2, 3] = 1
        elif batas[3] < cX < batas[4] and 200 < cY < 300:
            check_pos[2, 4] = 1
        elif batas[4] < cX < 175 and 200 < cY < 300:
            check_pos[2, 5] = 1

        if 0 < cX < batas[0] and 300 < cY < 400:
            check_pos[3, 0] = 1
        elif batas[0] < cX < batas[1] and 300 < cY < 400:
            check_pos[3, 1] = 1
        elif batas[1] < cX < batas[2] and 300 < cY < 400:
            check_pos[3, 2] = 1
        elif batas[2] < cX < batas[3] and 300 < cY < 400:
            check_pos[3, 3] = 1
        elif batas[3] < cX < batas[4] and 300 < cY < 400:
            check_pos[3, 4] = 1
        elif batas[4] < cX < 175 and 300 < cY < 400:
            check_pos[3, 5] = 1

        if 0 < cX < batas[0] and 400 < cY < 500:
            check_pos[4, 0] = 1
        elif batas[0] < cX < batas[1] and 400 < cY < 500:
            check_pos[4, 1] = 1
        elif batas[1] < cX < batas[2] and 400 < cY < 500:
            check_pos[4, 2] = 1
        elif batas[2] < cX < batas[3] and 400 < cY < 500:
            check_pos[4, 3] = 1
        elif batas[3] < cX < batas[4] and 400 < cY < 500:
            check_pos[4, 4] = 1
        elif batas[4] < cX < 175 and 400 < cY < 500:
            check_pos[4, 5] = 1

        if 0 < cX < batas[0] and 500 < cY < 600:
            check_pos[5, 0] = 1
        elif batas[0] < cX < batas[1] and 500 < cY < 600:
            check_pos[5, 1] = 1
        elif batas[1] < cX < batas[2] and 500 < cY < 600:
            check_pos[5, 2] = 1
        elif batas[2] < cX < batas[3] and 500 < cY < 600:
            check_pos[5, 3] = 1
        elif batas[3] < cX < batas[4] and 500 < cY < 600:
            check_pos[5, 4] = 1
        elif batas[4] < cX < 175 and 500 < cY < 600:
            check_pos[5, 5] = 1
    elif ha == 7:
        if 0 < cX <= batas[0] and 0 < cY < 100:
            check_pos[0, 0] = 1
        elif batas[0] < cX <= batas[1] and 0 < cY < 100:
            check_pos[0, 1] = 1
        elif batas[1] < cX <= batas[2] and 0 < cY < 100:
            check_pos[0, 2] = 1
        elif batas[2] < cX <= batas[3] and 0 < cY < 100:
            check_pos[0, 3] = 1
        elif batas[3] < cX <= batas[4] and 0 < cY < 100:
            check_pos[0, 4] = 1
        elif batas[4] < cX <= batas[5] and 0 < cY < 100:
            check_pos[0, 5] = 1
        elif batas[5] < cX <= 175 and 0 < cY < 100:
            check_pos[0, 6] = 1

        if 0 < cX <= batas[0] and 100 < cY < 200:
            check_pos[1, 0] = 1
        elif batas[0] < cX <= batas[1] and 100 < cY < 200:
            check_pos[1, 1] = 1
        elif batas[1] < cX <= batas[2] and 100 < cY < 200:
            check_pos[1, 2] = 1
        elif batas[2] < cX <= batas[3] and 100 < cY < 200:
            check_pos[1, 3] = 1
        elif batas[3] < cX <= batas[4] and 100 < cY < 200:
            check_pos[1, 4] = 1
        elif batas[4] < cX <= batas[5] and 100 < cY < 200:
            check_pos[1, 5] = 1
        elif batas[5] < cX <= 175 and 100 < cY < 200:
            check_pos[1, 6] = 1

        if 0 < cX <= batas[0] and 200 < cY < 300:
            check_pos[2, 0] = 1
        elif batas[0] < cX <= batas[1] and 200 < cY < 300:
            check_pos[2, 1] = 1
        elif batas[1] < cX <= batas[2] and 200 < cY < 300:
            check_pos[2, 2] = 1
        elif batas[2] < cX <= batas[3] and 200 < cY < 300:
            check_pos[2, 3] = 1
        elif batas[3] < cX <= batas[4] and 200 < cY < 300:
            check_pos[2, 4] = 1
        elif batas[4] < cX <= batas[5] and 200 < cY < 300:
            check_pos[2, 5] = 1
        elif batas[5] < cX <= 175 and 200 < cY < 300:
            check_pos[2, 6] = 1

        if 0 < cX <= batas[0] and 300 < cY < 400:
            check_pos[3, 0] = 1
        elif batas[0] < cX <= batas[1] and 300 < cY < 400:
            check_pos[3, 1] = 1
        elif batas[1] < cX <= batas[2] and 300 < cY < 400:
            check_pos[3, 2] = 1
        elif batas[2] < cX <= batas[3] and 300 < cY < 400:
            check_pos[3, 3] = 1
        elif batas[3] < cX <= batas[4] and 300 < cY < 400:
            check_pos[3, 4] = 1
        elif batas[4] < cX <= batas[5] and 300 < cY < 400:
            check_pos[3, 5] = 1
        elif batas[5] < cX <= 175 and 300 < cY < 400:
            check_pos[3, 6] = 1

        if 0 < cX <= batas[0] and 400 < cY < 500:
            check_pos[4, 0] = 1
        elif batas[0] < cX <= batas[1] and 400 < cY < 500:
            check_pos[4, 1] = 1
        elif batas[1] < cX <= batas[2] and 400 < cY < 500:
            check_pos[4, 2] = 1
        elif batas[2] < cX <= batas[3] and 400 < cY < 500:
            check_pos[4, 3] = 1
        elif batas[3] < cX <= batas[4] and 400 < cY < 500:
            check_pos[4, 4] = 1
        elif batas[4] < cX <= batas[5] and 400 < cY < 500:
            check_pos[4, 5] = 1
        elif batas[5] < cX <= 175 and 400 < cY < 500:
            check_pos[4, 6] = 1

        if 0 < cX <= batas[0] and 500 < cY < 600:
            check_pos[5, 0] = 1
        elif batas[0] < cX <= batas[1] and 500 < cY < 600:
            check_pos[5, 1] = 1
        elif batas[1] < cX <= batas[2] and 500 < cY < 600:
            check_pos[5, 2] = 1
        elif batas[2] < cX <= batas[3] and 500 < cY < 600:
            check_pos[5, 3] = 1
        elif batas[3] < cX <= batas[4] and 500 < cY < 600:
            check_pos[5, 4] = 1
        elif batas[4] < cX <= batas[5] and 500 < cY < 600:
            check_pos[5, 5] = 1
        elif batas[5] < cX <= 175 and 500 < cY < 600:
            check_pos[5, 6] = 1
    return check_pos

def area(data_dir):
    image_dir = data_dir+'Images/'
    images = os.listdir(image_dir)
    images.sort()

    info_dir = os.path.join(data_dir, 'Information/')
    info = os.listdir(info_dir)
    info.sort()

    seg_dir = os.path.join(data_dir, 'Lane_Seg/Mask_RCNN_BDD100k_Color/')
    seg = os.listdir(seg_dir)
    seg.sort()

    with h5py.File(data_dir+'parameters.h5','r') as pf:
        src = pf['src'].value
        bird_hight2 = pf['bird_hight'].value
        bird_width2 = pf['bird_width'].value
        bird_channels = pf['bird_channels'].value

    print("bird_hight2 = ", bird_hight2)
    print("bird_width2 = ", bird_width2)
    print("")

    area_dir = data_dir+'Free_Area/'
    rev_dir = data_dir+'Rev_Area/'
    raw_dir = data_dir+'Free_Area_Vis/Free_Area_Raw/'
    vis_dir = data_dir+'Free_Area_Vis/Free_Area_Col/'
    coba_dir = data_dir+'Coba/'
    check_dir([area_dir, raw_dir, vis_dir, rev_dir, coba_dir])

    dst = np.float32([[0, 0], [bird_width2, 0], [0, bird_hight2], [bird_width2, bird_hight2]])
    M = get_transform_matrix(src, dst)

    # Save the possibility
    poss = []
    dic_free = {}

    # Check reverse direction
    object_id_past = []
    x_past = []
    y_past = []
    x_rev = []
    y_rev = []
    rev = np.zeros((bird_hight2,bird_width2,3), np.uint8)
    poss_rev = []
    dic_free_rev = {}
    reverse_id = []

    simpan_reverse = {}

    for frame_id in range(len(images)):
        print("frame_id = ", frame_id)
        imgnum = str(frame_id).zfill(4)
        info_file = h5py.File(os.path.splitext(area_dir+images[frame_id])[0]+'.h5','w')
        rev_file = h5py.File(os.path.splitext(rev_dir+images[frame_id])[0]+'.h5','w')

        coba_file = h5py.File(os.path.splitext(coba_dir+images[frame_id])[0]+'.h5','w')


        # Read RGB Image
        img_path = image_dir+images[frame_id]
        img = cv2.imread(img_path)

        # Create Mask Image
        mask = np.zeros((bird_hight2,bird_width2,3), np.uint8)
        mask_contour = np.zeros((bird_hight2,bird_width2,3), np.uint8)
        mask_driveable = np.zeros((bird_hight2,bird_width2,3), np.uint8)
        mask_calc = np.zeros((bird_hight2,bird_width2,3), np.uint8)
        mask_final = np.zeros((bird_hight2,bird_width2,3), np.uint8)
        viz = np.zeros((bird_hight2,bird_width2,3), np.uint8)
        vizz = np.zeros((bird_hight2,bird_width2,3), np.uint8)
        coba = np.zeros((bird_hight2,bird_width2,3), np.uint8)
        rev2 = np.zeros((bird_hight2,bird_width2,3), np.uint8)

        # Read BEV Position
        info_path = info_dir + info[frame_id]
        object_id, x, y = read(info_path)

        # Warp Perspective
        warped_img = cv2.warpPerspective(img, M, (bird_width2, bird_hight2))

        # Calculate Position in OpenCV Format
        x_now = []
        y_now = []
        object_now = []

        dic_y_set = {}
        dic_x_set = {}
        
        for i in range(len(object_id)):
            pos_x = ((2*x[i]) + bird_width2)/2
            pos_y = bird_hight2 - y[i]
            # print(pos_x, " ", pos_y)
            cv2.circle(warped_img,(int(pos_x), int(pos_y)), 1, (0,255,0), -1)
            cv2.rectangle(mask, (int(pos_x) - 15, int(pos_y) - 80), (int(pos_x) + 15, int(pos_y) + 10), (0,0,255), cv2.FILLED)

            # Check reverse side
            x_now.append(pos_x)
            y_now.append(pos_y)
            object_now.append(object_id[i])

            if object_id[i] in dic_y_set:
                dic_y_set[object_id[i]] = pos_y
            else:
                dic_y_set[object_id[i]] = pos_y

            if object_id[i] in dic_x_set:
                dic_x_set[object_id[i]] = pos_x
            else:
                dic_x_set[object_id[i]] = pos_x

        ######################################################################
        print("x = ", dic_x_set)
        print("y = ", dic_y_set)

        if frame_id > 0:
            # Read the reverse id
            with h5py.File(data_dir+'reverse_id.h5','r') as ri:
                reverse_id = ri['reverse_id'].value

            for i in range(len(reverse_id)):
                id_objek = reverse_id[i]
                print("id_objek = ", id_objek)

                if id_objek in dic_y_set:
                    posisi_y = dic_y_set[id_objek]
                    posisi_x = dic_x_set[id_objek]
                    
                    y_rev.append(posisi_y)
                    x_rev.append(posisi_x)

        print("y_rev = ", y_rev)

        ######################################################################

        object_id_past = object_id
        x_past = x_now
        y_past = y_now
        
        # Divide in SxS Region
        mask2 = copy.copy(mask)

        # X Divide 5
        divx = bird_width2/5
        x0, ex0, y0, ey0 = divx, divx, 0, bird_hight2
        x1, ex1, y1, ey1 = divx+divx, divx+divx, 0, bird_hight2
        x2, ex2, y2, ey2 = divx+divx+divx, divx+divx+divx, 0, bird_hight2
        x3, ex3, y3, ey3 = divx+divx+divx+divx, divx+divx+divx+divx, 0, bird_hight2
        cv2.line(mask2, (int(x0), int(y0)), (int(ex0), int(ey0)), (0,0,255), 3)
        cv2.line(mask2, (int(x1), int(y1)), (int(ex1), int(ey1)), (0,0,255), 3)
        cv2.line(mask2, (int(x2), int(y2)), (int(ex2), int(ey2)), (0,0,255), 3)
        cv2.line(mask2, (int(x3), int(y3)), (int(ex3), int(ey3)), (0,0,255), 3)
        a = x1
        b = y1
        c = ex1
        d = ey1

        # Y
        divy = bird_hight2/8
        x0, ex0, y0, ey0 = 0, bird_hight2, divy, divy
        x1, ex1, y1, ey1 = 0, bird_hight2, divy+divy, divy+divy
        x2, ex2, y2, ey2 = 0, bird_hight2, divy+divy+divy, divy+divy+divy
        x3, ex3, y3, ey3 = 0, bird_hight2, divy+divy+divy+divy, divy+divy+divy+divy
        x4, ex4, y4, ey4 = 0, bird_hight2, divy+divy+divy+divy+divy, divy+divy+divy+divy+divy
        x5, ex5, y5, ey5 = 0, bird_hight2, divy+divy+divy+divy+divy+divy, divy+divy+divy+divy+divy+divy
        x6, ex6, y6, ey6 = 0, bird_hight2, divy+divy+divy+divy+divy+divy+divy, divy+divy+divy+divy+divy+divy+divy

        cv2.line(mask2, (int(x0), int(y0)), (int(ex0), int(ey0)), (0,0,255), 3)
        cv2.line(mask2, (int(x1), int(y1)), (int(ex1), int(ey1)), (0,0,255), 3)
        cv2.line(mask2, (int(x2), int(y2)), (int(ex2), int(ey2)), (0,0,255), 3)
        cv2.line(mask2, (int(x3), int(y3)), (int(ex3), int(ey3)), (0,0,255), 3)
        cv2.line(mask2, (int(x4), int(y4)), (int(ex4), int(ey4)), (0,0,255), 3)
        cv2.line(mask2, (int(x5), int(y5)), (int(ex5), int(ey5)), (0,0,255), 3)
        cv2.line(mask2, (int(x6), int(y6)), (int(ex6), int(ey6)), (0,0,255), 3)


        # Proceed The Mask
        proc_mask2 = cv2.cvtColor(mask2, cv2.COLOR_BGR2GRAY)
        _, proc_mask2 = cv2.threshold(proc_mask2, 30, 255, cv2.THRESH_BINARY_INV)

        # Contours for Divide 5
        _, contours, hier = cv2.findContours(proc_mask2, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        for cnt in contours:
            #print("cnt = ", cv2.contourArea(cnt))
            if 2000<cv2.contourArea(cnt)<2300:
                cv2.drawContours(mask_contour, [cnt], -1, (0,255,0), -1)

        # Combine Close Contour
        mask_contour2 = copy.copy(mask_contour)
        proc_mask_contour2 = cv2.cvtColor(mask_contour2, cv2.COLOR_BGR2GRAY)
        _, proc_mask_contour2 = cv2.threshold(proc_mask_contour2, 30, 255, cv2.THRESH_BINARY)

        kernel = np.ones((5,5),np.uint8)
        proc_mask_contour2 = cv2.dilate(proc_mask_contour2, kernel,iterations = 2)
        proc_mask_contour2 = cv2.cvtColor(proc_mask_contour2, cv2.COLOR_GRAY2BGR)
        mask_final = copy.copy(proc_mask_contour2)

        #################################################################################
        if frame_id == 0:
            # Segmentation   -----> Harusnya sekali aja
            seg_path = seg_dir+seg[frame_id]
            seg_img = cv2.imread(seg_path)

            # warpPerspective
            warped_seg = cv2.warpPerspective(seg_img, M, (bird_width2, bird_hight2))

            # Calculate the area
            warped_seg = cv2.cvtColor(warped_seg, cv2.COLOR_BGR2GRAY)
            _, thres_seg = cv2.threshold(warped_seg, 30, 255, cv2.THRESH_BINARY)

            seg_height, seg_width = thres_seg.shape

            list_colour_point = []

            # Check segmentation in X
            simpan_seg = []
            for x in range(0, seg_width):
                for y in range(0, seg_height):
                    if thres_seg[y][x] == 255:
                        simpan_seg.append(y)

            kiyoshi = mean(simpan_seg)
            print("kiyoshi = ", int(kiyoshi))

            for x in range(0, seg_width):
                if thres_seg[int(kiyoshi)][x] == 255 :    # if thres_seg[600-30][x] == 255 :
                    list_colour_point.append(x)

            seg_max = max(list_colour_point)
            seg_min = min(list_colour_point)
            mid = abs((seg_max+seg_min)/2)
            gap = seg_max - seg_min
            divider = round(bird_width2/gap)
            #print("gap = ", gap)
            #print("divider = ", divider)

        #cv2.imshow("thres_seg", thres_seg)

        print("divider = ", divider)

        batas = []
        if divider == 3:
            range_const = 29
            list_save = 4
            tengah = 2
            x0, ex0, y0, ey0 = mid-29, mid-29, 0, bird_hight2
            x1, ex1, y1, ey1 = mid+29, mid+29, 0, bird_hight2
            x2, ex2, y2, ey2 = mid-29-58, mid-29-58, 0, bird_hight2
            x3, ex3, y3, ey3 = mid+29+58, mid+29+58, 0, bird_hight2
            cv2.line(mask_final, (int(x0), int(y0)), (int(ex0), int(ey0)), (0,0,0), 3)
            cv2.line(mask_final, (int(x1), int(y1)), (int(ex1), int(ey1)), (0,0,0), 3)
            cv2.line(mask_final, (int(x2), int(y2)), (int(ex2), int(ey2)), (0,0,0), 3)
            cv2.line(mask_final, (int(x3), int(y3)), (int(ex3), int(ey3)), (0,0,0), 3)
            low_thres_1 = 2600
            high_thres_1 = 2940
            batas.append(mid-29-58)
            batas.append(mid-29)
            batas.append(mid+29)
            batas.append(mid+29+58)
        elif divider == 4:
            range_const = 22
            list_save = 5
            tengah = 2
            x0, ex0, y0, ey0 = mid-22, mid-22, 0, bird_hight2
            x1, ex1, y1, ey1 = mid+22, mid+22, 0, bird_hight2
            x2, ex2, y2, ey2 = mid-22-43, mid-22-43, 0, bird_hight2
            x3, ex3, y3, ey3 = mid+22+43, mid+22+43, 0, bird_hight2
            x4, ex4, y4, ey4 = mid-22-86, mid-22-86, 0, bird_hight2
            x5, ex5, y5, ey5 = mid+22+86, mid+22+86, 0, bird_hight2
            cv2.line(mask_final, (int(x0), int(y0)), (int(ex0), int(ey0)), (0,0,0), 3)
            cv2.line(mask_final, (int(x1), int(y1)), (int(ex1), int(ey1)), (0,0,0), 3)
            cv2.line(mask_final, (int(x2), int(y2)), (int(ex2), int(ey2)), (0,0,0), 3)
            cv2.line(mask_final, (int(x3), int(y3)), (int(ex3), int(ey3)), (0,0,0), 3)
            cv2.line(mask_final, (int(x4), int(y4)), (int(ex4), int(ey4)), (0,0,0), 3)
            cv2.line(mask_final, (int(x5), int(y5)), (int(ex5), int(ey5)), (0,0,0), 3)
            low_thres_1 = 3350
            high_thres_1 = 3690
            batas.append(mid-22-86)
            batas.append(mid-22-43)
            batas.append(mid-22)
            batas.append(mid+22)
            batas.append(mid+22+43)
            batas.append(mid+22+86)
        elif divider == 5:
            range_const = 18
            list_save = 6
            tengah = 3
            x0, ex0, y0, ey0 = mid-18, mid-18, 0, bird_hight2
            x1, ex1, y1, ey1 = mid+18, mid+22, 0, bird_hight2
            x2, ex2, y2, ey2 = mid-18-35, mid-18-35, 0, bird_hight2
            x3, ex3, y3, ey3 = mid+18+35, mid+18+35, 0, bird_hight2
            x4, ex4, y4, ey4 = mid-18-70, mid-18-70, 0, bird_hight2
            x5, ex5, y5, ey5 = mid+18+70, mid+18+70, 0, bird_hight2
            cv2.line(mask_final, (int(x0), int(y0)), (int(ex0), int(ey0)), (0,0,0), 3)
            cv2.line(mask_final, (int(x1), int(y1)), (int(ex1), int(ey1)), (0,0,0), 3)
            cv2.line(mask_final, (int(x2), int(y2)), (int(ex2), int(ey2)), (0,0,0), 3)
            cv2.line(mask_final, (int(x3), int(y3)), (int(ex3), int(ey3)), (0,0,0), 3)
            cv2.line(mask_final, (int(x4), int(y4)), (int(ex4), int(ey4)), (0,0,0), 3)
            cv2.line(mask_final, (int(x5), int(y5)), (int(ex5), int(ey5)), (0,0,0), 3)
            low_thres_1 = 2600
            high_thres_1 = 2940
            batas.append(mid-18-70)
            batas.append(mid-18-35)
            batas.append(mid-18)
            batas.append(mid+18)
            batas.append(mid+18+35)
            batas.append(mid+18+70)
        elif divider >= 6:
            range_const = 15
            list_save = 7
            tengah = 3
            x0, ex0, y0, ey0 = mid-15, mid-15, 0, bird_hight2
            x1, ex1, y1, ey1 = mid+15, mid+15, 0, bird_hight2
            x2, ex2, y2, ey2 = mid-15-29, mid-15-29, 0, bird_hight2
            x3, ex3, y3, ey3 = mid+15+29, mid+15+29, 0, bird_hight2
            x4, ex4, y4, ey4 = mid-15-58, mid-15-58, 0, bird_hight2
            x5, ex5, y5, ey5 = mid+15+58, mid+15+58, 0, bird_hight2
            cv2.line(mask_final, (int(x0), int(y0)), (int(ex0), int(ey0)), (0,0,0), 3)
            cv2.line(mask_final, (int(x1), int(y1)), (int(ex1), int(ey1)), (0,0,0), 3)
            cv2.line(mask_final, (int(x2), int(y2)), (int(ex2), int(ey2)), (0,0,0), 3)
            cv2.line(mask_final, (int(x3), int(y3)), (int(ex3), int(ey3)), (0,0,0), 3)
            cv2.line(mask_final, (int(x4), int(y4)), (int(ex4), int(ey4)), (0,0,0), 3)
            cv2.line(mask_final, (int(x5), int(y5)), (int(ex5), int(ey5)), (0,0,0), 3)
            low_thres_1 = 2100
            high_thres_1 = 2470
            batas.append(mid-15-58)
            batas.append(mid-15-29)
            batas.append(mid-15)
            batas.append(mid+15)
            batas.append(mid+15+29)
            batas.append(mid+15+58)

        #################################################################################

        divy = bird_hight2/6
        x0, ex0, y0, ey0 = 0, bird_hight2, divy, divy
        x1, ex1, y1, ey1 = 0, bird_hight2, divy+divy, divy+divy
        x2, ex2, y2, ey2 = 0, bird_hight2, divy+divy+divy, divy+divy+divy
        x3, ex3, y3, ey3 = 0, bird_hight2, divy+divy+divy+divy, divy+divy+divy+divy
        x4, ex4, y4, ey4 = 0, bird_hight2, divy+divy+divy+divy+divy, divy+divy+divy+divy+divy

        cv2.line(mask_final, (int(x0), int(y0)), (int(ex0), int(ey0)), (0,0,0), 3)
        cv2.line(mask_final, (int(x1), int(y1)), (int(ex1), int(ey1)), (0,0,0), 3)
        cv2.line(mask_final, (int(x2), int(y2)), (int(ex2), int(ey2)), (0,0,0), 3)
        cv2.line(mask_final, (int(x3), int(y3)), (int(ex3), int(ey3)), (0,0,0), 3)
        cv2.line(mask_final, (int(x4), int(y4)), (int(ex4), int(ey4)), (0,0,0), 3)

        mask_final = cv2.cvtColor(mask_final, cv2.COLOR_BGR2GRAY)
        _, mask_final = cv2.threshold(mask_final, 30, 255, cv2.THRESH_BINARY)
        _, contours, hier = cv2.findContours(mask_final, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        # Threshold for divide 5
        save_x = []
        save_y = []

        check_pos = np.zeros((6,list_save))
        check_x = np.zeros((6,list_save))
        check_y = np.zeros((6,list_save))

        for cnt in contours:
            #print("cnt = ", cv2.contourArea(cnt))
            if low_thres_1 < cv2.contourArea(cnt) < high_thres_1:
                cv2.drawContours(mask_calc, [cnt], -1, (0,255,0), 2)
                cv2.drawContours(viz, [cnt], -1, (0,255,0), -1)
                vizz = cv2.dilate(viz, kernel,iterations = 2)
                # Save the Position
                Mz = cv2.moments(cnt)
                cX = int(Mz["m10"] / Mz["m00"])
                cY = int(Mz["m01"] / Mz["m00"])
                cv2.circle(mask_calc, (cX, cY), 7, (255, 255, 255), -1)

                # Convert to current format
                # cX_conv = cX-bird_width2/2
                # cY_conv = bird_hight2-cY
                # save_x.append(cX_conv)
                # save_y.append(cY_conv)
                save_x.append(cX)
                save_y.append(cY)

                check_pos = check_posisi(cX, cY, check_pos, batas)

        inv_save_x = save_x[::-1]
        inv_save_y = save_y[::-1]

        nrow = len(check_pos)
        ncol = len(check_pos[0])

        #################################################################################################################################################
        # Forward Direction Information
        hitung_pos = 0
        for i in range(0, nrow):
            for j in range(0, ncol):
                if check_pos[i, j] == 1:
                    check_x[i,j] = inv_save_x[hitung_pos]
                    check_y[i,j] = inv_save_y[hitung_pos]
                    hitung_pos += 1

        # Remove occluded by car area
        for n in range(nrow-1, 0, -1):
            if n != 0:
                if check_pos[n, tengah] == 0 and check_pos[n-1, tengah] == 1:
                    check_pos[n-1, tengah] = 0
                    check_x[n-1, tengah] = 0
                    check_y[n-1, tengah] = 0

        flat_x = check_x.flatten()
        flat_y = check_y.flatten()

        # For when and where
        check_flat_x = check_x.flatten()
        check_flat_y = check_y.flatten()

        flat_x = remove_values_from_list(flat_x, 0)
        flat_y = remove_values_from_list(flat_y, 0)

        # For when and where
        for i in range(len(check_flat_x)):
            if check_flat_x[i] != 0:
                if i in dic_free:
                    dic_free[i] += 1
                else:
                    dic_free[i] = 1

        write_x = []
        write_y = []

        for n in range(len(check_flat_x)):
            cX = check_flat_x[n]
            cY = check_flat_y[n]
            cX_conv = cX-bird_width2/2
            cY_conv = bird_hight2-cY
            write_x.append(cX)
            write_y.append(cY)
            if cX != 0:
                cv2.rectangle(coba, (int(cX) - range_const, int(cY) - 51), (int(cX) + range_const, int(cY) + 51), (0,255,0), cv2.FILLED)

        #################################################################################################################################################

        #################################################################################################################################################
        # Reverse Direction Information
        if frame_id == 0:
            check_rev = np.zeros((6,list_save))

        check_rev2 = np.zeros((6,list_save))
        check_x_rev = np.zeros((6,list_save))
        check_y_rev = np.zeros((6,list_save))

        for p in range(len(y_rev)):
            cX_rev = x_rev[p]
            cY_rev = y_rev[p]
            #print(cX_rev, "  ", cY_rev)
            check_rev = check_posisi(cX_rev, cY_rev, check_rev, batas)
            check_rev2 = check_posisi(cX_rev, cY_rev, check_rev2, batas)
            cv2.rectangle(rev2, (int(cX_rev) - range_const, int(cY_rev) - 51), (int(cX_rev) + range_const, int(cY_rev) + 51), (0,0,255), cv2.FILLED)

        inv_save_x_rev = x_rev[::-1]
        inv_save_y_rev = y_rev[::-1]

        nrow_rev = len(check_rev2)
        ncol_rev = len(check_rev2[0])

        hitung_pos = 0
        for i in range(0, nrow_rev):
            for j in range(0, ncol_rev):
                if check_rev2[i, j] == 1:
                    check_x_rev[i,j] = inv_save_x_rev[hitung_pos]
                    check_y_rev[i,j] = inv_save_y_rev[hitung_pos]
                    hitung_pos += 1

        flat_x_rev = check_x_rev.flatten()
        flat_y_rev = check_y_rev.flatten()

        # For when and where
        check_flat_x_rev = check_x_rev.flatten()
        check_flat_y_rev = check_y_rev.flatten()

        # For starting point reverse
        for i in range(len(check_flat_x_rev)):
            if check_flat_x_rev[i] != 0:
                if i in simpan_reverse:
                    continue
                else:
                    simpan_reverse[i] = imgnum


        flat_x_rev = remove_values_from_list(flat_x_rev, 0)
        flat_y_rev = remove_values_from_list(flat_y_rev, 0)

        # For when and where
        for i in range(len(check_flat_x_rev)):
            if check_flat_x_rev[i] != 0:
                if i in dic_free_rev:
                    dic_free_rev[i] += 1
                else:
                    dic_free_rev[i] = 1

        write_x_rev = []
        write_y_rev = []

        for n in range(len(check_flat_x_rev)):
            cX = check_flat_x_rev[n]
            cY = check_flat_y_rev[n]
            write_x_rev.append(cX)
            write_y_rev.append(cY)
            if cX != 0:
                cv2.rectangle(rev2, (int(cX) - range_const, int(cY) - 51), (int(cX) + range_const, int(cY) + 51), (0,0,255), cv2.FILLED)
        #################################################################################################################################################

        rev_file.create_dataset('frame_id_rev', data = imgnum)
        rev_file.create_dataset('range_const_rev', data = range_const)
        rev_file.create_dataset('pos_x_rev', data = write_x_rev)
        rev_file.create_dataset('pos_y_rev', data = write_y_rev)

        # List of possibility frame reversw
        poss_rev.append(len(flat_x_rev))
        #####

        info_file.create_dataset('frame_id', data = imgnum)
        info_file.create_dataset('range_const', data = range_const)
        info_file.create_dataset('pos_x', data = write_x)
        info_file.create_dataset('pos_y', data = write_y)
        info_file.create_dataset('check_pos', data = check_pos)

        # COba ####################################
        coba_file.create_dataset('pos_x_rev', data = write_x)
        coba_file.create_dataset('pos_y_rev', data = write_y)
        coba_file.create_dataset('check_pos', data = check_pos)
        coba_file.create_dataset('range_const', data = range_const)
        coba_file.create_dataset('list_save', data = list_save)
        coba_file.create_dataset('tengah', data = tengah)

        # List of possibility frame
        poss.append(len(flat_x))

        # Optional Display
        cover_image = cv2.addWeighted(warped_img, 1, coba, 0.3, 0)
        cover_image_rev = cv2.addWeighted(warped_img, 1, rev2, 0.3, 0)

        # Inverse Display
        Minv = cv2.getPerspectiveTransform(dst, src)
        inverse_img = cv2.warpPerspective(cover_image, Minv, (1280, 385))

        cv2.imshow("img", img)
        cv2.imshow("cover_image", cover_image)
        cv2.imshow("cover_image_rev", cover_image_rev)
        cv2.imwrite(raw_dir+imgnum+'.png', coba)
        cv2.imwrite(vis_dir+imgnum+'.png', cover_image)
        print("")
        cv2.waitKey(1)

    print(" ")
    print(" ")

    print("poss = ", poss)
    print("dic_free = ", dic_free)

    print("")

    print("poss_rev = ", poss_rev)
    print("dic_free_rev = ", dic_free_rev)

    print("")
    print("size = ", 6*list_save)

    # # Range only 30 meters for forward direction
    # if list_save == 4:
    #     for i in range(0,11):
    #         if i in dic_free:
    #             dic_free.pop(i, None)
    #             dic_free_rev.pop(i, None)
    #         else:
    #             continue
    # elif list_save == 5:
    #     for i in range(0,14):
    #         if i in dic_free:
    #             dic_free.pop(i, None)
    #             dic_free_rev.pop(i, None)
    #         else:
    #             continue
    # elif list_save == 6:
    #     for i in range(0,18):
    #         if i in dic_free:
    #             dic_free.pop(i, None)
    #             dic_free_rev.pop(i, None)
    #         else:
    #             continue
    # elif list_save == 7:
    #     for i in range(0,20):
    #         if i in dic_free:
    #             dic_free.pop(i, None)
    #             dic_free_rev.pop(i, None)
    #         else:
    #             continue

    # Range only 30 meters for forward direction
    if list_save == 4:
        for i in range(0,16):
            if i in dic_free or i in dic_free_rev:
                dic_free.pop(i, None)
                dic_free_rev.pop(i, None)
            else:
                continue
    elif list_save == 5:
        for i in range(0,20):
            if i in dic_free or i in dic_free_rev:
                dic_free.pop(i, None)
                dic_free_rev.pop(i, None)
            else:
                continue
    elif list_save == 6:
        for i in range(0,24):
            if i in dic_free or i in dic_free_rev:
                dic_free.pop(i, None)
                dic_free_rev.pop(i, None)
            else:
                continue
    elif list_save == 7:
        for i in range(0,28):
            if i in dic_free or i in dic_free_rev:
                dic_free.pop(i, None)
                dic_free_rev.pop(i, None)
            else:
                continue

    print("dic_free = ", dic_free)
    print("dic_free_rev = ", dic_free_rev)
    print("simpan_reverse = ", simpan_reverse)


    # When start to add car
    rata2_free = np.mean(poss)
    print("rata2_free = ", rata2_free)
    start_flag = 0
    for i in range(len(poss)):
        if poss[i] >= rata2_free:
            if start_flag == 0:
                start_frame = str(i).zfill(4)
                start_flag = 1
            else:
                start_frame = start_frame

    # Where start to add car
    banyak = [k for k, v in dic_free.items() if v == max(dic_free.values())]

    # Save
    free_area_file = h5py.File(data_dir+'free_area.h5','w')
    free_area_file.create_dataset('start_frame', data = start_frame)
    free_area_file.create_dataset('position', data = banyak)
    free_area_file.create_dataset('list_save', data = list_save)
    print("avg free = ", rata2_free)
    print("banyak = ", banyak)
    print("start_frame = ", start_frame)
    print("")


    # When start to add car
    start_flag = 0
    for i in range(len(poss_rev)):
        if poss_rev[i] > 0:
            if start_flag == 0:
                start_frame = str(i).zfill(4)
                start_flag = 1
            else:
                start_frame = start_frame

    # Where start to add car
    banyak = [k for k, v in dic_free_rev.items() if v == max(dic_free_rev.values())]

    # Connect where to start
    # for i in range(len(banyak)):
    print("dic_free_rev = ", dic_free_rev)
    print("simpan_reverse = ", simpan_reverse)
    print("banyak[0] = ", banyak)
    if len(banyak) != 0:
        mulai = simpan_reverse[banyak[0]]
    else:
        mulai = 1
        mulai = str(mulai).zfill(4)

    # Save
    free_area_file = h5py.File(data_dir+'free_area_rev.h5','w')
    free_area_file.create_dataset('start_frame_rev', data = mulai)
    free_area_file.create_dataset('position_rev', data = banyak)
    free_area_file.create_dataset('list_save', data = list_save)
    print("banyak = ", banyak)
    print("start_frame = ", mulai)
    print("")

    # Revert back to front view
    Minv = cv2.getPerspectiveTransform(dst, src) # Inverse transformation
    inverse_img = cv2.warpPerspective(coba, Minv, (1280, 385))# Image warping
    final_image = cv2.addWeighted(img, 1, inverse_img, 0.3, 0)
    cv2.imshow("inverse_img.png", final_image)
    cv2.waitKey(1)

def read_area(data_dir):
    image_dir = data_dir+'Images/'
    images = os.listdir(image_dir)
    images.sort()

    print("Visualization ----------------------------------------------")

    mask_dir = data_dir+'Free_Area_Vis/Free_Area_Raw/'

    free_area_dir = data_dir+'Free_Area/'

    rev_area_dir = data_dir+'Rev_Area/'

    # Read information of starting point (selected area)
    with h5py.File(data_dir+'free_area.h5','r') as ra:
        start_frame = ra['start_frame'].value
        position = ra['position'].value
        list_save = ra['list_save'].value

    print("start_frame = ", start_frame)    # 0000
    print("position = ", position)          # 15
    print("list_save = ", list_save)
    print("")

    # Untuk bounding box
    total = 6 * list_save
    print("total = ", total)
    print("")

    # Read information of starting point (selected area) REVERSE
    with h5py.File(data_dir+'free_area_rev.h5','r') as ra:
        start_frame_rev = ra['start_frame_rev'].value
        position_rev = ra['position_rev'].value
        list_save = ra['list_save'].value

    # Unzfill
    start_frame_rev = start_frame_rev.lstrip('0')
    start_frame_rev = int(start_frame_rev)+2
    start_frame_rev = str(start_frame_rev).zfill(4)

    print("start_frame_rev = ", start_frame_rev)    # 0000
    print("position_rev = ", position_rev)          # 15
    print("list_save = ", list_save)
    print("")

    # Read information of BEV parameters
    with h5py.File(data_dir+'parameters.h5','r') as pf:
        src = pf['src'].value
        bird_hight2 = pf['bird_hight'].value
        bird_width2 = pf['bird_width'].value
        bird_channels = pf['bird_channels'].value

    single_mask = np.zeros((bird_hight2,bird_width2,3), np.uint8)
    single_mask_rev = np.zeros((bird_hight2,bird_width2,3), np.uint8)

    # Revert back to front view
    dst = np.float32([[0, 0], [bird_width2, 0], [0, bird_hight2], [bird_width2, bird_hight2]])
    Minv = cv2.getPerspectiveTransform(dst, src) # Inverse transformation
    img_rgb = cv2.imread(image_dir+start_frame+".png")
    img_rgb_rev = cv2.imread(image_dir+start_frame_rev+".png")

    #####################################################################################################################
    # Read free area information
    with h5py.File(free_area_dir+start_frame+'.h5','r') as fa:
        frame_id = fa['frame_id'].value
        range_const = fa['range_const'].value
        pos_x = fa['pos_x'].value
        pos_y = fa['pos_y'].value

    print("frame_id = ", frame_id)
    print("pos_x = ", pos_x)
    print("pos_y = ", pos_y)
    print("")

    # Read the selected free area based on the indexing
    added_fw = []
    for i in range(len(position)):
        data = position[i]
        selected_pos_x = pos_x[data]
        selected_pos_y = pos_y[data]
        print("data = ", data)
        print("selected_pos_x = ", selected_pos_x)
        print("selected_pos_y = ", selected_pos_y)
        cv2.rectangle(single_mask, (int(selected_pos_x) - range_const, int(selected_pos_y) - 51), (int(selected_pos_x) + range_const, int(selected_pos_y) + 51), (0,255,0), cv2.FILLED)

        if total-1-list_save < data <= total-1:
            added_fw.append(60)
        elif total-1-list_save-list_save < data <= total-1-list_save:
            added_fw.append(20)

    if len(added_fw) != 0:
        fw_value = min(added_fw)
        inverse_img_single = cv2.warpPerspective(single_mask, Minv, (1280, 385))
        free_area_img_single = cv2.addWeighted(img_rgb, 1, inverse_img_single, 0.3, 0)
        fw = cv2.cvtColor(inverse_img_single, cv2.COLOR_BGR2GRAY)
        _, fw_mask = cv2.threshold(fw, 30, 255, cv2.THRESH_BINARY)
        _, contours, hier = cv2.findContours(fw_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        for cnt in contours:
            x,y,w,h = cv2.boundingRect(cnt)
            cv2.rectangle(free_area_img_single,(x,y-fw_value),(x+w,y+h),(0,255,0),1)

        cv2.imshow("free_area_img_single.png", free_area_img_single)
        cv2.imwrite("free_area_img_single.png", free_area_img_single)
        cv2.waitKey(0)
    else :
        print("No Forward Free Area")


    print("")
    print("----------------------------------------------------")
    print("")

    #####################################################################################################################
    # Read free area information REVERSE
    with h5py.File(rev_area_dir+start_frame_rev+'.h5','r') as fa:
        frame_id_rev = fa['frame_id_rev'].value
        range_const_rev = fa['range_const_rev'].value
        pos_x_rev = fa['pos_x_rev'].value
        pos_y_rev = fa['pos_y_rev'].value

    print("frame_id_rev = ", frame_id_rev)
    print("pos_x_rev = ", pos_x_rev)
    print("pos_y_rev = ", pos_y_rev)
    print("")

    # Read the selected free area based on the indexing
    added_rw = []
    for i in range(len(position_rev)):
        data = position_rev[i]
        selected_pos_x = pos_x_rev[data]
        selected_pos_y = pos_y_rev[data]
        print("data = ", data)
        print("selected_pos_x = ", selected_pos_x)
        print("selected_pos_y = ", selected_pos_y)
        cv2.rectangle(single_mask_rev, (int(selected_pos_x) - range_const, int(selected_pos_y) - 51), (int(selected_pos_x) + range_const, int(selected_pos_y) + 51), (0,0,255), cv2.FILLED)

        print("1 = ", total-1)
        print("2 = ", total-1-list_save)
        print("3 = ", total-1-list_save-list_save)

        if total-1-list_save < data <= total-1:
            added_rw.append(60)
        elif total-1-list_save-list_save < data <= total-1-list_save:
            added_rw.append(20)

    if len(added_rw) != 0:
        rw_value = min(added_rw)
        inverse_img_single_rev = cv2.warpPerspective(single_mask_rev, Minv, (1280, 385))
        free_area_img_single_rev = cv2.addWeighted(img_rgb_rev, 1, inverse_img_single_rev, 0.3, 0)
        rw = cv2.cvtColor(inverse_img_single_rev, cv2.COLOR_BGR2GRAY)
        _, fw_mask = cv2.threshold(rw, 30, 255, cv2.THRESH_BINARY)
        _, contours, hier = cv2.findContours(fw_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        
        for cnt in contours:
            x,y,w,h = cv2.boundingRect(cnt)
            cv2.rectangle(free_area_img_single_rev,(x,y-rw_value),(x+w,y+h),(0,0,255),1)

        cv2.imshow("free_area_img_single_rev.png", free_area_img_single_rev)
        cv2.imwrite("free_area_img_single_rev.png", free_area_img_single_rev)
        cv2.waitKey(0)
    else :
        print("No Reverse Free Area")

    

if __name__ == '__main__':
    from det_reverse import det_rev2
    data_dir = "/media/ferdyan/LocalDiskE/Hasil/dataset/New/X_ooc14/"
    det_rev2(data_dir)
    area(data_dir)
    read_area(data_dir)
