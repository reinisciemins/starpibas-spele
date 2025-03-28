import random


#Klase, kas atbilst vienai virsotnei spēles kokā
class Virsotne:
    
    #Klases konstruktors, kas izveido virsotnes eksemplāru
    #Katrā virsotnes eksmeplārā glabājas virsotnes unikāls identifikators (id), skaitliskā virkne (virkne)
    #pirmā spēlētāja punkti (p1), otrā spēlētāja punkti(p2), un virsotnes atrašanās līmeņa numurs
    #Glabātie dati tiek padoti kā konstruktora argumenti
    def __init__(self, id, virkne, p1, p2, limenis):
        self.id = id
        self.virkne = virkne
        self.p1 = p1
        self.p2 = p2
        self.limenis = limenis
               
#Klase, kas atbilst spēles kokam        
class Speles_koks:
    
    #Klases konstruktors, kas izveido spēles koka eksemplāru
    #Spēles koka eksemplārs ietver sevī virsotņu kopu, kas tiek veidota kā Python saraksts un
    #loku kopu, kas tiek veidota kā Python vārdnīca (dictionary)
    def __init__(self):
        self.virsotnu_kopa = []
        self.loku_kopa = dict()
    
    #Klases Speles_koks metode, kas pievieno spēles kokam jaunu virsotni, kuru saņem kā argumentu
    def pievienot_virsotni(self, Virsotne):
        self.virsotnu_kopa.append(Virsotne)
        
    #Klases Speles_koks metode, kura papildina loku kopu
    def pievienot_loku(self, sakumvirsotne_id, beiguvirsotne_id):
        self.loku_kopa[sakumvirsotne_id] = self.loku_kopa.get(sakumvirsotne_id, []) + [beiguvirsotne_id]


#Funkcija, kas atbilstoši veiktajam gājienam iegūst jaunu spēles koka virsotni
def gajiena_parbaude(izveletais_skaitlis, generetas_virsotnes, pasreizeja_virsotne):
    if izveletais_skaitlis in pasreizeja_virsotne[1]:
        global j
        id_new = 'A' + str(j)
        j += 1
        
        # Veidojam jaunu virkni, izņemot izvēlēto skaitli
        mainita_virkne = pasreizeja_virsotne[1]
        pozicija = mainita_virkne.find(izveletais_skaitlis)
        mainita_virkne = mainita_virkne[:pozicija] + mainita_virkne[pozicija+1:]
        
        # Atjaunojam punktu skaitu - atņemot izvēlēto skaitli
        if (pasreizeja_virsotne[4] % 2) == 0:  # Otrā spēlētāja gājiens
            p1_new = pasreizeja_virsotne[2]
            p2_new = pasreizeja_virsotne[3] - int(izveletais_skaitlis)
        else:  # Pirmā spēlētāja gājiens
            p1_new = pasreizeja_virsotne[2] - int(izveletais_skaitlis)
            p2_new = pasreizeja_virsotne[3]
            
        limenis_new = pasreizeja_virsotne[4] + 1
        jauna_virsotne = Virsotne(id_new, mainita_virkne, p1_new, p2_new, limenis_new)
        
        # Pārbaudām, vai šāda virsotne jau eksistē
        parbaude = False
        i = 0
        while (not parbaude) and (i <= len(sp.virsotnu_kopa) - 1):
            if (sp.virsotnu_kopa[i].virkne == jauna_virsotne.virkne) and \
               (sp.virsotnu_kopa[i].p1 == jauna_virsotne.p1) and \
               (sp.virsotnu_kopa[i].p2 == jauna_virsotne.p2) and \
               (sp.virsotnu_kopa[i].limenis == jauna_virsotne.limenis):
                parbaude = True
            else:
                i += 1
                
        if not parbaude:
            sp.pievienot_virsotni(jauna_virsotne)
            generetas_virsotnes.append([id_new, mainita_virkne, p1_new, p2_new, limenis_new])
            sp.pievienot_loku(pasreizeja_virsotne[0], id_new)
        else:
            j -= 1
            sp.pievienot_loku(pasreizeja_virsotne[0], sp.virsotnu_kopa[i].id)

# Funkcija, kas ģenerē gadījuma skaitļu virkni
def genereta_virkne(garums):
    virkne = ""
    for _ in range(garums):
        virkne += str(random.randint(1, 3))
    return virkne

# Funkcija, kas ļauj spēlētājam ievadīt virknes garumu
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

# Funkcija, lai spēlētājs izvēlētos gājienu
def izvele_gajiena(virkne, speletaja_nr):
    while True:
        print(f"\nSpēlētājs {speletaja_nr}, izvēlieties skaitli no virknes:")
        izveleta_pozicija = input(f"Ievadiet pozīciju (1-{len(virkne)}): ")
        try:
            izveleta_pozicija = int(izveleta_pozicija)
            if 1 <= izveleta_pozicija <= len(virkne):
                return virkne[izveleta_pozicija-1]
            else:
                print(f"Pozīcijai jābūt no 1 līdz {len(virkne)}.")
        except ValueError:
            print("Lūdzu, ievadiet veselu skaitli.")

# Galvenā programma
def spelet_speli():
    # Iegūstam virknes garumu no lietotāja
    garums = ievadiet_virknes_garumu()
    
    # Ģenerējam gadījuma skaitļu virkni
    sakuma_virkne = genereta_virkne(garums)
    print(f"Ģenerētā virkne: {sakuma_virkne}")
    
    # Sākuma punktu skaits katram spēlētājam
    p1 = 80
    p2 = 80
    
    # Spēles koks
    global sp
    sp = Speles_koks()
    
    # Saģenerēto virsotņu saraksts
    generetas_virsotnes = []
    
    # Pievienojam sākuma virsotni
    sp.pievienot_virsotni(Virsotne('A1', sakuma_virkne, p1, p2, 1))
    generetas_virsotnes.append(['A1', sakuma_virkne, p1, p2, 1])
    
    # Virsotņu skaitītājs
    global j
    j = 2
    
    # Spēles cikls
    pasreizeja_virsotne = generetas_virsotnes[0]
    
    while pasreizeja_virsotne[1]:  # Kamēr virkne nav tukša
        attelo_speles_stavokli(pasreizeja_virsotne[1], pasreizeja_virsotne[2], pasreizeja_virsotne[3], pasreizeja_virsotne[4])
        
        # Nosakām, kurš spēlētājs veic gājienu
        speletaja_nr = 1 if pasreizeja_virsotne[4] % 2 == 1 else 2
        
        # Spēlētājs izvēlas skaitli
        izveletais_skaitlis = izvele_gajiena(pasreizeja_virsotne[1], speletaja_nr)
        
        # Pārbaudām gājienu un atjaunojam spēles stāvokli
        gajiena_parbaude(izveletais_skaitlis, generetas_virsotnes, pasreizeja_virsotne)
        
        # Atjaunojam pašreizējo virsotni
        pasreizeja_virsotne = generetas_virsotnes[0]
        generetas_virsotnes.pop(0)
    
    # Spēles beigas
    attelo_speles_stavokli(pasreizeja_virsotne[1], pasreizeja_virsotne[2], pasreizeja_virsotne[3], pasreizeja_virsotne[4])
    print("\nSpēle beigusies!")
    
    # Nosakām uzvarētāju
    if pasreizeja_virsotne[2] > pasreizeja_virsotne[3]:
        print("Uzvarētājs: Spēlētājs 1")
    elif pasreizeja_virsotne[2] < pasreizeja_virsotne[3]:
        print("Uzvarētājs: Spēlētājs 2")
    else:
        print("Neizšķirts!")

# Izsaucam galveno funkciju
if __name__ == "__main__":
    spelet_speli()
