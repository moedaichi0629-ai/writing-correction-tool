# ✏️ 伝わる文章添削ツール

AIが文章を添削し、修正文・理由・印象・別案までまとめて提案してくれるWebアプリです。

---

## 誰の課題を解決するか

文章に自信がない **大学生・社会人・10〜20代** の方が対象です。

---

## どんな課題を解決するか

- 自分の文章が正しいか分からない
- どこを直せばいいか分からない
- TPOに合った表現になっているか不安
- 相手にどう伝わるか分からない

---

## どう解決するか

AIが入力された文章を分析し、以下を出力します。

1. **修正文** — より伝わりやすくした文章
2. **変更した理由** — なぜそのように変えたかを箇条書きで説明
3. **相手に与える印象** — 読んだ相手がどう感じるかを説明
4. **別パターン案** — 丁寧版・短め版・やわらかい版などを提案
5. **コピペ用完成文** — そのまま使える完成形

用途（LINE / メール / 報告文 / 依頼文 / お礼文 / SNS投稿）と  
希望トーン（丁寧 / やわらかい / 短く / ビジネス向け / 親しみやすい）を選んで添削できます。

---

## 使用技術

| 技術 | 用途 |
|------|------|
| Python | プログラミング言語 |
| Streamlit | WebアプリのUI |
| OpenAI API (GPT-4o mini) | 文章添削AI |
| python-dotenv | APIキーの管理 |

---

## 使い方

### 1. リポジトリをクローン

```bash
git clone https://github.com/moedaichi0629-ai/writing-correction-tool.git
cd writing-correction-tool
```

### 2. パッケージをインストール

```bash
pip install -r requirements.txt
```

### 3. APIキーを設定

```bash
# Windows
copy .env.example .env

# Mac / Linux
cp .env.example .env
```

`.env` を開いて、OpenAI APIキーを貼り付けます：

```
OPENAI_API_KEY=sk-あなたのAPIキーをここに貼り付ける
```

> APIキーは https://platform.openai.com/api-keys で取得できます。

### 4. アプリを起動

```bash
# streamlit がPATHに通っている場合
streamlit run app.py

# 通っていない場合（Windowsでよくある）
python -m streamlit run app.py
```

ブラウザが自動で開き、`http://localhost:8501` でアプリが使えます。

---

## ファイル構成

```
writing-correction-tool/
├── app.py            # メインアプリ（Streamlit + OpenAI）
├── requirements.txt  # 必要なパッケージ一覧
├── .env.example      # APIキー設定のサンプル
├── .env              # 実際のAPIキー（GitHubには上げない）
├── .gitignore        # GitHubに上げないファイルの設定
└── README.md         # このファイル
```

---

## 今後追加したい機能

- [ ] 添削履歴の保存・一覧表示
- [ ] 添削前後の差分をハイライト表示
- [ ] よく使うフレーズのテンプレート機能
- [ ] 文章の長さ・読みやすさスコアの表示
- [ ] SNSシェア機能（添削結果をそのまま投稿）
- [ ] スマホ向けUIの最適化

---

## 注意事項

- `.env` ファイルは絶対にGitHubに公開しないでください（APIキーが漏れます）
- OpenAI APIの利用には料金が発生します（GPT-4o miniは低コストです）
