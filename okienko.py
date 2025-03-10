import pygame

pygame.init()
czy_gra = True
okno_szerokosc = 800 # Zapamiętaj szerokość okna
okno_wysokosc = 600
okno = pygame.display.set_mode((okno_szerokosc, okno_wysokosc)) # Rozmiar okna nadal inicjujemy
pygame.display.set_caption("Gra - Skalowanie do szerokości - POPRAWIONE")

ścieżka_obrazu = "tlo.png" # Ścieżka do Twojego obrazu tła

ekran_info_początkowe = pygame.display.Info() # Pobierz informacje o ekranie POCZĄTKOWO, dla okna
szerokość_ekranu_okno = ekran_info_początkowe.current_w # Szerokość ekranu dla okna (może być użyteczna)


def skaluj_tlo_do_szerokosci_ekranu(sciezka_obrazu, szerokosc_ekranu):
    """
    Wczytuje obraz tła i skaluje go tak, aby jego szerokość
    dopasowała się do szerokości ekranu, zachowując proporcje.
    """
    try:
        obraz_tlo_oryginalny = pygame.image.load(sciezka_obrazu)
        oryginalna_szerokość_obrazu, oryginalna_wysokość_obrazu = obraz_tlo_oryginalny.get_size()

        współczynnik_skalowania_szerokości = szerokosc_ekranu / oryginalna_szerokość_obrazu
        docelowa_wysokość_obrazu = int(oryginalna_wysokość_obrazu * współczynnik_skalowania_szerokości)
        obraz_tlo_skalowany = pygame.transform.scale(obraz_tlo_oryginalny, (szerokosc_ekranu, docelowa_wysokość_obrazu))
        return obraz_tlo_skalowany

    except pygame.error as komunikat_bledu:
        print(f"Błąd w funkcji skaluj_tlo_do_szerokosci_ekranu: Nie udało się wczytać obrazu: {sciezka_obrazu}")
        print(f"Błąd Pygame: {komunikat_bledu}")
        return None

# Początkowe skalowanie tła dla trybu okienkowego
obraz_tlo_skalowany_okno = skaluj_tlo_do_szerokosci_ekranu(ścieżka_obrazu, okno_szerokosc) # Skaluj do szerokości okna
if obraz_tlo_skalowany_okno is None:
    pygame.quit()
    exit()


class tlo:
    def __init__(self, obraz, x, y):
        self.obraz = obraz
        self.x = x
        self.y = y

    def rysuj(self, powierzchnia): # Metoda rysuj teraz przyjmuje argument 'powierzchnia'
        powierzchnia.blit(self.obraz, (self.x, self.y)) # Rysuj na przekazanej powierzchni, a nie na stałe na 'okno'

tło_gry = tlo(obraz_tlo_skalowany_okno, 0, 0) # Użyj SKALOWANEGO obrazu tła dla okna

pelny_ekran = False # Początkowo tryb okienkowy
powierzchnia_ekranu_do_rysowania = okno # Początkowo rysujemy na 'okno'

while czy_gra:
    powierzchnia_ekranu_do_rysowania.fill((0, 0, 0)) # Wypełniaj AKTUALNĄ powierzchnię

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            czy_gra = False
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_F11:
                pelny_ekran = not pelny_ekran
                if pelny_ekran:
                    ekran = pygame.display.set_mode((0, 0), pygame.FULLSCREEN | pygame.DOUBLEBUF | pygame.HWSURFACE)
                    powierzchnia_ekranu_do_rysowania = ekran # Zmień powierzchnię rysowania na 'ekran' (pełny ekran)

                    ekran_info_fullscreen = pygame.display.Info() # Pobierz informacje o ekranie TERAZ, w trybie pełnoekranowym
                    szerokość_ekranu_fullscreen = ekran_info_fullscreen.current_w # Szerokość ekranu FULLSCREEN
                    print(f"Przełączam na PEŁNY EKRAN. Szerokość ekranu FULLSCREEN: {szerokość_ekranu_fullscreen} pikseli") # Komunikat DEBUG z szerokością FULLSCREEN
                    print(f"Rzeczywista rozdzielczość Fullscreen po set_mode: {ekran.get_width()}x{ekran.get_height()}") # DODANE: Komunikat diagnostyczny ROZDZIELCZOŚCI

                    # Skaluj tło do szerokości ekranu PEŁNOEKRANOWEGO i zaktualizuj obiekt tło_gry
                    obraz_tlo_skalowany_fullscreen = skaluj_tlo_do_szerokosci_ekranu(ścieżka_obrazu, szerokość_ekranu_fullscreen)
                    if obraz_tlo_skalowany_fullscreen:
                        tło_gry.obraz = obraz_tlo_skalowany_fullscreen
                        print("Obraz tła zaktualizowany dla PEŁNEGO EKRANU.")

                else:
                    ekran = pygame.display.set_mode((okno_szerokosc, okno_wysokosc), pygame.RESIZABLE) # Powrót do okna
                    powierzchnia_ekranu_do_rysowania = okno # Zmień powierzchnię rysowania z powrotem na 'okno'

                    print(f"Przełączam na OKNO. Szerokość okna: {okno_szerokosc} pikseli")
                    # Skaluj tło do szerokości OKNA i zaktualizuj obiekt tło_gry
                    obraz_tlo_skalowany_okno = skaluj_tlo_do_szerokosci_ekranu(ścieżka_obrazu, okno_szerokosc)
                    if obraz_tlo_skalowany_okno:
                        tło_gry.obraz = obraz_tlo_skalowany_okno
                        print("Obraz tła zaktualizowany dla OKNA.")

    tło_gry.rysuj(powierzchnia_ekranu_do_rysowania) # Rysuj tło, przekazując AKTUALNĄ powierzchnię do rysowania!
    pygame.display.flip()

pygame.quit()