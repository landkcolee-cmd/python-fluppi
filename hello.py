print("Hello Python!")
print("Hello Claude Code!")

# 名前を受け取って、挨拶のメッセージを作って返す関数
def greet(name):
    return f"こんにちは、{name}さん!"

# 関数を呼び出して、結果を表示する
message = greet("ランド")
print(message)

# 今の在庫数と、追加する数を受け取って、新しい在庫数を返す関数
def add_stock(current_stock, add_count):
    return current_stock + add_count

# 関数を呼び出して、結果を表示する
new_stock = add_stock(5, 3)
print(f"新しい在庫数: {new_stock}")

# ユーザーから名前を入力してもらう
name = input("あなたの名前を入力してください: ")
# greet関数で挨拶する
print(greet(name))

# 今の在庫数と追加する数を入力してもらう
current = int(input("今の在庫数を入力してください: "))
add = int(input("追加する数を入力してください: "))
# add_stock関数で計算して結果を表示する
result = add_stock(current, add)
print(f"新しい在庫数: {result}")