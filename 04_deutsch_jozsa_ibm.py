"""
Praktikum 4: Deutsch-Jozsa di PERANGKAT KUANTUM NYATA IBM.

Sama seperti Praktikum 3, tapi dieksekusi di chip kuantum fisik.
Di sini kamu akan melihat noise: '00' untuk oracle konstan tidak
lagi 100%, dan muncul pola lain dari kesalahan hardware.

Jalankan: .venv/Scripts/python.exe 04_deutsch_jozsa_ibm.py
Butuh API key IBM (simpan dulu via 02_run_on_ibm.py --save).
"""

import sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

import random
from qiskit import QuantumCircuit, transpile
from qiskit_ibm_runtime import QiskitRuntimeService
from qiskit_ibm_runtime.executor_sampler import Sampler

N_INPUT = 2


def daftar_perangkat(service):
    backends = service.backends(operational=True, simulator=False)
    backends.sort(key=lambda b: b.name)
    return backends


def pilih_perangkat(service):
    backends = daftar_perangkat(service)
    tercepat = service.least_busy(operational=True, simulator=False)

    print("\n=== Komputer Kuantum yang Tersedia ===")
    print(f"{'No':<4}{'Nama':<16}{'Qubit':>6}{'Antrean':>9}")
    print("-" * 35)
    for i, b in enumerate(backends, start=1):
        tanda = " <-- paling kosong" if b.name == tercepat.name else ""
        print(f"{i:<4}{b.name:<16}{b.num_qubits:>6}{b.status().pending_jobs:>9}{tanda}")
    print("-" * 35)

    while True:
        pilihan = input(
            f"Pilih nomor perangkat [Enter = {tercepat.name}]: "
        ).strip()
        if pilihan == "":
            return tercepat
        if pilihan.isdigit() and 1 <= int(pilihan) <= len(backends):
            return backends[int(pilihan) - 1]
        print(f"Masukkan angka 1-{len(backends)} atau Enter.")


def buat_sirkuit_dj(oracle_type, param):
    qc = QuantumCircuit(N_INPUT + 1, N_INPUT)
    qc.x(N_INPUT)
    qc.h(range(N_INPUT + 1))
    if oracle_type == "konstan":
        if param == 1:
            qc.x(N_INPUT)
    else:  # balanced: f(x) = bitmask . x
        for i, bit in enumerate(param):
            if bit == "1":
                qc.cx(i, N_INPUT)
    qc.h(range(N_INPUT))
    qc.measure(range(N_INPUT), range(N_INPUT))
    return qc


def buat_semua_kasus():
    """2 konstan + 2 balanced (bitmask tidak boleh '00')."""
    bitmask_valid = [format(i, f"0{N_INPUT}b") for i in range(1, 2 ** N_INPUT)]
    b1, b2 = random.sample(bitmask_valid, 2)
    return [
        ("konstan", 0),
        ("konstan", 1),
        ("balanced", b1),
        ("balanced", b2),
    ]


def tebak_dari_noise(counts):
    """Di hardware nyata tidak ada hasil 100%.
    Ambil pola dengan count terbanyak sebagai jawaban."""
    return max(counts, key=counts.get)


def main():
    service = QiskitRuntimeService(instance="open-instance")
    backend = pilih_perangkat(service)
    print(f"\nPerangkat terpilih: {backend.name} "
          f"({backend.num_qubits} qubit, {backend.status().pending_jobs} job di antrean)")

    kasus_list = buat_semua_kasus()
    sirkuit_list = [buat_sirkuit_dj(t, p) for t, p in kasus_list]

    # Transpile semua sirkuit ke arsitektur perangkat
    sirkuit_tp = transpile(sirkuit_list, backend=backend)

    sampler = Sampler(mode=backend)
    job = sampler.run(sirkuit_tp, shots=1024)
    print(f"\n4 oracle dikirim dalam satu job. ID: {job.job_id()}")
    print("Tunggu hasil (cek juga di https://quantum.ibm.com/jobs)...")
    hasil = job.result()

    print("\n" + "=" * 66)
    print(f"{'Oracle':<12}{'Detail':<10}{'Hasil (top-3)':<30}{'Kesimpulan':<12}")
    print("-" * 66)

    semua_benar = True
    for (jenis, param), dist in zip(kasus_list, hasil):
        counts = dist.data.c.get_counts()
        tebakan = tebak_dari_noise(counts)
        kesimpulan = "konstan" if tebakan == "00" else "balanced"
        benar = kesimpulan == jenis
        semua_benar &= benar
        top3 = ", ".join(
            f"{k}:{v}" for k, v in sorted(counts.items(), key=lambda x: -x[1])[:3]
        )
        status = "BENAR" if benar else "SALAH"
        print(f"{jenis:<12}f(x)={param!s:<5}{top3:<30}{kesimpulan:<12}{status}")

    print("-" * 66)
    if semua_benar:
        print("Semua kasus BENAR walau ada noise: algoritma tetap bekerja di hardware nyata.")
    else:
        print("Ada kasus salah - noise terlalu besar, coba lagi atau ganti perangkat.")
    print("Bandingkan dengan Praktikum 3: di simulator hasilnya 100% bersih.")


if __name__ == "__main__":
    main()
