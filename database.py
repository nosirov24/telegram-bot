import json
import os


# =====================================================
# SAFE JSON LOADER
# =====================================================

def load_json(file_path, default):

    # Agar file mavjud bo‘lmasa yaratadi
    if not os.path.exists(file_path):
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(default, f, indent=4, ensure_ascii=False)
        return default

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return default


# =====================================================
# SAFE JSON SAVER
# =====================================================

def save_json(file_path, data):

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
