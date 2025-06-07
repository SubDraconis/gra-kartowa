import io
import sys
import csv
import random
import pygame 

# Importujemy funkcje i klasy z okienka
import okienko as ok
import definicje as defi

pygame.init()
#sys.stdin = io.TextIOWrapper(sys.stdin.buffer, encoding='utf-8')

# --- Klasy (Card) ---
class Card:
    def __init__(self, type, name, atak, hp, maxa_ammo, ammo, przeładowyanie):
        self.name = name
        self.type = type
        self.atak = int(atak)
        self.hp = int(hp)
        self.maxa_ammo = int(maxa_ammo)
        self.ammo = str(ammo)
        self.przeładowyanie = int(przeładowyanie)
        self.przeładowywania_czas = 0
        self.czy_wystrzelony = False
        self.obrazek = None  # Obrazek będzie ładowany w okienko.py

    def __str__(self):
        return f'{self.name} {self.type} {self.hp} {self.atak} {self.maxa_ammo} {self.ammo} {self.przeładowyanie} {self.przeładowywania_czas}'

# --- Zmienne globalne (stan gry) ---
karty = []
karty_gracza = [[], [], []]
postawienione_karty = [[], [], []]
aktualny_gracz = 1
koniec_gry = False

# --- Główna pętla gry ---
def run_game():
    """Główna funkcja uruchamiająca grę (logika)."""
    


    # Inicjalizacja gry
    defi.init_game()
    global koniec_gry, aktualny_gracz

    while not koniec_gry:
        # Faza wyboru kart
        proponowane = defi.proponowane_Karty()
        wybrane = defi.wyborKart(proponowane, aktualny_gracz)
        defi.usuwanieIDodawanieKart(proponowane, wybrane, aktualny_gracz)

        # Faza akcji
        akcje = defi.pobierz_akcje_gracza(aktualny_gracz)
        for akcja in akcje:
            if akcja == "postaw":
                defi.postaw_karte(aktualny_gracz)
            elif akcja == "atakuj":
                defi.atakuj(aktualny_gracz)

        # Faza przeładowania
        defi.przeładowanie_kart(1)
        defi.przeładowanie_kart(2)

        defi.zmien_gracza()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                koniec_gry = True
                break
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F11:
                    
                        ok.skaluj_tlo_do_szerokosci_ekranu("tlo.png", 800)
                    
        # Sprawdzenie warunków końca gry
        # TODO: Dodaj warunki końca gry

    print("Koniec gry!")

# --- Funkcja main ---
if __name__ == "__main__":
    run_game()