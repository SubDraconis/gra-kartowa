# 0 kolumna nazwa 1 kolumna liczba 2 kolumna typ 3 kolumna hp 4 kolumna atak 5 kolumna broń 5 kolumna amunicja 6 kolumna przładowyanie 7 kolumna max amunicji 8 kolumna ruch/max	9 kolmna czy jest to karta jedno razowa 10	czy jest tylko na daną jednostke
import csv
import random

karty = []
karty_gracza1 = []
karty_gracza2 = []
aktualny_gracz = 1


class Card:
    def __init__(self, type, name, atak, hp):
        self.name = name
        self.type = type
        self.atak = int(atak)
        self.hp = int(hp)

    def __str__(self):
        return f'{self.name} {self.type} {self.hp} {self.atak}'


def read_cards():
    with open('karty.csv', newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for row in reader:
            for i in range(int(row[1])):
                karty.append(Card(row[2], row[0], row[4], row[3]))


read_cards()
random.shuffle(karty)
'''for card in karty:
    print(card)'''


# pokaż graczowi 4 karty z wierzchu tablicy (z numerami 1 2 3 4)
def proponowane_Karty():
    proponowaneKarty = []
    for i in range(4):
        proponowanaKarta = karty.pop()
        proponowaneKarty.append(proponowanaKarta)

    print(f"Graczu nr {aktualny_gracz}, masz do wyboru takie karty: ", end=' ')
    for numer, karta in enumerate(proponowaneKarty):
        print(f"{numer+1}) {karta.name}, ", end=' ')
    print()

    return proponowaneKarty


def wyborKart():
    wybor = input(f"Wpisz które wybierasz:")
    karty_wybrane = wybor.split(",")
    print(karty_wybrane)
    return karty_wybrane


def usuwanieIDodawanieKart(proponowane_karty, karty_wybrane):
    for i in karty_wybrane:
        karta_dla_gracza1 = proponowane_karty.pop(int(i) - 1)
        if aktualny_gracz == 1:
            karty_gracza1.append(karta_dla_gracza1)
        else:
            karty_gracza2.append(karta_dla_gracza1)

    for a in proponowane_karty:
        karty.append(proponowane_karty.pop())

def atakuj():
    if aktualny_gracz == 2:
        hp = 0
        for karta in karty_gracza1:
            hp += karta.hp
        atak = 0
        for karta in karty_gracza2:
            atak += karta.atak
        liczba_kart = len(karty_gracza1)
        karta.hp -= atak / liczba_kart
        for karta in karty_gracza1:
            karta.hp -= atak / liczba_kart
            if karta.hp < 0 or karta.hp == 0:
                karty_gracza1.remove(karta)

    if aktualny_gracz == 1:
        hp = 0
        for karta in karty_gracza2:
            hp += karta.hp
        atak = 0
        for karta in karty_gracza1:
            atak += karta.atak
        liczba_kart = len(karty_gracza2)
        for karta in karty_gracza2:
            karta.hp -= atak / liczba_kart
            if karta.hp < 0 or karta.hp == 0:
                karty_gracza2.remove(karta)
# zeby bylo widac ile ma aktulanie hp
# ile gracz ma ataku
# podzielic atak : liczba kart

while True:
    proponowane_karty = proponowane_Karty()
    karty_wybrane = wyborKart()
    usuwanieIDodawanieKart(proponowane_karty, karty_wybrane)

    odpowiedź_gracza = input("Czy chcesz zaatakować przeciwnika?")
    if odpowiedź_gracza == "tak":
        print("Zaatakowałes przeciwnika!")
        atakuj()

    if aktualny_gracz == 1:
        aktualny_gracz = 2
    else:
        aktualny_gracz = 1
