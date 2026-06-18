import csv
import os
from flask import Flask, render_template, request, redirect, url_for, flash

# Flaskアプリを作成する
app = Flask(__name__)
# flash(メッセージ表示)に必要な秘密鍵
app.secret_key = "fluppi-secret"

# app.pyと同じフォルダにあるinventory.csvの絶対パスを取得する
# → どこから実行しても常に正しいファイルを読み込む
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_PATH = os.path.join(BASE_DIR, "inventory.csv")

# CSVを読み込んでリストで返す関数
def load_inventory():
    inventory = []
    with open(CSV_PATH, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            inventory.append(row)
    return inventory

# CSVにリストを保存する関数
def save_inventory(inventory):
    with open(CSV_PATH, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["product", "color", "size", "stock"])
        writer.writeheader()
        writer.writerows(inventory)

# 「/」にアクセスしたとき在庫一覧を表示する
@app.route("/")
def index():
    inventory = load_inventory()

    # UIに使うカラーとサイズの選択肢をCSVから取得する
    all_colors = sorted(set(row["color"] for row in inventory))
    all_sizes  = sorted(set(row["size"]  for row in inventory), key=lambda x: int(x))

    # フィルターパラメータを取得する
    selected_color = request.args.get("color", "")
    selected_sizes = request.args.getlist("size")  # 複数チェックボックスはgetlist
    min_val  = request.args.get("min", "")
    max_val  = request.args.get("max", "")
    reorder  = request.args.get("reorder", "")

    # カラーで絞り込む
    if selected_color:
        inventory = [row for row in inventory if row["color"] == selected_color]

    # サイズで絞り込む(1つ以上チェックされている場合)
    if selected_sizes:
        inventory = [row for row in inventory if row["size"] in selected_sizes]

    # 在庫数で絞り込む
    if reorder:
        inventory = [row for row in inventory if int(row["stock"]) <= 3]
    else:
        if min_val:
            inventory = [row for row in inventory if int(row["stock"]) >= int(min_val)]
        if max_val:
            inventory = [row for row in inventory if int(row["stock"]) <= int(max_val)]

    return render_template("index.html", inventory=inventory,
                           all_colors=all_colors, all_sizes=all_sizes,
                           selected_color=selected_color, selected_sizes=selected_sizes,
                           min_val=min_val, max_val=max_val, reorder=reorder)

# 「/add」にPOSTされたとき在庫を追加する
@app.route("/add", methods=["POST"])
def add():
    # フォームから送られたデータを受け取る
    product = request.form["product"]
    color = request.form["color"]
    size = request.form["size"]
    count = int(request.form["count"])

    inventory = load_inventory()

    # 一致する商品を探して在庫を増やす
    for row in inventory:
        if row["product"] == product and row["color"] == color and row["size"] == size:
            row["stock"] = str(int(row["stock"]) + count)
            save_inventory(inventory)
            flash(f"{product}({color}, サイズ{size})の在庫を{count}個追加しました。")
            return redirect(url_for("index"))

    flash("該当する商品が見つかりませんでした。")
    return redirect(url_for("index"))

# 「/reduce」にPOSTされたとき在庫を減らす
@app.route("/reduce", methods=["POST"])
def reduce():
    product = request.form["product"]
    color = request.form["color"]
    size = request.form["size"]
    count = int(request.form["count"])

    inventory = load_inventory()

    for row in inventory:
        if row["product"] == product and row["color"] == color and row["size"] == size:
            current = int(row["stock"])
            # 在庫より多く引こうとしていないか確認する
            if count > current:
                flash(f"エラー: 在庫({current}個)より多い数は引けません。")
                return redirect(url_for("index"))
            row["stock"] = str(current - count)
            save_inventory(inventory)
            flash(f"{product}({color}, サイズ{size})の在庫を{count}個減らしました。")
            return redirect(url_for("index"))

    flash("該当する商品が見つかりませんでした。")
    return redirect(url_for("index"))

# このファイルを直接実行したときだけサーバーを起動する
if __name__ == "__main__":
    app.run(debug=True)
