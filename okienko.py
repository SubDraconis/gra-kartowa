# okienko.py
import pygame
import main  # Importujemy main.py

class KartaUI:
    def __init__(self, x, y, szerokosc, wysokosc, karta=None, kolor_tla=(255, 255, 255), kolor_obramowania=(0, 0, 0), grubosc_obramowania=2):
        self.x = x
        self.y = y
        self.szerokosc = szerokosc
        self.wysokosc = wysokosc
        self.kolor_tla = kolor_tla
        self.kolor_obramowania = kolor_obramowania
        self.grubosc_obramowania = grubosc_obramowania
        self.rect = pygame.Rect(self.x, y, self.szerokosc, self.wysokosc)
        self.karta = karta
        self.czcionka = pygame.font.Font(None, 24)

    def rysuj(self, powierzchnia):
        pygame.draw.rect(powierzchnia, self.kolor_tla, self.rect)
        pygame.draw.rect(powierzchnia, self.kolor_obramowania, self.rect, self.grubosc_obramowania)

        if self.karta:
            tekst_nazwa = self.czcionka.render(self.karta.name, True, (0, 0, 0))
            powierzchnia.blit(tekst_nazwa, (self.x + 5, self.y + 5))
            tekst_atak = self.czcionka.render(f"Atak: {self.karta.atak}", True, (0,0,0))
            powierzchnia.blit(tekst_atak, (self.x + 5, self.y+ 30))
            tekst_hp = self.czcionka.render(f"HP: {self.karta.hp}", True, (0,0,0))
            powierzchnia.blit(tekst_hp, (self.x + 5, self.y + 55))
            if self.karta.obrazek:
                obrazek_skalowany = pygame.transform.scale(self.karta.obrazek, (self.szerokosc - 10, self.wysokosc - 80))
                powierzchnia.blit(obrazek_skalowany, (self.x + 5, self.y + 80))

class Tlo:
    def __init__(self, obraz, x, y):
        self.obraz = obraz
        self.x = x
        self.y = y

    def rysuj(self, powierzchnia):
        powierzchnia.blit(self.obraz, (self.x, self.y))

def skaluj_tlo_do_szerokosci_ekranu(sciezka_obrazu, szerokosc_ekranu):
    """Skaluje tło do szerokości ekranu."""
    try:
        obraz_tlo_oryginalny = pygame.image.load(sciezka_obrazu)
        oryginalna_szerokosc, oryginalna_wysokosc = obraz_tlo_oryginalny.get_size()
        wspolczynnik = szerokosc_ekranu / oryginalna_szerokosc
        nowa_wysokosc = int(oryginalna_wysokosc * wspolczynnik)
        obraz_skalowany = pygame.transform.scale(obraz_tlo_oryginalny, (szerokosc_ekranu, nowa_wysokosc))
        return obraz_skalowany
    except pygame.error as e:
        print(f"Błąd skalowania tła: {e}")
        return None
#--- brak obrazków kart w okienko.py---
def zaladuj_obrazki_kart():
    """Ładuje obrazki dla kart (teraz w okienko.py)."""
    for karta in main.karty:  # Odwołujemy się do main.karty
        try:
            karta.obrazek = pygame.image.load(f'karty/{karta.name}.png')
        except pygame.error as e:
            print(f"Nie udało się załadować obrazka dla karty {karta.name}: {e}")

def rysuj_karty(powierzchnia, karty, x_start, y_start, odstep):
    """Rysuje prostokąty reprezentujące karty."""
    for i, karta in enumerate(karty):
        karta_ui = KartaUI(x_start + i * (100 + odstep), y_start, 100, 150, karta)
        karta_ui.rysuj(powierzchnia)



# --- Inicjalizacja Pygame (w okienko.py) ---
pygame.init()  # Dodajemy inicjalizację Pygame
okno_szerokosc = 800
okno_wysokosc = 600
okno = pygame.display.set_mode((okno_szerokosc, okno_wysokosc))
pygame.display.set_caption("Gra")
pelny_ekran = False
powierzchnia_ekranu_do_rysowania = okno
sciezka_obrazu = "tlo.png"

# Skalowanie tła do szerokości ekranu
obraz_tlo_skalowany = skaluj_tlo_do_szerokosci_ekranu(sciezka_obrazu, okno_szerokosc)
if obraz_tlo_skalowany:
    # Tworzenie instancji klasy Tlo
    tlo = Tlo(obraz_tlo_skalowany, 0, 0)
    # Rysowanie tła
    tlo.rysuj(powierzchnia_ekranu_do_rysowania)
else:
    print("Nie udało się załadować i skalować obrazu tła")

pygame.display.flip()
braz_tlo_skalowany = skaluj_tlo_do_szerokosci_ekranu(sciezka_obrazu, okno_szerokosc)
