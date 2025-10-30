# pytest用テストファイル
import pytest
from kat_yoyaku.kat_yoyaku import scrape

def test_scrape():
    # テストケースの例
    try:
        scrape()
        assert True  # エラーが発生しなければ成功
    except Exception as e:
        pytest.fail(f"スクレイピング中にエラーが発生しました: {e}")