# Toko Online GraphQL API

## Cara Menjalankan
1. Aktifkan virtual environment: `env\Scripts\activate`
2. Jalankan server: `uvicorn main:app --reload`
3. Buka browser: http://127.0.0.1:8000/graphql

## Analisis REST vs GraphQL

GraphQL lebih cocok digunakan ketika aplikasi memiliki kebutuhan data yang
bervariasi antar klien, misalnya aplikasi mobile membutuhkan data lebih sedikit
dibandingkan aplikasi web. Selain itu, GraphQL unggul saat domain data memiliki
relasi kompleks (seperti produk → kategori → supplier) karena client dapat
mengambil semua relasi dalam satu request tanpa over-fetching.

REST lebih cocok digunakan untuk API publik yang sederhana dan perlu
didokumentasikan dengan mudah karena endpoint REST lebih intuitif dan familiar
bagi banyak developer. REST juga lebih tepat untuk operasi berbasis file atau
streaming (upload/download) yang tidak dirancang untuk query berbasis GraphQL.

Risiko utama GraphQL adalah query dengan nested depth yang sangat dalam dapat
membebani server secara berlebihan (misalnya produk → kategori → produk lagi
secara rekursif). Mitigasinya adalah menerapkan query depth limiting menggunakan
library seperti `strawberry-django` atau middleware custom yang membatasi
kedalaman query maksimum.