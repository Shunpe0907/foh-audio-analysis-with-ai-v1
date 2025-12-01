# 🔧 インストールエラーの修正方法

## ❌ エラー内容
```
ModuleNotFoundError: No module named 'librosa'
```

## ✅ 解決方法（3つの選択肢）

---

### 方法1: 自動インストールスクリプト（推奨⭐）

#### Windows:
```bash
install.bat
```
ダブルクリックでOK！

#### Mac/Linux:
```bash
chmod +x install.sh
./install.sh
```

これで全て自動でインストールされます。

---

### 方法2: 手動インストール（確実）

#### ステップ1: pipをアップグレード
```bash
pip install --upgrade pip
```

#### ステップ2: 依存関係を順番にインストール
```bash
# 基本ライブラリ
pip install numpy scipy numba joblib scikit-learn

# 音声処理
pip install decorator audioread soundfile pooch soxr lazy-loader msgpack

# Streamlit
pip install streamlit

# グラフ
pip install matplotlib pillow

# 音源解析（最後に）
pip install librosa
```

#### ステップ3: 確認
```bash
python -c "import librosa; print('OK!')"
```

---

### 方法3: requirements.txtから一括インストール

#### 新しいrequirements.txtを使用
```bash
pip install -r requirements_v4_simple_fixed.txt
```

**注意**: `requirements_v4_simple.txt`ではなく  
**`requirements_v4_simple_fixed.txt`**を使ってください！

---

## 🎸 楽器分離AI（オプション）

基本機能が動いたら、追加でインストール：

```bash
# CPU版（ほとんどの人向け）
pip install torch torchaudio --index-url https://download.pytorch.org/whl/cpu
pip install demucs

# GPU版（NVIDIA GPU搭載の場合）
pip install torch torchaudio --index-url https://download.pytorch.org/whl/cu118
pip install demucs
```

---

## 🔍 トラブルシューティング

### エラー: `pip: command not found`

**Mac/Linux**:
```bash
python -m pip install --upgrade pip
```

**Windows**:
```bash
py -m pip install --upgrade pip
```

### エラー: `Permission denied`

**Mac/Linux**:
```bash
pip install --user -r requirements_v4_simple_fixed.txt
```

### エラー: `Microsoft Visual C++ required`（Windows）

Visual C++ Build Toolsをインストール:
https://visualstudio.microsoft.com/visual-cpp-build-tools/

### エラー: `SSL certificate verify failed`

```bash
pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org librosa
```

### まだエラーが出る場合

Anaconda/Minicondaを使用：
```bash
conda create -n pa_analyzer python=3.10
conda activate pa_analyzer
conda install -c conda-forge librosa
pip install streamlit
```

---

## ✅ 動作確認

### 1. Pythonバージョン確認
```bash
python --version
```
**推奨**: Python 3.9以上

### 2. ライブラリ確認
```bash
python -c "import streamlit; import librosa; import numpy; print('全てOK!')"
```

### 3. アプリ起動
```bash
streamlit run pa_analyzer_v4_simple.py
```

---

## 📦 推奨環境

- **Python**: 3.9, 3.10, 3.11（3.12はまだ未対応）
- **OS**: Windows 10/11, macOS 10.15+, Ubuntu 20.04+
- **RAM**: 4GB以上（楽器分離使用時は8GB以上）

---

## 🆘 それでもダメな場合

### オンライン版を使用

Streamlit Cloudで動かす：
1. GitHubにコードをアップロード
2. Streamlit Cloudで無料デプロイ
3. ブラウザで使用

詳細: https://streamlit.io/cloud

---

## 📞 質問・サポート

エラーメッセージの全文をコピーして、開発者に連絡してください。

---

**ほとんどの場合、方法1の自動インストールスクリプトで解決します！** 🚀
