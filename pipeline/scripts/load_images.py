import os
import numpy as np

image_dir = r"C:\\Users\\hsanm\\Desktop\\data\\images"
output_dir = "outputs"
os.makedirs(output_dir, exist_ok=True)

valid_paths = []

for f in os.listdir(image_dir):
    name, ext = os.path.splitext(f)
    if ext.lower() in [".jpg", ".jpeg", ".png"] and len(name) == 11 and name[7] == "9":
        valid_paths.append(os.path.join(image_dir, f))

np.save(os.path.join(output_dir, "paths.npy"), valid_paths)
print(f"✅ {len(valid_paths)} images valides sauvegardées dans outputs/paths.npy")
