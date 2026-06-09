import cantera as ct
import matplotlib.pyplot as plt

gas = ct.Solution('gri30.yaml')
oh_idx = gas.species_index('OH')

T0 = 1300
P = 5 * 101325
H2_fractions = [0.0, 0.1, 0.3, 0.5]
labels = {
    0.0: 'Czysty CH4',
    0.1: '10% H2 + 90% CH4',
    0.3: '30% H2 + 70% CH4',
    0.5: '50% H2 + 50% CH4',
}

plt.figure(figsize=(10, 6))

for X_H2 in H2_fractions:
    X_CH4 = 1.0 - X_H2
    o2 = 2.0 * X_CH4 + 0.5 * X_H2
    n2 = o2 * 3.76
    mix = f'CH4:{X_CH4}, H2:{X_H2}, O2:{o2}, N2:{n2}'

    gas.TPX = T0, P, mix
    r = ct.Reactor(gas, clone=False)
    sim = ct.ReactorNet([r])

    times = []
    OH = []
    t = 0.0
    while t < 0.1:
        t = sim.step()
        times.append(t * 1e3)
        OH.append(r.phase.X[oh_idx])

    plt.plot(times, OH, label=labels[X_H2], linewidth=2)

plt.xlabel('Czas [ms]')
plt.ylabel('Udział molowy OH [-]')
plt.title(f'Profil rodnika OH podczas zapłonu (T₀ = {T0} K, P = 5 bar)', fontweight='bold')
plt.legend()
plt.grid(True)
plt.savefig('OH_profil_1300K.png', dpi=300)
plt.show()
