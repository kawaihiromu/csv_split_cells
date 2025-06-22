import zipfile
import xml.etree.ElementTree as ET
import csv
import os

# 入力ファイル（.kml または .kmz）
input_path = "kml/custom_map.kmz"  # または "kml/custom_map.kml"
csv_path = "kml/output.csv"
temp_kml_path = "kml/_temp_extracted.kml"

# 拡張子チェックして、.kmlファイルとして読み込むパスを決める
if input_path.lower().endswith('.kmz'):
    # KMZファイルを解凍して中のKMLを取り出す
    with zipfile.ZipFile(input_path, 'r') as kmz:
        for file in kmz.namelist():
            if file.endswith('.kml'):
                with open(temp_kml_path, 'wb') as f:
                    f.write(kmz.read(file))
                break
    kml_to_read = temp_kml_path
else:
    # そのままKMLとして使う
    kml_to_read = input_path

# KMLのパース処理
ns = {'kml': 'http://www.opengis.net/kml/2.2'}
tree = ET.parse(kml_to_read)
root = tree.getroot()
placemarks = root.findall('.//kml:Placemark', ns)

with open(csv_path, "w", newline='', encoding="utf-8-sig") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['prefecture', 'city', 'number', 'address', 'name', 'lat', 'long', 'note'])

    for idx, pm in enumerate(placemarks):
        name_elem = pm.find('kml:name', ns)
        name = name_elem.text if name_elem is not None else ''

        desc_elem = pm.find('kml:description', ns)
        desc = desc_elem.text.strip() if desc_elem is not None else ''

        coord_elem = pm.find('.//kml:coordinates', ns)
        coords = coord_elem.text.strip().split(',') if coord_elem is not None else []
        lon, lat = coords[0], coords[1] if len(coords) >= 2 else ('', '')

        prefecture = '北海道'
        city = '網走市'
        number = ''
        address = desc.split('<br>')[0] if '<br>' in desc else desc
        note = desc

        writer.writerow([prefecture, city, number, address, name, lat, lon, note])

# 一時ファイルを削除（kmzのときのみ）
if os.path.exists(temp_kml_path):
    os.remove(temp_kml_path)

print(f"CSV出力完了: {csv_path}")
