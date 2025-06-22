
---

# ポスター掲示場データで手動コピーしたものを整形するのに使用したツール

## 概要

このリポジトリでは、北海道の自治体が公開している**ポスター掲示場の一覧PDF**を、
手動でCSVにコピーしたのち、表形式のデータを**CSV形式へ変換・整形する処理**を行っています。

元のPDFでは以下のような制約があります：

- セルの結合が多く、表構造が崩れている
- 自動PDF変換ツールでは**データの欠落や分割ミス**が起こる

そのため、**PDFから目視でコピーし、プレーンテキスト形式のCSVに手動で整形**したうえで、Pythonスクリプトで分割処理を行っています。

> 💡 本ツールは **北海道の市区町村で用いられる地名形式**（例：本町1丁目、若菜8番地 等）を前提にしています。  
> 他地域の形式では正しく分割できない可能性があります。

---

## 入力ファイルについて

- 元のPDFは `sample/original_input/` フォルダに格納してください（参考用）。
- 実際に処理するのは、PDFから手動でコピーした**1列形式のCSVファイル**（`input.csv`）です。

例（input.csv の中身）:

```

1 1-1 社光 旧市立診療所駐車場前付近
2 1-2 本町1丁目 「栄」アパート前バス停付近
...

```

---

## 出力ファイルの形式

整形後の `output.csv` は以下の4列構成になります：

| ID | Code | Region      | Description                       |
|----|------|-------------|------------------------------------|
| 1  | 1-1  | 社光        | 旧市立診療所駐車場前付近           |
| 2  | 1-2  | 本町1丁目   | 「栄」アパート前バス停付近         |

- ファイル形式：**UTF-8（BOMなし）**、**LF改行（Unix形式）**

---

## Pythonスクリプトの実行方法（初心者向け）

### 1. Pythonをインストールする

公式サイトから Python をダウンロード・インストールしてください：

- 👉 https://www.python.org/downloads/

インストール時、「**Add Python to PATH**」にチェックを入れてください。

---

### 2. 必要なファイルを準備

#### 🔹 `input.csv`

PDFからコピーしたデータを、1行ごとに以下のような形式で貼り付けて保存してください：

```

1 1-1 社光 旧市立診療所駐車場前付近
2 1-2 本町1丁目 「栄」アパート前バス停付近
...

````

#### 🔹 `convert_csv.py`

Pythonのスクリプトファイルとして以下の内容を保存してください：

```python
import csv

input_path = "input.csv"
output_path = "output.csv"

rows = []

with open(input_path, "r", encoding="utf-8") as infile:
    reader = csv.reader(infile)
    for i, row in enumerate(reader):
        if i == 0:
            continue  # Skip header
        if not row or not row[0].strip():
            continue
        line = row[0].strip()
        parts = line.split(' ', 2)
        if len(parts) < 3:
            continue
        id_part, code_part, rest = parts
        tokens = rest.split()
        if len(tokens) >= 2 and ("丁目" in tokens[1] or "番地" in tokens[1]):
            region = tokens[0] + tokens[1]
            description = " ".join(tokens[2:])
        else:
            region = tokens[0]
            description = " ".join(tokens[1:])
        rows.append([id_part, code_part, region, description])

with open(output_path, "w", newline="\n", encoding="utf-8") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["ID", "Code", "Region", "Description"])
    writer.writerows(rows)
````

---

### 3. 実行する

#### Windows の場合：

1. `input.csv` と `convert_csv.py` を同じフォルダに置く
2. フォルダを右クリック → 「ターミナルを開く」または「PowerShellを開く」
3. 以下を入力：

```bash
python convert_csv.py
```

#### Mac/Linux の場合：

```bash
python3 convert_csv.py
```

---

### 出力の確認

`output.csv` が生成されていれば成功です。
Excelなどで開いて、データが正しく「ID / コード / 地域名 / 説明」に分かれていればOKです。

---

## 注意点と今後の改善

* 北海道以外の住所表記では、地域名の抽出ルールがうまく機能しない可能性があります。
* 地名と説明の区切りが曖昧な行（例：「川端1」や「滝ノ上」など1語地名）は例外処理が必要です。
* 将来的には、地名辞書などと照合してより高精度な分割を目指せるかもしれません。

---

## ライセンス

MITライセンスです。商用・非商用問わずご自由にお使いください。
ただし、北海道自治体の元データには各所の著作権・利用条件がある場合があるため、別途ご確認ください。

---
