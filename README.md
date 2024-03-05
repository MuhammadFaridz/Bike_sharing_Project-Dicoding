# Proyek Analisis Data: Bike Sharing Dataset

## Menentukan Pertanyaan Bisnis
- Bagaimana trend jumlah sewaan sepeda dalam beberapa tahun terakhir?
- Bagaimana pola penggunaan sewaan sepeda berdasarkan waktu?
- Pada musim apa aktivitas sewaan sepeda tertinggi?
- Apakah cuaca mempengaruhi jumlah penyewaan sepeda?
- Apakah ada korelasi antara suhu yang mengindikasikan kondisi saat penyewaan sepeda sedang tinggi (Menggunakan teknik analisis lanjutan yaitu clustering)?


## Insigth
Conclution Pertanyaan 1: bagaimana trend jumlah sewaan sepeda dalam beberapa tahun terakhir?

Jumlah penyewaan sepeda pada tahun 2012 lebih tinggi dibandingkan tahun 2011. Kedua tahun tersebut menunjukkan tren dan musim yang sama, dengan jumlah perjalanan meningkat pada pertengahan tahun dan menurun pada awal dan akhir tahun.
Conclution pertanyaan 2: Bagaimana pola penggunaan sewaan sepeda berdasarkan waktu?

penyewaan sepeda registered menunjukkan puncaknya pada pukul 08.00 dan 17.00. Mengingat kedua jam tersebut adalah waktu orang berangkat dan pulang kerja, ada kemungkinan pengguna registered yang menyewa sepeda dan menggunakan sepeda tersebut untuk berangkat kerja. Sebaliknya, frekuensi yang menyewa sepeda casual menunjukkan frekuensi yang lebih tinggi pada siang hari, kemudian mulai menurun setelah pukul 17.00.
Conclution pertanyaan 3: Pada musim apa aktivitas sewaan sepeda tertinggi?

Jumlah penyewaan sepeda tertinggi terjadi pada musim panas dan terendah pada musim dingin.
Conclution pertanyaan 4: Apakah cuaca mempengaruhi jumlah penyewaan sepeda?

ya, Jumlah pengguna yang sewa sepeda sebagian besar dipengaruhi oleh kondisi cuaca. Jumlah penumpang yang berkendara jauh lebih sedikit saat hujan lebat dan badai petir dibandingkan saat cuaca lebih baik. kondisi ini berlaku untuk semua musim
Conclution pertanyaan 5: Apakah ada korelasi antara suhu yang mengindikasikan kondisi saat penyewaan sepeda sedang tinggi (Menggunakan teknik analisis lanjutan yaitu clustering)?

ya, pada saat suhu lebih rendah jumlah penyewaan sepeda juga rendah. Hal ini terjadi selama musim dingin. dan Ketika suhu sedang tinggi, jumlah penyewaan sepeda juga meningkat. Hal ini terjadi selama musim panas. jumlah penyewaan sepeda yang tertinggi pada cluster musim gugur dan musim panas. yaitu pada suhu antara 20 hingga 30 derajat Celcius.


# BIKE-SHARING DASHBOARD
akses link berikut untuk melihat dasboard : ....

# Run streamlit dilokal
Untuk menginstal semua perpustakaan yang diperlukan, buka terminal/command prompt/conda prompt Anda, navigasikan ke folder proyek ini, dan jalankan perintah berikut:
'pip install -r requirements.txt'

# cara run dashboard
'streamlit run app.py'
