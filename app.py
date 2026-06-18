import csv
from flask import Flask, render_template, request, redirect, url_for, flash

# Flaskアプリを作成する
app = Flask(__name__)
# flash(メッセージ表示)に必要な秘密鍵
app.secret_key = "fluppi-secret"

# CSVを読み込んでリストで返す関数
def load_inventory():
    inventory = []
    with open("inventory.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            inventory.append(row)
    return inventory

# CSVにリストを保存する関数
def save_inventory(inventory):
    with open("inventory.csv", "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["product", "color", "size", "stock"])
        writer.writeheader()
        writer.writerows(inventory)

# 「/」にアクセスしたとき在庫一覧を表示する
@app.route("/")
def index():
    inventory = load_inventory()
    # 検索キーワードをURLパラメータから取得する(なければ空文字)
    query = request.args.get("q", "")
    if query:
        # 商品名またはカラーにキーワードが含まれる行だけ残す
        inventory = [row for row in inventory
                     if query in row["product"] or query in row["color"]]
    return render_template("index.html", inventory=inventory, query=query)

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
