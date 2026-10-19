# Qiskit Praktikum

Kumpulan praktikum Komputer Kuantum menggunakan [Qiskit](https://www.ibm.com/quantum/qiskit), mencakup simulasi lokal dan eksekusi di perangkat kuantum nyata IBM Quantum.

## Praktikum

| File | Materi | Lingkungan |
|---|---|---|
| `01_hello_qubit.py` | Sirkuit kuantum pertama: gate X, H, pengukuran, dan Bell state | Simulator lokal |
| `02_run_on_ibm.py` | Bell state di perangkat kuantum nyata IBM, transpilasi sirkuit | IBM Quantum (cloud) |
| `03_deutsch_jozsa.py` | Algoritma Deutsch-Jozsa: menentukan fungsi konstan/balanced dengan satu panggilan oracle | Simulator lokal |

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

## Materi Berikutnya (roadmap)

- Teleportasi kuantum
- GHZ state
- VQE / QAOA
