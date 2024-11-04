
import pytesseract
from PIL import Image
import cv2
import os
import json
import sys
import numpy as np

def save_json(dict):
    with open( os.path.join(os.getcwd(),'pytesseract_result.json'), 'w+',encoding='utf-8') as json_file:
        json.dump(dict, json_file)


def folder_or_img(path,func):
    count=0
    temp_dict=dict({})

    if os.path.isdir(path):

        img_lst=[f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
        for i in img_lst:
            count += 1
            if count%100==0:
                print(count)
            recognition=func(os.path.join(path,i))
            temp_dict[os.path.basename(i)]=recognition

        save_json(temp_dict)#폴더일 경우 내부 file들 전부를 ocr 텍스트 감지 후 json 저장///  key: file이름 value :감지 텍스트

    else:
        tempstr=str("")
        recognition_lst, confidence_lst=func(path)
        for str_ in recognition_lst:
            tempstr+=str_
        temp_dict[os.path.basename(path)]=tempstr

def detecting_pytesseract(path):
    img=cv2.imread(path, cv2.IMREAD_COLOR)
    text = pytesseract.image_to_string(img, lang='kor')

    return text


if __name__ == '__main__':
    path = 'C:/Users/needa/Downloads/word_images_split'
    #a,b=detection(image_path)
    #print(a,b)
    folder_or_img(path,detecting_pytesseract)
