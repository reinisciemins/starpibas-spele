import random

# Klase, kas atbilst vienai virsotnei spēles kokā
class Virsotne:
    def __init__(self, id, virkne, p1, p2, limenis):
        self.id = id
        self.virkne = virkne
        self.p1 = p1
        self.p2 = p2
        self.limenis = limenis

# Klase, kas atbilst spēles kokam        
class Speles_koks:
    def __init__(self):
        self.virsotnu_kopa = []
        self.loku_kopa = dict()
    def pievienot_virsotni(self, virsotne):
        self.virsotnu_kopa.append(virsotne)
    def pievienot_loku(self, sakumvirsotne_id, beiguvirsotne_id):
        self.loku_kopa[sakumvirsotne_id] = self.loku_kopa.get(sakumvirsotne_id, []) + [beiguvirsotne_id]

# Funkcija, kas ģenerē gadījuma skaitļu virkni noteiktam garumam
def genereta_virkne(garums):
    virkne = ""
    for _ in range(garums):
        virkne += str(random.randint(1, 3))
    return virkne

# Funkcija, kas ļauj lietotājam ievadīt virknes garumu
def ievadiet_virknes_garumu():
    while True:
        try:
            garums = int(input("Ievadiet virknes garumu (15-25): "))
            if 15 <= garums <= 25:
                return garums
            else:
                print("Garumam jābūt no 15 līdz 25. Mēģiniet vēlreiz.")
        except ValueError:
            print("Lūdzu, ievadiet veselu skaitli.")

# Funkcija, kas attēlo spēles stāvokli
def attelo_speles_stavokli(virkne, p1, p2, limenis):
    print("\n" + "="*40)
    print(f"Gājiens: {limenis}")
    print(f"Virkne: {virkne}")
    print(f"Spēlētājs 1 punkti: {p1}")
    print(f"Spēlētājs 2 punkti: {p2}")
    print("="*40)

# Funkcija, lai spēlētājs izvēlētos gājiena pozīciju
def izvele_gajiena(virkne, speletaja_nr):
    while True:
        print(f"\nSpēlētājs {speletaja_nr}, izvēlieties skaitli no virknes:")
        pozicija = input(f"Ievadiet pozīciju (1-{len(virkne)}): ")
        try:
            pozicija = int(pozicija)
            if 1 <= pozicija <= len(virkne):
                return virkne[pozicija-1]
            else:
                print(f"Pozīcijai jābūt no 1 līdz {len(virkne)}.")
        except ValueError:
            print("Lūdzu, ievadiet veselu skaitli.")

# Funkcija, kas veic gājiena pārbaudi un atjauno spēles stāvokli
def gajiena_parbaude(izveletais_skaitlis, generetas_virsotnes, pasreizeja_virsotne):
    if izveletais_skaitlis in pasreizeja_virsotne[1]:
        global j
        new_id = 'A' + str(j)
        j += 1
        # Izveidojam jaunu virkni, izņemot izvēlēto skaitli (atrodot pirmo atrasto)
        pozicija = pasreizeja_virsotne[1].find(izveletais_skaitlis)
        new_virkne = pasreizeja_virsotne[1][:pozicija] + pasreizeja_virsotne[1][pozicija+1:]
        # Punktu atjaunošana: ja pašreizējais līmenis ir nepāra – pirmā spēlētāja zaudē, citādi otrā
        if pasreizeja_virsotne[4] % 2 == 1:
            new_p1 = pasreizeja_virsotne[2] - int(izveletais_skaitlis)
            new_p2 = pasreizeja_virsotne[3]
        else:
            new_p1 = pasreizeja_virsotne[2]
            new_p2 = pasreizeja_virsotne[3] - int(izveletais_skaitlis)
        new_level = pasreizeja_virsotne[4] + 1
        jauna_virsotne = Virsotne(new_id, new_virkne, new_p1, new_p2, new_level)
        
        # Pārbaudām, vai šāds stāvoklis jau eksistē spēles kokā
        jau_eksiste = False
        i = 0
        while (not jau_eksiste) and (i < len(sp.virsotnu_kopa)):
            if (sp.virsotnu_kopa[i].virkne == jauna_virsotne.virkne and
                sp.virsotnu_kopa[i].p1 == jauna_virsotne.p1 and
                sp.virsotnu_kopa[i].p2 == jauna_virsotne.p2 and
                sp.virsotnu_kopa[i].limenis == jauna_virsotne.limenis):
                jau_eksiste = True
            else:
                i += 1
                
        if not jau_eksiste:
            sp.pievienot_virsotni(jauna_virsotne)
            generetas_virsotnes.append([new_id, new_virkne, new_p1, new_p2, new_level])
            sp.pievienot_loku(pasreizeja_virsotne[0], new_id)
        else:
            j -= 1
            sp.pievienot_loku(pasreizeja_virsotne[0], sp.virsotnu_kopa[i].id)

# ---------------------------------------------------------------------
# Rekurzīvā funkcija, kas ģenerē daļējo spēles koku līdz noteiktam (maksimālajam) dziļumam
def generet_daļu_speles_koku_rec(current_state, max_dziļums):
    if current_state[4] >= max_dziļums or current_state[1] == "":
        return
    for i in range(len(current_state[1])):
        digit = current_state[1][i]
        new_virkne = current_state[1][:i] + current_state[1][i+1:]
        if current_state[4] % 2 == 1:
            new_p1 = current_state[2] - int(digit)
            new_p2 = current_state[3]
        else:
            new_p1 = current_state[2]
            new_p2 = current_state[3] - int(digit)
        new_level = current_state[4] + 1
        
        global j
        new_id = 'A' + str(j)
        j += 1
        new_state = [new_id, new_virkne, new_p1, new_p2, new_level]
        
        # Pārbaudām, vai šāds stāvoklis jau ir koka virsotnēs
        eksiste = False
        for v in sp.virsotnu_kopa:
            if (v.virkne == new_state[1] and v.p1 == new_state[2] and 
                v.p2 == new_state[3] and v.limenis == new_state[4]):
                eksiste = True
                break
        if eksiste:
            sp.pievienot_loku(current_state[0], new_id)
        else:
            sp.pievienot_virsotni(Virsotne(new_id, new_virkne, new_p1, new_p2, new_level))
            sp.pievienot_loku(current_state[0], new_id)
            generet_daļu_speles_koku_rec(new_state, max_dziļums)
# ---------------------------------------------------------------------

# Interaktīvā spēles funkcija – spēle tiek izspēlēta no sākuma līdz brīdim,
# kad virknes vērtība kļūst tukša (spēle beidzas)
def spelet_speli():
    garums = ievadiet_virknes_garumu()
    sakuma_virkne = genereta_virkne(garums)
    print(f"Ģenerētā virkne: {sakuma_virkne}")
    p1 = 80
    p2 = 80
    global sp, j
    sp = Speles_koks()
    # Saglabājam sākuma stāvokli, kurš tiks izmantots arī vēlāk koka ģenerēšanai
    initial_state = ['A1', sakuma_virkne, p1, p2, 1]
    sp.pievienot_virsotni(Virsotne('A1', sakuma_virkne, p1, p2, 1))
    generetas_virsotnes = [initial_state]
    j = 2
    current_state = initial_state
    
    while current_state[1]:
        attelo_speles_stavokli(current_state[1], current_state[2], current_state[3], current_state[4])
        speletaja_nr = 1 if current_state[4] % 2 == 1 else 2
        izveletais = izvele_gajiena(current_state[1], speletaja_nr)
        gajiena_parbaude(izveletais, generetas_virsotnes, current_state)
        current_state = generetas_virsotnes[0]
        generetas_virsotnes.pop(0)
        
    attelo_speles_stavokli(current_state[1], current_state[2], current_state[3], current_state[4])
    print("\nSpēle beigusies!")
    if current_state[2] > current_state[3]:
        print("Uzvarētājs: Spēlētājs 1")
    elif current_state[2] < current_state[3]:
        print("Uzvarētājs: Spēlētājs 2")
    else:
        print("Neizšķirts!")
    
    # Pēc spēles beigām paprasām maksimālo dziļumu un izvadām daļējo spēles koku,
    # kas ģenerēts no sākuma stāvokļa (initial_state)
    while True:
        try:
            max_dziļums = int(input("Ievadiet maksimālo dziļumu, līdz kuram tiks ģenerēts koks: "))
            if max_dziļums >= 1:
                break
            else:
                print("Dziļumam jābūt vismaz 1.")
        except ValueError:
            print("Lūdzu, ievadiet veselu skaitli.")
    
    # Atjaunojam koka struktūru, sākot no sākuma stāvokļa
    sp = Speles_koks()
    sp.pievienot_virsotni(Virsotne(initial_state[0], initial_state[1], initial_state[2], initial_state[3], initial_state[4]))
    j = 2
    generet_daļu_speles_koku_rec(initial_state, max_dziļums)
    
    print("\nDaļējs spēles koks (dziļums", max_dziļums, "):")
    print("\nVirsotnes:")
    for v in sp.virsotnu_kopa:
        print(f"ID: {v.id}, Virkne: {v.virkne}, P1: {v.p1}, P2: {v.p2}, Dziļums: {v.limenis}")
    print("\nLoki:")
    for sakum, beigu in sp.loku_kopa.items():
        print(f"{sakum} -> {beigu}")

def main():
    print("Spēle sākas!")
    spelet_speli()

if __name__ == "__main__":
    main()
