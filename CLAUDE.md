# Claude Code Project Rules

## Language
- 回答は常に日本語で行う
- コードコメントも日本語で書く
- 初心者にも分かる言葉で説明する

## User Level
- ユーザーはPython初心者
- 専門用語は必ず簡単に説明する
- 完成コードを一気に出さず、小さなステップで進める

## Teaching Style
- まず目的を説明する
- 次に設計を説明する
- 次に必要なPython文法を説明する
- その後に少しずつ実装する
- エラーが出たら、原因と修正方法を説明する

## Project
このプロジェクトは犬用シューズ「Fluppi」の在庫管理ツールです。

## Goal
CSVファイルを使って、Fluppiの在庫を管理する。

## CSV Columns
inventory.csv は以下の列を持つ。

- product
- color
- size
- stock

## Features
最終的に以下の機能を作る。

1. 在庫一覧を表示する
2. 在庫を追加する
3. 販売数だけ在庫を減らす
4. 在庫が3個以下なら「再発注が必要です」と表示する
5. CSVに保存する

## Development Rule
最初のゴールは、inventory.csv を読み込んで在庫一覧を表示すること。