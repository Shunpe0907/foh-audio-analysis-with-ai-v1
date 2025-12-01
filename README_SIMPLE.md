# 🎛️ PA Audio Analyzer V4.0 - シンプル版

## ✨ たった2ファイルで動く！

1. `pa_analyzer_v4_simple.py` - メインアプリ（1ファイル完結）
2. `requirements_v4_simple.txt` - 必要なライブラリ

## 🚀 3ステップで起動

### ステップ1: ライブラリインストール

```bash
pip install -r requirements_v4_simple.txt
```

### ステップ2: 起動

```bash
streamlit run pa_analyzer_v4_simple.py
```

### ステップ3: ログイン

- メール: `admin@pa.local`
- パスワード: `admin123`

**完了！** 🎉

---

## 📋 主な機能

### ✅ 標準機能（追加インストール不要）

- ✅ ユーザー登録・ログイン
- ✅ 2mix音源解析
  - RMS音圧
  - ピークレベル
  - クレストファクター
  - ステレオ幅
  - 周波数7バンド分析
- ✅ AI学習機能
  - 個人の傾向分析
  - 音圧推移の追跡
  - 会場別統計
- ✅ 改善提案
- ✅ 解析履歴保存
- ✅ グラフ表示

### 🎸 楽器分離AI（オプション）

以下を追加インストールすると使えます：

```bash
pip install torch torchaudio --index-url https://download.pytorch.org/whl/cpu
pip install demucs
```

- Vocals（ボーカル）
- Drums（ドラム）
- Bass（ベース）
- Other（ギター等）

**注意**: 処理に数分かかります

---

## 💡 改善点（シンプル化）

### V4.0複雑版から削除した機能:

❌ メール送信機能  
❌ 管理者ダッシュボード  
❌ 詳細なプロフィール管理  
❌ 複雑なUI  
❌ 過剰なドキュメント  

### 残した機能:

✅ AI学習  
✅ 楽器分離（オプション）  
✅ 基本解析  
✅ 履歴保存  
✅ 簡単ログイン  

---

## 📊 データ保存先

```
user_data/          # 解析データ
ai_data.json        # AI学習データ
users.json          # ユーザー情報
```

---

## 🔧 トラブルシューティング

### Q: 楽器分離が使えない

```bash
pip install torch torchaudio demucs
```

### Q: ログインできない

`users.json`を削除して再起動

### Q: エラーが出る

```bash
pip install --upgrade -r requirements_v4_simple.txt
```

---

## 🎯 使い方のコツ

1. **まず基本解析で慣れる**
2. **3回以上解析してAI機能を体験**
3. **余裕があれば楽器分離を試す**

---

## ⚡ 処理速度

| 機能 | 時間 |
|-----|------|
| 基本解析 | 5秒 |
| 楽器分離（CPU） | 2-3分 |
| 楽器分離（GPU） | 15-30秒 |

---

**シンプル・イズ・ベスト！** 🎛️✨
