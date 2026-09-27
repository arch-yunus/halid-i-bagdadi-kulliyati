#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
rabita_index.py - Hâlidiyye Usûl, Râbıta ve Hulefâ Kavram İndeksi Oluşturucu

Kullanım:
    python scripts/rabita_index.py
"""

import os
import sys

# Ensure safe UTF-8 output on Windows consoles
if hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

CORPUS_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

CONCEPTS = {
    "Seyr u Sülûk & Zikir": [
        "Hafî Zikir", "Hatm-i Hâcegân", "Letâif", "Murâkabe", "Nefy ü İsbât", 
        "Hûş der-Dem", "Nazar ber-Kadem", "Halvet der-Encümen", "Vukûf-i Kalbî"
    ],
    "Râbıta & Vesile": [
        "Râbıta", "Mürşid-i Kâmil", "Vesile", "Feyz", "İstimdât", "Muhabbet"
    ],
    "Akâid & Kelâm": [
        "Ehl-i Sünnet", "Kazâ ve Kader", "Kesb", "İrade-i Cüz'iyye", "Cebriyye", "Mu'tezile", "Eş'arî", "Mâtürîdî"
    ],
    "Tarihî Şahsiyetler & Hulefâ": [
        "Şâh Abdullah ed-Dehlevî", "İbn Âbidîn", "Seyyid Tâhâ-i Hakkârî", "Şehâbeddîn Mahmûd el-Âlûsî",
        "İsmâil en-Nârbendî", "Muhammed el-Hânî", "Ahmed el-Ervâdî", "Ahmed Ziyâüddîn Gümüşhânevî"
    ]
}

def generate_index():
    md_files = []
    for root, dirs, files in os.walk(CORPUS_ROOT):
        if '.git' in root:
            continue
        for f in files:
            if f.endswith('.md'):
                md_files.append(os.path.join(root, f))

    index_data = {cat: {c: [] for c in items} for cat, items in CONCEPTS.items()}

    for fp in md_files:
        rel_path = os.path.relpath(fp, CORPUS_ROOT)
        try:
            with open(fp, 'r', encoding='utf-8') as f:
                content = f.read().lower()
        except Exception:
            continue

        for cat, items in CONCEPTS.items():
            for concept in items:
                if concept.lower() in content:
                    index_data[cat][concept].append(rel_path)

    print("================================================================")
    print("      Hâlidiyye Külliyatı Tematik ve Kavramsal Dizin Fihristi    ")
    print("================================================================")
    for cat, items in index_data.items():
        print(f"\n[+] [{cat}]")
        for concept, paths in items.items():
            if paths:
                print(f"  * {concept} ({len(paths)} belgede geçmektedir):")
                for p in sorted(paths)[:4]:
                    print(f"      └── {p}")
                if len(paths) > 4:
                    print(f"      └── ... ve {len(paths)-4} belge daha")
            else:
                print(f"  - {concept}: (Henüz doğrudan eşleşmedi)")
    print("\n================================================================")

if __name__ == "__main__":
    generate_index()
