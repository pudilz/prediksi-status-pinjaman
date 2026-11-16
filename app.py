import streamlit as st
import pandas as pd
import joblib

# Konfigurasi halaman
st.set_page_config(
    page_title="Prediksi Status Pinjaman",
    page_icon="🏦",
    layout="centered"
)

# Memuat model
model = joblib.load('model_status_pinjaman.pkl')

# Judul aplikasi
st.title("🏦 Prediksi Status Pinjaman")

st.write(
    "Aplikasi prediksi status pinjaman "
    "menggunakan Machine Learning."
)

st.divider()

# =====================================
# DATA PELANGGAN
# =====================================

st.subheader("Data Pelanggan")

usia = st.number_input(
    "Usia",
    min_value=18,
    max_value=100,
    value=30
)

status_pekerjaan = st.selectbox(
    "Status Pekerjaan",
    ["Bekerja", "Mahasiswa", "Wiraswasta"]
)

lama_bekerja_tahun = st.number_input(
    "Lama Bekerja (Tahun)",
    min_value=0.0,
    value=5.0
)

pendapatan_tahunan = st.number_input(
    "Pendapatan Tahunan",
    min_value=0,
    value=50000
)

skor_kredit = st.number_input(
    "Skor Kredit",
    min_value=0,
    max_value=1000,
    value=650
)

lama_riwayat_kredit_tahun = st.number_input(
    "Lama Riwayat Kredit (Tahun)",
    min_value=0.0,
    value=5.0
)

aset_tabungan = st.number_input(
    "Aset Tabungan",
    min_value=0,
    value=10000
)

hutang_saat_ini = st.number_input(
    "Hutang Saat Ini",
    min_value=0,
    value=5000
)

gagal_bayar_tercatat = st.selectbox(
    "Pernah Gagal Bayar?",
    [0, 1]
)

tunggakan_2thn_terakhir = st.number_input(
    "Tunggakan 2 Tahun Terakhir",
    min_value=0,
    value=0
)

catatan_negatif = st.number_input(
    "Catatan Negatif",
    min_value=0,
    value=0
)

tipe_produk = st.selectbox(
    "Tipe Produk",
    [
        "Kartu Kredit",
        "Kredit Berjalan",
        "Pinjaman Pribadi"
    ]
)

tujuan_pinjaman = st.selectbox(
    "Tujuan Pinjaman",
    [
        "Bisnis",
        "Konsolidasi Hutang",
        "Medis",
        "Pendidikan",
        "Pribadi",
        "Renovasi Rumah"
    ]
)

# =====================================
# DATA PINJAMAN
# =====================================

st.divider()
st.subheader("Data Pinjaman")

jumlah_pinjaman = st.number_input(
    "Jumlah Pinjaman",
    min_value=0,
    value=10000
)

suku_bunga = st.number_input(
    "Suku Bunga Flat (% per Tahun)",
    min_value=0.0,
    value=10.0
)

tenor_pinjaman = st.number_input(
    "Tenor Pinjaman (Bulan)",
    min_value=1,
    value=12
)

# =====================================
# PERHITUNGAN BUNGA FLAT
# =====================================

bunga_total = (
    jumlah_pinjaman
    * (suku_bunga / 100)
    * (tenor_pinjaman / 12)
)

total_pembayaran = jumlah_pinjaman + bunga_total

angsuran_pokok = (
    jumlah_pinjaman / tenor_pinjaman
)

angsuran_bunga = (
    bunga_total / tenor_pinjaman
)

angsuran_bulanan = (
    angsuran_pokok + angsuran_bunga
)

# =====================================
# PERHITUNGAN RASIO OTOMATIS
# =====================================

# Rasio Hutang terhadap Pendapatan
rasio_hutang_terhadap_pendapatan = (
    hutang_saat_ini / pendapatan_tahunan
    if pendapatan_tahunan > 0 else 0
)

# Rasio Pinjaman terhadap Pendapatan
rasio_pinjaman_terhadap_pendapatan = (
    jumlah_pinjaman / pendapatan_tahunan
    if pendapatan_tahunan > 0 else 0
)

# Rasio Pembayaran terhadap Pendapatan
# Mengikuti rumus pada dataset:
# Jumlah Pinjaman / (3 x Pendapatan Tahunan)

rasio_pembayaran_terhadap_pendapatan = (
    jumlah_pinjaman / (3 * pendapatan_tahunan)
    if pendapatan_tahunan > 0 else 0
)

# =====================================
# HASIL SIMULASI PINJAMAN
# =====================================

st.divider()
st.subheader("💰 Simulasi Angsuran Bunga Flat")

col1, col2 = st.columns(2)

with col1:
    st.metric(
        "Total Bunga",
        f"{bunga_total:,.2f}"
    )

with col2:
    st.metric(
        "Total Pembayaran",
        f"{total_pembayaran:,.2f}"
    )

st.success(
    f"Estimasi Angsuran Bulanan: "
    f"{angsuran_bulanan:,.2f}"
)

st.caption(
    "Perhitungan menggunakan metode bunga flat. "
    "Angsuran pokok dan bunga memiliki nilai tetap setiap bulan."
)

# =====================================
# HASIL RASIO
# =====================================

st.divider()
st.subheader("📊 Hasil Perhitungan Rasio")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Rasio Hutang",
        f"{rasio_hutang_terhadap_pendapatan:.3f}"
    )

with col2:
    st.metric(
        "Rasio Pinjaman",
        f"{rasio_pinjaman_terhadap_pendapatan:.3f}"
    )

with col3:
    st.metric(
        "Rasio Pembayaran",
        f"{rasio_pembayaran_terhadap_pendapatan:.3f}"
    )

st.caption(
    "Ketiga rasio dihitung otomatis berdasarkan "
    "data yang dimasukkan dan mengikuti rumus dataset."
)

# =====================================
# PREDIKSI MACHINE LEARNING
# =====================================

st.divider()

tombol = st.button(
    "🔍 Prediksi Status Pinjaman",
    use_container_width=True
)

if tombol:

    data = pd.DataFrame([{
        'usia': usia,
        'status_pekerjaan': status_pekerjaan,
        'lama_bekerja_tahun': lama_bekerja_tahun,
        'pendapatan_tahunan': pendapatan_tahunan,
        'skor_kredit': skor_kredit,
        'lama_riwayat_kredit_tahun': lama_riwayat_kredit_tahun,
        'aset_tabungan': aset_tabungan,
        'hutang_saat_ini': hutang_saat_ini,
        'gagal_bayar_tercatat': gagal_bayar_tercatat,
        'tunggakan_2thn_terakhir': tunggakan_2thn_terakhir,
        'catatan_negatif': catatan_negatif,
        'tipe_produk': tipe_produk,
        'tujuan_pinjaman': tujuan_pinjaman,
        'jumlah_pinjaman': jumlah_pinjaman,
        'suku_bunga': suku_bunga,
        'rasio_hutang_terhadap_pendapatan':
            rasio_hutang_terhadap_pendapatan,
        'rasio_pinjaman_terhadap_pendapatan':
            rasio_pinjaman_terhadap_pendapatan,
        'rasio_pembayaran_terhadap_pendapatan':
            rasio_pembayaran_terhadap_pendapatan
    }])

    # Feature Engineering
    data['indikator_riwayat_bermasalah'] = (
        (data['gagal_bayar_tercatat'] > 0) |
        (data['tunggakan_2thn_terakhir'] > 0) |
        (data['catatan_negatif'] > 0)
    ).astype(int)

    # Prediksi
    hasil = model.predict(data)[0]

    probabilitas = model.predict_proba(data)[0]

    st.subheader("📋 Hasil Prediksi")

    st.write(
        f"Status Pinjaman: **{hasil}**"
    )

    st.write(
        f"Probabilitas kelas 0: "
        f"{probabilitas[0]*100:.2f}%"
    )

    st.write(
        f"Probabilitas kelas 1: "
        f"{probabilitas[1]*100:.2f}%"
    )

    st.info(
        "Hasil ini merupakan prediksi model "
        "untuk keperluan analisis dan pembelajaran, "
        "bukan keputusan kredit resmi."
        )
