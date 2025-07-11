import pygame
from spritesheet import SpriteSheet

BLACK = (0, 0, 0) # Color key to remove black background from sprites

class Dino(pygame.sprite.Sprite):

    # Animation states: maps to index in animation list
    IDLE, RUN, JUMP, HURT, CROUCH = range(5)
    # Number of frames for each animation in the sprite sheet
    animation_steps = [4, 6, 3, 4, 7]  # idle, run, jump, hurt, crouch

    def __init__(self, x, ground_y, scroll_speed):
        super().__init__()

        # Load the full sprite sheet image for animations
        sprite_sheet_image = pygame.image.load("Assets/images/doux.png").convert_alpha()
        self.sheet = SpriteSheet(sprite_sheet_image)

        #
        self.animation_list = []
        frame_index = 0  # Tracks current frame number in sprite sheet
        # Loop through each action's frame count and extract those frames
        for animation in self.animation_steps:
            temp = []  # Temporary list for one action
            for _ in range(animation):
                # Extract frame using SpriteSheet helper
                temp.append(self.sheet.get_image(frame_index, 24, 24, 3, BLACK))
                frame_index += 1  # Move to next frame in sheet
            self.animation_list.append(temp)  # Add completed animation to main list

        # Animation control
        self.action = self.IDLE  # Start with idle animation
        self.frame = 0  # Current frame index within animation
        self.last_update = pygame.time.get_ticks()  # Time of last frame switch
        self.animation_cooldown = 100  # Time (ms) between animation frames

        # Starting image and rect (used for position and collisions)
        self.image = self.animation_list[self.action][self.frame]
        self.rect = self.image.get_rect()
        self.world_x = x  # Dino's position in the game world (not screen-relative)
        self.rect.bottom = ground_y  # Place on top of the ground
        self.ground_y = ground_y  # Store ground level for jump/gravity checks

        # Jumping and gravity mechanics
        self.vel_y = 0  # Vertical velocity
        self.gravity = 0.6  # Downward acceleration
        self.jump_vel = -12  # Upward force when jumping
        self.on_ground = True  # True if character is on the ground
        self.jump_count = 0  # Number of jumps made (used for double jump)

        # Scroll speed: used for syncing with background and movement
        self.scroll_speed = scroll_speed

    def update(self, keys):
        prev_action = self.action  # Track previous state to reset frame if it changes

        # --- Animation State Logic ---
        if not self.on_ground:
            self.action = self.JUMP
            self.world_x += self.scroll_speed  # Keep Dino moving in mid-air
        elif keys[pygame.K_DOWN]:
            self.action = self.CROUCH
            self.world_x += self.scroll_speed  # Move forward while crouching
        else:
            self.action = self.RUN
            self.world_x += self.scroll_speed  # Default running state

        # If action changed (e.g., from RUN → JUMP), reset the frame counter
        if self.action != prev_action:
            self.frame = 0

        self.apply_gravity()  # Apply gravity
        self.update_animation()  # Advance the sprite frame

    def jump(self):
        if self.jump_count < 2:  # Allow double jump (2 max)
            self.vel_y = self.jump_vel  # Apply upward velocity
            self.on_ground = False  # Mark as airborne
            self.jump_count += 1  # Track how many jumps used

    def draw(self, surface, scroll):
        # Convert world position to screen position
        screen_x = self.world_x - scroll
        # Draw the current sprite frame at that screen position
        surface.blit(self.image, (screen_x, self.rect.y))

    def apply_gravity(self):
        self.vel_y += self.gravity  # Accelerate downward
        self.rect.y += self.vel_y  # Apply velocity to vertical position

        # Check if Dino hits the ground
        if self.rect.bottom >= self.ground_y:
            self.rect.bottom = self.ground_y  # Stick to ground
            self.vel_y = 0  # Stop falling
            self.on_ground = True  # Mark as grounded
            self.jump_count = 0  # Reset jump count

    def update_animation(self):
        current_time = pygame.time.get_ticks()  # Get current time in ms
        if current_time - self.last_update >= self.animation_cooldown:
            # Advance to next frame in animation loop
            self.frame = (self.frame + 1) % len(self.animation_list[self.action])
            self.last_update = current_time  # Reset timer
        self.image = self.animation_list[self.action][self.frame]  # Update sprite





