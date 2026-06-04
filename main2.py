import pygame
import random
import math

pygame.init()

WIDTH, HEIGHT = 720, 400
SCREEN_WIDTH, SCREEN_HEIGHT = 720, 600

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("EEG Art Installation")

clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 20)
small_font = pygame.font.SysFont("Arial", 14)
big_font = pygame.font.SysFont("Arial", 28, bold=True)

time_value = 0
current_mode = "focus"

mode_info = {
    "focus": {
        "background": (5, 5, 16),
        "colors": [(91, 158, 247), (249, 123, 91), (255, 255, 255), (167, 139, 250)],
        "label": "Focus"
    },
    "relax": {
        "background": (5, 15, 8),
        "colors": [(123, 224, 165), (91, 200, 224), (181, 247, 200), (212, 240, 255)],
        "label": "Relax"
    },
    "meditation": {
        "background": (10, 5, 16),
        "colors": [(196, 160, 245), (240, 196, 245), (123, 91, 247), (255, 183, 232)],
        "label": "Meditation"
    }
}

buttons = {
    "focus": pygame.Rect(170, 535, 110, 35),
    "relax": pygame.Rect(305, 535, 110, 35),
    "meditation": pygame.Rect(440, 535, 130, 35)
}

shapes = []


def create_shapes():
    for _ in range(20):
        shapes.append({
            "x": random.random() * WIDTH,
            "y": random.random() * HEIGHT,
            "radius": 10 + random.random() * 55,
            "speed_x": (random.random() - 0.5) * 0.7,
            "speed_y": (random.random() - 0.5) * 0.7,
            "phase": random.random() * math.pi * 2,
            "type": random.randint(0, 2)
        })


def calculate_waves():
    def noise(freq):
        return (
            math.sin(time_value * freq) * 0.5 +
            math.sin(time_value * freq * 1.3 + 1) * 0.3 +
            math.sin(time_value * freq * 0.7 + 2) * 0.2
        )

    if current_mode == "focus":
        alpha = 0.3 + noise(0.4) * 0.15
        beta = 0.7 + noise(1.1) * 0.2
        theta = 0.2 + noise(0.3) * 0.1

    elif current_mode == "relax":
        alpha = 0.75 + noise(0.3) * 0.15
        beta = 0.25 + noise(0.9) * 0.1
        theta = 0.35 + noise(0.5) * 0.15

    else:
        alpha = 0.5 + noise(0.2) * 0.1
        beta = 0.15 + noise(0.7) * 0.08
        theta = 0.85 + noise(0.4) * 0.1

    return {
        "alpha": max(0, min(1, alpha)),
        "beta": max(0, min(1, beta)),
        "theta": max(0, min(1, theta))
    }


def draw_shape(surface, x, y, radius, shape_type, color, opacity):
    temp = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    color_with_alpha = (*color, int(opacity * 255))

    if shape_type == 0:
        pygame.draw.circle(temp, color_with_alpha, (int(x), int(y)), int(radius))

    elif shape_type == 1:
        points = [
            (x, y - radius),
            (x + radius * 0.866, y + radius * 0.5),
            (x - radius * 0.866, y + radius * 0.5)
        ]
        pygame.draw.polygon(temp, color_with_alpha, points)

    else:
        rect = pygame.Rect(
            x - radius * 0.7,
            y - radius * 0.7,
            radius * 1.4,
            radius * 1.4
        )
        pygame.draw.rect(temp, color_with_alpha, rect)

    surface.blit(temp, (0, 0))


def draw_wave_line(surface, waves, mode):
    points = []

    for x in range(WIDTH):
        ratio = x / WIDTH
        y = HEIGHT - 28
        y += math.sin(ratio * 18 + time_value * 5) * 8 * waves["alpha"]
        y += math.sin(ratio * 33 + time_value * 9) * 5 * waves["beta"]
        y += math.sin(ratio * 9 + time_value * 3) * 12 * waves["theta"]
        points.append((x, int(y)))

    pygame.draw.lines(surface, mode["colors"][0], False, points, 2)


def draw_text(text, x, y, color=(255, 255, 255), used_font=None):
    if used_font is None:
        used_font = font

    img = used_font.render(text, True, color)
    screen.blit(img, (x, y))


def draw_buttons():
    for mode_name, rect in buttons.items():
        if current_mode == mode_name:
            button_color = (42, 26, 78)
            border_color = (123, 91, 247)
        else:
            button_color = (26, 26, 46)
            border_color = (85, 85, 85)

        pygame.draw.rect(screen, button_color, rect, border_radius=6)
        pygame.draw.rect(screen, border_color, rect, 2, border_radius=6)

        text = mode_info[mode_name]["label"]
        text_img = small_font.render(text, True, (255, 255, 255))
        text_rect = text_img.get_rect(center=rect.center)
        screen.blit(text_img, text_rect)


def draw_ui(waves, mode):
    pygame.draw.rect(screen, (26, 26, 46), (0, 0, SCREEN_WIDTH, 55))

    draw_text("EEG Art Installation", 20, 15)
    draw_text(f"Mode: {mode['label']}", 560, 17, (180, 180, 180), small_font)

    y = 430

    draw_text("Alpha Wave", 80, y, (180, 180, 180), small_font)
    draw_text(f"{waves['alpha']:.2f}", 95, y + 22, (91, 158, 247), big_font)

    draw_text("Beta Wave", 310, y, (180, 180, 180), small_font)
    draw_text(f"{waves['beta']:.2f}", 320, y + 22, (249, 123, 91), big_font)

    draw_text("Theta Wave", 535, y, (180, 180, 180), small_font)
    draw_text(f"{waves['theta']:.2f}", 545, y + 22, (123, 224, 165), big_font)

    draw_buttons()


create_shapes()

running = True

while running:
    clock.tick(60)
    time_value += 0.018

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()

            for mode_name, rect in buttons.items():
                if rect.collidepoint(mouse_pos):
                    current_mode = mode_name

    waves = calculate_waves()
    mode = mode_info[current_mode]

    screen.fill((13, 13, 13))

    canvas_surface = pygame.Surface((WIDTH, HEIGHT))
    canvas_surface.fill(mode["background"])

    for index, shape in enumerate(shapes):
        shape["x"] += shape["speed_x"] * (0.5 + waves["beta"] * 1.5)
        shape["y"] += shape["speed_y"] * (0.5 + waves["beta"] * 1.5)

        if shape["x"] < -120:
            shape["x"] = WIDTH + 80
        if shape["x"] > WIDTH + 120:
            shape["x"] = -80
        if shape["y"] < -120:
            shape["y"] = HEIGHT + 80
        if shape["y"] > HEIGHT + 120:
            shape["y"] = -80

        pulse = math.sin(time_value * 1.5 + shape["phase"]) * 0.3 + 0.7
        size = shape["radius"] * (0.6 + waves["alpha"] * 0.8) * pulse
        opacity = 0.07 + waves["theta"] * 0.25
        color = mode["colors"][index % len(mode["colors"])]

        draw_shape(
            canvas_surface,
            shape["x"],
            shape["y"],
            size,
            shape["type"],
            color,
            opacity
        )

    draw_wave_line(canvas_surface, waves, mode)

    screen.blit(canvas_surface, (0, 55))
    draw_ui(waves, mode)

    pygame.display.flip()

pygame.quit()