# Qiskit Praktikum

Kumpulan praktikum Komputer Kuantum menggunakan [Qiskit](https://www.ibm.com/quantum/qiskit), mencakup simulasi lokal dan eksekusi di perangkat kuantum nyata IBM Quantum.

## Praktikum

| File | Materi | Lingkungan |
|---|---|---|
| `01_hello_qubit.py` | Sirkuit kuantum pertama: gate X, H, pengukuran, dan Bell state | Simulator lokal |
| `02_run_on_ibm.py` | Bell state di perangkat kuantum nyata IBM, transpilasi sirkuit | IBM Quantum (cloud) |
| `03_deutsch_jozsa.py` | Algoritma Deutsch-Jozsa: menentukan fungsi konstan/balanced dengan satu panggilan oracle | Simulator lokal |
| `04_deutsch_jozsa_ibm.py` | Deutsch-Jozsa di chip kuantum nyata dengan analisis noise | IBM Quantum (cloud) |

## Setup

Membutuhkan Python 3.10+.

```powershell
# 1. Buat virtual environment
python -m venv .venv

# 2. Aktifkan (PowerShell)
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
& ".venv\Scripts\Activate.ps1"

# 3. Install dependensi
pip install qiskit qiskit-ibm-runtime qiskit-aer
```

## Setup API Key IBM Quantum

Praktikum 2 dan 4 membutuhkan akun IBM Quantum. Praktikum 1 dan 3 jalan lokal tanpa akun.

1. **Buat akun** di [quantum.ibm.com](https://quantum.ibm.com) — gratis (Open Plan), cukup email dan verifikasi.

2. **Ambil API key**: setelah login, klik ikon profil (pojok kanan atas) → **Account Settings** → **API token** → salin token.

3. **Simpan token** di komputer (sekali saja):
   ```powershell
   python 02_run_on_ibm.py --save
   ```
   Saat diminta, tempel (paste) token lalu Enter. Token tersimpan lokal di profil user Windows — tidak masuk ke repo, tidak ter-commit ke git.

4. **Cek bahwa tersambung**: jalankan praktikum 2 seperti biasa. Kalau daftar perangkat muncul, API key sudah aktif:
   ```powershell
   python 02_run_on_ibm.py
   ```

Catatan keamanan:
- Jangan pernah paste token ke chat, screenshot, atau file yang di-commit ke GitHub.
- Kalau ragu token ter-expose, regenerate di Account Settings — token lama langsung mati, lalu simpan ulang dengan `--save`.
- Open Plan gratis memberi kuota bulanan ~10 menit eksekusi di perangkat nyata; simulator lokal tidak terbatas.

## Cara Menjalankan

```powershell
# Praktikum 1: simulator lokal, tidak butuh akun
python 01_hello_qubit.py

# Praktikum 2: pertama kali, simpan API key IBM Quantum
python 02_run_on_ibm.py --save

# Praktikum 2: jalankan di perangkat nyata
python 02_run_on_ibm.py

# Praktikum 3: algoritma Deutsch-Jozsa di simulator lokal
python 03_deutsch_jozsa.py

# Praktikum 4: Deutsch-Jozsa di chip kuantum nyata (butuh API key)
python 04_deutsch_jozsa_ibm.py
```

API key didapat dari [quantum.ibm.com](https://quantum.ibm.com) (Account Settings → API token). Token tersimpan lokal di komputer, tidak masuk ke repo.

## Contoh Hasil

Bell state di simulator lokal (ideal, tanpa noise):

```
{'00': 517, '11': 483}
```

Bell state di perangkat nyata `ibm_fez` (1024 shots):

```
{'00': 528, '11': 484, '01': 9, '10': 3}
```

Hanya `00` dan `11` yang muncul ~50/50 sesuai teori; sedikit `01`/`10` adalah noise hardware (dekoherensi dan readout error) — perbedaan inilah yang membedakan simulasi dari perangkat kuantum fisik.

Deutsch-Jozsa di simulator lokal (deterministik, tanpa noise):

```
konstan   f(x)=0    {'00': 100}    konstan   BENAR
konstan   f(x)=1    {'00': 100}    konstan   BENAR
balanced  f(x)=01   {'10': 100}    balanced  BENAR
balanced  f(x)=11   {'11': 100}    balanced  BENAR
```

Deutsch-Jozsa di perangkat nyata (contoh fake backend dengan noise):

```
konstan   f(x)=0    00:1020, 01:3, 10:1    konstan   BENAR
balanced  f(x)=01   10:1014, 00:8, 11:2    balanced  BENAR
```

Noise membuat hasil tidak lagi 100%, tapi kesimpulan algoritma tetap bisa ditarik dari pola dominan.

## Materi Berikutnya (roadmap)

- Teleportasi kuantum
- GHZ state
- VQE / QAOA
