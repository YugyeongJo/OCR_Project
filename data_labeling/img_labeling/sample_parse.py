import re
import os
import json


def save_json(dict_,path,file_name):
    if not os.path.isdir(os.path.join(path,"parsed_json")):
        os.mkdir(os.path.join(path,"parsed_json"))
    with open(f'{path}/parsed_json/{file_name}.json','w+',encoding='utf-8') as j:
        json.dump(dict_,j)
def save_dict_to_text(dict_,path,file_name):
    if not os.path.isdir(os.path.join(path,"ground_truth")):
        os.mkdir(os.path.join(path,"ground_truth"))
    with open(f'{path}/ground_truth/{file_name}','w+',encoding='utf-8') as j:
        temp_str=""
        for x,y in dict_.items():
            xmin,xmax,ymin,ymax=y[0][0],y[0][1],y[0][2],y[0][3]
            temp_str+=f'{xmin} {ymin} {xmin} {ymax} {xmax} {ymin} {xmax} {ymax}##::{y[1]}\n'
        j.write(temp_str)



def parsing(text):
    pattern = r'box_(\d+):\[(\d+ \d+ \d+ \d+),([^\]]+)\]'

    box_dict = {}
    for match in re.finditer(pattern, text):
        box_number = f"box_{match.group(1)}"
        coordinates = list(map(int, match.group(2).split()))
        label = match.group(3)
        box_dict[box_number] =[coordinates, label]

    return box_dict



if __name__=="__main__":
    path="C:/develops/OCR_Project/data_labeling/img_labeling/3/detail"#test 라벨링 완료된 특정 folder를 기입하면 해당 경로에 json 폴더와 txt 폴더를 만듭니다.
    if os.path.isdir(path):
        dir_list=os.listdir(path)
        file_list=[i  for i in dir_list if os.path.isfile(os.path.join(path,i))]
        for file in file_list:
            with open (os.path.join(path,file),'r',encoding='utf-8') as f:
                text=f.read()
            dict_=parsing(text)
            save_json(dict_,path,file)
            save_dict_to_text(dict_, path, file)
