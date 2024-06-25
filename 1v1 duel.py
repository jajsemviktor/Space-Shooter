import pygame
import sys
import random
from random import randint

pygame.init()
clock = pygame.time.Clock()
font = pygame.font.Font(None, 64)
game_over = False

# Barvy
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (200, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
MAGENTA = (255, 0, 255)

# OBRAZKY
vs_img = pygame.image.load('versus.png')
vs_img = pygame.transform.scale(vs_img, (100, 100))
srdce_img = pygame.image.load("srdicko.png")
srdce_img = pygame.transform.scale(srdce_img, (50, 50))
pozadi_img = pygame.image.load("space2.jpg")
pozadi_img = pygame.transform.scale(pozadi_img, (1280, 720))
modrej_img = pygame.image.load("modrej.jpg")
modrej_img = pygame.transform.scale(modrej_img, (50, 50))
zelenej_img = pygame.image.load("zelenej.png")
zelenej_img = pygame.transform.scale(zelenej_img, (50, 50))

# POZICE
WIDTH, HEIGHT = 1280, 720
rect_x = 0
rect_y = random.randint(0, HEIGHT)
rectz_x = 1230
rectz_y = random.randint(0, HEIGHT)
rectzivotyzelene_x = 1000
rectzivotyzelene_y = 20
rectzivotymodre_x = 200
rectzivotymodre_y = 20

zivoty_modre = 3
zivoty_zelene = 3

# Střely
strelamodreho = []
strelazeleneho = []

# Počitadla střel a časovače
modre_strely_count = 0
zelene_strely_count = 0
modre_last_shot_time = 0
zelene_last_shot_time = 0
shot_limit = 8
cooldown_time = 3000  # 3 sekundy


def restart_game():
    global rect_x, rect_y, game_over, rectz_x, rectz_y, rectzivotyzelene_x, rectzivotyzelene_y, rectzivotymodre_x, rectzivotymodre_y, zivoty_modre, zivoty_zelene
    game_over = False
    zivoty_modre = 3
    zivoty_zelene = 3
    strelamodreho = []
    strelazeleneho = []
    modre_strely_count = 0
    zelene_strely_count = 0
    modre_last_shot_time = 0
    zelene_last_shot_time = 0
    shot_limit = 8
    cooldown_time = 3000

# Funkce pro střílení
def strilet(x, y):
    global modre_strely_count, modre_last_shot_time
    if modre_strely_count < shot_limit:
        strelamodreho.append(pygame.Rect(x, y, 40, 10))
        modre_strely_count += 1
        if modre_strely_count == shot_limit:
            modre_last_shot_time = pygame.time.get_ticks()

def striletzeleny(x, y):
    global zelene_strely_count, zelene_last_shot_time
    if zelene_strely_count < shot_limit:
        strelazeleneho.append(pygame.Rect(x, y, 40, 10))
        zelene_strely_count += 1
        if zelene_strely_count == shot_limit:
            zelene_last_shot_time = pygame.time.get_ticks()

# OBRAZOVKA
screen = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Gta VI.exe")

# ZAKLADHRY
while True:
    current_time = pygame.time.get_ticks()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_d:
                if modre_strely_count < shot_limit or current_time - modre_last_shot_time >= cooldown_time:
                    if modre_strely_count >= shot_limit:
                        modre_strely_count = 0
                    strilet(rect_x + 50, rect_y + 20)
            if event.key == pygame.K_LEFT:
                if zelene_strely_count < shot_limit or current_time - zelene_last_shot_time >= cooldown_time:
                    if zelene_strely_count >= shot_limit:
                        zelene_strely_count = 0
                    striletzeleny(rectz_x - 50, rectz_y + 20)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r and game_over:
                    restart_game()

    # Reset střel po cooldownu
    if modre_strely_count >= shot_limit and current_time - modre_last_shot_time >= cooldown_time:
        modre_strely_count = 0

    if zelene_strely_count >= shot_limit and current_time - zelene_last_shot_time >= cooldown_time:
        zelene_strely_count = 0

    # OVLADANI
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        rectz_y -= 1
    if keys[pygame.K_DOWN]:
        rectz_y += 1
    if keys[pygame.K_w]:
        rect_y -= 1
    elif keys[pygame.K_s]:
        rect_y += 1
    
    rect_y = max(120, min(rect_y, HEIGHT - 50))
    rectz_y = max(120, min(rectz_y, HEIGHT - 50))
    
    screen.fill(WHITE)
    screen.blit(pozadi_img, (0, 0))
    screen.blit(vs_img, (rectzivotyzelene_x - 400, rectzivotyzelene_y))
    modre = screen.blit(modrej_img, (rect_x, rect_y))
    zelene = screen.blit(zelenej_img, (rectz_x, rectz_y))
    zivotzeleny1 = screen.blit(srdce_img, (rectzivotyzelene_x, rectzivotyzelene_y))

    for i in range(zivoty_zelene):
        screen.blit(srdce_img, (rectzivotyzelene_x - i * 100, rectzivotyzelene_y))

    for i in range(zivoty_modre):
        screen.blit(srdce_img, (rectzivotymodre_x + i * 100, rectzivotymodre_y))
  
    # Aktualizace a vykreslení střel
    for strela in strelamodreho:
        strela.x += 4
        pygame.draw.rect(screen, RED, strela)
        if strela.colliderect(zelene):
            strelamodreho.remove(strela)
            zivoty_zelene -= 1
            if zivoty_zelene == 0:
                print("VYHRÁL MODRÝ")
                game_over = True
               

    for strelaz in strelazeleneho:
        strelaz.x -= 4
        pygame.draw.rect(screen, RED, strelaz)
        if strelaz.colliderect(modre):
            strelazeleneho.remove(strelaz)
            zivoty_modre -= 1
            if zivoty_modre == 0:
                print("VYHRÁL ZELENÝ")
                game_over = True
               

    # Odstranění střel mimo obrazovku
    strelamodreho = [strela for strela in strelamodreho if strela.x < WIDTH]
    strelazeleneho = [strelaz for strelaz in strelazeleneho if strelaz.x > 0]
    
    # Vykreslení textu pro počet zbývajících střel
    modre_zbyva_strely = shot_limit - modre_strely_count
    zelene_zbyva_strely = shot_limit - zelene_strely_count

    modre_text = font.render(f"{modre_zbyva_strely}", True, WHITE)
    zelene_text = font.render(f"{zelene_zbyva_strely}", True, WHITE)

    screen.blit(modre_text, (rect_x + 50, rect_y - 30))
    screen.blit(zelene_text, (rectz_x - 50, rectz_y - 30))
    
    if game_over:
            font = pygame.font.SysFont(None, 36)
            text = font.render("Konec hry! Stiskni 'R' pro restart.", True, RED)
            text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
            screen.blit(text, text_rect)
    
    pygame.display.flip()

h