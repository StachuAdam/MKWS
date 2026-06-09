import cantera as ct
import matplotlib.pyplot as plt
import numpy as np

gas = ct.Solution('gri30.yaml')

# Definiujemy dwa przypadki: czysty metan oraz metan z 30% wodoru
cases = {
    'Czysty CH4': 'O2:2, N2:7.52, CH4:1.0',
    'CH4 + 30% H2': 'O2:2, N2:7.52, CH4:0.7, H2:0.3'
}

plt.figure(figsize=(10, 5))

for label, mixture in cases.items():
    gas.TPX = 1100, 5 * 101325, mixture # 1100 K, 5 bar
    r = ct.Reactor(gas, clone=False)
    sim = ct.ReactorNet([r])
    
    times = []
    T = []
    
    time = 0.0
    # Symulacja przez 0.1 sekundy z małym krokiem
    for i in range(1000):
        time += 1e-4
        sim.advance(time)
        times.append(time * 1e3) # zamiana na ms
        T.append(r.T)
        
    plt.plot(times, T, label=label, linewidth=2)

plt.xlabel('Czas [ms]')
plt.ylabel('Temperatura [K]')
plt.title('Wpływ dodatku wodoru na profil temperatury podczas zapłonu')
plt.legend()
plt.grid(True)
plt.savefig('wodor_porownanie_T.png', dpi=300)
plt.show()
