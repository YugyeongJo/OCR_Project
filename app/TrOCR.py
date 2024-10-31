from transformers import TrOCRProcessor, VisionEncoderDecoderModel
from PIL import Image
import requests

# 모델과 프로세서 로드
processor = TrOCRProcessor.from_pretrained("microsoft/trocr-base-handwritten")
model = VisionEncoderDecoderModel.from_pretrained("microsoft/trocr-base-handwritten")

# 이미지 로드
url = "https://example.com/sample_image.png"
image = Image.open(requests.get(url, stream=True).raw).convert("RGB")

# 이미지에서 텍스트 추출
pixel_values = processor(images=image, return_tensors="pt").pixel_values
generated_ids = model.generate(pixel_values)
generated_text = processor.batch_decode(generated_ids, skip_special_tokens=True)[0]

print("Extracted Text:", generated_text)