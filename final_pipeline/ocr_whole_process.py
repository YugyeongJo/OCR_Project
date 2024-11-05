from transformers import TrOCRProcessor, VisionEncoderDecoderModel, AutoTokenizer
import requests
import unicodedata
from io import BytesIO
from PIL import Image
import os
import time
import torch
import cv2
import numpy as np
from torch.autograd import Variable
import json
import sys

custom_folder = './CRAFT_pytorch'
sys.path.append(custom_folder)

from collections import OrderedDict
from craft import CRAFT
import craft_utils
import imgproc

def copyStateDict(state_dict):
    if list(state_dict.keys())[0].startswith("module"):
        start_idx = 1
    else:
        start_idx = 0
    new_state_dict = OrderedDict()
    for k, v in state_dict.items():
        name = ".".join(k.split(".")[start_idx:])
        new_state_dict[name] = v
    return new_state_dict


device = "cuda" if torch.cuda.is_available() else "cpu"



class CLOVA_CRAFT:

    def load_craft_model(self,model_path):
        net = CRAFT()  # Initialize CRAFT
        net.load_state_dict(copyStateDict(torch.load(model_path, map_location='cuda' if torch.cuda.is_available() else 'cpu')))
        net.eval()
        return net

    def detect_text_boxes(self,net, image, text_threshold=0.7, link_threshold=0.4, low_text=0.4):
        # Resize image
        img_resized, target_ratio, size_heatmap = imgproc.resize_aspect_ratio(image, 1280, interpolation=cv2.INTER_LINEAR, mag_ratio=1.5)
        ratio_h = ratio_w = 1 / target_ratio

        # Preprocess image
        x = imgproc.normalizeMeanVariance(img_resized)
        x = torch.from_numpy(x).permute(2, 0, 1)  # [h, w, c] to [c, h, w]
        x = Variable(x.unsqueeze(0))              # [c, h, w] to [b, c, h, w]

        if torch.cuda.is_available():
            x = x.cuda()

        # Forward pass
        with torch.no_grad():
            y, feature = net(x)

        # Score maps
        score_text = y[0, :, :, 0].cpu().numpy()
        score_link = y[0, :, :, 1].cpu().numpy()

        # Post-processing
        boxes, polys = craft_utils.getDetBoxes(score_text, score_link, text_threshold, link_threshold, low_text)

        # Coordinate adjustment
        boxes = craft_utils.adjustResultCoordinates(boxes, ratio_w, ratio_h)
        polys = craft_utils.adjustResultCoordinates(polys, ratio_w, ratio_h)

        for k in range(len(polys)):
            if polys[k] is None: polys[k] = boxes[k]

        return boxes, polys



class Just_TrOCR:

    def detecting(self,img):
        processor = TrOCRProcessor.from_pretrained("ddobokki/ko-trocr")
        model = VisionEncoderDecoderModel.from_pretrained("ddobokki/ko-trocr").to(device)
        tokenizer = AutoTokenizer.from_pretrained("ddobokki/ko-trocr")

        pixel_values = processor(img, return_tensors="pt").pixel_values.to(device)
        generated_ids = model.generate(pixel_values, max_length=64)
        generated_text = tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]
        generated_text = unicodedata.normalize("NFC", generated_text)
        return generated_text


def save_json(dict):
    with open( os.path.join(os.getcwd(),'pred_result.json'), 'w+',encoding='utf-8') as json_file:
        json.dump(dict, json_file)

def folder_or_img(path,func):
    temp_dict=dict({})

    if os.path.isdir(path):
        img_lst=[f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]

        pred_text_path = os.path.join(path, "pred_text")#박스의 좌표와 그에 따른 텍스트 저장을 위한 경로 만들기
        if not os.path.exists(pred_text_path):
            os.makedirs(pred_text_path)

        for i in img_lst:
            res_text=func(os.path.join(path,i))
            temp_dict[os.path.basename(i)]=res_text
        save_json(temp_dict)#폴더일 경우 내부 file들 전부를 ocr 텍스트 감지 후 json 저장///  key: file이름 value :감지 텍스트

    else:
        pass
        #res_text=func(os.path.join(path,i))
        #temp_dict[os.path.basename(i)] = res_text
        #save_json(temp_dict)


def group_and_sort_boxes(boxes):
    # Step 1: 그룹을 위한 리스트 초기화
    grouped_boxes = []

    # Step 2: 각 박스를 확인하며 그룹화
    for box in boxes:
        x_min, y_min = box[0]  # 왼쪽 위 좌표
        x_max, y_max = box[2]  # 오른쪽 아래 좌표
        height = y_max - y_min

        # 높이 좌표 유사성 그룹을 찾거나 새로운 그룹 생성
        added_to_group = False
        for group in grouped_boxes:
            _, y_min_group = group[0][0]
            _, y_max_group = group[0][2]
            group_height = y_max_group - y_min_group
            if abs(y_min - y_min_group) <= group_height / 2:  # 높이 유사성 기준
                group.append(box)
                added_to_group = True
                break

        if not added_to_group:
            grouped_boxes.append([box])  # 새로운 그룹 생성

    # Step 3: 각 그룹을 x 좌표의 최소값 기준으로 정렬
    for group in grouped_boxes:
        group.sort(key=lambda b: b[0][0])

    return grouped_boxes


if __name__ == '__main__':

    just_craft=CLOVA_CRAFT()
    ddobokki_trocr=Just_TrOCR()
    path="F:/abc/img_sample"

    def process(image_path):
        text_temp=str("")
        model_path = './CRAFT_pytorch/weights/craft_mlt_25k.pth'
        net = just_craft.load_craft_model(model_path)
        image = imgproc.loadImage(image_path)

        current_folder_path=os.path.dirname(image_path)
        pred_text_path = os.path.join(current_folder_path, "pred_text")
        pred_text_file_path =os.path.join(pred_text_path, f'{os.path.basename(image_path)}_pred.txt')

        boxes, polys = just_craft.detect_text_boxes(net, image)#박스영역 검출 결과
        image = Image.open(image_path)

        sorted_box=group_and_sort_boxes(boxes)#y유사성에 따라 박스를 묶은 뒤 x를 기준으로 sort

        with open(pred_text_file_path , "w+") as file:# 다시 돌릴 경우 초기화
            pass

        for sort_idx,box_y_sort in enumerate( sorted_box):

            assert isinstance(sorted_box,list)

            for idx,box in enumerate(box_y_sort):
                #print('box printing',box)
                assert isinstance(box_y_sort,list)
                assert isinstance(box,np.ndarray)

                box=box.tolist()

                """
                box[0],box[1],box[2],box[3]
                box printing [[ 8.       10.666667]
                                 [28.       10.666667]
                                 [28.       28.      ]
                                 [ 8.       28.      ]]
                """

                left,upper,right,lower=int(box[0][0]),int(box[1][1]),int(box[2][0]),int(box[3][1])

                cropped_image = image.crop((left,upper,right,lower))

                text_detected=ddobokki_trocr.detecting(cropped_image)
                assert isinstance(text_detected,str)

                with open(pred_text_file_path, "a+") as file:#txt 파일로도 추출 좌표##:: 텍스트 형태
                    pop_standard=f'{int(box[0][0])} {int(box[0][1])} {int(box[1][0])} {int(box[1][1])} {int(box[2][0])} {int(box[2][1])} {int(box[3][0])} {int(box[3][1])}##::{text_detected}\n'
                    file.write(pop_standard)

                text_temp+=text_detected

                if idx != len(box_y_sort)-1:
                    text_temp+=str(" ")

            if sort_idx!=len(sorted_box)-1:
                text_temp+="\n"

        print(text_temp)
        return text_temp

    folder_or_img(path,process)



