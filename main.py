import csv
import sys

# 出力時の文字コードをUTF-8にする(日本語の文字化け対策)
sys.stdout.reconfigure(encoding="utf-8")

# 在庫一覧を表示する関数
def show_inventory(inventory):
    print("--- 在庫一覧 ---")
    for row in inventory:
        print(f"商品: {row['product']}, サイズ: {row['size']}, カラー: {row['color']}, 在庫: {row['stock']}")
        # 在庫が3個以下なら警告を表示する
        if int(row['stock']) <= 3:
            print("  ⚠ 再発注が必要です")

# 在庫を追加する関数
def add_to_stock(inventory):
    product = input("商品名を入力してください: ")
    color = input("カラーを入力してください: ")
    size = input("サイズを入力してください: ")
    add_count = int(input("追加する数を入力してください: "))

    for row in inventory:
        # 商品名・カラー・サイズがすべて一致する行を探す
        if row['product'] == product and row['color'] == color and row['size'] == size:
            row['stock'] = str(int(row['stock']) + add_count)
            print(f"{product}({color}, サイズ{size})の在庫を{add_count}個追加しました。")
            return

    print("該当する商品が見つかりませんでした。")

# inventory.csvを読み込んで、リストに保存する
inventory = []
with open("inventory.csv", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        inventory.append(row)

# 販売数だけ在庫を減らす関数
def reduce_stock(inventory):
    product = input("商品名を入力してください: ")
    color = input("カラーを入力してください: ")
    size = input("サイズを入力してください: ")
    sold_count = int(input("販売した数を入力してください: "))

    for row in inventory:
        # 商品名・カラー・サイズがすべて一致する行を探す
        if row['product'] == product and row['color'] == color and row['size'] == size:
            current = int(row['stock'])
            # 在庫より多く引こうとしていないか確認する
            if sold_count > current:
                print(f"エラー: 在庫({current}個)より多い数は引けません。")
                return
            row['stock'] = str(current - sold_count)
            print(f"{product}({color}, サイズ{size})の在庫を{sold_count}個減らしました。")
            return

    print("該当する商品が見つかりませんでした。")

# CSVファイルに在庫データを保存する関数
def save_to_csv(inventory):
    with open("inventory.csv", "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["product", "color", "size", "stock"])
        writer.writeheader()
        writer.writerows(inventory)
    print("CSVに保存しました。")

# 操作前の在庫一覧を表示する
show_inventory(inventory)

# 在庫を減らす
reduce_stock(inventory)

# 操作後の在庫一覧を表示する
show_inventory(inventory)

# CSVに保存する
save_to_csv(inventory)
