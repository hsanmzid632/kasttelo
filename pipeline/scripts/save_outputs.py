import os
import numpy as np
import faiss

backend_dir = os.path.join("..", "backend", "outputs")
os.makedirs(backend_dir, exist_ok=True)

embeddings = np.load("outputs/embeddings.npy")
paths = np.load("outputs/paths.npy")
index = faiss.read_index("outputs/faiss.index")

np.save(os.path.join(backend_dir, "embeddings.npy"), embeddings)
np.save(os.path.join(backend_dir, "paths.npy"), paths)
faiss.write_index(index, os.path.join(backend_dir, "faiss.index"))

print(f"✅ Fichiers enregistrés dans {backend_dir}")
