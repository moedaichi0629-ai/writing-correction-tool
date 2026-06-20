"""
伝わる文章添削ツール
OpenAI APIを使って、入力した文章をAIが添削するWebアプリです。
"""

import os
from datetime import datetime
import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv

# .envファイルから環境変数を読み込む
load_dotenv()

# OpenAIクライアントの初期化
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# ページ設定
st.set_page_config(
    page_title="伝わる文章添削ツール",
    page_icon="✏️",
    layout="centered",
)

# スマホ向けCSSの適用
st.markdown("""
<style>
/* スマホ向け全体調整 */
@media (max-width: 768px) {
    /* 文章入力欄のフォントサイズ（iOSで自動ズームを防ぐため16px以上） */
    .stTextArea textarea {
        font-size: 16px !important;
    }
    /* セレクトボックスのフォントサイズ */
    .stSelectbox select,
    .stSelectbox div[data-baseweb="select"] {
        font-size: 16px !important;
    }
    /* 添削ボタンを大きく */
    .stButton > button {
        font-size: 1.1rem !important;
        padding: 0.9rem 1rem !important;
        min-height: 3rem !important;
    }
    /* セクション間の余白を狭める */
    section.main > div { padding: 0.5rem 0.8rem !important; }
    /* 見出しを小さめに */
    h1 { font-size: 1.6rem !important; }
    h2 { font-size: 1.2rem !important; }
    h3 { font-size: 1rem !important; }
}

/* 履歴カード */
.history-card {
    background: #f8f9fa;
    border-left: 3px solid #4361ee;
    border-radius: 6px;
    padding: 0.6rem 0.9rem;
    margin-bottom: 0.5rem;
    font-size: 0.88rem;
}
.history-meta {
    color: #888;
    font-size: 0.78rem;
    margin-bottom: 0.2rem;
}
</style>
""", unsafe_allow_html=True)

# 添削履歴をセッション内で保持する（ブラウザを閉じるとリセットされる）
if "history" not in st.session_state:
    st.session_state.history = []

# タイトルと説明
st.title("✏️ 伝わる文章添削ツール")
st.markdown("文章を入力すると、AIが修正文・理由・印象・別案まで提案します")
st.divider()

# 文章入力欄
user_text = st.text_area(
    "添削したい文章を入力してください",
    placeholder="例：お世話になります。先日の件ですが、確認していただけましたでしょうか。",
    height=180,
)

col1, col2 = st.columns(2)

# 用途選択
with col1:
    purpose = st.selectbox(
        "文章の用途",
        options=["LINE", "メール", "報告文", "依頼文", "お礼文", "SNS投稿"],
    )

# トーン選択
with col2:
    tone = st.selectbox(
        "希望するトーン",
        options=["丁寧", "やわらかい", "短く", "ビジネス向け", "親しみやすい"],
    )

st.divider()

# 添削実行ボタン
run_button = st.button("✨ 添削する", type="primary", use_container_width=True)


def build_prompt(text: str, purpose: str, tone: str) -> str:
    """AIに送るプロンプトを組み立てる関数"""
    return f"""
あなたは日本語の文章添削の専門家です。
以下の文章を添削してください。

【入力文章】
{text}

【用途】
{purpose}

【希望するトーン】
{tone}

以下の観点で添削してください：
- 誤字脱字
- 分かりにくい表現
- 文章の順番
- TPOに合っているか
- 相手に失礼になっていないか
- 伝えたい内容が分かりやすいか
- 文章が長すぎないか

必ず以下の形式で回答してください（マークダウン形式）：

### 修正文
（添削後の文章をここに記載）

### 変更した理由
（変更点を箇条書きで説明）

### 相手に与える印象
（この文章を読んだ相手がどのように感じるかを説明）

### 別パターン案
（丁寧版・短め版・やわらかい版など、2〜3パターンを提案）

### コピペ用完成文
（そのままコピーして使える完成文を記載）
"""


# 添削処理
if run_button:
    if not user_text.strip():
        st.warning("⚠️ 文章を入力してください")
    elif not os.getenv("OPENAI_API_KEY"):
        st.error("❌ APIキーが設定されていません。.envファイルにOPENAI_API_KEYを設定してください。")
    else:
        with st.spinner("AIが添削中です。少しお待ちください..."):
            try:
                prompt = build_prompt(user_text, purpose, tone)

                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {
                            "role": "system",
                            "content": "あなたは日本語文章の添削の専門家です。丁寧かつ分かりやすく添削結果を返してください。",
                        },
                        {"role": "user", "content": prompt},
                    ],
                    temperature=0.7,
                )

                result = response.choices[0].message.content

                # 添削結果を履歴に保存する
                st.session_state.history.append({
                    "timestamp": datetime.now().strftime("%m/%d %H:%M"),
                    "original": user_text[:40] + "…" if len(user_text) > 40 else user_text,
                    "purpose": purpose,
                    "tone": tone,
                    "result": result,
                })

                # 結果表示
                st.success("✅ 添削が完了しました！")
                st.divider()
                st.markdown("## 添削結果")
                st.markdown(result)

            except Exception as e:
                error_msg = str(e)
                if "api_key" in error_msg.lower() or "authentication" in error_msg.lower():
                    st.error("❌ APIキーが正しくありません。設定を確認してください。")
                elif "rate_limit" in error_msg.lower():
                    st.error("❌ API利用制限に達しました。しばらく待ってから再度お試しください。")
                elif "connection" in error_msg.lower():
                    st.error("❌ インターネット接続を確認してください。")
                else:
                    st.error(f"❌ エラーが発生しました：{error_msg}")

# 添削履歴の表示
if st.session_state.history:
    st.divider()
    st.markdown("## 📋 添削履歴")
    st.caption("※ この履歴はブラウザを閉じるとリセットされます")

    # 新しい順に表示する
    for i, item in enumerate(reversed(st.session_state.history)):
        with st.expander(f"🕐 {item['timestamp']}　{item['purpose']} × {item['tone']}　｜　{item['original']}"):
            st.markdown(item["result"])

    # 履歴を全件削除するボタン
    if st.button("🗑️ 履歴をすべて削除", use_container_width=True):
        st.session_state.history = []
        st.rerun()

# フッター
st.divider()
st.markdown(
    "<p style='text-align:center; color:gray; font-size:0.85rem;'>Powered by OpenAI GPT-4o mini</p>",
    unsafe_allow_html=True,
)
