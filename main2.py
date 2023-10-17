import xpress as xp

# Daten
I = ['Hamburg', 'Berlin', 'Frankfurt', 'München']
J = ['Region 1', 'Region 2', 'Region 3']

ME = {
    'Hamburg': 10000,
    'Berlin': 10000,    
    'Frankfurt': 10000,
    'München': 10000
}

D = {
    'Region 1': 8000,
    'Region 2': 7000,
    'Region 3': 40000
}

C = {
    'Hamburg': 40000,
    'Berlin': 30000,
    'Frankfurt': 35000,
    'München': 50000
}

T = {
    ('Hamburg', 'Region 1'): 20,
    ('Hamburg', 'Region 2'): 40,
    ('Hamburg', 'Region 3'): 50,
    ('Berlin', 'Region 1'): 48,
    ('Berlin', 'Region 2'): 15,
    ('Berlin', 'Region 3'): 26,
    ('Frankfurt', 'Region 1'): 26,
    ('Frankfurt', 'Region 2'): 35,
    ('Frankfurt', 'Region 3'): 18,
    ('München', 'Region 1'): 24,
    ('München', 'Region 2'): 50,
    ('München', 'Region 3'): 35
}

K = 2

# Variablen
x = {(i,j): xp.var(vartype=xp.continuous, name=f'x_{i}_{j}') for i in I for j in J}
y = {i: xp.var(vartype=xp.binary, name=f'y_{i}') for i in I}

# Modell
model = xp.problem("Lagerstandortwahl")

# Variablen dem Modell hinzufügen
model.addVariable(x, y)

# Zielfunktion
# Zielfunktion (Transportkosten pro Einheit)
model.setObjective(xp.Sum(C[i] * y[i] for i in I) + xp.Sum(T[i,j] * x[i,j]/20 for i in I for j in J))

# Nebenbedingungen
# Deckung der Nachfrage
for j in J:
    model.addConstraint(xp.Sum(x[i,j] for i in I) >= D[j])

# Kapazitätsbeschränkung
for i in I:
    model.addConstraint(xp.Sum(x[i,j] for j in J) <= ME[i] * y[i])

# Maximale Anzahl der Lager
model.addConstraint(xp.Sum(y[i] for i in I) <= K)

# Zusätzliche Bedingungen
model.addConstraint(y['Frankfurt'] <= y['Berlin'])
model.addConstraint(y['Hamburg'] + y['Berlin'] >= 1)

# Modell lösen
model.solve()

# Ausgabe
# Überprüfen, ob das Problem unlösbar ist, und wenn ja, ein Infeasibility-Datei erstellen
if model.getProbStatusString() == 'infeasible':
    print("Das Modell ist unlösbar.")
else:
    # Ausgabe
    print(f"Zielfunktionswert: {model.getObjVal()}")
    for i in I:
        if model.getSolution(y[i]) > 0.5:
            print(f"Lager {i} wird eröffnet.")
            for j in J:
                print(f"  An {j} werden {model.getSolution(x[i,j])} Einheiten versendet.")
        else:
            print(f"Lager {i} wird nicht eröffnet.")
            for j in J:
                print(f"  An {j} werden 0 Einheiten versendet.")