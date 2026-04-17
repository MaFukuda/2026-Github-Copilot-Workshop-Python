"""
バックエンドテスト - Flask ルート と HTML レスポンステスト
"""

import pytest


class TestIndexRoute:
    """GET / ルートのテスト"""

    def test_index_returns_200(self, client):
        """インデックスページが 200 OK を返すか"""
        response = client.get('/')
        assert response.status_code == 200

    def test_index_returns_html(self, client):
        """インデックスページが HTML を返すか"""
        response = client.get('/')
        assert response.content_type == 'text/html; charset=utf-8'

    def test_index_contains_title(self, client):
        """ページタイトル「ポモドーロタイマー」が含まれるか"""
        response = client.get('/')
        assert 'ポモドーロタイマー' in response.get_data(as_text=True)

    def test_index_contains_status_text(self, client):
        """ステータステキスト「作業中」が含まれるか"""
        response = client.get('/')
        html = response.get_data(as_text=True)
        assert '作業中' in html

    def test_index_contains_timer_display(self, client):
        """タイマー表示「25:00」が含まれるか"""
        response = client.get('/')
        html = response.get_data(as_text=True)
        assert '25:00' in html

    def test_index_contains_buttons(self, client):
        """開始・リセットボタンが含まれるか"""
        response = client.get('/')
        html = response.get_data(as_text=True)
        assert '開始' in html
        assert 'リセット' in html

    def test_index_contains_progress_card(self, client):
        """進捗カードが含まれるか"""
        response = client.get('/')
        html = response.get_data(as_text=True)
        assert '今日の進捗' in html
        assert '完了' in html
        assert '集中時間' in html

    def test_index_contains_progress_values(self, client):
        """進捗カードの値（4、1時間40分）が含まれるか"""
        response = client.get('/')
        html = response.get_data(as_text=True)
        # 最初のダミーデータをチェック
        assert '4' in html  # 完了数
        assert '1時間40分' in html  # 集中時間

    def test_index_contains_circular_progress(self, client):
        """円形プログレスバー（SVG）が含まれるか"""
        response = client.get('/')
        html = response.get_data(as_text=True)
        assert '<svg' in html
        assert 'circular-progress' in html

    def test_index_contains_window_controls(self, client):
        """ウィンドウコントロールボタンが含まれるか"""
        response = client.get('/')
        html = response.get_data(as_text=True)
        assert 'window-controls' in html


class TestStaticFiles:
    """静的ファイルのロードテスト"""

    def test_css_file_loads(self, client):
        """CSSファイルが正常にロードされるか"""
        response = client.get('/static/css/styles.css')
        assert response.status_code == 200
        assert response.content_type == 'text/css; charset=utf-8'

    def test_js_file_loads(self, client):
        """JavaScriptファイルが正常にロードされるか"""
        response = client.get('/static/js/app.js')
        assert response.status_code == 200
        # JavaScriptファイルのコンテンツタイプをチェック
        assert 'javascript' in response.content_type or 'text/plain' in response.content_type

    def test_css_contains_primary_color(self, client):
        """CSSが紫系カラー（#6B5B95）を含むか"""
        response = client.get('/static/css/styles.css')
        css_content = response.get_data(as_text=True)
        assert '#6B5B95' in css_content

    def test_js_has_content(self, client):
        """JavaScriptファイルがコンテンツを持つか"""
        response = client.get('/static/js/app.js')
        js_content = response.get_data(as_text=True)
        assert len(js_content) > 0


class TestHTMLStructure:
    """HTMLの構造・レイアウトテスト"""

    def test_html_has_proper_structure(self, client):
        """HTMLが正しい構造を持つか（DOCTYPE、lang属性）"""
        response = client.get('/')
        html = response.get_data(as_text=True)
        assert '<!DOCTYPE html>' in html
        assert 'lang="ja"' in html

    def test_html_has_meta_charset(self, client):
        """HTMLが UTF-8 charset を指定しているか"""
        response = client.get('/')
        html = response.get_data(as_text=True)
        assert 'charset=' in html and 'UTF-8' in html

    def test_html_has_viewport_meta(self, client):
        """HTMLがレスポンシブ対応用の viewport メタタグを持つか"""
        response = client.get('/')
        html = response.get_data(as_text=True)
        assert 'viewport' in html

    def test_html_links_stylesheet(self, client):
        """HTMLが CSSファイルをリンクしているか"""
        response = client.get('/')
        html = response.get_data(as_text=True)
        assert 'styles.css' in html
        assert '<link' in html and 'css' in html

    def test_html_links_script(self, client):
        """HTMLが JavaScriptファイルをリンクしているか"""
        response = client.get('/')
        html = response.get_data(as_text=True)
        assert 'app.js' in html
        assert '<script' in html


class TestNotFound:
    """存在しないページのテスト"""

    def test_nonexistent_route_returns_404(self, client):
        """存在しないルートが 404 を返すか"""
        response = client.get('/nonexistent')
        assert response.status_code == 404
