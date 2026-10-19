"""
Praktikum 3: Algoritma Deutsch-Jozsa
Algoritma kuantum pertama yang membuktikan keunggulan kuantum:
menentukan fungsi konstan atau balanced dengan SATU panggilan oracle,
sedangkan klasik butuh hingga 2^n panggilan.

Jalankan: .venv/Scripts/python.exe 03_deutsch_jozsa.py
Tidak butuh API key IBM - jalan di simulator lokal.
"""

import sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

import random
from qiskit import QuantumCircuit
from qiskit.primitives import StatevectorSampler

N_INPUT = 2  # jumlah qubit input


def oracle_konstan(qc, nilai):
    """Fungsi konstan: f(x) = nilai untuk semua x."""
    if nilai == 1:
        qc.x(N_INPUT)  # flip ancilla


def oracle_balanced(qc, bitmask):
    """Fungsi balanced: f(x) = bitmask . x (parity).
    Contoh bitmask='10': f(x) = x0, bitmask='11': f(x) = x0 XOR x1."""
    for i, bit in enumerate(bitmask):
        if bit == "1":
            qc.cx(i, N_INPUT)


def buat_sirkuit_dj(oracle_type, param):
    """Sirkuit Deutsch-Jozsa: n qubit input + 1 ancilla."""
    qc = QuantumCircuit(N_INPUT + 1, N_INPUT)
    qc.x(N_INPUT)      # ancilla ke |1>
    qc.h(range(N_INPUT + 1))  # superposisi semua qubit

    # Panggil oracle SATU kali (di sinilah keunggulan kuantum)
    if oracle_type == "konstan":
        oracle_konstan(qc, param)
    else:
        oracle_balanced(qc, param)

    qc.h(range(N_INPUT))  # interferensi: ekstrak informasi global
    qc.measure(range(N_INPUT), range(N_INPUT))
    return qc


def buat_semua_kasus():
    """Empat kasus uji: 2 konstan + 2 balanced.
    Bitmask balanced harus punya minimal satu '1',
    karena '00' berarti f(x)=0 (itu konstan, bukan balanced)."""
    bitmask_valid = [format(i, f"0{N_INPUT}b")
                     for i in range(1, 2 ** N_INPUT)]
    b1, b2 = random.sample(bitmask_valid, 2)
    return [
        ("konstan", 0),
        ("konstan", 1),
        ("balanced", b1),
        ("balanced", b2),
    ]


def tebak_jenis(counts):
    """Dari satu pengukuran: semua nol = konstan, selain itu balanced."""
    if set(counts.keys()) == {"00"}:
        return "konstan"
    return "balanced"


def main():
    print("=== Praktikum 3: Deutsch-Jozsa ===")
    print(f"Fungsi 2-bit, klasik butuh hingga {2**N_INPUT} panggilan oracle.")
    print("Kuantum: SATU panggilan.\n")

    kasus_list = buat_semua_kasus()
    sirkuit_list = [buat_sirkuit_dj(t, p) for t, p in kasus_list]

    print(f"Contoh sirkuit (oracle {kasus_list[0][0]}, f(x)={kasus_list[0][1]}):")
    print(sirkuit_list[0].draw(output="text"))

    sampler = StatevectorSampler()
    job = sampler.run(sirkuit_list, shots=100)
    hasil = job.result()

    print("\n" + "=" * 58)
    print(f"{'Oracle':<12}{'Detail':<10}{'Hasil ukur':<22}{'Kesimpulan':<12}")
    print("-" * 58)

    semua_benar = True
    for (jenis, param), dist in zip(kasus_list, hasil):
        counts = dist.data.c.get_counts()
        tebakan = tebak_jenis(counts)
        benar = tebakan == jenis
        semua_benar &= benar
        status = "BENAR" if benar else "SALAH"
        print(f"{jenis:<12}f(x)={param!s:<5}{str(counts):<22}{tebakan:<12}{status}")

    print("-" * 58)
    if semua_benar:
        print("Semua kasus terjawab BENAR dengan satu panggilan oracle.")
        print("Hasil '00' murni = konstan; ada pola lain = balanced.")
        print("Catatan: pola bit terbalik dari bitmask karena Qiskit "
              "memakai little-endian (q0 = bit paling kanan).")
    else:
        print("Ada kasus salah - periksa implementasi oracle.")


if __name__ == "__main__":
    main()
