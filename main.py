import pygame
import random
import math
import sys

pygame.init()

WIDTH, HEIGHT = 600, 790
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("CatchQuest- Code In Place 2025")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BG_COLOR = (30, 30, 40)
BASKET_COLOR = (200, 100, 50)
OBJECT_COLORS = [
    (255, 50, 50), (50, 255, 50), (50, 50, 255),
    (255, 255, 0), (255, 165, 0), (128, 0, 128),
    (0, 255, 255), (255, 105, 180)
]

clock = pygame.time.Clock()
FPS = 60

BASKET_WIDTH = 120
BASKET_HEIGHT = 30
BASKET_SPEED = 10

OBJ_RADIUS = 20
OBJ_FALL_SPEED_START = 4
OBJ_FALL_SPEED_INCREMENT = 0.3
MIN_SPAWN_DELAY = 10

font_title = pygame.font.SysFont("bookmanoldstyle", 24)
font_text = pygame.font.SysFont("bookmanoldstyle", 20)
font_button = pygame.font.SysFont("bookmanoldstyle", 40)
font_score = pygame.font.SysFont("bookmanoldstyle", 32)

logo_image = pygame.image.load("CatchQuest.jpg").convert_alpha()

class Basket:
    def __init__(self):
        self.width = BASKET_WIDTH
        self.height = BASKET_HEIGHT
        self.x = WIDTH // 2 - self.width // 2
        self.y = HEIGHT - self.height - 20
        self.speed = BASKET_SPEED
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def move(self, direction):
        if direction == "left" and self.rect.left > 0:
            self.rect.x -= self.speed
        if direction == "right" and self.rect.right < WIDTH:
            self.rect.x += self.speed

    def draw(self, screen):
        # Inverted trapezoid shape for basket
        top_width = self.width * 0.6
        bottom_width = self.width
        height = self.height

        top_x1 = self.rect.centerx - top_width // 2
        top_x2 = self.rect.centerx + top_width // 2
        bottom_x1 = self.rect.centerx - bottom_width // 2
        bottom_x2 = self.rect.centerx + bottom_width // 2
        top_y = self.rect.y
        bottom_y = self.rect.y + height

        inverted_points = [
            (top_x1, bottom_y),
            (top_x2, bottom_y),
            (bottom_x2, top_y),
            (bottom_x1, top_y)
        ]

        pygame.draw.polygon(screen, BASKET_COLOR, inverted_points)

        # Inner lighter shade for 3D effect
        inner_color = (255, 170, 120)
        inner_offset = 6
        inner_points = [
            (top_x1 + inner_offset, bottom_y - inner_offset),
            (top_x2 - inner_offset, bottom_y - inner_offset),
            (bottom_x2 - inner_offset, top_y + inner_offset),
            (bottom_x1 + inner_offset, top_y + inner_offset)
        ]
        pygame.draw.polygon(screen, inner_color, inner_points)

        # Shadow above basket
        shadow_color = (90, 50, 30)
        shadow_height = 5
        pygame.draw.rect(screen, shadow_color, (bottom_x1, top_y - shadow_height, bottom_width, shadow_height))

class FallingObject:
    SHAPES = ['circle', 'square', 'star', 'moon']

    def __init__(self, speed):
        self.radius = OBJ_RADIUS
        self.x = random.randint(self.radius, WIDTH - self.radius)
        self.y = -self.radius * 2
        self.color = random.choice(OBJECT_COLORS)
        self.speed = speed
        self.shape = random.choice(FallingObject.SHAPES)
        self.rect = pygame.Rect(self.x - self.radius, self.y - self.radius, self.radius * 2, self.radius * 2)

    def update(self):
        self.y += self.speed
        self.rect.y = self.y - self.radius

    def draw(self, screen):
        if self.shape == 'circle':
            pygame.draw.circle(screen, (20, 20, 20), (self.x + 2, int(self.y + 2)), self.radius)  # Shadow
            pygame.draw.circle(screen, self.color, (self.x, int(self.y)), self.radius)
        elif self.shape == 'square':
            pygame.draw.rect(screen, (20, 20, 20), (self.x - self.radius + 2, int(self.y - self.radius + 2), self.radius * 2, self.radius * 2))  # Shadow
            pygame.draw.rect(screen, self.color, (self.x - self.radius, int(self.y - self.radius), self.radius * 2, self.radius * 2))
        elif self.shape == 'star':
            self.draw_star(screen, self.color, self.x, int(self.y), self.radius)
        elif self.shape == 'moon':
            self.draw_moon(screen, self.color, self.x, int(self.y), self.radius)

    def draw_star(self, surface, color, x, y, radius):
        points = []
        for i in range(10):
            angle = i * math.pi / 5
            r = radius if i % 2 == 0 else radius // 2
            px = x + int(r * math.sin(angle))
            py = y - int(r * math.cos(angle))
            points.append((px, py))
        shadow = [(px + 2, py + 2) for px, py in points]
        pygame.draw.polygon(surface, (20, 20, 20), shadow)
        pygame.draw.polygon(surface, color, points)

    def draw_moon(self, surface, color, x, y, radius):
        pygame.draw.circle(surface, (20, 20, 20), (x + 2, y + 2), radius)  # Shadow
        pygame.draw.circle(surface, color, (x, y), radius)
        pygame.draw.circle(surface, BG_COLOR, (x + radius // 3, y - radius // 3), radius)

def draw_text(screen, text, x, y, font, color=WHITE):
    img = font.render(text, True, color)
    screen.blit(img, (x, y))

def draw_start_screen():
    screen.fill(BG_COLOR)

    # Project name at top
    title = "CatchQuest - Code In Place 2025"
    title_surf = font_title.render(title, True, WHITE)
    title_x = (WIDTH - title_surf.get_width()) // 2
    screen.blit(title_surf, (title_x, 30))

    # Resize and center logo (250x250)
    scaled_logo = pygame.transform.scale(logo_image, (250, 250))
    logo_x = (WIDTH - 250) // 2  # Center horizontally
    logo_y = 80  # Below title
    screen.blit(scaled_logo, (logo_x, logo_y))

    # Instructions start below the logo
    instructions = [
        "How to Play:",
        "- Move the basket using LEFT and RIGHT arrow keys",
        "- Catch the falling objects to score points",
        "- Don't miss any object or it's game over",
        "",
        "Press the START button below to begin!"
    ]

    start_y = logo_y + 250 + 20  # 250px logo + 20px spacing
    left_padding = 40
    line_height = 35

    for i, line in enumerate(instructions):
        draw_text(screen, line, left_padding, start_y + i * line_height, font_text)

    # Draw Start button
    button_width = 200
    button_height = 60
    button_x = (WIDTH - button_width) // 2
    button_y = HEIGHT - 120
    button_rect = pygame.Rect(button_x, button_y, button_width, button_height)
    pygame.draw.rect(screen, BASKET_COLOR, button_rect)

    # Center START text in the button
    start_text = "START"
    text_x = button_rect.x + (button_width - font_button.size(start_text)[0]) // 2
    text_y = button_rect.y + (button_height - font_button.get_height()) // 2
    draw_text(screen, start_text, text_x, text_y, font_button)

    return button_rect




def main():
    running = True
    game_started = False
    basket = Basket()
    objects = []
    spawn_timer = 0
    spawn_delay = 30
    fall_speed = OBJ_FALL_SPEED_START
    score = 0
    game_over = False

    while running:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if not game_started:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if start_button.collidepoint(event.pos):
                        game_started = True
                        # Reset game variables on start
                        basket = Basket()
                        objects = []
                        spawn_timer = 0
                        spawn_delay = 30
                        fall_speed = OBJ_FALL_SPEED_START
                        score = 0
                        game_over = False

            else:  # Game running
                if game_over and event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        # Reset game
                        basket = Basket()
                        objects = []
                        spawn_timer = 0
                        spawn_delay = 30
                        fall_speed = OBJ_FALL_SPEED_START
                        score = 0
                        game_over = False

        if not game_started:
            start_button = draw_start_screen()

        else:
            screen.fill(BG_COLOR)

            keys = pygame.key.get_pressed()
            if not game_over:
                if keys[pygame.K_LEFT]:
                    basket.move("left")
                if keys[pygame.K_RIGHT]:
                    basket.move("right")

                spawn_timer += 1
                if spawn_timer >= spawn_delay:
                    spawn_timer = 0
                    objects.append(FallingObject(fall_speed))

                for obj in objects[:]:
                    obj.update()
                    if obj.rect.colliderect(basket.rect):
                        objects.remove(obj)
                        score += 1
                        if score % 10 == 0:
                            fall_speed += OBJ_FALL_SPEED_INCREMENT
                            if spawn_delay > MIN_SPAWN_DELAY:
                                spawn_delay -= 1
                    elif obj.y - obj.radius > HEIGHT:
                        game_over = True

            basket.draw(screen)
            for obj in objects:
                obj.draw(screen)

            draw_text(screen, f"Score: {score}", 20, 20, font_score)

            if game_over:
                draw_text(screen, "Game Over! Press R to Restart", WIDTH // 2 - 180, HEIGHT // 2, font_text, color=(255, 100, 100))

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
