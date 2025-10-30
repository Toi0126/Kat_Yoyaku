# -*- coding: utf-8 -*-
"""
Kat_Yoyaku / test.py
Mac / Windows 両対応版
ChromeDriverManager を安全に扱う設定込み
"""

import os
import time
import json
import datetime
import hashlib
import requests
import numpy as np
import cv2
import boto3
from botocore.exceptions import NoCredentialsError
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.utils import ChromeType
import platform

# ==============================
# 定数定義
# ==============================
BUCKET_NAME = "line-bot-images-bucket"
LINE_API_URL = "https://api.line.me/v2/bot/message/push"
ACCESS_TOKEN = "33wOmQjQIFVbl/ng40GTPq8f1SgxG75mayOpG8j90AEzyUkbXGcewkG+WO0SKxCpUMes1fo0K3TlW5VgDR4jwaqhBiWGMOEoKWCqbpluAIky1OyP1yoXFCo7QDe7/mAWe1rNowbhAGMfWsV/eAlHMwdB04t89/1O/w1cDnyilFU="
USER_ID = "U852b7b0dff51e24b81bb171b589b1a7b"
HEADERS = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {ACCESS_TOKEN}",
}
IMAGE_DIR = "image"
JST = datetime.timezone(datetime.timedelta(hours=9), "JST")


# ==============================
# ユーティリティ関数
# ==============================
def hash_file(path: str) -> str:
    """ファイルのMD5ハッシュを計算"""
    with open(path, "rb") as f:
        hasher = hashlib.md5()
        hasher.update(f.read())
        return hasher.hexdigest()


def upload_image_to_s3(local_image_path: str, bucket_name: str, object_name: str) -> str | None:
    """画像をAWS S3にアップロード"""
    s3 = boto3.client("s3")
    try:
        s3.upload_file(local_image_path, bucket_name, object_name, ExtraArgs={"ACL": "public-read"})
        return f"https://{bucket_name}.s3.ap-southeast-2.amazonaws.com/{object_name}"
    except FileNotFoundError:
        print(f"ファイルが見つかりません: {local_image_path}")
    except NoCredentialsError:
        print("認証情報が見つかりません。")
    return None


def send_line_notify(message: str, image_url: str | None = None) -> None:
    """LINEに通知を送信"""
    data = {"to": USER_ID, "messages": [{"type": "text", "text": message}]}
    if image_url:
        data["messages"] = [
            {"type": "image", "originalContentUrl": image_url, "previewImageUrl": image_url}
        ]
    response = requests.post(LINE_API_URL, headers=HEADERS, data=json.dumps(data))
    if response.status_code == 200:
        print("メッセージが送信されました！")
    else:
        print(f"エラー: {response.status_code}, {response.text}")


# ==============================
# WebDriver 初期化（Mac / Win 両対応）
# ==============================
def initialize_driver() -> webdriver.Chrome:
    """ヘッドレスモードでWebDriverを初期化（Mac / Win対応）"""

    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")  # Chrome >=109用のヘッドレスモード
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")

    # WindowsとMacでキャッシュパスを分ける（権限エラー防止）
    if platform.system() == "Windows":
        cache_path = os.path.join(os.getenv("LOCALAPPDATA", ""), "wdm_cache")
    else:
        cache_path = os.path.expanduser("~/.wdm_cache")

    os.makedirs(cache_path, exist_ok=True)
    driver_path = ChromeDriverManager(
        path=cache_path, chrome_type=ChromeType.GOOGLE
    ).install()

    service = ChromeService(driver_path)
    driver = webdriver.Chrome(service=service, options=options)
    return driver


# ==============================
# 画像比較処理
# ==============================
def capture_and_compare(driver, xpath, old_file, new_file, message):
    """スクリーンショットを撮影し、比較してLINE通知を送信"""
    element = driver.find_element(By.XPATH, xpath)
    element.click()
    time.sleep(4)

    old_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), old_file)
    new_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), new_file)

    old_image = cv2.imread(old_path) if os.path.exists(old_path) else None
    driver.save_screenshot(new_path)
    new_image = cv2.imread(new_path)

    if old_image is None or not np.array_equal(old_image, new_image):
        print("画像が変更されました。LINE通知を送信します。")
        send_line_notify(message, new_path)
    else:
        print("画像に変更はありません。")


# ==============================
# 施設ごとの確認
# ==============================
def check_availability():
    """空き情報を確認する"""
    driver = initialize_driver()
    driver.get("https://rsv.shisetsu.city.katsushika.lg.jp/katsushika/web/menu.jsp")
    time.sleep(4)
    driver.maximize_window()
    time.sleep(4)

    capture_and_compare(
        driver,
        '//*[@id="disp"]/center/form/table[3]/tbody/tr[1]/td/table/tbody/tr[2]/td[1]/table/tbody/tr[2]/td/a/img',
        "image/01.png",
        "image/06.png",
        "荒川河川敷 荒川小菅",
    )

    capture_and_compare(
        driver,
        '//*[@id="selectBldCd"]/option[3]',
        "image/03.png",
        "image/08.png",
        "荒川河川敷 四つ木橋",
    )

    capture_and_compare(
        driver,
        '//*[@id="selectBldCd"]/option[7]',
        "image/02.png",
        "image/07.png",
        "東新小岩野球",
    )

    capture_and_compare(
        driver,
        '//*[@id="selectBldCd"]/option[5]',
        "image/04.png",
        "image/09.png",
        "江戸川河川敷 柴又",
    )

    capture_and_compare(
        driver,
        '//*[@id="selectBldCd"]/option[6]',
        "image/05.png",
        "image/010.png",
        "江戸川河川敷 第二柴又",
    )

    driver.quit()


# ==============================
# メインループ
# ==============================
def main():
    while True:
        now = datetime.datetime.now(JST)
        if 6 <= now.hour < 24:
            print("空き情報を確認します...")
            check_availability()
        time.sleep(120)


if __name__ == "__main__":
    main()
