import csv
import sys

# 出力時の文字コードをUTF-8にする(日本語の文字化け対策)
sys.stdout.reconfigure(encoding="utf-8")

# inventory.csvを開く
with open("inventory.csv", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        print(f"商品: {row['product']}, サイズ: {row['size']}, カラー: {row['color']}, 在庫: {row['stock']}")
