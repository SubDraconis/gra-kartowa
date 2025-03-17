import io
import sys
import csv
import random
import pygame  # Importujemy pygame tutaj

import main as m #Importujemy main.py

def read_cards():
    """Wczytuje karty z pliku CSV."""
    try:
        with open('karty.csv', newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            for row in reader:
                for _ in range(int(row[1])):
                    try:
                        m.karty.append(m.Card(row[2], row[0], row[4], row[3], row[8], row[6], row[7]))
                    except (ValueError, IndexError) as e:
                        print(f"Błąd wczytywania karty {row[0]}: {e}")
    except FileNotFoundError:
        print("Błąd: Nie znaleziono pliku 'karty.csv'")
        sys.exit(1)

def proponowane_Karty():
    """Zwraca listę 4 losowych kart."""
    return random.sample(m.karty, k=4)

def wyborKart(proponowane_karty, gracz):
    """Obsługuje wybór kart przez gracza (interakcja w konsoli)."""
    print(f"Graczu nr {gracz}, masz do wyboru takie karty: ")
    for numer, karta in enumerate(proponowane_karty):
        print(f"{numer + 1}) {karta.name} (Atak: {karta.atak}, HP: {karta.hp})")
    while True:
        wybor = input("Wybierz karty (np. 1,3) lub wpisz 'pas': ")
        if wybor.lower() == 'pas':
            return []
        try:
            wybrane_indeksy = [int(i) - 1 for i in wybor.split(",")]
            if all(0 <= i < len(proponowane_karty) for i in wybrane_indeksy):
                wybrane_karty = [proponowane_karty[i] for i in wybrane_indeksy]
                return wybrane_karty
            else:
                print("Nieprawidłowe numery kart. Spróbuj ponownie.")
        except ValueError:
            print("Nieprawidłowy format. Wprowadź numery kart oddzielone przecinkami.")


def usuwanieIDodawanieKart(proponowane_karty, karty_wybrane, gracz):
    """Usuwa wybrane karty i dodaje je graczowi."""
    for karta in karty_wybrane:
        proponowane_karty.remove(karta)
    m.karty_gracza[gracz].extend(karty_wybrane)

def postaw_karte(gracz):
    """Obsługuje postawienie karty przez gracza."""
    if not m.karty_gracza[gracz]:
        print("Gracz nie ma kart do postawienia.")
        return None

    print(f"Gracz {gracz}, twoje karty:")
    for i, karta in enumerate(m.karty_gracza[gracz]):
        print(f"{i + 1}. {karta.name} (Atak: {karta.atak}, HP: {karta.hp})")

    while True:
        try:
            wybor = input("Wybierz kartę do postawienia (numer) lub wpisz 'pas': ")
            if wybor.lower() == 'pas':
                return None
            wybor = int(wybor) - 1
            if 0 <= wybor < len(m.karty_gracza[gracz]):
                karta = m.karty_gracza[gracz].pop(wybor)
                m.postawienione_karty[gracz].append(karta)
                print(f"Postawiono kartę: {karta.name}")
                return karta
            else:
                print("Nieprawidłowy numer karty.")
        except ValueError:
            print("Nieprawidłowy format. Wprowadź numer karty.")

def atakuj(gracz):
    """Obsługuje atak."""
    if not m.postawienione_karty[gracz]:
        print("Gracz nie ma kart na stole, nie może atakować.")
        return

    print(f"Gracz {gracz}, twoje karty na stole:")
    for i, karta in enumerate(m.postawienione_karty[gracz]):
        print(f"{i + 1}. {karta.name} (Atak: {karta.atak}, HP: {karta.hp})")

    while True:
        try:
            wybor = input("Wybierz kartę do ataku (numer) lub wpisz 'pas': ")
            if wybor.lower() == 'pas':
                return
            wybor = int(wybor) - 1
            if 0 <= wybor < len(m.postawienione_karty[gracz]):
                karta_atakujaca = m.postawienione_karty[gracz][wybor]
                if karta_atakujaca.czy_wystrzelony:
                    print("Ta karta już atakowała w tej turze!")
                    continue
                break
            else:
                print("Nieprawidłowy numer karty.")
        except ValueError:
            print("Nieprawidłowy format. Wprowadź numer karty.")

    if gracz == 1:
        przeciwnik = 2
    else:
        przeciwnik = 1

    if not m.postawienione_karty[przeciwnik]:
        print("Przeciwnik nie ma kart na stole. Atakujesz bazę!")
        # TODO: Dodaj logikę ataku na bazę
        return

    print(f"Gracz {przeciwnik}, karty przeciwnika na stole:")
    for i, karta in enumerate(m.postawienione_karty[przeciwnik]):
        print(f"{i + 1}. {karta.name} (Atak: {karta.atak}, HP: {karta.hp})")

    while True:
        try:
            wybor_celu = input("Wybierz kartę przeciwnika do zaatakowania (numer) lub 'pas': ")
            if wybor_celu.lower() == 'pas':
                return
            wybor_celu = int(wybor_celu) - 1
            if 0 <= wybor_celu < len(m.postawienione_karty[przeciwnik]):
                karta_cel = m.postawienione_karty[przeciwnik][wybor_celu]
                break
            else:
                print("Nieprawidłowy numer karty.")
        except ValueError:
            print("Nieprawidłowy format. Wprowadź numer karty.")

    karta_cel.hp -= karta_atakujaca.atak
    karta_atakujaca.czy_wystrzelony = True
    print(f"Atakujesz kartę {karta_cel.name} ({karta_cel.hp} HP) kartą {karta_atakujaca.name} ({karta_atakujaca.atak} Atak)")

    if karta_cel.hp <= 0:
        m.postawienione_karty[przeciwnik].remove(karta_cel)
        print(f"Karta {karta_cel.name} została zniszczona!")

def przeładowanie_kart(gracz):
    """Przeładowuje karty gracza."""
    for karta in m.postawienione_karty[gracz]:
        if karta.czy_wystrzelony:
            przeładowanie(karta)

def przeładowanie(karta):
    """Przeładowuje pojedynczą kartę."""
    if karta.przeładowywania_czas == karta.przeładowyanie:
        karta.czy_wystrzelony = False
        karta.przeładowywania_czas = 0
    else:
        karta.przeładowywania_czas += 1

def zmien_gracza():
    """Zmienia aktualnego gracza."""
    m.aktualny_gracz
    m.aktualny_gracz = 3 - m.aktualny_gracz  # 1 -> 2, 2 -> 1

def pobierz_akcje_gracza(gracz):
    """Pobiera akcje gracza i zwraca je jako listę stringów."""
    akcje = []
    print(f"\nTura gracza {gracz}:")
    while True:
        akcja = input("Wybierz akcję (postaw, atakuj, pas): ").lower()
        if akcja in ("postaw", "atakuj", "pas"):
            akcje.append(akcja)
            if akcja == "pas":
                break
            if akcja == "postaw":
                break # Po postawieniu karty nie pytamy już o akcje w tej turze
        else:
            print("Nieprawidłowa akcja. Wpisz 'postaw', 'atakuj' lub 'pas'.")
    return akcje


def init_game():
    """Inicjalizuje stan gry."""
    read_cards()
    random.shuffle(m.karty)