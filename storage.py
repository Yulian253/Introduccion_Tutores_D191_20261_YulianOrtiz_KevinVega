import json, os
DB_FILE = "database.json"

def cargar_datos():
    if not os.path.exists(DB_FILE):
        return {"usuarios": [], "tutorias": []}
    with open(DB_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
    if "tutorias" not in data:
        data["tutorias"] = []
    return data

def guardar_datos(data):
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)