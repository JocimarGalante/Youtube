import sys
import os
import pygame
import random
import os

def resource_path(relative_path):
    """Retorna o caminho absoluto para o recurso, seja no .exe ou não"""
    try:
        # Para PyInstaller
        base_path = sys._MEIPASS  
    except Exception:
        # Caso contrário, caminho local
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# Inicializa o Pygame
pygame.init()

# Definir as cores
WHITE = (255, 255, 255)

# Tamanho da tela
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Definindo o tamanho da tela
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Space Shooter")

# Carregar imagens
background_image = pygame.image.load(resource_path('./Image/space_background.jpg'))  # Usando resource_path
bullet_image = pygame.Surface([5, 10])  # Imagem do tiro (faremos um retângulo branco)
bullet_image.fill(WHITE)

# Carregar imagens de personagens (naves)
player_images = [
    pygame.image.load(resource_path('./Image/spaceship.png')),
    pygame.image.load(resource_path('./Image/spaceship1.png')),
    pygame.image.load(resource_path('./Image/spaceship2.png')),
    pygame.image.load(resource_path('./Image/spaceship3.png')),
    pygame.image.load(resource_path('./Image/spaceship4.png'))
]

def load_highscore():
    if os.path.exists("highscore.txt"):
        with open("highscore.txt", "r") as f:
            return int(f.read())
    return 0

def save_highscore(score):
    with open("highscore.txt", "w") as f:
        f.write(str(score))

class Player(pygame.sprite.Sprite):
    def __init__(self, image):
        super().__init__()
        self.image = pygame.transform.scale(image, (50, 50))
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50)
        self.speed = 5

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.x > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.x < SCREEN_WIDTH - self.rect.width:
            self.rect.x += self.speed

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load(resource_path('./Image/asteroid.png'))
        self.image = pygame.transform.scale(self.image, (40, 40))
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, SCREEN_WIDTH - self.rect.width)
        self.rect.y = random.randint(-100, -40)
        self.speed = random.randint(3, 6)

    def update(self):
        self.rect.y += self.speed
        if self.rect.y > SCREEN_HEIGHT:
            self.rect.y = random.randint(-100, -40)
            self.rect.x = random.randint(0, SCREEN_WIDTH - self.rect.width)

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = bullet_image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = 7

    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()

def draw_pause_menu():
    font = pygame.font.SysFont("Arial", 40)
    text_continue = font.render("Pressione C para continuar", True, WHITE)
    text_reset = font.render("Pressione R para resetar", True, WHITE)
    text_exit = font.render("Pressione Q para sair", True, WHITE)
    screen.fill((0, 0, 0))
    screen.blit(text_continue, (SCREEN_WIDTH // 2 - text_continue.get_width() // 2, SCREEN_HEIGHT // 2 - 50))
    screen.blit(text_reset, (SCREEN_WIDTH // 2 - text_reset.get_width() // 2, SCREEN_HEIGHT // 2))
    screen.blit(text_exit, (SCREEN_WIDTH // 2 - text_exit.get_width() // 2, SCREEN_HEIGHT // 2 + 50))
    pygame.display.flip()

def draw_game_over_menu(score, highscore, player_image):
    font = pygame.font.SysFont("Arial", 40)
    screen.fill((0, 0, 0))
    text_game_over = font.render("Game Over", True, WHITE)
    text_score = font.render(f"Score: {score}", True, WHITE)
    text_highscore = font.render(f"Recorde: {highscore}", True, WHITE)
    text_retry = font.render("Pressione R para tentar novamente", True, WHITE)
    text_menu = font.render("Pressione M para voltar ao menu", True, WHITE)
    text_exit = font.render("Pressione Q para sair", True, WHITE)

    screen.blit(text_game_over, (SCREEN_WIDTH // 2 - text_game_over.get_width() // 2, 100))
    screen.blit(text_score, (SCREEN_WIDTH // 2 - text_score.get_width() // 2, 180))
    screen.blit(text_highscore, (SCREEN_WIDTH // 2 - text_highscore.get_width() // 2, 230))
    screen.blit(text_retry, (SCREEN_WIDTH // 2 - text_retry.get_width() // 2, 300))
    screen.blit(text_menu, (SCREEN_WIDTH // 2 - text_menu.get_width() // 2, 350))
    screen.blit(text_exit, (SCREEN_WIDTH // 2 - text_exit.get_width() // 2, 400))
    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    game(player_image)
                    waiting = False
                elif event.key == pygame.K_m:
                    start_game()
                    waiting = False
                elif event.key == pygame.K_q:
                    pygame.quit()
                    exit()

def game(player_image):
    clock = pygame.time.Clock()
    all_sprites = pygame.sprite.Group()
    bullets = pygame.sprite.Group()
    enemies = pygame.sprite.Group()

    player = Player(player_image)
    all_sprites.add(player)

    for i in range(10):
        enemy = Enemy()
        all_sprites.add(enemy)
        enemies.add(enemy)

    score = 0
    highscore = load_highscore()
    font = pygame.font.SysFont("Arial", 30)

    running = True
    paused = False

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not paused:
                    bullet = Bullet(player.rect.centerx, player.rect.top)
                    all_sprites.add(bullet)
                    bullets.add(bullet)
                elif event.key == pygame.K_ESCAPE:
                    paused = True
                elif event.key == pygame.K_c and paused:
                    paused = False
                elif event.key == pygame.K_r and paused:
                    return game(player_image)
                elif event.key == pygame.K_q and paused:
                    running = False

        if not paused:
            all_sprites.update()

            for bullet in bullets:
                enemy_hits = pygame.sprite.spritecollide(bullet, enemies, True)
                for enemy in enemy_hits:
                    score += 10
                    bullet.kill()
                    enemy = Enemy()
                    all_sprites.add(enemy)
                    enemies.add(enemy)

            if pygame.sprite.spritecollideany(player, enemies):
                if score > highscore:
                    save_highscore(score)
                draw_game_over_menu(score, max(score, highscore), player_image)
                return

            screen.blit(background_image, (0, 0))
            all_sprites.draw(screen)

            score_text = font.render(f"Score: {score}", True, WHITE)
            highscore_text = font.render(f"Highscore: {highscore}", True, (0, 255, 0))
            screen.blit(score_text, [10, 10])
            screen.blit(highscore_text, [SCREEN_WIDTH - highscore_text.get_width() - 10, 10])

        if paused:
            draw_pause_menu()

        pygame.display.flip()
        clock.tick(60)

def start_game():
    selected_player_image = None
    running = True
    ship_rects = []

    while running:
        screen.fill((0, 0, 0))
        font = pygame.font.SysFont("Arial", 40)
        text_select = font.render("Escolha sua nave e pressione Enter", True, WHITE)
        screen.blit(text_select, (SCREEN_WIDTH // 2 - text_select.get_width() // 2, 50))

        ship_rects.clear()
        for i, image in enumerate(player_images):
            x = (SCREEN_WIDTH // 6) * (i + 1) - 25
            y = SCREEN_HEIGHT // 2
            image_scaled = pygame.transform.scale(image, (50, 50))
            rect = image_scaled.get_rect(topleft=(x, y))
            screen.blit(image_scaled, rect.topleft)
            ship_rects.append((rect, image_scaled, player_images[i]))

            if selected_player_image == player_images[i]:
                pygame.draw.rect(screen, (0, 255, 0), rect, 3)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and selected_player_image is not None:
                    game(selected_player_image)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                for rect, image_scaled, original_image in ship_rects:
                    if rect.collidepoint(mouse_pos):
                        selected_player_image = original_image

if __name__ == "__main__":
    start_game()
