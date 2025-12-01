#!/bin/bash
# PA Audio Analyzer V4.0 - 自動インストールスクリプト

echo "=================================="
echo "PA Audio Analyzer V4.0"
echo "自動インストール開始"
echo "=================================="
echo ""

# Python環境確認
echo "📋 Python環境確認..."
python --version
echo ""

# pipアップグレード
echo "⬆️  pipをアップグレード..."
pip install --upgrade pip
echo ""

# 基本ライブラリのインストール
echo "📦 基本ライブラリをインストール中..."
pip install numpy scipy numba joblib scikit-learn decorator audioread soundfile pooch soxr lazy-loader msgpack
echo ""

# Streamlitのインストール
echo "🎨 Streamlitをインストール中..."
pip install streamlit
echo ""

# Matplotlibのインストール
echo "📊 Matplotlibをインストール中..."
pip install matplotlib pillow
echo ""

# Librosaのインストール
echo "🎵 Librosaをインストール中..."
pip install librosa
echo ""

echo "=================================="
echo "✅ 基本インストール完了！"
echo "=================================="
echo ""

# 楽器分離AI（オプション）
read -p "🎸 楽器分離AI機能もインストールしますか？（y/N）: " install_demucs

if [[ $install_demucs =~ ^[Yy]$ ]]; then
    echo ""
    echo "🤖 楽器分離AIをインストール中..."
    echo "⚠️  これには数分かかります..."
    
    # CPU版PyTorch
    pip install torch torchaudio --index-url https://download.pytorch.org/whl/cpu
    
    # Demucs
    pip install demucs
    
    echo ""
    echo "✅ 楽器分離AIのインストール完了！"
else
    echo ""
    echo "⏭️  楽器分離AIはスキップしました"
    echo "   （後でインストールする場合: pip install torch torchaudio demucs）"
fi

echo ""
echo "=================================="
echo "🎉 すべてのインストールが完了しました！"
echo "=================================="
echo ""
echo "🚀 起動方法:"
echo "   streamlit run pa_analyzer_v4_simple.py"
echo ""
echo "🔐 初回ログイン:"
echo "   メール: admin@pa.local"
echo "   パスワード: admin123"
echo ""
echo "=================================="
