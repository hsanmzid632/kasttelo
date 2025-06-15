from rest_framework.decorators import api_view
import pandas as pd
# API pour récupérer ventes et saisonnalité à partir d'une liste de codes articles
@api_view(['POST'])
def article_infos(request):
    """
    Reçoit { "codes": [code1, code2, ...] } et retourne
    { code1: { quantite, collection }, ... }
    """
    codes = set(str(c) for c in request.data.get("codes", []))
    csv_path = os.path.join(settings.BASE_DIR, "outputs", "resultat_filtre.csv")
    df = pd.read_csv(csv_path, dtype=str)
    infos = {}
    for _, row in df.iterrows():
        code = row['article']
        if code in codes and code not in infos:
            infos[code] = {
                "quantite": row['quantite'],
                "collection": row['collection']
            }
    return Response(infos)
# myapp/views.py
import os
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"
from rest_framework.views import APIView
from rest_framework.response import Response
from django.core.files.storage import default_storage
from django.conf import settings
from PIL import Image
import numpy as np
import cv2
import torch
import os
from .embedding_service import EmbeddingService
from .load_models import fclip, swin, device


# 📥 Chargement image
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
    top, bottom = delta_h // 2, delta_h - (delta_h // 2)
    left, right = delta_w // 2, delta_w - (delta_w // 2)
    color = [0, 0, 0]
    new_image = cv2.copyMakeBorder(
        resized, top, bottom, left, right, cv2.BORDER_CONSTANT, value=color
    )
    return new_image


# 🧼 Prétraitements visuels
def preprocess_texture(image):
    enhanced = cv2.detailEnhance(image, sigma_s=15, sigma_r=0.2)
    filtered = cv2.bilateralFilter(enhanced, d=9, sigmaColor=75, sigmaSpace=75)
    return filtered


def preprocess_structure(image):
    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    edges = cv2.Canny(gray, 100, 200)
    return np.stack([edges] * 3, axis=-1)


def preprocess_detail(image):
    kernel_sharpen = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])
    sharpened = cv2.filter2D(image, -1, kernel_sharpen)
    lap = cv2.Laplacian(sharpened, cv2.CV_64F, ksize=3)
    lap = cv2.convertScaleAbs(lap)
    detail_enhanced = cv2.addWeighted(sharpened, 0.8, lap, 0.4, 0)
    return detail_enhanced


def preprocess_shape(image):
    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    thresh = cv2.adaptiveThreshold(
        gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2
    )
    return np.stack([thresh] * 3, axis=-1)


# 🔢 Embeddings
def extract_embedding_with_fclip(image_array):
    image_pil = Image.fromarray(image_array)
    embeddings = fclip.encode_images([image_pil], batch_size=1)
    return embeddings[0]


@torch.no_grad()
def extract_swin_embedding(image_array):
    image_resized = resize_image(image_array, size=224)
    image_resized = image_resized / 255.0
    mean = np.array([0.485, 0.456, 0.406])
    std = np.array([0.229, 0.224, 0.225])
    normalized = (image_resized - mean) / std
    image_tensor = (
        torch.tensor(normalized, dtype=torch.float32)
        .permute(2, 0, 1)
        .unsqueeze(0)
        .to(device)
    )
    features = swin(image_tensor)
    embedding = features.squeeze(0).flatten().cpu().numpy()
    return embedding


# 🔀 Fusion des vecteurs
def extract_combined_features(image):
    image_resized = resize_image(image, size=384)
    fclip_emb = extract_embedding_with_fclip(image_resized)
    s1 = extract_swin_embedding(preprocess_texture(image_resized))
    s2 = extract_swin_embedding(preprocess_structure(image_resized))
    s3 = extract_swin_embedding(preprocess_detail(image_resized))
    s4 = extract_swin_embedding(preprocess_shape(image_resized))
    swin_emb = np.concatenate([s1, s2, s3, s4])
    combined = np.concatenate([fclip_emb, swin_emb])
    return combined


# 🌐 API View
class SearchView(APIView):
    
    def post(self, request):
        embedding_service = EmbeddingService()
        image_file = request.FILES.get("image")
        if not image_file:
            return Response({"error": "Aucune image fournie."}, status=400)

        path = default_storage.save("temp.jpg", image_file)
        full_path = os.path.join(
            settings.MEDIA_ROOT, path
        )  # ou juste path selon config

        try:
            image_np = load_image(full_path)
            embedding = extract_combined_features(image_np)
            embedding = embedding.astype("float32").reshape(1, -1)
            results = embedding_service.search(embedding)
            return Response({"results": results})
        except Exception as e:
            print("Erreur API /api/similar :", e)  # Ajoute ceci
            return Response({"error": str(e)}, status=500)
