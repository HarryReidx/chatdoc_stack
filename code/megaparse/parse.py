from onnxtr.io import DocumentFile
from onnxtr.models import ocr_predictor, linknet_resnet18, parseq
import cv2
import numpy as np

def resize_and_pad(img, size=1024):
    h, w = img.shape[:2]
    scale = size / max(h, w)
    new_w, new_h = int(w * scale), int(h * scale)
    img_resized = cv2.resize(img, (new_w, new_h))
    pad_img = np.full((size, size, 3), 114, dtype=np.uint8)
    pad_img[(size-new_h)//2:(size-new_h)//2+new_h,
    (size-new_w)//2:(size-new_w)//2+new_w] = img_resized
    return pad_img


# 加载检测和识别模型
det_model = linknet_resnet18("D:\\1-workspace\\6-ai\\0-models\\model.onnx")
reco_model = parseq("D:\\1-workspace\\6-ai\\0-models\\model.onnx", vocab="...")  # 若需要识别模型

ocr = ocr_predictor(det_arch=det_model, reco_arch=reco_model, assume_straight_pages=True)
doc = DocumentFile.from_pdf("黄鑫-清云智通简历.pdf")
res = ocr(doc)
print(res)
