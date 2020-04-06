import os
import cv2
import sys
import random
import numpy as np

from tqdm import tqdm
import matplotlib.pyplot as plt
# import tensorflow as tf
from sklearn.metrics import confusion_matrix

from ulitities.base_functions import load_img_by_cv2,get_file,load_img_by_gdal,send_message_callback

ROAD_VALUE=127
BUILDING_VALUE=255
SMOOTH=0.001

def check_input_file(files):
    ret, img_1 = load_img_by_cv2(files[0], grayscale=True)
    assert (ret == 0)

    height, width = img_1.shape
    num_img = len(files)

    for next_index in range(1,num_img):
        # print(files[next_index])
        next_ret, next_img=load_img_by_cv2(files[next_index],grayscale=True)
        assert (next_ret ==0 )
        next_height, next_width = next_img.shape
        assert(height==next_height and width==next_width)
    return height, width

def binarize_mask(input_dict):
    threshold = input_dict['threshold']
    grayscale_mask_path = input_dict['grayscale_mask']
    binary_mask_saving_path = input_dict['binary_mask']

    if not os.path.isfile(grayscale_mask_path):
        print("input file do not exist!\n")
        return -2
    print("input grayscale mask: {}".format(grayscale_mask_path))

    img = cv2.imread(grayscale_mask_path, cv2.IMREAD_GRAYSCALE)

    result = np.zeros(img.shape, np.uint8)
    ind_foreground = np.where(img>threshold)
    result[ind_foreground]=1
    plt.imshow(result)
    plt.show()

    cv2.imwrite(binary_mask_saving_path,result)

    return 0

def batchbinarize_masks(send_message_callback,inputdict):
    threshold = inputdict['threshold']
    inputdir=inputdict['inputdir']
    outputdir=inputdict['outputdir']
    if not os.path.isdir(inputdir):
        print("Warning: ")
        return -1

    files, num= get_file(inputdir)

    for file in files:#tqdm(files):
        send_message_callback("Dealing : "+file)
        img = cv2.imread(file, cv2.IMREAD_GRAYSCALE)

        result = np.zeros(img.shape, np.uint8)
        ind_foreground = np.where(img > threshold)
        result[ind_foreground] = 1
        # plt.imshow(result)
        # plt.show()

        absname = os.path.split(file)[1]
        # absname = absname.split('.')[0]
        # absname = 'shuidao.png'
        # absname = ''.join([absname, '.png'])

        mask_saving_path = os.path.join(outputdir, absname)

        cv2.imwrite(mask_saving_path, result)


    return 0


def combine_masks(send_message_callback,input_dict):
    send_message_callback("Begin")
    FOREGROUND = input_dict['foreground']
    road_mask = input_dict['road_mask']
    building_mask = input_dict['building_mask']
    output_file = input_dict['save_mask']

    files = [road_mask, building_mask]
    print("road mask:{}".format(road_mask))
    print("building mask:{}".format(building_mask))
    height, width = check_input_file(files)

    final_mask = np.zeros((height, width), np.uint8)
    for idx, file in enumerate(files):
        send_message_callback("Dealing : " + file )
        ret, img = load_img_by_cv2(file, grayscale=True)
        assert (ret == 0)
        label_value = 0
        if idx ==0:
            label_value = ROAD_VALUE
        else:
            label_value = BUILDING_VALUE
        # label_value = idx+1
        # print("buildings prior")
        print("Roads prior")
        for i in tqdm(range(height)):
            for j in range(width):
                if img[i, j] >= FOREGROUND:
                    # print ("img[{},{}]:{}".format(i,j,img[i,j]))

                    if label_value == ROAD_VALUE:
                        final_mask[i, j] = label_value
                    elif label_value == BUILDING_VALUE and final_mask[i, j] != ROAD_VALUE:
                        final_mask[i, j] = label_value

                    # if label_value == BUILDING_VALUE:
                    #     final_mask[i, j] = label_value
                    # elif label_value == ROAD_VALUE and final_mask[i, j] != BUILDING_VALUE:
                    #     final_mask[i, j] = label_value

    final_mask[final_mask == ROAD_VALUE] = 1
    final_mask[final_mask == BUILDING_VALUE] = 2

    plt.imshow(final_mask, cmap='gray')
    plt.title("combined mask")
    plt.show()

    cv2.imwrite(output_file, final_mask)
    print("Saved to : {}".format(output_file))


def vote_masks(send_message_callback,input_dict):
    send_message_callback("Begin")

    target_values = input_dict['target_values']
    num_target = len(target_values)
    input_files = input_dict['input_files']
    output_file = input_dict['save_mask']

    send_message_callback("Dealing : " + input_files)

    files = input_files.split(';')

    height, width = check_input_file(files)

    mask_list = []
    for file in files:
        ret, img = load_img_by_cv2(file, grayscale=True)
        print(file)
        assert (ret == 0)
        mask_list.append(img)

    vote_mask = np.zeros((height, width), np.uint8)

    for i in tqdm(range(height)):
        for j in range(width):
            # record=np.zeros(256,np.uint8)
            record = np.zeros(num_target, np.uint8)
            for n in range(len(mask_list)):
                mask = mask_list[n]
                pixel = mask[i, j]
                record[pixel] += 1

            # """Alarming"""
            if record.argmax() == 0:  # if argmax of 0 = 125 or 255, not prior considering background(0)
                record[0] -= 1
            # print("record:{}".format(record))
            # a = record[1:]
            # print("else:{}".format(a))
            # if a.any()>1:
            #     record[0]=0

            label = record.argmax()
            # print ("{},{} label={}".format(i,j,label))
            vote_mask[i, j] = label
    # vote_mask[vote_mask==125]=1
    # vote_mask[vote_mask == 255] = 2
    print(np.unique(vote_mask))

    cv2.imwrite(output_file, vote_mask)
    return 0




def accuracy_evalute(send_message_callback,input_dict):
    ref_file = input_dict['gt_file']
    pred_file = input_dict['mask_file']
    valid_labels = input_dict['valid_values']
    n_class = len(valid_labels)
    check_rate = input_dict['check_rate']
    # gup_id = input_dict['GPUID']
    # os.environ["CUDA_VISIBLE_DEVICES"] = gup_id
    # input_files = []
    # if os.path.isfile(config.img_input):
    #     print("[INFO] input is one file...")
    #     input_files.append(config.img_input)
    # elif os.path.isdir(config.img_input):
    #     print("[INFO] input is a directory...")
    #     in_files, _ = get_file(config.img_input)
    #     for file in in_files:
    #         input_files.append(file)
    # if len(input_files) == 0:
    #     print("no input images")
    #     sys.exit(-1)
    # print("{} images will be classified".format(len(input_files)))


    ref_img = load_img_by_gdal(ref_file, grayscale=True)

    pred_img = load_img_by_gdal(pred_file, grayscale=True)

    send_message_callback("\nfile: {}".format(os.path.split(pred_file)[1]))

    send_message_callback("[INFO] Calculate confusion matrix..\n")

    ref_img = np.array(ref_img)
    height, width = ref_img.shape
    send_message_callback(height, width)
    if height != pred_img.shape[0] or width != pred_img.shape[1]:
        send_message_callback("image sizes of reference and predicted are not equal!\n")

    img_length = height * width
    if check_rate<0.01:
        check_rate=0.01
    elif check_rate>1.00:
        check_rate=1.00
    else:
        pass

    # assert (check_rate > 0.001 and check_rate <= 1.00)
    num_checkpoints = np.int(img_length * check_rate)

    pos = random.sample(range(img_length), num_checkpoints)

    """reshape images from two to one dimension"""
    ref_img = np.reshape(ref_img, height * width)
    pred_img = np.reshape(pred_img, height * width)

    labels = ref_img[pos]

    """ignore nodata pixels"""
    valid_index = []
    for tt in valid_labels:
        ind = np.where(labels == tt)
        ind = list(ind)
        valid_index.extend(ind[0])

    valid_index.sort()
    valid_num_checkpoints = len(valid_index)
    send_message_callback("{}points have been selected, and {} valid points will be used to evaluate accuracy!\n".format(num_checkpoints,
                                                                                                   valid_num_checkpoints))
    # valid_ref=ref_img[valid_index]
    valid_ref = labels[valid_index]
    send_message_callback("valid value in reference image: {}".format(np.unique(valid_ref)))

    ts = pred_img[pos]
    valid_pred = ts[valid_index]
    send_message_callback("valid value in predicton image: {}".format(np.unique(valid_pred)))

    tmp = np.unique(valid_pred)
    """make nodata to zero in predicted results"""
    for ss in tmp:
        if not ss in valid_labels:
            nodata_index = np.where(valid_pred==ss)
            valid_pred[nodata_index]=0

    confus_matrix = confusion_matrix(valid_ref,valid_pred,range(n_class))
    # confus_matrix = tf.contrib.metrics.confusion_matrix(valid_pred, valid_ref, n_class)
    # with tf.Session() as sess:
    #     confus_matrix = sess.run(confus_matrix)
    send_message_callback(confus_matrix)

    confus_matrix = np.array(confus_matrix)

    oa = 0
    x_row_plus = []
    x_col_plus = []
    x_diagonal = []
    for i in range(n_class):
        oa += confus_matrix[i, i]
        x_diagonal.append(confus_matrix[i, i])
        row_sum = sum(confus_matrix[i, :])
        col_sum = sum(confus_matrix[:, i])
        x_row_plus.append(row_sum)
        x_col_plus.append(col_sum)

    send_message_callback("x_row_plus:{}".format(x_row_plus))
    send_message_callback("x_col_plus:{}".format(x_col_plus))
    x_row_plus = np.array(x_row_plus)
    x_col_plus = np.array(x_col_plus)
    x_diagonal = np.array(x_diagonal)
    x_total = sum(x_row_plus)
    OA_acc = oa / (sum(x_row_plus))
    send_message_callback("\nOA:{:.3f}".format(OA_acc))
    tmp = x_col_plus * x_row_plus
    kappa = (x_total * sum(x_diagonal) - sum(x_col_plus * x_row_plus)) / np.float(
        x_total * x_total - sum(x_col_plus * x_row_plus))

    send_message_callback("Kappa:{:.3f}".format(kappa))

    for i in range(n_class):
        i = i
        prec = x_diagonal[i] / (x_row_plus[i]+SMOOTH)
        send_message_callback("\nForground of {}".format(i))
        send_message_callback("precision= {:.3f}".format(prec))
        recall = x_diagonal[i] / (x_col_plus[i]+SMOOTH)
        send_message_callback("recall= {:.3f}".format(recall))
        F1_score = (2*recall*prec)/(recall+prec)
        send_message_callback("F1_score= {:.3f}".format(F1_score))
        iou = x_diagonal[i] / (x_row_plus[i] + x_col_plus[i] - x_diagonal[i]+SMOOTH)
        send_message_callback("iou= {:.3f}".format(iou))

