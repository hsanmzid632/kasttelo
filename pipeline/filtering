import os

# 📁 Dossier à traiter
folder_path = "pipeline/data/images"

# 📜 Extensions autorisées
valid_exts = [".jpg", ".jpeg", ".png"]

# 🔁 Parcours des fichiers dans le dossier
for filename in os.listdir(folder_path):
    filepath = os.path.join(folder_path, filename)
    
    # Vérifie que c'est bien un fichier
    if os.path.isfile(filepath):
        name, ext = os.path.splitext(filename)
        
        # Condition de conservation
        if ext.lower() in valid_exts and len(name) == 11 and name[7] == "9":
            continue  # Garde le fichier
        else:
            os.remove(filepath)  # Supprime le fichier non conforme
            print(f"Supprimé : {filename}")
