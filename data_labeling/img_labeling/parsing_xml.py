import xml.etree.ElementTree as ET
import os


file_path = 'H:/temp/Preliminary_cheese_gratin_taste_2.xml'#파싱할 xml 파일 경로
file_name = os.path.basename(file_path)
tree = ET.parse(file_path)
root = tree.getroot()


filename = root.find('filename').text
width = int(root.find('size/width').text)
height = int(root.find('size/height').text)
depth = int(root.find('size/depth').text)

rough_or_detail="detailed"
print(f"File: {filename}")
print(f"Image Dimensions: {width}x{height}, Depth: {depth}")
# with open(f'H:/2/rough/{file_name}.txt', 'a', encoding="utf-8") as file:
#     pass

for obj in root.findall('object'):
    box_name = obj.find('name').text
    xmin = int(obj.find('bndbox/xmin').text)
    ymin = int(obj.find('bndbox/ymin').text)
    xmax = int(obj.find('bndbox/xmax').text)
    ymax = int(obj.find('bndbox/ymax').text)

    print(f"Box Name: {box_name}")
    print(f"Coordinates: ({xmin},{xmax} ,{ymin} ,{ymax})")


    output_folder_path='H:/2/detailed'#저장하고 싶은 파싱 폴더


    with open(f'{output_folder_path}/{file_name}.txt', 'a+', encoding="utf-8") as file:
        file.write(f"{box_name}:[{xmin} {xmax} {ymin} {ymax}]\n")
    print("-" * 30)
