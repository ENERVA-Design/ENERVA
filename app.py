import streamlit as st
import pandas as pd
import numpy as np
from pathlib import Path
import plotly.express as px
import plotly.graph_objects as go

# Mengimpor modul inti enerva_core yang ada di folder yang sama
from enerva_core import analyze_enerva, preprocess_csv

# =========================================================
# 1. KONFIGURASI HALAMAN
# =========================================================

st.set_page_config(
    page_title="ENERVA | Energy Monitoring",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================================================
# 2. WARNA DAN TEMA
# =========================================================

EMERALD = "#1CC998"
DARK_GREEN = "#064E3B"
LIGHT_GREEN = "#D1FAE5"
MINT = "#ECFDF5"
GOLD = "#F59E0B"
DARK_TEXT = "#1F2937"
MUTED_TEXT = "#64748B"

# =========================================================
# 3. CUSTOM CSS
# =========================================================

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background-color: #F8FAFC;
    color: #1F2937;
}

[data-testid="stSidebar"] {
    background-color: #064E3B;
}

[data-testid="stSidebar"] * {
    color: white !important;
}

.main-title {
    font-size: 46px;
    font-weight: 800;
    color: #064E3B;
}

.section-title {
    font-size: 28px;
    font-weight: 800;
    color: #064E3B;
    margin-top: 25px;
    margin-bottom: 12px;
}

.section-description {
    font-size: 16px;
    line-height: 1.8;
    color: #64748B;
}

.hero {
    padding: 45px;
    border-radius: 22px;
    background: linear-gradient(90deg, #064E3B, #047857);
    color: white;
    margin-bottom: 30px;
}

.hero h1 {
    color: white;
    font-size: 43px;
    font-weight: 800;
}

.hero p {
    color: #ECFDF5;
    font-size: 17px;
    line-height: 1.8;
}

.info-card, .dataset-card {
    background: white;
    border: 1px solid #D1FAE5;
    border-radius: 16px;
    padding: 22px;
    margin-bottom: 12px;
}

.info-card h3 {
    color: #047857;
}

.info-card p {
    color: #64748B;
    line-height: 1.7;
}

.workflow-card {
    background: white;
    border: 1px solid #E2E8F0;
    border-left: 5px solid #059669;
    border-radius: 14px;
    padding: 20px 24px;
    margin-bottom: 16px;
}

.workflow-card h4 {
    color: #064E3B;
}

.workflow-card p {
    color: #64748B;
    line-height: 1.7;
}

.variable-card {
    background: white;
    border-left: 5px solid #059669;
    border-radius: 12px;
    padding: 17px;
    margin-bottom: 12px;
}

.variable-card h4 {
    color: #065F46;
}

.variable-card p {
    color: #64748B;
    font-size: 14px;
}

.warning-card {
    background: #FFFBEB;
    border: 1px solid #FDE68A;
    border-radius: 14px;
    padding: 20px;
    color: #92400E;
    line-height: 1.8;
}

.footer {
    text-align: center;
    padding: 25px;
    color: #94A3B8;
    font-size: 13px;
    margin-top: 40px;
}

.analysis-header {
    background: linear-gradient(120deg, #064E3B, #0F766E, #1CC998);
    padding: 38px 42px;
    border-radius: 20px;
    margin-bottom: 35px;
    box-shadow: 0 8px 25px rgba(6,78,59,0.13);
}

.analysis-header h1 {
    color: white;
    font-size: 36px;
    font-weight: 800;
}

.analysis-header p {
    color: #D1FAE5;
    font-size: 16px;
    line-height: 1.8;
}

.analysis-heading {
    color: #064E3B;
    font-size: 22px;
    font-weight: 750;
    margin-top: 28px;
    margin-bottom: 15px;
}

.analysis-description {
    color: #64748B;
    font-size: 14px;
    line-height: 1.7;
    margin-bottom: 15px;
}

.analysis-card {
    background: white;
    border: 1px solid #D1FAE5;
    border-radius: 16px;
    padding: 20px;
    min-height: 150px;
    box-shadow: 0 4px 13px rgba(6,78,59,0.045);
}

.analysis-card .card-icon {
    font-size: 26px;
    margin-bottom: 12px;
}

.analysis-card .card-label {
    color: #64748B;
    font-size: 13px;
    margin-bottom: 8px;
}

.analysis-card .card-value {
    color: #064E3B;
    font-size: 23px;
    font-weight: 800;
}

.analysis-note {
    background: #ECFDF5;
    border-left: 5px solid #059669;
    border-radius: 12px;
    padding: 20px;
    color: #065F46;
    line-height: 1.8;
}
</style>
""", unsafe_allow_html=True)

# =========================================
   #pemuatan data
#========================================= 

from pathlib import Path
import pandas as pd
import streamlit as st

# Lokasi folder
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"

# Lokasi file CSV
FINAL_FILE = DATA_DIR / "enerva_final_analysis.csv"
ANOMALY_FILE = DATA_DIR / "enerva_anomalies.csv"

@st.cache_data
def load_enerva_data():
    # Periksa keberadaan file
    if not FINAL_FILE.exists():
        raise FileNotFoundError(f"File tidak ditemukan: {FINAL_FILE}")

    if not ANOMALY_FILE.exists():
        raise FileNotFoundError(f"File tidak ditemukan: {ANOMALY_FILE}")

    # Baca kedua file CSV
    final_data = pd.read_csv(FINAL_FILE, encoding="utf-8-sig")
    anomaly_data = pd.read_csv(ANOMALY_FILE, encoding="utf-8-sig")

    return final_data, anomaly_data


# Memuat data
try:
    enerva_result, enerva_anomalies = load_enerva_data()
    

except Exception as e:
    st.error(f"Gagal memuat data: {e}")
    st.stop()

# =========================================================
# SIDEBAR
# =========================================================
with st.sidebar:
    st.markdown("""
    <div style="text-align:center; padding:25px 20px;">
        <div style="font-size:80px;">⚡</div>
        <h2 style="margin:0;font-size:30px">ENERVA</h2>
        <p style="font-size:16px; color:#D1FAE5;">
            Energy + Observe + Awarness
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    st.markdown("### MENU")

    menu = st.radio(
        "Pilih Halaman",
        ["Beranda", "Informasi Dataset", "Analisis Konsumsi Listrik", "Deteksi Anomali", "Cek Konsumsi Listrik"],
        label_visibility="collapsed"
    )

    st.divider()
    st.caption("Dashboard Interaktif")
    st.caption("Sistem Monitoring Konsumsi Listrik Rumah Tangga")

# =========================================================
# HALAMAN: BERANDA
# =========================================================
if menu == "Beranda":
    st.markdown("""
    <div class="hero">
        <div style="font-size:14px; font-weight:700; letter-spacing:2px;">
            ENERGY MONITORING SYSTEM
        </div>
        <h1>ENERVA</h1>
        <p>Sistem cerdas pemantauan energi dan deteksi anomali konsumsi listrik rumah tangga.</p>
        <div style="
            display:inline-block;
            background:#F59E0B;
            color:#064E3B;
            padding:9px 18px;
            border-radius:30px;
            font-weight:700;
            margin-top:10px;">
            Smart Energy Analysis
        </div>
    </div>
    """, unsafe_allow_html=True)

# =========================================================
# MENGENAL ENERVA
# =========================================================
    st.markdown('<div class="section-title">Mengenal ENERVA</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="section-description">
        ENERVA merupakan dashboard analisis energi listrik yang
        berfokus pada pemantauan pola konsumsi dan pendeteksian
        anomali. Sistem ini memanfaatkan pendekatan analisis data
        untuk menemukan kondisi penggunaan listrik yang berbeda
        dari pola umumnya.
    </div>
    """, unsafe_allow_html=True)

    st.write("")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        <div class="info-card">
            <h3>📊 Monitoring Energi</h3>
            <p>Membantu memahami perubahan dan pola konsumsi energi berdasarkan variabel pengukuran listrik.</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="info-card">
            <h3>🔍 Deteksi Anomali</h3>
            <p>Mengidentifikasi pengamatan yang memiliki karakteristik berbeda dari pola konsumsi pada umumnya.</p>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class="info-card">
            <h3>💡 Rekomendasi</h3>
            <p>Menyajikan rekomendasi berdasarkan kategori anomali yang ditemukan dalam proses analisis.</p>
        </div>
        """, unsafe_allow_html=True)

# =========================================================
# LATAR BELAKANG DAN TUJUAN
# =========================================================
    st.markdown('<div class="section-title">Latar Belakang dan Tujuan</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="section-description">
        Penggunaan energi listrik rumah tangga menghasilkan pola konsumsi yang dapat berubah dari waktu ke waktu.
        Perubahan tersebut tidak selalu mudah dikenali hanya melalui pengamatan data biasa.
    </div>
    """, unsafe_allow_html=True)

    st.write("")
    background1, background2 = st.columns(2)

    with background1:
        st.markdown("""
        <div class="info-card">
            <h3>⚠️ Permasalahan</h3>
            <p>Pola konsumsi listrik dapat berubah-ubah berdasarkan waktu dan aktivitas rumah tangga secara manual.</p>
        </div>
        """, unsafe_allow_html=True)

    with background2:
        st.markdown("""
        <div class="info-card">
            <h3>🎯 Tujuan Pengembangan</h3>
            <p>Membantu pengguna memahami pola konsumsi, mendeteksi anomali, dan memperoleh rekomendasi efisiensi energi.</p>
        </div>
        """, unsafe_allow_html=True)

# =========================================================
# METODE ANALISIS
# =========================================================
    st.markdown('<div class="section-title">Metode Analisis ENERVA</div>', unsafe_allow_html=True)
    method1, method2 = st.columns(2)

    with method1:
        st.markdown("""
        <div class="info-card">
            <h3>Median Absolute Deviation (MAD)</h3>
            <p>Metode statistik yang menggunakan median dan deviasi absolut untuk mengukur penyimpangan dari nilai pusat data.</p>
        </div>
        """, unsafe_allow_html=True)

    with method2:
        st.markdown("""
        <div class="info-card">
            <h3>Isolation Forest (IF)</h3>
            <p>Metode machine learning unsupervised yang mengidentifikasi anomali dengan mengisolasi karakteristik berbeda.</p>
        </div>
        """, unsafe_allow_html=True)
# =========================================================
# ALUR KERJA ENERVA
# =========================================================
    st.markdown('<div class="section-title">Alur Kerja ENERVA</div>', unsafe_allow_html=True)
    workflow = [
        ("01", "Data Konsumsi Listrik", "Data penggunaan energi listrik rumah tangga menjadi masukan sistem."),
        ("02", "Prapemrosesan Data", "Data disiapkan dan diolah agar dapat digunakan dalam proses analisis."),
        ("03", "Deteksi Anomali", "Metode MAD dan Isolation Forest digunakan untuk mengenali pola konsumsi yang tidak biasa."),
        ("04", "Pengelompokan Hasil", "Hasil kedua metode dibandingkan untuk menentukan kategori data normal dan anomali."),
        ("05", "Rekomendasi Energi", "Sistem menyajikan rekomendasi berdasarkan karakteristik konsumsi yang terdeteksi.")
    ]

    for number, title, description in workflow:
        st.markdown(f"""
        <div class="workflow-card">
            <h4>{number} &nbsp; | &nbsp; {title}</h4>
            <p>{description}</p>
        </div>
        """, unsafe_allow_html=True)

 # =========================================================
# KETERBATASAN SISTEM
# =========================================================       
    st.markdown('<div class="section-title">Keterbatasan Sistem</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="warning-card">
        <b>Hal yang perlu diperhatikan:</b>
        <ul>
            <li>
                Hasil deteksi anomali menunjukkan pola yang tidak biasa
                berdasarkan data, bukan bukti pasti adanya kerusakan
                perangkat atau pemborosan energi.
            </li>
            <li>
                Hasil deteksi dipengaruhi oleh karakteristik, kualitas,
                dan kelengkapan dataset yang digunakan.
            </li>
            <li>
                MAD dan Isolation Forest memiliki pendekatan yang berbeda,
                sehingga hasil deteksi keduanya tidak selalu sama.
            </li>
            <li>
                Rekomendasi yang diberikan bersifat informatif dan perlu
                disesuaikan dengan kondisi penggunaan listrik sebenarnya.
            </li>
            <li>
                Analisis berdasarkan data historis tidak secara langsung
                menjamin prediksi konsumsi energi pada masa mendatang.
            </li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("""
    <div class="footer">
        <b>ENERVA</b> — Energy Monitoring & Anomaly Detection System
        <br>Data-Driven Energy Analysis
    </div>
    """, unsafe_allow_html=True)

# =========================================================
# HALAMAN: INFORMASI DATASET
# =========================================================
elif menu == "Informasi Dataset":
   
    st.markdown("""
    <style>
    .dataset-header {
        background: linear-gradient(120deg, #064E3B, #0F766E, #1CC998);
        padding: 32px;
        border-radius: 18px;
        color: white;
        margin-bottom: 25px;
        box-shadow: 0 8px 25px rgba(6,78,59,0.13);
    }
    .dataset-header h1 {
        color: white;
        font-size: 30px;
        font-weight: 750;
        margin-bottom: 10px;
    }
    .dataset-header p {
        color: #D1FAE5;
        font-size: 15px;
        line-height: 1.7;
        margin-bottom: 0;
    }
    .section-heading {
        color: #064E3B;
        font-size: 21px;
        font-weight: 750;
        margin-top: 30px;
        margin-bottom: 7px;
    }
    .dataset-card {
        background: white;
        border: 1px solid #D1FAE5;
        border-radius: 15px;
        padding: 20px;
        min-height: 125px;
        box-shadow: 0 4px 13px rgba(6,78,59,0.045);
    }
    .dataset-card .icon {
        font-size: 25px;
        margin-bottom: 10px;
    }
    .dataset-card .label {
        color: #64748B;
        font-size: 13px;
        margin-bottom: 5px;
    }
    .dataset-card .value {
        color: #064E3B;
        font-size: 23px;
        font-weight: 750;
    }
    .variable-unit {
        display: inline-block;
        background: #D1FAE5;
        color: #047857;
        padding: 4px 9px;
        border-radius: 20px;
        font-size: 11px;
        font-weight: 650;
    }
    .process-card {
        background: white;
        border: 1px solid #D1FAE5;
        border-radius: 13px;
        padding: 17px 20px;
        margin-bottom: 12px;
    }
    .process-card h4 {
        color: #064E3B;
        font-size: 16px;
        margin-bottom: 6px;
    }
    .process-card p {
        color: #64748B;
        font-size: 14px;
        line-height: 1.6;
        margin-bottom: 0;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="dataset-header">
        <h1>📈 Informasi Dataset</h1>
        <p>Kenali sumber data, karakteristik, dan variabel yang digunakan dalam proses analisis konsumsi energi listrik.</p>
    </div>
    """, unsafe_allow_html=True)


# =========================================================
# RINGKASAN DATASET
# =========================================================

    st.markdown(
        '<div class="section-heading">📌 Ringkasan Dataset</div>',
        unsafe_allow_html=True
    )

    # Menggunakan hasil analisis utama ENERVA
    dataset_view = enerva_result.copy()

    total_data = len(dataset_view)
    total_variabel = len(dataset_view.columns)
    missing_data = int(dataset_view.isnull().sum().sum())

    tanggal_awal = "16 Des 2006"
    tanggal_akhir = "26 Nov 2010"

    col1, col2, col3, col4 = st.columns(4)

    metrics = [
        (col1, "📁", "Total Observasi", f"{total_data:,}"),
        (col2, "🎛️", "Jumlah Variabel", str(total_variabel)),
        (col3, "🧹", "Missing Values", f"{missing_data:,}"),
        (col4, "⏱️", "Resolusi Data", "Per Jam")
    ]

    for col, icon, label, value in metrics:

        with col:

            st.markdown(f"""
            <div class="dataset-card">
                <div class="icon">{icon}</div>
                <div class="label">{label}</div>
                <div class="value">{value}</div>
            </div>
            """, unsafe_allow_html=True)

# =========================================================
# SUMBER DATASET
# =========================================================
    st.markdown('<div class="section-heading">🌐 Sumber Dataset</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="info-card" style="margin-bottom: 10px;">
        <h4>Individual Household Electric Power Consumption</h4>
        <p>
            Dataset ini berasal dari <a href="https://archive.ics.uci.edu/dataset/235/individual%2Bhousehold%2Belectric%2Bpower%2BConsumption" target="_blank" style="color: #047857; font-weight: 600;">UCI Machine Learning Repository</a>.
            Data berisi catatan konsumsi listrik sebuah rumah tangga di Prancis dengan pencatatan data konsumsi listrik per menit.
        </p>
    </div>
    """, unsafe_allow_html=True)

    col_s1, col_s2 = st.columns(2)
    with col_s1:
        st.markdown("""
        <div class="dataset-card">
            <div class="label">📚 Repository</div>
            <div class="value" style="font-size:18px;">
                <a href="https://archive.ics.uci.edu/dataset/235/individual%2Bhousehold%2Belectric%2Bpower%2BConsumption" target="_blank" style="color: #064E3B; text-decoration: none;">UCI Machine Learning ↗</a>
            </div>
            <p style="color:#64748B; font-size:13px;">Repository penyedia dataset pembelajaran machine learning.</p>
        </div>
        """, unsafe_allow_html=True)

    with col_s2:
        st.markdown(f"""
        <div class="dataset-card">
            <div class="label">📅 Periode Data yang Diolah</div>
            <div class="value" style="font-size:17px;">
                {tanggal_awal} – {tanggal_akhir}
            </div>
            <p style="color:#64748B; font-size:13px;">Rentang waktu berdasarkan hasil preprocessing per jam.</p>
        </div>
        """, unsafe_allow_html=True)

# =========================================================
# VARIABEL DATASET
# =========================================================
    st.markdown('<div class="section-heading">⚡ Variabel Dataset</div>', unsafe_allow_html=True)
    variables = [
        ("⚡", "Global Active Power", "Total daya listrik aktif yang digunakan oleh rumah tangga.", "kilowatt (kW)"),
        ("🔋", "Global Reactive Power", "Besarnya daya reaktif yang digunakan oleh rumah tangga.", "kilovar (kVAR)"),
        ("🔌", "Voltage", "Tegangan listrik rata-rata yang disuplai ke rumah tangga.", "volt (V)"),
        ("📶", "Global Intensity", "Intensitas arus listrik yang digunakan oleh rumah tangga.", "ampere (A)"),
        ("🏠", "Sub Metering 1", "Energi listrik yang digunakan pada area dapur.", "watt-hour (Wh)"),
        ("🧺", "Sub Metering 2", "Energi listrik yang digunakan pada area laundry.", "watt-hour (Wh)"),
        ("🌡️", "Sub Metering 3", "Energi listrik yang digunakan oleh pemanas air dan pendingin ruangan.", "watt-hour (Wh)")
    ]

    for i in range(0, len(variables), 2):
        cols = st.columns(2)
        for j, col in enumerate(cols):
            index = i + j
            if index < len(variables):
                icon, name, description, unit = variables[index]
                with col:
                    st.markdown(f"""
                    <div class="variable-card">
                        <h4 style="font-size: 16px;">{icon} {name}</h4>
                        <p>{description}</p>
                        <span class="variable-unit">{unit}</span>
                    </div>
                    """, unsafe_allow_html=True)

# =========================================================
# PENGOLAHAN DATASET
# =========================================================
    st.markdown('<div class="section-heading">🛠️ Pengolahan Dataset</div>', unsafe_allow_html=True)
    processes = [
        ("01", "Pemeriksaan Data", "Memeriksa struktur dataset, tipe data, dan kelengkapan nilai."),
        ("02", "Pembersihan Data", "Menangani nilai yang hilang agar data siap digunakan."),
        ("03", "Konversi Waktu", "Menggabungkan informasi tanggal dan waktu menjadi indeks DateTime."),
        ("04", "Agregasi Per Jam", "Mengolah data berdasarkan interval waktu per jam untuk memperoleh data terstruktur."),
        ("05", "Data Siap Dianalisis", "Menghasilkan dataset bersih untuk metode MAD dan Isolation Forest.")
    ]

    for number, title, description in processes:
        st.markdown(f"""
        <div class="process-card">
            <div style="display:flex; align-items:flex-start; gap:15px;">
                <div style="background:#D1FAE5; color:#047857; font-size:15px; font-weight:750; padding:9px 12px; border-radius:9px;">{number}</div>
                <div>
                    <h4>{title}</h4>
                    <p>{description}</p>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

# =========================================================
# PREVIEW DATASET
# =========================================================
    st.markdown('<div class="section-heading">🗂️ Preview Dataset Hasil Analisis</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="section-description">
        Berikut merupakan beberapa baris data hasil pembersihan dan agregasi data per jam serta hasil analisis pada konsumsi listrik salah satu rumah tangga di Sceaux, Prancis.
    </div>
    """, unsafe_allow_html=True)

    st.dataframe(
    enerva_result.head(10),
    use_container_width=True,
    height=370
    )
    st.caption(f"Menampilkan 10 dari total {total_data:,} observasi hasil preprocessing.")

    # Tombol Unduh Data Preprocessing
    csv_data = enerva_result.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Unduh Data Hasil Preprocessing (CSV)",
        data=csv_data,
        file_name="enerva_preprocessed_hourly_data.csv",
        mime="text/csv",
        help="Klik untuk mengunduh seluruh data hasil agregasi per jam dari enerva_core."
    )

# =========================================================
# CATATAN DATASET
# =========================================================
    st.markdown("""
    <div class="info-card" style="margin-top: 20px;">
        <h4>💡 Catatan Dataset</h4>
        <p>
            Tujuh variabel di atas merupakan fitur utama yang digunakan sebagai dasar analisis. Kolom seperti MAD Score, 
            Isolation Forest Score, kategori anomali, dan rekomendasi merupakan hasil pengolahan sistem ENERVA.
        </p>
    </div>
    """, unsafe_allow_html=True)



# =========================================================
# SECTION 3: ANALISIS KONSUMSI LISTRIK
# =========================================================

elif menu == "Analisis Konsumsi Listrik":

    # -----------------------------------------------------
    # 1. PERSIAPAN DATA DAN VALIDASI WAKTU
    # -----------------------------------------------------

    analysis_data = enerva_result.copy()

    # Pastikan waktu tersedia sebagai DatetimeIndex
    if not isinstance(analysis_data.index, pd.DatetimeIndex):

        datetime_col = None

        # Cari kolom waktu yang mungkin tersedia
        possible_datetime_cols = [
            "DateTime", "Datetime", "datetime",
            "Timestamp", "timestamp"
        ]

        for col in possible_datetime_cols:
            if col in analysis_data.columns:
                datetime_col = col
                break

        if datetime_col is not None:
            parsed_time = pd.to_datetime(
                analysis_data[datetime_col],
                dayfirst=True,
                errors="coerce"
            )

            analysis_data = analysis_data.drop(
                columns=[datetime_col]
            )
            analysis_data.index = parsed_time

        elif "Date" in analysis_data.columns and "Time" in analysis_data.columns:

            parsed_time = pd.to_datetime(
                analysis_data["Date"].astype(str)
                + " "
                + analysis_data["Time"].astype(str),
                dayfirst=True,
                errors="coerce"
            )

            analysis_data = analysis_data.drop(
                columns=["Date", "Time"]
            )
            analysis_data.index = parsed_time

        else:
            # Menangani CSV yang menyimpan indeks waktu
            # sebagai kolom pertama, misalnya Unnamed: 0
            possible_index_cols = [
                col for col in analysis_data.columns
                if str(col).startswith("Unnamed:")
            ]

            if possible_index_cols:
                index_col = possible_index_cols[0]

                parsed_time = pd.to_datetime(
                    analysis_data[index_col],
                    dayfirst=True,
                    errors="coerce"
                )

                if parsed_time.notna().sum() > 0:
                    analysis_data = analysis_data.drop(
                        columns=[index_col]
                    )
                    analysis_data.index = parsed_time

    # Validasi indeks waktu
    if not isinstance(analysis_data.index, pd.DatetimeIndex):

        st.error(
            "Kolom waktu tidak ditemukan dalam "
            "enerva_final_analysis.csv. "
            "Pastikan file menyimpan indeks DateTime."
        )
        st.stop()

    # Hapus waktu yang tidak valid
    analysis_data = analysis_data.loc[
        analysis_data.index.notna()
    ].copy()

    # Urutkan berdasarkan waktu
    analysis_data = analysis_data.sort_index()

    # Hilangkan indeks waktu yang duplikat
    analysis_data = analysis_data[
        ~analysis_data.index.duplicated(keep="first")
    ]

    # -----------------------------------------------------
    # 2. VALIDASI VARIABEL KELISTRIKAN
    # -----------------------------------------------------

    FEATURES = [
        "Global_active_power",
        "Global_reactive_power",
        "Voltage",
        "Global_intensity",
        "Sub_metering_1",
        "Sub_metering_2",
        "Sub_metering_3"
    ]

    available_features = [
        col for col in FEATURES
        if col in analysis_data.columns
    ]

    if "Global_active_power" not in analysis_data.columns:
        st.error(
            "Kolom Global_active_power tidak ditemukan "
            "dalam file enerva_final_analysis.csv."
        )
        st.stop()

    # Pastikan variabel pengukuran berupa angka
    for col in available_features:
        analysis_data[col] = pd.to_numeric(
            analysis_data[col],
            errors="coerce"
        )

    analysis_data = analysis_data.dropna(
        subset=["Global_active_power"]
    )

    if analysis_data.empty:
        st.error("Tidak terdapat data konsumsi listrik yang valid.")
        st.stop()

    # -----------------------------------------------------
    # 3. HEADER SECTION 3
    # -----------------------------------------------------
    st.markdown("""
    <style>
    .dataset-header {
        background: linear-gradient(
            120deg,
            #064E3B,
            #0F766E,
            #1CC998
        );
        padding: 32px 38px;
        border-radius: 18px;
        color: white;
        margin-bottom: 25px;
        box-shadow: 0 8px 25px rgba(6,78,59,0.13);
    }

    .dataset-header h1 {
        color: #FFFFFF;
        font-size: 30px;
        font-weight: 800;
        margin: 0 0 12px 0;
    }

    .dataset-header p {
        color: #D1FAE5;
        font-size: 15px;
        line-height: 1.8;
        margin: 0;
    }
    </style>
    """, unsafe_allow_html=True)
    st.markdown("""
    <div class="dataset-header">
        <h1>⚡ Analisis Konsumsi Energi</h1>
        <p>
            Visualisasi pola penggunaan energi listrik berdasarkan
            hasil preprocessing dataset ENERVA dengan interval waktu per jam.
        </p>
    </div>
    """, unsafe_allow_html=True)


    # -----------------------------------------------------
    # 4. FILTER PERIODE ANALISIS
    # -----------------------------------------------------

    st.markdown(
        '<div class="analysis-heading">📅 Periode Analisis</div>',
        unsafe_allow_html=True
    )

    st.markdown("""
    <div class="analysis-description">
        Pilih rentang tanggal untuk melihat karakteristik
        konsumsi listrik pada periode tertentu.
    </div>
    """, unsafe_allow_html=True)

    min_date = analysis_data.index.min().date()
    max_date = analysis_data.index.max().date()

    selected_dates = st.date_input(
        "Pilih rentang tanggal analisis:",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date,
        key="analysis_date_range"
    )

    if isinstance(selected_dates, (tuple, list)):

        if len(selected_dates) == 2:
            start_date, end_date = selected_dates

            filtered_data = analysis_data.loc[
                (analysis_data.index.date >= start_date)
                & (analysis_data.index.date <= end_date)
            ].copy()
        else:
            filtered_data = analysis_data.copy()

    else:
        filtered_data = analysis_data.copy()

    if filtered_data.empty:

        st.warning(
            "Tidak terdapat data pada rentang tanggal yang dipilih."
        )

    else:

        # -------------------------------------------------
        # 5. RINGKASAN KONSUMSI LISTRIK
        # -------------------------------------------------

        st.markdown(
            '<div class="analysis-heading">'
            '📊 Ringkasan Konsumsi Listrik'
            '</div>',
            unsafe_allow_html=True
        )

        avg_power = filtered_data[
            "Global_active_power"
        ].mean()

        max_power = filtered_data[
            "Global_active_power"
        ].max()

        if "Voltage" in filtered_data.columns:
            avg_voltage = filtered_data["Voltage"].mean()
        else:
            avg_voltage = np.nan

        if "Global_intensity" in filtered_data.columns:
            avg_intensity = filtered_data["Global_intensity"].mean()
        else:
            avg_intensity = np.nan

        col1, col2, col3, col4 = st.columns(4)

        metrics = [
            (
                col1,
                "⚡",
                "Rata-rata Daya Aktif",
                f"{avg_power:,.3f} kW"
            ),
            (
                col2,
                "📈",
                "Daya Aktif Tertinggi",
                f"{max_power:,.3f} kW"
            ),
            (
                col3,
                "🔌",
                "Rata-rata Tegangan",
                f"{avg_voltage:,.2f} V"
                if pd.notna(avg_voltage) else "Tidak tersedia"
            ),
            (
                col4,
                "📊",
                "Rata-rata Intensitas",
                f"{avg_intensity:,.2f} A"
                if pd.notna(avg_intensity) else "Tidak tersedia"
            )
        ]

        for col, icon, label, value in metrics:

            with col:
                st.markdown(f"""
                <div class="analysis-card">
                    <div class="card-icon">{icon}</div>
                    <div class="card-label">{label}</div>
                    <div class="card-value">{value}</div>
                </div>
                """, unsafe_allow_html=True)

        st.caption(
            f"Total observasi: {len(filtered_data):,} jam."
        )

        # -------------------------------------------------
        # 6. TREN KONSUMSI DAYA AKTIF
        # -------------------------------------------------

        st.markdown(
            '<div class="analysis-heading">'
            '📈 Tren Konsumsi Daya Aktif'
            '</div>',
            unsafe_allow_html=True
        )

        st.markdown("""
        <div class="analysis-description">
            Grafik memperlihatkan perubahan rata-rata daya aktif
            listrik berdasarkan waktu pengamatan.
        </div>
        """, unsafe_allow_html=True)

        daily_power = (
            filtered_data["Global_active_power"]
            .resample("D")
            .mean()
            .dropna()
        )

        fig_power = go.Figure()

        fig_power.add_trace(go.Scatter(
            x=daily_power.index,
            y=daily_power.values,
            mode="lines",
            name="Rata-rata Daya Aktif",
            line=dict(color="#059669", width=2),
            fill="tozeroy",
            fillcolor="rgba(28,201,152,0.10)"
        ))

        fig_power.update_layout(
            height=400,
            template="plotly_white",
            xaxis_title="Tanggal",
            yaxis_title="Daya Aktif (kW)",
            hovermode="x unified",
            margin=dict(l=20, r=20, t=30, b=20)
        )

        st.plotly_chart(
            fig_power,
            use_container_width=True
        )

        # -------------------------------------------------
        # 7. ANALISIS VARIABEL KELISTRIKAN
        # -------------------------------------------------

        st.markdown(
            '<div class="analysis-heading">'
            '🔍 Analisis Variabel Kelistrikan'
            '</div>',
            unsafe_allow_html=True
        )

        st.markdown("""
        <div class="analysis-description">
            Perbandingan karakteristik daya reaktif dan tegangan
            listrik berdasarkan hasil pengamatan.
        </div>
        """, unsafe_allow_html=True)

        numeric_data = filtered_data[
            available_features
        ].select_dtypes(include=[np.number])

        daily_data = numeric_data.resample("D").mean()

        col_left, col_right = st.columns(2)

        with col_left:

            if "Global_reactive_power" in daily_data.columns:

                fig_reactive = px.line(
                    daily_data,
                    x=daily_data.index,
                    y="Global_reactive_power",
                    title="Tren Daya Reaktif",
                    labels={
                        "x": "Tanggal",
                        "Global_reactive_power": "Daya Reaktif (kVAR)"
                    }
                )

                fig_reactive.update_traces(
                    line_color="#0F766E",
                    line_width=2
                )

                fig_reactive.update_layout(
                    height=350,
                    template="plotly_white"
                )

                st.plotly_chart(
                    fig_reactive,
                    use_container_width=True
                )

            else:
                st.info("Kolom daya reaktif tidak tersedia.")

        with col_right:

            if "Voltage" in daily_data.columns:

                fig_voltage = px.line(
                    daily_data,
                    x=daily_data.index,
                    y="Voltage",
                    title="Tren Tegangan Listrik",
                    labels={
                        "x": "Tanggal",
                        "Voltage": "Tegangan (V)"
                    }
                )

                fig_voltage.update_traces(
                    line_color="#F59E0B",
                    line_width=2
                )

                fig_voltage.update_layout(
                    height=350,
                    template="plotly_white"
                )

                st.plotly_chart(
                    fig_voltage,
                    use_container_width=True
                )

            else:
                st.info("Kolom tegangan tidak tersedia.")

        # -------------------------------------------------
        # 8. DISTRIBUSI PENGGUNAAN ENERGI
        # -------------------------------------------------

        st.markdown(
            '<div class="analysis-heading">'
            '🏠 Distribusi Penggunaan Energi'
            '</div>',
            unsafe_allow_html=True
        )

        st.markdown("""
        <div class="analysis-description">
            Distribusi rata-rata penggunaan listrik berdasarkan
            tiga variabel sub-metering pada dataset.
        </div>
        """, unsafe_allow_html=True)

        sub_meter_columns = [
            "Sub_metering_1",
            "Sub_metering_2",
            "Sub_metering_3"
        ]

        available_sub = [
            col for col in sub_meter_columns
            if col in filtered_data.columns
        ]

        if available_sub:

            sub_values = filtered_data[available_sub].mean()

            sub_labels = {
                "Sub_metering_1": "Dapur",
                "Sub_metering_2": "Laundry",
                "Sub_metering_3": "AC & Pemanas Air"
            }

            fig_sub = px.bar(
                x=[
                    sub_labels.get(col, col)
                    for col in sub_values.index
                ],
                y=sub_values.values,
                text_auto=".2f",
                labels={
                    "x": "Kategori Penggunaan",
                    "y": "Rata-rata Sub-metering"
                },
                title="Rata-rata Penggunaan Sub-metering"
            )

            fig_sub.update_traces(
                marker_color="#059669"
            )

            fig_sub.update_layout(
                height=380,
                template="plotly_white",
                showlegend=False
            )

            st.plotly_chart(
                fig_sub,
                use_container_width=True
            )

        else:
            st.info("Data sub-metering tidak tersedia.")

        # -------------------------------------------------
        # 9. STATISTIK DESKRIPTIF
        # -------------------------------------------------

        st.markdown(
            '<div class="analysis-heading">'
            '📋 Statistik Deskriptif Konsumsi Listrik'
            '</div>',
            unsafe_allow_html=True
        )

        descriptive_columns = [
            col for col in available_features
            if col in filtered_data.columns
        ]

        if descriptive_columns:

            descriptive_stats = filtered_data[
                descriptive_columns
            ].describe().T

            descriptive_stats = descriptive_stats.rename(
                columns={
                    "count": "Jumlah Data",
                    "mean": "Rata-rata",
                    "std": "Standar Deviasi",
                    "min": "Minimum",
                    "25%": "Q1",
                    "50%": "Median",
                    "75%": "Q3",
                    "max": "Maksimum"
                }
            )

            st.dataframe(
                descriptive_stats.round(3),
                use_container_width=True
            )

        else:
            st.info("Tidak tersedia variabel numerik untuk statistik.")

        # -------------------------------------------------
        # 10. CATATAN ANALISIS
        # -------------------------------------------------

        st.markdown("""
        <div class="analysis-note">
            <b>💡 Catatan Analisis</b><br>
            Hasil visualisasi menggambarkan karakteristik konsumsi
            listrik berdasarkan periode yang dipilih. Perubahan
            daya aktif, daya reaktif, tegangan, intensitas, dan
            sub-metering dapat digunakan untuk memahami pola
            penggunaan energi sebelum dilakukan proses deteksi
            anomali.
        </div>
        """, unsafe_allow_html=True)

        # -------------------------------------------------
        # 11. UNDUH DATA ANALISIS
        # -------------------------------------------------

        st.markdown(
            '<div class="analysis-heading">'
            '📥 Unduh Data Analisis'
            '</div>',
            unsafe_allow_html=True
        )

        csv_analysis = filtered_data.to_csv(
            index=True,
            index_label="DateTime"
        ).encode("utf-8-sig")

        st.download_button(
            label="📥 Unduh Data Periode Analisis (CSV)",
            data=csv_analysis,
            file_name="enerva_analysis_data.csv",
            mime="text/csv"
        )

        # -------------------------------------------------
        # 12. FOOTER
        # -------------------------------------------------

        st.markdown("""
        <div class="footer">
            <b>ENERVA</b> — Energy Monitoring & Anomaly Detection System
            <br>Data-Driven Energy Analysis
        </div>
        """, unsafe_allow_html=True)


# =========================================================
# SECTION 4: DETEKSI ANOMALI DAN REKOMENDASI
# =========================================================

elif menu == "Deteksi Anomali":

    # -----------------------------------------------------
    # 1. HEADER SECTION 4
    # -----------------------------------------------------
    st.markdown("""
    <style>
    .dataset-header {
        background: linear-gradient(
            120deg,
            #064E3B,
            #0F766E,
            #1CC998
        );
        padding: 32px 38px;
        border-radius: 18px;
        color: white;
        margin-bottom: 25px;
        box-shadow: 0 8px 25px rgba(6,78,59,0.13);
    }

    .dataset-header h1 {
        color: #FFFFFF;
        font-size: 30px;
        font-weight: 800;
        margin: 0 0 12px 0;
    }

    .dataset-header p {
        color: #D1FAE5;
        font-size: 15px;
        line-height: 1.8;
        margin: 0;
    }
    </style>
    """, unsafe_allow_html=True)
    st.markdown("""
    <div class="dataset-header">
        <h1>🚨 Deteksi Anomali dan Rekomendasi</h1>
        <p>
            Identifikasi pola konsumsi listrik yang tidak biasa
            menggunakan metode Median Absolute Deviation (MAD)
            dan Isolation Forest, disertai rekomendasi penggunaan
            energi berdasarkan hasil analisis ENERVA.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # -----------------------------------------------------
    # 2. PERSIAPAN DATA
    # -----------------------------------------------------

    detection_view = enerva_result.copy()

    # Pastikan indeks waktu berbentuk DatetimeIndex
    if not isinstance(detection_view.index, pd.DatetimeIndex):

        if "DateTime" in detection_view.columns:
            detection_view["DateTime"] = pd.to_datetime(
                detection_view["DateTime"],
                errors="coerce"
            )
            detection_view = detection_view.set_index("DateTime")

        else:
            st.error(
                "Indeks waktu tidak ditemukan. "
                "Pastikan hasil preprocessing memiliki DateTime."
            )
            st.stop()

    detection_view = detection_view[
        ~detection_view.index.isna()
    ].sort_index()

    required_columns = [
        "Global_active_power",
        "MAD_Score",
        "MAD_Anomaly",
        "IF_Score",
        "IF_Anomaly",
        "Anomaly_Category",
        "Recommendation"
    ]

    missing_columns = [
        col for col in required_columns
        if col not in detection_view.columns
    ]

    if missing_columns:
        st.error(
            f"Kolom hasil deteksi belum tersedia: {missing_columns}"
        )
        st.stop()

    # Pastikan kolom deteksi berbentuk boolean
    detection_view["MAD_Anomaly"] = (
        detection_view["MAD_Anomaly"].astype(bool)
    )

    detection_view["IF_Anomaly"] = (
        detection_view["IF_Anomaly"].astype(bool)
    )

    mad_flag = detection_view["MAD_Anomaly"]
    if_flag = detection_view["IF_Anomaly"]

    both_flag = mad_flag & if_flag

    # -----------------------------------------------------
    # 3. FILTER PERIODE
    # -----------------------------------------------------

    st.markdown(
        '<div class="section-heading">📅 Periode Deteksi Anomali</div>',
        unsafe_allow_html=True
    )

    min_date = detection_view.index.min().date()
    max_date = detection_view.index.max().date()

    selected_dates = st.date_input(
        "Pilih rentang tanggal:",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date,
        key="anomaly_date_range"
    )

    if isinstance(selected_dates, (tuple, list)) and len(selected_dates) == 2:

        start_date, end_date = selected_dates

        if start_date > end_date:
            st.warning("Tanggal awal tidak boleh melebihi tanggal akhir.")
            st.stop()

        detection_view = detection_view.loc[
            (detection_view.index.date >= start_date) &
            (detection_view.index.date <= end_date)
        ].copy()

    else:
        st.info("Silakan pilih tanggal awal dan akhir.")
        st.stop()

    if detection_view.empty:
        st.warning("Tidak terdapat data pada periode yang dipilih.")
        st.stop()

    # -----------------------------------------------------
    # 4. RINGKASAN DETEKSI ANOMALI
    # -----------------------------------------------------

    st.markdown(
        '<div class="section-heading">📊 Ringkasan Hasil Deteksi</div>',
        unsafe_allow_html=True
    )

    total_data = len(detection_view)

    mad_flag = detection_view["MAD_Anomaly"]
    if_flag = detection_view["IF_Anomaly"]

    both_flag = mad_flag & if_flag

    total_anomaly = int((mad_flag | if_flag).sum())
    total_normal = total_data - total_anomaly

    anomaly_percentage = (
        total_anomaly / total_data * 100
    )

    col1, col2, col3, col4 = st.columns(4)

    metrics = [
        (col1, "📁", "Total Observasi", f"{total_data:,}"),
        (col2, "🚨", "Total Anomali", f"{total_anomaly:,}"),
        (col3, "✅", "Data Normal", f"{total_normal:,}"),
        (col4, "📈", "Persentase Anomali",
         f"{anomaly_percentage:.2f}%")
    ]

    for col, icon, label, value in metrics:
        with col:
            st.markdown(f"""
            <div class="dataset-card">
                <div class="icon">{icon}</div>
                <div class="label">{label}</div>
                <div class="value">{value}</div>
            </div>
            """, unsafe_allow_html=True)

    st.write("")

    # -----------------------------------------------------
    # 5. PERBANDINGAN METODE DETEKSI
    # -----------------------------------------------------

    st.markdown(
        '<div class="section-heading">🧠 Perbandingan Metode Deteksi</div>',
        unsafe_allow_html=True
    )

    col1, col2, col3 = st.columns(3)

    method_metrics = [
        (col1, "MAD", int(mad_flag.sum()),
         "Anomali berdasarkan Modified Z-score"),

        (col2, "Isolation Forest", int(if_flag.sum()),
         "Anomali berdasarkan Machine Learning"),

        (col3, "Kedua Metode", int(both_flag.sum()),
         "Anomali yang terdeteksi oleh kedua metode")
    ]

    for col, title, value, description in method_metrics:

        with col:
            st.markdown(f"""
            <div class="info-card">
                <h3>{title}</h3>
                <div style="
                    font-size:30px;
                    font-weight:800;
                    color:#064E3B;
                    margin:10px 0;">
                    {value:,}
                </div>
                <p>{description}</p>
            </div>
            """, unsafe_allow_html=True)

    st.caption(
        "Jumlah deteksi MAD dan Isolation Forest dapat beririsan. "
        "Karena itu, keduanya tidak boleh langsung dijumlahkan "
        "untuk memperoleh total anomali."
    )

    # -----------------------------------------------------
    # 6. DISTRIBUSI KATEGORI ANOMALI
    # -----------------------------------------------------

    st.markdown(
        '<div class="section-heading">📊 Distribusi Kategori Anomali</div>',
        unsafe_allow_html=True
    )

    category_order = [
        "Normal",
        "Anomali MAD Saja",
        "Anomali IF Saja",
        "Anomali Kedua Metode"
    ]

    category_counts = (
        detection_view["Anomaly_Category"]
        .value_counts()
        .reindex(category_order, fill_value=0)
        .rename_axis("Kategori")
        .reset_index(name="Jumlah")
    )

    fig_category = px.pie(
        category_counts,
        names="Kategori",
        values="Jumlah",
        hole=0.48,
        color="Kategori",
        color_discrete_map={
            "Normal": "#10B981",
            "Anomali MAD Saja": "#F59E0B",
            "Anomali IF Saja": "#0F766E",
            "Anomali Kedua Metode": "#DC2626"
        }
    )

    fig_category.update_layout(
        template="plotly_white",
        height=420,
        legend_title="Kategori Deteksi"
    )

    st.plotly_chart(
        fig_category,
        use_container_width=True
    )

    # -----------------------------------------------------
    # 7. TREN ANOMALI BERDASARKAN WAKTU
    # -----------------------------------------------------

    st.markdown(
        '<div class="section-heading">📈 Tren Anomali Berdasarkan Waktu</div>',
        unsafe_allow_html=True
    )

    trend = detection_view.copy()

    trend["Status"] = np.where(
        trend["MAD_Anomaly"] | trend["IF_Anomaly"],
        "Anomali",
        "Normal"
    )

    trend_daily = (
        trend.groupby([
            pd.Grouper(freq="D"),
            "Status"
        ])
        .size()
        .reset_index(name="Jumlah")
    )

    trend_daily.columns = [
        "Tanggal",
        "Status",
        "Jumlah"
    ]

    fig_trend = px.bar(
        trend_daily,
        x="Tanggal",
        y="Jumlah",
        color="Status",
        barmode="stack",
        color_discrete_map={
            "Normal": "#10B981",
            "Anomali": "#DC2626"
        },
        labels={
            "Tanggal": "Tanggal",
            "Jumlah": "Jumlah Observasi"
        }
    )

    fig_trend.update_layout(
        template="plotly_white",
        height=400,
        hovermode="x unified"
    )

    st.plotly_chart(
        fig_trend,
        use_container_width=True
    )

    # -----------------------------------------------------
    # 8. DISTRIBUSI SKOR DETEKSI
    # -----------------------------------------------------

    st.markdown(
        '<div class="section-heading">🎯 Distribusi Skor Deteksi</div>',
        unsafe_allow_html=True
    )

    score1, score2 = st.columns(2)

    with score1:

        st.markdown("**Modified Z-score (MAD)**")

        fig_mad = px.histogram(
            detection_view,
            x="MAD_Score",
            color="MAD_Anomaly",
            nbins=40,
            color_discrete_map={
                False: "#10B981",
                True: "#DC2626"
            },
            labels={
                "MAD_Score": "MAD Score",
                "MAD_Anomaly": "Anomali"
            }
        )

        fig_mad.add_vline(
            x=3.5,
            line_dash="dash",
            line_color="#DC2626",
            annotation_text="Ambang 3,5"
        )

        fig_mad.update_layout(
            template="plotly_white",
            height=350
        )

        st.plotly_chart(
            fig_mad,
            use_container_width=True
        )

    with score2:

        st.markdown("**Isolation Forest Score**")

        fig_if = px.histogram(
            detection_view,
            x="IF_Score",
            color="IF_Anomaly",
            nbins=40,
            color_discrete_map={
                False: "#10B981",
                True: "#DC2626"
            },
            labels={
                "IF_Score": "Isolation Forest Score",
                "IF_Anomaly": "Anomali"
            }
        )

        fig_if.update_layout(
            template="plotly_white",
            height=350
        )

        st.plotly_chart(
            fig_if,
            use_container_width=True
        )

    st.caption(
        "MAD menggunakan ambang Modified Z-score > 3,5. "
        "Isolation Forest menggunakan model dengan contamination 0,02."
    )

    # -----------------------------------------------------
    # 9. REKOMENDASI PENGGUNAAN ENERGI
    # -----------------------------------------------------

    st.markdown(
        '<div class="section-heading">💡 Rekomendasi Penggunaan Energi</div>',
        unsafe_allow_html=True
    )

    st.markdown("""
    <div class="section-description">
        Rekomendasi diambil langsung dari hasil analisis ENERVA Core.
        Setiap rekomendasi disesuaikan dengan karakteristik konsumsi
        listrik pada waktu terdeteksi.
    </div>
    """, unsafe_allow_html=True)

    anomaly_view = detection_view.loc[
        detection_view["MAD_Anomaly"] |
        detection_view["IF_Anomaly"]
    ].copy()

    if anomaly_view.empty:

        st.success(
            "Tidak ditemukan anomali pada periode yang dipilih."
        )

    else:

        available_categories = [
            category for category in category_order[1:]
            if category in anomaly_view["Anomaly_Category"].values
        ]

        selected_category = st.selectbox(
            "Filter kategori anomali:",
            ["Semua Kategori"] + available_categories,
            key="recommendation_category_filter"
        )

        if selected_category != "Semua Kategori":

            recommendation_view = anomaly_view[
                anomaly_view["Anomaly_Category"] == selected_category
            ].copy()

        else:
            recommendation_view = anomaly_view.copy()

        recommendation_view = recommendation_view.sort_values(
            "MAD_Score",
            ascending=False
        )

        st.markdown(
            f"**Ditemukan {len(recommendation_view):,} "
            "observasi anomali pada kategori yang dipilih.**"
        )

        display_limit = 10

        for timestamp, row in recommendation_view.head(
            display_limit
        ).iterrows():

            category = row["Anomaly_Category"]

            if category == "Anomali Kedua Metode":
                icon = "🚨"
            elif category == "Anomali MAD Saja":
                icon = "📊"
            else:
                icon = "🔍"

            with st.expander(
                f"{icon} {timestamp.strftime('%d-%m-%Y %H:%M')} | {category}"
            ):

                st.markdown(
                    f"**Rekomendasi:** {row['Recommendation']}"
                )

                detail1, detail2, detail3 = st.columns(3)

                detail1.metric(
                    "Daya Aktif",
                    f"{row['Global_active_power']:.3f} kW"
                )

                detail2.metric(
                    "MAD Score",
                    f"{row['MAD_Score']:.3f}"
                )

                detail3.metric(
                    "IF Score",
                    f"{row['IF_Score']:.5f}"
                )

        if len(recommendation_view) > display_limit:

            st.info(
                f"Menampilkan {display_limit} rekomendasi pertama. "
                "Unduh hasil lengkap melalui tombol di bawah."
            )

        # -------------------------------------------------
        # 10. UNDUH HASIL DETEKSI
        # -------------------------------------------------

        st.markdown(
            '<div class="section-heading">📥 Unduh Hasil Deteksi</div>',
            unsafe_allow_html=True
        )

        download_data = recommendation_view.reset_index()

        csv_output = download_data.to_csv(
            index=False
        ).encode("utf-8-sig")

        st.download_button(
            label="Data Anomali dan Rekomendasi (CSV)",
            data=csv_output,
            file_name="enerva_hasil_deteksi_anomali.csv",
            mime="text/csv",
            use_container_width=True
        )

    # -----------------------------------------------------
    # 11. CATATAN METODOLOGI
    # -----------------------------------------------------

    st.markdown("""
    <div class="info-card" style="margin-top:25px;">
        <h3>💡 Catatan Metodologi</h3>
        <p>
            ENERVA menggabungkan metode Median Absolute Deviation
            (MAD) dan Isolation Forest untuk mendeteksi pola konsumsi
            listrik yang tidak biasa.
        </p>
        <p>
            Hasil deteksi merupakan indikasi statistik berdasarkan
            karakteristik dataset, bukan bukti pasti adanya kerusakan
            perangkat atau pemborosan energi.
        </p>
        <p>
            Rekomendasi yang diberikan bersifat informatif dan perlu
            disesuaikan dengan kondisi penggunaan listrik sebenarnya.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # -----------------------------------------------------
    # 12. FOOTER
    # -----------------------------------------------------

    st.markdown("""
    <div class="footer">
        <b>ENERVA</b> — Energy Monitoring & Anomaly Detection System
        <br>Data-Driven Energy Analysis
    </div>
    """, unsafe_allow_html=True)


# =========================================================
# SECTION 5: CEK KONSUMSI LISTRIK
# =========================================================

elif menu == "Cek Konsumsi Listrik":

    import io

    # -----------------------------------------------------
    # HEADER SECTION 5
    # -----------------------------------------------------
    st.markdown("""
    <style>
    .dataset-header {
        background: linear-gradient(
            120deg,
            #064E3B,
            #0F766E,
            #1CC998
        );
        padding: 32px 38px;
        border-radius: 18px;
        color: white;
        margin-bottom: 25px;
        box-shadow: 0 8px 25px rgba(6,78,59,0.13);
    }

    .dataset-header h1 {
        color: #FFFFFF;
        font-size: 30px;
        font-weight: 800;
        margin: 0 0 12px 0;
    }

    .dataset-header p {
        color: #D1FAE5;
        font-size: 15px;
        line-height: 1.8;
        margin: 0;
    }
    </style>
    """, unsafe_allow_html=True)
    st.markdown("""
    <div class="dataset-header">
        <h1>⚡ Cek Konsumsi Listrik</h1>
        <p>
            Analisis konsumsi listrik secara mandiri.
            Unggah dataset konsumsi listrik untuk mengetahui
            pola penggunaan energi, mendeteksi anomali,
            dan memperoleh rekomendasi penghematan energi.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # -----------------------------------------------------
    # CSS TAMBAHAN
    # -----------------------------------------------------

    st.markdown("""
    <style>
    .upload-card {
        background: white;
        border: 1px solid #D1FAE5;
        border-radius: 16px;
        padding: 24px;
        margin-bottom: 20px;
    }

    .result-card {
        background: white;
        border: 1px solid #D1FAE5;
        border-radius: 15px;
        padding: 20px;
        min-height: 135px;
        box-shadow: 0 4px 13px rgba(6,78,59,0.045);
    }

    .result-label {
        color: #64748B;
        font-size: 13px;
        margin-bottom: 8px;
    }

    .result-value {
        color: #064E3B;
        font-size: 26px;
        font-weight: 800;
    }

    .result-icon {
        font-size: 25px;
        margin-bottom: 10px;
    }

    .recommendation-card {
        background: #ECFDF5;
        border-left: 5px solid #059669;
        border-radius: 12px;
        padding: 17px;
        margin-bottom: 12px;
        color: #064E3B;
        line-height: 1.7;
    }
    </style>
    """, unsafe_allow_html=True)

    # -----------------------------------------------------
    # INFORMASI FITUR
    # -----------------------------------------------------

    st.markdown(
        '<div class="section-heading">📋 Analisis Konsumsi Mandiri</div>',
        unsafe_allow_html=True
    )

    st.markdown("""
    <div class="section-description">
        Fitur ini memungkinkan pengguna melakukan analisis
        konsumsi listrik menggunakan data milik sendiri.
        Hasil analisis akan ditampilkan secara otomatis
        setelah file berhasil diproses.
    </div>
    """, unsafe_allow_html=True)

    st.write("")

    # -----------------------------------------------------
    # UPLOAD DATASET
    # -----------------------------------------------------

    st.markdown("""
    <div class="upload-card">
        <h3 style="color:#064E3B;">📂 Unggah Dataset Konsumsi Listrik</h3>
        <p style="color:#64748B;">
            Pilih file CSV dengan struktur kolom sesuai
            format dataset ENERVA.
        </p>
    </div>
    """, unsafe_allow_html=True)

    uploaded_file = st.file_uploader(
        "Pilih file CSV",
        type=["csv"],
        key="user_electricity_file"
    )

    st.caption(
        "Format yang didukung: CSV dengan separator titik koma (;)."
    )

    # -----------------------------------------------------
    # PROSES ANALISIS
    # -----------------------------------------------------

    if uploaded_file is not None:

        try:

            # Mengembalikan posisi file ke awal
            uploaded_file.seek(0)

            # Analisis menggunakan fungsi inti ENERVA
            with st.spinner(
                "Sedang memproses dan menganalisis konsumsi listrik..."
            ):

                user_result, user_anomalies, user_summary, user_model = (
                    analyze_enerva(uploaded_file)
                )

            st.success(
                "Dataset berhasil diproses dan dianalisis!"
            )

            # -------------------------------------------------
            # RINGKASAN HASIL
            # -------------------------------------------------

            st.markdown(
                '<div class="section-heading">📊 Ringkasan Hasil Analisis</div>',
                unsafe_allow_html=True
            )

            col1, col2, col3, col4 = st.columns(4)

            metrics = [
                (
                    col1,
                    "📁",
                    "Total Observasi",
                    f"{user_summary['total_observations']:,}"
                ),
                (
                    col2,
                    "🚨",
                    "Total Anomali",
                    f"{user_summary['total_anomalies']:,}"
                ),
                (
                    col3,
                    "✅",
                    "Data Normal",
                    f"{user_summary['normal_observations']:,}"
                ),
                (
                    col4,
                    "📈",
                    "Anomali MAD",
                    f"{user_summary['mad_anomalies']:,}"
                )
            ]

            for col, icon, label, value in metrics:

                with col:

                    st.markdown(f"""
                    <div class="result-card">
                        <div class="result-icon">{icon}</div>
                        <div class="result-label">{label}</div>
                        <div class="result-value">{value}</div>
                    </div>
                    """, unsafe_allow_html=True)

            st.write("")

            # -------------------------------------------------
            # PERBANDINGAN METODE
            # -------------------------------------------------

            st.markdown(
                '<div class="section-heading">🔍 Perbandingan Metode Deteksi</div>',
                unsafe_allow_html=True
            )

            method_col1, method_col2, method_col3 = st.columns(3)

            comparison = [
                (
                    method_col1,
                    "MAD",
                    user_summary["mad_anomalies"]
                ),
                (
                    method_col2,
                    "Isolation Forest",
                    user_summary["if_anomalies"]
                ),
                (
                    method_col3,
                    "Kedua Metode",
                    user_summary["both_methods"]
                )
            ]

            for col, name, value in comparison:

                with col:

                    st.metric(
                        label=name,
                        value=f"{value:,} anomali"
                    )

            # -------------------------------------------------
            # GRAFIK NORMAL DAN ANOMALI
            # -------------------------------------------------

            st.markdown(
                '<div class="section-heading">📈 Visualisasi Hasil Deteksi</div>',
                unsafe_allow_html=True
            )

            category_counts = (
                user_result["Anomaly_Category"]
                .value_counts()
                .reset_index()
            )

            category_counts.columns = [
                "Kategori",
                "Jumlah"
            ]

            fig_category = px.pie(
                category_counts,
                names="Kategori",
                values="Jumlah",
                title="Distribusi Kategori Konsumsi Listrik",
                hole=0.45
            )

            fig_category.update_layout(
                template="plotly_white",
                height=400
            )

            st.plotly_chart(
                fig_category,
                use_container_width=True
            )

            # -------------------------------------------------
            # TREN KONSUMSI LISTRIK
            # -------------------------------------------------

            st.markdown(
                '<div class="section-heading">⚡ Tren Konsumsi Listrik</div>',
                unsafe_allow_html=True
            )

            fig_trend = go.Figure()

            fig_trend.add_trace(
                go.Scatter(
                    x=user_result.index,
                    y=user_result["Global_active_power"],
                    mode="lines",
                    name="Daya Aktif",
                    line=dict(color="#059669", width=1.5)
                )
            )

            if not user_anomalies.empty:

                fig_trend.add_trace(
                    go.Scatter(
                        x=user_anomalies.index,
                        y=user_anomalies["Global_active_power"],
                        mode="markers",
                        name="Anomali",
                        marker=dict(
                            color="#EF4444",
                            size=6
                        )
                    )
                )

            fig_trend.update_layout(
                title="Tren Daya Aktif dan Titik Anomali",
                xaxis_title="Waktu",
                yaxis_title="Daya Aktif (kW)",
                template="plotly_white",
                height=420,
                hovermode="x unified"
            )

            st.plotly_chart(
                fig_trend,
                use_container_width=True
            )

            # -------------------------------------------------
            # REKOMENDASI
            # -------------------------------------------------

            st.markdown(
                '<div class="section-heading">💡 Rekomendasi Konsumsi Listrik</div>',
                unsafe_allow_html=True
            )

            if not user_anomalies.empty:

                # Mengelompokkan rekomendasi yang sama
                recommendation_counts = (
                    user_anomalies["Recommendation"]
                    .value_counts()
                )

                for recommendation, count in recommendation_counts.items():

                    st.markdown(f"""
                    <div class="recommendation-card">
                        <b>💡 Rekomendasi</b>
                        <p>{recommendation}</p>
                        <small>
                            Ditemukan pada {count:,} observasi anomali.
                        </small>
                    </div>
                    """, unsafe_allow_html=True)

            else:

                st.info(
                    "Tidak ditemukan indikasi anomali "
                    "pada dataset yang diunggah."
                )

            # -------------------------------------------------
            # TABEL DETAIL ANOMALI
            # -------------------------------------------------

            st.markdown(
                '<div class="section-heading">🚨 Detail Data Anomali</div>',
                unsafe_allow_html=True
            )

            if not user_anomalies.empty:

                anomaly_display = user_anomalies.copy()

                anomaly_display.index.name = "Waktu"

                st.dataframe(
                    anomaly_display,
                    use_container_width=True,
                    height=400
                )

            else:

                st.info(
                    "Tidak terdapat data anomali untuk ditampilkan."
                )

            # -------------------------------------------------
            # PREVIEW SELURUH HASIL
            # -------------------------------------------------

            st.markdown(
                '<div class="section-heading">🗂️ Preview Hasil Analisis</div>',
                unsafe_allow_html=True
            )

            st.dataframe(
                user_result.head(20),
                use_container_width=True
            )

            # -------------------------------------------------
            # DOWNLOAD HASIL ANALISIS
            # -------------------------------------------------

            st.markdown(
                '<div class="section-heading">📥 Unduh Hasil Analisis</div>',
                unsafe_allow_html=True
            )

            csv_output = user_result.to_csv(
                index=True,
                index_label="DateTime"
            ).encode("utf-8-sig")

            st.download_button(
                label="📥 Unduh Seluruh Hasil Analisis (CSV)",
                data=csv_output,
                file_name="enerva_user_analysis.csv",
                mime="text/csv"
            )

            anomaly_csv = user_anomalies.to_csv(
                index=True,
                index_label="DateTime"
            ).encode("utf-8-sig")

            st.download_button(
                label="🚨 Unduh Data Anomali (CSV)",
                data=anomaly_csv,
                file_name="enerva_user_anomalies.csv",
                mime="text/csv"
            )

        except Exception as e:

            st.error(
                f"Terjadi kesalahan saat memproses dataset: {e}"
            )

            st.warning("""
            Pastikan file CSV memiliki kolom Date, Time,
            Global_active_power, Global_reactive_power,
            Voltage, Global_intensity, Sub_metering_1,
            Sub_metering_2, dan Sub_metering_3.

            Pastikan juga format tanggal dan waktu valid,
            serta data pengukuran menggunakan angka.
            """)

    else:

        st.info(
            "Silakan unggah file CSV untuk memulai analisis konsumsi listrik."
        )

    # -----------------------------------------------------
    # FOOTER
    # -----------------------------------------------------

    st.markdown("""
    <div class="footer">
        <b>ENERVA</b> — Energy Monitoring & Anomaly Detection System
        <br>Data-Driven Energy Analysis
    </div>
    """, unsafe_allow_html=True)
