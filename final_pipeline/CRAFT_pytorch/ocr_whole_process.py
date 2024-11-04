from transformers import TrOCRProcessor, VisionEncoderDecoderModel, AutoTokenizer
import requests
from io import BytesIO
from PIL import Image
import os
import time
import torch
import cv2
import numpy as np
from torch.autograd import Variable



from craft import CRAFT
import craft_utils
import imgproc

from collections import OrderedDict

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
        processor = TrOCRProcessor.from_pretrained("microsoft/trocr-base-handwritten")
        model = VisionEncoderDecoderModel.from_pretrained("daekeun-ml/ko-trocr-base-nsmc-news-chatbot")
        tokenizer = AutoTokenizer.from_pretrained("daekeun-ml/ko-trocr-base-nsmc-news-chatbot")

        pixel_values = processor(img, return_tensors="pt").pixel_values
        generated_ids = model.generate(pixel_values, max_length=64)
        generated_text = tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]
        return generated_text


def save_json(dict):
    with open( os.path.join(os.getcwd(),'pred_result.json'), 'w+',encoding='utf-8') as json_file:
        json.dump(dict, json_file)

def folder_or_img(path,func):
    temp_dict=dict({})

    if os.path.isdir(path):

        img_lst=[f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
        for i in img_lst:
            res_text=func(os.path.join(path,i))
            temp_dict[os.path.basename(i)]=res_text
        save_json(temp_dict)#폴더일 경우 내부 file들 전부를 ocr 텍스트 감지 후 json 저장///  key: file이름 value :감지 텍스트

    else:
        pass
        # tempstr=str("")
        # recognition_lst, confidence_lst=func(path)
        # for str_ in recognition_lst:
        #     tempstr+=str_
        # temp_dict[os.path.basename(path)]=tempstr

if __name__ == '__main__':
    just_craft=CLOVA_CRAFT()
    daekeun_trocr=Just_TrOCR()
    path="H:/img_sample"

    def process(image_path):
        text_temp=str("")
        model_path = 'weights/craft_mlt_25k.pth'
        net = just_craft.load_craft_model(model_path)
        image = imgproc.loadImage(image_path)


        boxes, polys = just_craft.detect_text_boxes(net, image)
        image = Image.open(image_path)

        for box in boxes:# 한 박스당 한 줄씩 저장 y 값에 따라 줄을 분리 하려면 추가 수정 필요
            cropped_image = image.crop(int(box[0]), int(box[1]),int(box[2]), int(box[3]))
            text_detected=daekeun_trocr.detecting(cropped_image)
            if text_temp!="":
                text_temp+="\n"
            text_temp+=text_detected
        return text_temp

    folder_or_img(path,process)



