import pygame
import math
import time
import random
from text import drawText
from fontDict import fonts
from particles import Tree

pygame.init()

# ---------------- Setting up the screen, assigning some global variables, and loading text fonts
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
clock = pygame.time.Clock()
fps = 60
scaleDownFactor = 5
screen_width = int(screen.get_width() / scaleDownFactor)
screen_height = int(screen.get_height() / scaleDownFactor)
screen_center = [screen_width / 2, screen_height / 2]
screen2 = pygame.Surface((screen_width, screen_height)).convert_alpha()
screenT = pygame.Surface((screen_width, screen_height)).convert_alpha()
screenT.set_alpha(100)
screenUI = pygame.Surface((screen_width, screen_height)).convert_alpha()
timer = 0
shake = [0, 0]
shake_strength = 3
montserratRegularAdaptive = fonts[f"regular{int(25 / (scaleDownFactor ** (1 / 1.5)))}"]
montserratExtralightAdaptive = fonts[f"extralight{int(25 / (scaleDownFactor ** (1 / 1.5)))}"]
montserratBoldAdaptive = fonts[f"bold{int(25 / (scaleDownFactor ** (1 / 1.5)))}"]
montserratThinAdaptive = fonts[f"thin{int(25 / (scaleDownFactor ** (1 / 1.5)))}"]


class Endesga:
    maroon_red = [87, 28, 39]
    lighter_maroon_red = [127, 36, 51]
    dark_green = [9, 26, 23]
    light_brown = [191, 111, 74]
    black = [19, 19, 19]
    grey_blue = [66, 76, 110]
    cream = [237, 171, 80]
    white = [255, 255, 255]
    greyL = [200, 200, 200]
    grey = [150, 150, 150]
    greyD = [100, 100, 100]
    greyVD = [50, 50, 50]
    very_light_blue = [199, 207, 221]
    my_blue = [32, 36, 46]
    debug_red = [255, 96, 141]
    sebastian_lague_purple = [70, 74, 124]
    sebastian_lague_light_purple = [137, 133, 181]
    network_green = [64, 128, 67]
    network_red = [127, 45, 41]


class FireCols:
    cols = [[255, 242, 157], [255, 212, 124], [255, 169, 70], [254, 128, 3], [230, 106, 37], [179, 46, 19], [126, 19, 6], [70, 2, 14]]
    colsReversed = [[70, 2, 14], [126, 19, 6], [179, 46, 19], [230, 106, 37], [254, 128, 3], [255, 169, 70], [255, 212, 124], [255, 242, 157]]


# Defining some more variables to use in the game loop
oscillating_random_thing = 0
ShakeCounter = 0
toggle = True
click = False


leafCols = [(40, 77, 103), (59, 96, 98), (77, 110, 100), (93, 125, 104)]


def spawn():
    return [Tree([(_ + 0.5) * screen_width / 3, screen_height / 2 - 35], 40, "s", leafCols, leafSize=8, sproutCountPerBush=50) for _ in range(3)] + \
            [Tree([(_ + 0.5) * screen_width / 4, screen_height / 2 + 30], 30, "s", leafCols, leafSize=7, sproutCountPerBush=40) for _ in range(4)] + \
            [Tree([(_ + 1) * screen_width / 6, screen_height / 2 + 75], 20, "s", leafCols, leafSize=6, sproutCountPerBush=15) for _ in range(5)]


trees = spawn()
gustStrength = 0.01
bushToggle = True

# ---------------- Main Game Loop
last_time = time.time()
running = True
while running:

    # ---------------- Reset Variables and Clear screens
    mx, my = pygame.mouse.get_pos()
    mx, my = mx / scaleDownFactor, my / scaleDownFactor
    screen.fill(Endesga.black)
    screen2.fill(Endesga.black)
    screenT.fill((0, 0, 0, 0))
    screenUI.fill((0, 0, 0, 0))
    dt = time.time() - last_time
    dt *= fps
    last_time = time.time()
    timer -= 1 * dt
    shake = [0, 0]
    oscillating_random_thing += math.pi / fps * dt

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            click = True
        if event.type == pygame.MOUSEBUTTONUP:
            click = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            if event.key == pygame.K_SPACE:
                toggle = not toggle
            if event.key == pygame.K_w:
                gustStrength = 0.1
            if event.key == pygame.K_s:
                trees = spawn()
            if event.key == pygame.K_t:
                bushToggle = not bushToggle
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_w:
                gustStrength = 0.01

    for tree in trees:
        tree.update(dt, gustStrength)
        tree.draw(screen2, bushToggle, not bushToggle)

    # ---------------- Updating Screen
    if toggle:
        items = {"KYBD : w, s, t": None,
                 round(clock.get_fps()): None,
                 }
        for i, label in enumerate(items.keys()):
            string = str(label)
            if items[label] is not None:
                string = f"{items[label]}: " + string
            drawText(screenUI, Endesga.debug_red, montserratRegularAdaptive, 5, screen_height - (30 + 25 * i) / (scaleDownFactor ** (1 / 1.8)), string, Endesga.black, int(3 / scaleDownFactor) + int(3 / scaleDownFactor) < 1, antiAliasing=False)
        pygame.mouse.set_visible(False)
        pygame.draw.circle(screenUI, Endesga.black, (mx + 1, my + 1), 2, 1)
        pygame.draw.circle(screenUI, Endesga.white, (mx, my), 2, 1)
    screen.blit(pygame.transform.scale(screen2, (screen_width * scaleDownFactor, screen_height * scaleDownFactor)), (shake[0], shake[1]))
    screen.blit(pygame.transform.scale(screenT, (screen_width * scaleDownFactor, screen_height * scaleDownFactor)), (shake[0], shake[1]))
    screen.blit(pygame.transform.scale(screenUI, (screen_width * scaleDownFactor, screen_height * scaleDownFactor)), (0, 0))
    pygame.display.update()
    clock.tick(fps)
