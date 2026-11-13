
import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest

FEATURES = [
    'Global_active_power',
    'Global_reactive_power',
    'Voltage',
    'Global_intensity',
    'Sub_metering_1',
    'Sub_metering_2',
    'Sub_metering_3'
]

def preprocess_csv(file):

    # 1. Membaca file CSV
    df = pd.read_csv(
        file,
        sep=';',
        na_values=['?', ''],
        low_memory=False
    )

    # Membersihkan spasi pada nama kolom
    df.columns = df.columns.str.strip()

    # 2. Memeriksa kolom yang dibutuhkan
    required_columns = ['Date', 'Time'] + FEATURES

    missing_columns = [
        col for col in required_columns
        if col not in df.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Kolom berikut tidak ditemukan: {missing_columns}"
        )

    # 3. Menggabungkan Date dan Time
    df['DateTime'] = pd.to_datetime(
        df['Date'].astype(str) + ' ' + df['Time'].astype(str),
        dayfirst=True,
        errors='coerce'
    )

    # 4. Mengubah fitur listrik menjadi numerik
    for col in FEATURES:
        df[col] = pd.to_numeric(
            df[col],
            errors='coerce'
        )

    # 5. Menghapus data dengan waktu atau pengukuran tidak valid
    df = df.dropna(
        subset=['DateTime'] + FEATURES
    )

    # 6. Mengurutkan data berdasarkan waktu
    df = df.sort_values('DateTime')

    # 7. Menggunakan DateTime sebagai index
    df = df.set_index('DateTime')

    # 8. Mengagregasikan data menjadi rata-rata per jam
    hourly = df[FEATURES].resample('h').mean()

    # Menghapus jam yang tidak memiliki data
    hourly = hourly.dropna()

    # 9. Memastikan hasil preprocessing tidak kosong
    if hourly.empty:
        raise ValueError(
            "Tidak ada data valid setelah preprocessing."
        )

    return hourly


def detect_anomalies(hourly):

    result = hourly.copy()

    # =====================================
    # 1. DETEKSI ANOMALI MENGGUNAKAN MAD
    # =====================================

    power = result['Global_active_power']

    median_power = power.median()
    mad_value = np.median(
        np.abs(power - median_power)
    )

    if mad_value == 0:
        raise ValueError(
            "MAD bernilai nol. Data tidak cukup bervariasi."
        )

    # Modified Z-score
    result['MAD_Score'] = (
        0.6745 * np.abs(power - median_power) / mad_value
    )

    # Ambang 3.5
    result['MAD_Anomaly'] = (
        result['MAD_Score'] > 3.5
    )

    # =====================================
    # 2. DETEKSI ANOMALI ISOLATION FOREST
    # =====================================

    model = IsolationForest(
        n_estimators=200,
        contamination=0.02,
        random_state=42,
        n_jobs=-1
    )

    # Melatih model menggunakan 7 fitur listrik
    model.fit(result[FEATURES])

    # Prediksi: -1 = anomali, 1 = normal
    prediction = model.predict(result[FEATURES])

    result['IF_Anomaly'] = (
        prediction == -1
    ).astype(bool)

    # Skor semakin besar = semakin anomali
    result['IF_Score'] = (
        -model.decision_function(result[FEATURES])
    )

    # =====================================
    # 3. INTEGRASI HASIL KEDUA METODE
    # =====================================

    result['Anomaly_Category'] = np.select(
        [
            result['MAD_Anomaly'] & result['IF_Anomaly'],
            result['MAD_Anomaly'] & ~result['IF_Anomaly'],
            ~result['MAD_Anomaly'] & result['IF_Anomaly']
        ],
        [
            'Anomali Kedua Metode',
            'Anomali MAD Saja',
            'Anomali IF Saja'
        ],
        default='Normal'
    )

    return result, model


def generate_recommendations(result):

    result = result.copy()

    # Menghitung ambang statistik dari data yang dianalisis
    power_median = result['Global_active_power'].median()
    power_q01 = result['Global_active_power'].quantile(0.01)
    power_q99 = result['Global_active_power'].quantile(0.99)

    voltage_q01 = result['Voltage'].quantile(0.01)
    voltage_q99 = result['Voltage'].quantile(0.99)

    sub1_q99 = result['Sub_metering_1'].quantile(0.99)
    sub2_q99 = result['Sub_metering_2'].quantile(0.99)
    sub3_q99 = result['Sub_metering_3'].quantile(0.99)

    recommendations = []

    for timestamp, row in result.iterrows():

        rules = []

        # R01: Konsumsi daya sangat tinggi
        if row['Global_active_power'] >= power_q99:
            rules.append(
                "Konsumsi daya aktif sangat tinggi. "
                "Periksa perangkat listrik berdaya besar "
                "dan hindari penggunaan bersamaan."
            )

        # R02: Konsumsi tinggi pada malam hari
        hour = timestamp.hour

        if (
            row['Global_active_power'] > power_median
            and (hour >= 22 or hour < 5)
        ):
            rules.append(
                "Konsumsi listrik relatif tinggi pada malam hari. "
                "Periksa perangkat yang tetap menyala "
                "ketika tidak digunakan."
            )

        # R03: Tegangan berada di luar rentang statistik
        if (
            row['Voltage'] < voltage_q01
            or row['Voltage'] > voltage_q99
        ):
            rules.append(
                "Tegangan berada di luar rentang statistik dataset. "
                "Periksa kembali kondisi kelistrikan."
            )

        # R04: Kelompok perangkat dapur
        if row['Sub_metering_1'] >= sub1_q99:
            rules.append(
                "Penggunaan energi pada kelompok perangkat dapur "
                "relatif tinggi. Evaluasi penggunaan oven, "
                "microwave, atau mesin pencuci piring."
            )

        # R05: Kelompok perangkat laundry
        if row['Sub_metering_2'] >= sub2_q99:
            rules.append(
                "Penggunaan energi pada kelompok laundry "
                "relatif tinggi. Evaluasi penggunaan mesin cuci "
                "dan perangkat terkait."
            )

        # R06: Water heater dan AC
        if row['Sub_metering_3'] >= sub3_q99:
            rules.append(
                "Penggunaan energi pada kelompok water heater "
                "dan AC relatif tinggi. Periksa durasi operasionalnya."
            )

        # R07: Konsumsi daya sangat rendah
        if row['Global_active_power'] <= power_q01:
            rules.append(
                "Konsumsi daya sangat rendah dibandingkan "
                "distribusi dataset. Periksa apakah kondisi ini "
                "sesuai dengan aktivitas rumah tangga."
            )

        # R08: Konsumsi tinggi tanpa dominasi satu kelompok perangkat
        if (
            row['Global_active_power'] > power_median
            and row['Sub_metering_1'] < sub1_q99
            and row['Sub_metering_2'] < sub2_q99
            and row['Sub_metering_3'] < sub3_q99
            and voltage_q01 <= row['Voltage'] <= voltage_q99
        ):
            rules.append(
                "Konsumsi daya rumah tangga tergolong tinggi, "
                "tetapi tidak ditemukan dominasi penggunaan "
                "pada satu kelompok perangkat. Periksa beberapa "
                "perangkat yang beroperasi secara bersamaan."
            )

        # Menentukan apakah observasi merupakan anomali
        is_anomaly = (
            row['MAD_Anomaly'] or row['IF_Anomaly']
        )

        if not is_anomaly:
            recommendation = "Tidak ditemukan indikasi anomali."

        elif rules:
            recommendation = " ".join(dict.fromkeys(rules))

        else:
            recommendation = (
                "Terdapat pola kelistrikan yang tidak biasa. "
                "Periksa kembali karakteristik konsumsi "
                "pada waktu tersebut."
            )

        recommendations.append(recommendation)

    result['Recommendation'] = recommendations

    return result


def analyze_enerva(file):

    # 1. Preprocessing CSV
    processed_data = preprocess_csv(file)

    # 2. Deteksi anomali MAD dan Isolation Forest
    detected_data, trained_model = detect_anomalies(
        processed_data
    )

    # 3. Membuat rekomendasi otomatis
    final_data = generate_recommendations(
        detected_data
    )

    # 4. Mengambil seluruh observasi anomali
    anomaly_data = final_data[
        final_data['MAD_Anomaly'] |
        final_data['IF_Anomaly']
    ].copy()

    # 5. Membuat ringkasan hasil analisis
    summary = {
        'total_observations': len(final_data),
        'total_anomalies': len(anomaly_data),
        'normal_observations': (
            len(final_data) - len(anomaly_data)
        ),
        'mad_anomalies': int(
            final_data['MAD_Anomaly'].sum()
        ),
        'if_anomalies': int(
            final_data['IF_Anomaly'].sum()
        ),
        'both_methods': int(
            (
                final_data['MAD_Anomaly'] &
                final_data['IF_Anomaly']
            ).sum()
        ),
        'mad_only': int(
            (
                final_data['MAD_Anomaly'] &
                ~final_data['IF_Anomaly']
            ).sum()
        ),
        'if_only': int(
            (
                ~final_data['MAD_Anomaly'] &
                final_data['IF_Anomaly']
            ).sum()
        )
    }

    return final_data, anomaly_data, summary, trained_model


