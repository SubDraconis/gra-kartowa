import pygame
import main

pygame.init()
czy_gra = True
okno = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Gra")
ścieżka_obrazu = "tlo.png"
pelny_ekran = False
try:
    obraz_tlo = pygame.image.load(ścieżka_obrazu)
    szerokość_obrazu, wysokość_obrazu = obraz_tlo.get_size()
except pygame.error as komunikat_bledu:
    print(f"Nie udało się wczytać obrazu: {ścieżka_obrazu}")
    print(f"Błąd Pygame: {komunikat_bledu}")
    print("Program zakończony z błędem wczytywania obrazu.") # Dodana linijka!
    pygame.quit()
    exit()

class tlo:
    def __init__(self, obraz, x, y, powierzchnia_rysująca): # Dodajemy argument powierzchnia_rysująca
        self.obraz = obraz
        self.x = x
        self.y = y
        self.powierzchnia_rysująca = powierzchnia_rysująca # Zapisujemy powierzchnię

    def rysuj(self):
        self.powierzchnia_rysująca.blit(self.obraz, (self.x, self.y)) # Rysujemy na ZAPISANEJ powierzchni

ekran_rysujący = okno # Domyślnie rysujemy na oknie
tło_gry = tlo(obraz_tlo, 0, 0, ekran_rysujący) # Przekazujemy powierzchnię do konstruktora tła!


while czy_gra:
    okno.fill((0, 0, 0))
    for event in pygame.event.get(): # Pętla zdarzeń
        if event.type == pygame.QUIT:
            czy_gra = False
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_F11:
                pelny_ekran = not pelny_ekran
                if pelny_ekran:
                    ekran = pygame.display.set_mode((0, 0), pygame.FULLSCREEN | pygame.DOUBLEBUF | pygame.HWSURFACE)
                    ekran_rysujący = ekran # Aktualizujemy powierzchnię rysującą na 'ekran' (pełny ekran)
                    tło_gry.powierzchnia_rysująca = ekran # **WAŻNE**: Aktualizacja powierzchni w obiekcie tło_gry!
                else:
                    ekran = pygame.display.set_mode((800, 600), pygame.RESIZABLE)
                    ekran_rysujący = okno # Aktualizujemy powierzchnię rysującą na 'okno' (okienkowy)
                    tło_gry.powierzchnia_rysująca = okno # **WAŻNE**: Aktualizacja powierzchni w obiekcie tło_gry!


    tło_gry.rysuj() # Teraz metoda rysuj() używa ZAPISANEJ powierzchni 'powierzchnia_rysująca'

    pygame.display.flip()
