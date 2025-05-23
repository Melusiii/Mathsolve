import pygame 
import sys
import random
import time

# Initialize
pygame.init()
pygame.mixer.init()

# Screen
WIDTH, HEIGHT = 800, 600
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("🚀 Mathsolve")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (100, 100, 255)
YELLOW = (255, 255, 0)
GRAY = (150, 150, 150)

# Load assets
try:
    pygame.mixer.music.load("bg_music.mp3")
    correct_sound = pygame.mixer.Sound("correct.wav")
    wrong_sound = pygame.mixer.Sound("wrong.wav")
except:
    print("Missing assets! Place bg_music.mp3, correct.wav, wrong.wav in the same folder.")
    sys.exit()

pygame.mixer.music.play(-1)

# Fonts
font = pygame.font.Font(None, 36)
big_font = pygame.font.Font(None, 72)

# Game Variables
score = 0
user_answer = ""
feedback = ""
rocket_x = 50
rocket_y = 300
lives = 3
level = 1
flash_red = False
flash_timer = 0
correct_streak = 0
max_lives = 5
particles = []

# Background
background = pygame.Surface((WIDTH, HEIGHT))
background.fill((5, 5, 25))
for _ in range(200):
    pygame.draw.circle(background, WHITE,
                       (random.randint(0, WIDTH), random.randint(0, HEIGHT)),
                       random.choice([1, 1, 1, 2]))

# Question Generator
def generate_question(level):
    max_num = 10 + level * 2
    num1 = random.randint(1, max_num)
    num2 = random.randint(1, max_num)
    op = random.choice(["+", "-", "*"])
    q = f"What is {num1} {op} {num2}?"
    a = str(eval(f"{num1}{op}{num2}"))
    return q, a

current_question, answer = generate_question(level)
start_time = time.time()
question_time_limit = 10

# Draw Text with Shadow
def draw_text(text, font, color, x, y):
    shadow = font.render(text, True, BLACK)
    window.blit(shadow, (x + 2, y + 2))
    main = font.render(text, True, color)
    window.blit(main, (x, y))

# --- Start Menu ---
menu_options = ["Start Game", "How to Play", "Quit"]
menu_index = 0
game_state = "menu"  # can be 'menu', 'playing', 'game_over', 'how_to_play'
how_to_play_text = [
    "Instructions:",
    "Type the answer to the math question and press Enter.",
    "You have limited lives, so avoid mistakes!",
    "Answer quickly before the timer runs out.",
    "Press B to go back to the menu."
]

running = True
game_over = False

while running:
    current_time = time.time()
    elapsed = current_time - start_time

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if game_state == "menu":
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    menu_index = (menu_index - 1) % len(menu_options)
                elif event.key == pygame.K_DOWN:
                    menu_index = (menu_index + 1) % len(menu_options)
                elif event.key == pygame.K_RETURN:
                    selected = menu_options[menu_index]
                    if selected == "Start Game":
                        score = 0
                        lives = 3
                        rocket_x = 50
                        user_answer = ""
                        feedback = ""
                        correct_streak = 0
                        current_question, answer = generate_question(1)
                        start_time = current_time
                        level = 1
                        game_over = False
                        game_state = "playing"
                    elif selected == "How to Play":
                        game_state = "how_to_play"
                    elif selected == "Quit":
                        running = False

        elif game_state == "how_to_play":
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_b:
                    game_state = "menu"

        elif game_state == "playing" and not game_over:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if user_answer == answer:
                        correct_sound.play()
                        feedback = "✅ Correct! +10 points"
                        score += 10
                        rocket_x = min(rocket_x + 50, WIDTH - 100)
                        correct_streak += 1

                        for _ in range(15):
                            particles.append({
                                'x': rocket_x + 40,
                                'y': rocket_y + 15,
                                'dx': random.uniform(-3, 3),
                                'dy': random.uniform(-5, 0),
                                'life': 30,
                                'color': (random.randint(200, 255), random.randint(100, 200), 0)
                            })

                        if correct_streak == 5:
                            if lives < max_lives:
                                lives += 1
                                feedback += " ❤️ +1 Life!"
                            correct_streak = 0
                    else:
                        wrong_sound.play()
                        feedback = "❌ Incorrect!"
                        lives -= 1
                        correct_streak = 0
                        flash_red = True
                        flash_timer = current_time

                    user_answer = ""
                    current_question, answer = generate_question(level)
                    start_time = current_time

                elif event.key == pygame.K_BACKSPACE:
                    user_answer = user_answer[:-1]
                elif event.unicode.isnumeric() or event.unicode in ["-", "."]:
                    user_answer += event.unicode

        elif game_state == "game_over":
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    score = 0
                    lives = 3
                    rocket_x = 50
                    user_answer = ""
                    feedback = ""
                    correct_streak = 0
                    current_question, answer = generate_question(1)
                    start_time = current_time
                    level = 1
                    game_over = False
                    game_state = "playing"
                elif event.key == pygame.K_q:
                    running = False

    # Time limit check (only deduct life, don't end game)
    if game_state == "playing" and elapsed > question_time_limit and not game_over:
        wrong_sound.play()
        feedback = "⏰ Time's up!"
        lives -= 1
        correct_streak = 0
        flash_red = True
        flash_timer = current_time
        user_answer = ""
        current_question, answer = generate_question(level)
        start_time = current_time

    # Lives check (only end game when lives reach 0)
    if lives <= 0 and not game_over and game_state == "playing":
        game_over = True
        final_score = score
        game_state = "game_over"

    window.fill((5, 5, 25))

    if game_state == "menu":
        draw_text("🚀 Mathsolve", big_font, WHITE, 250, 150)
        for i, option in enumerate(menu_options):
            color = YELLOW if i == menu_index else WHITE
            draw_text(option, font, color, 350, 300 + i * 50)
        draw_text("Use UP/DOWN keys and ENTER to select", font, GRAY, 220, 500)

    elif game_state == "how_to_play":
        y_offset = 150
        for line in how_to_play_text:
            draw_text(line, font, WHITE, 50, y_offset)
            y_offset += 40
        draw_text("Press B to go back", font, GRAY, 50, y_offset + 20)

    elif game_state == "playing":
        window.blit(background, (0, 0))

        for _ in range(3):
            if random.random() < 0.01:
                x, y = random.randint(0, WIDTH), random.randint(0, HEIGHT)
                pygame.draw.circle(window, (200, 200, 255), (x, y), 2)

        for i in range(3, 0, -1):
            pygame.draw.circle(window, (0, 50 + i * 20, 0), (700, 300), 30 + i * 5)
        pygame.draw.circle(window, GREEN, (700, 300), 30)

        for p in particles[:]:
            pygame.draw.circle(window, p['color'], (int(p['x']), int(p['y'])), 2)
            p['x'] += p['dx']
            p['y'] += p['dy']
            p['life'] -= 1
            if p['life'] <= 0:
                particles.remove(p)

        pygame.draw.polygon(window, WHITE, [
            (rocket_x, rocket_y + 15),
            (rocket_x + 40, rocket_y),
            (rocket_x + 50, rocket_y + 15),
            (rocket_x + 40, rocket_y + 30)
        ])
        pygame.draw.rect(window, (200, 200, 255), (rocket_x + 10, rocket_y + 5, 20, 20))

        flame_size = abs(int((current_time * 10) % 6) - 3) + 5
        pygame.draw.polygon(window, (255, flame_size * 20, 0), [
            (rocket_x, rocket_y + 10),
            (rocket_x - flame_size, rocket_y + 15),
            (rocket_x, rocket_y + 20)
        ])

        if flash_red and current_time - flash_timer < 0.3:
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill((255, 0, 0, 50))
            window.blit(overlay, (0, 0))
        else:
            flash_red = False

        draw_text(current_question, font, WHITE, 50, 50)
        draw_text(f"Answer: {user_answer}", font, WHITE, 50, 100)

        if "Correct" in feedback:
            size = int(36 + abs((current_time * 10) % 8 - 4))
            fb_font = pygame.font.Font(None, size)
            draw_text(feedback, fb_font, GREEN, 50, 150)
        else:
            draw_text(feedback, font, RED, 50, 150)

        draw_text(f"Score: {score}", font, YELLOW, 600, 50)
        draw_text(f"Lives: {lives}", font, RED, 600, 100)
        draw_text(f"Level: {level}", font, WHITE, 600, 150)
        draw_text(f"Streak: {correct_streak}/5", font, GREEN, 600, 200)

        pygame.draw.rect(window, (50, 50, 50), (50, 180, 200, 10))
        pygame.draw.rect(window, BLUE, (50, 180, 200 * (1 - elapsed / question_time_limit), 10))

        level = score // 50 + 1
        question_time_limit = max(3, 10 - level)

    elif game_state == "game_over":
        draw_text("GAME OVER", big_font, RED, 200, 200)
        draw_text(f"Final Score: {final_score}", font, WHITE, 300, 300)
        draw_text("Press R to Restart | Q to Quit", font, WHITE, 220, 400)

    for y in range(0, HEIGHT, 4):
        pygame.draw.line(window, (0, 0, 0, 30), (0, y), (WIDTH, y), 1)

    pygame.display.flip()

pygame.quit()
sys.exit()