"""
Praktikum 2: Jalankan Bell state di komputer kuantum NYATA IBM.

Pertama kali: simpan API key kamu dengan:
    .venv/Scripts/python.exe 02_run_on_ibm.py --save

Lalu jalankan seperti biasa:
    .venv/Scripts/python.exe 02_run_on_ibm.py
"""

import sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from qiskit import QuantumCircuit, transpile
from qiskit_ibm_runtime import QiskitRuntimeService
from qiskit_ibm_runtime.executor_sampler import Sampler


def save_token():
    token = input("Tempel (paste) API key IBM Quantum kamu: ").strip()
    QiskitRuntimeService.save_account(
        token=token,
        channel="ibm_quantum_platform",  # IBM Quantum Platform baru
        set_as_default=True,
        overwrite=True,
    )
    print("Token tersimpan di komputer kamu. Sekarang jalankan lagi tanpa --save.")


def daftar_perangkat(service):
    """Ambil daftar perangkat kuantum nyata yang operasional."""
    backends = service.backends(operational=True, simulator=False)
    backends.sort(key=lambda b: b.name)
    return backends


def pilih_perangkat(service):
    """Tampilkan tabel perangkat, minta user memilih. Enter = paling kosong."""
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


def buat_bell():
    bell = QuantumCircuit(2, 2)
    bell.h(0)
    bell.cx(0, 1)
    bell.measure([0, 1], [0, 1])
    return bell


def tampilkan_hasil(counts, nama_perangkat):
    """Histogram ASCII + ringkasan noise."""
    total = sum(counts.values())
    maks = max(counts.values())

    print(f"\n=== Hasil dari {nama_perangkat} ({total} shots) ===")
    for bit, c in sorted(counts.items(), key=lambda x: -x[1]):
        panjang = max(1, round(36 * c / maks))
        persen = c / total * 100
        print(f"{bit:>4} |{'█' * panjang:<36}{c:>6}  ({persen:4.1f}%)")

    benar = counts.get("00", 0) + counts.get("11", 0)
    error = total - benar
    print("-" * 56)
    print(f"Benar (00/11): {benar} ({benar / total * 100:.1f}%)  "
          f"Noise (01/10): {error} ({error / total * 100:.1f}%)")


def main():
    service = QiskitRuntimeService(instance="open-instance")

    backend = pilih_perangkat(service)
    print(f"\nPerangkat terpilih: {backend.name} "
          f"({backend.num_qubits} qubit, {backend.status().pending_jobs} job di antrean)")

    bell = buat_bell()

    # Transpile agar sirkuit sesuai arsitektur perangkat
    bell_tp = transpile(bell, backend=backend)

    sampler = Sampler(mode=backend)
    job = sampler.run([bell_tp], shots=1024)
    print(f"Job dikirim. ID: {job.job_id()}")
    print("Tunggu hasil (cek juga di https://quantum.ibm.com/jobs)...")

    result = job.result()
    counts = result[0].data.c.get_counts()
    tampilkan_hasil(counts, backend.name)


if __name__ == "__main__":
    if "--save" in sys.argv:
        save_token()
    else:
        main()
