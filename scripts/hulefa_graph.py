#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
hulefa_graph.py - Hâlidiyye Halifeler Ağı Görselleştirici ve GeoJSON Üretici

Kullanım:
    python scripts/hulefa_graph.py --mermaid
    python scripts/hulefa_graph.py --geojson data/hulefa_map.geojson
"""

import os
import sys
import json
import argparse

if hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

CORPUS_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def load_hulefa_data():
    json_path = os.path.join(CORPUS_ROOT, "data", "hulefa_network.json")
    with open(json_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def generate_mermaid():
    data = load_hulefa_data()
    print("```mermaid")
    print("flowchart TD")
    print("    DEH[\"Şâh Abdullah ed-Dehlevî (Delhi)\"] --> MHB[\"Mevlânâ Hâlid-i Bağdâdî (Şam/Bağdat)\"]")
    
    for item in data:
        if item["id"] == "mevlana_halid":
            continue
        lineage = item["lineage_from"]
        parent_id = "MHB"
        if "Ahmed el-Ervâdî" in lineage:
            parent_id = "ahmed_ervadi"
        elif "Seyyid Tâhâ" in lineage:
            parent_id = "seyyid_taha"
        elif "Seyyid Sıbgatullah" in lineage:
            parent_id = "sibgatullah_arvasi"

        node_id = item["id"]
        node_label = f"{item['name']} ({item['center']})"
        print(f"    {parent_id} --> {node_id}[\"{node_label}\"]")
    print("```")

def generate_geojson(out_file):
    data = load_hulefa_data()
    geojson = {
        "type": "FeatureCollection",
        "features": []
    }

    for item in data:
        feature = {
            "type": "Feature",
            "properties": {
                "id": item["id"],
                "name": item["name"],
                "death_year": item["death_year"],
                "center": item["center"],
                "role": item["role"],
                "region": item["region"]
            },
            "geometry": {
                "type": "Point",
                "coordinates": [item["coordinates"][1], item["coordinates"][0]] # [lng, lat]
            }
        }
        geojson["features"].append(feature)

    out_path = os.path.join(CORPUS_ROOT, out_file)
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(geojson, f, ensure_ascii=False, indent=2)

    print(f"[+] GeoJSON başarıyla üretildi: {out_file}")

def main():
    parser = argparse.ArgumentParser(description="Hâlidiyye ağ diyagramı ve harita üretici.")
    parser.add_argument("--mermaid", action="store_true", help="Mermaid akış şemasını ekrana basar")
    parser.add_argument("--geojson", default="data/hulefa_map.geojson", help="GeoJSON harita dosya yolu")
    args = parser.parse_args()

    if args.mermaid:
        generate_mermaid()
    else:
        generate_geojson(args.geojson)

if __name__ == "__main__":
    main()
