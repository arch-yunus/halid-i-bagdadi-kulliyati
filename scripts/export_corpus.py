#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
export_corpus.py - Mevlânâ Hâlid-i Bağdâdî Külliyatı Dışa Aktarma ve Doğrulama Aracı

Kullanım:
    python scripts/export_corpus.py --output data/corpus_bundle.json
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

def export_bundle(output_file):
    bundle = {
        "metadata": {
            "title": "Mevlânâ Hâlid-i Bağdâdî Külliyatı Metin Korpusu",
            "author": "Mevlânâ Ziyâüddîn Hâlid-i Bağdâdî (1779-1827)",
            "license": "MIT",
            "version": "2.0.0"
        },
        "documents": []
    }

    for root, dirs, files in os.walk(CORPUS_ROOT):
        if '.git' in root:
            continue
        for f in sorted(files):
            if f.endswith('.md'):
                full_path = os.path.join(root, f)
                rel_path = os.path.relpath(full_path, CORPUS_ROOT)
                try:
                    with open(full_path, 'r', encoding='utf-8') as fh:
                        content = fh.read()
                    bundle["documents"].append({
                        "path": rel_path.replace("\\", "/"),
                        "filename": f,
                        "line_count": len(content.splitlines()),
                        "word_count": len(content.split()),
                        "content": content
                    })
                except Exception as e:
                    print(f"[-] Hata: {rel_path} okunamadı: {e}")

    out_path = os.path.join(CORPUS_ROOT, output_file)
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, 'w', encoding='utf-8') as out_f:
        json.dump(bundle, out_f, ensure_ascii=False, indent=2)

    print(f"[+] Başarılı: {len(bundle['documents'])} belge '{output_file}' dosyasına aktarıldı.")
    return len(bundle['documents'])

def main():
    parser = argparse.ArgumentParser(description="Külliyatı JSON formatında birleştirip dışa aktarır.")
    parser.add_argument("--output", "-o", default="data/corpus_bundle.json", help="Çıktı JSON dosya yolu")
    args = parser.parse_args()

    export_bundle(args.output)

if __name__ == "__main__":
    main()
