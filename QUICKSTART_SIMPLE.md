# 🚀 V4.0シンプル版 - 超簡単スタート！

## 📦 必要なファイル（3つだけ！）

```
v4_simple/
├── pa_analyzer_v4_simple.py          ← これだけで全機能！
├── requirements_v4_simple.txt        ← ライブラリリスト
└── README_SIMPLE.md                  ← この説明書
```

---

## ⚡ 30秒で起動

### 1. インストール
```bash
pip install -r requirements_v4_simple.txt
```

### 2. 起動
```bash
streamlit run pa_analyzer_v4_simple.py
```

### 3. ログイン
- メール: `admin@pa.local`
- パスワード: `admin123`

**完了！** 🎉

---

## ✨ できること

### 基本機能（すぐ使える）
- ✅ 音源解析（5秒）
- ✅ AI学習
- ✅ 改善提案
- ✅ 履歴保存

### オプション（追加インストール）
- 🎸 楽器分離AI

追加したい場合：
```bash
pip install torch torchaudio --index-url https://download.pytorch.org/whl/cpu
pip install demucs
```

---

## 🎯 3ステップ解析

1. **音源アップロード** - WAV/MP3をドロップ
2. **情報入力** - 会場名、ミキサーなど
3. **解析開始** - ボタンクリック！

---

## 💡 シンプル版の違い

### 削除したもの
- ❌ メール送信
- ❌ 管理者機能
- ❌ 複雑な設定

### 残したもの
- ✅ **AI学習**
- ✅ **楽器分離**（オプション）
- ✅ **全ての解析機能**

---

## 📊 データ保存

アプリと同じフォルダに自動作成：
```
user_data/     # あなたのデータ
ai_data.json   # AI学習データ
users.json     # ログイン情報
```

---

## ❓ よくある質問

**Q: 複雑版との違いは？**  
A: 機能は同じ、ファイルが1つだけ

**Q: どっちを使うべき？**  
A: 迷ったらシンプル版！

**Q: データは移行できる？**  
A: はい、同じ形式です

---

**シンプル・イズ・ベスト！** 🎛️✨
