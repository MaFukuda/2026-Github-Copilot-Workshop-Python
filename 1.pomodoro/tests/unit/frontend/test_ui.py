"""
フロントエンドテスト - UIコンポーネント と JavaScriptのテスト
"""

import pytest


class TestUIElements:
    """UIエレメントの存在・構造テスト"""

    def test_card_container_exists(self, client):
        """カードコンテナが存在するか"""
        response = client.get('/')
        html = response.get_data(as_text=True)
        assert 'class="card"' in html

    def test_header_section_exists(self, client):
        """ヘッダーセクションが存在するか"""
        response = client.get('/')
        html = response.get_data(as_text=True)
        assert 'class="header"' in html
        assert 'class="title"' in html

    def test_timer_section_exists(self, client):
        """タイマーセクションが存在するか"""
        response = client.get('/')
        html = response.get_data(as_text=True)
        assert 'class="timer-section"' in html
        assert 'class="time-display"' in html

    def test_button_group_exists(self, client):
        """ボタングループが存在するか"""
        response = client.get('/')
        html = response.get_data(as_text=True)
        assert 'class="button-group"' in html

    def test_primary_button_exists(self, client):
        """プライマリボタン（開始）が存在するか"""
        response = client.get('/')
        html = response.get_data(as_text=True)
        assert 'btn-primary' in html

    def test_secondary_button_exists(self, client):
        """セカンダリボタン（リセット）が存在するか"""
        response = client.get('/')
        html = response.get_data(as_text=True)
        assert 'btn-secondary' in html

    def test_progress_card_has_number(self, client):
        """進捗カードが数値を持つか"""
        response = client.get('/')
        html = response.get_data(as_text=True)
        assert 'class="progress-number"' in html

    def test_progress_card_has_time(self, client):
        """進捗カードが時間を持つか"""
        response = client.get('/')
        html = response.get_data(as_text=True)
        assert 'class="progress-time"' in html


class TestCSSStyles:
    """CSSスタイルの内容テスト"""

    def test_css_has_flexbox(self, client):
        """CSS が Flexbox を使用しているか"""
        response = client.get('/static/css/styles.css')
        css_content = response.get_data(as_text=True)
        assert 'display: flex' in css_content or 'display:flex' in css_content

    def test_css_has_gradient(self, client):
        """CSS がグラデーション背景を持つか"""
        response = client.get('/static/css/styles.css')
        css_content = response.get_data(as_text=True)
        assert 'linear-gradient' in css_content

    def test_css_has_border_radius(self, client):
        """CSS がボーダーラディウス（角丸）を持つか"""
        response = client.get('/static/css/styles.css')
        css_content = response.get_data(as_text=True)
        assert 'border-radius' in css_content

    def test_css_has_transitions(self, client):
        """CSS がトランジション効果を持つか"""
        response = client.get('/static/css/styles.css')
        css_content = response.get_data(as_text=True)
        assert 'transition' in css_content

    def test_css_has_responsive_design(self, client):
        """CSS がレスポンシブデザイン（メディアクエリ）を持つか"""
        response = client.get('/static/css/styles.css')
        css_content = response.get_data(as_text=True)
        assert '@media' in css_content

    def test_css_has_circular_progress_styles(self, client):
        """CSS が円形プログレスバーのスタイルを持つか"""
        response = client.get('/static/css/styles.css')
        css_content = response.get_data(as_text=True)
        assert 'circular-progress' in css_content or 'stroke-dasharray' in css_content


class TestJavaScript:
    """JavaScriptファイルの基本テスト"""

    def test_js_file_is_valid_javascript_skeleton(self, client):
        """JavaScriptファイルが有効な基本構造を持つか"""
        response = client.get('/static/js/app.js')
        js_content = response.get_data(as_text=True)
        # 最小限のJavaScript構造をチェック
        # Phase 1では実装がまだなので、コメントが入っていることを確認
        assert '//' in js_content or '/*' in js_content


class TestResponsiveness:
    """レスポンシブデザインのテスト"""

    def test_html_has_responsive_viewport(self, client):
        """ビューポートが正しく設定されているか"""
        response = client.get('/')
        html = response.get_data(as_text=True)
        assert 'viewport' in html
        assert 'width=device-width' in html
        assert 'initial-scale=1.0' in html

    def test_card_has_max_width(self, client):
        """カードが最大幅を持つか（レスポンシブ対応）"""
        response = client.get('/static/css/styles.css')
        css_content = response.get_data(as_text=True)
        assert 'max-width' in css_content
