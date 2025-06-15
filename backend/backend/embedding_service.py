import os
import numpy as np
import faiss
from django.conf import settings
from sklearn.metrics.pairwise import cosine_similarity


class EmbeddingService:
    def __init__(self):
        outputs_dir = os.path.join(settings.BASE_DIR, "outputs")
        embeddings_path = os.path.join(outputs_dir, "embeddings.npy")
        paths_path = os.path.join(outputs_dir, "paths.npy")
        index_path = os.path.join(outputs_dir, "faiss.index")

        if os.path.exists(embeddings_path):
            self.embeddings = np.load(embeddings_path)
        else:
            self.embeddings = None
            print(f"[WARNING] {embeddings_path} not found. Embeddings not loaded.")

        if os.path.exists(paths_path):
            self.paths = np.load(paths_path)
        else:
            self.paths = None
            print(f"[WARNING] {paths_path} not found. Paths not loaded.")

        if os.path.exists(index_path):
            self.index = faiss.read_index(index_path)
        else:
            self.index = None
            print(f"[WARNING] {index_path} not found. FAISS index not loaded.")



    def search(self, query_vector, top_k=10):
        if self.index is None or self.paths is None or self.embeddings is None:
            raise ValueError("FAISS index, paths or embeddings not loaded.")
        # Normalise le query comme lors du build
        query = query_vector.reshape(1, -1)
        faiss.normalize_L2(query)
        distances, indices = self.index.search(query, top_k)
        # Calcule la vraie cosine similarity
        sims = cosine_similarity(query, self.embeddings[indices[0]])[0]
        results = []
        for idx, i in enumerate(indices[0]):
            abs_path = str(self.paths[i])
            rel_path = os.path.relpath(abs_path, settings.EXTRA_IMAGE_DIR)
            url_path = f"images/{rel_path.replace(os.sep, '/')}"
            # Correction: code_article = nom de fichier sans les 3 premiers caractères
            filename = os.path.splitext(os.path.basename(abs_path))[0]
            if len(filename) > 3:
                code_article = filename[3:]
            else:
                code_article = filename
            # Vérifie si le fichier image existe réellement
            full_image_path = os.path.join(settings.EXTRA_IMAGE_DIR, rel_path)
            if not os.path.exists(full_image_path):
                url_path = None
            results.append({
                "path": url_path,
                "distance": float(sims[idx]),  # c'est la vraie cosine similarity [-1, 1]
                "code_article": code_article
            })
        results.sort(key=lambda x: x["distance"], reverse=True)
        return results