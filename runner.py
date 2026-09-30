import pygame
import random
import sys
import math
import array
import os

# --- Settings ---
WIDTH, HEIGHT = 800, 400
FPS = 60
GROUND_HEIGHT = 50
GRAVITY = 0.8
JUMP_STRENGTH = -15
OBSTACLE_SPEED = 6
SPAWN_RATE = 90  # frames between obstacles
HIGHSCORE_FILE = "highscore.txt"

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (34, 139, 34)
RED = (220, 20, 60)
SKY = (135, 206, 235)
BROWN = (139, 69, 19)
GOLD = (255, 215, 0)

pygame.init()
pygame.mixer.init(frequency=22050, size=-16, channels=1, buffer=512)
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Simple Runner")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 28)
big_font = pygame.font.SysFont("Arial", 48)
small_font = pygame.font.SysFont("Arial", 20)

# --- Sound generation (no external files needed) ---
def make_beep(freq, duration_ms, volume=0.4):
    sample_rate = 22050
    n_samples = int(sample_rate * duration_ms / 1000.0)
    buf = array.array("h")
    for t in range(n_samples):
        # Simple sine with fade-out to avoid clicks
        envelope = 1.0 - (t / n_samples)
        value = int(32767 * volume * envelope * math.sin(2 * math.pi * freq * t / sample_rate))
        buf.append(value)
    sound = pygame.sndarray.make_sound(buf)
    return sound

try:
    jump_sound = make_beep(600, 120)
    crash_sound = make_beep(150, 300)
    score_sound = make_beep(900, 80)
    SOUNDS_OK = True
except Exception:
    jump_sound = crash_sound = score_sound = None
    SOUNDS_OK = False

def play(sound):
    if SOUNDS_OK and sound:
        sound.play()

# --- High score helpers ---
def load_highscore():
    try:
        if os.path.exists(HIGHSCORE_FILE):
            with open(HIGHSCORE_FILE, "r") as f:
                return int(f.read().strip() or 0)
    except Exception:
        pass
    return 0

def save_highscore(score):
    try:
        with open(HIGHSCORE_FILE, "w") as f:
            f.write(str(score))
    except Exception:
        pass

# --- Player ---
class Player:
    def __init__(self):
        self.width = 40
        self.height = 50
        self.x = 100
        self.y = HEIGHT - GROUND_HEIGHT - self.height
        self.vel_y = 0
        self.on_ground = True
        self.score = 0

    def jump(self):
        if self.on_ground:
            self.vel_y = JUMP_STRENGTH
            self.on_ground = False
            play(jump_sound)

    def update(self):
        self.vel_y += GRAVITY
        self.y += self.vel_y

        if self.y >= HEIGHT - GROUND_HEIGHT - self.height:
            self.y = HEIGHT - GROUND_HEIGHT - self.height
            self.vel_y = 0
            self.on_ground = True

    def draw(self, surface):
        pygame.draw.rect(surface, GREEN, (self.x, self.y, self.width, self.height))
        pygame.draw.circle(surface, BLACK, (self.x + 28, self.y + 15), 5)

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

# --- Obstacle ---
class Obstacle:
    def __init__(self):
        self.width = random.randint(25, 45)
        self.height = random.randint(40, 80)
        self.x = WIDTH + 10
        self.y = HEIGHT - GROUND_HEIGHT - self.height
        self.passed = False

    def update(self):
        self.x -= OBSTACLE_SPEED

    def draw(self, surface):
        pygame.draw.rect(surface, RED, (self.x, self.y, self.width, self.height))

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def is_off_screen(self):
        return self.x + self.width < 0

# --- Game ---
def main():
    player = Player()
    obstacles = []
    frame_count = 0
    game_over = False
    highscore = load_highscore()
    running = True

    while running:
        clock.tick(FPS)
        frame_count += 1

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_SPACE, pygame.K_UP):
                    if not game_over:
                        player.jump()
                    else:
                        # Restart
                        player = Player()
                        obstacles = []
                        frame_count = 0
                        game_over = False
                if event.key == pygame.K_ESCAPE:
                    running = False

        if not game_over:
            if frame_count % SPAWN_RATE == 0:
                obstacles.append(Obstacle())

            player.update()

            for obs in obstacles[:]:
                obs.update()
                if obs.is_off_screen():
                    obstacles.remove(obs)
                if not obs.passed and obs.x + obs.width < player.x:
                    obs.passed = True
                    player.score += 1
                    play(score_sound)
                    if player.score > highscore:
                        highscore = player.score
                        save_highscore(highscore)

            player_rect = player.get_rect()
            for obs in obstacles:
                if player_rect.colliderect(obs.get_rect()):
                    game_over = True
                    play(crash_sound)
                    if player.score > highscore:
                        highscore = player.score
                        save_highscore(highscore)

        # Draw
        screen.fill(SKY)
        pygame.draw.rect(screen, BROWN, (0, HEIGHT - GROUND_HEIGHT, WIDTH, GROUND_HEIGHT))
        pygame.draw.line(screen, BLACK, (0, HEIGHT - GROUND_HEIGHT), (WIDTH, HEIGHT - GROUND_HEIGHT), 3)

        player.draw(screen)
        for obs in obstacles:
            obs.draw(screen)

        score_text = font.render(f"Score: {player.score}", True, BLACK)
        hs_text = font.render(f"High: {highscore}", True, GOLD)
        screen.blit(score_text, (20, 20))
        screen.blit(hs_text, (20, 55))

        if not SOUNDS_OK:
            muted = small_font.render("(sounds unavailable)", True, (80, 80, 80))
            screen.blit(muted, (WIDTH - 180, 20))

        if game_over:
            over_text = big_font.render("GAME OVER", True, RED)
            restart_text = font.render("Press SPACE to restart", True, BLACK)
            screen.blit(over_text, (WIDTH // 2 - over_text.get_width() // 2, HEIGHT // 2 - 50))
            screen.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2 + 10))

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
