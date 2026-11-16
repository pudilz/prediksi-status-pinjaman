import streamlit as st
import pandas as pd
import joblib


# ==========================================
# KONFIGURASI HALAMAN
# ==========================================

st.set_page_config(
    page_title="Prediksi Status Pinjaman",
    page_icon="🏦",
    layout="centered"
)


# ==========================================
# MEMUAT MODEL
# ==========================================

@st.cache_resource
def load_model():
    return joblib.load("model_status_pinjaman.pkl")


model = load_model()


# ==========================================
# FUNGSI FORMAT RUPIAH
# ==========================================

def format_rupiah(nilai):
    return "Rp " + f"{nilai:,.0f}".replace(",", ".")


# ==========================================
# JUDUL APLIKASI
# ==========================================

st.title("🏦 Prediksi Status Pinjaman")

st.write(
    "Aplikasi ini digunakan untuk memprediksi status kelayakan "
    "pinjaman berdasarkan data calon peminjam."
)

st.divider()


# ==========================================
# DATA CALON PEMINJAM
# ==========================================

st.header("📝 Data Calon Peminjam")

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
    value=5.0,
    step=0.5
)

pendapatan_tahunan = st.number_input(
    "Pendapatan Tahunan (Rp)",
    min_value=0.0,
    value=50000.0,
    step=1000.0,
    format="%.0f"
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
    value=5.0,
    step=0.5
)

aset_tabungan = st.number_input(
    "Aset Tabungan (Rp)",
    min_value=0.0,
    value=10000.0,
    step=1000.0,
    format="%.0f"
)

hutang_saat_ini = st.number_input(
    "Hutang Saat Ini (Rp)",
    min_value=0.0,
    value=5000.0,
    step=1000.0,
    format="%.0f"
)

gagal_bayar_tercatat = st.selectbox(
    "Pernah Gagal Bayar?",
    [0, 1],
    format_func=lambda x: "Tidak" if x == 0 else "Ya"
)

tunggakan_2thn_terakhir = st.number_input(
    "Jumlah Tunggakan dalam 2 Tahun Terakhir",
    min_value=0,
    value=0
)

catatan_negatif = st.number_input(
    "Jumlah Catatan Negatif Kredit",
    min_value=0,
    value=0
)

tipe_produk = st.selectbox(
    "Tipe Produk Pinjaman",
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


# ==========================================
# DATA PENGAJUAN PINJAMAN
# ==========================================

st.divider()
st.header("💰 Data Pengajuan Pinjaman")

jumlah_pinjaman = st.number_input(
    "Jumlah Pinjaman (Rp)",
    min_value=0.0,
    value=10000.0,
    step=1000.0,
    format="%.0f"
)

suku_bunga = st.number_input(
    "Suku Bunga Tahunan (%)",
    min_value=0.0,
    max_value=100.0,
    value=5.0,
    step=0.5
)

tenor_pinjaman = st.number_input(
    "Tenor Pinjaman (Bulan)",
    min_value=1,
    value=12,
    step=1
)


# ==========================================
# PERHITUNGAN ANGSURAN BUNGA FLAT
# ==========================================

st.divider()
st.header("📊 Simulasi Angsuran Pinjaman")

# Menghitung total bunga dengan metode flat
bunga_total = (
    jumlah_pinjaman
    * (suku_bunga / 100)
    * (tenor_pinjaman / 12)
)

# Menghitung total pembayaran
total_pembayaran = jumlah_pinjaman + bunga_total

# Menghitung angsuran per bulan
angsuran_pokok = jumlah_pinjaman / tenor_pinjaman
angsuran_bunga = bunga_total / tenor_pinjaman

angsuran_bulanan = angsuran_pokok + angsuran_bunga

st.write("**Rincian Perhitungan:**")

st.write(
    f"Pokok Pinjaman: **{format_rupiah(jumlah_pinjaman)}**"
)

st.write(
    f"Total Bunga: **{format_rupiah(bunga_total)}**"
)

st.write(
    f"Total Pembayaran: **{format_rupiah(total_pembayaran)}**"
)

st.success(
    f"Estimasi Angsuran Bulanan: {format_rupiah(angsuran_bulanan)}"
)


# ==========================================
# PERHITUNGAN RASIO OTOMATIS
# ==========================================

st.divider()
st.header("📈 Perhitungan Rasio Keuangan")

# Rasio Hutang terhadap Pendapatan
if pendapatan_tahunan > 0:
    rasio_hutang_terhadap_pendapatan = (
        hutang_saat_ini / pendapatan_tahunan
    )
else:
    rasio_hutang_terhadap_pendapatan = 0


# Rasio Pinjaman terhadap Pendapatan
if pendapatan_tahunan > 0:
    rasio_pinjaman_terhadap_pendapatan = (
        jumlah_pinjaman / pendapatan_tahunan
    )
else:
    rasio_pinjaman_terhadap_pendapatan = 0


# Rasio Pembayaran terhadap Pendapatan
# Mengikuti perhitungan fitur yang digunakan pada versi sebelumnya.
if pendapatan_tahunan > 0:
    rasio_pembayaran_terhadap_pendapatan = (
        jumlah_pinjaman / (3 * pendapatan_tahunan)
    )
else:
    rasio_pembayaran_terhadap_pendapatan = 0


# Menampilkan hasil rasio
col1, col2 = st.columns(2)

with col1:
    st.metric(
        "Rasio Hutang / Pendapatan",
        f"{rasio_hutang_terhadap_pendapatan:.4f}"
    )

    st.metric(
        "Rasio Pinjaman / Pendapatan",
        f"{rasio_pinjaman_terhadap_pendapatan:.4f}"
    )

with col2:
    st.metric(
        "Rasio Pembayaran / Pendapatan",
        f"{rasio_pembayaran_terhadap_pendapatan:.4f}"
    )

    st.metric(
        "Angsuran Bulanan",
        format_rupiah(angsuran_bulanan)
    )


# ==========================================
# TOMBOL PREDIKSI
# ==========================================

st.divider()

if st.button(
    "🔍 Prediksi Status Pinjaman",
    use_container_width=True
):

    # Membuat indikator riwayat bermasalah
    indikator_riwayat_bermasalah = int(
        gagal_bayar_tercatat > 0
        or tunggakan_2thn_terakhir > 0
        or catatan_negatif > 0
    )

    # Membuat DataFrame untuk prediksi
    data = pd.DataFrame([{
        "usia": usia,
        "status_pekerjaan": status_pekerjaan,
        "lama_bekerja_tahun": lama_bekerja_tahun,
        "pendapatan_tahunan": pendapatan_tahunan,
        "skor_kredit": skor_kredit,
        "lama_riwayat_kredit_tahun": lama_riwayat_kredit_tahun,
        "aset_tabungan": aset_tabungan,
        "hutang_saat_ini": hutang_saat_ini,
        "gagal_bayar_tercatat": gagal_bayar_tercatat,
        "tunggakan_2thn_terakhir": tunggakan_2thn_terakhir,
        "catatan_negatif": catatan_negatif,
        "tipe_produk": tipe_produk,
        "tujuan_pinjaman": tujuan_pinjaman,
        "jumlah_pinjaman": jumlah_pinjaman,
        "suku_bunga": suku_bunga,
        "rasio_hutang_terhadap_pendapatan":
            rasio_hutang_terhadap_pendapatan,
        "rasio_pinjaman_terhadap_pendapatan":
            rasio_pinjaman_terhadap_pendapatan,
        "rasio_pembayaran_terhadap_pendapatan":
            rasio_pembayaran_terhadap_pendapatan,
        "indikator_riwayat_bermasalah":
            indikator_riwayat_bermasalah
    }])

    # Melakukan prediksi
    hasil = model.predict(data)[0]

    # Menampilkan hasil prediksi
    st.divider()
    st.header("📋 Hasil Prediksi")

    st.write(f"**Status Pinjaman:** {hasil}")

    # Menampilkan probabilitas jika model mendukungnya
    if hasattr(model, "predict_proba"):
        probabilitas = model.predict_proba(data)[0]

        st.subheader("Probabilitas Prediksi")

        for i, nilai in enumerate(probabilitas):
            nama_kelas = model.classes_[i]

            st.write(
                f"Probabilitas kelas {nama_kelas}: "
                f"**{nilai * 100:.2f}%**"
            )

    st.info(
        "Hasil prediksi merupakan estimasi berdasarkan pola data "
        "yang digunakan untuk melatih model."
    )
