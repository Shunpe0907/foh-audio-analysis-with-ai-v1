"""
PA Audio Analyzer V4.0 - シンプル版
AI学習 + 楽器分離 + 認証システム

使い方:
    pip install -r requirements_v4_simple.txt
    streamlit run pa_analyzer_v4_simple.py
"""

import streamlit as st
import numpy as np
import librosa
import matplotlib.pyplot as plt
from scipy import signal
import io
from pathlib import Path
import tempfile
import json
from datetime import datetime
import os
import hashlib
import secrets

# 楽器分離（オプション）
try:
    import torch
    import torchaudio
    from demucs.pretrained import get_model
    from demucs.apply import apply_model
    DEMUCS_AVAILABLE = True
except ImportError:
    DEMUCS_AVAILABLE = False

plt.rcParams['figure.max_open_warning'] = 50

st.set_page_config(
    page_title="PA Audio Analyzer V4.0",
    page_icon="🎛️",
    layout="wide"
)

st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        text-align: center;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .good-point {
        background-color: #e6ffe6;
        padding: 1rem;
        border-left: 4px solid #44ff44;
        margin: 0.5rem 0;
        border-radius: 0.25rem;
    }
    .critical {
        background-color: #ffe6e6;
        padding: 1rem;
        border-left: 4px solid #ff4444;
        margin: 0.5rem 0;
        border-radius: 0.25rem;
    }
    .ai-insight {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)


# =====================================
# 簡易認証システム
# =====================================

class SimpleAuth:
    def __init__(self):
        self.users_file = Path('users.json')
        self.users = self.load_users()
        
    def load_users(self):
        if self.users_file.exists():
            with open(self.users_file, 'r') as f:
                return json.load(f)
        else:
            # デフォルト管理者
            default = {
                'admin@pa.local': {
                    'password': self._hash('admin123'),
                    'username': '管理者',
                    'created': datetime.now().isoformat()
                }
            }
            self.save_users(default)
            return default
    
    def save_users(self, users):
        with open(self.users_file, 'w') as f:
            json.dump(users, f, ensure_ascii=False, indent=2)
    
    def _hash(self, password):
        salt = secrets.token_hex(8)
        pwd_hash = hashlib.sha256((password + salt).encode()).hexdigest()
        return f"{salt}:{pwd_hash}"
    
    def _verify(self, password, stored):
        salt, pwd_hash = stored.split(':')
        return hashlib.sha256((password + salt).encode()).hexdigest() == pwd_hash
    
    def register(self, email, password, username):
        if email in self.users:
            return False, "既に登録済みです"
        self.users[email] = {
            'password': self._hash(password),
            'username': username,
            'created': datetime.now().isoformat()
        }
        self.save_users(self.users)
        return True, "登録完了"
    
    def login(self, email, password):
        if email not in self.users:
            return False, None
        if self._verify(password, self.users[email]['password']):
            return True, self.users[email]
        return False, None


# =====================================
# AI学習システム（シンプル版）
# =====================================

class SimpleAI:
    def __init__(self):
        self.data_file = Path('ai_data.json')
        self.data = self.load_data()
    
    def load_data(self):
        if self.data_file.exists():
            with open(self.data_file, 'r') as f:
                return json.load(f)
        return {'users': {}, 'mixers': {}}
    
    def save_data(self):
        with open(self.data_file, 'w') as f:
            json.dump(self.data, f, ensure_ascii=False, indent=2)
    
    def learn(self, user_email, result, metadata):
        # ユーザーデータ
        if user_email not in self.data['users']:
            self.data['users'][user_email] = {
                'count': 0,
                'rms_history': [],
                'venues': {}
            }
        
        user = self.data['users'][user_email]
        user['count'] += 1
        user['rms_history'].append(result['rms_db'])
        
        venue = metadata.get('venue', '不明')
        user['venues'][venue] = user['venues'].get(venue, 0) + 1
        
        # ミキサーデータ
        mixer = metadata.get('mixer', '不明')
        if mixer not in self.data['mixers']:
            self.data['mixers'][mixer] = {'count': 0, 'avg_rms': []}
        
        self.data['mixers'][mixer]['count'] += 1
        self.data['mixers'][mixer]['avg_rms'].append(result['rms_db'])
        
        self.save_data()
    
    def get_insights(self, user_email, current_result):
        insights = []
        
        if user_email not in self.data['users']:
            return ["🎉 初回解析！データを蓄積していきましょう"]
        
        user = self.data['users'][user_email]
        
        if user['count'] >= 3:
            avg_rms = np.mean(user['rms_history'][-5:])
            current_rms = current_result['rms_db']
            
            if current_rms > avg_rms + 2:
                insights.append(f"📈 音圧が向上！平均より{current_rms - avg_rms:.1f}dB高いです")
            elif current_rms < avg_rms - 2:
                insights.append(f"📉 音圧が低下。平均より{avg_rms - current_rms:.1f}dB低いです")
            else:
                insights.append(f"✅ 安定した音圧です（平均: {avg_rms:.1f}dB）")
        
        if user['count'] >= 5:
            insights.append(f"🎯 総解析数: {user['count']}回")
        
        return insights if insights else ["📊 データを蓄積中...（3回以上でAI分析開始）"]


# =====================================
# 楽器分離（シンプル版）
# =====================================

class SimpleSeparator:
    def __init__(self):
        self.available = DEMUCS_AVAILABLE
        self.model = None
        
        if self.available:
            try:
                self.model = get_model('htdemucs')
                self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
                self.model.to(self.device)
            except:
                self.available = False
    
    def separate(self, audio_path):
        if not self.available or self.model is None:
            return None, "楽器分離機能が利用できません"
        
        try:
            audio, sr = torchaudio.load(audio_path)
            if audio.shape[0] == 1:
                audio = audio.repeat(2, 1)
            
            audio = audio.to(self.device).unsqueeze(0)
            
            with torch.no_grad():
                sources = apply_model(self.model, audio, device=self.device)
            
            sources = sources.squeeze(0).cpu().numpy()
            
            return {
                'drums': sources[0],
                'bass': sources[1],
                'other': sources[2],
                'vocals': sources[3]
            }, None
            
        except Exception as e:
            return None, f"分離エラー: {str(e)}"


# =====================================
# 音源解析（シンプル版）
# =====================================

class SimpleAnalyzer:
    def __init__(self, audio_path):
        self.audio_path = audio_path
        self.y, self.sr = librosa.load(audio_path, sr=44100, mono=False)
        if len(self.y.shape) == 1:
            self.y = np.stack([self.y, self.y])
    
    def analyze(self):
        mono = np.mean(self.y, axis=0)
        
        # 基本指標
        rms = np.sqrt(np.mean(mono ** 2))
        rms_db = 20 * np.log10(rms + 1e-10)
        
        peak = np.max(np.abs(mono))
        peak_db = 20 * np.log10(peak + 1e-10)
        
        crest = peak_db - rms_db
        
        # ステレオ幅
        L, R = self.y[0], self.y[1]
        mid = (L + R) / 2
        side = (L - R) / 2
        mid_e = np.sum(mid ** 2)
        side_e = np.sum(side ** 2)
        stereo_width = (side_e / (mid_e + side_e + 1e-10)) * 100
        
        # 周波数解析
        bands = {
            'sub_bass': (20, 60),
            'bass': (60, 250),
            'low_mid': (250, 500),
            'mid': (500, 2000),
            'high_mid': (2000, 4000),
            'presence': (4000, 8000),
            'brilliance': (8000, 20000)
        }
        
        band_energies = {}
        for name, (low, high) in bands.items():
            filtered = self.bandpass(mono, low, high)
            energy = 20 * np.log10(np.sqrt(np.mean(filtered ** 2)) + 1e-10)
            band_energies[name] = float(energy)
        
        return {
            'rms_db': float(rms_db),
            'peak_db': float(peak_db),
            'crest_factor': float(crest),
            'stereo_width': float(stereo_width),
            'band_energies': band_energies
        }
    
    def bandpass(self, audio, low, high):
        nyq = self.sr / 2
        low_n = np.clip(low / nyq, 0.001, 0.999)
        high_n = np.clip(high / nyq, 0.001, 0.999)
        
        if low_n >= high_n:
            return audio * 0
        
        try:
            sos = signal.butter(4, [low_n, high_n], btype='band', output='sos')
            return signal.sosfilt(sos, audio)
        except:
            return audio * 0


# =====================================
# データ保存
# =====================================

class SimpleStorage:
    def __init__(self):
        self.data_dir = Path('user_data')
        self.data_dir.mkdir(exist_ok=True)
    
    def save(self, user_email, result, metadata):
        filename = user_email.replace('@', '_at_').replace('.', '_') + '.json'
        filepath = self.data_dir / filename
        
        data = {'analyses': []}
        if filepath.exists():
            with open(filepath, 'r') as f:
                data = json.load(f)
        
        data['analyses'].append({
            'id': datetime.now().strftime('%Y%m%d_%H%M%S'),
            'timestamp': datetime.now().isoformat(),
            'metadata': metadata,
            'result': result
        })
        
        with open(filepath, 'w') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def load(self, user_email):
        filename = user_email.replace('@', '_at_').replace('.', '_') + '.json'
        filepath = self.data_dir / filename
        
        if filepath.exists():
            with open(filepath, 'r') as f:
                data = json.load(f)
                return sorted(data['analyses'], key=lambda x: x['timestamp'], reverse=True)
        return []


# =====================================
# メインアプリ
# =====================================

def init_session():
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    if 'user' not in st.session_state:
        st.session_state.user = None
    if 'page' not in st.session_state:
        st.session_state.page = 'login'


def show_login():
    auth = SimpleAuth()
    
    st.markdown('<h1 class="main-header">🎛️ PA Audio Analyzer V4.0</h1>', unsafe_allow_html=True)
    st.markdown("### 🔐 ログイン")
    
    tab1, tab2 = st.tabs(["ログイン", "新規登録"])
    
    with tab1:
        with st.form("login"):
            email = st.text_input("メールアドレス", placeholder="your@email.com")
            password = st.text_input("パスワード", type="password")
            
            if st.form_submit_button("ログイン", use_container_width=True, type="primary"):
                success, user = auth.login(email, password)
                if success:
                    st.session_state.authenticated = True
                    st.session_state.user = {'email': email, 'username': user['username']}
                    st.rerun()
                else:
                    st.error("ログイン失敗")
    
    with tab2:
        with st.form("register"):
            email = st.text_input("メールアドレス", placeholder="your@email.com", key="reg_email")
            username = st.text_input("ユーザー名", placeholder="山田太郎")
            password = st.text_input("パスワード", type="password", key="reg_pass")
            
            if st.form_submit_button("登録", use_container_width=True, type="primary"):
                if email and username and password:
                    success, msg = auth.register(email, password, username)
                    if success:
                        st.success("✅ 登録完了！ログインしてください")
                    else:
                        st.error(msg)
                else:
                    st.error("全て入力してください")


def show_analyzer():
    user = st.session_state.user
    
    with st.sidebar:
        st.markdown(f"### 👤 {user['username']}")
        st.caption(user['email'])
        st.markdown("---")
        
        menu = st.radio("メニュー", ["🎵 解析", "📊 履歴", "🚪 ログアウト"], label_visibility="collapsed")
        
        if menu == "🚪 ログアウト":
            st.session_state.authenticated = False
            st.session_state.user = None
            st.rerun()
    
    if menu == "🎵 解析":
        show_analysis_page(user)
    elif menu == "📊 履歴":
        show_history_page(user)


def show_analysis_page(user):
    st.markdown('<h1 class="main-header">🎛️ PA Audio Analyzer V4.0</h1>', unsafe_allow_html=True)
    
    # 楽器分離の可否表示
    separator = SimpleSeparator()
    if separator.available:
        st.success("✅ 楽器分離AI: 利用可能")
    else:
        st.warning("⚠️ 楽器分離AI: 未インストール（基本解析のみ利用可能）")
    
    st.markdown("---")
    
    uploaded = st.file_uploader("音源ファイル（WAV/MP3）", type=['wav', 'mp3'])
    
    if uploaded:
        col1, col2 = st.columns(2)
        
        with col1:
            name = st.text_input("解析名", placeholder="ライブ本番")
            venue = st.text_input("会場名", placeholder="CLUB QUATTRO")
        
        with col2:
            mixer = st.text_input("ミキサー", placeholder="Yamaha CL5")
            use_separation = st.checkbox("楽器分離AI使用", value=False, disabled=not separator.available)
        
        if st.button("🚀 解析開始", type="primary", use_container_width=True):
            with st.spinner("解析中..."):
                # 一時保存
                with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as tmp:
                    tmp.write(uploaded.getvalue())
                    tmp_path = tmp.name
                
                try:
                    # 基本解析
                    analyzer = SimpleAnalyzer(tmp_path)
                    result = analyzer.analyze()
                    
                    # メタデータ
                    metadata = {
                        'analysis_name': name or '名称未設定',
                        'venue': venue or '不明',
                        'mixer': mixer or '不明'
                    }
                    
                    # AI学習
                    ai = SimpleAI()
                    ai.learn(user['email'], result, metadata)
                    
                    # データ保存
                    storage = SimpleStorage()
                    storage.save(user['email'], result, metadata)
                    
                    # 結果表示
                    st.success("✅ 解析完了！")
                    
                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        st.metric("RMS", f"{result['rms_db']:.1f} dB")
                    with col2:
                        st.metric("Peak", f"{result['peak_db']:.1f} dB")
                    with col3:
                        st.metric("Crest", f"{result['crest_factor']:.1f} dB")
                    with col4:
                        st.metric("Stereo", f"{result['stereo_width']:.1f}%")
                    
                    # グラフ
                    st.markdown("### 📊 周波数分布")
                    fig, ax = plt.subplots(figsize=(10, 4))
                    bands = list(result['band_energies'].keys())
                    energies = list(result['band_energies'].values())
                    colors = ['#8B0000', '#FF4500', '#FFD700', '#32CD32', '#4169E1', '#9370DB', '#FF1493']
                    ax.bar(bands, energies, color=colors, alpha=0.7)
                    ax.set_ylabel('Energy (dB)')
                    ax.grid(True, alpha=0.3)
                    plt.xticks(rotation=45)
                    st.pyplot(fig)
                    plt.close()
                    
                    # AI提案
                    st.markdown("### 🧠 AI分析")
                    insights = ai.get_insights(user['email'], result)
                    for insight in insights:
                        st.markdown(f'<div class="ai-insight">{insight}</div>', unsafe_allow_html=True)
                    
                    # 改善提案
                    st.markdown("### 💡 改善提案")
                    
                    rms = result['rms_db']
                    if -20 <= rms <= -16:
                        st.markdown(f'<div class="good-point">✅ RMS音圧が適切です（{rms:.1f}dB）</div>', unsafe_allow_html=True)
                    elif rms < -23:
                        st.markdown(f'<div class="critical">⚠️ 音圧が低すぎます（{rms:.1f}dB）。マスターを上げてください</div>', unsafe_allow_html=True)
                    
                    peak = result['peak_db']
                    if peak > -1:
                        st.markdown(f'<div class="critical">⚠️ ピークが高すぎます（{peak:.1f}dB）。クリッピングの危険</div>', unsafe_allow_html=True)
                    
                    width = result['stereo_width']
                    if 50 <= width <= 70:
                        st.markdown(f'<div class="good-point">✅ ステレオ幅が理想的です（{width:.1f}%）</div>', unsafe_allow_html=True)
                    
                    # 楽器分離
                    if use_separation:
                        st.markdown("---")
                        st.markdown("### 🎸 楽器分離解析")
                        
                        with st.spinner("楽器分離中...（数分かかります）"):
                            separated, error = separator.separate(tmp_path)
                            
                            if separated:
                                st.success("✅ 分離完了！")
                                
                                for inst_name, inst_audio in separated.items():
                                    with st.expander(f"🎵 {inst_name.upper()}"):
                                        mono = np.mean(inst_audio, axis=0)
                                        rms = 20 * np.log10(np.sqrt(np.mean(mono ** 2)) + 1e-10)
                                        peak = 20 * np.log10(np.max(np.abs(mono)) + 1e-10)
                                        
                                        col1, col2 = st.columns(2)
                                        with col1:
                                            st.metric("RMS", f"{rms:.1f} dB")
                                        with col2:
                                            st.metric("Peak", f"{peak:.1f} dB")
                            else:
                                st.error(error)
                    
                finally:
                    os.unlink(tmp_path)


def show_history_page(user):
    st.markdown("## 📊 解析履歴")
    
    storage = SimpleStorage()
    analyses = storage.load(user['email'])
    
    if not analyses:
        st.info("まだ解析データがありません")
        return
    
    st.write(f"**総解析数: {len(analyses)}件**")
    
    for analysis in analyses:
        name = analysis['metadata']['analysis_name']
        venue = analysis['metadata']['venue']
        timestamp = datetime.fromisoformat(analysis['timestamp'])
        
        with st.expander(f"🎵 {name} - {venue} ({timestamp.strftime('%Y/%m/%d %H:%M')})"):
            result = analysis['result']
            
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("RMS", f"{result['rms_db']:.1f} dB")
            with col2:
                st.metric("Peak", f"{result['peak_db']:.1f} dB")
            with col3:
                st.metric("Crest", f"{result['crest_factor']:.1f} dB")
            with col4:
                st.metric("Stereo", f"{result['stereo_width']:.1f}%")


def main():
    init_session()
    
    if not st.session_state.authenticated:
        show_login()
    else:
        show_analyzer()


if __name__ == "__main__":
    main()
