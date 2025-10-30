# test.py


# pip3 uninstall webdriver-manager
# pip3 install webdriver-manager
import time
import datetime
import requests
import os
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
import hashlib
import json
import cv2
import numpy as np
import boto3
from botocore.exceptions import NoCredentialsError

# 定数定義
BUCKET_NAME = "line-bot-images-bucket"
LINE_API_URL = 'https://api.line.me/v2/bot/message/push'
ACCESS_TOKEN = '33wOmQjQIFVbl/ng40GTPq8f1SgxG75mayOpG8j90AEzyUkbXGcewkG+WO0SKxCpUMes1fo0K3TlW5VgDR4jwaqhBiWGMOEoKWCqbpluAIky1OyP1yoXFCo7QDe7/mAWe1rNowbhAGMfWsV/eAlHMwdB04t89/1O/w1cDnyilFU='
USER_ID = 'U852b7b0dff51e24b81bb171b589b1a7b'
HEADERS = {
    'Content-Type': 'application/json',
    'Authorization': f'Bearer {ACCESS_TOKEN}'
}
IMAGE_DIR = "image"
JST = datetime.timezone(datetime.timedelta(hours=9), 'JST')

# ユーティリティ関数
def hash_file(path):
    """ファイルのMD5ハッシュを計算"""
    with open(path, 'rb') as f:
        hasher = hashlib.md5()
        hasher.update(f.read())
        return hasher.hexdigest()

def upload_image_to_s3(local_image_path, bucket_name, object_name):
    """画像をAWS S3にアップロード"""
    s3 = boto3.client('s3')
    try:
        s3.upload_file(local_image_path, bucket_name, object_name, ExtraArgs={'ACL': 'public-read'})
        return f"https://{bucket_name}.s3.ap-southeast-2.amazonaws.com/{object_name}"
    except FileNotFoundError:
        print(f"ファイルが見つかりません: {local_image_path}")
    except NoCredentialsError:
        print("認証情報が見つかりません。")
    return None

def send_line_notify(message, image_url=None):
    """LINEに通知を送信"""
    data = {
        "to": USER_ID,
        "messages": [{"type": "text", "text": message}]
    }
    if image_url:
        data["messages"] = [{"type": "image", "originalContentUrl": image_url, "previewImageUrl": image_url}]
    response = requests.post(LINE_API_URL, headers=HEADERS, data=json.dumps(data))
    if response.status_code == 200:
        print('メッセージが送信されました！')
    else:
        print(f'エラー: {response.status_code}, {response.text}')

def initialize_driver():
    """ヘッドレスモードでWebDriverを初期化"""
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    return webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)

def capture_and_compare(driver, xpath, old_file, new_file, message):
    """スクリーンショットを撮影し、比較してLINE通知を送信"""
    element = driver.find_element(By.XPATH, xpath)
    element.click()
    time.sleep(4)

    old_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), old_file)
    new_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), new_file)

    if os.path.exists(old_path):
        old_image = cv2.imread(old_path)
    else:
        old_image = None

    driver.save_screenshot(new_path)
    new_image = cv2.imread(new_path)

    if old_image is None or not np.array_equal(old_image, new_image):
        print("画像が変更されました。LINE通知を送信します。")
        send_line_notify(message, new_path)
    else:
        print("画像に変更はありません。")

def check_availability():
    """空き情報を確認する"""
    driver = initialize_driver()
    driver.get('https://rsv.shisetsu.city.katsushika.lg.jp/katsushika/web/menu.jsp')
    time.sleep(4)
    driver.maximize_window()
    time.sleep(4)

    # 各施設の確認
    capture_and_compare(driver, '//*[@id="disp"]/center/form/table[3]/tbody/tr[1]/td/table/tbody/tr[2]/td[1]/table/tbody/tr[2]/td/a/img',
                        "image/01.png", "image/06.png", "荒川河川敷 荒川小菅")

    capture_and_compare(driver, '//*[@id="selectBldCd"]/option[3]',
                        "image/03.png", "image/08.png", "荒川河川敷 四つ木橋")

    capture_and_compare(driver, '//*[@id="selectBldCd"]/option[7]',
                        "image/02.png", "image/07.png", "東新小岩野球")

    capture_and_compare(driver, '//*[@id="selectBldCd"]/option[5]',
                        "image/04.png", "image/09.png", "江戸川河川敷 柴又")

    capture_and_compare(driver, '//*[@id="selectBldCd"]/option[6]',
                        "image/05.png", "image/010.png", "江戸川河川敷 第二柴又")

    driver.quit()

def main():
    while True:
        now = datetime.datetime.now(JST)
        if 6 <= now.hour < 24:
            print("空き情報を確認します...")
            check_availability()
        time.sleep(120)

if __name__ == "__main__":
    main()