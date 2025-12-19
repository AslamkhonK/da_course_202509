import pygame
import random

# ---------------- Конфигурация ----------------
WIDTH, HEIGHT = 800, 400
FPS = 60
GROUND_HEIGHT = 300

# Цвета
WHITE = (255,255,255)
BLACK = (0,0,0)
GREEN = (0,200,0)
RED = (200,0,0)
GRAY = (220,220,220)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dino Game")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 30)

# ---------------- Динозавр ----------------
class Dino:
    def __init__(self):
        self.width = 40
        self.height = 50
        self.x = 50
        self.y = GROUND_HEIGHT - self.height
        self.vel_y = 0
        self.jump_power = -15
        self.gravity = 1
        self.is_jumping = False

    def jump(self):
        if not self.is_jumping:
            self.vel_y = self.jump_power
            self.is_jumping = True

    def update(self):
        self.vel_y += self.gravity
        self.y += self.vel_y
        if self.y >= GROUND_HEIGHT - self.height:
            self.y = GROUND_HEIGHT - self.height
            self.vel_y = 0
            self.is_jumping = False

    def draw(self, surface):
        pygame.draw.rect(surface, GREEN, (self.x, self.y, self.width, self.height))

# ---------------- Кактус ----------------
class Cactus:
    def __init__(self):
        self.width = 20
        self.height = random.randint(40, 60)
        self.x = WIDTH
        self.y = GROUND_HEIGHT - self.height
        self.color = RED
        self.speed = 10

    def update(self):
        self.x -= self.speed

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, (self.x, self.y, self.width, self.height))

    def off_screen(self):
        return self.x + self.width < 0

# ---------------- Игра ----------------
def main():
    run = True
    dino = Dino()
    obstacles = []
    spawn_timer = 0
    score = 0
    speed = 10

    while run:
        clock.tick(FPS)
        screen.fill(WHITE)

        # --- События ---
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                run = False
            elif e.type == pygame.KEYDOWN:
                if e.key == pygame.K_SPACE:
                    dino.jump()

        # --- Спавн кактусов ---
        spawn_timer += 1
        if spawn_timer > 60:
            obstacles.append(Cactus())
            spawn_timer = 0

        # --- Обновление объектов ---
        dino.update()
        for obs in obstacles:
            obs.speed = speed
            obs.update()
            obs.draw(screen)
        obstacles = [o for o in obstacles if not o.off_screen()]

        # --- Проверка столкновений ---
        dino_rect = pygame.Rect(dino.x, dino.y, dino.width, dino.height)
        for obs in obstacles:
            obs_rect = pygame.Rect(obs.x, obs.y, obs.width, obs.height)
            if dino_rect.colliderect(obs_rect):
                run = False

        # --- Отрисовка ---
        dino.draw(screen)
        pygame.draw.line(screen, BLACK, (0, GROUND_HEIGHT), (WIDTH, GROUND_HEIGHT), 2)

        # --- Счёт ---
        score += 1
        score_text = font.render(f"Score: {score}", True, BLACK)
        screen.blit(score_text, (10,10))

        pygame.display.flip()

    pygame.quit()
    print(f"Game Over! Score: {score}")

if __name__ == "__main__":
    main()
