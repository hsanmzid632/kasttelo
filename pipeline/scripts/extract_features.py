import os
import numpy as np
import torch
from tqdm import tqdm
from scripts.utils import load_image, extract_combined_features

device = "cuda" if torch.cuda.is_available() else "cpu"

paths = np.load("outputs/paths.npy", allow_pickle=True)
embeddings = []

for path in tqdm(paths):
    try:
        img = load_image(path)
        emb = extract_combined_features(img)
        embeddings.append(emb)
        torch.cuda.empty_cache()
    except Exception as e:
        print(f"Erreur avec {path}: {e}")

embeddings = np.vstack(embeddings).astype("float32")
np.save("outputs/embeddings.npy", embeddings)
print("✅ Embeddings sauvegardés dans outputs/embeddings.npy")
