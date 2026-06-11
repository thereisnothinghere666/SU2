import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import glob

from scipy.signal import welch
from scipy.fft import rfft, rfftfreq

# =====================================================
# PARAMETRY
# =====================================================

gamma = 1.4

dt = 5e-4             # krok czasowy [s]
U_inf = 30.0          # prędkość napływu [m/s]
chord = 1.0           # cięciwa [m]

x_obs = 1.5           # punkt obserwacyjny
y_obs = 0.5

# =====================================================
# WCZYTANIE PLIKÓW
# =====================================================

files = sorted(glob.glob("data/restart_flow_*.csv"))

if len(files) < 10:
    raise ValueError("Za mało plików do analizy.")

print(f"Znaleziono {len(files)} snapshotów")

# =====================================================
# WYBÓR PUNKTU OBSERWACYJNEGO
# =====================================================

ref = pd.read_csv(files[0])

dist = np.sqrt(
    (ref["x"] - x_obs)**2 +
    (ref["y"] - y_obs)**2
)

idx = np.argmin(dist)

print("\nPunkt obserwacyjny:")
print(ref.loc[idx, ["x", "y"]])

# =====================================================
# HISTORIE CZASOWE
# =====================================================

pressure_history = []
mass_history = []
energy_history = []

for file in files:

    df = pd.read_csv(file)

    rho = df["Density"].values
    rhou = df["Momentum_x"].values
    rhov = df["Momentum_y"].values
    E = df["Energy"].values

    u = rhou / rho
    v = rhov / rho

    pressure = (gamma - 1.0) * (
        E - 0.5 * rho * (u*u + v*v)
    )

    # punkt obserwacyjny
    pressure_history.append(pressure[idx])

    # całkowita masa
    mass_history.append(np.sum(rho))

    # całkowita energia
    energy_history.append(np.sum(E))

pressure_history = np.array(pressure_history)
mass_history = np.array(mass_history)
energy_history = np.array(energy_history)

time = np.arange(len(files)) * dt

# =====================================================
# FLUKTUACJE CIŚNIENIA
# =====================================================

p_mean = np.mean(pressure_history)
p_prime = pressure_history - p_mean

p_rms = np.sqrt(np.mean(p_prime**2))

# =====================================================
# SPL
# =====================================================

p_ref = 20e-6

SPL = 20 * np.log10(p_rms / p_ref)

print("\n=== AKUSTYKA ===")
print(f"p_rms = {p_rms:.6f} Pa")
print(f"SPL   = {SPL:.2f} dB")

# =====================================================
# FFT
# =====================================================

N = len(p_prime)

freq = rfftfreq(N, dt)
fft_amp = np.abs(rfft(p_prime))

peak_index = np.argmax(fft_amp[1:]) + 1
peak_frequency = freq[peak_index]

print(f"\nDominująca częstotliwość: {peak_frequency:.2f} Hz")

# =====================================================
# STROUHAL
# =====================================================

St = peak_frequency * chord / U_inf

print(f"Liczba Strouhala: {St:.4f}")

# =====================================================
# PSD
# =====================================================

f_psd, psd = welch(
    p_prime,
    fs=1/dt,
    nperseg=min(1024, N)
)

# =====================================================
# WYKRESY
# =====================================================

plt.figure(figsize=(10,5))
plt.plot(time, pressure_history)
plt.title("Ciśnienie całkowite")
plt.xlabel("t [s]")
plt.ylabel("p [Pa]")
plt.grid()
plt.tight_layout()

plt.figure(figsize=(10,5))
plt.plot(time, p_prime)
plt.title("Fluktuacje ciśnienia")
plt.xlabel("t [s]")
plt.ylabel("p' [Pa]")
plt.grid()
plt.tight_layout()

plt.figure(figsize=(10,5))
plt.semilogy(freq, fft_amp)
plt.title("FFT")
plt.xlabel("f [Hz]")
plt.ylabel("Amplitude")
plt.grid()
plt.tight_layout()

plt.figure(figsize=(10,5))
plt.semilogy(f_psd, psd)
plt.title("PSD (Welch)")
plt.xlabel("f [Hz]")
plt.ylabel("PSD")
plt.grid()
plt.tight_layout()

plt.show()
