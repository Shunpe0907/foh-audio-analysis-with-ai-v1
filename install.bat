@echo off
REM PA Audio Analyzer V4.0 - Windowsインストールスクリプト

echo ==================================
echo PA Audio Analyzer V4.0
echo 自動インストール開始
echo ==================================
echo.

REM Python環境確認
echo 📋 Python環境確認...
python --version
echo.

REM pipアップグレード
echo ⬆️  pipをアップグレード...
pip install --upgrade pip
echo.

REM 基本ライブラリのインストール
echo 📦 基本ライブラリをインストール中...
pip install numpy scipy numba joblib scikit-learn decorator audioread soundfile pooch soxr lazy-loader msgpack
echo.

REM Streamlitのインストール
echo 🎨 Streamlitをインストール中...
pip install streamlit
echo.

REM Matplotlibのインストール
echo 📊 Matplotlibをインストール中...
pip install matplotlib pillow
echo.

REM Librosaのインストール
echo 🎵 Librosaをインストール中...
pip install librosa
echo.

echo ==================================
echo ✅ 基本インストール完了！
echo ==================================
echo.

REM 楽器分離AI（オプション）
set /p install_demucs="🎸 楽器分離AI機能もインストールしますか？（y/N）: "

if /i "%install_demucs%"=="y" (
    echo.
    echo 🤖 楽器分離AIをインストール中...
    echo ⚠️  これには数分かかります...
    
    REM CPU版PyTorch
    pip install torch torchaudio --index-url https://download.pytorch.org/whl/cpu
    
    REM Demucs
    pip install demucs
    
    echo.
    echo ✅ 楽器分離AIのインストール完了！
) else (
    echo.
    echo ⏭️  楽器分離AIはスキップしました
    echo    （後でインストールする場合: pip install torch torchaudio demucs）
)

echo.
echo ==================================
echo 🎉 すべてのインストールが完了しました！
echo ==================================
echo.
echo 🚀 起動方法:
echo    streamlit run pa_analyzer_v4_simple.py
echo.
echo 🔐 初回ログイン:
echo    メール: admin@pa.local
echo    パスワード: admin123
echo.
echo ==================================
pause
