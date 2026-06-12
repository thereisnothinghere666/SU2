import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Parametry powietrza
gamma = 1.4
rho_inf = 1.225
c0 = 343.0

# Wczytanie danych SU2
df = pd.read_csv("surface_flow.csv")

# Prędkości
u = df["Momentum_x"] / df["Density"]
v = df["Momentum_y"] / df["Density"]

# Moduł prędkości
V = np.sqrt(u**2 + v**2)

# Ciśnienie
p = (gamma - 1.0) * (
    df["Energy"]
    - 0.5 * df["Density"] * (u**2 + v**2)
)

df["Pressure"] = p
df["Velocity"] = V

print(df.head())

#Rozkład ciśnienia na profilu
plt.figure(figsize=(10,5))
plt.plot(df["x"], df["Pressure"])
plt.xlabel("x/c")
plt.ylabel("Pressure [Pa]")
plt.title("Rozkład ciśnienia na profilu")
plt.grid()
plt.show()



# Średnie ciśnienie
p_mean = np.mean(df["Pressure"])

# Fluktuacje ciśnienia
p_prime = df["Pressure"] - p_mean

# Uproszczona amplituda akustyczna
p_acoustic = p_prime

plt.figure(figsize=(10,5))
plt.plot(df["x"], p_acoustic)
plt.xlabel("x/c")
plt.ylabel("p' [Pa]")
plt.title("Przybliżone źródło akustyczne")
plt.grid()
plt.show()


r = 1.0        # odległość obserwatora [m]
p_ref = 20e-6 # ciśnienie odniesienia

# Uproszczone ciśnienie akustyczne w punkcie obserwacji
p_obs = np.sum(np.abs(p_acoustic)) / (4*np.pi*r)

SPL = 20*np.log10(np.abs(p_obs)/p_ref)

print(f"SPL = {SPL:.2f} dB")

plt.plot(alpha, spl_values, 'o-')
plt.xlabel("Kąt natarcia [deg]")
plt.ylabel("SPL [dB]")
plt.grid()
plt.show()