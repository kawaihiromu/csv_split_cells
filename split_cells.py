import csv

input_path = "input.csv"
output_path = "output.csv"

rows = []

with open(input_path, "r", encoding="utf-8") as infile:
    reader = csv.reader(infile)
    
    for i, row in enumerate(reader):
        if i == 0:
            # ヘッダー行をスキップ（"ID,Code,Region,Description" など）
            continue

        if not row or not row[0].strip():
            continue  # 空行スキップ

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

# CSV書き出し（BOMなし・CRLF）
with open(output_path, "w", newline="", encoding="utf-8") as csvfile:
    writer = csv.writer(csvfile, lineterminator="\r\n")
    writer.writerow(["ID", "Code", "Region", "Description"])
    writer.writerows(rows)

