#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
kulliyat_search.py - Mevlânâ Hâlid-i Bağdâdî Külliyatı Metin Korpusu Arama Motoru

Kullanım:
    python scripts/kulliyat_search.py "râbıta"
    python scripts/kulliyat_search.py --category hulefa "Seyyid Tâhâ"
    python scripts/kulliyat_search.py --stats
"""

import os
import sys
import argparse
import re

# Ensure safe UTF-8 output on Windows consoles
if hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

CORPUS_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def get_all_markdown_files(root_dir):
    md_files = []
    for root, dirs, files in os.walk(root_dir):
        if '.git' in root:
            continue
        for f in files:
            if f.endswith('.md'):
                md_files.append(os.path.join(root, f))
    return md_files

def search_corpus(query, category=None, ignore_case=True):
    files = get_all_markdown_files(CORPUS_ROOT)
    results = []
    
    flags = re.IGNORECASE if ignore_case else 0
    pattern = re.compile(re.escape(query), flags)

    for file_path in sorted(files):
        rel_path = os.path.relpath(file_path, CORPUS_ROOT)
        
        if category and not rel_path.startswith(category):
            continue

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
        except Exception:
            continue

        file_matches = []
        for line_num, line in enumerate(lines, 1):
            if pattern.search(line):
                file_matches.append((line_num, line.strip()))

        if file_matches:
            results.append((rel_path, file_matches))

    return results

def print_stats():
    files = get_all_markdown_files(CORPUS_ROOT)
    total_lines = 0
    total_words = 0
    total_chars = 0
    file_counts = {}

    for fp in files:
        rel_path = os.path.relpath(fp, CORPUS_ROOT)
        section = rel_path.split(os.sep)[0] if os.sep in rel_path else 'kök'
        file_counts[section] = file_counts.get(section, 0) + 1

        try:
            with open(fp, 'r', encoding='utf-8') as f:
                content = f.read()
                lines = content.splitlines()
                total_lines += len(lines)
                total_words += len(content.split())
                total_chars += len(content)
        except Exception:
            pass

    print("================================================================")
    print("      Mevlânâ Hâlid-i Bağdâdî Külliyatı Metin İstatistikleri     ")
    print("================================================================")
    print(f" Toplam Markdown Dosyası : {len(files)}")
    print(f" Toplam Satır Sayısı     : {total_lines:,}")
    print(f" Toplam Kelime Sayısı    : {total_words:,}")
    print(f" Toplam Karakter Sayısı  : {total_chars:,}")
    print("----------------------------------------------------------------")
    print(" Bölümlere Göre Dosya Dağılımı:")
    for sec, count in sorted(file_counts.items()):
        print(f"   - {sec:<24}: {count} dosya")
    print("================================================================")

def main():
    parser = argparse.ArgumentParser(description="Mevlânâ Hâlid-i Bağdâdî Külliyatı Arama ve İndeksleme Aracı")
    parser.add_argument("query", nargs="?", default="", help="Aranacak kelime veya kavram (örn: râbıta, istikamet, Dehlevî)")
    parser.add_argument("--category", "-c", help="Aramayı sınırlandırmak için dizin (docs, metinler, hulefa, kaynakca)")
    parser.add_argument("--stats", "-s", action="store_true", help="Korpus istatistiklerini gösterir")

    args = parser.parse_args()

    if args.stats:
        print_stats()
        return

    if not args.query:
        parser.print_help()
        sys.exit(1)

    print(f"\n[?] Külliyat içinde arama yapılıyor: '{args.query}'...\n")
    results = search_corpus(args.query, category=args.category)

    if not results:
        print("[-] Eşleşen kayıt bulunamadı.")
        return

    total_hits = sum(len(m[1]) for m in results)
    print(f"[+] Toplam {len(results)} dosyada {total_hits} eşleşme bulundu:\n")

    for rel_path, matches in results:
        print(f"[*] {rel_path} ({len(matches)} eşleşme):")
        for line_num, line_content in matches[:5]:
            print(f"   Satır {line_num:>3}: {line_content}")
        if len(matches) > 5:
            print(f"   ... ve {len(matches) - 5} satır daha")
        print()

if __name__ == "__main__":
    main()
