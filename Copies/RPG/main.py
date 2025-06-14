import pygame
import button
from damagetext import DamageText
from fighter import Fighter
from healthbar import HealthBar

# -----------------------
# Game Configuration
# -----------------------
BOTTOM_PANEL = 150
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 400 + BOTTOM_PANEL
FPS = 60

# -----------------------
# Initializations
# -----------------------
pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Battle")

# Define game variables
current_fighter = 1
total_fighters = 3
action_cooldown = 0
action_wait_time = 90
attack = False
potion = False
potion_effect = 15
clicked = False

# Define fonts
font = pygame.font.SysFont('Times New Roman', 26)

# Define colors
red = (255, 0, 0)
green = (0, 255, 0)

# Load images
background_img = pygame.image.load('img/Background/background.png').convert_alpha()
panel_img = pygame.image.load('img/Icons/panel.png').convert_alpha()
sword_img = pygame.image.load('img/Icons/sword.png').convert_alpha()
potion_img = pygame.image.load('img/Icons/potion.png').convert_alpha()


# -----------------------
# Helper Functions
# -----------------------

def draw_text(text, font, text_color, x, y):
    image = font.render(text, True, text_color)
    screen.blit(image, (x, y))

def draw_bg():
    screen.blit(background_img, (0, 0))

def draw_panel():
    screen.blit(panel_img, (0, SCREEN_HEIGHT - BOTTOM_PANEL))
    # show knight's  stats
    draw_text(f'{knight.name} HP: {knight.hp}', font, red, 100, SCREEN_HEIGHT - BOTTOM_PANEL + 10)
    # show bandit's stats
    for count, i in enumerate(bandit_list):
        # show name and health
        draw_text(f'{i.name} HP: {i.hp}', font, red, 550, (SCREEN_HEIGHT - BOTTOM_PANEL + 10) + count * 60)


# -----------------------
# Game Objects
# -----------------------

# Groups
damage_text_group = pygame.sprite.Group()

# Fighters
knight = Fighter(200, 260, 'Knight', 30, 10, 3)
bandit1 = Fighter(550, 270, 'Bandit', 20, 6, 1)
bandit2 = Fighter(700, 270, 'Bandit', 20, 6, 1)
bandit_list = [bandit1, bandit2]

# Health Bars
knight_health_bar = HealthBar(100, SCREEN_HEIGHT - BOTTOM_PANEL + 40, knight.hp, knight.max_hp)
bandit1_health_bar = HealthBar(550, SCREEN_HEIGHT - BOTTOM_PANEL + 40, bandit1.hp, bandit1.max_hp)
bandit2_health_bar = HealthBar(550, SCREEN_HEIGHT - BOTTOM_PANEL + 100, bandit2.hp, bandit2.max_hp)

# Potion Buttons
potion_button = button.Button(screen, 100, SCREEN_HEIGHT - BOTTOM_PANEL + 70, potion_img, 64, 64)

# -----------------------
# Game Loop
# -----------------------
run = True
while run:

    clock.tick(FPS)

    # Draw onto screen
    draw_bg()
    draw_panel()

    # Draw text onto panel
    knight_health_bar.draw(screen, knight.hp, red, green)
    bandit1_health_bar.draw(screen, bandit1.hp , red, green)
    bandit2_health_bar.draw(screen, bandit2.hp, red, green)

    # Draw fighters
    knight.update()
    knight.draw(screen)
    for bandit in bandit_list:
        bandit.update()
        bandit.draw(screen)

    # draw the damage text
    damage_text_group.update()
    damage_text_group.draw(screen)


    # Control Player Actions
    # Reset action variables
    attack = False
    potion = False
    target = None
    # make sure mouse is visible
    pygame.mouse.set_visible(True)
    pos = pygame.mouse.get_pos()
    for count, bandit in enumerate(bandit_list):
        if bandit.rect.collidepoint(pos):
            # hide mouse
            pygame.mouse.set_visible(False)
            # show sword in place of mouse cursor
            screen.blit(sword_img, pos)
            if clicked:
                attack = True
                target = bandit_list[count]

    if potion_button.draw():
        potion = True
    # show number of potions remaining
    draw_text(str(knight.potions), font, red, 150, SCREEN_HEIGHT - BOTTOM_PANEL + 70)


    # Player action
    if knight.alive:
        if current_fighter == 1:
            action_cooldown += 1
            if action_cooldown >= action_wait_time:
                # look for player action
                # attack
                if attack and target is not None:
                    knight.attack(target, red, font, damage_text_group)
                    current_fighter += 1
                    action_cooldown = 0
                # potion
                if potion:
                    if knight.potions > 0:
                        # check if potion would heal beyond max health
                        if knight.max_hp - knight.hp > potion_effect:
                            heal_amount = potion_effect
                        else:
                            heal_amount = knight.max_hp - knight.hp
                        knight.hp += heal_amount
                        knight.potions -= 1
                        damage_text = DamageText(knight.rect.centerx, knight.rect.y, str(heal_amount), green, font)
                        damage_text_group.add(damage_text)
                        current_fighter += 1
                        action_cooldown = 0


    # Enemy Action
    for count, bandit in enumerate(bandit_list):
        if current_fighter == 2 + count:
            if bandit.alive:
                action_cooldown += 1
                if action_cooldown >= action_wait_time:
                    # check if bandit to heal first
                    if (bandit.hp / bandit.max_hp) < 0.5 and bandit.potions > 0:
                        # check if potion would heal beyond max health
                        if bandit.max_hp - bandit.hp > potion_effect:
                            heal_amount = potion_effect
                        else:
                            heal_amount = bandit.max_hp - bandit.hp
                        bandit.hp += heal_amount
                        bandit.potions -= 1
                        damage_text = DamageText(bandit.rect.centerx, bandit.rect.y, str(heal_amount), green, font)
                        damage_text_group.add(damage_text)
                        current_fighter += 1
                        action_cooldown = 0
                    # attack
                    else:
                        bandit.attack(knight, red, font, damage_text_group)
                        current_fighter += 1
                        action_cooldown = 0
            else:
                current_fighter += 1

    # if all fighter had a turn then reset
    if current_fighter > total_fighters:
        current_fighter = 1

    # Event Handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            clicked = True
        else:
            clicked = False


    pygame.display.update()
pygame.quit()