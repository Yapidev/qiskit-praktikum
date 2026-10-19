"""
Praktikum 1: Sirkuit kuantum pertama - Bell State
Menjalankan sirkuit di simulator lokal (StatevectorSampler), tidak butuh IBM.

Jalankan: .venv/Scripts/python.exe 01_hello_qubit.py
"""

import sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from qiskit import QuantumCircuit
from qiskit.primitives import StatevectorSampler

# 1 qubit circuit
qc = QuantumCircuit(1)
qc.x(0)          # X gate: membalik |0> menjadi |1>
qc.h(0)          # Hadamard: |0> -> (|0> + |1>)/sqrt(2)
qc.measure_all() # tambah register klasik + ukur semua qubit
print(qc.draw(output="text"))

# Jalankan 100 shots di simulator lokal
sampler = StatevectorSampler()
job = sampler.run([qc], shots=100)
result = job.result()[0]
counts = result.data.meas.get_counts()
print("\nHasil pengukuran (100 shots):", counts)

# Bell state: dua qubit terhubung
bell = QuantumCircuit(2, 2)
bell.h(0)
bell.cx(0, 1)
bell.measure([0, 1], [0, 1])
print("\nBell circuit:")
print(bell.draw(output="text"))

job = sampler.run([bell], shots=1000)
counts = job.result()[0].data.c.get_counts()
print("\nBell state (1000 shots):", counts)
print("Perhatikan: hanya '00' dan '11' muncul -> qubit terkorelasi (entangled).")
