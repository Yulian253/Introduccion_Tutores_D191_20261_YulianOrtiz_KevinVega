import json, os
DB_FILE = "database.json"

def cargar_datos():
    if not os.path.exists(DB_FILE):
        return {"usuarios": []}
    with open(DB_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def guardar_datos(data):
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)