import cantera as ct
import matplotlib.pyplot as plt

gas = ct.Solution('gri30.yaml')
oh_idx = gas.species_index('OH')

def IgnitionDelay(gas):
    r = ct.Reactor(gas, clone=False)
    sim = ct.ReactorNet([r])

    max_time = 1.0
    OH_fraction_prev = 0
    t = 0

    while t < max_time:
        t = sim.step()
        OH_fraction = r.phase.X[oh_idx]
        if OH_fraction < OH_fraction_prev:
            break
        OH_fraction_prev = OH_fraction

    return t * 1e3

P = 5 * 101325
hydrogen_shares = [0.0, 0.1, 0.3, 0.5]

plt.figure(figsize=(10, 6))

for X_H2 in hydrogen_shares:
    X_CH4 = 1.0 - X_H2

    o2_needed = 2.0 * X_CH4 + 0.5 * X_H2
    n2_present = o2_needed * 3.76

    X_string = f'CH4:{X_CH4}, H2:{X_H2}, O2:{o2_needed}, N2:{n2_present}'

    T_list = []
    ign_delay = []

    for T in range(1100, 1650, 50):
        T_list.append(T)
        gas.TPX = T, P, X_string
        ign_delay.append(IgnitionDelay(gas))

    label_text = "Czysty CH4" if X_H2 == 0.0 else f"{X_H2*100:.0f}% H2 + {X_CH4*100:.0f}% CH4"
    plt.plot(T_list, ign_delay, 'o-', label=label_text)

plt.legend()
plt.xlabel('Temperatura początkowa [K]')
plt.ylabel('Opóźnienie zapłonu [ms]')
plt.yscale('log')
plt.title('Wpływ dodatku wodoru na czas opóźnienia zapłonu metanu (P = 5 bar)', fontweight='bold')
plt.grid(True, which="both", ls="--")
plt.savefig('wodor_metan_temperatura.png', dpi=300)
plt.show()
