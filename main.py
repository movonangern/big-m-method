import xpress as xp

def def_variables(model, lager_namen, n_regionen):
    lager_eröffnet = [xp.var(vartype=xp.binary, name=f"Lager_{name}") for name in lager_namen]
    transport_menge = [[xp.var(name=f"Transport_{name}_{r}") for r in range(n_regionen)] for name in lager_namen]
    
    model.addVariable(lager_eröffnet)
    for tm in transport_menge:
        model.addVariable(tm)
        
    return lager_eröffnet, transport_menge

def add_constraints(model, lager_eröffnet, transport_menge, nachfrage, n_lager, n_regionen, lager_kapazität):
   
    # Nachfragebedingung
    for r in range(n_regionen):
        model.addConstraint(xp.Sum(transport_menge[l][r] for l in range(n_lager)) == nachfrage[r])
        
    # Kapazitätsbedingung
    for l in range(n_lager):
        model.addConstraint(xp.Sum(transport_menge[l][r] for r in range(n_regionen)) <= lager_kapazität[l] * lager_eröffnet[l])
        
    # Höchstens 2 Lager eröffnen
    model.addConstraint(xp.Sum(lager_eröffnet[l] for l in range(n_lager)) <= 2)
    
    # Spezifische Bedingungen
    model.addConstraint(lager_eröffnet[2] <= lager_eröffnet[1])  # Wenn Frankfurt eröffnet wird, dann auch Berlin
    model.addConstraint(lager_eröffnet[0] + lager_eröffnet[1] >= 1)  # Entweder Hamburg oder Berlin


def define_objective(model, lager_eröffnet, transport_menge, betriebskosten, transportkosten, lager_namen, n_regionen):
    model.setObjective(xp.Sum(betriebskosten[l] * lager_eröffnet[l] for l in range(len(lager_namen))) +
                       xp.Sum(transportkosten[l][r] * transport_menge[l][r] for l in range(len(lager_namen)) for r in range(n_regionen)))
    
def solve_model(model):
    model.solve()

def print_results(model, lager_eröffnet, transport_menge, lager_namen, n_regionen):
    print(f"Lösungsstatus: {model.getProbStatusString()} \
          \nZielfunktionswert: {model.getObjVal()}" )
    for l, name in enumerate(lager_namen):
        if model.getSolution(lager_eröffnet[l]) > 0.5:
            print(f"Lager {name} wird eröffnet.")
        else:
            print(f"Lager {name} wird nicht eröffnet.")
            
    for l, name in enumerate(lager_namen):
        for r in range(n_regionen):
            print(f"Transportmenge von Lager {name} zu Region {r}: {model.getSolution(transport_menge[l][r])}")


def main():
    model = xp.problem("Lagerstandortwahl")
    
    n_lager = 4
    n_regionen = 3
    lager_namen = ["Hamburg", "Berlin", "Frankfurt", "München"]
    lager_kapazität = [10000] * n_lager
    nachfrage = [8000, 7000, 40000]
    betriebskosten = [10000, 12000, 8000, 15000]
    transportkosten = [[20, 40, 50], [48, 15, 26], [26, 35, 18], [24, 50, 35]]
    
    lager_eröffnet, transport_menge = def_variables(model, lager_namen, n_regionen)
    
    # Beim Aufrufen von add_constraints() werden die Argumente betriebskosten und transportkosten entfernt
    add_constraints(model, lager_eröffnet, transport_menge, nachfrage, n_lager, n_regionen, lager_kapazität)
    
    define_objective(model, lager_eröffnet, transport_menge, betriebskosten, transportkosten, lager_namen, n_regionen)
    solve_model(model)
    print_results(model, lager_eröffnet, transport_menge, lager_namen, n_regionen)

if __name__ == "__main__":
    main()






