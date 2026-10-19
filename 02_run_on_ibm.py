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

def main():
    service = QiskitRuntimeService(instance="open-instance")

    # Pilih perangkat: yang paling sibuk antreannya
    backend = service.least_busy(operational=True, simulator=False)
    print(f"Menggunakan perangkat: {backend.name}")

    bell = QuantumCircuit(2, 2)
    bell.h(0)
    bell.cx(0, 1)
    bell.measure([0, 1], [0, 1])

    # Transpile agar sirkuit sesuai arsitektur perangkat
    bell_tp = transpile(bell, backend=backend)

    sampler = Sampler(mode=backend)
    job = sampler.run([bell_tp], shots=1024)
    print(f"Job dikirim. ID: {job.job_id()}")
    print("Tunggu hasil (cek juga di https://quantum.ibm.com/jobs)...")
    result = job.result()
    counts = result[0].data.c.get_counts()
    print(f"\nHasil dari {backend.name}: {counts}")

if __name__ == "__main__":
    if "--save" in sys.argv:
        save_token()
    else:
        main()
