import os
import cv2
import torch
import timm
import numpy as np
from PIL import Image
from fashion_clip.fashion_clip import FashionCLIP

device = "cuda" if torch.cuda.is_available() else "cpu"
fclip = FashionCLIP("fashion-clip")
swin = (
    timm.create_model("swin_base_patch4_window7_224", pretrained=True, num_classes=0)
    .to(device)
    .eval()
)


def load_image(image_path):
    image = Image.open(image_path).convert("RGB")
    return np.array(image)


def resize_image(image_array, size=224):
    h, w = image_array.shape[:2]
    scale = size / max(h, w)
    new_w, new_h = int(w * scale), int(h * scale)
    resized = cv2.resize(image_array, (new_w, new_h))
    delta_w = size - new_w
    delta_h = size - new_h
    top, bottom = delta_h // 2, delta_h - delta_h // 2
    left, right = delta_w // 2, delta_w - delta_w // 2
    new_image = cv2.copyMakeBorder(
        resized, top, bottom, left, right, cv2.BORDER_CONSTANT, value=[0, 0, 0]
    )
    return new_image


def preprocess_texture(image):
    enhanced = cv2.detailEnhance(image, sigma_s=15, sigma_r=0.2)
    return cv2.bilateralFilter(enhanced, 9, 75, 75)


def preprocess_structure(image):
    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    edges = cv2.Canny(gray, 100, 200)
    return np.stack([edges] * 3, axis=-1)


def preprocess_detail(image):
    sharpened = cv2.filter2D(image, -1, np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]]))
    lap = cv2.Laplacian(sharpened, cv2.CV_64F)
    lap = cv2.convertScaleAbs(lap)
    return cv2.addWeighted(sharpened, 0.8, lap, 0.4, 0)


def preprocess_shape(image):
    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    thresh = cv2.adaptiveThreshold(
        gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2
    )
    return np.stack([thresh] * 3, axis=-1)


def extract_embedding_with_fclip(image_array):
    image_pil = Image.fromarray(image_array)
    return fclip.encode_images([image_pil])[0]


@torch.no_grad()
def extract_swin_embedding(image_array):
    resized = resize_image(image_array, 224)
    img = resized / 255.0
    img = (img - [0.485, 0.456, 0.406]) / [0.229, 0.224, 0.225]
    tensor = (
        torch.tensor(img, dtype=torch.float32).permute(2, 0, 1).unsqueeze(0).to(device)
    )
    features = swin(tensor)
    return features.squeeze().cpu().numpy().flatten()


def extract_combined_features(image):
    img_resized = resize_image(image, size=384)
    fclip_emb = extract_embedding_with_fclip(img_resized)
    s1 = extract_swin_embedding(preprocess_texture(img_resized))
    s2 = extract_swin_embedding(preprocess_structure(img_resized))
    s3 = extract_swin_embedding(preprocess_detail(img_resized))
    s4 = extract_swin_embedding(preprocess_shape(img_resized))
    return np.concatenate([fclip_emb, s1, s2, s3, s4])
