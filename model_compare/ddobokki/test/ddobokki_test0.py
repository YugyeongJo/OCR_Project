import os
import torch
from transformers import pipeline
from transformers import AutoTokenizer, AutoModel
from transformers import TrOCRProcessor, VisionEncoderDecoderModel, AutoTokenizer
from io import BytesIO
from PIL import Image

# Use a pipeline as a high-level helper
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

pipe = pipeline("image-to-text", model="ddobokki/ko-trocr", device=device)

processor = TrOCRProcessor.from_pretrained("ddobokki/ko-trocr") 
model = VisionEncoderDecoderModel.from_pretrained("ddobokki/ko-trocr")
tokenizer = AutoTokenizer.from_pretrained("ddobokki/ko-trocr")

image_folder_path = "C:/Users/user/Desktop/SeSAC_DATA_AI/Medium_Project/TROCR/TROCR_DJ/data"

# 이미지 파일 목록 생성
image_files = [os.path.join(image_folder_path, f) for f in os.listdir(image_folder_path) if f.endswith(('.png', '.jpg', '.jpeg'))]
    

# 각 이미지에 대해 OCR 수행
for image_path in image_files:
    # 이미지 열기
    image = Image.open(image_path).convert("RGB") # Chang: add .convert("RGB")
    f_name = image_path.split('/')[-1]
    f_name = f_name.split('.')[0]
    
    # 이미지로 OCR 수행
    pixel_values = processor(images=image, return_tensors="pt").pixel_values
    generated_ids = model.generate(pixel_values)
    generated_text = processor.batch_decode(generated_ids, skip_special_tokens=True)[0]
    
    with open(f"result/{f_name}_output.txt", "w+", encoding="utf-8") as file:
        result = generated_text # + '\n' + combined_word
        file.write(result)

    print("===============")