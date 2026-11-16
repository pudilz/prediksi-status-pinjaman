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
model = joblib.load(
    'model_status_pinjaman.pkl'
)

# Judul aplikasi
st.title("🏦 Prediksi Status Pinjaman")

st.write(
    "Aplikasi prediksi status pinjaman "
    "menggunakan Machine Learning."
)

st.divider()

# Form input
st.subheader("Data Pelanggan")

with st.form("form_prediksi"):

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

    jumlah_pinjaman = st.number_input(
        "Jumlah Pinjaman",
        min_value=0,
        value=10000
    )

    suku_bunga = st.number_input(
        "Suku Bunga",
        min_value=0.0,
        value=10.0
    )

    rasio_hutang_terhadap_pendapatan = st.number_input(
        "Rasio Hutang terhadap Pendapatan",
        min_value=0.0,
        value=0.2
    )

    rasio_pinjaman_terhadap_pendapatan = st.number_input(
        "Rasio Pinjaman terhadap Pendapatan",
        min_value=0.0,
        value=0.5
    )

    rasio_pembayaran_terhadap_pendapatan = st.number_input(
        "Rasio Pembayaran terhadap Pendapatan",
        min_value=0.0,
        value=0.2
    )

    tombol = st.form_submit_button(
        "Prediksi Status Pinjaman"
    )

# Proses prediksi
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
        'rasio_hutang_terhadap_pendapatan': rasio_hutang_terhadap_pendapatan,
        'rasio_pinjaman_terhadap_pendapatan': rasio_pinjaman_terhadap_pendapatan,
        'rasio_pembayaran_terhadap_pendapatan': rasio_pembayaran_terhadap_pendapatan
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

    st.divider()

    st.subheader("Hasil Prediksi")

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
