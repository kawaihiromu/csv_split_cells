from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import time
import csv

# ヘッドレスChromeの設定
options = Options()
# options.add_argument("--headless")  # GUIを表示しない場合はコメント外す
options.add_argument("--window-size=1920,1080")

# Chromeドライバ起動
driver = webdriver.Chrome(options=options)
url = "https://www.google.com/maps/d/u/0/viewer?mid=1Vlz8hFQcUlOru9g9kFRW38JWbuv8_fk"
driver.get(url)

# ページ読み込み待機
time.sleep(10)

# 🧹 邪魔なUIを非表示にする
js_hide_overlay = """
let overlays = document.querySelectorAll('[aria-label="キーボード ショートカット"], .widget-minimap, .app-viewcard-strip');
overlays.forEach(e => e.style.display = 'none');
"""
driver.execute_script(js_hide_overlay)
time.sleep(1)

# ピンの要素を探す（My Mapsのサイドパネル内のボタン）
items = driver.find_elements(By.TAG_NAME, "button")

print(f"Found {len(items)} points")

data = []

for index, item in enumerate(items):
    try:
        print(f"Clicking item {index}...")
        driver.execute_script("arguments[0].scrollIntoView(true);", item)
        time.sleep(0.5)
        driver.execute_script("arguments[0].click();", item)
        time.sleep(1.5)

        # ピンの詳細から情報取得（適宜クラス名調整）
        title_elem = driver.find_element(By.CLASS_NAME, "qqvbed-ibnC6b")
        desc_elem = driver.find_element(By.CLASS_NAME, "qqvbed-gmcfzf")

        title = title_elem.text.strip()
        desc = desc_elem.text.strip()

        data.append(["北海道", "網走市", str(index + 1), desc, title, "", "", ""])
        print(f"{index + 1}: {title} - {desc}")

    except Exception as e:
        print(f"Error on item {index}: {e}")

driver.quit()

# CSVに保存
with open("my_maps_scraped.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["prefecture", "city", "number", "address", "name", "lat", "long", "note"])
    writer.writerows(data)

print("CSV出力完了: my_maps_scraped.csv")
