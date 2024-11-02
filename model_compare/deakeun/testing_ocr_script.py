from paddleocr import PaddleOCR
from PIL import Image
import numpy as np
import json
import os

# json 파일로 저장
def save_json(dict):
    with open( os.path.join(os.getcwd(),'paddle_result.json'), 'w+',encoding='utf-8') as json_file:
        json.dump(dict, json_file)


def folder_or_img(path,func):
    temp_dict=dict({})

    if os.path.isdir(path):

        img_lst=[f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
        for i in img_lst:
            tempstr=str("")
            recognition_lst, confidence_lst=func(os.path.join(path,i))
            for str_ in recognition_lst:
                if tempstr!="":
                    tempstr+="\n"
                tempstr+=str_
            temp_dict[os.path.basename(i)]=tempstr

        save_json(temp_dict)#폴더일 경우 내부 file들 전부를 ocr 텍스트 감지 후 json 저장///  key: file이름 value :감지 텍스트

    else:
        tempstr=str("")
        recognition_lst, confidence_lst=func(path)
        for str_ in recognition_lst:
            tempstr+=str_
        temp_dict[os.path.basename(path)]=tempstr




def detection(image_path):
    recognition_lst=[]
    confidence_lst=[]
    # PaddleOCR 인스턴스 생성
    ocr = PaddleOCR(use_angle_cls=True, lang='korean')

    # 이미지 열기 및 PIL 이미지로 변환
    image = Image.open(image_path).convert('RGB')

    # PIL 이미지를 NumPy 배열로 변환
    image_np = np.array(image)

    # 텍스트 인식 (NumPy 배열로 전달)
    result = ocr.ocr(image_np, det=False, cls=True)
    for i in result[0]:
        #print(f'인식결과// {i[0]}')
        #print(f'confidence// {i[1]}')
        recognition_lst.append(i[0])
        confidence_lst.append(i[1])
    assert len(recognition_lst) == len(confidence_lst)
    return recognition_lst, confidence_lst


if __name__ == '__main__':
    path = 'F:/abc/img_folder'
    #a,b=detection(image_path)
    #print(a,b)
    folder_or_img(path,detection)